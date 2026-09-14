"""
Tests for Centralized Application Settings
"""

from backend.app.core.config import get_settings


def test_settings_load_defaults():
    """Verify that settings load with valid canonical defaults."""
    settings = get_settings()
    assert settings.APP_NAME == "OIL Safety Intelligence Platform"
    assert settings.APP_VERSION == "0.1.0"
    assert settings.API_V1_PREFIX == "/api/v1"
    assert "postgresql://" in settings.DATABASE_URL
    assert settings.ALGORITHM == "HS256"
    assert settings.MODEL_CACHE_DIR == "/app/models/cache"
