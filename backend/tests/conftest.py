"""
Shared Pytest Fixtures for Backend Test Suite
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Session-scoped test client for FastAPI endpoints."""
    with TestClient(app) as test_client:
        yield test_client
