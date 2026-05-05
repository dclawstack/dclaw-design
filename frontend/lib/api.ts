const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export interface GenerateDesignRequest {
  prompt: string;
  brand_kit_id?: string;
  artboard_size?: [number, number];
}

export interface Artboard {
  id: string;
  project_id: string;
  width: number;
  height: number;
  bg_color: string;
  layers_json: unknown[];
  sort_order: number;
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: string;
  name: string;
  user_id: string;
  brand_kit_id: string | null;
  canvas_json: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface TemplateItem {
  id: string;
  name: string;
  category: string;
  tags: string[];
  thumbnail_url: string | null;
  usage_count: number;
}

export const api = {
  generateDesign: (body: GenerateDesignRequest) =>
    fetchJson<{ artboard: Artboard; model_used: string }>("/api/v1/generate/design", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  listProjects: () =>
    fetchJson<{ items: Project[]; total: number }>("/api/v1/canvas/projects"),
  listTemplates: (category?: string) =>
    fetchJson<{ items: TemplateItem[]; total: number }>(
      `/api/v1/templates?${category ? `category=${category}&` : ""}`,
    ),
  exportCode: (artboardId: string, framework: "react" | "nextjs" = "react") =>
    fetchJson<{ code: string; framework: string }>("/api/v1/export/code", {
      method: "POST",
      body: JSON.stringify({ artboard_id: artboardId, framework }),
    }),
};
