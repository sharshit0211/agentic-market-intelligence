from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.research import ResearchProject


class GeneratedReport(TimestampMixin, Base):
    __tablename__ = "generated_reports"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    report_type: Mapped[str] = mapped_column(
        String(50), default="market_analysis", nullable=False
    )  # market_analysis | competitor_comparison | trend_report | custom
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    format: Mapped[str] = mapped_column(
        "format", String(20), default="markdown", nullable=False
    )  # markdown | html | pdf
    status: Mapped[str] = mapped_column(
        String(50), default="generating", nullable=False
    )  # generating | completed | failed
    metadata_: Mapped[dict | None] = mapped_column(
        "metadata", JSON, nullable=True
    )

    # Relationships
    project: Mapped[ResearchProject] = relationship(back_populates="reports")

    def __repr__(self) -> str:
        return f"<GeneratedReport {self.title}>"

