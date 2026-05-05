# ADR 004: MinIO for Object Storage

## Status
Accepted

## Context
Video assets, storyboard frames, and rendered outputs need durable, scalable storage. Local filesystem does not scale across workers.

## Decision
Use MinIO (S3-compatible) for all blob storage:
- Raw uploads: `uploads/{project_id}/`
- Storyboard frames: `frames/{project_id}/`
- Rendered clips: `clips/{scene_id}/`
- Final videos: `renders/{project_id}.mp4`

## Consequences
- All services must use presigned URLs or internal MinIO client
- Backups can use standard S3 tools
- Can migrate to AWS S3 later with no code changes
