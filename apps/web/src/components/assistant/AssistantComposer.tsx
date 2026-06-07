'use client';

import { FormEvent, useState } from 'react';
import { usePathname } from 'next/navigation';
import { Send } from 'lucide-react';
import { assistantApi } from '@/lib/api';
import { useAssistant } from './AssistantProvider';

export function AssistantComposer() {
  const pathname = usePathname();
  const { appendMessage, busy, setBusy } = useAssistant();
  const [value, setValue] = useState('');

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (!value.trim()) return;

    const text = value.trim();
    appendMessage({ id: `user-${Date.now()}`, role: 'user', text, createdAt: new Date().toISOString() });
    setValue('');
    setBusy(true);

    try {
      const result: any = await assistantApi.sendMessage({
        message: text,
        page_context: { route: pathname },
        attachments: [],
      });
      appendMessage({
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        text: result.assistant_reply?.text || result.assistant_reply?.question || 'Done.',
        createdAt: new Date().toISOString(),
        action: result.action || null,
      });
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="border-t border-line p-4">
      <label className="sr-only" htmlFor="assistant-message">Assistant message</label>
      <textarea
        id="assistant-message"
        aria-label="Assistant message"
        value={value}
        onChange={(event) => setValue(event.target.value)}
        className="min-h-24 w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
        placeholder="Ask me anything — capture mistakes, get tutor help, or run quick commands."
      />
      <button
        type="submit"
        className="btn-primary mt-3 inline-flex items-center gap-2"
        disabled={busy || !value.trim()}
      >
        <Send size={14} />
        Send
      </button>
    </form>
  );
}
