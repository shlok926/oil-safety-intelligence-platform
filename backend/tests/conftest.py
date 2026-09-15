"""
Shared Pytest Fixtures for Backend Test Suite
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.db.session import SessionLocal


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Session-scoped test client for FastAPI endpoints."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def db_session():
    """Function-scoped database session with automatic rollback."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
