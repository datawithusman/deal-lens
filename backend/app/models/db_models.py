"""
DealLens SQLAlchemy Database Models
Defines all database tables.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """User account for authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    analyses = relationship("Analysis", back_populates="user")
    fund_profiles = relationship("FundProfile", back_populates="user")


class FundProfile(Base):
    """Custom fund investment criteria profiles."""
    __tablename__ = "fund_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Investment Criteria
    fund_name = Column(String(255), nullable=False)
    target_stages = Column(Text, nullable=False)  # JSON string: ["Seed", "Series A"]
    target_sectors = Column(Text, nullable=False)  # JSON string: ["FinTech", "AI"]
    excluded_sectors = Column(Text, nullable=True)  # JSON string: ["Hardware", "Biotech"]
    valuation_min = Column(Float, nullable=True)  # In millions
    valuation_max = Column(Float, nullable=True)  # In millions
    focus_description = Column(Text, nullable=True)
    additional_notes = Column(Text, nullable=True)

    is_default = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="fund_profiles")
    analyses = relationship("Analysis", back_populates="fund_profile")


class Analysis(Base):
    """Saved analysis results."""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fund_profile_id = Column(Integer, ForeignKey("fund_profiles.id"), nullable=True)

    # Input
    company_name = Column(String(255), nullable=False)
    website_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    llm_provider = Column(String(50), default="glm")  # "glm" or "openai"

    # Output
    one_liner = Column(Text, nullable=True)
    sector = Column(String(100), nullable=True)
    stage = Column(String(100), nullable=True)
    problem_solution = Column(Text, nullable=True)
    target_market = Column(Text, nullable=True)
    business_model = Column(Text, nullable=True)
    team_assessment = Column(Text, nullable=True)
    traction_signals = Column(Text, nullable=True)
    competitive_landscape = Column(Text, nullable=True)
    regulatory_notes = Column(Text, nullable=True)
    red_flags = Column(Text, nullable=True)

    # Fit Score
    total_score = Column(Integer, nullable=True)
    sector_match = Column(Integer, nullable=True)
    stage_match = Column(Integer, nullable=True)
    team_quality = Column(Integer, nullable=True)
    market_size = Column(Integer, nullable=True)
    verdict = Column(String(50), nullable=True)

    # Metadata
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    processing_time_seconds = Column(Float, nullable=True)
    raw_response = Column(Text, nullable=True)  # Store raw LLM response

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="analyses")
    fund_profile = relationship("FundProfile", back_populates="analyses")