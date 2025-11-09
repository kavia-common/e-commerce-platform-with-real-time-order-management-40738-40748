import os
from functools import lru_cache
from typing import List, Optional

from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env if available
load_dotenv()


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # Auth / JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "CHANGE_ME")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # CORS
    ALLOW_ORIGINS: List[str] = (
        os.getenv("ALLOW_ORIGINS", "*").split(",") if os.getenv("ALLOW_ORIGINS") else ["*"]
    )

    # Optional Supabase verification
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_JWT_SECRET: Optional[str] = os.getenv("SUPABASE_JWT_SECRET")


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings object populated from environment variables."""
    return Settings()
