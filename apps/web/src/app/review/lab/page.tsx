'use client';

import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Brain, Pause, Play, RotateCcw, HelpCircle } from 'lucide-react';

import { useLabSession } from '@/hooks/useLabSession';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';
import { RecallRevealCard } from '@/components/review-lab/RecallRevealCard';
import { FormulaLabCard } from '@/components/review-lab/FormulaLabCard';
import { ReviewOutcomeButtons } from '@/components/review-lab/ReviewOutcomeButtons';
import { LabCompletionModal } from '@/components/review-lab/LabCompletionModal';
import { ErrorState, LoadingState, ShortcutHelp } from '@/components/ux/UXStates';

export default function ReviewLabPage() {
  const router = useRouter();
  const [paramsReady, setParamsReady] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const {
    session,
    loading,
    error,
    revealed,
    paused,
    hintVisible,
    hintText,
    submitting,
    createSession,
    loadSession,
    reveal,
    requestHint,
    submitOutcome,
    togglePause,
    completeSession,
    fetchReport,
  } = useLabSession({ sessionId });

  const [report, setReport] = useState<any>(null);
  const [showCompletion, setShowCompletion] = useState(false);
  const [creating, setCreating] = useState(false);
  const [recallDraft, setRecallDraft] = useState('');
  const [showShortcuts, setShowShortcuts] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setSessionId(params.get('session') || undefined);
    setParamsReady(true);
  }, []);

  // Keyboard shortcuts
  useKeyboardShortcuts({
    enabled: !!session && !showCompletion,
    onAction: useCallback(
      (action) => {
        switch (action) {
          case 'reveal':
            reveal();
            break;
          case 'rate-forgot':
            submitOutcome('forgot', 0);
            break;
          case 'rate-partial':
            submitOutcome('partial', 1);
            break;
          case 'rate-recalled':
            submitOutcome('recalled', 3);
            break;
          case 'rate-skipped':
            submitOutcome('skipped', 2);
            break;
          case 'next':
            if (revealed) submitOutcome('skipped', 2);
            break;
          case 'hint':
            requestHint();
            break;
          case 'help':
            setShowShortcuts((value) => !value);
            break;
          case 'pause':
          case 'resume':
            togglePause();
            break;
        }
      },
      [reveal, revealed, submitOutcome, requestHint, togglePause]
    ),
    revealed,
    paused,
  });

  // Auto-start: try to load latest active session or create new
  useEffect(() => {
    if (!paramsReady || session || creating || sessionId || error) return;

    const init = async () => {
      // Try to find an active session from history
      try {
        const res = await fetch('/api/review-lab/history?limit=10');
        if (res.ok) {
          const data = await res.json();
          const active = (data.sessions || []).find(
            (s: any) => s.status === 'active' || s.status === 'paused'
          );
          if (active) {
            await loadSession(active.session_id);
            return;
          }
        }
      } catch {
        // ignore
      }

      // Create new session
      setCreating(true);
      const sid = await createSession({ max_units: 20 });
      setCreating(false);
      if (sid) {
        router.replace(`/review/lab?session=${sid}`);
      }
    };

    init();
  }, [paramsReady, session, creating, sessionId, error, createSession, loadSession, router]);

  // Handle completion
  useEffect(() => {
    if (session?.is_complete && !showCompletion) {
      completeSession().then(() => {
        fetchReport().then((r) => {
          if (r) {
            setReport(r);
            setShowCompletion(true);
          }
        });
      });
    }
  }, [session?.is_complete, showCompletion, completeSession, fetchReport]);

  useEffect(() => {
    setRecallDraft('');
  }, [session?.current_unit_index]);

  const handleOutcome = useCallback(
    (outcome: 'forgot' | 'partial' | 'recalled' | 'skipped') => {
      const mapping: Record<string, { outcome: 'forgot' | 'partial' | 'recalled' | 'skipped'; confidence: number }> = {
        forgot: { outcome: 'forgot', confidence: 0 },
        partial: { outcome: 'partial', confidence: 1 },
        recalled: { outcome: 'recalled', confidence: 3 },
        skipped: { outcome: 'skipped', confidence: 2 },
      };
      const mapped = mapping[outcome];
      submitOutcome(mapped.outcome, mapped.confidence);
    },
    [submitOutcome]
  );

  const handleStartNew = useCallback(async () => {
    setShowCompletion(false);
    setReport(null);
    const sid = await createSession({ max_units: 20 });
    if (sid) {
      router.replace(`/review/lab?session=${sid}`);
    }
  }, [createSession, router]);

  // Error state
  if (error && !session) {
    return (
      <div className="max-w-2xl mx-auto py-12">
        <ErrorState message={error} onAction={() => window.location.reload()} />
      </div>
    );
  }

  // Loading state
  if (loading || creating || !session) {
    return (
      <div className="max-w-2xl mx-auto py-24">
        <LoadingState title="Preparing review session" detail="Loading correct-only units and keyboard controls." />
      </div>
    );
  }

  const current = session.current_unit;
  const progress = Math.round(session.progress_pct * 100);

  return (
    <div className="max-w-2xl mx-auto pb-12">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Brain size={18} className="text-accent" />
          <h2 className="text-lg font-bold">Review Lab</h2>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted">
            {session.completed_unit_ids.length} / {session.units.length}
          </span>
          <button
            type="button"
            onClick={togglePause}
            className="rounded-lg border border-line bg-surface-field p-2 text-muted hover:text-foreground transition-colors"
            title={paused ? 'Resume (P)' : 'Pause (P)'}
            aria-label={paused ? 'Resume review session' : 'Pause review session'}
          >
            {paused ? <Play size={14} /> : <Pause size={14} />}
          </button>
        </div>
      </div>

      {/* Progress bar */}
      <div className="h-1.5 rounded-full bg-surface-field mb-6 overflow-hidden">
        <div
          className="h-full rounded-full bg-accent transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>

      <ShortcutHelp open={showShortcuts} onToggle={() => setShowShortcuts((value) => !value)} className="mb-6" />

      {/* Paused overlay */}
      {paused && (
        <div className="rounded-2xl border border-line bg-surface-raised p-8 text-center mb-6">
          <Pause size={32} className="mx-auto mb-3 text-muted" />
          <h3 className="text-lg font-semibold">Session Paused</h3>
          <p className="text-sm text-muted mt-1">Press P or click resume to continue.</p>
          <button
            type="button"
            onClick={togglePause}
            className="mt-4 rounded-xl bg-accent-solid hover:bg-accent-strong px-5 py-2 text-sm font-semibold text-white transition-colors"
          >
            Resume
          </button>
        </div>
      )}

      {/* Current unit */}
      {!paused && current && (
        <div className="space-y-4">
          {/* Unit card */}
          {current.interaction_mode === 'formula_input' || current.formula_latex ? (
            <FormulaLabCard
              prompt={current.prompt}
              formulaLatex={current.formula_latex || ''}
              recallInstruction={current.recall_instruction}
              answer={current.answer}
              workedExample={current.worked_example}
              commonWrongPath={current.common_wrong_path}
              examTrap={current.exam_trap}
              variables={current.variables}
              appliesWhen={current.applies_when}
              boundaryRules={current.boundary_rules}
              baIiPlusSteps={current.ba_ii_plus_steps}
              revealed={revealed}
              onReveal={reveal}
              subject={current.subject}
              dueReason={current.due_reason}
              memoryState={current.memory_state}
            />
          ) : (
            <RecallRevealCard
              prompt={current.prompt}
              recallInstruction={current.recall_instruction}
              answer={current.answer}
              workedExample={current.worked_example}
              commonWrongPath={current.common_wrong_path}
              examTrap={current.exam_trap}
              revealed={revealed}
              onReveal={reveal}
              unitType={current.unit_type}
              subject={current.subject}
              dueReason={current.due_reason}
              memoryState={current.memory_state}
            />
          )}

          {!revealed && (
            <label className="block rounded-xl border border-line bg-surface-field p-3">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-muted">
                Recall
              </span>
              <textarea
                value={recallDraft}
                onChange={(event) => setRecallDraft(event.target.value)}
                rows={4}
                placeholder="Write your answer before revealing."
                className="mt-2 w-full resize-none bg-transparent text-sm outline-none placeholder:text-muted"
              />
            </label>
          )}

          <div className="rounded-xl border border-line bg-surface-field p-3">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-muted">
              Why this today?
            </span>
            <p className="mt-1 text-sm leading-relaxed">
              {current.due_reason || 'Selected by review priority and memory state.'}
            </p>
            {current.source_refs?.length ? (
              <p className="mt-1 text-xs text-muted">
                Source: {current.source_refs.slice(0, 2).join(', ')}
              </p>
            ) : null}
          </div>

          {/* Hint */}
          {hintVisible && hintText && (
            <div className="rounded-xl bg-accent-soft border border-accent-soft p-3 text-sm animate-in fade-in">
              <span className="text-[10px] uppercase tracking-wider text-accent font-semibold">
                Hint
              </span>
              <p className="mt-1 text-sm">{hintText}</p>
            </div>
          )}

          {/* Hint button (only before reveal) */}
          {!revealed && !hintVisible && (
            <button
              type="button"
              onClick={requestHint}
              className="flex items-center gap-1.5 text-xs text-accent hover:underline"
            >
              <HelpCircle size={12} />
              Need a hint? (H)
            </button>
          )}

          {/* Outcome buttons (only after reveal) */}
          {revealed && (
            <div className="pt-2">
              <ReviewOutcomeButtons onOutcome={handleOutcome} disabled={submitting} />
              <p className="text-center text-[10px] text-muted mt-2">
                1 = Forgot · 2 = Partial · 3 = Recalled · S = Skip · ? = Shortcuts
              </p>
            </div>
          )}
        </div>
      )}

      {/* Completion */}
      {!paused && !current && session.is_complete && (
        <div className="text-center py-12">
          <RotateCcw size={32} className="mx-auto mb-3 text-muted" />
          <h3 className="text-lg font-semibold">All done!</h3>
          <button
            type="button"
            onClick={handleStartNew}
            className="mt-4 rounded-xl bg-accent-solid hover:bg-accent-strong px-5 py-2 text-sm font-semibold text-white transition-colors"
          >
            Start New Session
          </button>
        </div>
      )}

      {/* Completion modal */}
      <LabCompletionModal
        report={report}
        onClose={() => setShowCompletion(false)}
        onStartNew={handleStartNew}
      />
    </div>
  );
}
