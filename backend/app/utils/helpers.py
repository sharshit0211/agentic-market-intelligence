from __future__ import annotations

import uuid
from datetime import datetime, timezone


def generate_uuid() -> uuid.UUID:
    """Generate a new UUID4."""
    return uuid.uuid4()


def get_utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)


def sanitize_url(url: str) -> str:
    """Clean and normalize a URL."""
    url = url.strip()
    if url and not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    return url

