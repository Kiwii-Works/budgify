"""Admin schemas (DTOs) for identity module."""

from pydantic import BaseModel


class AdminUpdateUserRequest(BaseModel):
    """Request schema for admin user update."""

    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None


class AdminToggleActiveRequest(BaseModel):
    """Request schema for toggling user active status."""

    is_active: bool
