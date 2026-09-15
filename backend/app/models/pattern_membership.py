"""
Pattern Membership Association Model
Source of Truth: docs/09_DATABASE_DESIGN.md §20, §48, §50
"""

import uuid
from decimal import Decimal
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    DateTime,
    Numeric,
    ForeignKey,
    UniqueConstraint,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.pattern_cluster import RecurringPattern
    from backend.app.models.safety_report import SafetyReport


class PatternMembership(Base):
    __tablename__ = "pattern_memberships"

    membership_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    pattern_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recurring_patterns.pattern_id", ondelete="CASCADE"),
        nullable=False,
    )
    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("safety_reports.report_id", ondelete="CASCADE"),
        nullable=False,
    )
    contribution_weight: Mapped[Decimal] = mapped_column(
        Numeric(4, 3),
        default=Decimal("1.000"),
        server_default=text("1.000"),
        nullable=False,
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    pattern: Mapped["RecurringPattern"] = relationship("RecurringPattern", back_populates="pattern_memberships")
    safety_report: Mapped["SafetyReport"] = relationship("SafetyReport", back_populates="pattern_memberships")

    __table_args__ = (
        UniqueConstraint("pattern_id", "report_id", name="uq_pattern_report"),
        Index("idx_pattern_memberships_report", "report_id"),
        Index("idx_pattern_memberships_pattern", "pattern_id"),
    )
