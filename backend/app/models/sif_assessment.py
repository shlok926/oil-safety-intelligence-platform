"""
SIF Potential Assessment Model
Source of Truth: docs/09_DATABASE_DESIGN.md §15, §48, §50
"""

import uuid
from decimal import Decimal
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Numeric,
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
    from backend.app.models.processing_run import ProcessingRun


class SIFAssessment(Base):
    __tablename__ = "sif_assessments"

    assessment_id: Mapped[uuid.UUID] = mapped_column(
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
    sif_potential: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint(
            "sif_potential IN ('YES', 'NO', 'REVIEW')",
            name="chk_sif_potential_canonical",
        ),
        nullable=False,
    )
    priority_level: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint(
            "priority_level IN ('P1_CRITICAL', 'P2_HIGH', 'P3_STANDARD')",
            name="chk_sif_priority_level",
        ),
        nullable=False,
    )
    assessment_confidence: Mapped[Decimal] = mapped_column(
        Numeric(4, 3),
        CheckConstraint("assessment_confidence BETWEEN 0.0 AND 1.0", name="chk_sif_confidence"),
        nullable=False,
    )
    causal_rule_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    reasoning_summary: Mapped[str] = mapped_column(Text, nullable=False)
    is_active_assessment: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("TRUE"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    safety_report: Mapped["SafetyReport"] = relationship("SafetyReport", back_populates="sif_assessments")
    processing_run: Mapped["ProcessingRun"] = relationship("ProcessingRun", back_populates="sif_assessments")

    __table_args__ = (
        Index(
            "idx_sif_active",
            "report_id",
            "sif_potential",
            "priority_level",
            postgresql_where=text("is_active_assessment = TRUE"),
        ),
    )
