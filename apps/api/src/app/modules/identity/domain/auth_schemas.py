from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime


# Request schemas
class LoginRequest(BaseModel):
    """Login request with email, password, and tenant selection."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password")
    tenant_id: UUID = Field(..., description="Tenant to authenticate for")


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str = Field(..., min_length=32, description="Refresh token from login response")


# Response schemas
class TokenResponse(BaseModel):
    """Token response containing access and refresh tokens."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="Refresh token (opaque string)")
    token_type: str = Field(default="Bearer", description="Token type (always Bearer)")
    expires_in: int = Field(..., description="Access token expiry in seconds")


class MeResponse(BaseModel):
    """Current user information response."""
    user_id: UUID
    email: str
    username: str
    tenant_id: UUID
    roles: list[str]
    is_active: bool
    created_at: datetime


class AuthResponse(BaseModel):
    """Full authentication response (tokens + user info)."""
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user_id: UUID
    tenant_id: UUID
