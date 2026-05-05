# ADR 002: Async Video Pipeline with Celery

## Status
Accepted

## Context
Video generation is long-running (minutes to hours). HTTP request/response cycles cannot block on render completion.

## Decision
Use Celery + Redis for all async video work:
- API returns `job_id` immediately
- Clients poll `GET /status` or connect via WebSocket `WS /render/{job_id}/progress`
- Celery workers run on GPU-enabled nodes with ComfyUI accessible

## Consequences
- Requires Redis and Celery worker deployment
- Must handle worker crashes and idempotency
- Scene-level regeneration must be a patch, not full rebuild
