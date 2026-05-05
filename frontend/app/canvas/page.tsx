"use client";

import { useState } from "react";
import { SvgCanvas } from "@/components/canvas/svg-canvas";
import { LayerPanel } from "@/components/canvas/layer-panel";
import { PropertyPanel } from "@/components/canvas/property-panel";
import { ChatPanel } from "@/components/ai-chat/chat-panel";
import { ExportModal } from "@/components/export/export-modal";

export default function CanvasPage() {
  const [showExport, setShowExport] = useState(false);

  return (
    <div className="flex h-[calc(100vh-5rem)] gap-4">
      <aside className="w-64 shrink-0 overflow-y-auto rounded-xl border bg-white p-4">
        <LayerPanel />
      </aside>

      <section className="flex-1 rounded-xl border bg-white p-4">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="font-semibold text-gray-900">Artboard</h2>
          <div className="flex gap-2">
            <button
              onClick={() => setShowExport(true)}
              className="rounded-lg bg-design-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-design-700"
            >
              Export
            </button>
          </div>
        </div>
        <SvgCanvas />
      </section>

      <aside className="w-80 shrink-0 flex flex-col gap-4">
        <div className="rounded-xl border bg-white p-4">
          <PropertyPanel />
        </div>
        <div className="flex-1 rounded-xl border bg-white p-4">
          <ChatPanel />
        </div>
      </aside>

      {showExport && <ExportModal onClose={() => setShowExport(false)} />}
    </div>
  );
}
