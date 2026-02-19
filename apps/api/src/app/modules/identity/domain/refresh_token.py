"""RefreshToken domain entity."""

from datetime import datetime
from uuid import UUID


class RefreshToken:
    """Domain entity representing a refresh token."""

    def __init__(
        self,
        refresh_token_id: UUID,
        user_id: UUID,
        tenant_id: UUID,
        token_hash: str,
        expires_at: datetime,
        revoked_at: datetime | None,
        created_at: datetime,
        last_used_at: datetime | None = None,
        created_by: UUID | None = None,
    ):
        """
        Initialize RefreshToken.

        Args:
            refresh_token_id: Unique token identifier
            user_id: User who owns this token
            tenant_id: Tenant context
            token_hash: SHA256 hash of token (for storage)
            expires_at: Token expiration timestamp
            revoked_at: Revocation timestamp (None if active)
            created_at: Creation timestamp
            last_used_at: Timestamp of last usage
            created_by: User ID who created this token
        """
        self.refresh_token_id = refresh_token_id
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.token_hash = token_hash
        self.expires_at = expires_at
        self.revoked_at = revoked_at
        self.created_at = created_at
        self.last_used_at = last_used_at
        self.created_by = created_by

    def is_expired(self) -> bool:
        """Check if token has expired."""
        from datetime import UTC

        return self.expires_at <= datetime.now(UTC)

    def is_revoked(self) -> bool:
        """Check if token has been revoked."""
        return self.revoked_at is not None

    def is_valid(self) -> bool:
        """Check if token is valid (not expired, not revoked)."""
        return not self.is_expired() and not self.is_revoked()
