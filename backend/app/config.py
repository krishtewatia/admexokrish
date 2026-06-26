"""Application settings."""
import os
from pathlib import Path
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    mongodb_uri: str = Field(default="mongodb://localhost:27017")
    mongodb_db_name: str = Field(default="adh_leads_db")
    cors_origins: List[str] = Field(default=["http://localhost:5173"])
    backend_base_url: str = Field(default="http://localhost:8000")

    # Brevo (Sendinblue) email
    brevo_api_key: str = Field(default="")
    email_from_name: str = Field(default="Lead Management")
    email_from_email: str = Field(default="noreply@example.com")

    # OpenAI (optional)
    openai_api_key: str = Field(default="")

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
