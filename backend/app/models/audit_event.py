"""
Audit Event Cryptographic Ledger Model
Source of Truth: docs/09_DATABASE_DESIGN.md §31, §48, §50
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING
from sqlalchemy import (
    String,
    BigInteger,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.app_user import AppUser


class AuditEvent(Base):
    __tablename__ = "audit_events"

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    sequence_number: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1, increment=1),
        unique=True,
        nullable=False,
    )
    actor_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app_users.user_id"),
        nullable=True,
    )
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    payload_delta: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    client_ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    prev_event_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    event_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    actor: Mapped[Optional["AppUser"]] = relationship("AppUser", back_populates="audit_events")

    __table_args__ = (
        Index("idx_audit_seq", "sequence_number"),
    )
