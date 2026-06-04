'use client';

import Link from 'next/link';
import { FormEvent, useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  Brain,
  CalendarCheck2,
  CheckCircle2,
  Gauge,
  Loader2,
  Search,
  Sparkles,
  Target,
  Wrench,
} from 'lucide-react';

import { CockpitSummary, navigationApi } from '@/lib/api';

export default function ReviewCockpitPage() {
  const [cockpit, setCockpit] = useState<CockpitSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      setCockpit(await navigationApi.cockpit('default'));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Cockpit load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const planBlocks = cockpit?.today_plan_preview || [];
  const health = cockpit?.learning_health || {};
  const primary = cockpit?.primary_action || {
    label: 'Begin setup',
    href: '/onboarding',
    reason: 'Set a focused goal to unlock the first useful plan.',
  };
  const supporting = (cockpit?.supporting_actions || []).slice(0, 4);
  const readiness = cockpit?.active_goal?.readiness_status || health.readiness || 'not_started';

  const tutorHref = useMemo(() => {
    const trimmed = query.trim();
    return trimmed ? `/review/tutor?q=${encodeURIComponent(trimmed)}` : '/review/tutor';
  }, [query]);

  const ask = (event: FormEvent) => {
    event.preventDefault();
    window.location.href = tutorHref;
  };

  return (
    <div className="mx-auto max-w-6xl pb-12">
      <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-surface-raised px-3 py-1 text-xs font-medium text-muted">
            <CheckCircle2 size={13} className="text-success" />
            Correct-only learning
          </div>
          <h2 className="mt-4 text-3xl font-semibold tracking-normal md:text-4xl">Today</h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-muted">
            {cockpit?.active_goal?.title || 'Choose a goal, then let OpenExam narrow the day to one useful next step.'}
          </p>
        </div>
        <Link href="/review/tools" className="btn-secondary inline-flex w-fit items-center gap-2">
          <Wrench size={15} />
          More Tools
        </Link>
      </div>

      {error && (
        <div className="mb-4 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
          {error}
        </div>
      )}

      <main data-testid="primary-cockpit" className="grid min-w-0 gap-5 lg:grid-cols-[minmax(0,1.15fr)_minmax(320px,0.85fr)]">
        <section className="min-w-0 rounded-lg bg-surface-raised p-6 shadow-sm">
          <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
            <div className="min-w-0">
              <div className="flex items-center gap-2 text-sm font-medium text-accent">
                <Target size={17} />
                Next best step
              </div>
              <h3 className="mt-4 text-2xl font-semibold">{primary.label}</h3>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-muted">{primary.reason}</p>
            </div>
            <Link href={primary.href} className="btn-primary inline-flex shrink-0 items-center justify-center gap-2 px-5 py-3">
              <ArrowRight size={16} />
              {primary.label}
            </Link>
          </div>

          <div className="mt-8 grid gap-3 sm:grid-cols-3">
            <QuietMetric icon={Gauge} label="Readiness" value={labelize(readiness)} />
            <QuietMetric icon={CalendarCheck2} label="Plan" value={labelize(String(health.plan_status || 'not planned'))} />
            <QuietMetric icon={Brain} label="Next blocks" value={String(health.next_blocks || planBlocks.length || 0)} />
          </div>
        </section>

        <section className="min-w-0 rounded-lg bg-surface-raised p-5">
          <div className="flex items-center justify-between gap-3">
            <h3 className="font-semibold">Today Plan</h3>
            <Link href="/review/study-planner" className="text-sm font-medium text-accent hover:underline">
              Open plan
            </Link>
          </div>
          <div className="mt-4 space-y-3">
            {loading ? (
              <div className="rounded-lg bg-surface-field p-4 text-sm text-muted">
                <Loader2 size={15} className="mr-2 inline animate-spin" />
                Preparing today...
              </div>
            ) : planBlocks.length ? (
              <Link href="/review/focus" className="block rounded-lg bg-surface-field p-4 transition-colors hover:bg-surface-hover">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="text-sm font-semibold">Start Focus Session</p>
                    <p className="mt-1 line-clamp-2 text-xs leading-5 text-muted">
                      {planBlocks.length} guided steps / {planBlocks.reduce((total, block) => total + Number(block.target_minutes || 0), 0)}m planned
                    </p>
                  </div>
                  <ArrowRight size={15} className="shrink-0 text-accent" />
                </div>
              </Link>
            ) : (
              <CalmEmptyState title="No plan yet" actionHref="/review/focus" actionLabel="Start Focus Session" />
            )}
          </div>
        </section>

        <section className="min-w-0 rounded-lg bg-surface-raised p-5 lg:col-span-2">
          <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_360px]">
            <div className="min-w-0">
              <h3 className="font-semibold">Focus</h3>
              <div className="mt-4 grid gap-2 sm:grid-cols-4">
                {supporting.map((action) => (
                  <Link key={action.href} href={action.href} className="rounded-lg bg-surface-field px-3 py-3 text-sm font-medium transition-colors hover:bg-surface-hover">
                    {action.label}
                  </Link>
                ))}
              </div>
            </div>
            <form onSubmit={ask} className="min-w-0 rounded-lg bg-surface-field p-3">
              <label className="flex min-w-0 items-center gap-2 text-sm">
                <Search size={15} className="shrink-0 text-muted" />
                <input
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  placeholder="Ask about your plan or a concept..."
                  className="min-w-0 flex-1 bg-transparent outline-none placeholder:text-muted"
                />
              </label>
              <div className="mt-3 flex justify-end">
                <Link href={tutorHref} className="btn-secondary inline-flex items-center gap-2">
                  <Sparkles size={14} />
                  Ask Tutor
                </Link>
              </div>
            </form>
          </div>
        </section>
      </main>
    </div>
  );
}

function QuietMetric({ icon: Icon, label, value }: { icon: any; label: string; value: string }) {
  return (
    <div className="rounded-lg bg-surface-field p-3">
      <div className="flex items-center gap-2 text-muted">
        <Icon size={15} />
        <span className="text-xs">{label}</span>
      </div>
      <p className="mt-2 text-sm font-semibold">{value}</p>
    </div>
  );
}

function CalmEmptyState({ title, actionHref, actionLabel }: { title: string; actionHref: string; actionLabel: string }) {
  return (
    <div className="rounded-lg bg-surface-field p-4 text-sm text-muted">
      <p className="font-medium text-foreground">{title}</p>
      <Link href={actionHref} className="mt-3 inline-flex items-center gap-2 text-accent hover:underline">
        {actionLabel}
        <ArrowRight size={13} />
      </Link>
    </div>
  );
}

function labelize(value: string) {
  return value.replace(/[_-]+/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}
