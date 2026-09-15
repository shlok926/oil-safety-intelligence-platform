"""
Processing Run Execution Metadata Model
Source of Truth: docs/09_DATABASE_DESIGN.md §25, §48
"""

import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, DateTime, Text, CheckConstraint, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.models.safety_report import SafetyReport
    from backend.app.models.model_version import ModelVersion
    from backend.app.models.rule_version import RuleVersion
    from backend.app.models.safety_entity import SafetyEntity
    from backend.app.models.safety_relation import SafetyRelation
    from backend.app.models.safety_signal import SafetySignal
    from backend.app.models.sif_assessment import SIFAssessment
    from backend.app.models.barrier_finding import BarrierFinding
    from backend.app.models.lsr_mapping import LSRMapping


class ProcessingRun(Base):
    __tablename__ = "processing_runs"

    run_id: Mapped[uuid.UUID] = mapped_column(
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
    pipeline_version: Mapped[str] = mapped_column(String(50), nullable=False)
    model_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("model_versions.model_version_id"),
        nullable=True,
    )
    rule_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rule_versions.rule_version_id"),
        nullable=True,
    )
    execution_status: Mapped[str] = mapped_column(
        String(50),
        CheckConstraint(
            "execution_status IN ('SUCCESS', 'FAILED', 'TIMED_OUT')",
            name="chk_processing_run_status",
        ),
        nullable=False,
    )
    execution_duration_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    execution_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships
    safety_report: Mapped["SafetyReport"] = relationship("SafetyReport", back_populates="processing_runs")
    model_version: Mapped[Optional["ModelVersion"]] = relationship("ModelVersion", back_populates="processing_runs")
    rule_version: Mapped[Optional["RuleVersion"]] = relationship("RuleVersion", back_populates="processing_runs")
    safety_entities: Mapped[List["SafetyEntity"]] = relationship(
        "SafetyEntity", back_populates="processing_run", cascade="all, delete-orphan"
    )
    safety_relations: Mapped[List["SafetyRelation"]] = relationship(
        "SafetyRelation", back_populates="processing_run", cascade="all, delete-orphan"
    )
    safety_signals: Mapped[List["SafetySignal"]] = relationship(
        "SafetySignal", back_populates="processing_run", cascade="all, delete-orphan"
    )
    sif_assessments: Mapped[List["SIFAssessment"]] = relationship(
        "SIFAssessment", back_populates="processing_run", cascade="all, delete-orphan"
    )
    barrier_findings: Mapped[List["BarrierFinding"]] = relationship(
        "BarrierFinding", back_populates="processing_run", cascade="all, delete-orphan"
    )
    lsr_mappings: Mapped[List["LSRMapping"]] = relationship(
        "LSRMapping", back_populates="processing_run", cascade="all, delete-orphan"
    )
