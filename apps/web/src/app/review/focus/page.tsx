'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  CircleHelp,
  Clock3,
  Eye,
  Loader2,
  PauseCircle,
  ShieldCheck,
  SkipForward,
  Sparkles,
  Wrench,
} from 'lucide-react';

import { FocusSession, FocusStep, focusApi, tutorApi } from '@/lib/api';

const stepLabels: Record<string, string> = {
  review_lab: 'Review',
  formula_lab: 'Formula',
  lexical_review: 'Lexical',
  assessment: 'Assessment',
  tutor_hint: 'Tutor',
  coverage_confirmation: 'Coverage',
  resource_confirmation: 'Resource',
  reflection: 'Reflection',
};

export default function FocusSessionPage() {
  const [session, setSession] = useState<FocusSession | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState('');
  const [error, setError] = useState('');
  const [revealed, setRevealed] = useState(false);
  const [evidenceOpen, setEvidenceOpen] = useState(false);
  const [shortcutsOpen, setShortcutsOpen] = useState(false);
  const [hint, setHint] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const params = typeof window !== 'undefined' ? new URLSearchParams(window.location.search) : new URLSearchParams();
      const planId = params.get('plan');
      const started = await focusApi.start({
        profile_id: 'default',
        plan_id: planId || undefined,
        source: planId ? 'study_planner' : 'today_plan',
        force_new: Boolean(planId),
      });
      setSession(started);
      setRevealed(false);
      setEvidenceOpen(false);
      setHint('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Focus session load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const activeStep = useMemo(() => currentStep(session), [session]);
  const activeIndex = session && activeStep ? session.steps.findIndex((step) => step.step_id === activeStep.step_id) : -1;
  const progress = session?.steps.length ? Math.round(((session.summary.completed_steps || 0) / session.steps.length) * 100) : 0;
  const completeLikeCount = Number(session?.summary.completed_steps || 0) + Number(session?.summary.skipped_steps || 0) + Number(session?.summary.blocked_steps || 0);

  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null;
      const editing = target?.tagName === 'INPUT' || target?.tagName === 'TEXTAREA' || target?.tagName === 'SELECT' || target?.isContentEditable;
      if (event.key === 'Escape') {
        setShortcutsOpen(false);
        return;
      }
      if (editing || !activeStep) return;
      if (event.key === '?') {
        event.preventDefault();
        setShortcutsOpen((current) => !current);
      }
      if (event.key.toLowerCase() === 'r') {
        event.preventDefault();
        setRevealed(true);
      }
      if (busy) return;
      if (event.key === '1') {
        event.preventDefault();
        completeCurrent('recalled').catch(() => undefined);
      }
      if (event.key === '2') {
        event.preventDefault();
        completeCurrent('partial').catch(() => undefined);
      }
      if (event.key === '3') {
        event.preventDefault();
        skipCurrent('Skipped from keyboard').catch(() => undefined);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [activeStep, busy, session]);

  const completeCurrent = async (outcome: string) => {
    if (!session || !activeStep || activeStep.status === 'blocked') return;
    setBusy(`complete:${outcome}`);
    setError('');
    try {
      const updated = await focusApi.completeStep(session.focus_id, activeStep.step_id, {
        outcome,
        actual_minutes: activeStep.target_minutes,
        notes: outcome === 'recalled' ? 'Completed in Focus Session' : 'Completed with a learning gap',
      });
      setSession(updated);
      setRevealed(false);
      setEvidenceOpen(false);
      setHint('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Step completion failed');
    } finally {
      setBusy('');
    }
  };

  const skipCurrent = async (reason = 'Deferred from Focus Session') => {
    if (!session || !activeStep) return;
    setBusy('skip');
    setError('');
    try {
      const updated = await focusApi.skipStep(session.focus_id, activeStep.step_id, reason);
      setSession(updated);
      setRevealed(false);
      setEvidenceOpen(false);
      setHint('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Step skip failed');
    } finally {
      setBusy('');
    }
  };

  const askHint = async () => {
    if (!activeStep) return;
    setBusy('hint');
    setHint('');
    try {
      const payload = activeStep.embedded_payload || {};
      const answer = await tutorApi.ask({
        profile_id: session?.profile_id || 'default',
        mode: activeStep.step_type === 'formula_lab' ? 'formula_help' : activeStep.step_type === 'lexical_review' ? 'language_help' : 'hint',
        query: `${activeStep.title}. ${payload.prompt || activeStep.description}`,
      });
      setHint(answer.answer || 'Hint unavailable for this step.');
    } catch {
      setHint('Hint unavailable for this step.');
    } finally {
      setBusy('');
    }
  };

  if (loading) {
    return (
      <div className="mx-auto flex min-h-[70vh] max-w-5xl items-center justify-center">
        <div className="inline-flex items-center gap-2 rounded-lg bg-surface-raised px-4 py-3 text-sm text-muted">
          <Loader2 size={16} className="animate-spin" />
          Preparing focus session...
        </div>
      </div>
    );
  }

  const showSummary = Boolean(session && (session.status !== 'active' || !activeStep));

  return (
    <div className="mx-auto max-w-6xl pb-12">
      <div className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div className="min-w-0">
          <div className="inline-flex items-center gap-2 rounded-full bg-surface-raised px-3 py-1 text-xs font-medium text-muted">
            <ShieldCheck size={13} className="text-success" />
            Focus Session
          </div>
          <h2 className="mt-4 text-3xl font-semibold tracking-normal">Focus Session</h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-muted">
            Today's guided path / {session?.total_target_minutes || 0} min planned
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <button type="button" onClick={() => setShortcutsOpen(true)} className="btn-secondary inline-flex items-center gap-2">
            <CircleHelp size={14} />
            Shortcuts
          </button>
          <Link href="/review/tools" className="inline-flex items-center gap-2 rounded-lg border border-line px-3 py-2 text-xs font-semibold text-muted transition-colors hover:text-foreground">
            <Wrench size={14} />
            Tools
          </Link>
        </div>
      </div>

      {error && (
        <div className="mb-4 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          {error}
        </div>
      )}

      {shortcutsOpen && (
        <section className="mb-4 rounded-lg border border-line bg-surface-raised p-4" aria-label="Shortcuts">
          <div className="flex items-center justify-between gap-3">
            <h3 className="font-semibold">Shortcuts</h3>
            <button type="button" onClick={() => setShortcutsOpen(false)} className="text-sm font-medium text-accent">
              Close
            </button>
          </div>
          <div className="mt-3 grid gap-2 text-sm text-muted sm:grid-cols-4">
            <Shortcut label="?" value="Shortcuts" />
            <Shortcut label="R" value="Reveal" />
            <Shortcut label="1" value="Complete" />
            <Shortcut label="3" value="Skip" />
          </div>
        </section>
      )}

      {showSummary && session ? (
        <SummaryPanel session={session} onRestart={load} />
      ) : activeStep && session ? (
        <main data-testid="focus-main-task" className="rounded-lg border border-line bg-surface-raised shadow-sm">
          <div className="border-b border-line p-4">
            <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2 text-sm text-muted">
                  <span>Step {activeIndex + 1} of {session.steps.length}</span>
                  <span className="rounded border border-line px-2 py-0.5 text-xs font-semibold">{stepLabels[activeStep.step_type] || activeStep.step_type}</span>
                  <span className="rounded border border-success-soft bg-success-soft px-2 py-0.5 text-xs font-semibold text-success">{statusLabel(activeStep.status)}</span>
                  <span className="inline-flex items-center gap-1">
                    <Clock3 size={13} />
                    Target {activeStep.target_minutes}m
                  </span>
                </div>
                <h3 className="mt-3 text-2xl font-semibold">{activeStep.title}</h3>
              </div>
              <div className="min-w-[180px]">
                <div className="flex items-center justify-between text-xs text-muted">
                  <span>{completeLikeCount}/{session.steps.length}</span>
                  <span>{progress}%</span>
                </div>
                <div data-testid="focus-progress" className="mt-2 h-2 overflow-hidden rounded-full bg-surface-field">
                  <div className="h-full rounded-full bg-accent-solid transition-all" style={{ width: `${Math.max(4, progress)}%` }} />
                </div>
              </div>
            </div>
          </div>

          <div className="grid gap-0 lg:grid-cols-[minmax(0,1fr)_320px]">
            <section className="min-w-0 p-5 lg:p-6">
              <p className="text-sm leading-6 text-muted">{activeStep.description}</p>
              <div className="mt-5 rounded-lg border border-line bg-surface-field p-4">
                <p className="text-xs font-semibold uppercase tracking-normal text-muted">Prompt</p>
                <p className="mt-3 whitespace-pre-wrap text-lg leading-8">{String(activeStep.embedded_payload?.prompt || activeStep.description || activeStep.title)}</p>
              </div>

              {activeStep.blocked_reason ? (
                <div className="mt-5 rounded-lg border border-warning-soft bg-warning-soft p-4 text-sm text-warning">
                  <p className="font-semibold">Needs setup</p>
                  <p className="mt-1 leading-6">{activeStep.blocked_reason}</p>
                  {activeStep.launch_route && (
                    <Link href={activeStep.launch_route} className="mt-3 inline-flex items-center gap-2 font-semibold">
                      Open setup
                      <ArrowRight size={14} />
                    </Link>
                  )}
                </div>
              ) : (
                <>
                  <textarea
                    className="mt-5 min-h-28 w-full resize-y rounded-lg border border-line bg-surface-field px-3 py-3 text-sm outline-none focus:border-accent"
                    placeholder="Recall first, then reveal."
                    aria-label="Focus answer"
                  />
                  {revealed && <RevealPanel step={activeStep} />}
                </>
              )}

              {hint && (
                <div className="mt-4 rounded-lg border border-accent-soft bg-accent-soft p-4 text-sm leading-6 text-accent">
                  <p className="font-semibold">Hint</p>
                  <p className="mt-1">{hint}</p>
                </div>
              )}
            </section>

            <aside className="border-t border-line p-5 lg:border-l lg:border-t-0">
              <div className="space-y-3">
                {!activeStep.blocked_reason && (
                  <button
                    type="button"
                    onClick={() => setRevealed(true)}
                    disabled={revealed}
                    className={`${revealed ? 'btn-secondary' : 'btn-primary'} inline-flex w-full items-center justify-center gap-2`}
                  >
                    <Eye size={15} />
                    Reveal
                  </button>
                )}
                {!activeStep.blocked_reason && (
                  <>
                    <button
                      type="button"
                      onClick={() => completeCurrent('recalled')}
                      disabled={Boolean(busy)}
                      className={`${revealed ? 'btn-primary' : 'btn-secondary'} inline-flex w-full items-center justify-center gap-2`}
                    >
                      {busy === 'complete:recalled' ? <Loader2 size={15} className="animate-spin" /> : <CheckCircle2 size={15} />}
                      Complete
                    </button>
                    <button
                      type="button"
                      onClick={() => completeCurrent('partial')}
                      disabled={Boolean(busy)}
                      className="btn-secondary inline-flex w-full items-center justify-center gap-2"
                    >
                      <PauseCircle size={15} />
                      Partial
                    </button>
                  </>
                )}
                <button
                  type="button"
                  onClick={() => skipCurrent()}
                  disabled={Boolean(busy)}
                  className="btn-secondary inline-flex w-full items-center justify-center gap-2"
                >
                  {busy === 'skip' ? <Loader2 size={15} className="animate-spin" /> : <SkipForward size={15} />}
                  Skip
                </button>
                <button
                  type="button"
                  onClick={() => activeStep.blocked_reason ? skipCurrent('Moved past blocked focus step') : completeCurrent('recalled')}
                  disabled={Boolean(busy)}
                  className={`${activeStep.blocked_reason ? 'btn-primary' : 'btn-secondary'} inline-flex w-full items-center justify-center gap-2`}
                >
                  <ArrowRight size={15} />
                  Next
                </button>
              </div>

              <button
                type="button"
                onClick={() => setEvidenceOpen((current) => !current)}
                className="mt-5 flex w-full items-center justify-between gap-3 rounded-lg border border-line bg-surface-field px-3 py-2 text-left text-sm font-semibold"
              >
                <span>Source evidence</span>
                {evidenceOpen ? <ChevronDown size={15} /> : <ChevronRight size={15} />}
              </button>
              {evidenceOpen && <EvidencePanel step={activeStep} />}

              <button
                type="button"
                onClick={askHint}
                disabled={Boolean(busy)}
                className="btn-secondary mt-4 inline-flex w-full items-center justify-center gap-2"
              >
                {busy === 'hint' ? <Loader2 size={15} className="animate-spin" /> : <Sparkles size={15} />}
                Ask Tutor
              </button>

              {activeStep.correct_only_warning && (
                <p className="mt-4 rounded-lg border border-success-soft bg-success-soft p-3 text-xs leading-5 text-success">
                  {activeStep.correct_only_warning}
                </p>
              )}
            </aside>
          </div>
        </main>
      ) : (
        <div className="rounded-lg border border-line bg-surface-raised p-8 text-center text-sm text-muted">
          No focus session is available.
        </div>
      )}
    </div>
  );
}

function currentStep(session: FocusSession | null): FocusStep | null {
  if (!session) return null;
  return (
    session.steps.find((step) => step.step_id === session.current_step_id) ||
    session.steps.find((step) => step.status === 'in_progress' || step.status === 'pending') ||
    null
  );
}

function statusLabel(status: FocusStep['status']) {
  return {
    pending: 'Ready',
    in_progress: 'In progress',
    completed: 'Completed',
    skipped: 'Skipped',
    blocked: 'Needs setup',
  }[status] || status;
}

function RevealPanel({ step }: { step: FocusStep }) {
  const payload = step.embedded_payload || {};
  const revealPayload = payload.reveal_payload || payload;
  const title = step.step_type === 'formula_lab' ? 'Formula' : step.step_type === 'lexical_review' ? 'Meaning' : 'Correct answer';
  return (
    <div className="mt-5 rounded-lg border border-success-soft bg-success-soft p-4 text-sm leading-6 text-success">
      <p className="font-semibold">{title}</p>
      <p className="mt-2 whitespace-pre-wrap">{String(revealPayload.correct_answer || revealPayload.correct_reasoning || 'Correct answer is not embedded for this step.')}</p>
      {revealPayload.correct_reasoning && revealPayload.correct_reasoning !== revealPayload.correct_answer && (
        <p className="mt-3 whitespace-pre-wrap">{String(revealPayload.correct_reasoning)}</p>
      )}
      {Array.isArray(revealPayload.ba_ii_plus_steps) && revealPayload.ba_ii_plus_steps.length > 0 && (
        <ol className="mt-3 space-y-1">
          {revealPayload.ba_ii_plus_steps.map((stepText: string, index: number) => (
            <li key={`${stepText}-${index}`}>{index + 1}. {stepText}</li>
          ))}
        </ol>
      )}
    </div>
  );
}

function EvidencePanel({ step }: { step: FocusStep }) {
  const revealPayload = step.embedded_payload?.reveal_payload || {};
  const refs = Array.from(new Set([...(step.source_refs || []), ...((step.embedded_payload?.source_refs as string[]) || []), ...((revealPayload.source_refs as string[]) || [])])).filter(Boolean);
  const linked = [
    ...step.linked_asset_ids.map((id) => `asset:${id}`),
    ...step.linked_topic_ids.map((id) => `topic:${id}`),
    ...step.linked_lexical_ids.map((id) => `lexical:${id}`),
    ...step.linked_gap_ids.map((id) => `gap:${id}`),
  ];
  return (
    <div className="mt-3 rounded-lg border border-line bg-surface-field p-3 text-xs leading-5 text-muted">
      <p className="font-semibold text-foreground">Evidence</p>
      <div className="mt-2 space-y-1">
        {refs.length ? refs.map((ref) => <p key={ref}>{ref}</p>) : <p>No source refs embedded.</p>}
      </div>
      {linked.length > 0 && (
        <div className="mt-3 border-t border-line pt-3">
          {linked.map((item) => <p key={item}>{item}</p>)}
        </div>
      )}
    </div>
  );
}

function SummaryPanel({ session, onRestart }: { session: FocusSession; onRestart: () => void }) {
  return (
    <section data-testid="focus-summary" className="rounded-lg border border-line bg-surface-raised p-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-success-soft px-3 py-1 text-xs font-semibold text-success">
            <CheckCircle2 size={13} />
            Session closed
          </div>
          <h3 className="mt-4 text-2xl font-semibold">Focus summary</h3>
          <p className="mt-2 text-sm text-muted">You moved through the guided path. Return to Today for the next calm step.</p>
        </div>
        <button type="button" onClick={onRestart} className="btn-primary inline-flex items-center gap-2">
          <ArrowRight size={15} />
          Start Today
        </button>
      </div>
      <div className="mt-6 grid gap-3 sm:grid-cols-3">
        <SummaryMetric label="Completed" value={String(session.summary.completed_steps || 0)} />
        <SummaryMetric label="Skipped" value={String(session.summary.skipped_steps || 0)} />
        <SummaryMetric label="Blocked" value={String(session.summary.blocked_steps || 0)} />
      </div>
      <div className="mt-5 rounded-lg border border-line bg-surface-field p-4 text-sm text-muted">
        <p className="font-semibold text-foreground">Next recommended action</p>
        <p className="mt-1 leading-6">Use Today to continue with the next ready item, or confirm setup items before the next recall step.</p>
      </div>
    </section>
  );
}

function SummaryMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-surface-field p-4">
      <p className="text-2xl font-semibold">{value}</p>
      <p className="mt-1 text-xs font-semibold text-muted">{label}</p>
    </div>
  );
}

function Shortcut({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-lg border border-line bg-surface-field px-3 py-2">
      <kbd className="font-semibold text-foreground">{label}</kbd>
      <span>{value}</span>
    </div>
  );
}
