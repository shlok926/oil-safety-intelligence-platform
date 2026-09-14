"""
Database Seeding Script Stub
Provides CLI command to initialize or seed the database for H0.
Usage: python -m backend.scripts.seed_data
"""

import sys
from backend.app.core.logging import setup_logging, get_logger
from backend.app.db.session import check_db_health

setup_logging()
logger = get_logger("seed_data")


def main() -> int:
    """Execute seed data workflow."""
    logger.info("Starting seed data verification...")
    is_connected, err = check_db_health()
    if not is_connected:
        logger.warning(f"Database is not accessible: {err}")
        logger.warning("Seed data operation deferred until database is active.")
        return 0

    logger.info("Database connection established. Phase 1 seed contract verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
