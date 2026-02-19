"""Unit tests for AuthService."""

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from passlib.context import CryptContext

from app.core.errors import (
    InvalidCredentialsError,
    InvalidTokenError,
    TenantMembershipError,
    UserInactiveError,
)
from app.modules.identity.application.auth_service import AuthService
from app.modules.identity.domain.entities import Role, User
from app.modules.identity.domain.refresh_token import RefreshToken

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_user(*, is_active: bool = True, password: str = "correct_password") -> User:
    now = datetime.now(UTC)
    return User(
        user_id=uuid4(),
        username="testuser",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        phone_number="+1234567890",
        password_hash=_pwd_context.hash(password),
        is_active=is_active,
        is_platform_admin=False,
        created_by=None,
        modified_by=None,
        created_date=now,
        created_date_utc=now,
        modified_date=None,
        modified_date_utc=None,
    )


def _make_role(name: str = "READER") -> Role:
    now = datetime.now(UTC)
    return Role(
        role_id=uuid4(),
        role_name=name,
        created_by=None,
        modified_by=None,
        created_date=now,
        created_date_utc=now,
        modified_date=None,
        modified_date_utc=None,
    )


def _make_refresh_token(
    user_id,
    tenant_id,
    *,
    revoked: bool = False,
    expired: bool = False,
) -> RefreshToken:
    now = datetime.now(UTC)
    expires_at = now - timedelta(hours=1) if expired else now + timedelta(days=7)
    return RefreshToken(
        refresh_token_id=uuid4(),
        user_id=user_id,
        tenant_id=tenant_id,
        token_hash="some_hash",
        expires_at=expires_at,
        revoked_at=now if revoked else None,
        created_at=now,
    )


def _make_service():
    user_repo = MagicMock()
    token_repo = MagicMock()
    return AuthService(user_repo, token_repo), user_repo, token_repo


# ---------------------------------------------------------------------------
# _verify_password
# ---------------------------------------------------------------------------

class TestVerifyPassword:
    def test_correct_password_returns_true(self):
        service, _, _ = _make_service()
        user = _make_user(password="secret123")
        assert service._verify_password("secret123", user.password_hash) is True

    def test_wrong_password_returns_false(self):
        service, _, _ = _make_service()
        user = _make_user(password="secret123")
        assert service._verify_password("wrongpass", user.password_hash) is False


# ---------------------------------------------------------------------------
# login()
# ---------------------------------------------------------------------------

class TestLogin:
    def test_success_returns_tokens(self):
        service, user_repo, token_repo = _make_service()
        user = _make_user()
        tenant_id = uuid4()
        role = _make_role("READER")

        user_repo.get_by_email.return_value = user
        user_repo.has_tenant_membership.return_value = True
        user_repo.get_user_roles_for_tenant.return_value = [role]
        token_repo.create.return_value = MagicMock()

        result = service.login("test@example.com", "correct_password", tenant_id)

        assert "access_token" in result
        assert "refresh_token" in result
        assert result["token_type"] == "Bearer"
        assert result["user_id"] == str(user.user_id)
        assert result["tenant_id"] == str(tenant_id)
        token_repo.create.assert_called_once()

    def test_user_not_found_raises_invalid_credentials(self):
        service, user_repo, _ = _make_service()
        user_repo.get_by_email.return_value = None

        with pytest.raises(InvalidCredentialsError):
            service.login("nobody@example.com", "pass", uuid4())

    def test_wrong_password_raises_invalid_credentials(self):
        service, user_repo, _ = _make_service()
        user_repo.get_by_email.return_value = _make_user(password="correct")

        with pytest.raises(InvalidCredentialsError):
            service.login("test@example.com", "wrongpass", uuid4())

    def test_inactive_user_raises_user_inactive_error(self):
        service, user_repo, _ = _make_service()
        user_repo.get_by_email.return_value = _make_user(is_active=False)

        with pytest.raises(UserInactiveError):
            service.login("test@example.com", "correct_password", uuid4())

    def test_no_membership_raises_tenant_membership_error(self):
        service, user_repo, _ = _make_service()
        user_repo.get_by_email.return_value = _make_user()
        user_repo.has_tenant_membership.return_value = False

        with pytest.raises(TenantMembershipError):
            service.login("test@example.com", "correct_password", uuid4())


# ---------------------------------------------------------------------------
# refresh_token()
# ---------------------------------------------------------------------------

class TestRefreshToken:
    def test_success_rotates_tokens(self):
        service, user_repo, token_repo = _make_service()
        user = _make_user()
        tenant_id = uuid4()
        stored = _make_refresh_token(user.user_id, tenant_id)
        role = _make_role("READER")

        token_repo.get_by_token_hash.return_value = stored
        user_repo.get_by_id.return_value = user
        user_repo.get_user_roles_for_tenant.return_value = [role]
        token_repo.create.return_value = MagicMock()

        raw_token = "some_opaque_token"
        result = service.refresh_token(raw_token)

        token_repo.revoke.assert_called_once_with(stored.refresh_token_id, tenant_id)
        token_repo.create.assert_called_once()
        assert "access_token" in result
        assert "refresh_token" in result

    def test_token_not_found_raises_invalid_token_error(self):
        service, _, token_repo = _make_service()
        token_repo.get_by_token_hash.return_value = None

        with pytest.raises(InvalidTokenError):
            service.refresh_token("nonexistent_token")

    def test_revoked_token_raises_invalid_token_error(self):
        service, _, token_repo = _make_service()
        token_repo.get_by_token_hash.return_value = _make_refresh_token(
            uuid4(), uuid4(), revoked=True
        )

        with pytest.raises(InvalidTokenError):
            service.refresh_token("revoked_token")

    def test_expired_token_raises_invalid_token_error(self):
        service, _, token_repo = _make_service()
        token_repo.get_by_token_hash.return_value = _make_refresh_token(
            uuid4(), uuid4(), expired=True
        )

        with pytest.raises(InvalidTokenError):
            service.refresh_token("expired_token")


# ---------------------------------------------------------------------------
# logout()
# ---------------------------------------------------------------------------

class TestLogout:
    def test_success_revokes_token(self):
        service, _, token_repo = _make_service()
        user_id = uuid4()
        tenant_id = uuid4()
        stored = _make_refresh_token(user_id, tenant_id)
        token_repo.get_by_token_hash.return_value = stored

        service.logout("some_token")

        token_repo.revoke.assert_called_once_with(stored.refresh_token_id, tenant_id)

    def test_token_not_found_raises_invalid_token_error(self):
        service, _, token_repo = _make_service()
        token_repo.get_by_token_hash.return_value = None

        with pytest.raises(InvalidTokenError):
            service.logout("nonexistent_token")
