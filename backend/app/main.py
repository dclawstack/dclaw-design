"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import canvas, export, generate, health, templates
from app.seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_data()
    yield
    await engine.dispose()


app = FastAPI(
    title="DClaw Design API",
    description="AI-Native Design Studio",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(generate.router, prefix="/api/v1")
app.include_router(canvas.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")
app.include_router(templates.router, prefix="/api/v1")


@app.get("/health")
async def root_health() -> dict[str, str]:
    return {"status": "ok"}
