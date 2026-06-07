'use client';

import { MessageSquareText } from 'lucide-react';
import { useAssistant } from './AssistantProvider';

export function AssistantLauncher() {
  const { setOpen } = useAssistant();
  return (
    <button
      type="button"
      onClick={() => setOpen(true)}
      className="fixed bottom-20 right-4 z-40 flex items-center gap-2 rounded-full border border-accent-soft bg-surface-raised px-3 py-2 text-xs text-accent shadow-lg backdrop-blur-xl transition-colors hover:bg-accent-soft lg:bottom-5"
      aria-label="Open AI assistant"
      title="AI Assistant"
    >
      <MessageSquareText size={14} />
      <span>AI Assistant</span>
    </button>
  );
}
