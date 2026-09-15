"""
Safety Report Model
Source of Truth: docs/09_DATABASE_DESIGN.md §7-10, §48, §50
"""

import uuid
from datetime import date, time, datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import (
    String,
    Date,
    Time,
    DateTime,
    Text,
    CheckConstraint,
    ForeignKey,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.data_source import DataSource
    from backend.app.models.processing_run import ProcessingRun
    from backend.app.models.safety_entity import SafetyEntity
    from backend.app.models.safety_relation import SafetyRelation
    from backend.app.models.safety_signal import SafetySignal
    from backend.app.models.sif_assessment import SIFAssessment
    from backend.app.models.barrier_finding import BarrierFinding
    from backend.app.models.lsr_mapping import LSRMapping
    from backend.app.models.evidence_span import EvidenceSpan
    from backend.app.models.pattern_membership import PatternMembership
    from backend.app.models.human_review import HumanReview


class SafetyReport(Base):
    __tablename__ = "safety_reports"

    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("data_sources.source_id"),
        nullable=False,
    )
    source_report_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    report_type: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "report_type IN ('UNSAFE_ACT', 'UNSAFE_CONDITION', 'NEAR_MISS', 'INCIDENT')",
            name="chk_safety_report_type",
        ),
        nullable=False,
    )
    event_date: Mapped[date] = mapped_column(
        Date,
        CheckConstraint("event_date <= CURRENT_DATE", name="chk_event_date_past_or_present"),
        nullable=False,
    )
    event_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    facility_id: Mapped[str] = mapped_column(String(100), nullable=False)
    specific_location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    raw_narrative: Mapped[str] = mapped_column(
        Text,
        CheckConstraint("LENGTH(TRIM(raw_narrative)) >= 10", name="chk_raw_narrative_length"),
        nullable=False,
    )
    normalized_narrative: Mapped[str] = mapped_column(Text, nullable=False)
    actual_outcome_severity: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "actual_outcome_severity IN ('NO_INJURY_NEAR_MISS', 'FIRST_AID', 'MEDICAL_TREATMENT', 'LOST_TIME_INJURY', 'FATALITY', 'UNKNOWN')",
            name="chk_actual_outcome_severity",
        ),
        nullable=False,
    )
    processing_status: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "processing_status IN ('PENDING', 'PROCESSING', 'PROCESSED', 'PROCESSING_FAILED', 'REVIEWED')",
            name="chk_processing_status",
        ),
        default="PENDING",
        server_default=text("'PENDING'"),
        nullable=False,
    )
    duplicate_cluster_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    narrative_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    data_source: Mapped["DataSource"] = relationship("DataSource", back_populates="safety_reports")
    processing_runs: Mapped[List["ProcessingRun"]] = relationship(
        "ProcessingRun", back_populates="safety_report", cascade="all, delete-orphan"
    )
    safety_entities: Mapped[List["SafetyEntity"]] = relationship(
        "SafetyEntity", back_populates="safety_report", cascade="all, delete-orphan"
    )
    safety_relations: Mapped[List["SafetyRelation"]] = relationship(
        "SafetyRelation", back_populates="safety_report", cascade="all, delete-orphan"
    )
    safety_signals: Mapped[List["SafetySignal"]] = relationship(
        "SafetySignal", back_populates="safety_report", cascade="all, delete-orphan"
    )
    sif_assessments: Mapped[List["SIFAssessment"]] = relationship(
        "SIFAssessment", back_populates="safety_report", cascade="all, delete-orphan"
    )
    barrier_findings: Mapped[List["BarrierFinding"]] = relationship(
        "BarrierFinding", back_populates="safety_report", cascade="all, delete-orphan"
    )
    lsr_mappings: Mapped[List["LSRMapping"]] = relationship(
        "LSRMapping", back_populates="safety_report", cascade="all, delete-orphan"
    )
    evidence_spans: Mapped[List["EvidenceSpan"]] = relationship(
        "EvidenceSpan", back_populates="safety_report", cascade="all, delete-orphan"
    )
    pattern_memberships: Mapped[List["PatternMembership"]] = relationship(
        "PatternMembership", back_populates="safety_report", cascade="all, delete-orphan"
    )
    human_reviews: Mapped[List["HumanReview"]] = relationship(
        "HumanReview", back_populates="safety_report", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_reports_facility_date", "facility_id", event_date.desc()),
        Index("idx_reports_status", "processing_status"),
        Index("idx_reports_duplicate", "duplicate_cluster_id", postgresql_where=text("duplicate_cluster_id IS NOT NULL")),
    )
