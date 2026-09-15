"""
Rule Version Tracking Model
Source of Truth: docs/09_DATABASE_DESIGN.md §27, §48
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.processing_run import ProcessingRun


class RuleVersion(Base):
    __tablename__ = "rule_versions"

    rule_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    ruleset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    ruleset_semantic_ver: Mapped[str] = mapped_column(String(50), nullable=False)
    ruleset_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    ruleset_definition: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("TRUE"))
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Relationships
    processing_runs: Mapped[List["ProcessingRun"]] = relationship(
        "ProcessingRun",
        back_populates="rule_version",
    )
