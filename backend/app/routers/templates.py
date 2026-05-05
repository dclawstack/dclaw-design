"""Template router."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Template
from app.schemas import (
    TemplateCreate,
    TemplateListResponse,
    TemplateResponse,
)

router = APIRouter(prefix="/templates", tags=["templates"])


@router.post("", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    data: TemplateCreate,
    db: AsyncSession = Depends(get_db),
) -> Template:
    template = Template(
        name=data.name,
        category=data.category,
        tags=data.tags,
        canvas_json=data.canvas_json,
        thumbnail_url=data.thumbnail_url,
    )
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


@router.get("", response_model=TemplateListResponse)
async def list_templates(
    category: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    stmt = select(Template)
    if category:
        stmt = stmt.where(Template.category == category)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    templates = result.scalars().all()
    total_result = await db.execute(select(func.count()).select_from(Template))
    total = total_result.scalar() or 0
    return {"items": templates, "total": total}


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Template:
    template = await db.get(Template, template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )
    return template
