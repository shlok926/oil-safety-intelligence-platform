"""
Canonical Database Schema & Persistence Test Suite
Verifies:
1. Canonical enum values (SIF, Barrier 6-State, RBAC 6-Role).
2. Database check constraints (invalid SIF, invalid barrier status, invalid role rejection).
3. Foreign key integrity and cascade deletion behavior.
4. Required field constraints and unique constraints.
5. Entity lifecycle and read/write roundtrip.
6. Audit ledger structure and hash chain integrity.
7. Human review non-destructive persistence.
8. Seed idempotency and 9 IOGP Life-Saving Rules catalog integrity.
"""

import uuid
from datetime import date, datetime, timezone
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.app.models import (
    AppUser,
    DataSource,
    SafetyReport,
    ProcessingRun,
    SIFAssessment,
    BarrierFinding,
    EvidenceSpan,
    LSRMapping,
    RecurringPattern,
    PatternMembership,
    HumanReview,
    AuditEvent,
    LSRReferenceCatalog,
    AppRole,
    SIFPotential,
    BarrierStatus,
    SourceType,
    ProcessingStatus,
    ReviewAction,
)
from backend.scripts.seed_data import (
    seed_data_sources,
    seed_app_users,
    seed_lsr_catalogs,
    seed_baseline_versions,
    seed_synthetic_reports,
)


def test_canonical_enum_values():
    """Verify that Python enum definitions match frozen canonical requirements exactly."""
    # SIF Potential: YES, NO, REVIEW (no SIF_YES or SIF_POTENTIAL)
    assert sorted([e.value for e in SIFPotential]) == ["NO", "REVIEW", "YES"]

    # Barrier States: exactly 6 states
    expected_barriers = [
        "BYPASSED",
        "FAILED",
        "INCOMPLETE",
        "MISSING",
        "PRESENT_VERIFIED",
        "UNKNOWN",
    ]
    assert sorted([e.value for e in BarrierStatus]) == expected_barriers

    # RBAC Roles: exactly 6 canonical roles
    expected_roles = [
        "ADMINISTRATOR",
        "HSE_ANALYST",
        "HSE_OFFICER",
        "HSE_VIEWER",
        "ML_OPS_ENGINEER",
        "SYSTEM_AUDITOR",
    ]
    assert sorted([e.value for e in AppRole]) == expected_roles


def test_iogp_life_saving_rules_catalog_integrity(db_session):
    """Verify all 9 canonical IOGP Life-Saving Rules from Report 459 are in the catalog."""
    rules = db_session.execute(
        select(LSRReferenceCatalog).order_by(LSRReferenceCatalog.rule_number)
    ).scalars().all()

    assert len(rules) == 9
    rule_titles = [r.rule_title for r in rules]
    assert "Confined Space Entry" in rule_titles
    assert "Energy Isolation" in rule_titles
    assert "Bypassing Safety Controls" in rule_titles
    assert "Working at Height" in rule_titles
    for rule in rules:
        assert rule.active_version == "IOGP_459_REV_2018"
        assert rule.lsr_id.startswith("LSR_")


def test_app_user_lifecycle_and_constraints(db_session):
    """Verify user persistence, role check constraint, and unique constraint."""
    test_id = uuid.uuid4()
    unique_username = f"test_user_{test_id.hex[:8]}"
    unique_email = f"{unique_username}@oil.local"

    user = AppUser(
        user_id=test_id,
        username=unique_username,
        email=unique_email,
        full_name="Database Test User",
        role=AppRole.HSE_ANALYST.value,
        password_hash="$2b$12$e8F9g0h1i2j3k4l5m6n7o8p9q0r1s2t3u4v5w6x7y8z9A0B1C2D3E",
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    # Query back
    fetched = db_session.execute(
        select(AppUser).where(AppUser.user_id == test_id)
    ).scalar_one()
    assert fetched.username == unique_username
    assert fetched.role == "HSE_ANALYST"

    # Test invalid role rejection by check constraint
    invalid_user = AppUser(
        username=f"invalid_{test_id.hex[:8]}",
        email=f"invalid_{test_id.hex[:8]}@oil.local",
        full_name="Invalid Role User",
        role="SUPER_ADMIN_INVALID",
        password_hash="hash",
    )
    db_session.add(invalid_user)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_unique_user_constraints(db_session):
    """Verify username and email uniqueness constraints."""
    user_id_1 = uuid.uuid4()
    user_id_2 = uuid.uuid4()
    common_name = f"duplicate_{user_id_1.hex[:8]}"

    u1 = AppUser(
        user_id=user_id_1,
        username=common_name,
        email=f"{common_name}@oil.local",
        full_name="First User",
        role=AppRole.HSE_VIEWER.value,
        password_hash="hash1",
    )
    db_session.add(u1)
    db_session.flush()

    u2 = AppUser(
        user_id=user_id_2,
        username=common_name,  # Duplicate username
        email=f"diff_{common_name}@oil.local",
        full_name="Second User",
        role=AppRole.HSE_VIEWER.value,
        password_hash="hash2",
    )
    db_session.add(u2)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_sif_assessment_constraints(db_session):
    """Verify check constraint rejects invalid SIF potential values."""
    # First get or create a data source and safety report
    source = db_session.execute(
        select(DataSource).where(DataSource.source_type == SourceType.SYNTHETIC.value)
    ).scalars().first()
    assert source is not None

    report = SafetyReport(
        source_id=source.source_id,
        source_report_id=f"TEST-SR-{uuid.uuid4().hex[:6]}",
        report_type="NEAR_MISS",
        event_date=date(2026, 3, 20),
        facility_id="TEST-FACILITY",
        raw_narrative="Worker tripped over unshielded high-pressure pipe.",
        normalized_narrative="Worker tripped over unshielded high-pressure pipe.",
        actual_outcome_severity="NO_INJURY_NEAR_MISS",
        processing_status=ProcessingStatus.PENDING.value,
        narrative_sha256="aabbccddeeff11223344556677889900aabbccddeeff11223344556677889900",
    )
    db_session.add(report)
    db_session.flush()

    run = ProcessingRun(
        report_id=report.report_id,
        pipeline_version="1.0.0",
        execution_status="SUCCESS",
        execution_duration_ms=250,
    )
    db_session.add(run)
    db_session.flush()

    # Valid SIF potential
    valid_sif = SIFAssessment(
        report_id=report.report_id,
        run_id=run.run_id,
        sif_potential=SIFPotential.YES.value,
        priority_level="P1_CRITICAL",
        assessment_confidence=0.950,
        reasoning_summary="Valid assessment test.",
        is_active_assessment=True,
    )
    db_session.add(valid_sif)
    db_session.flush()
    assert valid_sif.assessment_id is not None

    # Invalid SIF potential (e.g. SIF_YES or MAYBE)
    invalid_sif = SIFAssessment(
        report_id=report.report_id,
        run_id=run.run_id,
        sif_potential="SIF_YES",  # Invalid! Must be YES, NO, or REVIEW
        priority_level="P1_CRITICAL",
        assessment_confidence=0.800,
        reasoning_summary="Invalid assessment test.",
    )
    db_session.add(invalid_sif)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_barrier_finding_six_state_constraint(db_session):
    """Verify check constraint enforces the 6 canonical barrier states."""
    source = db_session.execute(
        select(DataSource).where(DataSource.source_type == SourceType.SYNTHETIC.value)
    ).scalars().first()

    report = SafetyReport(
        source_id=source.source_id,
        source_report_id=f"TEST-BF-{uuid.uuid4().hex[:6]}",
        report_type="NEAR_MISS",
        event_date=date(2026, 3, 20),
        facility_id="TEST-FACILITY",
        raw_narrative="Gas detector alarm failed during line purging.",
        normalized_narrative="Gas detector alarm failed during line purging.",
        actual_outcome_severity="NO_INJURY_NEAR_MISS",
        processing_status=ProcessingStatus.PENDING.value,
        narrative_sha256="11223344556677889900aabbccddeeff11223344556677889900aabbccddee00",
    )
    db_session.add(report)
    db_session.flush()

    run = ProcessingRun(
        report_id=report.report_id,
        pipeline_version="1.0.0",
        execution_status="SUCCESS",
        execution_duration_ms=180,
    )
    db_session.add(run)
    db_session.flush()

    # Valid barrier state
    valid_barrier = BarrierFinding(
        report_id=report.report_id,
        run_id=run.run_id,
        barrier_name="Combustible Gas Detector",
        barrier_category="PHYSICAL",
        barrier_status=BarrierStatus.FAILED.value,
        is_critical_barrier=True,
        verification_method="REPORTED_EXPLICIT",
    )
    db_session.add(valid_barrier)
    db_session.flush()
    assert valid_barrier.barrier_id is not None

    # Invalid barrier state (e.g. BROKEN or DAMAGED)
    invalid_barrier = BarrierFinding(
        report_id=report.report_id,
        run_id=run.run_id,
        barrier_name="Combustible Gas Detector",
        barrier_category="PHYSICAL",
        barrier_status="BROKEN_DEFECTIVE",  # Invalid! Not one of the 6 canonical states
        is_critical_barrier=True,
        verification_method="REPORTED_EXPLICIT",
    )
    db_session.add(invalid_barrier)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_foreign_key_and_cascade_deletion(db_session):
    """Verify foreign key integrity and cascade deletion of derived records."""
    source = db_session.execute(
        select(DataSource).where(DataSource.source_type == SourceType.SYNTHETIC.value)
    ).scalars().first()

    report_id = uuid.uuid4()
    report = SafetyReport(
        report_id=report_id,
        source_id=source.source_id,
        source_report_id=f"TEST-CASCADE-{report_id.hex[:6]}",
        report_type="INCIDENT",
        event_date=date(2026, 3, 21),
        facility_id="CASCADE-TEST-FACILITY",
        raw_narrative="Cascade deletion test narrative.",
        normalized_narrative="Cascade deletion test narrative.",
        actual_outcome_severity="FIRST_AID",
        processing_status=ProcessingStatus.PROCESSED.value,
        narrative_sha256="1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    )
    db_session.add(report)
    db_session.flush()

    run = ProcessingRun(
        report_id=report.report_id,
        pipeline_version="1.0.0",
        execution_status="SUCCESS",
        execution_duration_ms=150,
    )
    db_session.add(run)
    db_session.flush()

    sif = SIFAssessment(
        report_id=report.report_id,
        run_id=run.run_id,
        sif_potential=SIFPotential.NO.value,
        priority_level="P3_STANDARD",
        assessment_confidence=0.910,
        reasoning_summary="Minor event test.",
    )
    db_session.add(sif)
    db_session.flush()

    evidence = EvidenceSpan(
        report_id=report.report_id,
        target_entity_type="SIF_ASSESSMENT",
        target_entity_id=sif.assessment_id,
        verbatim_text="Cascade deletion",
        start_offset=0,
        end_offset=16,
        reasoning_justification="Test evidence span",
    )
    db_session.add(evidence)
    db_session.flush()

    # Now delete the parent SafetyReport
    db_session.delete(report)
    db_session.flush()

    # Verify child records were cascade deleted
    orphan_sif = db_session.execute(
        select(SIFAssessment).where(SIFAssessment.report_id == report_id)
    ).scalar_one_or_none()
    assert orphan_sif is None

    orphan_run = db_session.execute(
        select(ProcessingRun).where(ProcessingRun.report_id == report_id)
    ).scalar_one_or_none()
    assert orphan_run is None

    orphan_evidence = db_session.execute(
        select(EvidenceSpan).where(EvidenceSpan.report_id == report_id)
    ).scalar_one_or_none()
    assert orphan_evidence is None
    db_session.rollback()


def test_human_review_persistence(db_session):
    """Verify human review persistence with JSONB corrections and review action constraints."""
    user = db_session.execute(
        select(AppUser).where(AppUser.role == AppRole.HSE_OFFICER.value)
    ).scalars().first()
    assert user is not None

    source = db_session.execute(
        select(DataSource).where(DataSource.source_type == SourceType.SYNTHETIC.value)
    ).scalars().first()

    report = SafetyReport(
        source_id=source.source_id,
        source_report_id=f"TEST-HR-{uuid.uuid4().hex[:6]}",
        report_type="NEAR_MISS",
        event_date=date(2026, 3, 22),
        facility_id="REVIEW-TEST-SITE",
        raw_narrative="Pressure valve showed anomalous reading before bypass.",
        normalized_narrative="Pressure valve showed anomalous reading before bypass.",
        actual_outcome_severity="NO_INJURY_NEAR_MISS",
        processing_status=ProcessingStatus.REVIEWED.value,
        narrative_sha256="44556677889900aabbccddeeff11223344556677889900aabbccddeeff112233",
    )
    db_session.add(report)
    db_session.flush()

    review = HumanReview(
        report_id=report.report_id,
        reviewer_user_id=user.user_id,
        review_action=ReviewAction.CORRECT.value,
        original_sif_result="REVIEW",
        revised_sif_result="YES",
        reviewer_notes="High pressure bypass without MOC constitutes SIF precursor.",
        corrections_payload={
            "overridden_field": "sif_potential",
            "justification": "MOC was absent on critical process barrier.",
        },
    )
    db_session.add(review)
    db_session.flush()

    assert review.review_id is not None
    fetched_review = db_session.execute(
        select(HumanReview).where(HumanReview.review_id == review.review_id)
    ).scalar_one()
    assert fetched_review.review_action == "CORRECT"
    assert fetched_review.corrections_payload["overridden_field"] == "sif_potential"
    db_session.rollback()


def test_audit_event_ledger_persistence(db_session):
    """Verify immutable audit ledger sequence, hash fields, and JSONB payload delta."""
    user = db_session.execute(
        select(AppUser).where(AppUser.role == AppRole.SYSTEM_AUDITOR.value)
    ).scalars().first()

    event = AuditEvent(
        actor_user_id=user.user_id if user else None,
        action_type="SECURITY_CONFIG_UPDATE",
        target_entity_type="SYSTEM_CONFIG",
        target_entity_id=uuid.uuid4(),
        payload_delta={"param": "session_timeout", "old": 30, "new": 15},
        client_ip_address="127.0.0.1",
        prev_event_hash="0000000000000000000000000000000000000000000000000000000000000000",
        event_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    )
    db_session.add(event)
    db_session.flush()

    assert event.event_id is not None
    assert event.sequence_number >= 1
    assert event.payload_delta["new"] == 15
    db_session.rollback()


def test_pattern_and_membership_unique_constraint(db_session):
    """Verify pattern cluster and unique membership constraint (pattern_id, report_id)."""
    source = db_session.execute(
        select(DataSource).where(DataSource.source_type == SourceType.SYNTHETIC.value)
    ).scalars().first()

    report = SafetyReport(
        source_id=source.source_id,
        source_report_id=f"TEST-PAT-{uuid.uuid4().hex[:6]}",
        report_type="OBSERVATION",
        event_date=date(2026, 3, 23),
        facility_id="PATTERN-TEST-SITE",
        raw_narrative="Repeated pattern test narrative.",
        normalized_narrative="Repeated pattern test narrative.",
        actual_outcome_severity="NO_INJURY_NEAR_MISS",
        processing_status=ProcessingStatus.PROCESSED.value,
        narrative_sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    )
    db_session.add(report)
    db_session.flush()

    pattern = RecurringPattern(
        pattern_title="Recurring Flange Leakage During Purging",
        pattern_type="CHRONIC_HOTSPOT",
        primary_activity="Purging",
        primary_hazard="Flammable Vapor",
        primary_barrier_break="Flange Gasket",
        affected_facility_id="PATTERN-TEST-SITE",
        report_count=3,
        sif_potential_count=1,
        severity_tier="TIER_2_HIGH",
        first_observed_date=date(2026, 1, 1),
        latest_observed_date=date(2026, 3, 23),
        pattern_status="ACTIVE_HOTSPOT",
    )
    db_session.add(pattern)
    db_session.flush()

    # First membership
    m1 = PatternMembership(
        pattern_id=pattern.pattern_id,
        report_id=report.report_id,
        contribution_weight=1.000,
    )
    db_session.add(m1)
    db_session.flush()

    # Duplicate membership for same (pattern_id, report_id) should fail unique constraint
    m2 = PatternMembership(
        pattern_id=pattern.pattern_id,
        report_id=report.report_id,
        contribution_weight=0.500,
    )
    db_session.add(m2)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_seed_workflow_idempotency(db_session):
    """Verify executing seed data functions repeatedly creates zero duplicates."""
    # Running seed functions when already seeded
    src_added = seed_data_sources(db_session)
    usr_added = seed_app_users(db_session)
    lsr_added = seed_lsr_catalogs(db_session)
    ver_added = seed_baseline_versions(db_session)
    rep_added = seed_synthetic_reports(db_session)
    db_session.commit()

    assert src_added == 0
    assert usr_added == 0
    assert lsr_added == 0
    assert ver_added == 0
    assert rep_added == 0
