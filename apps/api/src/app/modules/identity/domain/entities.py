"""Domain entities for identity module (plain Python, no framework dependencies)."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    """
    User domain entity.

    Represents a global user identity across all tenants.
    """

    user_id: UUID
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password_hash: str
    is_active: bool
    is_platform_admin: bool
    created_by: UUID | None
    modified_by: UUID | None
    created_date: datetime
    created_date_utc: datetime
    modified_date: datetime | None
    modified_date_utc: datetime | None


@dataclass
class Role:
    """
    Role domain entity.

    Represents a global role definition (SUDO, READER, EDITOR, REPORTER).
    Role assignments are tenant-scoped.
    """

    role_id: UUID
    role_name: str
    created_by: UUID | None
    modified_by: UUID | None
    created_date: datetime
    created_date_utc: datetime
    modified_date: datetime | None
    modified_date_utc: datetime | None


@dataclass
class Tenant:
    """
    Tenant domain entity.

    Represents a tenant (organization) in the multi-tenant system.
    """

    tenant_id: UUID
    tenant_name: str
    is_active: bool
    created_by: UUID | None
    modified_by: UUID | None
    created_date: datetime
    created_date_utc: datetime
    modified_date: datetime | None
    modified_date_utc: datetime | None


@dataclass
class UserTenantMembership:
    """
    User-Tenant membership domain entity.

    Links a user to a tenant. A user can belong to multiple tenants.
    """

    user_id: UUID
    tenant_id: UUID
    is_default: bool
    created_by: UUID | None
    modified_by: UUID | None
    created_date: datetime
    created_date_utc: datetime
    modified_date: datetime | None
    modified_date_utc: datetime | None


@dataclass
class UserTenantRole:
    """
    User-Tenant-Role assignment domain entity.

    Assigns a role to a user within a specific tenant.
    Same user can have different roles in different tenants.
    """

    user_id: UUID
    tenant_id: UUID
    role_id: UUID
    created_by: UUID | None
    modified_by: UUID | None
    created_date: datetime
    created_date_utc: datetime
    modified_date: datetime | None
    modified_date_utc: datetime | None
