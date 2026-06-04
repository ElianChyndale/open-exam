'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  Brain,
  CalendarCheck2,
  CheckCircle2,
  CirclePlay,
  ClipboardCheck,
  Clock3,
  ExternalLink,
  Flag,
  Gauge,
  LineChart,
  Loader2,
  Map,
  RefreshCw,
  Rocket,
  Search,
  ShieldAlert,
  SkipForward,
  Sparkles,
  Target,
} from 'lucide-react';

import { AdaptiveStudyPlan, StudyEnergyMode, StudyPlanBlock, studyPlannerApi } from '@/lib/api';

const energyOptions: Array<{ mode: StudyEnergyMode; label: string; minutes: number }> = [
  { mode: 'low', label: 'Low', minutes: 40 },
  { mode: 'normal', label: 'Normal', minutes: 90 },
  { mode: 'high', label: 'High', minutes: 150 },
];

const blockLabels: Record<StudyPlanBlock['block_type'], string> = {
  review_lab: 'Review Lab',
  formula_lab: 'Formula Lab',
  lexical_review: 'Lexical',
  coverage_gap: 'Coverage',
  mock_transfer_drill: 'Mock Transfer',
  resource_confirmation: 'Resource',
  asset_confirmation: 'Asset',
  file_ingestion_cleanup: 'File Cleanup',
  mission_control_review: 'Mission',
  reflection: 'Reflection',
};

const statusStyles: Record<StudyPlanBlock['status'], string> = {
  pending: 'border-line bg-surface-field text-muted',
  in_progress: 'border-accent-soft bg-accent-soft text-accent',
  completed: 'border-success-soft bg-success-soft text-success',
  skipped: 'border-warning-soft bg-warning-soft text-warning',
  blocked: 'border-danger-soft bg-danger-soft text-danger',
};

