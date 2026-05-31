'use client';

import { useEffect } from 'react';
import { attemptsApi } from '@/lib/api';
import { flushPendingAttempts } from '@/lib/offline';

export default function OfflineCaptureRegistration() {
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(() => undefined);
    }
    const flush = () => flushPendingAttempts(attemptsApi.record).catch(() => undefined);
    window.addEventListener('online', flush);
    flush();
    return () => window.removeEventListener('online', flush);
  }, []);

  return null;
}
