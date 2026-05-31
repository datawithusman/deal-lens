"""
DealLens Backend Configuration
Loads environment variables and provides settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # App
    APP_NAME: str = "DealLens API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./deallens.db")

    # JWT Auth
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-this-to-a-secure-secret-key-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # GLM-5.1 (Z.ai)
    GLM_API_KEY: str = os.getenv("GLM_API_KEY", "")
    GLM_BASE_URL: str = "https://open.bigmodel.cn/api/paas/v4/"
    GLM_MODEL: str = "glm-5.1"

    # OpenAI GPT-4 Fallback
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")

    # CORS
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))

    # Scraping
    SCRAPER_TIMEOUT: int = 15
    SCRAPER_MAX_CHARS: int = 5000

    # LLM Settings
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 2500


settings = Settings()