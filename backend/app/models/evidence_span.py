"""
Evidence Span Verbatim Character Offset Model
Source of Truth: docs/09_DATABASE_DESIGN.md §14, §48, §50
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Text,
    CheckConstraint,
    ForeignKey,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.safety_report import SafetyReport


class EvidenceSpan(Base):
    __tablename__ = "evidence_spans"

    evidence_id: Mapped[uuid.UUID] = mapped_column(
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
    target_entity_type: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "target_entity_type IN ('SIF_ASSESSMENT', 'BARRIER_FINDING', 'LSR_MAPPING', 'SAFETY_SIGNAL')",
            name="chk_evidence_target_type",
        ),
        nullable=False,
    )
    target_entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    verbatim_text: Mapped[str] = mapped_column(Text, nullable=False)
    start_offset: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("start_offset >= 0", name="chk_evidence_start_offset"),
        nullable=False,
    )
    end_offset: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("end_offset > start_offset", name="chk_evidence_end_offset"),
        nullable=False,
    )
    reasoning_justification: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    safety_report: Mapped["SafetyReport"] = relationship("SafetyReport", back_populates="evidence_spans")

    __table_args__ = (
        Index("idx_evidence_target", "target_entity_type", "target_entity_id"),
    )
