from __future__ import annotations

import httpx
import pytest_asyncio
from app.main import app


@pytest_asyncio.fixture
async def client():
    """Async test client for FastAPI using httpx ASGITransport."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
