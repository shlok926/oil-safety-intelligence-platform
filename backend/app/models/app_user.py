"""
Application User Model
Source of Truth: docs/09_DATABASE_DESIGN.md §32, §48
"""

import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.models.enums import AppRole

if TYPE_CHECKING:
    from backend.app.models.human_review import HumanReview
    from backend.app.models.audit_event import AuditEvent


class AppUser(Base):
    __tablename__ = "app_users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "role IN ('HSE_VIEWER', 'HSE_ANALYST', 'HSE_OFFICER', 'ADMINISTRATOR', 'SYSTEM_AUDITOR', 'ML_OPS_ENGINEER')",
            name="chk_app_user_role",
        ),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("TRUE"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    human_reviews: Mapped[List["HumanReview"]] = relationship(
        "HumanReview",
        back_populates="reviewer",
    )
    audit_events: Mapped[List["AuditEvent"]] = relationship(
        "AuditEvent",
        back_populates="actor",
    )
