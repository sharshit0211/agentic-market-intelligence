from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import get_settings
from app.database.session import _get_engine
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
@router.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Basic liveness check."""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.VERSION,
        environment=settings.APP_ENV,
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/ready", response_model=ReadinessResponse)
async def readiness_check() -> ReadinessResponse:
    """Deep readiness check including database connectivity."""
    db_status = "unavailable"
    try:
        engine = _get_engine()
        async with asyncio.timeout(2.0):
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            db_status = "available"
    except Exception:
        db_status = "unavailable"

    status = "healthy" if db_status == "available" else "degraded"
    return ReadinessResponse(
        status=status,
        database=db_status,
        timestamp=datetime.now(timezone.utc),
    )
