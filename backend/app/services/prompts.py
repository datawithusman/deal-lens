"""
DealLens Prompt Engineering Service
Dynamic prompt templates that adapt to different fund profiles.
"""
import json
from typing import Optional, List


# Default K Street Capital criteria (used when no fund profile is selected)
DEFAULT_FUND_CRITERIA = {
    "fund_name": "K Street Capital",
    "target_stages": ["Seed", "Series A"],
    "target_sectors": ["FinTech", "HealthTech", "CyberSecurity", "ClimateTech", "AI", "EdTech"],
    "excluded_sectors": ["Hardware", "Biotech", "Medical Devices", "CPG", "Food and Beverage", "Weapons"],
    "valuation_range": "$5M to $15M",
    "focus": "Regulated marketplaces and high-growth technology",
}


def build_analysis_prompt(
    company_name: str,
    website_text: str = "",
    description: str = "",
    fund_criteria: Optional[dict] = None,
) -> str:
    """
    Build the analysis prompt for the LLM.
    Dynamically adjusts based on the selected fund profile.
    """
    criteria = fund_criteria or DEFAULT_FUND_CRITERIA

    # Build context section
    context_parts = []
    if description:
        context_parts.append(f"Analyst notes: {description}")
    if website_text:
        context_parts.append(f"Website content:\n{website_text}")

    context = "\n\n".join(context_parts) if context_parts else "No additional context provided."

    # Format fund criteria for the prompt
    fund_name = criteria.get("fund_name", "K Street Capital")
    target_stages = ", ".join(criteria.get("target_stages", ["Seed", "Series A"]))
    target_sectors = ", ".join(criteria.get("target_sectors", ["FinTech", "AI"]))
    excluded = ", ".join(criteria.get("excluded_sectors", []))
    valuation = criteria.get("valuation_range", "Not specified")
    focus = criteria.get("focus", "High-growth technology")

    return f"""You are evaluating a startup for {fund_name}, a venture capital firm.

{fund_name}'s investment criteria:
- Stage: {target_stages}
- Valuation range: {valuation}
- Sectors: {target_sectors}
- Focus: {focus}
- Does NOT invest in: {excluded}

Company to evaluate: {company_name}

Available context:
{context}

Produce a JSON object with exactly these fields. Be factual and analytical. If specific information is not available from the context or your training data, write "Insufficient public data available" for that field. Do not invent or fabricate facts. Use your training knowledge to fill in what you reasonably can about this company.

{{
  "one_liner": "One sentence describing what the company does in plain English, no buzzwords",
  "sector": "Single best-fit sector classification",
  "stage": "Estimated stage based on available signals (e.g., Pre-seed, Seed, Series A, Series B, Growth)",
  "problem_solution": "2-3 sentences on the core problem they solve and their approach to solving it",
  "target_market": "Who they sell to (target customer), estimated TAM if determinable, and market growth indicators",
  "business_model": "How they generate revenue (subscription, transaction fees, licensing, marketplace, etc.)",
  "team_assessment": "Founder backgrounds, relevant experience, domain expertise based on publicly available information",
  "traction_signals": "Any revenue figures, user metrics, growth rate indicators, partnerships, or milestones available publicly",
  "competitive_landscape": "Top 3-5 competitors or alternatives with brief notes on how this company differentiates",
  "regulatory_notes": "Any compliance requirements, licensing needs, or regulatory considerations relevant to their sector",
  "red_flags": "Any concerns: weak team signals, saturated market, regulatory risk, technology risk, or competitive threats. Write 'No significant red flags identified' if none found.",
  "fit_score": {{
    "sector_match": <0-25 integer, score based on alignment with {fund_name}'s sector focus>,
    "stage_match": <0-25 integer, score based on alignment with {fund_name}'s stage criteria>,
    "team_quality": <0-25 integer, score based on founder experience and domain expertise>,
    "market_size": <0-25 integer, score based on market size, growth potential, and tailwinds>,
    "total": <sum of all four scores>,
    "verdict": <"Strong Fit" if total >= 70, "Possible Fit" if total >= 40, "Weak Fit" if total < 40>
  }}
}}

Remember: Return ONLY valid JSON. No markdown code fences, no explanatory text before or after the JSON."""


def build_comparison_prompt(
    company_names: List[str],
    analyses: List[dict],
    fund_criteria: Optional[dict] = None,
) -> str:
    """
    Build a prompt for comparing multiple companies.
    Used in comparison mode.
    """
    criteria = fund_criteria or DEFAULT_FUND_CRITERIA
    fund_name = criteria.get("fund_name", "K Street Capital")

    companies_text = ""
    for i, (name, analysis) in enumerate(zip(company_names, analyses), 1):
        companies_text += f"\n--- Company {i}: {name} ---\n"
        companies_text += json.dumps(analysis, indent=2) if isinstance(analysis, dict) else str(analysis)
        companies_text += "\n"

    return f"""You are comparing startups for {fund_name}.

Here are the analyses of {len(company_names)} companies:
{companies_text}

Produce a comparative analysis as JSON:
{{
  "ranking": [
    {{"company": "name", "rank": 1, "reason": "why ranked here"}}
  ],
  "summary": "2-3 sentence overall comparison",
  "recommendation": "Which company should {fund_name} prioritize and why"
}}

Return ONLY valid JSON, no markdown."""


def get_default_kstreet_profile() -> dict:
    """Return the default K Street Capital fund profile for seeding."""
    return {
        "name": "K Street Capital (Default)",
        "fund_name": "K Street Capital",
        "target_stages": json.dumps(["Seed", "Series A"]),
        "target_sectors": json.dumps(["FinTech", "HealthTech", "CyberSecurity", "ClimateTech", "AI", "EdTech"]),
        "excluded_sectors": json.dumps(["Hardware", "Biotech", "Medical Devices", "CPG", "Food and Beverage", "Weapons"]),
        "valuation_min": 5.0,
        "valuation_max": 15.0,
        "focus_description": "Regulated marketplaces and high-growth technology",
        "is_default": True,
    }