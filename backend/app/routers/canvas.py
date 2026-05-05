"""Canvas CRUD router."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Artboard, Layer, Project
from app.schemas import (
    ArtboardCreate,
    ArtboardResponse,
    ArtboardUpdate,
    LayerCreate,
    LayerResponse,
    LayerUpdate,
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)

router = APIRouter(prefix="/canvas", tags=["canvas"])


# Projects
@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
) -> Project:
    project = Project(
        name=data.name,
        brand_kit_id=data.brand_kit_id,
        canvas_json=data.canvas_json,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.get("/projects", response_model=ProjectListResponse)
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    result = await db.execute(select(Project).offset(skip).limit(limit))
    projects = result.scalars().all()
    total_result = await db.execute(select(func.count()).select_from(Project))
    total = total_result.scalar() or 0
    return {"items": projects, "total": total}


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Project:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: uuid.UUID,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
) -> Project:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    await db.delete(project)
    await db.commit()


# Artboards
@router.post("/artboards", response_model=ArtboardResponse, status_code=status.HTTP_201_CREATED)
async def create_artboard(
    data: ArtboardCreate,
    db: AsyncSession = Depends(get_db),
) -> Artboard:
    artboard = Artboard(
        project_id=uuid.uuid4(),  # placeholder
        width=data.width,
        height=data.height,
        bg_color=data.bg_color,
        sort_order=data.sort_order,
    )
    db.add(artboard)
    await db.commit()
    await db.refresh(artboard)
    return artboard


@router.get("/artboards/{artboard_id}", response_model=ArtboardResponse)
async def get_artboard(
    artboard_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Artboard:
    artboard = await db.get(Artboard, artboard_id)
    if not artboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artboard not found",
        )
    return artboard


@router.patch("/artboards/{artboard_id}", response_model=ArtboardResponse)
async def update_artboard(
    artboard_id: uuid.UUID,
    data: ArtboardUpdate,
    db: AsyncSession = Depends(get_db),
) -> Artboard:
    artboard = await db.get(Artboard, artboard_id)
    if not artboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artboard not found",
        )
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(artboard, key, value)
    await db.commit()
    await db.refresh(artboard)
    return artboard


@router.delete("/artboards/{artboard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artboard(
    artboard_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    artboard = await db.get(Artboard, artboard_id)
    if not artboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artboard not found",
        )
    await db.delete(artboard)
    await db.commit()


# Layers
@router.post("/layers", response_model=LayerResponse, status_code=status.HTTP_201_CREATED)
async def create_layer(
    data: LayerCreate,
    artboard_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Layer:
    layer = Layer(
        artboard_id=artboard_id,
        type=data.type,
        name=data.name,
        transform_json=data.transform_json.model_dump(),
        style_json=data.style_json.model_dump(),
        content=data.content,
        ai_generated=data.ai_generated,
        ai_prompt=data.ai_prompt,
    )
    db.add(layer)
    await db.commit()
    await db.refresh(layer)
    return layer


@router.get("/layers/{layer_id}", response_model=LayerResponse)
async def get_layer(
    layer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Layer:
    layer = await db.get(Layer, layer_id)
    if not layer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Layer not found",
        )
    return layer


@router.patch("/layers/{layer_id}", response_model=LayerResponse)
async def update_layer(
    layer_id: uuid.UUID,
    data: LayerUpdate,
    db: AsyncSession = Depends(get_db),
) -> Layer:
    layer = await db.get(Layer, layer_id)
    if not layer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Layer not found",
        )
    update_data = data.model_dump(exclude_unset=True)
    if "transform_json" in update_data and update_data["transform_json"] is not None:
        update_data["transform_json"] = update_data["transform_json"].model_dump()
    if "style_json" in update_data and update_data["style_json"] is not None:
        update_data["style_json"] = update_data["style_json"].model_dump()
    for key, value in update_data.items():
        setattr(layer, key, value)
    await db.commit()
    await db.refresh(layer)
    return layer


@router.delete("/layers/{layer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_layer(
    layer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    layer = await db.get(Layer, layer_id)
    if not layer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Layer not found",
        )
    await db.delete(layer)
    await db.commit()
