'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Clock3,
  Battery,
  BatteryFull,
  BatteryLow,
  BatteryMedium,
  Loader2,
  NotebookPen,
  RefreshCcw,
  Sparkles,
  Wrench,
} from 'lucide-react';

import { energyApi, reviewApi } from '@/lib/api';
import { ReviewProjection } from '@/components/review/ReviewProjection';

interface ReviewPack {
  review_id: string;
  generated_for: string;
  focus_topic: string;
  review_item_count: number;
  warm_start_item_count: number;
  source_event_count: number;
  markdown_content: string;
  items: Array<Record<string, any>>;
}

interface DueSummary {
  date: string;
  total_due: number;
  total_recent_low_confidence: number;
  total_patterns: number;
  merged_count: number;
  top_items: Array<{
    topic: string;
    los: string;
    error_type: string;
    priority: number;
    reasons: string[];
  }>;
}

interface EnergyHistoryEvent {
  check_in_id?: string;
  energy_level?: number;
  mental_clarity?: number;
  physical_fatigue?: number;
  motivation?: number;
  created_at?: string;
}

export default function DailyReviewPage() {
  const [pack, setPack] = useState<ReviewPack | null>(null);
  const [due, setDue] = useState<DueSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [energyBusy, setEnergyBusy] = useState<number | null>(null);
  const [selectedEnergyLevel, setSelectedEnergyLevel] = useState<number | null>(null);
  const [latestEnergy, setLatestEnergy] = useState<EnergyHistoryEvent | null>(null);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('');

  const load = async (energyLevel?: number | null) => {
    setLoading(true);
    setError('');
    try {
      const [packPayload, duePayload] = await Promise.all([
        reviewApi.getToday(energyLevel === null || energyLevel === undefined ? undefined : { energy_level: String(energyLevel) }),
        reviewApi.listDue(),
      ]);
      setPack(packPayload as ReviewPack);
      setDue(duePayload as DueSummary);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Daily review load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    Promise.all([
      load().catch(() => undefined),
      energyApi.history(1).then((payload: any) => {
        const history = Array.isArray(payload?.history) ? payload.history : [];
        setLatestEnergy(history[0] || null);
      }).catch(() => undefined),
    ]).catch(() => undefined);
  }, []);

  const effectiveEnergy = selectedEnergyLevel ?? latestEnergy?.energy_level ?? 2;
  const energyMessage = useMemo(() => {
    if (!pack?.markdown_content) return '';
    const lines = pack.markdown_content.split('\n').map((line) => line.trim()).filter(Boolean);
    return lines.find((line) => /^[⚠⚡🧠🛑😴]/.test(line)) || '';
  }, [pack]);

  const completeReview = async () => {
    if (!pack?.review_id) return;
    setCompleting(true);
    setStatus('');
    try {
      const result = await reviewApi.complete(pack.review_id) as {
        review_id: string;
        completed: boolean;
        newly_reviewed_items: number;
      };
      setStatus(`Marked ${result.newly_reviewed_items} items as reviewed.`);
      await load(selectedEnergyLevel);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Review completion failed');
    } finally {
      setCompleting(false);
    }
  };

  const checkInEnergy = async (energyLevel: number) => {
    setEnergyBusy(energyLevel);
    setStatus('');
    setError('');
    try {
      await energyApi.checkIn({
        energy_level: energyLevel,
        mental_clarity: Math.max(1, Math.min(10, 2 + energyLevel * 2)),
        physical_fatigue: Math.max(1, Math.min(10, 9 - energyLevel * 2)),
        motivation: Math.max(1, Math.min(10, 3 + energyLevel * 2)),
        sleep_hours: 0,
        stress_level: 0,
      });
      setSelectedEnergyLevel(energyLevel);
      const historyPayload = await energyApi.history(1) as { history: EnergyHistoryEvent[] };
      setLatestEnergy(historyPayload.history?.[0] || null);
      await load(energyLevel);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Energy check-in failed');
    } finally {
      setEnergyBusy(null);
    }
  };

  const EnergyIcon = effectiveEnergy >= 3 ? BatteryFull : effectiveEnergy >= 1 ? BatteryMedium : BatteryLow;

  return (
    <div className="mx-auto max-w-6xl pb-12">
      <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-surface-raised px-3 py-1 text-xs font-medium text-muted">
            <BookOpen size={13} />
            Daily review
          </div>
          <h2 className="mt-4 text-3xl font-semibold tracking-normal md:text-4xl">Daily Review</h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-muted">
            Review what you studied today: due mistake cards, low-confidence points, and repeated patterns.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/today" className="btn-secondary inline-flex w-fit items-center gap-2">
            <ArrowRight size={15} />
            Back to Today
          </Link>
          <Link href="/review/tools" className="btn-secondary inline-flex w-fit items-center gap-2">
            <Wrench size={15} />
            More Tools
          </Link>
        </div>
      </div>

      {error && (
        <div className="mb-4 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
          {error}
        </div>
      )}
      {status && (
        <div className="mb-4 rounded-lg border border-success-soft bg-success-soft p-3 text-sm text-success">
          {status}
        </div>
      )}

      <main className="grid min-w-0 gap-5 lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)]">
        <section className="min-w-0 rounded-lg bg-surface-raised p-5 lg:col-span-2">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div className="min-w-0">
              <div className="flex items-center gap-2 text-sm font-medium text-accent">
                <EnergyIcon size={16} />
                Energy subsystem
              </div>
              <h3 className="mt-2 text-lg font-semibold">Shape today&apos;s review intensity before you start</h3>
              <p className="mt-1 text-sm leading-6 text-muted">
                Daily Review is energy-aware. Lower energy reduces review volume and pushes you toward core items first.
              </p>
              {energyMessage && <p className="mt-3 text-sm font-medium text-ink">{energyMessage}</p>}
            </div>
            <div className="grid shrink-0 grid-cols-5 gap-2" role="group" aria-label="Select effective review energy">
              {[0, 1, 2, 3, 4].map((level) => (
                <button
                  key={level}
                  type="button"
                  onClick={() => checkInEnergy(level)}
                  disabled={energyBusy !== null}
                  aria-pressed={effectiveEnergy === level}
                  className={`h-10 w-10 rounded-full border text-sm font-semibold transition-colors ${
                    effectiveEnergy === level
                      ? 'border-accent bg-accent-solid text-white'
                      : 'border-line bg-surface-field text-muted hover:border-accent-soft hover:text-accent'
                  } disabled:opacity-50`}
                >
                  {energyBusy === level ? <Loader2 size={14} className="mx-auto animate-spin" /> : level}
                </button>
              ))}
            </div>
          </div>
        </section>

        <section className="min-w-0 rounded-lg bg-surface-raised p-6 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
            <div className="min-w-0">
              <div className="flex items-center gap-2 text-sm font-medium text-accent">
                <NotebookPen size={17} />
                Today&apos;s review pack
              </div>
              <h3 className="mt-4 text-2xl font-semibold">
                {loading ? 'Loading review pack...' : (pack?.focus_topic || 'General review')}
              </h3>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-muted">
                Keep this page as your main review surface. The pack below is generated from local events and memory, not from guessed summaries.
              </p>
            </div>
            <div className="flex shrink-0 flex-wrap gap-2">
              <button type="button" onClick={() => load(selectedEnergyLevel)} className="btn-secondary inline-flex items-center gap-2" disabled={loading}>
                <RefreshCcw size={14} className={loading ? 'animate-spin' : ''} />
                Refresh
              </button>
              <button type="button" onClick={completeReview} className="btn-primary inline-flex items-center gap-2" disabled={loading || completing || !pack?.review_id}>
                <CheckCircle2 size={14} />
                {completing ? 'Completing...' : 'Mark Reviewed'}
              </button>
            </div>
          </div>

          <div className="mt-8 grid gap-3 sm:grid-cols-3">
            <QuietMetric icon={BookOpen} label="Review items" value={String(pack?.review_item_count || 0)} />
            <QuietMetric icon={Sparkles} label="Warm start" value={String(pack?.warm_start_item_count || 0)} />
            <QuietMetric icon={Clock3} label="Source events" value={String(pack?.source_event_count || 0)} />
          </div>
        </section>

        <section className="min-w-0 rounded-lg bg-surface-raised p-5">
          <div className="flex items-center justify-between gap-3">
            <h3 className="font-semibold">What needs review</h3>
            <Link href="/review/lab" className="text-sm font-medium text-accent hover:underline">
              Open Review Lab
            </Link>
          </div>
          <div className="mt-4 space-y-3">
            {loading ? (
              <div className="rounded-lg bg-surface-field p-4 text-sm text-muted">
                <Loader2 size={15} className="mr-2 inline animate-spin" />
                Loading due items...
              </div>
            ) : (
              <>
                <div className="rounded-lg bg-surface-field p-4">
                  <p className="text-sm font-semibold">{due?.merged_count || 0} items in the merged queue</p>
                  <p className="mt-1 text-xs text-muted">
                    Due: {due?.total_due || 0} · Low confidence: {due?.total_recent_low_confidence || 0} · Patterns: {due?.total_patterns || 0}
                  </p>
                </div>
                <div className="space-y-2">
                  {(due?.top_items || []).slice(0, 5).map((item, index) => (
                    <div key={`${item.topic}-${item.los}-${index}`} className="rounded-lg bg-surface-field px-3 py-3">
                      <p className="text-sm font-medium">{item.topic || 'Unknown topic'}{item.los ? ` · ${item.los}` : ''}</p>
                      <p className="mt-1 text-xs text-muted">
                        {item.error_type || 'review'} · priority {item.priority || 0}
                      </p>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </section>

        <section className="min-w-0 rounded-lg bg-surface-raised p-5 lg:col-span-2">
          <div className="mb-4 flex items-center justify-between gap-3">
            <h3 className="font-semibold">Review content</h3>
            <span className="text-xs text-muted">{pack?.generated_for || ''}</span>
          </div>

          {loading ? (
            <div className="rounded-lg bg-surface-field p-6 text-sm text-muted">
              <Loader2 size={15} className="mr-2 inline animate-spin" />
              Building daily review...
            </div>
          ) : (
            <ReviewProjection markdown={pack?.markdown_content || '# Daily Review\n\n暂无复习内容。'} />
          )}
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
