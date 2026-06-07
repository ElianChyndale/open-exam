/** Assistant thread types and cross-page persistence helpers. */

export interface AssistantMessage {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  createdAt: string;
  action?: Record<string, unknown> | null;
}

export const ASSISTANT_STORAGE_KEY = 'openexam.assistant.thread';

export function loadAssistantThread(): AssistantMessage[] {
  if (typeof window === 'undefined') return [];
  try {
    return JSON.parse(window.localStorage.getItem(ASSISTANT_STORAGE_KEY) || '[]');
  } catch {
    return [];
  }
}

export function saveAssistantThread(messages: AssistantMessage[]) {
  if (typeof window === 'undefined') return;
  window.localStorage.setItem(ASSISTANT_STORAGE_KEY, JSON.stringify(messages));
}
