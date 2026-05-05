# DClaw Design

AI-Native Design Studio — generative-first canvas where you describe layouts and the AI generates editable vector designs.

## Stack

- **Frontend:** Next.js 14, Tailwind CSS, shadcn/ui
- **Backend:** FastAPI, SQLAlchemy 2.0, asyncpg, Pydantic v2
- **Desktop:** Tauri v2
- **AI:** Ollama (llava-phi3), OpenRouter fallback
- **Storage:** MinIO for assets, PostgreSQL for metadata

## Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8095
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Desktop

```bash
cd src-tauri
cargo tauri dev
```

## Ports

- Frontend dev: `3006`
- Backend: `8095`

## Features

- Prompt-to-canvas: single prompt generates complete multi-artboard designs
- Smart variants: one-click generate brand-aligned variations
- Local-first generation via Ollama
- Code export: React/Tailwind components
- Brain Mode: conversational editing
