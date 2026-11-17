from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.competitor import Competitor
    from app.models.report import GeneratedReport
    from app.models.user import User


class ResearchProject(TimestampMixin, Base):
    __tablename__ = "research_projects"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="draft", nullable=False
    )
    industry: Mapped[str | None] = mapped_column(String(255), nullable=True)
    keywords: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    user: Mapped[User] = relationship(back_populates="research_projects")
    tasks: Mapped[list[ResearchTask]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    competitors: Mapped[list[Competitor]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    reports: Mapped[list[GeneratedReport]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ResearchProject {self.title}>"


class ResearchTask(TimestampMixin, Base):
    __tablename__ = "research_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("research_projects.id", ondelete="CASCADE"), nullable=False
    )
    task_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # scrape | analyze | report | monitor
    status: Mapped[str] = mapped_column(
        String(50), default="pending", nullable=False
    )  # pending | running | completed | failed | cancelled
    config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    project: Mapped[ResearchProject] = relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"<ResearchTask {self.task_type} — {self.status}>"

