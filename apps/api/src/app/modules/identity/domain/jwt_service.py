"""JWT token generation and validation service."""

import hashlib
from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import jwt


class JWTService:
    """Service for JWT token generation, validation, and hashing."""

    @staticmethod
    def generate_access_token(
        user_id: UUID,
        tenant_id: UUID,
        roles: list[str],
        secret_key: str,
        expire_minutes: int = 60,
    ) -> str:
        """
        Generate an access token (JWT).

        Args:
            user_id: User identifier
            tenant_id: Tenant context
            roles: List of role names
            secret_key: Secret key for signing (must be 32+ chars for HS256)
            expire_minutes: Token expiry in minutes

        Returns:
            Signed JWT token string
        """
        now = datetime.now(UTC)
        exp = now + timedelta(minutes=expire_minutes)
        
        payload = {
            "sub": str(user_id),  # Subject (user ID)
            "tenant_id": str(tenant_id),
            "roles": roles,
            "iat": int(now.timestamp()),  # Issued at
            "exp": int(exp.timestamp()),  # Expiration
        }
        
        token = jwt.encode(
            payload,
            secret_key,
            algorithm="HS256",
        )
        return token

    @staticmethod
    def verify_access_token(
        token: str,
        secret_key: str,
    ) -> dict:
        """
        Verify and decode an access token.

        Args:
            token: JWT token string
            secret_key: Secret key for verification

        Returns:
            Decoded token payload dict

        Raises:
            jwt.InvalidTokenError: if token is invalid/expired
        """
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"],
        )
        return payload

    @staticmethod
    def hash_refresh_token(token: str) -> str:
        """
        Hash a refresh token for storage.

        Args:
            token: Opaque refresh token string

        Returns:
            SHA256 hash as hex string
        """
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def verify_refresh_token_hash(token: str, hash_value: str) -> bool:
        """
        Verify a refresh token against its hash.

        Args:
            token: Opaque refresh token string to verify
            hash_value: Stored hash value

        Returns:
            True if token hash matches stored hash
        """
        return hashlib.sha256(token.encode()).hexdigest() == hash_value
