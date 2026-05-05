"""Seed initial data."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models import Template


async def seed_data() -> None:
    """Seed default templates if none exist."""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select, func
        result = await session.execute(select(func.count()).select_from(Template))
        count = result.scalar() or 0
        if count > 0:
            return

        templates = [
            Template(
                name="Instagram Post",
                category="social",
                tags=["instagram", "square", "social media"],
                canvas_json={
                    "width": 1080,
                    "height": 1080,
                    "bg_color": "#F3F4F6",
                    "layers": [],
                },
            ),
            Template(
                name="Story",
                category="social",
                tags=["instagram", "story", "vertical"],
                canvas_json={
                    "width": 1080,
                    "height": 1920,
                    "bg_color": "#000000",
                    "layers": [],
                },
            ),
            Template(
                name="Business Card",
                category="print",
                tags=["business", "card", "print"],
                canvas_json={
                    "width": 1050,
                    "height": 600,
                    "bg_color": "#FFFFFF",
                    "layers": [],
                },
            ),
        ]
        session.add_all(templates)
        await session.commit()
