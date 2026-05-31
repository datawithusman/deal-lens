"""
DealLens History Routes
View and manage past analyses.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import AnalysisListResponse, MessageResponse
from app.models.db_models import Analysis, User
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/history", tags=["History"])


@router.get("", response_model=List[AnalysisListResponse])
def get_analysis_history(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum records to return"),
    status_filter: str = Query(None, description="Filter by status: completed, failed, processing"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get paginated analysis history for the current user."""
    query = db.query(Analysis).filter(Analysis.user_id == current_user.id)

    if status_filter:
        query = query.filter(Analysis.status == status_filter)

    query = query.order_by(Analysis.created_at.desc())

    analyses = query.offset(skip).limit(limit).all()

    return [
        AnalysisListResponse(
            id=a.id,
            company_name=a.company_name,
            sector=a.sector,
            stage=a.stage,
            total_score=a.total_score,
            verdict=a.verdict,
            status=a.status,
            created_at=a.created_at,
        )
        for a in analyses
    ]


@router.get("/stats", tags=["Stats"])
def get_analysis_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get analysis statistics for the current user."""
    total = db.query(Analysis).filter(Analysis.user_id == current_user.id).count()
    completed = db.query(Analysis).filter(
        Analysis.user_id == current_user.id,
        Analysis.status == "completed",
    ).count()
    failed = db.query(Analysis).filter(
        Analysis.user_id == current_user.id,
        Analysis.status == "failed",
    ).count()

    # Get verdict distribution
    strong_fits = db.query(Analysis).filter(
        Analysis.user_id == current_user.id,
        Analysis.verdict == "Strong Fit",
    ).count()
    possible_fits = db.query(Analysis).filter(
        Analysis.user_id == current_user.id,
        Analysis.verdict == "Possible Fit",
    ).count()
    weak_fits = db.query(Analysis).filter(
        Analysis.user_id == current_user.id,
        Analysis.verdict == "Weak Fit",
    ).count()

    # Get top sectors analyzed
    from sqlalchemy import func
    sector_counts = (
        db.query(Analysis.sector, func.count(Analysis.id).label("count"))
        .filter(
            Analysis.user_id == current_user.id,
            Analysis.sector.isnot(None),
        )
        .group_by(Analysis.sector)
        .order_by(func.count(Analysis.id).desc())
        .limit(5)
        .all()
    )

    return {
        "total_analyses": total,
        "completed": completed,
        "failed": failed,
        "verdict_distribution": {
            "strong_fit": strong_fits,
            "possible_fit": possible_fits,
            "weak_fit": weak_fits,
        },
        "top_sectors": [
            {"sector": s, "count": c} for s, c in sector_counts if s
        ],
    }