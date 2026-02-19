"""Repository interfaces (Protocols) for identity domain."""

from typing import Protocol
from uuid import UUID

from app.modules.identity.domain.entities import (
    Role,
    Tenant,
    User,
    UserTenantMembership,
    UserTenantRole,
)
from app.modules.identity.domain.refresh_token import RefreshToken


class UserRepository(Protocol):
    """User repository interface."""

    def create(self, user: User) -> User: ...

    def get_by_id(self, user_id: UUID) -> User | None: ...

    def get_by_email(self, email: str) -> User | None: ...

    def get_by_username(self, username: str) -> User | None: ...

    def get_by_phone(self, phone: str) -> User | None: ...

    def update(self, user: User) -> User: ...


class TenantRepository(Protocol):
    """Tenant repository interface."""

    def create(self, tenant: Tenant) -> Tenant: ...

    def get_by_id(self, tenant_id: UUID) -> Tenant | None: ...

    def exists(self, tenant_id: UUID) -> bool: ...


class RoleRepository(Protocol):
    """Role repository interface."""

    def get_by_name(self, role_name: str) -> Role | None: ...


class MembershipRepository(Protocol):
    """User-Tenant membership repository interface."""

    def create(self, membership: UserTenantMembership) -> UserTenantMembership: ...


class RoleAssignmentRepository(Protocol):
    """User-Tenant-Role assignment repository interface."""

    def assign(self, assignment: UserTenantRole) -> UserTenantRole: ...


class AuditRepository(Protocol):
    """Audit logging repository interface."""

    def log_transaction(
        self,
        transaction_uid: UUID,
        action_type: str,
        user_id: UUID | None,
        tenant_id: UUID | None,
    ) -> None: ...

    def log_detail(
        self,
        transaction_uid: UUID,
        action_type: str,
        entity_domain: str,
        entity_id: UUID,
        operation_type: str,
        tenant_id: UUID | None,
    ) -> None: ...

class RefreshTokenRepository(Protocol):
    """Refresh token repository interface."""

    async def create(self, refresh_token: RefreshToken) -> RefreshToken: ...

    async def get_by_token_hash(
        self,
        token_hash: str,
        tenant_id: UUID | None = None,
    ) -> RefreshToken | None: ...

    async def revoke(
        self,
        refresh_token_id: UUID,
        tenant_id: UUID,
    ) -> None: ...

    async def delete_expired(self) -> int: ...