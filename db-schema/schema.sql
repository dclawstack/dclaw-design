-- DClaw Video Database Schema
-- PostgreSQL 15+

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE project_status AS ENUM ('draft', 'storyboard', 'rendering', 'done');
CREATE TYPE scene_status AS ENUM ('pending', 'generating', 'done', 'error');
CREATE TYPE render_job_status AS ENUM ('pending', 'started', 'success', 'failure');

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    script_text TEXT NOT NULL,
    status project_status NOT NULL DEFAULT 'draft',
    video_url TEXT,
    duration INTEGER,
    template TEXT DEFAULT 'youtube_explainer',
    voice_profile_id UUID,
    character_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE scenes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    scene_number INTEGER NOT NULL,
    narration_text TEXT NOT NULL DEFAULT '',
    visual_prompt TEXT NOT NULL DEFAULT '',
    duration_seconds NUMERIC(6,2) NOT NULL DEFAULT 5.0,
    status scene_status NOT NULL DEFAULT 'pending',
    video_clip_url TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (project_id, scene_number)
);

CREATE TABLE storyboards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scene_id UUID NOT NULL REFERENCES scenes(id) ON DELETE CASCADE,
    frame_number INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    prompt_used TEXT,
    selected BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (scene_id, frame_number)
);

CREATE TABLE characters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    reference_image_url TEXT NOT NULL,
    face_embedding VECTOR(512), -- requires pgvector extension
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE voice_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    kokoro_voice_id TEXT NOT NULL,
    speed NUMERIC(3,2) NOT NULL DEFAULT 1.0,
    language TEXT NOT NULL DEFAULT 'en',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE render_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    celery_task_id TEXT NOT NULL,
    progress_percent INTEGER NOT NULL DEFAULT 0,
    status render_job_status NOT NULL DEFAULT 'pending',
    logs TEXT,
    result_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_scenes_project ON scenes(project_id);
CREATE INDEX idx_storyboards_scene ON storyboards(scene_id);
CREATE INDEX idx_characters_project ON characters(project_id);
CREATE INDEX idx_render_jobs_project ON render_jobs(project_id);
CREATE INDEX idx_render_jobs_task ON render_jobs(celery_task_id);
