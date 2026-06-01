'use client';

import { useState, useEffect } from 'react';
import './globals.css';
import { Sidebar } from '@/components/cockpit/Sidebar';
import QuickCapture from '@/components/capture/QuickCapture';
import OfflineCaptureRegistration from '@/components/capture/OfflineCaptureRegistration';
import { PenLine } from 'lucide-react';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [quickOpen, setQuickOpen] = useState(false);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === 'E') {
        e.preventDefault();
        setQuickOpen(q => !q);
      }
      if (e.key === 'Escape' && quickOpen) {
        setQuickOpen(false);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [quickOpen]);

  return (
    <html lang="zh-CN">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      </head>
      <body className="min-h-screen lg:flex">
        <Sidebar />
        <main className="min-h-screen flex-1 p-4 pb-24 lg:ml-60 lg:p-6 overflow-auto">
          {children}
        </main>
        <OfflineCaptureRegistration />
        <button
          type="button"
          onClick={() => setQuickOpen(true)}
          className="fixed bottom-20 right-4 z-40 flex items-center gap-2 rounded-full border border-accent-soft bg-surface-raised px-3 py-2 text-xs text-accent shadow-lg backdrop-blur-xl transition-colors hover:bg-accent-soft lg:bottom-5"
          aria-label="打开快速录入，快捷键 Ctrl 或 Command 加 Shift 加 E"
          title="快速录入 · Ctrl/Command + Shift + E"
        >
          <PenLine size={14} />
          <span>快速录入</span>
          <kbd className="hidden rounded border border-line bg-surface-field px-1.5 py-0.5 text-[10px] text-muted sm:inline">
            Ctrl/⌘ Shift E
          </kbd>
        </button>
        <QuickCapture isOpen={quickOpen} onClose={() => setQuickOpen(false)} />
      </body>
    </html>
  );
}
