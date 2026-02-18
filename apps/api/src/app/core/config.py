"""Application configuration using Pydantic settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the API root directory (apps/api/)
API_ROOT = Path(__file__).parent.parent.parent.parent
ENV_FILE = API_ROOT / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str
    database_echo: bool = False

    # Application
    app_env: str = "development"
    app_name: str = "Budgify"
    log_level: str = "INFO"
    api_prefix: str = "/api"

    # Security (placeholders for Phase 2+)
    platform_admin_key: str
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()
