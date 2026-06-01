const LEGACY_QUEUE_KEY = 'openexam.pending-attempts';
const DB_NAME = 'openexam-offline';
const STORE_NAME = 'pending-writes';

interface PendingWrite {
  id?: number;
  family: 'attempt' | 'todo';
  payload: Record<string, unknown>;
  request?: { path: string; method: string; body?: Record<string, unknown> };
  queuedAt: string;
}

function openQueue(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = window.indexedDB.open(DB_NAME, 1);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: 'id', autoIncrement: true });
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

async function migrateLegacyQueue(db: IDBDatabase) {
  const raw = window.localStorage.getItem(LEGACY_QUEUE_KEY);
  if (!raw) return;
  try {
    const payloads = JSON.parse(raw) as Record<string, unknown>[];
    const transaction = db.transaction(STORE_NAME, 'readwrite');
    payloads.forEach((payload) => transaction.objectStore(STORE_NAME).add({
      family: 'attempt',
      payload,
      queuedAt: new Date().toISOString(),
    } satisfies PendingWrite));
    await transactionDone(transaction);
  } finally {
    window.localStorage.removeItem(LEGACY_QUEUE_KEY);
  }
}

function transactionDone(transaction: IDBTransaction): Promise<void> {
  return new Promise((resolve, reject) => {
    transaction.oncomplete = () => resolve();
    transaction.onerror = () => reject(transaction.error);
    transaction.onabort = () => reject(transaction.error);
  });
}

export async function queueAttempt(payload: Record<string, unknown>) {
  const db = await openQueue();
  await migrateLegacyQueue(db);
  const transaction = db.transaction(STORE_NAME, 'readwrite');
  transaction.objectStore(STORE_NAME).add({ family: 'attempt', payload, queuedAt: new Date().toISOString() } satisfies PendingWrite);
  await transactionDone(transaction);
}

export async function queueTodoWrite(path: string, method: string, body?: Record<string, unknown>) {
  const db = await openQueue();
  await migrateLegacyQueue(db);
  const transaction = db.transaction(STORE_NAME, 'readwrite');
  transaction.objectStore(STORE_NAME).add({
    family: 'todo',
    payload: {},
    request: { path, method, body },
    queuedAt: new Date().toISOString(),
  } satisfies PendingWrite);
  await transactionDone(transaction);
}

export async function loadPendingAttempts(): Promise<PendingWrite[]> {
  if (typeof window === 'undefined') return [];
  const db = await openQueue();
  await migrateLegacyQueue(db);
  return new Promise((resolve, reject) => {
    const request = db.transaction(STORE_NAME).objectStore(STORE_NAME).getAll();
    request.onsuccess = () => resolve(request.result as PendingWrite[]);
    request.onerror = () => reject(request.error);
  });
}

export async function flushPendingAttempts(
  send: (payload: Record<string, unknown>) => Promise<unknown>,
) {
  const pending = await loadPendingAttempts();
  let sent = 0;
  for (const item of pending.filter((write) => write.family === 'attempt')) {
    try {
      await send(item.payload);
      const db = await openQueue();
      const transaction = db.transaction(STORE_NAME, 'readwrite');
      transaction.objectStore(STORE_NAME).delete(item.id!);
      await transactionDone(transaction);
      sent += 1;
    } catch {
      // Keep failed writes for the next explicit online retry.
    }
  }
  return { sent, remaining: pending.filter((write) => write.family === 'attempt').length - sent };
}

export async function flushPendingWrites(
  sendAttempt: (payload: Record<string, unknown>) => Promise<unknown>,
) {
  const attemptResult = await flushPendingAttempts(sendAttempt);
  const pending = await loadPendingAttempts();
  let todoSent = 0;
  for (const item of pending.filter((write) => write.family === 'todo' && write.request)) {
    try {
      await fetch(item.request!.path, {
        method: item.request!.method,
        headers: item.request!.body ? { 'Content-Type': 'application/json' } : undefined,
        body: item.request!.body ? JSON.stringify(item.request!.body) : undefined,
      }).then((response) => {
        if (!response.ok) throw new Error(`Todo retry failed: ${response.status}`);
      });
      const db = await openQueue();
      const transaction = db.transaction(STORE_NAME, 'readwrite');
      transaction.objectStore(STORE_NAME).delete(item.id!);
      await transactionDone(transaction);
      todoSent += 1;
    } catch {
      // Leave the Todo write queued. A revision conflict is surfaced on the next online retry.
    }
  }
  return { sent: attemptResult.sent + todoSent, remaining: (await loadPendingAttempts()).length };
}
