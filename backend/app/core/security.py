"""
Cryptographic, Hashing, Token, and Sanitization Utilities
Pure utility module for Phase 1 — intentionally without auth middleware,
login endpoints, user models, or RBAC dependencies.
"""

import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt
import bcrypt

from backend.app.core.config import settings

# Precompiled regex patterns for structured PII sanitization
# Note: Arbitrary person names are excluded from regex masking (deferred to NLP entity recognition)
PHONE_REGEX = re.compile(
    r"(?:\+?91[-.\s]?)?[6-9]\d{9}|\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
)
EMAIL_REGEX = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    re.IGNORECASE,
)
BADGE_ID_REGEX = re.compile(
    r"\b(?:EMP|BADGE|OIL|STAFF|ID)[-_]?\d{3,8}\b",
    re.IGNORECASE,
)


# --- Password Hashing Utilities ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8")[:72],
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Generate a secure bcrypt hash for a plain-text password."""
    # Adheres to bcrypt 72-byte limit
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8")[:72], salt).decode("utf-8")


# --- JWT Encode/Decode Utilities ---

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Encode a JWT access token with expiration claims."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError as exc:
        raise ValueError("Invalid or expired JWT token") from exc


# --- Cryptographic Audit Hashing ---

def calculate_sha256(data: str | bytes) -> str:
    """Calculate the SHA-256 hexadecimal digest of input data."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def chain_audit_event(prev_hash: str, event_payload: Dict[str, Any]) -> str:
    """
    Calculate the hash for an immutable audit trail entry:
    SHA-256(prev_hash + canonical_json(event_payload))
    """
    serialized = json.dumps(event_payload, sort_keys=True, separators=(",", ":"))
    content = f"{prev_hash}{serialized}"
    return calculate_sha256(content)


# --- Structured PII Sanitization ---

def sanitize_pii(text: str) -> str:
    """
    Mask structured identifiers (phone numbers, emails, badge/employee IDs).
    Arbitrary person names are NOT masked here with regex.
    """
    if not text:
        return ""

    sanitized = EMAIL_REGEX.sub("[EMAIL_MASKED]", text)
    sanitized = PHONE_REGEX.sub("[PHONE_MASKED]", sanitized)
    sanitized = BADGE_ID_REGEX.sub("[ID_MASKED]", sanitized)
    return sanitized
