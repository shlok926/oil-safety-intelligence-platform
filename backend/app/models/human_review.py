"""
Human HSE Review Model
Source of Truth: docs/09_DATABASE_DESIGN.md §23, §48
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING
from sqlalchemy import (
    String,
    DateTime,
    Text,
    CheckConstraint,
    ForeignKey,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.safety_report import SafetyReport
    from backend.app.models.app_user import AppUser


class HumanReview(Base):
    __tablename__ = "human_reviews"

    review_id: Mapped[uuid.UUID] = mapped_column(
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
    reviewer_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app_users.user_id"),
        nullable=False,
    )
    review_action: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "review_action IN ('CONFIRM', 'CORRECT', 'REJECT', 'MARK_INSUFFICIENT_EVIDENCE', 'REQUEST_REANALYSIS')",
            name="chk_human_review_action",
        ),
        nullable=False,
    )
    original_sif_result: Mapped[str] = mapped_column(String(20), nullable=False)
    revised_sif_result: Mapped[str] = mapped_column(String(20), nullable=False)
    reviewer_notes: Mapped[str] = mapped_column(Text, nullable=False)
    corrections_payload: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    safety_report: Mapped["SafetyReport"] = relationship("SafetyReport", back_populates="human_reviews")
    reviewer: Mapped["AppUser"] = relationship("AppUser", back_populates="human_reviews")
