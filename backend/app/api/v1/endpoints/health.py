"""
Health and Readiness Endpoints
Provides liveness (/health) and database readiness (/health/ready) checks.
"""

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from typing import Optional

from backend.app.core.config import settings
from backend.app.db.session import check_db_health

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str


class ReadinessResponse(BaseModel):
    status: str
    database: str
    service: str
    version: str
    detail: Optional[str] = None


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service Liveness Probe",
    description="Returns 200 if the backend process is running.",
)
def get_health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="oil-safety-intelligence-backend",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    summary="Service Readiness Probe",
    description="Checks downstream database connectivity. Returns 200 if ready, 503 if database disconnected.",
)
def get_readiness(response: Response) -> ReadinessResponse:
    db_connected, err = check_db_health()
    if db_connected:
        return ReadinessResponse(
            status="ready",
            database="connected",
            service="oil-safety-intelligence-backend",
            version=settings.APP_VERSION,
        )

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadinessResponse(
        status="degraded",
        database="disconnected",
        service="oil-safety-intelligence-backend",
        version=settings.APP_VERSION,
        detail="Database unreachable or not yet ready",
    )
