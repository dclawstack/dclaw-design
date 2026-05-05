"""Export router."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Artboard, Layer
from app.schemas import ExportCodeRequest, ExportCodeResponse

router = APIRouter(prefix="/export", tags=["export"])


def _layer_to_tailwind(layer: Layer) -> str:
    """Convert a layer to Tailwind JSX."""
    t = layer.transform_json
    s = layer.style_json
    style_props: list[str] = []

    # Use Tailwind utility classes where possible
    if s.get("fill"):
        style_props.append(f'className="bg-[{s["fill"]}]"')
    if layer.type == "text":
        text_classes = []
        if s.get("fontSize"):
            size = s["fontSize"]
            if size <= 12:
                text_classes.append("text-xs")
            elif size <= 14:
                text_classes.append("text-sm")
            elif size <= 18:
                text_classes.append("text-lg")
            elif size <= 24:
                text_classes.append("text-xl")
            elif size <= 30:
                text_classes.append("text-2xl")
            else:
                text_classes.append("text-3xl")
        if s.get("fontWeight") == "bold":
            text_classes.append("font-bold")
        style_props.append(f'className="{" ".join(text_classes)}"')

    inline = f"position: absolute; left: {t.get('x', 0)}px; top: {t.get('y', 0)}px; width: {t.get('width', 100)}px; height: {t.get('height', 100)}px;"
    if s.get("opacity") is not None and s["opacity"] != 1.0:
        inline += f" opacity: {s['opacity']};"

    content = layer.content or ""
    if layer.type == "text":
        return f'<div style="{{{inline}}}" {" ".join(style_props)}>{content}</div>'
    elif layer.type == "shape":
        return f'<div style="{{{inline}}}" {" ".join(style_props)} />'
    elif layer.type == "image":
        return f'<img src="{content}" style="{{{inline}}}" alt="" />'
    return f'<div style="{{{inline}}}" />'


@router.post("/code", response_model=ExportCodeResponse)
async def export_code(
    data: ExportCodeRequest,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Export an artboard to React/Tailwind code."""
    artboard = await db.get(Artboard, data.artboard_id)
    if not artboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artboard not found",
        )

    layers = await db.execute(
        __import__("sqlalchemy", fromlist=["select"]).select(Layer).where(Layer.artboard_id == artboard.id)
    )
    layer_list = layers.scalars().all()

    jsx_layers = "\n".join(f"      {_layer_to_tailwind(layer)}" for layer in layer_list)

    style_obj = f'{{ width: {artboard.width}, height: {artboard.height} }}'
    if data.framework == "nextjs":
        code = f"""export default function DesignPage() {{
  return (
    <div className="relative bg-white" style={style_obj}>
{jsx_layers}
    </div>
  );
}}
"""
    else:
        code = f"""import React from "react";

export default function DesignComponent() {{
  return (
    <div className="relative bg-white" style={style_obj}>
{jsx_layers}
    </div>
  );
}}
"""

    return {"code": code, "framework": data.framework}


@router.get("/png/{artboard_id}")
async def export_png(
    artboard_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Stub for PNG export."""
    return {"format": "png", "url": f"/exports/{artboard_id}.png"}


@router.get("/svg/{artboard_id}")
async def export_svg(
    artboard_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Stub for SVG export."""
    return {"format": "svg", "url": f"/exports/{artboard_id}.svg"}
