"""Pydantic schemas (DTOs) for identity module."""

from app.modules.identity.schemas.admin import (
    AdminToggleActiveRequest,
    AdminUpdateUserRequest,
)
from app.modules.identity.schemas.auth import RegisterRequest, RegisterResponse
from app.modules.identity.schemas.platform import (
    CreateTenantRequest,
    CreateTenantResponse,
    InitialAdminRequest,
)

__all__ = [
    "RegisterRequest",
    "RegisterResponse",
    "CreateTenantRequest",
    "CreateTenantResponse",
    "InitialAdminRequest",
    "AdminUpdateUserRequest",
    "AdminToggleActiveRequest",
]
