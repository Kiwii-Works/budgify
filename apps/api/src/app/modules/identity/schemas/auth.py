"""Authentication schemas (DTOs) for identity module."""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Request schema for user registration."""

    username: str = Field(..., min_length=3, max_length=30)
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str = Field(..., min_length=8)


class RegisterResponse(BaseModel):
    """Response schema for user registration."""

    user_id: str
    username: str
    email: str
