"""
Database Engine and Session Management
Provides session generator and resilient health check functions.
"""

from typing import Generator, Tuple, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from backend.app.core.config import settings
from backend.app.core.logging import get_logger

logger = get_logger(__name__)

# Engine configuration with connection pre-ping
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_health() -> Tuple[bool, Optional[str]]:
    """
    Check database connectivity via a lightweight query.
    Returns (is_connected, error_message).
    Resilient: never raises unhandled exceptions.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True, None
    except SQLAlchemyError as exc:
        logger.warning(f"Database health check failed: {exc}")
        return False, str(exc)
    except Exception as exc:
        logger.error(f"Unexpected error during database health check: {exc}")
        return False, str(exc)
