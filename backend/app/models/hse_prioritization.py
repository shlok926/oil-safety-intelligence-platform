"""
HSE Prioritization Triage Model
Source of Truth: docs/09_DATABASE_DESIGN.md §22, §48
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Text,
    CheckConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class HSEPrioritization(Base):
    __tablename__ = "hse_prioritizations"

    priority_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    target_type: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "target_type IN ('REPORT', 'RECURRING_PATTERN', 'FACILITY')",
            name="chk_prioritization_target_type",
        ),
        nullable=False,
    )
    target_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    priority_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    urgency_level: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint(
            "urgency_level IN ('IMMEDIATE_ACTION', 'SCHEDULED_AUDIT', 'ROUTINE_LOG')",
            name="chk_prioritization_urgency_level",
        ),
        nullable=False,
    )
    prioritization_basis: Mapped[str] = mapped_column(Text, nullable=False)
    review_status: Mapped[str] = mapped_column(
        String(50),
        default="UNREVIEWED",
        server_default=text("'UNREVIEWED'"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )
