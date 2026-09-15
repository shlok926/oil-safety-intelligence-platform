"""
Canonical Seed Data Workflow
Seeds bootstrap reference catalogs, app users, data sources, baseline versions,
and synthetic benchmark records for the OIL Safety Intelligence Platform.

Usage:
    python -m backend.scripts.seed_data
"""

import os
import sys
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import select

from backend.app.core.logging import setup_logging, get_logger
from backend.app.core.security import get_password_hash, calculate_sha256
from backend.app.db.session import SessionLocal, check_db_health
from backend.app.models import (
    AppUser,
    DataSource,
    LSRReferenceCatalog,
    ModelVersion,
    RuleVersion,
    SafetyReport,
    AppRole,
    SourceType,
    ProcessingStatus,
    ReleaseState,
)

setup_logging()
logger = get_logger("seed_data")

# Fixed canonical UUIDs for deterministic bootstrap references
SYNTHETIC_SOURCE_ID = uuid.UUID("9a8b7c6d-1e2f-3a4b-5c6d-7e8f9a0b1c2d")
PUBLIC_SOURCE_ID = uuid.UUID("8a7b6c5d-2e3f-4a5b-6c7d-8e9f0a1b2c3d")
OIL_METADATA_SOURCE_ID = uuid.UUID("7a6b5c4d-3e4f-5a6b-7c8d-9e0f1a2b3c4d")

BASELINE_MODEL_ID = uuid.UUID("11111111-2222-3333-4444-555555555555")
BASELINE_RULE_ID = uuid.UUID("22222222-3333-4444-5555-666666666666")

SAMPLE_REPORT_1_ID = uuid.UUID("c1f7a240-8f63-4b6e-a28a-7d4e5f1b2c3d")
SAMPLE_REPORT_2_ID = uuid.UUID("c2f8b351-9f74-4c7f-b39b-8e5f6a2b3c4e")


def seed_data_sources(db) -> int:
    """Seed canonical data sources (idempotent)."""
    sources = [
        {
            "source_id": SYNTHETIC_SOURCE_ID,
            "source_name": "Hackathon-MVD-60-Synthetic",
            "source_type": SourceType.SYNTHETIC.value,
            "license_or_nda_ref": "Tech Smashers Synthetic Safety Dataset v1.0",
            "acquisition_date": date(2026, 1, 15),
            "contains_pii": False,
            "description": "Synthetic safety incident and near-miss reports calibrated against energy-based SIF taxonomies.",
        },
        {
            "source_id": PUBLIC_SOURCE_ID,
            "source_name": "OSHA-Public-Incident-Reports",
            "source_type": SourceType.PUBLIC.value,
            "license_or_nda_ref": "Public Domain / OSHA Open Data",
            "acquisition_date": date(2026, 1, 10),
            "contains_pii": False,
            "description": "Publicly available anonymized oil & gas industrial incident records for benchmark testing.",
        },
        {
            "source_id": OIL_METADATA_SOURCE_ID,
            "source_name": "OIL-Internal-HSE-Metadata",
            "source_type": SourceType.AUTHORIZED_OIL.value,
            "license_or_nda_ref": "SIH26165 Problem Statement Metadata Definition",
            "acquisition_date": date(2026, 2, 1),
            "contains_pii": True,
            "description": "Metadata container reserved for authorized Oil India Limited internal HSE observation schemas.",
        },
    ]

    added = 0
    for src in sources:
        existing = db.execute(
            select(DataSource).where(DataSource.source_id == src["source_id"])
        ).scalar_one_or_none()
        if not existing:
            db.add(DataSource(**src))
            added += 1
    return added


def get_seed_password() -> str:
    """
    Retrieve seed password from environment variable SEED_DEFAULT_PASSWORD.
    Uses a clearly documented development-only placeholder strategy if not provided.
    Never logs or prints the password.
    """
    pwd = os.getenv("SEED_DEFAULT_PASSWORD")
    if not pwd:
        logger.info("SEED_DEFAULT_PASSWORD environment variable not set. Using dev placeholder strategy.")
        pwd = "dev_placeholder_seed_credential_unusable_in_production"
    return pwd


