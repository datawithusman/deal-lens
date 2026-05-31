"""
DealLens Analyzer Service
Core analysis engine supporting GLM-5.1 and OpenAI GPT-4.
"""
import json
import time
from typing import Optional

from openai import AsyncOpenAI
from loguru import logger

from app.config import settings
from app.services.prompts import build_analysis_prompt


# System prompt for the LLM
SYSTEM_PROMPT = (
    "You are a senior venture capital analyst with 15+ years of experience. "
    "You produce structured, factual, and insightful startup assessments. "
    "You respond only in valid JSON. No markdown formatting, no preamble, no commentary."
)


def _get_client(provider: str = "glm") -> AsyncOpenAI:
    """Get the appropriate OpenAI client based on provider."""
    if provider == "openai":
        return AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
        )
    else:  # glm (default)
        return AsyncOpenAI(
            api_key=settings.GLM_API_KEY,
            base_url=settings.GLM_BASE_URL,
        )


def _get_model(provider: str = "glm") -> str:
    """Get the model name for the provider."""
    if provider == "openai":
        return settings.OPENAI_MODEL
    return settings.GLM_MODEL


def _clean_llm_response(raw: str) -> str:
    """Clean and extract JSON from LLM response."""
    # Strip whitespace
    raw = raw.strip()

    # Remove markdown code fences if present
    if raw.startswith("```"):
        lines = raw.split("\n")
        # Remove first line (```json or ```)
        lines = lines[1:]
        # Remove last line (```)
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)

    # Try to find JSON object boundaries
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        raw = raw[start:end]

    return raw


async def run_analysis(
    company_name: str,
    website_text: str = "",
    description: str = "",
    fund_criteria: Optional[dict] = None,
    provider: str = "glm",
) -> dict:
    """
    Run startup analysis using the selected LLM provider.
    Returns parsed analysis data as a dictionary.
    """
    start_time = time.time()

    # Build the prompt
    prompt = build_analysis_prompt(
        company_name=company_name,
        website_text=website_text,
        description=description,
        fund_criteria=fund_criteria,
    )

    logger.info(f"Starting analysis for '{company_name}' using {provider}")

    # Get client and model
    client = _get_client(provider)
    model = _get_model(provider)

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )

        raw_content = response.choices[0].message.content.strip()
        logger.debug(f"Raw LLM response length: {len(raw_content)} chars")

        # Clean and parse JSON response
        cleaned = _clean_llm_response(raw_content)
        data = json.loads(cleaned)

        # Validate required fields exist
        required_fields = [
            "one_liner", "sector", "stage", "problem_solution",
            "target_market", "business_model", "team_assessment",
            "traction_signals", "competitive_landscape", "regulatory_notes",
            "red_flags", "fit_score"
        ]

        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing field in LLM response: {field}")
                if field == "fit_score":
                    data[field] = {
                        "sector_match": 0,
                        "stage_match": 0,
                        "team_quality": 0,
                        "market_size": 0,
                        "total": 0,
                        "verdict": "Weak Fit",
                    }
                else:
                    data[field] = "Insufficient public data available"

        # Validate fit_score structure
        fit = data.get("fit_score", {})
        for score_field in ["sector_match", "stage_match", "team_quality", "market_size", "total"]:
            if score_field not in fit:
                fit[score_field] = 0
        if "verdict" not in fit:
            total = fit.get("total", 0)
            fit["verdict"] = "Strong Fit" if total >= 70 else ("Possible Fit" if total >= 40 else "Weak Fit")

        data["fit_score"] = fit

        elapsed = time.time() - start_time
        data["_metadata"] = {
            "processing_time_seconds": round(elapsed, 2),
            "llm_provider": provider,
            "model": model,
            "raw_response": raw_content,
        }

        logger.info(f"Analysis completed for '{company_name}' in {elapsed:.2f}s")
        return data

    except json.JSONDecodeError as e:
        elapsed = time.time() - start_time
        logger.error(f"JSON parse error for '{company_name}': {str(e)}")
        raise Exception(f"Failed to parse LLM response as JSON: {str(e)}")

    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Analysis error for '{company_name}': {str(e)}")

        # If primary provider fails, try fallback
        if provider == "glm" and settings.OPENAI_API_KEY:
            logger.info(f"Attempting fallback to OpenAI for '{company_name}'")
            try:
                return await run_analysis(
                    company_name=company_name,
                    website_text=website_text,
                    description=description,
                    fund_criteria=fund_criteria,
                    provider="openai",
                )
            except Exception as fallback_err:
                logger.error(f"Fallback also failed: {str(fallback_err)}")
                raise Exception(f"Both LLM providers failed. Primary: {str(e)}, Fallback: {str(fallback_err)}")

        raise Exception(f"Analysis failed: {str(e)}")