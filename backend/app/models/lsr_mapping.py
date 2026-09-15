"""
IOGP Life-Saving Rule Mapping Model
Source of Truth: docs/09_DATABASE_DESIGN.md §18, §48, §50
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
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.safety_report import SafetyReport
    from backend.app.models.processing_run import ProcessingRun


class LSRMapping(Base):
    __tablename__ = "lsr_mappings"

    mapping_id: Mapped[uuid.UUID] = mapped_column(
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
    lsr_rule_code: Mapped[str] = mapped_column(String(50), nullable=False)
    lsr_rule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    mapping_confidence: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(4, 3),
        CheckConstraint("mapping_confidence BETWEEN 0.0 AND 1.0", name="chk_lsr_confidence"),
        nullable=True,
    )
    mapping_mechanism: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "mapping_mechanism IN ('RULE_BASED', 'SEMANTIC_COSINE', 'HYBRID')",
            name="chk_lsr_mapping_mechanism",
        ),
        nullable=False,
    )
    is_primary_rule: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("TRUE"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    safety_report: Mapped["SafetyReport"] = relationship("SafetyReport", back_populates="lsr_mappings")
    processing_run: Mapped["ProcessingRun"] = relationship("ProcessingRun", back_populates="lsr_mappings")

    __table_args__ = (
        Index("idx_lsr_code", "lsr_rule_code", "report_id"),
    )
