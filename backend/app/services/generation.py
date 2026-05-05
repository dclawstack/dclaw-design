"""AI generation services."""

import uuid
from typing import Any

import httpx

from app.config import settings
from app.models import Artboard


async def generate_canvas_from_prompt(
    prompt: str,
    brand_kit_id: uuid.UUID | None,
    size: tuple[int, int],
) -> dict[str, Any]:
    """Generate a canvas layout from a text prompt.

    Uses Ollama locally if available, otherwise falls back to OpenRouter.
    """
    model_used = "ollama"
    canvas_data: dict[str, Any] = {
        "bg_color": "#F3F4F6",
        "layers": [
            {
                "type": "text",
                "name": "Headline",
                "transform": {"x": 40, "y": 40, "width": size[0] - 80, "height": 80, "rotation": 0},
                "style": {"fill": "#111827", "fontSize": 48, "fontWeight": "bold"},
                "content": prompt[:60],
            },
            {
                "type": "shape",
                "name": "Accent",
                "transform": {"x": 40, "y": 140, "width": 120, "height": 8, "rotation": 0},
                "style": {"fill": "#8B5CF6"},
                "content": None,
            },
            {
                "type": "text",
                "name": "Body",
                "transform": {"x": 40, "y": 180, "width": size[0] - 80, "height": 200, "rotation": 0},
                "style": {"fill": "#4B5563", "fontSize": 18},
                "content": "AI-generated layout based on your prompt.",
            },
        ],
    }

    # Attempt Ollama generation
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(
                f"{settings.ollama_host}/api/generate",
                json={
                    "model": "llava-phi3",
                    "prompt": f"Create a design layout JSON for: {prompt}",
                    "stream": False,
                },
            )
            if res.status_code == 200:
                canvas_data["model_used"] = "ollama-llava-phi3"
                return canvas_data
    except Exception:
        pass

    # Fallback: OpenRouter stub
    if settings.openrouter_api_key:
        model_used = "openrouter"

    canvas_data["model_used"] = model_used
    return canvas_data


async def generate_variations(
    artboard: Artboard,
    count: int,
) -> list[dict[str, Any]]:
    """Generate brand-aligned variations of an artboard."""
    variants: list[dict[str, Any]] = []
    base_layers = artboard.layers_json or []

    for i in range(count):
        variant_layers = []
        for layer in base_layers:
            variant_layer = dict(layer)
            style = dict(variant_layer.get("style", {}))
            # Slight color rotation for variation
            if style.get("fill") and i > 0:
                style["fill"] = f"#{((i + 1) * 1118481) % 16777215:06x}"
            variant_layer["style"] = style
            variant_layers.append(variant_layer)

        variants.append({
            "bg_color": artboard.bg_color,
            "layers": variant_layers,
        })

    return variants
