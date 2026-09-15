"""
Model Version Tracking Model
Source of Truth: docs/09_DATABASE_DESIGN.md §26, §48
"""

import uuid
from datetime import date
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Date, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.processing_run import ProcessingRun


class ModelVersion(Base):
    __tablename__ = "model_versions"

    model_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    semantic_version: Mapped[str] = mapped_column(String(50), nullable=False)
    model_architecture: Mapped[str] = mapped_column(String(100), nullable=False)
    training_dataset_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    release_state: Mapped[str] = mapped_column(
        String(50),
        default="ACTIVE_PRODUCTION",
        server_default=text("'ACTIVE_PRODUCTION'"),
        nullable=False,
    )
    release_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Relationships
    processing_runs: Mapped[List["ProcessingRun"]] = relationship(
        "ProcessingRun",
        back_populates="model_version",
    )
