'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { ArrowRight, Loader2, ShieldCheck } from 'lucide-react';

import { securityApi } from '@/lib/api';

type SecurityEvent = {
  event_id: string;
  event_type: string;
  created_at: string;
  [key: string]: unknown;
};

export default function ReviewSecurityPage() {
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const payload = await securityApi.listEvents();
      setEvents((payload.events || []) as SecurityEvent[]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Security audit load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  return (
    <div className="mx-auto max-w-5xl pb-12">
      <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-surface-raised px-3 py-1 text-xs font-medium text-muted">
            <ShieldCheck size={13} />
            Read-only security audit
          </div>
          <h2 className="mt-4 text-3xl font-semibold tracking-normal">Security Events</h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-muted">
            Review local auth bootstrap, login, logout, and access-control events. This page is admin-session aware and never shows raw passwords or bearer tokens.
          </p>
        </div>
        <Link href="/review/admin-auth" className="btn-secondary inline-flex w-fit items-center gap-2">
          <ArrowRight size={15} />
          Back to Admin Session
        </Link>
      </div>

      {error && <div className="mb-4 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">{error}</div>}

      <section className="rounded-lg bg-surface-raised p-5">
        <div className="flex items-center justify-between gap-3">
          <h3 className="font-semibold">Recent events</h3>
          <button onClick={() => load().catch(() => undefined)} className="btn-secondary inline-flex items-center gap-2">
            Refresh
          </button>
        </div>

        {loading ? (
          <div className="mt-4 rounded-lg bg-surface-field p-4 text-sm text-muted">
            <Loader2 size={15} className="mr-2 inline animate-spin" />
            Loading security audit...
          </div>
        ) : events.length ? (
          <div className="mt-4 space-y-3">
            {events.map((event) => (
              <div key={event.event_id} className="rounded-lg bg-surface-field p-4 text-sm">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded-full bg-surface-hover px-2 py-0.5 text-xs font-medium text-accent">{event.event_type}</span>
                  <span className="text-xs text-muted">{String(event.created_at || '')}</span>
                </div>
                <pre className="mt-3 overflow-x-auto whitespace-pre-wrap break-words text-xs text-muted">
{JSON.stringify(event, null, 2)}
                </pre>
              </div>
            ))}
          </div>
        ) : (
          <div className="mt-4 rounded-lg bg-surface-field p-4 text-sm text-muted">
            No security events yet. Bootstrap or login first.
          </div>
        )}
      </section>
    </div>
  );
}
