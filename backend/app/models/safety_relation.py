"""
Safety Relation Dependency Graph Model
Source of Truth: docs/09_DATABASE_DESIGN.md §13, §48
"""

import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import (
    String,
    Boolean,
    ForeignKey,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.safety_report import SafetyReport
    from backend.app.models.processing_run import ProcessingRun
    from backend.app.models.safety_entity import SafetyEntity


class SafetyRelation(Base):
    __tablename__ = "safety_relations"

    relation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("safety_reports.report_id", ondelete="CASCADE"),
        nullable=False,
    )
    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("processing_runs.run_id", ondelete="CASCADE"),
        nullable=False,
    )
    subject_entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("safety_entities.entity_id"),
        nullable=False,
    )
    relation_verb: Mapped[str] = mapped_column(String(100), nullable=False)
    object_entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("safety_entities.entity_id"),
        nullable=False,
    )
    temporal_preposition: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_negated: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("FALSE"))

    # Relationships
    safety_report: Mapped["SafetyReport"] = relationship("SafetyReport", back_populates="safety_relations")
    processing_run: Mapped["ProcessingRun"] = relationship("ProcessingRun", back_populates="safety_relations")
    subject_entity: Mapped["SafetyEntity"] = relationship(
        "SafetyEntity", foreign_keys=[subject_entity_id], back_populates="subject_relations"
    )
    object_entity: Mapped["SafetyEntity"] = relationship(
        "SafetyEntity", foreign_keys=[object_entity_id], back_populates="object_relations"
    )
