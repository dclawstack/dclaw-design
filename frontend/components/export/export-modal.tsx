"use client";

import { useState } from "react";

interface ExportModalProps {
  onClose: () => void;
}

export function ExportModal({ onClose }: ExportModalProps) {
  const [format, setFormat] = useState<"png" | "svg" | "react" | "nextjs">("png");
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleExport() {
    setLoading(true);
    if (format === "react" || format === "nextjs") {
      try {
        const { api } = await import("@/lib/api");
        const res = await api.exportCode("placeholder-id", format);
        setCode(res.code);
      } catch {
        setCode("// Export failed");
      }
    } else {
      setCode(`${format.toUpperCase()} export URL: /exports/placeholder-id.${format}`);
    }
    setLoading(false);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-lg rounded-xl bg-white p-6 shadow-lg">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Export</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            ✕
          </button>
        </div>

        <div className="mb-4 flex gap-2">
          {(["png", "svg", "react", "nextjs"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFormat(f)}
              className={`rounded-lg px-3 py-1.5 text-xs font-medium ${
                format === f
                  ? "bg-design-600 text-white"
                  : "border bg-white text-gray-700 hover:bg-gray-50"
              }`}
            >
              {f.toUpperCase()}
            </button>
          ))}
        </div>

        <button
          onClick={handleExport}
          disabled={loading}
          className="mb-4 w-full rounded-lg bg-design-600 py-2 text-sm font-medium text-white hover:bg-design-700 disabled:opacity-50"
        >
          {loading ? "Generating..." : `Export as ${format.toUpperCase()}`}
        </button>

        {code && (
          <pre className="max-h-64 overflow-auto rounded-lg bg-gray-900 p-4 text-xs text-gray-100">
            {code}
          </pre>
        )}
      </div>
    </div>
  );
}
