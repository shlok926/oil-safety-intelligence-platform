"""
Recurring Pattern Cluster Model
Source of Truth: docs/09_DATABASE_DESIGN.md §19, §48
"""

import uuid
from datetime import date, datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import (
    String,
    Integer,
    Date,
    DateTime,
    CheckConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.pattern_membership import PatternMembership


class RecurringPattern(Base):
    __tablename__ = "recurring_patterns"

    pattern_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    pattern_title: Mapped[str] = mapped_column(String(255), nullable=False)
    pattern_type: Mapped[str] = mapped_column(String(50), nullable=False)
    primary_activity: Mapped[str] = mapped_column(String(100), nullable=False)
    primary_hazard: Mapped[str] = mapped_column(String(100), nullable=False)
    primary_barrier_break: Mapped[str] = mapped_column(String(100), nullable=False)
    affected_facility_id: Mapped[str] = mapped_column(String(100), nullable=False)
    report_count: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("report_count >= 3", name="chk_pattern_min_reports"),
        nullable=False,
    )
    sif_potential_count: Mapped[int] = mapped_column(Integer, nullable=False)
    severity_tier: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint(
            "severity_tier IN ('TIER_1_CRITICAL', 'TIER_2_HIGH', 'TIER_3_MONITORED')",
            name="chk_pattern_severity_tier",
        ),
        nullable=False,
    )
    first_observed_date: Mapped[date] = mapped_column(Date, nullable=False)
    latest_observed_date: Mapped[date] = mapped_column(Date, nullable=False)
    pattern_status: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "pattern_status IN ('ACTIVE_HOTSPOT', 'INVESTIGATING', 'RESOLVED', 'ARCHIVED')",
            name="chk_pattern_status",
        ),
        default="ACTIVE_HOTSPOT",
        server_default=text("'ACTIVE_HOTSPOT'"),
        nullable=False,
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    pattern_memberships: Mapped[List["PatternMembership"]] = relationship(
        "PatternMembership",
        back_populates="pattern",
        cascade="all, delete-orphan",
    )
