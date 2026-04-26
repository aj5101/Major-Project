"""
Health Check Endpoint

Simple endpoint to verify the API is running and healthy.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns API status and timestamp.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ASL Video Narration Platform API"
    }

