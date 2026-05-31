const QUEUE_KEY = 'openexam.pending-attempts';

export function queueAttempt(payload: Record<string, unknown>) {
  const pending = loadPendingAttempts();
  pending.push(payload);
  window.localStorage.setItem(QUEUE_KEY, JSON.stringify(pending));
}

export function loadPendingAttempts(): Record<string, unknown>[] {
  if (typeof window === 'undefined') return [];
  try {
    return JSON.parse(window.localStorage.getItem(QUEUE_KEY) || '[]');
  } catch {
    return [];
  }
}

export async function flushPendingAttempts(
  send: (payload: Record<string, unknown>) => Promise<unknown>,
) {
  const pending = loadPendingAttempts();
  const remaining: Record<string, unknown>[] = [];
  for (const payload of pending) {
    try {
      await send(payload);
    } catch {
      remaining.push(payload);
    }
  }
  window.localStorage.setItem(QUEUE_KEY, JSON.stringify(remaining));
  return { sent: pending.length - remaining.length, remaining: remaining.length };
}
