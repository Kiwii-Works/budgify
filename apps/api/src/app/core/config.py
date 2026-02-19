"""Application configuration using Pydantic settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

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

    # Security
    platform_admin_key: str = "dev-platform-admin-key"
    secret_key: str = "dev-secret-key"
    
    # JWT Configuration
    jwt_secret_key: str = "dev-jwt-secret-key-32-chars-minimum-1234567890"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret_key(cls, v: str, info) -> str:
        """Validate JWT secret key is secure in production."""
        app_env = info.data.get("app_env", "development")
        
        if app_env == "production":
            if len(v) < 32:
                raise ValueError("JWT secret key must be at least 32 characters in production")
            if "change-in-production" in v.lower() or "your-" in v.lower():
                raise ValueError("JWT secret key contains insecure placeholder in production")
        
        return v

    @field_validator("platform_admin_key")
    @classmethod
    def validate_platform_admin_key(cls, v: str, info) -> str:
        """Validate platform admin key is set in production."""
        app_env = info.data.get("app_env", "development")
        
        if app_env == "production":
            if "change-in-production" in v.lower() or not v or len(v) < 16:
                raise ValueError("Platform admin key must be a strong value in production")
        
        return v


# Global settings instance
settings = Settings()
