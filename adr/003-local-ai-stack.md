# ADR 003: Local-First AI Stack

## Status
Accepted

## Context
Cloud video APIs (Runway, HeyGen) charge per-video. DClaw differentiates on zero marginal cost via local inference.

## Decision
Primary generation stack runs locally:
- **LLM**: Ollama for script breakdown and scene logic
- **Image**: FLUX / SD via ComfyUI API
- **Animation**: AnimateDiff + LivePortrait via ComfyUI
- **TTS**: Kokoro (local, high quality)
- **Assembly**: FFmpeg

Cloud fallback may be added later, but the default is local.

## Consequences
- Users must have GPU hardware or access to a GPU node
- ComfyUI workflow JSONs must be versioned and tested
- Model weights are not shipped; documented in `dclaw-research/`
