'use client';

import { useAssistant } from './AssistantProvider';

export function AssistantThread() {
  const { messages } = useAssistant();

  return (
    <div className="flex-1 space-y-3 overflow-auto p-4">
      {messages.length === 0 && (
        <p className="text-sm text-muted">Ask me anything — capture mistakes, get tutor help, or run quick commands.</p>
      )}
      {messages.map((message) => (
        <div
          key={message.id}
          className={`rounded-lg border p-3 ${
            message.role === 'assistant'
              ? 'border-accent-soft bg-accent-soft'
              : 'border-line bg-surface-field'
          }`}
        >
          <p className="text-xs font-semibold uppercase text-muted">{message.role}</p>
          <p className="mt-2 text-sm leading-6">{message.text}</p>
        </div>
      ))}
    </div>
  );
}
