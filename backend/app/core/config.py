"""
Centralized Application Configuration
Pydantic Settings reading environment variables for App, Database, Security, and ML paths.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Metadata
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "OIL Safety Intelligence Platform"
    APP_VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # PostgreSQL Database Connection
    DATABASE_URL: str = "postgresql://oil_admin:oil_secure_password_dev_only@postgres:5432/oil_safety_db"

    # Security Utilities Configuration
    SECRET_KEY: str = "dev_secret_key_change_in_production_f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # ML & Offline Cache Contracts
    MODEL_CACHE_DIR: str = "/app/models/cache"
    SPACY_MODEL_NAME: str = "en_core_web_sm"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """Cached singleton instance of application settings."""
    return Settings()


settings = get_settings()
