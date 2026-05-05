"""SQLAlchemy database models."""

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    brand_kit_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("brand_kits.id"), nullable=True
    )
    canvas_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=now_utc, onupdate=now_utc
    )

    artboards: Mapped[list["Artboard"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    brand_kit: Mapped["BrandKit | None"] = relationship(back_populates="projects")


class Artboard(Base):
    __tablename__ = "artboards"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False
    )
    width: Mapped[int] = mapped_column(Integer, nullable=False, default=1080)
    height: Mapped[int] = mapped_column(Integer, nullable=False, default=1080)
    bg_color: Mapped[str] = mapped_column(String, nullable=False, default="#FFFFFF")
    layers_json: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=now_utc, onupdate=now_utc
    )

    project: Mapped["Project"] = relationship(back_populates="artboards")
    layers: Mapped[list["Layer"]] = relationship(back_populates="artboard", cascade="all, delete-orphan")


class Layer(Base):
    __tablename__ = "layers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    artboard_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("artboards.id"), nullable=False
    )
    type: Mapped[str] = mapped_column(String, nullable=False)  # text | shape | image | group
    name: Mapped[str] = mapped_column(String, nullable=False, default="Layer")
    transform_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    style_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_generated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ai_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=now_utc, onupdate=now_utc
    )

    artboard: Mapped["Artboard"] = relationship(back_populates="layers")


class BrandKit(Base):
    __tablename__ = "brand_kits"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    colors: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    fonts: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    tone_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=now_utc, onupdate=now_utc
    )

    projects: Mapped[list["Project"]] = relationship(back_populates="brand_kit")


class Generation(Base):
    __tablename__ = "generations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    model_used: Mapped[str] = mapped_column(String, nullable=False)
    output_urls: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    meta: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=now_utc)


class Template(Base):
    __tablename__ = "templates"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    canvas_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    usage_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=now_utc, onupdate=now_utc
    )
