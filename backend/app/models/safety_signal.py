"""
Safety Signal Physical Operational Reality Model
Source of Truth: docs/09_DATABASE_DESIGN.md §11, §48
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


class SafetySignal(Base):
    __tablename__ = "safety_signals"

    signal_id: Mapped[uuid.UUID] = mapped_column(
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
    signal_category: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "signal_category IN ('ACTIVITY', 'HAZARD', 'EXPOSURE', 'CONTROL', 'UNSAFE_ACT', 'UNSAFE_CONDITION', 'OUTCOME', 'INTERVENTION')",
            name="chk_signal_category",
        ),
        nullable=False,
    )
    canonical_name: Mapped[str] = mapped_column(String(100), nullable=False)
    raw_text_mention: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    signal_status: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "signal_status IN ('ACTIVE', 'INACTIVE', 'SUSPECTED', 'UNKNOWN')",
            name="chk_signal_status",
        ),
        nullable=False,
    )
    confidence_score: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(4, 3),
        CheckConstraint("confidence_score BETWEEN 0.0 AND 1.0", name="chk_signal_confidence"),
        nullable=True,
    )
    is_critical_precursor: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("FALSE"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    safety_report: Mapped["SafetyReport"] = relationship("SafetyReport", back_populates="safety_signals")
    processing_run: Mapped["ProcessingRun"] = relationship("ProcessingRun", back_populates="safety_signals")