def seed_app_users(db) -> int:
    """Seed canonical development users with bcrypt-hashed passwords for all 6 roles (idempotent)."""
    raw_password = get_seed_password()
    default_dev_hash = get_password_hash(raw_password)
    users = [
        {
            "username": "hse_viewer",
            "email": "viewer@oil.local",
            "full_name": "HSE Field Viewer",
            "role": AppRole.HSE_VIEWER.value,
            "password_hash": default_dev_hash,
            "is_active": True,
        },
        {
            "username": "hse_analyst",
            "email": "analyst@oil.local",
            "full_name": "HSE Safety Data Analyst",
            "role": AppRole.HSE_ANALYST.value,
            "password_hash": default_dev_hash,
            "is_active": True,
        },
        {
            "username": "hse_officer",
            "email": "officer@oil.local",
            "full_name": "HSE Senior Officer",
            "role": AppRole.HSE_OFFICER.value,
            "password_hash": default_dev_hash,
            "is_active": True,
        },
        {
            "username": "oil_admin",
            "email": "admin@oil.local",
            "full_name": "System Administrator",
            "role": AppRole.ADMINISTRATOR.value,
            "password_hash": default_dev_hash,
            "is_active": True,
        },
        {
            "username": "system_auditor",
            "email": "auditor@oil.local",
            "full_name": "Safety Compliance Auditor",
            "role": AppRole.SYSTEM_AUDITOR.value,
            "password_hash": default_dev_hash,
            "is_active": True,
        },
        {
            "username": "ml_ops",
            "email": "mlops@oil.local",
            "full_name": "ML Operations Engineer",
            "role": AppRole.ML_OPS_ENGINEER.value,
            "password_hash": default_dev_hash,
            "is_active": True,
        },
    ]

    added = 0
    for u in users:
        existing = db.execute(
            select(AppUser).where(AppUser.username == u["username"])
        ).scalar_one_or_none()
        if not existing:
            db.add(AppUser(**u))
            added += 1
    return added


def seed_lsr_catalogs(db) -> int:
    """Seed the 9 canonical IOGP Life-Saving Rules from Report 459 (idempotent)."""
    rules = [
        {
            "lsr_id": "LSR_BYPASSING_SAFETY_CONTROLS",
            "rule_number": 1,
            "rule_title": "Bypassing Safety Controls",
            "icon_name": "shield-alert",
            "canonical_definition": "Obtain authorization before overriding or disabling safety controls.",
            "active_version": "IOGP_459_REV_2018",
        },
        {
            "lsr_id": "LSR_CONFINED_SPACE",
            "rule_number": 2,
            "rule_title": "Confined Space Entry",
            "icon_name": "door-closed",
            "canonical_definition": "Obtain authorization before entering a confined space.",
            "active_version": "IOGP_459_REV_2018",
        },
        {
            "lsr_id": "LSR_DRIVING",
            "rule_number": 3,
            "rule_title": "Driving",
            "icon_name": "truck",
            "canonical_definition": "Follow safe driving rules: vehicle pre-check, speed compliance, seatbelts, no mobile phone use.",
            "active_version": "IOGP_459_REV_2018",
        },
        {
            "lsr_id": "LSR_ENERGY_ISOLATION",
            "rule_number": 4,
            "rule_title": "Energy Isolation",
            "icon_name": "lock",
            "canonical_definition": "Verify isolation and zero energy before work begins.",
            "active_version": "IOGP_459_REV_2018",
        },
        {
            "lsr_id": "LSR_HOT_WORK",
            "rule_number": 5,
            "rule_title": "Hot Work",
            "icon_name": "flame",
            "canonical_definition": "Control flammables and ignition sources.",
            "active_version": "IOGP_459_REV_2018",
        },
        {
            "lsr_id": "LSR_LINE_OF_FIRE",
            "rule_number": 6,
            "rule_title": "Line of Fire",
            "icon_name": "target",
            "canonical_definition": "Keep yourself and others out of the line of fire.",
            "active_version": "IOGP_459_REV_2018",
        },
        {
            "lsr_id": "LSR_SAFE_MECHANICAL_LIFTING",
            "rule_number": 7,
            "rule_title": "Safe Mechanical Lifting",
            "icon_name": "crane",
            "canonical_definition": "Plan lifting operations and control the area.",
            "active_version": "IOGP_459_REV_2018",
        },
        {
            "lsr_id": "LSR_WORK_AUTHORIZATION",
            "rule_number": 8,
            "rule_title": "Work Authorization",
            "icon_name": "file-check",
            "canonical_definition": "Work with a valid permit when required.",
            "active_version": "IOGP_459_REV_2018",
        },
        {
            "lsr_id": "LSR_WORKING_AT_HEIGHT",
            "rule_number": 9,
            "rule_title": "Working at Height",
            "icon_name": "ladder",
            "canonical_definition": "Protect yourself against a fall when working at height.",
            "active_version": "IOGP_459_REV_2018",
        },
    ]

    added = 0
    for r in rules:
        existing = db.execute(
            select(LSRReferenceCatalog).where(LSRReferenceCatalog.lsr_id == r["lsr_id"])
        ).scalar_one_or_none()
        if not existing:
            db.add(LSRReferenceCatalog(**r))
            added += 1
    return added


