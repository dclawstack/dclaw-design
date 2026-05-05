"""Pydantic v2 schemas for API requests and responses."""

import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class TransformSchema(BaseModel):
    x: float = 0.0
    y: float = 0.0
    width: float = 100.0
    height: float = 100.0
    rotation: float = 0.0


class StyleSchema(BaseModel):
    fill: str | None = None
    stroke: str | None = None
    strokeWidth: float | None = None
    fontFamily: str | None = None
    fontSize: float | None = None
    fontWeight: str | None = None
    opacity: float = 1.0


class LayerCreate(BaseModel):
    type: Literal["text", "shape", "image", "group"]
    name: str = "Layer"
    transform_json: TransformSchema = Field(default_factory=TransformSchema)
    style_json: StyleSchema = Field(default_factory=StyleSchema)
    content: str | None = None
    ai_generated: bool = False
    ai_prompt: str | None = None


class LayerUpdate(BaseModel):
    name: str | None = None
    transform_json: TransformSchema | None = None
    style_json: StyleSchema | None = None
    content: str | None = None
    ai_prompt: str | None = None


class LayerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    artboard_id: uuid.UUID
    type: str
    name: str
    transform_json: dict[str, Any]
    style_json: dict[str, Any]
    content: str | None
    ai_generated: bool
    ai_prompt: str | None
    created_at: datetime
    updated_at: datetime


class ArtboardCreate(BaseModel):
    width: int = 1080
    height: int = 1080
    bg_color: str = "#FFFFFF"
    sort_order: int = 0


class ArtboardUpdate(BaseModel):
    width: int | None = None
    height: int | None = None
    bg_color: str | None = None
    layers_json: list[dict[str, Any]] | None = None
    sort_order: int | None = None


class ArtboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    width: int
    height: int
    bg_color: str
    layers_json: list[dict[str, Any]]
    sort_order: int
    created_at: datetime
    updated_at: datetime
    layers: list[LayerResponse] = []


class BrandKitCreate(BaseModel):
    name: str
    colors: list[str] = Field(default_factory=list)
    fonts: list[str] = Field(default_factory=list)
    logo_url: str | None = None
    tone_description: str | None = None


class BrandKitUpdate(BaseModel):
    name: str | None = None
    colors: list[str] | None = None
    fonts: list[str] | None = None
    logo_url: str | None = None
    tone_description: str | None = None


class BrandKitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    user_id: uuid.UUID
    colors: list[str]
    fonts: list[str]
    logo_url: str | None
    tone_description: str | None
    created_at: datetime
    updated_at: datetime


class ProjectCreate(BaseModel):
    name: str
    brand_kit_id: uuid.UUID | None = None
    canvas_json: dict[str, Any] = Field(default_factory=dict)


class ProjectUpdate(BaseModel):
    name: str | None = None
    brand_kit_id: uuid.UUID | None = None
    canvas_json: dict[str, Any] | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    user_id: uuid.UUID
    brand_kit_id: uuid.UUID | None
    canvas_json: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    artboards: list[ArtboardResponse] = []


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int


class GenerateDesignRequest(BaseModel):
    prompt: str
    brand_kit_id: uuid.UUID | None = None
    artboard_size: tuple[int, int] = (1080, 1080)


class GenerateDesignResponse(BaseModel):
    artboard: ArtboardResponse
    model_used: str


class GenerateVariationsRequest(BaseModel):
    artboard_id: uuid.UUID
    count: int = 5


class GenerateVariationsResponse(BaseModel):
    variants: list[ArtboardResponse]
    model_used: str


class ExportCodeRequest(BaseModel):
    artboard_id: uuid.UUID
    framework: Literal["react", "nextjs"] = "react"


class ExportCodeResponse(BaseModel):
    code: str
    framework: str


class TemplateCreate(BaseModel):
    name: str
    category: str
    tags: list[str] = Field(default_factory=list)
    canvas_json: dict[str, Any] = Field(default_factory=dict)
    thumbnail_url: str | None = None


class TemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    category: str
    tags: list[str]
    canvas_json: dict[str, Any]
    thumbnail_url: str | None
    usage_count: int
    created_at: datetime
    updated_at: datetime


class TemplateListResponse(BaseModel):
    items: list[TemplateResponse]
    total: int


class GenerationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    prompt: str
    model_used: str
    output_urls: list[str]
    meta: dict[str, Any]
    created_at: datetime
