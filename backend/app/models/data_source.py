"""
Data Source & Provenance Model
Source of Truth: docs/09_DATABASE_DESIGN.md §29, §48
"""

import uuid
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Date, DateTime, Text, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.models.enums import SourceType

if TYPE_CHECKING:
    from backend.app.models.safety_report import SafetyReport


class DataSource(Base):
    __tablename__ = "data_sources"

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    source_name: Mapped[str] = mapped_column(String(100), nullable=False)
    source_type: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "source_type IN ('AUTHORIZED_OIL', 'PUBLIC', 'SYNTHETIC', 'MANUAL_LABEL')",
            name="chk_data_source_type",
        ),
        nullable=False,
    )
    license_or_nda_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    acquisition_date: Mapped[date] = mapped_column(Date, nullable=False)
    contains_pii: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("FALSE"))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    safety_reports: Mapped[List["SafetyReport"]] = relationship(
        "SafetyReport",
        back_populates="data_source",
        cascade="all, delete-orphan",
    )
