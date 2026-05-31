"""
DealLens Analysis Routes
Core analysis endpoint for startup evaluation.
"""
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import AnalysisRequest, AnalysisResponse, FitScore, MessageResponse
from app.models.db_models import Analysis, FundProfile, User
from app.services.auth_service import get_current_user
from app.services.scraper import scrape_website
from app.services.analyzer import run_analysis

router = APIRouter(prefix="/analyze", tags=["Analysis"])


def _get_fund_criteria(db: Session, user_id: int, profile_id: int = None) -> dict:
    """Get fund criteria from profile or default."""
    if profile_id:
        profile = db.query(FundProfile).filter(
            FundProfile.id == profile_id,
            FundProfile.user_id == user_id,
        ).first()
        if not profile:
            return None

        return {
            "fund_name": profile.fund_name,
            "target_stages": json.loads(profile.target_stages) if isinstance(profile.target_stages, str) else profile.target_stages,
            "target_sectors": json.loads(profile.target_sectors) if isinstance(profile.target_sectors, str) else profile.target_sectors,
            "excluded_sectors": json.loads(profile.excluded_sectors) if profile.excluded_sectors else [],
            "valuation_range": f"${profile.valuation_min}M to ${profile.valuation_max}M" if profile.valuation_min and profile.valuation_max else "Not specified",
            "focus": profile.focus_description or "High-growth technology",
        }

    # Try to get user's default profile
    default_profile = db.query(FundProfile).filter(
        FundProfile.user_id == user_id,
        FundProfile.is_default == 1,
    ).first()

    if default_profile:
        return {
            "fund_name": default_profile.fund_name,
            "target_stages": json.loads(default_profile.target_stages) if isinstance(default_profile.target_stages, str) else default_profile.target_stages,
            "target_sectors": json.loads(default_profile.target_sectors) if isinstance(default_profile.target_sectors, str) else default_profile.target_sectors,
            "excluded_sectors": json.loads(default_profile.excluded_sectors) if default_profile.excluded_sectors else [],
            "valuation_range": f"${default_profile.valuation_min}M to ${default_profile.valuation_max}M" if default_profile.valuation_min and default_profile.valuation_max else "Not specified",
            "focus": default_profile.focus_description or "High-growth technology",
        }

    # Return None to use default K Street Capital criteria
    return None


@router.post("", response_model=AnalysisResponse)
async def analyze_startup(
    request: AnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Analyze a startup and generate a VC-style investment snapshot."""
    # Create analysis record
    analysis = Analysis(
        user_id=current_user.id,
        fund_profile_id=request.fund_profile_id,
        company_name=request.company_name,
        website_url=request.website_url,
        description=request.description,
        llm_provider=request.llm_provider,
        status="processing",
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    try:
        # Step 1: Scrape website if URL provided
        website_text = ""
        if request.website_url:
            website_text = await scrape_website(request.website_url)

        # Step 2: Get fund criteria
        fund_criteria = _get_fund_criteria(db, current_user.id, request.fund_profile_id)

        # Step 3: Run analysis
        result = await run_analysis(
            company_name=request.company_name,
            website_text=website_text,
            description=request.description or "",
            fund_criteria=fund_criteria,
            provider=request.llm_provider,
        )

        # Step 4: Extract metadata
        metadata = result.pop("_metadata", {})

        # Step 5: Update analysis record with results
        fit_score = result.get("fit_score", {})

        analysis.one_liner = result.get("one_liner")
        analysis.sector = result.get("sector")
        analysis.stage = result.get("stage")
        analysis.problem_solution = result.get("problem_solution")
        analysis.target_market = result.get("target_market")
        analysis.business_model = result.get("business_model")
        analysis.team_assessment = result.get("team_assessment")
        analysis.traction_signals = result.get("traction_signals")
        analysis.competitive_landscape = result.get("competitive_landscape")
        analysis.regulatory_notes = result.get("regulatory_notes")
        analysis.red_flags = result.get("red_flags")
        analysis.total_score = fit_score.get("total")
        analysis.sector_match = fit_score.get("sector_match")
        analysis.stage_match = fit_score.get("stage_match")
        analysis.team_quality = fit_score.get("team_quality")
        analysis.market_size = fit_score.get("market_size")
        analysis.verdict = fit_score.get("verdict")
        analysis.status = "completed"
        analysis.processing_time_seconds = metadata.get("processing_time_seconds")
        analysis.raw_response = metadata.get("raw_response")

        db.commit()
        db.refresh(analysis)

        return _format_analysis_response(analysis)

    except Exception as e:
        analysis.status = "failed"
        analysis.error_message = str(e)
        db.commit()
        db.refresh(analysis)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}",
        )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific analysis by ID."""
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id,
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found.",
        )

    return _format_analysis_response(analysis)


