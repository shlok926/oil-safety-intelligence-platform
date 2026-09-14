"""
API Version 1 Main Router
Aggregates all version 1 endpoints.
"""

from fastapi import APIRouter
from backend.app.api.v1.endpoints import health

api_router = APIRouter()

# Mount health endpoints
api_router.include_router(health.router)
