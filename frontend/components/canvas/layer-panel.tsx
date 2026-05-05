"use client";

import { useState } from "react";
import type { LayerData } from "@/types";

const SAMPLE_LAYERS: LayerData[] = [
  { id: "1", type: "text", name: "Headline", transform: { x: 0, y: 0, width: 0, height: 0, rotation: 0 }, style: {} },
  { id: "2", type: "shape", name: "Accent", transform: { x: 0, y: 0, width: 0, height: 0, rotation: 0 }, style: {} },
  { id: "3", type: "text", name: "Body", transform: { x: 0, y: 0, width: 0, height: 0, rotation: 0 }, style: {} },
];

export function LayerPanel() {
  const [layers] = useState<LayerData[]>(SAMPLE_LAYERS);

  return (
    <div>
      <h3 className="mb-3 text-sm font-semibold text-gray-900">Layers</h3>
      <ul className="space-y-1">
        {layers.map((layer) => (
          <li
            key={layer.id}
            className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm hover:bg-gray-50 cursor-pointer"
          >
            <span className="text-xs text-gray-400 uppercase">{layer.type[0]}</span>
            <span className="text-gray-700">{layer.name}</span>
            {layer.ai_generated && (
              <span className="ml-auto text-[10px] rounded-full bg-design-100 text-design-700 px-1.5 py-0.5">
                AI
              </span>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