export default function StudyPlannerPage() {
  const [energyMode, setEnergyMode] = useState<StudyEnergyMode>('normal');
  const [availableMinutes, setAvailableMinutes] = useState(90);
  const [goal, setGoal] = useState('');
  const [plan, setPlan] = useState<AdaptiveStudyPlan | null>(null);
  const [busy, setBusy] = useState(false);
  const [actionBusy, setActionBusy] = useState('');
  const [error, setError] = useState('');

  const loadToday = async () => {
    setBusy(true);
    setError('');
    try {
      const today = await studyPlannerApi.getToday();
      setPlan(today);
      setEnergyMode(today.energy_mode);
      setAvailableMinutes(today.available_minutes);
      setGoal(today.goal || '');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Study plan load failed');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    loadToday().catch(() => undefined);
  }, []);

  const generatePlan = async () => {
    setBusy(true);
    setError('');
    try {
      const generated = await studyPlannerApi.generate({
        energy_mode: energyMode,
        available_minutes: availableMinutes,
        goal,
      });
      setPlan(generated);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Study plan generation failed');
    } finally {
      setBusy(false);
    }
  };

  const runBlockAction = async (block: StudyPlanBlock, action: 'start' | 'complete' | 'skip') => {
    setActionBusy(`${action}:${block.block_id}`);
    setError('');
    try {
      const result =
        action === 'start'
          ? await studyPlannerApi.startBlock(block.block_id)
          : action === 'complete'
            ? await studyPlannerApi.completeBlock(block.block_id, {
                outcome: `Completed ${blockLabels[block.block_type]} block`,
                actual_minutes: block.target_minutes,
              })
            : await studyPlannerApi.skipBlock(block.block_id, `Skipped ${blockLabels[block.block_type]} block`);
      setPlan(result.plan);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Block update failed');
    } finally {
      setActionBusy('');
    }
  };

  const completePlan = async () => {
    if (!plan) return;
    setActionBusy(`complete-plan:${plan.plan_id}`);
    setError('');
    try {
      setPlan(await studyPlannerApi.completePlan(plan.plan_id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Plan completion failed');
    } finally {
      setActionBusy('');
    }
  };

  const typeCounts = useMemo(() => {
    const counts = plan?.summary?.block_type_counts || {};
    return Object.entries(counts).sort((a, b) => String(a[0]).localeCompare(String(b[0])));
  }, [plan]);

  const statusCounts = plan?.summary?.status_counts || {};
  const totalMinutes = Number(plan?.summary?.total_minutes || 0);
  const blockedCount = Number(plan?.summary?.blocked_blocks || 0);

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <CalendarCheck2 size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Study Planner</h2>
          </div>
          <p className="mt-1 text-sm text-muted">
            {plan ? `${plan.plan_date} / ${plan.status} / ${plan.plan_id}` : 'No plan loaded'}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Link href={plan?.plan_id ? `/review/focus?plan=${encodeURIComponent(plan.plan_id)}` : '/review/focus'} className="btn-primary inline-flex items-center gap-2">
            <CirclePlay size={14} />
            Start as Focus Session
          </Link>
          <Link href="/onboarding" className="btn-secondary inline-flex items-center gap-2">
            <Rocket size={14} />
            Onboarding
          </Link>
          <Link href="/review/goals" className="btn-secondary inline-flex items-center gap-2">
            <Gauge size={14} />
            Goals
          </Link>
          <Link href="/review/mission-control" className="btn-secondary inline-flex items-center gap-2">
            <Gauge size={14} />
            Mission Control
          </Link>
          <Link href="/review/search" className="btn-secondary inline-flex items-center gap-2">
            <Search size={14} />
            Search
          </Link>
          <Link href="/review/knowledge-map" className="btn-secondary inline-flex items-center gap-2">
            <Map size={14} />
            Knowledge Map
          </Link>
          <Link href="/review/tutor?mode=study_strategy&q=What%20should%20I%20do%20next%20if%20I%20only%20have%2020%20minutes%3F" className="btn-secondary inline-flex items-center gap-2">
            <Sparkles size={14} />
            Tutor
          </Link>
          <Link href="/review/analytics" className="btn-secondary inline-flex items-center gap-2">
            <LineChart size={14} />
            Analytics
          </Link>
          <Link href="/review/assessments" className="btn-secondary inline-flex items-center gap-2">
            <ClipboardCheck size={14} />
            Assessments
          </Link>
          <button type="button" onClick={loadToday} disabled={busy} className="btn-secondary inline-flex items-center gap-2">
            {busy ? <Loader2 size={14} className="animate-spin" /> : <RefreshCw size={14} />}
            Today
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <section className="mb-4 grid gap-3 xl:grid-cols-[minmax(0,1fr)_260px_260px_auto]">
        <div className="rounded-lg border border-line bg-surface-raised p-3">
          <label className="mb-2 block text-xs font-semibold text-muted" htmlFor="study-goal">
            Goal
          </label>
          <input
            id="study-goal"
            value={goal}
            onChange={(event) => setGoal(event.target.value)}
            className="w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
            placeholder="WACC, duration, lexical recall"
          />
        </div>

        <div className="rounded-lg border border-line bg-surface-raised p-3">
          <span className="mb-2 block text-xs font-semibold text-muted">Energy</span>
          <div className="grid grid-cols-3 gap-1 rounded-lg border border-line bg-surface-field p-1">
            {energyOptions.map((option) => (
              <button
                key={option.mode}
                type="button"
                onClick={() => {
                  setEnergyMode(option.mode);
                  setAvailableMinutes(option.minutes);
                }}
                className={`rounded-md px-2 py-1.5 text-xs font-semibold transition-colors ${
                  energyMode === option.mode ? 'bg-accent-solid text-white' : 'text-muted hover:bg-surface-hover'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-lg border border-line bg-surface-raised p-3">
          <label className="mb-2 block text-xs font-semibold text-muted" htmlFor="available-minutes">
            Minutes
          </label>
          <div className="flex items-center gap-2">
            <Clock3 size={15} className="text-muted" />
            <input
              id="available-minutes"
              type="number"
              min={10}
              max={300}
              value={availableMinutes}
              onChange={(event) => setAvailableMinutes(Number(event.target.value))}
              className="w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
            />
          </div>
        </div>

        <button type="button" onClick={generatePlan} disabled={busy} className="btn-primary inline-flex items-center justify-center gap-2 px-4">
          {busy ? <Loader2 size={15} className="animate-spin" /> : <Target size={15} />}
          Generate plan
        </button>
      </section>

      <div className="mb-4 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
        Draft, low-quality, unconfirmed, failed, and no-text content is excluded from review blocks.
      </div>

      {plan && (
        <>
          <section className="mb-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
            <MetricCard icon={Clock3} label="Plan Minutes" value={`${totalMinutes}/${plan.available_minutes}`} />
            <MetricCard icon={Brain} label="Blocks" value={String(plan.summary?.block_count || plan.blocks.length)} />
            <MetricCard icon={Gauge} label="Energy" value={plan.energy_mode} />
            <MetricCard icon={CheckCircle2} label="Completed" value={String(statusCounts.completed || 0)} />
            <MetricCard icon={ShieldAlert} label="Blocked" value={String(blockedCount)} danger={blockedCount > 0} />
          </section>

          <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_340px]">
            <section className="space-y-3">
              {plan.blocks.map((block, index) => (
                <article key={block.block_id} className="rounded-lg border border-line bg-surface-raised p-4">
                  <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                    <div className="min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="rounded border border-line bg-surface-field px-2 py-0.5 text-xs font-semibold text-muted">
                          {index + 1}
                        </span>
                        <span className="rounded border border-accent-soft bg-accent-soft px-2 py-0.5 text-xs font-semibold text-accent">
                          {blockLabels[block.block_type]}
                        </span>
                        <span className={`rounded border px-2 py-0.5 text-xs font-semibold ${statusStyles[block.status]}`}>
                          {block.status}
                        </span>
                      </div>
                      <h3 className="mt-3 text-base font-semibold">{block.title}</h3>
                      <p className="mt-1 text-sm leading-5 text-muted">{block.description}</p>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-right text-sm lg:min-w-[170px]">
                      <div className="rounded-lg border border-line bg-surface-field p-2">
                        <span className="block text-xs text-muted">Minutes</span>
                        <span className="font-semibold">{block.target_minutes}</span>
                      </div>
                      <div className="rounded-lg border border-line bg-surface-field p-2">
                        <span className="block text-xs text-muted">Priority</span>
                        <span className="font-semibold">{block.priority.toFixed(1)}</span>
                      </div>
                    </div>
                  </div>

                  <div className="mt-3 grid gap-3 lg:grid-cols-[minmax(0,1fr)_minmax(220px,0.45fr)]">
                    <div className="rounded-lg border border-line bg-surface-field p-3">
                      <p className="text-xs font-semibold text-muted">Due Reason</p>
                      <p className="mt-1 text-sm leading-5">{block.due_reason}</p>
                      {block.blocked_reason && (
                        <p className="mt-2 rounded border border-danger-soft bg-danger-soft px-2 py-1 text-xs font-semibold text-danger">
                          {block.blocked_reason}
                        </p>
                      )}
                      {block.completion_outcome && (
                        <p className="mt-2 rounded border border-success-soft bg-success-soft px-2 py-1 text-xs font-semibold text-success">
                          {block.completion_outcome}
                        </p>
                      )}
                    </div>

                    <div className="rounded-lg border border-line bg-surface-field p-3 text-xs text-muted">
                      <p className="font-semibold text-foreground">Links</p>
                      <div className="mt-2 grid grid-cols-2 gap-2">
                        <CountPill label="Assets" count={block.linked_asset_ids.length} />
                        <CountPill label="Topics" count={block.linked_topic_ids.length} />
                        <CountPill label="Gaps" count={block.linked_gap_ids.length} />
                        <CountPill label="Lexical" count={block.linked_lexical_ids.length} />
                      </div>
                    </div>
                  </div>

                  <div className="mt-3 flex flex-wrap gap-2">
                    <Link href={block.launch_route} className="btn-secondary inline-flex items-center gap-2">
                      <ExternalLink size={14} />
                      Open subsystem
                    </Link>
                    {block.status === 'pending' && (
                      <button
                        type="button"
                        onClick={() => runBlockAction(block, 'start')}
                        disabled={Boolean(actionBusy)}
                        className="btn-secondary inline-flex items-center gap-2"
                      >
                        {actionBusy === `start:${block.block_id}` ? <Loader2 size={14} className="animate-spin" /> : <CirclePlay size={14} />}
                        Start
                      </button>
                    )}
                    {block.status !== 'completed' && block.status !== 'skipped' && block.status !== 'blocked' && (
                      <button
                        type="button"
                        onClick={() => runBlockAction(block, 'complete')}
                        disabled={Boolean(actionBusy)}
                        className="btn-secondary inline-flex items-center gap-2"
                      >
                        {actionBusy === `complete:${block.block_id}` ? <Loader2 size={14} className="animate-spin" /> : <CheckCircle2 size={14} />}
                        Complete
                      </button>
                    )}
                    {block.status !== 'completed' && block.status !== 'skipped' && (
                      <button
                        type="button"
                        onClick={() => runBlockAction(block, 'skip')}
                        disabled={Boolean(actionBusy)}
                        className="btn-secondary inline-flex items-center gap-2"
                      >
                        {actionBusy === `skip:${block.block_id}` ? <Loader2 size={14} className="animate-spin" /> : <SkipForward size={14} />}
                        Skip
                      </button>
                    )}
                  </div>
                </article>
              ))}
            </section>

            <aside className="space-y-4">
              <section className="rounded-lg border border-line bg-surface-raised p-4">
                <h3 className="font-semibold">Source Signals</h3>
                <div className="mt-3 grid gap-2 text-sm">
                  <SignalRow label="Review due" value={plan.source_signals?.mission_control?.review_lab?.due_count || 0} />
                  <SignalRow label="Coverage gaps" value={coverageGapCount(plan)} />
                  <SignalRow label="Transfer gaps" value={plan.source_signals?.mission_control?.mock_retro?.open_transfer_gap_count || 0} />
                  <SignalRow label="Lexical due" value={plan.source_signals?.mission_control?.language?.due_lexical_count || 0} />
                  <SignalRow label="Candidate blocks" value={plan.source_signals?.candidate_block_count || 0} />
                </div>
              </section>

              <section className="rounded-lg border border-line bg-surface-raised p-4">
                <h3 className="font-semibold">Block Mix</h3>
                <div className="mt-3 space-y-2 text-sm">
                  {typeCounts.map(([type, count]) => (
                    <div key={type} className="flex items-center justify-between gap-3">
                      <span className="text-muted">{blockLabels[type as StudyPlanBlock['block_type']] || type}</span>
                      <span className="font-semibold">{String(count)}</span>
                    </div>
                  ))}
                </div>
              </section>

              <section className="rounded-lg border border-line bg-surface-raised p-4">
                <h3 className="font-semibold">Next Actions</h3>
                <div className="mt-3 space-y-2 text-sm">
                  {plan.recommended_next_actions.map((action) => (
                    <div key={action} className="flex items-start gap-2 rounded-lg border border-line bg-surface-field p-2">
                      <ArrowRight size={14} className="mt-0.5 shrink-0 text-accent" />
                      <span>{action}</span>
                    </div>
                  ))}
                </div>
              </section>

              {plan.summary?.retro && (
                <section className="rounded-lg border border-line bg-surface-raised p-4">
                  <div className="flex items-center justify-between gap-3">
                    <h3 className="font-semibold">Retro Summary</h3>
                    <Link href="/review/analytics" className="text-xs font-semibold text-accent hover:underline">
                      Analytics
                    </Link>
                  </div>
                  <div className="mt-3 grid gap-2 text-sm">
                    <SignalRow label="Completed" value={plan.summary.retro.completed_blocks || 0} />
                    <SignalRow label="Skipped" value={plan.summary.retro.skipped_blocks || 0} />
                    <SignalRow label="Minutes" value={plan.summary.retro.completed_minutes || 0} />
                  </div>
                </section>
              )}

              <button
                type="button"
                onClick={completePlan}
                disabled={!plan || plan.status === 'completed' || Boolean(actionBusy)}
                className="btn-primary inline-flex w-full items-center justify-center gap-2"
              >
                {actionBusy === `complete-plan:${plan.plan_id}` ? <Loader2 size={15} className="animate-spin" /> : <Flag size={15} />}
                Complete plan
              </button>
            </aside>
          </div>
        </>
      )}
    </div>
  );
}

function MetricCard({
  icon: Icon,
  label,
  value,
  danger = false,
}: {
  icon: typeof Clock3;
  label: string;
  value: string;
  danger?: boolean;
}) {
  return (
    <div className="rounded-lg border border-line bg-surface-raised p-4">
      <div className="flex items-center justify-between gap-3">
        <Icon size={18} className={danger ? 'text-danger' : 'text-accent'} />
        <span className="text-xl font-bold">{value}</span>
      </div>
      <p className="mt-2 text-xs font-semibold text-muted">{label}</p>
    </div>
  );
}

function CountPill({ label, count }: { label: string; count: number }) {
  return (
    <div className="rounded border border-line bg-surface-raised px-2 py-1">
      <span>{label}</span>
      <span className="float-right font-semibold text-foreground">{count}</span>
    </div>
  );
}

function SignalRow({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-lg border border-line bg-surface-field px-3 py-2">
      <span className="text-muted">{label}</span>
      <span className="font-semibold">{value}</span>
    </div>
  );
}

function coverageGapCount(plan: AdaptiveStudyPlan) {
  const coverage = plan.source_signals?.mission_control?.coverage || {};
  return Number(coverage.missing || 0) + Number(coverage.partial || 0) + Number(coverage.weak || 0) + Number(coverage.stale || 0) + Number(coverage.draft_only || 0);
}
