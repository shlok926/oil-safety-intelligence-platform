"""
Safety Entity Linguistic Token Model
Source of Truth: docs/09_DATABASE_DESIGN.md §12, §48
"""

import uuid
from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import (
    String,
    Integer,
    Numeric,
    CheckConstraint,
    ForeignKey,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.safety_report import SafetyReport
    from backend.app.models.processing_run import ProcessingRun
    from backend.app.models.safety_relation import SafetyRelation


class SafetyEntity(Base):
    __tablename__ = "safety_entities"

    entity_id: Mapped[uuid.UUID] = mapped_column(
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
    entity_class: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "entity_class IN ('EN_ACTIVITY', 'EN_HAZARD', 'EN_EQUIPMENT', 'EN_EXPOSURE', 'EN_CONTROL', 'EN_UNSAFE_ACT', 'EN_UNSAFE_COND')",
            name="chk_entity_class",
        ),
        nullable=False,
    )
    verbatim_text: Mapped[str] = mapped_column(String(255), nullable=False)
    start_char_offset: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("start_char_offset >= 0", name="chk_entity_start_offset"),
        nullable=False,
    )
    end_char_offset: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("end_char_offset > start_char_offset", name="chk_entity_end_offset"),
        nullable=False,
    )
    normalized_concept: Mapped[str] = mapped_column(String(100), nullable=False)
    extraction_confidence: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(4, 3),
        CheckConstraint("extraction_confidence BETWEEN 0.0 AND 1.0", name="chk_entity_confidence"),
        nullable=True,
    )

    # Relationships
    safety_report: Mapped["SafetyReport"] = relationship("SafetyReport", back_populates="safety_entities")
    processing_run: Mapped["ProcessingRun"] = relationship("ProcessingRun", back_populates="safety_entities")
    subject_relations: Mapped[List["SafetyRelation"]] = relationship(
        "SafetyRelation",
        foreign_keys="SafetyRelation.subject_entity_id",
        back_populates="subject_entity",
        cascade="all, delete-orphan",
    )
    object_relations: Mapped[List["SafetyRelation"]] = relationship(
        "SafetyRelation",
        foreign_keys="SafetyRelation.object_entity_id",
        back_populates="object_entity",
        cascade="all, delete-orphan",
    )
