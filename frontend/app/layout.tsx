import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DClaw Design",
  description: "AI-Native Design Studio",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <nav className="border-b bg-white px-6 py-3">
          <div className="flex items-center gap-6">
            <a href="/" className="text-lg font-bold text-design-600">
              DClaw Design
            </a>
            <div className="flex gap-4 text-sm text-gray-600">
              <a href="/" className="hover:text-design-600">
                Dashboard
              </a>
              <a href="/canvas" className="hover:text-design-600">
                Canvas
              </a>
              <a href="/brand-kit" className="hover:text-design-600">
                Brand Kit
              </a>
            </div>
          </div>
        </nav>
        <main className="p-6">{children}</main>
      </body>
    </html>
  );
}
