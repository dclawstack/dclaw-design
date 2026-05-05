"use client";

import { useState } from "react";
import type { LayerData } from "@/types";

const SAMPLE_LAYERS: LayerData[] = [
  {
    id: "1",
    type: "text",
    name: "Headline",
    transform: { x: 40, y: 40, width: 600, height: 80, rotation: 0 },
    style: { fill: "#111827", fontSize: 48, fontWeight: "bold" },
    content: "Your Design Here",
  },
  {
    id: "2",
    type: "shape",
    name: "Accent",
    transform: { x: 40, y: 140, width: 120, height: 8, rotation: 0 },
    style: { fill: "#8B5CF6" },
  },
  {
    id: "3",
    type: "text",
    name: "Body",
    transform: { x: 40, y: 180, width: 600, height: 200, rotation: 0 },
    style: { fill: "#4B5563", fontSize: 18 },
    content: "AI-generated layout. Every element is editable.",
  },
];

export function SvgCanvas() {
  const [layers] = useState<LayerData[]>(SAMPLE_LAYERS);
  const width = 1080;
  const height = 1080;
  const scale = 0.5;

  return (
    <div className="flex h-full items-center justify-center overflow-auto bg-gray-100">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        width={width * scale}
        height={height * scale}
        className="rounded-lg border bg-white shadow-sm"
      >
        <rect width={width} height={height} fill="#FFFFFF" />
        {layers.map((layer) => (
          <g
            key={layer.id}
            transform={`translate(${layer.transform.x}, ${layer.transform.y}) rotate(${layer.transform.rotation})`}
          >
            {layer.type === "text" && (
              <text
                x={0}
                y={layer.style.fontSize || 16}
                fill={layer.style.fill || "#000"}
                fontSize={layer.style.fontSize}
                fontWeight={layer.style.fontWeight}
                fontFamily={layer.style.fontFamily || "sans-serif"}
                opacity={layer.style.opacity ?? 1}
              >
                {layer.content}
              </text>
            )}
            {layer.type === "shape" && (
              <rect
                width={layer.transform.width}
                height={layer.transform.height}
                fill={layer.style.fill || "#ccc"}
                opacity={layer.style.opacity ?? 1}
              />
            )}
            {layer.type === "image" && layer.content && (
              <image
                href={layer.content}
                width={layer.transform.width}
                height={layer.transform.height}
                opacity={layer.style.opacity ?? 1}
              />
            )}
          </g>
        ))}
      </svg>
    </div>
  );
}
