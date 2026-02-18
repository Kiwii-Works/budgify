"""Platform schemas (DTOs) for identity module."""

from pydantic import BaseModel, Field


class InitialAdminRequest(BaseModel):
    """Request schema for initial admin user."""

    username: str = Field(..., min_length=3, max_length=30)
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str = Field(..., min_length=8)


class CreateTenantRequest(BaseModel):
    """Request schema for creating a tenant."""

    tenant_name: str = Field(..., min_length=1, max_length=100)
    initial_admin: InitialAdminRequest | None = None


class CreateTenantResponse(BaseModel):
    """Response schema for tenant creation."""

    tenant_id: str
    tenant_name: str
    admin_user_id: str | None = None
