"""
Domain Schemas and Data Transfer Objects
Standard Pydantic models for Incident narratives, Precursor Triad, and Safety Barriers.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PrecursorTriad(BaseModel):
    """Precursor Triad domain structure."""
    activity: str = Field(..., description="Operational activity during event (e.g., Tripping pipe)")
    mechanism: str = Field(..., description="Accident mechanism or physical hazard (e.g., Caught between)")
    energy_source: str = Field(..., description="Dominant energy source (e.g., Mechanical / Tension)")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class BarrierStatus(BaseModel):
    """Safety Barrier state model."""
    barrier_id: str
    barrier_name: str
    category: str  # Physical, Engineered, Administrative
    status: str    # INTACT, DEGRADED, FAILED, MISSING, UNKNOWN
    rationale: Optional[str] = None


class IncidentPayload(BaseModel):
    """Incident report input data contract."""
    incident_id: str
    title: str
    narrative: str
    location: str
    date_time: str
    reporter_id: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None