def seed_baseline_versions(db) -> int:
    """Seed baseline model version and deterministic rule version (idempotent)."""
    added = 0
    existing_model = db.execute(
        select(ModelVersion).where(ModelVersion.model_version_id == BASELINE_MODEL_ID)
    ).scalar_one_or_none()
    if not existing_model:
        db.add(
            ModelVersion(
                model_version_id=BASELINE_MODEL_ID,
                model_name="all-MiniLM-L6-v2-sif-classifier",
                semantic_version="1.0.0",
                model_architecture="SentenceTransformer-MiniLM-L6-v2",
                training_dataset_ref="synthetic-sif-precursor-v1.0",
                release_state=ReleaseState.ACTIVE_PRODUCTION.value,
                release_date=date(2026, 2, 1),
            )
        )
        added += 1

    existing_rule = db.execute(
        select(RuleVersion).where(RuleVersion.rule_version_id == BASELINE_RULE_ID)
    ).scalar_one_or_none()
    if not existing_rule:
        db.add(
            RuleVersion(
                rule_version_id=BASELINE_RULE_ID,
                ruleset_name="sif-deterministic-decision-matrix",
                ruleset_semantic_ver="1.0.0",
                ruleset_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                ruleset_definition={
                    "ruleset_id": "SIF_RULES_V1",
                    "version": "1.0.0",
                    "thresholds": {"high_energy": True, "critical_barrier_missing": True},
                },
                is_active=True,
                effective_from=datetime.now(timezone.utc),
            )
        )
        added += 1

    return added


def seed_synthetic_reports(db) -> int:
    """Seed representative synthetic incident reports (idempotent)."""
    reports = [
        {
            "report_id": SAMPLE_REPORT_1_ID,
            "source_id": SYNTHETIC_SOURCE_ID,
            "source_report_id": "SYN-MVD-001",
            "report_type": "NEAR_MISS",
            "event_date": date(2026, 3, 15),
            "facility_id": "SITE-A-OILFIELD",
            "specific_location": "Vessel Separator Area V-101",
            "department": "Production Operations",
            "raw_narrative": "During maintenance activity at Site A, a technician entered a confined space before atmospheric testing was completed. No standby person was present. Work was stopped after supervisor noticed. No injuries occurred.",
            "normalized_narrative": "During maintenance activity at Site A, a technician entered a confined space before atmospheric gas testing was completed. No standby attendant was present. Work was stopped after supervisor noticed. No injuries occurred.",
            "actual_outcome_severity": "NO_INJURY_NEAR_MISS",
            "processing_status": ProcessingStatus.PROCESSED.value,
            "narrative_sha256": calculate_sha256(
                "During maintenance activity at Site A, a technician entered a confined space before atmospheric testing was completed. No standby person was present. Work was stopped after supervisor noticed. No injuries occurred."
            ),
        },
        {
            "report_id": SAMPLE_REPORT_2_ID,
            "source_id": SYNTHETIC_SOURCE_ID,
            "source_report_id": "SYN-MVD-002",
            "report_type": "OBSERVATION",
            "event_date": date(2026, 3, 16),
            "facility_id": "RIG-B-DRILLING",
            "specific_location": "Rig Floor Derrick Area",
            "department": "Drilling",
            "raw_narrative": "During high-pressure line rigging, crane hoisted a 2-ton drill pipe bundle without positive exclusion tag lines. Crew member walked directly beneath the suspended load. Load shifted slightly before crane operator stopped hoist.",
            "normalized_narrative": "During high-pressure line rigging, crane hoisted a 2-ton drill pipe bundle without positive exclusion tag lines. Crew member walked directly beneath the suspended load. Load shifted slightly before crane operator stopped hoist.",
            "actual_outcome_severity": "NO_INJURY_NEAR_MISS",
            "processing_status": ProcessingStatus.PENDING.value,
            "narrative_sha256": calculate_sha256(
                "During high-pressure line rigging, crane hoisted a 2-ton drill pipe bundle without positive exclusion tag lines. Crew member walked directly beneath the suspended load. Load shifted slightly before crane operator stopped hoist."
            ),
        },
    ]

    added = 0
    for rep in reports:
        existing = db.execute(
            select(SafetyReport).where(SafetyReport.report_id == rep["report_id"])
        ).scalar_one_or_none()
        if not existing:
            db.add(SafetyReport(**rep))
            added += 1
    return added


def main() -> int:
    """Execute complete seed data workflow."""
    logger.info("Executing canonical database seed workflow...")
    is_connected, err = check_db_health()
    if not is_connected:
        logger.error(f"Database connection failed: {err}")
        return 1

    db = SessionLocal()
    try:
        sources_added = seed_data_sources(db)
        users_added = seed_app_users(db)
        lsr_added = seed_lsr_catalogs(db)
        versions_added = seed_baseline_versions(db)
        reports_added = seed_synthetic_reports(db)
        db.commit()

        logger.info(
            f"Seed complete. New records added: DataSources={sources_added}, "
            f"Users={users_added}, LSRs={lsr_added}, Versions={versions_added}, "
            f"Reports={reports_added}"
        )
        return 0
    except Exception as exc:
        db.rollback()
        logger.error(f"Seed workflow failed: {exc}", exc_info=True)
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
