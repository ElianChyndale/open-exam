'use client';

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { AssistantMessage, loadAssistantThread, saveAssistantThread } from '@/lib/assistant';

type AssistantContextValue = {
  open: boolean;
  setOpen: (value: boolean) => void;
  messages: AssistantMessage[];
  appendMessage: (message: AssistantMessage) => void;
  busy: boolean;
  setBusy: (value: boolean) => void;
};

const AssistantContext = createContext<AssistantContextValue | null>(null);

export function AssistantProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<AssistantMessage[]>(() => loadAssistantThread());
  const [busy, setBusy] = useState(false);

  const appendMessage = useCallback((message: AssistantMessage) => {
    setMessages((prev) => {
      const next = [...prev, message];
      saveAssistantThread(next);
      return next;
    });
  }, []);

  const value = useMemo(
    () => ({ open, setOpen, messages, appendMessage, busy, setBusy }),
    [open, messages, appendMessage, busy],
  );

  return <AssistantContext.Provider value={value}>{children}</AssistantContext.Provider>;
}

export function useAssistant() {
  const value = useContext(AssistantContext);
  if (!value) throw new Error('useAssistant must be used within AssistantProvider');
  return value;
}
