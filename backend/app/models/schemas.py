"""
DealLens Pydantic Schemas
Request/Response models for API validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ============================================================
# Auth Schemas
# ============================================================

class UserSignup(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============================================================
# Fund Profile Schemas
# ============================================================

class FundProfileCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    fund_name: str = Field(..., min_length=1, max_length=255)
    target_stages: List[str] = Field(..., min_length=1)
    target_sectors: List[str] = Field(..., min_length=1)
    excluded_sectors: Optional[List[str]] = []
    valuation_min: Optional[float] = None
    valuation_max: Optional[float] = None
    focus_description: Optional[str] = None
    additional_notes: Optional[str] = None
    is_default: bool = False


class FundProfileUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    fund_name: Optional[str] = None
    target_stages: Optional[List[str]] = None
    target_sectors: Optional[List[str]] = None
    excluded_sectors: Optional[List[str]] = None
    valuation_min: Optional[float] = None
    valuation_max: Optional[float] = None
    focus_description: Optional[str] = None
    additional_notes: Optional[str] = None
    is_default: Optional[bool] = None


class FundProfileResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    fund_name: str
    target_stages: List[str]
    target_sectors: List[str]
    excluded_sectors: Optional[List[str]]
    valuation_min: Optional[float]
    valuation_max: Optional[float]
    focus_description: Optional[str]
    additional_notes: Optional[str]
    is_default: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# Analysis Schemas
# ============================================================

class AnalysisRequest(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=255)
    website_url: Optional[str] = None
    description: Optional[str] = None
    fund_profile_id: Optional[int] = None
    llm_provider: str = Field(default="glm", pattern="^(glm|openai)$")


class FitScore(BaseModel):
    total: int = Field(..., ge=0, le=100)
    sector_match: int = Field(..., ge=0, le=25)
    stage_match: int = Field(..., ge=0, le=25)
    team_quality: int = Field(..., ge=0, le=25)
    market_size: int = Field(..., ge=0, le=25)
    verdict: str = Field(..., pattern="^(Strong Fit|Possible Fit|Weak Fit)$")


class AnalysisResponse(BaseModel):
    id: int
    company_name: str
    one_liner: Optional[str]
    sector: Optional[str]
    stage: Optional[str]
    problem_solution: Optional[str]
    target_market: Optional[str]
    business_model: Optional[str]
    team_assessment: Optional[str]
    traction_signals: Optional[str]
    competitive_landscape: Optional[str]
    regulatory_notes: Optional[str]
    red_flags: Optional[str]
    fit_score: Optional[FitScore]
    llm_provider: str
    status: str
    processing_time_seconds: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisListResponse(BaseModel):
    id: int
    company_name: str
    sector: Optional[str]
    stage: Optional[str]
    total_score: Optional[int]
    verdict: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# Generic Response
# ============================================================

class MessageResponse(BaseModel):
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    detail: str
    success: bool = False