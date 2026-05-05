"use client";

import { useState } from "react";

export function PropertyPanel() {
  const [fill, setFill] = useState("#111827");
  const [fontSize, setFontSize] = useState(48);
  const [opacity, setOpacity] = useState(1);

  return (
    <div>
      <h3 className="mb-3 text-sm font-semibold text-gray-900">Properties</h3>
      <div className="space-y-4">
        <div>
          <label className="mb-1 block text-xs text-gray-500">Fill</label>
          <div className="flex items-center gap-2">
            <input
              type="color"
              value={fill}
              onChange={(e) => setFill(e.target.value)}
              className="h-8 w-8 rounded border"
            />
            <input
              type="text"
              value={fill}
              onChange={(e) => setFill(e.target.value)}
              className="flex-1 rounded-lg border px-2 py-1 text-xs"
            />
          </div>
        </div>

        <div>
          <label className="mb-1 block text-xs text-gray-500">Font Size</label>
          <input
            type="number"
            value={fontSize}
            onChange={(e) => setFontSize(Number(e.target.value))}
            className="w-full rounded-lg border px-2 py-1 text-xs"
          />
        </div>

        <div>
          <label className="mb-1 block text-xs text-gray-500">Opacity</label>
          <input
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={opacity}
            onChange={(e) => setOpacity(Number(e.target.value))}
            className="w-full"
          />
          <div className="text-right text-xs text-gray-500">{Math.round(opacity * 100)}%</div>
        </div>
      </div>
    </div>
  );
}
