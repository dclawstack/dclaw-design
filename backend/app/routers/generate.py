"""AI generation router."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Artboard, Generation, Layer
from app.schemas import (
    GenerateDesignRequest,
    GenerateDesignResponse,
    GenerateVariationsRequest,
    GenerateVariationsResponse,
)
from app.services.generation import generate_canvas_from_prompt, generate_variations

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("/design", response_model=GenerateDesignResponse)
async def create_design(
    data: GenerateDesignRequest,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Generate a complete design from a text prompt."""
    canvas_data = await generate_canvas_from_prompt(
        prompt=data.prompt,
        brand_kit_id=data.brand_kit_id,
        size=data.artboard_size,
    )

    artboard = Artboard(
        project_id=uuid.uuid4(),  # placeholder; real impl links to project
        width=data.artboard_size[0],
        height=data.artboard_size[1],
        bg_color=canvas_data.get("bg_color", "#FFFFFF"),
        layers_json=canvas_data.get("layers", []),
    )
    db.add(artboard)
    await db.commit()
    await db.refresh(artboard)

    for layer_data in canvas_data.get("layers", []):
        layer = Layer(
            artboard_id=artboard.id,
            type=layer_data.get("type", "shape"),
            name=layer_data.get("name", "Layer"),
            transform_json=layer_data.get("transform", {}),
            style_json=layer_data.get("style", {}),
            content=layer_data.get("content"),
            ai_generated=True,
            ai_prompt=data.prompt,
        )
        db.add(layer)

    await db.commit()
    await db.refresh(artboard)

    generation = Generation(
        prompt=data.prompt,
        model_used=canvas_data.get("model_used", "ollama"),
        output_urls=[],
        meta={"artboard_id": str(artboard.id)},
    )
    db.add(generation)
    await db.commit()

    return {
        "artboard": artboard,
        "model_used": canvas_data.get("model_used", "ollama"),
    }


@router.post("/variations", response_model=GenerateVariationsResponse)
async def create_variations(
    data: GenerateVariationsRequest,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Generate brand-aligned variations of an existing artboard."""
    artboard = await db.get(Artboard, data.artboard_id)
    if not artboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artboard not found",
        )

    variants = await generate_variations(artboard, data.count)
    created_variants: list[Artboard] = []

    for variant_data in variants:
        variant = Artboard(
            project_id=artboard.project_id,
            width=artboard.width,
            height=artboard.height,
            bg_color=variant_data.get("bg_color", artboard.bg_color),
            layers_json=variant_data.get("layers", []),
        )
        db.add(variant)
        await db.flush()

        for layer_data in variant_data.get("layers", []):
            layer = Layer(
                artboard_id=variant.id,
                type=layer_data.get("type", "shape"),
                name=layer_data.get("name", "Layer"),
                transform_json=layer_data.get("transform", {}),
                style_json=layer_data.get("style", {}),
                content=layer_data.get("content"),
                ai_generated=True,
                ai_prompt=f"Variation of {artboard.id}",
            )
            db.add(layer)

        created_variants.append(variant)

    await db.commit()
    for v in created_variants:
        await db.refresh(v)

    return {
        "variants": created_variants,
        "model_used": "ollama",
    }
