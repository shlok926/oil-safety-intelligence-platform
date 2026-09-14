"""
SQLAlchemy Declarative Base
Root declarative base for all ORM models across the application.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass
