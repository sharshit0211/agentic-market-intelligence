from __future__ import annotations

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None
    timestamp: datetime


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]  # type: ignore[type-var]
    total: int
    page: int
    page_size: int
    total_pages: int

