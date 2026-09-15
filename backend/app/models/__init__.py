"""
SQLAlchemy Models Package
Exports all canonical models and enums for the OIL Safety Intelligence Platform.
Source of Truth: docs/09_DATABASE_DESIGN.md
"""

from backend.app.models.enums import (
    SourceType,
    AppRole,
    ReportType,
    OutcomeSeverity,
    ProcessingStatus,
    ReleaseState,
    ExecutionStatus,
    EntityClass,
    SignalCategory,
    SignalStatus,
    SIFPotential,
    PriorityLevel,
    BarrierCategory,
    BarrierStatus,
    MappingMechanism,
    TargetEntityType,
    SeverityTier,
    PatternStatus,
    PrioritizationTargetType,
    UrgencyLevel,
    ReviewAction,
)

from backend.app.models.data_source import DataSource
from backend.app.models.app_user import AppUser
from backend.app.models.model_version import ModelVersion
from backend.app.models.rule_version import RuleVersion
from backend.app.models.safety_report import SafetyReport
from backend.app.models.processing_run import ProcessingRun
from backend.app.models.safety_entity import SafetyEntity
from backend.app.models.safety_relation import SafetyRelation
from backend.app.models.safety_signal import SafetySignal
from backend.app.models.sif_assessment import SIFAssessment
from backend.app.models.barrier_finding import BarrierFinding
from backend.app.models.lsr_mapping import LSRMapping
from backend.app.models.evidence_span import EvidenceSpan
from backend.app.models.pattern_cluster import RecurringPattern
from backend.app.models.pattern_membership import PatternMembership
from backend.app.models.hse_prioritization import HSEPrioritization
from backend.app.models.human_review import HumanReview
from backend.app.models.audit_event import AuditEvent
from backend.app.models.lsr_catalog import LSRReferenceCatalog

__all__ = [
    # Enums
    "SourceType",
    "AppRole",
    "ReportType",
    "OutcomeSeverity",
    "ProcessingStatus",
    "ReleaseState",
    "ExecutionStatus",
    "EntityClass",
    "SignalCategory",
    "SignalStatus",
    "SIFPotential",
    "PriorityLevel",
    "BarrierCategory",
    "BarrierStatus",
    "MappingMechanism",
    "TargetEntityType",
    "SeverityTier",
    "PatternStatus",
    "PrioritizationTargetType",
    "UrgencyLevel",
    "ReviewAction",
    # Models
    "DataSource",
    "AppUser",
    "ModelVersion",
    "RuleVersion",
    "SafetyReport",
    "ProcessingRun",
    "SafetyEntity",
    "SafetyRelation",
    "SafetySignal",
    "SIFAssessment",
    "BarrierFinding",
    "LSRMapping",
    "EvidenceSpan",
    "RecurringPattern",
    "PatternMembership",
    "HSEPrioritization",
    "HumanReview",
    "AuditEvent",
    "LSRReferenceCatalog",
]
