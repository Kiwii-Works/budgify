"""Application service for authentication operations: login, refresh, logout."""

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4
import secrets
import hashlib

from passlib.context import CryptContext

from app.core.config import settings
from app.core.errors import (
    InvalidCredentialsError,
    UserInactiveError,
    TenantMembershipError,
    InvalidTokenError,
)
from app.modules.identity.domain.jwt_service import JWTService
from app.modules.identity.domain.refresh_token import RefreshToken
from app.modules.identity.infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyRefreshTokenRepository

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication operations: login, refresh, logout."""

    def __init__(
        self,
        user_repository: SQLAlchemyUserRepository,
        refresh_token_repository: SQLAlchemyRefreshTokenRepository,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    def _hash_token(self, token: str) -> str:
        """Hash a token for storage."""
        return hashlib.sha256(token.encode()).hexdigest()

    def _generate_refresh_token(self) -> str:
        """Generate a secure random refresh token."""
        return secrets.token_urlsafe(32)

    def _verify_password(self, plain_password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, password_hash)

    def login(
        self,
        email: str,
        password: str,
        tenant_id: UUID,
    ) -> dict:
        """
        Authenticate user and return tokens.

        Args:
            email: User email
            password: User password
            tenant_id: Tenant context for login

        Returns:
            {
                "access_token": str,
                "refresh_token": str,
                "token_type": "Bearer",
                "expires_in": int (seconds),
                "user_id": UUID,
                "tenant_id": UUID
            }

        Raises:
            InvalidCredentialsError: if email/password incorrect
            TenantMembershipError: if user not member of tenant
            UserInactiveError: if user.is_active == False
            InvalidTokenError: if token generation fails
        """
        # Find user by email
        user = self.user_repository.get_by_email(email)
        if not user:
            raise InvalidCredentialsError("Invalid email or password")

        # Verify password
        if not self._verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password")

        # Check user is active
        if not user.is_active:
            raise UserInactiveError("User account is inactive")

        # Verify user has tenant membership
        has_membership = self.user_repository.has_tenant_membership(user.user_id, tenant_id)
        if not has_membership:
            raise TenantMembershipError(
                f"User {user.user_id} is not a member of tenant {tenant_id}"
            )

        # Get user roles for tenant
        roles = self.user_repository.get_user_roles_for_tenant(user.user_id, tenant_id)

        # Generate access token with 60 minute expiry
        access_token_expires_at = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

        access_token = JWTService.generate_access_token(
            user_id=user.user_id,
            tenant_id=tenant_id,
            roles=[r.role_name for r in roles],
            secret_key=settings.jwt_secret_key,
            expire_minutes=settings.access_token_expire_minutes,
        )

        # Generate refresh token
        refresh_token_str = self._generate_refresh_token()
        refresh_token_hash = JWTService.hash_refresh_token(refresh_token_str)

        # Create RefreshToken entity with 7-day expiry
        refresh_token_expires_at = datetime.now(UTC) + timedelta(
            days=settings.refresh_token_expire_days
        )
        refresh_token = RefreshToken(
            refresh_token_id=uuid4(),
            user_id=user.user_id,
            tenant_id=tenant_id,
            token_hash=refresh_token_hash,
            expires_at=refresh_token_expires_at,
            revoked_at=None,
            created_at=datetime.now(UTC),
            last_used_at=None,
        )

        # Store refresh token in database
        self.refresh_token_repository.create(refresh_token)

        # Return auth response
        expires_in = int((access_token_expires_at - datetime.now(UTC)).total_seconds())
        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str,
            "token_type": "Bearer",
            "expires_in": expires_in,
            "user_id": str(user.user_id),
            "tenant_id": str(tenant_id),
        }

    def refresh_token(
        self,
        refresh_token: str,
    ) -> dict:
        """
        Refresh access token using refresh token.

        Returns same structure as login().

        Raises:
            InvalidTokenError: if refresh token invalid/expired/revoked
        """
        # Hash the incoming refresh token
        refresh_token_hash = JWTService.hash_refresh_token(refresh_token)

        # Query database for token by hash
        stored_token = self.refresh_token_repository.get_by_token_hash(refresh_token_hash)
        if not stored_token:
            raise InvalidTokenError("Refresh token not found")

        # Validate token not revoked
        if stored_token.revoked_at is not None:
            raise InvalidTokenError("Refresh token has been revoked")

        # Validate token not expired
        if stored_token.expires_at <= datetime.now(UTC):
            raise InvalidTokenError("Refresh token has expired")

        # Extract user_id and tenant_id from stored token
        user_id = stored_token.user_id
        tenant_id = stored_token.tenant_id

        # Get fresh user data from database
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise InvalidTokenError("User not found")

        # Get user roles for tenant
        roles = self.user_repository.get_user_roles_for_tenant(user_id, tenant_id)

        # Revoke old refresh token
        self.refresh_token_repository.revoke(stored_token.refresh_token_id, tenant_id)

        # Generate new access token
        access_token = JWTService.generate_access_token(
            user_id=user_id,
            tenant_id=tenant_id,
            roles=[r.role_name for r in roles],
            secret_key=settings.jwt_secret_key,
            expire_minutes=settings.access_token_expire_minutes,
        )

        # Generate new refresh token
        new_refresh_token_str = self._generate_refresh_token()
        new_refresh_token_hash = JWTService.hash_refresh_token(new_refresh_token_str)

        # Create new RefreshToken entity
        refresh_token_expires_at = datetime.now(UTC) + timedelta(
            days=settings.refresh_token_expire_days
        )
        new_refresh_token = RefreshToken(
            refresh_token_id=uuid4(),
            user_id=user_id,
            tenant_id=tenant_id,
            token_hash=new_refresh_token_hash,
            expires_at=refresh_token_expires_at,
            revoked_at=None,
            created_at=datetime.now(UTC),
            last_used_at=None,
        )

        # Store new token in database
        self.refresh_token_repository.create(new_refresh_token)

        # Return auth response
        access_token_expires_at = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        expires_in = int((access_token_expires_at - datetime.now(UTC)).total_seconds())
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token_str,
            "token_type": "Bearer",
            "expires_in": expires_in,
            "user_id": str(user_id),
            "tenant_id": str(tenant_id),
        }

    def logout(
        self,
        refresh_token: str,
    ) -> None:
        """
        Revoke refresh token and logout user.

        Raises:
            InvalidTokenError: if refresh token not found
        """
        # Hash the incoming refresh token
        refresh_token_hash = JWTService.hash_refresh_token(refresh_token)

        # Query database for token
        stored_token = self.refresh_token_repository.get_by_token_hash(refresh_token_hash)

        if stored_token:
            self.refresh_token_repository.revoke(stored_token.refresh_token_id, stored_token.tenant_id)
        else:
            raise InvalidTokenError("Refresh token not found")
