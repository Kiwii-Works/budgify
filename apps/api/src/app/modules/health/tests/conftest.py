"""Health tests configuration."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="function")
def client() -> TestClient:
    """
    FastAPI test client fixture.

    Provides a test client for making HTTP requests to the API.

    Returns:
        FastAPI TestClient instance
    """
    return TestClient(app)
