"""Tests for health check endpoint."""

from fastapi.testclient import TestClient


def test_health_endpoint_returns_200(client: TestClient) -> None:
    """Test that health endpoint returns 200 OK."""
    response = client.get("/api/health")
    assert response.status_code == 200


def test_health_endpoint_response_structure(client: TestClient) -> None:
    """Test that health endpoint returns correct response structure."""
    response = client.get("/api/health")
    data = response.json()

    # Verify top-level keys
    assert "data" in data
    assert "meta" in data

    # Verify data payload
    assert data["data"]["status"] == "ok"

    # Verify metadata
    assert "request_id" in data["meta"]
    assert "timestamp" in data["meta"]


def test_health_endpoint_request_id_is_unique(client: TestClient) -> None:
    """Test that each request generates a unique request_id."""
    response1 = client.get("/api/health")
    response2 = client.get("/api/health")

    request_id1 = response1.json()["meta"]["request_id"]
    request_id2 = response2.json()["meta"]["request_id"]

    assert request_id1 != request_id2
