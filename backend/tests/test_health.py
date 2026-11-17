from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """Health endpoint returns 200 with correct structure."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_health_has_app_name(client):
    """Health response includes the application name."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["app_name"] == "MarketIntel AI"


@pytest.mark.asyncio
async def test_health_readiness(client):
    """Readiness endpoint returns 200 with database status."""
    response = await client.get("/api/v1/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "ready", "degraded")
    assert data["database"] in ("available", "connected", "unavailable")