@router.post("/demo", response_model=AnalysisResponse)
async def demo_analysis(
    request: AnalysisRequest,
):
    """Demo analysis with dummy data - no API key or auth required."""
    import random
    from datetime import datetime, timezone

    company = request.company_name or "TechStart AI"
    
    demo_data = {
        "one_liner": f"{company} is an AI-powered enterprise platform that automates complex business workflows using advanced machine learning.",
        "sector": "Enterprise AI / SaaS",
        "stage": "Series A",
        "problem_solution": f"**Problem:** Enterprises spend 40% of employee time on repetitive manual data processing across disparate systems.\n\n**Solution:** {company}'s platform uses proprietary ML models to automate these workflows, reducing processing time by 85% and error rates by 95%.",
        "target_market": "**TAM:** $45B global enterprise automation market\n**SAM:** $12B AI-first workflow automation\n**SOM:** $800M initial target in financial services & healthcare\n\nKey verticals: Financial Services, Healthcare, Legal, Insurance.",
        "business_model": "**Revenue Model:** B2B SaaS subscription\n- **Starter:** $2,500/mo (up to 10 workflows)\n- **Growth:** $8,000/mo (up to 50 workflows + priority support)\n- **Enterprise:** Custom pricing (unlimited + dedicated CSM)\n\n**Gross Margin:** ~78%\n**Net Revenue Retention:** 135%\n**LTV:CAC:** 5.2x",
        "team_assessment": "✅ **CEO:** Ex-Google Brain researcher, PhD in ML from Stanford\n✅ **CTO:** Built AWS Lambda's inference pipeline\n✅ **VP Sales:** Former VP at Salesforce (grew ARR from $5M to $50M)\n⚠️ **Gap:** No dedicated CFO yet\n\nOverall: Strong technical founding team with relevant domain expertise.",
        "traction_signals": "- 📈 **ARR:** $2.8M (growing 15% MoM)\n- 👥 **Customers:** 42 enterprise clients including 3 Fortune 500\n- 💰 **Net Revenue Retention:** 135%\n- 🏆 Won 'Best AI Product' at Enterprise Connect 2024\n- 📊 99.97% platform uptime SLA achieved\n- 🔄 89% of customers expanded contracts within 6 months",
        "competitive_landscape": "| Competitor | Strength | Weakness |\n|------------|----------|----------|\n| UiPath | Market leader, strong brand | Legacy architecture, expensive |\n| Automation Anywhere | Large customer base | Complex deployment |\n| **" + company + "** | AI-native, faster ROI | Smaller, less brand recognition |\n\n**Moat:** Proprietary ML models trained on 50M+ workflow patterns. 18-month data advantage.",
        "regulatory_notes": "- SOC 2 Type II certified ✅\n- GDPR compliant ✅\n- HIPAA ready (BAA available) ✅\n- No significant regulatory risk identified\n- AI governance framework in place for EU AI Act compliance",
        "red_flags": "⚠️ **Concentration Risk:** Top 3 customers = 35% of ARR\n⚠️ **Burn Rate:** $180K/mo operating expenses, 18 months runway\n⚠️ **Key Person:** Heavy reliance on CTO for ML model maintenance\n⚠️ **Competitive:** Microsoft and Google investing heavily in this space",
    }

    fit_score = FitScore(
        total=round(random.uniform(72, 85), 1),
        sector_match=round(random.uniform(80, 95), 1),
        stage_match=round(random.uniform(70, 90), 1),
        team_quality=round(random.uniform(75, 92), 1),
        market_size=round(random.uniform(78, 88), 1),
        verdict="Strong Fit",
    )

    return AnalysisResponse(
        id=0,
        company_name=company,
        **demo_data,
        fit_score=fit_score,
        llm_provider="demo",
        status="completed",
        processing_time_seconds=0.8,
        created_at=datetime.now(timezone.utc),
    )


@router.delete("/{analysis_id}", response_model=MessageResponse)
def delete_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a specific analysis."""
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id,
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found.",
        )

    db.delete(analysis)
    db.commit()

    return MessageResponse(message="Analysis deleted successfully.")


def _format_analysis_response(analysis: Analysis) -> AnalysisResponse:
    """Format a database Analysis record into API response."""
    fit_score = None
    if analysis.total_score is not None:
        fit_score = FitScore(
            total=analysis.total_score,
            sector_match=analysis.sector_match or 0,
            stage_match=analysis.stage_match or 0,
            team_quality=analysis.team_quality or 0,
            market_size=analysis.market_size or 0,
            verdict=analysis.verdict or "Weak Fit",
        )

    return AnalysisResponse(
        id=analysis.id,
        company_name=analysis.company_name,
        one_liner=analysis.one_liner,
        sector=analysis.sector,
        stage=analysis.stage,
        problem_solution=analysis.problem_solution,
        target_market=analysis.target_market,
        business_model=analysis.business_model,
        team_assessment=analysis.team_assessment,
        traction_signals=analysis.traction_signals,
        competitive_landscape=analysis.competitive_landscape,
        regulatory_notes=analysis.regulatory_notes,
        red_flags=analysis.red_flags,
        fit_score=fit_score,
        llm_provider=analysis.llm_provider,
        status=analysis.status,
        processing_time_seconds=analysis.processing_time_seconds,
        created_at=analysis.created_at,
    )