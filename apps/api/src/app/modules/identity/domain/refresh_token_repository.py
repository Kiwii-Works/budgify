"""RefreshTokenRepository interface/protocol."""

from typing import Protocol
from uuid import UUID

from app.modules.identity.domain.refresh_token import RefreshToken


class RefreshTokenRepository(Protocol):
    """Refresh token repository interface."""

    def create(self, refresh_token: RefreshToken) -> RefreshToken: ...

    def get_by_token_hash(
        self,
        token_hash: str,
        tenant_id: UUID | None = None,
    ) -> RefreshToken | None: ...

    def revoke(
        self,
        refresh_token_id: UUID,
        tenant_id: UUID,
    ) -> None: ...

    def delete_expired(self) -> int: ...
