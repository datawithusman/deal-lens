"""
DealLens Fund Profile Routes
CRUD operations for fund investment criteria profiles.
"""
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import (
    FundProfileCreate,
    FundProfileUpdate,
    FundProfileResponse,
    MessageResponse,
)
from app.models.db_models import FundProfile, User
from app.services.auth_service import get_current_user
from app.services.prompts import get_default_kstreet_profile

router = APIRouter(prefix="/profiles", tags=["Fund Profiles"])


def _profile_to_response(profile: FundProfile) -> FundProfileResponse:
    """Convert a FundProfile DB model to response schema."""
    return FundProfileResponse(
        id=profile.id,
        name=profile.name,
        description=profile.description,
        fund_name=profile.fund_name,
        target_stages=json.loads(profile.target_stages) if isinstance(profile.target_stages, str) else profile.target_stages,
        target_sectors=json.loads(profile.target_sectors) if isinstance(profile.target_sectors, str) else profile.target_sectors,
        excluded_sectors=json.loads(profile.excluded_sectors) if profile.excluded_sectors else [],
        valuation_min=profile.valuation_min,
        valuation_max=profile.valuation_max,
        focus_description=profile.focus_description,
        additional_notes=profile.additional_notes,
        is_default=bool(profile.is_default),
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


@router.get("", response_model=List[FundProfileResponse])
def list_profiles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all fund profiles for the current user."""
    profiles = db.query(FundProfile).filter(
        FundProfile.user_id == current_user.id
    ).order_by(FundProfile.is_default.desc(), FundProfile.created_at.desc()).all()

    # If no profiles exist, create the default K Street Capital profile
    if not profiles:
        default_data = get_default_kstreet_profile()
        default = FundProfile(
            user_id=current_user.id,
            **default_data,
        )
        db.add(default)
        db.commit()
        db.refresh(default)
        profiles = [default]

    return [_profile_to_response(p) for p in profiles]


@router.post("", response_model=FundProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    request: FundProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new fund profile."""
    # If this is set as default, unset other defaults
    if request.is_default:
        db.query(FundProfile).filter(
            FundProfile.user_id == current_user.id,
            FundProfile.is_default == 1,
        ).update({"is_default": 0})

    profile = FundProfile(
        user_id=current_user.id,
        name=request.name,
        description=request.description,
        fund_name=request.fund_name,
        target_stages=json.dumps(request.target_stages),
        target_sectors=json.dumps(request.target_sectors),
        excluded_sectors=json.dumps(request.excluded_sectors) if request.excluded_sectors else None,
        valuation_min=request.valuation_min,
        valuation_max=request.valuation_max,
        focus_description=request.focus_description,
        additional_notes=request.additional_notes,
        is_default=1 if request.is_default else 0,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return _profile_to_response(profile)


@router.get("/{profile_id}", response_model=FundProfileResponse)
def get_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific fund profile."""
    profile = db.query(FundProfile).filter(
        FundProfile.id == profile_id,
        FundProfile.user_id == current_user.id,
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund profile not found.",
        )

    return _profile_to_response(profile)


@router.put("/{profile_id}", response_model=FundProfileResponse)
def update_profile(
    profile_id: int,
    request: FundProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a fund profile."""
    profile = db.query(FundProfile).filter(
        FundProfile.id == profile_id,
        FundProfile.user_id == current_user.id,
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund profile not found.",
        )

    # If setting as default, unset other defaults
    if request.is_default:
        db.query(FundProfile).filter(
            FundProfile.user_id == current_user.id,
            FundProfile.is_default == 1,
            FundProfile.id != profile_id,
        ).update({"is_default": 0})

    # Update only provided fields
    update_data = request.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field in ("target_stages", "target_sectors", "excluded_sectors") and value is not None:
            value = json.dumps(value)
        if field == "is_default" and value is not None:
            value = 1 if value else 0
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return _profile_to_response(profile)


@router.delete("/{profile_id}", response_model=MessageResponse)
def delete_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a fund profile."""
    profile = db.query(FundProfile).filter(
        FundProfile.id == profile_id,
        FundProfile.user_id == current_user.id,
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund profile not found.",
        )

    if profile.is_default:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete the default profile. Set another profile as default first.",
        )

    db.delete(profile)
    db.commit()

    return MessageResponse(message="Fund profile deleted successfully.")