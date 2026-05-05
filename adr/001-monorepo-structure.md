# ADR 001: Monorepo Structure

## Status
Accepted

## Context
DClaw is a multi-product AI media stack. We need clear separation between design specifications, the video production runtime, and ongoing research.

## Decision
Adopt a monorepo under `dclawstack/` with three top-level repositories:
- `dclaw-design/` — Source of truth for specs, ADRs, API contracts, DB schemas, UI/UX
- `dclaw-video/` — The script-to-video runtime (backend, frontend, desktop, infra)
- `dclaw-research/` — Model benchmarks, prompt libraries, experiment logs

## Consequences
- Each repo can version independently
- `dclaw-design` acts as the anchor; code changes in `dclaw-video` must reference ADRs
- `dclaw-research` informs ADRs, which then drive `dclaw-video` implementation
