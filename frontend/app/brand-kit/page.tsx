"use client";

import { useState } from "react";

export default function BrandKitPage() {
  const [colors, setColors] = useState(["#8B5CF6", "#10B981", "#F59E0B"]);
  const [fonts, setFonts] = useState(["Inter", "Playfair Display"]);
  const [tone, setTone] = useState("Modern, minimal, and confident.");

  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Brand Kit</h1>

      <div className="space-y-6">
        <div className="rounded-xl border bg-white p-6">
          <h2 className="mb-4 text-lg font-semibold">Colors</h2>
          <div className="flex flex-wrap gap-3">
            {colors.map((c, i) => (
              <div
                key={i}
                className="flex h-12 w-12 items-center justify-center rounded-lg border shadow-sm"
                style={{ backgroundColor: c }}
              >
                <span className="text-xs font-medium text-white mix-blend-difference">{c}</span>
              </div>
            ))}
            <button className="flex h-12 w-12 items-center justify-center rounded-lg border border-dashed text-gray-400 hover:border-design-500 hover:text-design-600">
              +
            </button>
          </div>
        </div>

        <div className="rounded-xl border bg-white p-6">
          <h2 className="mb-4 text-lg font-semibold">Fonts</h2>
          <ul className="space-y-2">
            {fonts.map((f, i) => (
              <li key={i} className="flex items-center justify-between rounded-lg border px-4 py-2">
                <span className="text-sm">{f}</span>
                <button className="text-xs text-red-500 hover:underline">Remove</button>
              </li>
            ))}
          </ul>
        </div>

        <div className="rounded-xl border bg-white p-6">
          <h2 className="mb-4 text-lg font-semibold">Tone Description</h2>
          <textarea
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            className="w-full rounded-lg border px-3 py-2 text-sm focus:border-design-500 focus:outline-none focus:ring-2 focus:ring-design-200"
            rows={4}
          />
        </div>
      </div>
    </div>
  );
}
