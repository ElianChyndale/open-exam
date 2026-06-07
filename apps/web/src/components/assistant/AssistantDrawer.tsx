'use client';

import { usePathname } from 'next/navigation';
import { X } from 'lucide-react';
import { useAssistant } from './AssistantProvider';
import { AssistantThread } from './AssistantThread';
import { AssistantComposer } from './AssistantComposer';

export function AssistantDrawer() {
  const pathname = usePathname();
  const { open, setOpen } = useAssistant();

  if (!open) return null;

  return (
    <aside
      aria-label="AI Assistant"
      className="fixed inset-y-0 right-0 z-50 flex w-full max-w-xl flex-col border-l border-line bg-surface-raised shadow-2xl"
    >
      <div className="flex items-center justify-between border-b border-line px-4 py-3">
        <div>
          <p className="text-sm font-semibold">AI Assistant</p>
          <p className="text-xs text-muted">Current page: {pathname}</p>
        </div>
        <button type="button" onClick={() => setOpen(false)} aria-label="Close AI assistant">
          <X size={18} />
        </button>
      </div>
      <AssistantThread />
      <AssistantComposer />
    </aside>
  );
}
