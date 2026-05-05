"use client";

import { useState } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hi! Describe changes like 'make it more premium' or 'add pricing section'." },
  ]);
  const [input, setInput] = useState("");

  function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Applied: updated layout styling." },
      ]);
    }, 800);
  }

  return (
    <div className="flex h-full flex-col">
      <h3 className="mb-3 text-sm font-semibold text-gray-900">Brain Mode</h3>
      <div className="flex-1 space-y-3 overflow-y-auto text-sm">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`rounded-lg px-3 py-2 ${
              m.role === "user" ? "ml-4 bg-design-50 text-design-900" : "mr-4 bg-gray-100 text-gray-800"
            }`}
          >
            {m.content}
          </div>
        ))}
      </div>
      <form onSubmit={handleSend} className="mt-3 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="make it more premium"
          className="flex-1 rounded-lg border px-3 py-2 text-xs focus:border-design-500 focus:outline-none focus:ring-2 focus:ring-design-200"
        />
        <button
          type="submit"
          className="rounded-lg bg-design-600 px-3 py-2 text-xs font-medium text-white hover:bg-design-700"
        >
          Send
        </button>
      </form>
    </div>
  );
}
