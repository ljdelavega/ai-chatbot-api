"""
API v1 router containing all version 1 endpoints.

This module defines the API routes for version 1 of the chat API.
"""

from datetime import datetime
from fastapi import APIRouter, Depends

from app.api.models import HealthResponse
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create API router
router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the health status of the API service"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint that returns the current status of the API.
    
    This endpoint is excluded from authentication and can be used
    for monitoring and load balancer health checks.
    
    Returns:
        HealthResponse: Current service status, timestamp, and version
    """
    logger.debug("Health check endpoint accessed")
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="0.1.0"
    ) 