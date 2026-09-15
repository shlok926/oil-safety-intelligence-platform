"""
Barrier Finding & Degradation Model
Source of Truth: docs/09_DATABASE_DESIGN.md §17, §48, §50
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
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


class BarrierFinding(Base):
    __tablename__ = "barrier_findings"

    barrier_id: Mapped[uuid.UUID] = mapped_column(
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
    barrier_name: Mapped[str] = mapped_column(String(100), nullable=False)
    barrier_category: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "barrier_category IN ('PHYSICAL', 'ADMINISTRATIVE', 'PROCEDURAL', 'PPE')",
            name="chk_barrier_category",
        ),
        nullable=False,
    )
    barrier_status: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "barrier_status IN ('PRESENT_VERIFIED', 'INCOMPLETE', 'MISSING', 'FAILED', 'BYPASSED', 'UNKNOWN')",
            name="chk_barrier_status_six_state",
        ),
        nullable=False,
    )
    is_critical_barrier: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("FALSE"),
    )
    verification_method: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    safety_report: Mapped["SafetyReport"] = relationship("SafetyReport", back_populates="barrier_findings")
    processing_run: Mapped["ProcessingRun"] = relationship("ProcessingRun", back_populates="barrier_findings")

    __table_args__ = (
        Index("idx_barriers_report_status", "report_id", "barrier_status"),
        Index(
            "idx_barriers_critical",
            "barrier_name",
            "barrier_status",
            postgresql_where=text("is_critical_barrier = TRUE"),
        ),
    )
