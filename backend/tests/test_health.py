"""
Tests for Health and Readiness Endpoints
"""

from unittest.mock import patch
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Verify root metadata endpoint returns online status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["service"] == "OIL Safety Intelligence Platform"
    assert data["version"] == "0.1.0"


def test_health_liveness_endpoint(client: TestClient):
    """Verify /api/v1/health liveness probe returns 200 healthy."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "oil-safety-intelligence-backend"
    assert data["version"] == "0.1.0"
    assert "environment" in data


def test_readiness_healthy_database(client: TestClient):
    """Verify /api/v1/health/ready returns 200 ready when database is connected."""
    with patch("backend.app.api.v1.endpoints.health.check_db_health", return_value=(True, None)):
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["database"] == "connected"


def test_readiness_unhealthy_database(client: TestClient):
    """Verify /api/v1/health/ready returns 503 degraded when database is unreachable."""
    with patch(
        "backend.app.api.v1.endpoints.health.check_db_health",
        return_value=(False, "Database connection timeout"),
    ):
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "degraded"
        assert data["database"] == "disconnected"
        assert "detail" in data
