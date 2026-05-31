'use client';

import { useState, useEffect } from 'react';
import './globals.css';
import { Sidebar } from '@/components/cockpit/Sidebar';
import QuickCapture from '@/components/capture/QuickCapture';

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
      <body className="min-h-screen lg:flex">
        <Sidebar />
        <main className="min-h-screen flex-1 p-4 pt-24 lg:ml-60 lg:p-6 lg:pt-6 overflow-auto">
          {children}
        </main>
        <QuickCapture isOpen={quickOpen} onClose={() => setQuickOpen(false)} />
      </body>
    </html>
  );
}
