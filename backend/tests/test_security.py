"""
Tests for Core Security Utilities
Validates bcrypt non-deterministic salting, JWT token flow, SHA-256 audit chaining,
and structured PII sanitization.
"""

from backend.app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    calculate_sha256,
    chain_audit_event,
    sanitize_pii,
)


def test_password_hashing_and_verification():
    """
    Verify password hashing produces a valid bcrypt hash,
    hashes are non-deterministic due to random salt, and
    verification validates matching passwords while rejecting mismatches.
    """
    password = "OilSecurePassword2026!"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Valid bcrypt hash structure
    assert hash1.startswith("$2")
    assert hash2.startswith("$2")

    # Bcrypt salting makes consecutive hashes distinct
    assert hash1 != hash2

    # Verification against generated hashes
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True
    assert verify_password("WrongPassword123", hash1) is False


def test_jwt_encode_and_decode():
    """Verify JWT token encoding, claims preservation, and decoding."""
    payload = {"sub": "oil-employee-001", "role": "HSE_MANAGER"}
    token = create_access_token(payload)

    assert isinstance(token, str)
    decoded = decode_access_token(token)

    assert decoded["sub"] == "oil-employee-001"
    assert decoded["role"] == "HSE_MANAGER"
    assert "exp" in decoded
    assert "iat" in decoded


def test_sha256_and_audit_chaining():
    """Verify SHA-256 digest computation and deterministic audit hash chaining."""
    h1 = calculate_sha256("genesis-block")
    assert len(h1) == 64

    event_payload = {"incident_id": "INC-2026-001", "status": "REPORTED"}
    chained_hash = chain_audit_event(h1, event_payload)
    assert len(chained_hash) == 64
    assert chained_hash != h1


def test_structured_pii_sanitization():
    """
    Verify structured PII (phone, email, badge ID) is sanitized,
    while non-structured text and arbitrary person names remain intact.
    """
    raw_text = (
        "Supervisor Ramesh Kumar (EMP-84721) reported an issue. "
        "Contact him at ramesh.kumar@oilindia.in or +91-9876543210 regarding Rig 4."
    )
    sanitized = sanitize_pii(raw_text)

    # Structured identifiers are masked
    assert "EMP-84721" not in sanitized
    assert "[ID_MASKED]" in sanitized
    assert "ramesh.kumar@oilindia.in" not in sanitized
    assert "[EMAIL_MASKED]" in sanitized
    assert "+91-9876543210" not in sanitized
    assert "[PHONE_MASKED]" in sanitized

    # Arbitrary person name is NOT stripped by regex
    assert "Ramesh Kumar" in sanitized
    assert "Rig 4" in sanitized
