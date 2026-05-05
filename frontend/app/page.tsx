"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export default function HomePage() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleGenerate(e: React.FormEvent) {
    e.preventDefault();
    if (!prompt.trim()) return;
    setLoading(true);
    try {
      await api.generateDesign({ prompt, artboard_size: [1080, 1080] });
      setPrompt("");
      alert("Design generated! Navigate to Canvas to view.");
    } catch (err) {
      alert("Generation failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-4xl">
      <div className="mb-8 rounded-xl bg-gradient-to-r from-design-500 to-design-700 p-8 text-white">
        <h1 className="mb-2 text-3xl font-bold">DClaw Design</h1>
        <p className="text-lg opacity-90">
          Describe your design. We generate editable vector layouts.
        </p>
      </div>

      <form onSubmit={handleGenerate} className="mb-8">
        <div className="flex gap-3">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Instagram carousel for a coffee shop, earthy tones, 3 slides"
            className="flex-1 rounded-lg border px-4 py-3 text-sm focus:border-design-500 focus:outline-none focus:ring-2 focus:ring-design-200"
          />
          <button
            type="submit"
            disabled={loading}
            className="rounded-lg bg-design-600 px-6 py-3 text-sm font-medium text-white hover:bg-design-700 disabled:opacity-50"
          >
            {loading ? "Generating..." : "Generate"}
          </button>
        </div>
      </form>

      <div className="grid gap-6 md:grid-cols-2">
        <a
          href="/canvas"
          className="rounded-xl border bg-white p-6 shadow-sm transition hover:shadow-md"
        >
          <h2 className="mb-2 text-xl font-semibold text-gray-900">Canvas Editor</h2>
          <p className="text-gray-600">
            Edit artboards, layers, and properties with AI assistance.
          </p>
        </a>

        <a
          href="/brand-kit"
          className="rounded-xl border bg-white p-6 shadow-sm transition hover:shadow-md"
        >
          <h2 className="mb-2 text-xl font-semibold text-gray-900">Brand Kit</h2>
          <p className="text-gray-600">
            Manage colors, fonts, logos, and tone for consistent designs.
          </p>
        </a>
      </div>
    </div>
  );
}
