"""API tests for authentication endpoints."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.errors import InvalidCredentialsError, InvalidTokenError
from app.core.dependencies.auth import get_current_user, CurrentUser
from app.main import app
from app.modules.identity.api.routes import get_auth_service


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_auth_response(user_id=None, tenant_id=None):
    uid = str(user_id or uuid4())
    tid = str(tenant_id or uuid4())
    return {
        "access_token": "fake.access.token",
        "refresh_token": "fake_refresh_token_value",
        "token_type": "Bearer",
        "expires_in": 3600,
        "user_id": uid,
        "tenant_id": tid,
    }


def _mock_current_user(roles=None):
    user = CurrentUser(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=roles or ["READER"],
        iat=0,
        exp=9999999999,
    )
    return user


# ---------------------------------------------------------------------------
# POST /api/auth/login
# ---------------------------------------------------------------------------

class TestLoginEndpoint:
    def test_login_success_returns_200_with_tokens(self):
        mock_service = MagicMock()
        mock_service.login.return_value = _mock_auth_response()

        with TestClient(app) as client:
            app.dependency_overrides[get_auth_service] = lambda: mock_service
            response = client.post(
                "/api/auth/login",
                json={"email": "test@example.com", "password": "pass1234", "tenant_id": str(uuid4())},
            )
            app.dependency_overrides.clear()

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert data["data"]["token_type"] == "Bearer"

    def test_login_wrong_credentials_returns_401(self):
        mock_service = MagicMock()
        mock_service.login.side_effect = InvalidCredentialsError()

        with TestClient(app) as client:
            app.dependency_overrides[get_auth_service] = lambda: mock_service
            response = client.post(
                "/api/auth/login",
                json={"email": "test@example.com", "password": "wrongpass", "tenant_id": str(uuid4())},
            )
            app.dependency_overrides.clear()

        assert response.status_code == 401

    def test_login_missing_fields_returns_422(self):
        with TestClient(app) as client:
            response = client.post(
                "/api/auth/login",
                json={"email": "test@example.com"},
            )
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/auth/refresh
# ---------------------------------------------------------------------------

class TestRefreshEndpoint:
    def test_refresh_success_returns_200_with_new_tokens(self):
        mock_service = MagicMock()
        mock_service.refresh_token.return_value = _mock_auth_response()

        with TestClient(app) as client:
            app.dependency_overrides[get_auth_service] = lambda: mock_service
            response = client.post(
                "/api/auth/refresh",
                json={"refresh_token": "a" * 32},
            )
            app.dependency_overrides.clear()

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data["data"]

    def test_refresh_invalid_token_returns_401(self):
        mock_service = MagicMock()
        mock_service.refresh_token.side_effect = InvalidTokenError()

        with TestClient(app) as client:
            app.dependency_overrides[get_auth_service] = lambda: mock_service
            response = client.post(
                "/api/auth/refresh",
                json={"refresh_token": "a" * 32},
            )
            app.dependency_overrides.clear()

        assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /api/auth/logout
# ---------------------------------------------------------------------------

class TestLogoutEndpoint:
    def test_logout_success_returns_204(self):
        mock_service = MagicMock()
        mock_service.logout.return_value = None

        with TestClient(app) as client:
            app.dependency_overrides[get_auth_service] = lambda: mock_service
            response = client.post(
                "/api/auth/logout",
                json={"refresh_token": "a" * 32},
            )
            app.dependency_overrides.clear()

        assert response.status_code == 204

    def test_logout_invalid_token_returns_401(self):
        mock_service = MagicMock()
        mock_service.logout.side_effect = InvalidTokenError()

        with TestClient(app) as client:
            app.dependency_overrides[get_auth_service] = lambda: mock_service
            response = client.post(
                "/api/auth/logout",
                json={"refresh_token": "a" * 32},
            )
            app.dependency_overrides.clear()

        assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /api/auth/me
# ---------------------------------------------------------------------------

class TestMeEndpoint:
    def test_me_returns_user_info(self):
        user_id = uuid4()
        tenant_id = uuid4()
        current_user = _mock_current_user(roles=["READER"])
        current_user.user_id = user_id
        current_user.tenant_id = tenant_id

        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.username = "testuser"
        mock_user.is_active = True
        mock_user.created_date_utc = None

        mock_db = MagicMock()

        from app.core.database import get_db
        from app.modules.identity.infrastructure.repositories import SQLAlchemyUserRepository

        with TestClient(app) as client:
            app.dependency_overrides[get_current_user] = lambda: current_user
            app.dependency_overrides[get_db] = lambda: mock_db

            with MagicMock() as mock_repo_cls:
                original = SQLAlchemyUserRepository.get_by_id

                def fake_get_by_id(self, uid):
                    return mock_user

                SQLAlchemyUserRepository.get_by_id = fake_get_by_id
                response = client.get("/api/auth/me")
                SQLAlchemyUserRepository.get_by_id = original

            app.dependency_overrides.clear()

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["user_id"] == str(user_id)
        assert data["data"]["tenant_id"] == str(tenant_id)
        assert "roles" in data["data"]

    def test_me_without_token_returns_403(self):
        # FastAPI HTTPBearer returns 403 when Authorization header is missing
        with TestClient(app) as client:
            response = client.get("/api/auth/me")
        assert response.status_code == 403
