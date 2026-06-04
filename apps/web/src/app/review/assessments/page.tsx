'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  BarChart3,
  BookOpenCheck,
  Brain,
  CalendarCheck2,
  Calculator,
  CheckCircle2,
  CirclePlay,
  ClipboardCheck,
  Gauge,
  GitBranch,
  Languages,
  LineChart,
  Loader2,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  Target,
} from 'lucide-react';

import {
  AssessmentMode,
  AssessmentQuestion,
  AssessmentSession,
  assessmentsApi,
} from '@/lib/api';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';
import { ShortcutHelp } from '@/components/ux/UXStates';

const modeOptions: Array<{ value: AssessmentMode; label: string }> = [
  { value: 'quick_check', label: 'Quick' },
  { value: 'interleaving_drill', label: 'Interleaving' },
  { value: 'formula_drill', label: 'Formula' },
  { value: 'coverage_gap_drill', label: 'Coverage' },
  { value: 'mock_transfer_drill', label: 'Transfer' },
  { value: 'lexical_drill', label: 'Lexical' },
  { value: 'mixed_exam_drill', label: 'Mixed Exam' },
];

const focusOptions = ['mixed', 'coverage', 'formula', 'transfer', 'lexical'] as const;
const difficultyOptions = ['easy', 'medium', 'hard'] as const;

const systemLinks = [
  { href: '/review/tutor?mode=assessment_retro', label: 'Tutor', icon: Sparkles },
  { href: '/review/lab', label: 'Review Lab', icon: Brain },
  { href: '/review/formulas', label: 'Formula Lab', icon: Calculator },
  { href: '/review/coverage', label: 'Coverage', icon: BookOpenCheck },
  { href: '/review/mock-retro', label: 'Mock Retro', icon: GitBranch },
  { href: '/language/review', label: 'Language', icon: Languages },
  { href: '/review/analytics', label: 'Analytics', icon: LineChart },
  { href: '/review/study-planner', label: 'Planner', icon: CalendarCheck2 },
  { href: '/review/mission-control', label: 'Mission', icon: Gauge },
];

export default function AssessmentsPage() {
  const [mode, setMode] = useState<AssessmentMode>('interleaving_drill');
  const [targetMinutes, setTargetMinutes] = useState(30);
  const [questionCount, setQuestionCount] = useState(6);
  const [difficulty, setDifficulty] = useState<'easy' | 'medium' | 'hard'>('medium');
  const [focus, setFocus] = useState<(typeof focusOptions)[number]>('mixed');
  const [sessions, setSessions] = useState<AssessmentSession[]>([]);
  const [recommendations, setRecommendations] = useState<any>(null);
  const [session, setSession] = useState<AssessmentSession | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [selectedChoice, setSelectedChoice] = useState('');
  const [confidenceBefore, setConfidenceBefore] = useState(0.5);
  const [confidenceAfter, setConfidenceAfter] = useState(0.5);
  const [response, setResponse] = useState<any>(null);
  const [retro, setRetro] = useState<any>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [showShortcuts, setShowShortcuts] = useState(false);

  const load = async () => {
    try {
      const [list, recs] = await Promise.all([
        assessmentsApi.list(),
        assessmentsApi.recommendations(),
      ]);
      setSessions(list.assessments || []);
      setRecommendations(recs);
      if (!session && list.assessments?.[0]) {
        setSession(list.assessments[0]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Assessment load failed');
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const currentQuestion = session?.questions?.[currentIndex] || null;
  const answeredQuestionIds = useMemo(() => new Set((session?.responses || []).map((item: any) => item.question_id)), [session]);
  const scorePct = retro ? Math.round(Number(retro.score || 0) * 100) : Math.round(Number(session?.summary?.score || 0) * 100);

  const generate = async () => {
    setBusy(true);
    setError('');
    setResponse(null);
    setRetro(null);
    try {
      const generated = await assessmentsApi.generate({
        mode,
        target_minutes: targetMinutes,
        question_count: questionCount,
        difficulty,
        focus,
      });
      setSession(generated);
      setCurrentIndex(0);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Assessment generation failed');
    } finally {
      setBusy(false);
    }
  };

  const selectSession = async (assessmentId: string) => {
    setBusy(true);
    setError('');
    setResponse(null);
    setRetro(null);
    try {
      const next = await assessmentsApi.get(assessmentId);
      setSession(next);
      setCurrentIndex(0);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Assessment load failed');
    } finally {
      setBusy(false);
    }
  };

  const start = async () => {
    if (!session) return;
    setBusy(true);
    setError('');
    try {
      setSession(await assessmentsApi.start(session.assessment_id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Assessment start failed');
    } finally {
      setBusy(false);
    }
  };

  const submit = async () => {
    if (!currentQuestion) return;
    setBusy(true);
    setError('');
    try {
      const submitted = await assessmentsApi.answer(currentQuestion.question_id, {
        answer_text: currentQuestion.choices.length ? undefined : answer,
        selected_choice: currentQuestion.choices.length ? selectedChoice : undefined,
        confidence_before: confidenceBefore,
        time_spent_seconds: 30,
      });
      setResponse(submitted);
      setAnswer('');
      setSelectedChoice('');
      if (session) setSession(await assessmentsApi.get(session.assessment_id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Answer submission failed');
    } finally {
      setBusy(false);
    }
  };

  const selfGrade = async (grade: 'correct' | 'partial' | 'incorrect') => {
    if (!currentQuestion) return;
    setBusy(true);
    setError('');
    try {
      const graded = await assessmentsApi.selfGrade(currentQuestion.question_id, { grade, confidence_after: confidenceAfter });
      setResponse(graded);
      if (session) setSession(await assessmentsApi.get(session.assessment_id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Self-grade failed');
    } finally {
      setBusy(false);
    }
  };

  const nextQuestion = () => {
    if (!session) return;
    setResponse(null);
    setAnswer('');
    setSelectedChoice('');
    setCurrentIndex((value) => Math.min(value + 1, Math.max(0, session.questions.length - 1)));
  };

  const complete = async () => {
    if (!session) return;
    setBusy(true);
    setError('');
    try {
      const completed = await assessmentsApi.complete(session.assessment_id);
      setSession(completed);
      setRetro(await assessmentsApi.retro(session.assessment_id));
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Assessment completion failed');
    } finally {
      setBusy(false);
    }
  };

  useKeyboardShortcuts({
    enabled: Boolean(currentQuestion),
    revealed: Boolean(response),
    onAction: (action) => {
      if (action === 'help') {
        setShowShortcuts((value) => !value);
        return;
      }
      if (!currentQuestion || busy) return;
      if ((action === 'reveal' || action === 'submit') && !response) {
        if (answer.trim() || selectedChoice) submit();
      } else if (response && action === 'rate-forgot') {
        selfGrade('incorrect');
      } else if (response && action === 'rate-partial') {
        selfGrade('partial');
      } else if (response && (action === 'rate-recalled' || action === 'submit')) {
        selfGrade('correct');
      } else if (action === 'next') {
        nextQuestion();
      }
    },
  });

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <ClipboardCheck size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Adaptive Assessments</h2>
          </div>
          <p className="mt-1 text-sm text-muted">
            {session ? `${session.title} / ${session.status} / ${session.question_ids.length} questions` : 'Generate transfer-first practice'}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button type="button" onClick={load} disabled={busy} className="btn-secondary inline-flex items-center gap-2">
            <RefreshCw size={14} />
            Refresh
          </button>
          <button type="button" onClick={generate} disabled={busy} className="btn-primary inline-flex items-center gap-2">
            {busy ? <Loader2 size={15} className="animate-spin" /> : <Target size={15} />}
            Generate assessment
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="mb-4 flex items-start gap-2 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
        <ShieldCheck size={16} className="mt-0.5 shrink-0" />
        <span>Correct-only assessment feedback shows confirmed answers, rules, reasoning, boundaries, source refs, and next actions. Raw submitted misses are not reused as learning content.</span>
      </div>

      <ShortcutHelp
        open={showShortcuts}
        onToggle={() => setShowShortcuts((value) => !value)}
        className="mb-4"
        shortcuts={[
          { keys: 'Ctrl/⌘ + Enter', action: 'Submit answer or self-grade correct' },
          { keys: '1', action: 'Self-grade incorrect' },
          { keys: '2', action: 'Self-grade partial' },
          { keys: '3', action: 'Self-grade correct' },
          { keys: 'N', action: 'Next question' },
          { keys: '?', action: 'Show or hide this help' },
        ]}
      />

      <section className="mb-4 grid gap-3 xl:grid-cols-[minmax(0,1fr)_150px_150px_150px_150px]">
        <div className="rounded-lg border border-line bg-surface-raised p-3">
          <span className="mb-2 block text-xs font-semibold text-muted">Mode</span>
          <div className="grid gap-1 sm:grid-cols-4 xl:grid-cols-7">
            {modeOptions.map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setMode(option.value)}
                className={`rounded-md px-2 py-1.5 text-xs font-semibold transition-colors ${
                  mode === option.value ? 'bg-accent-solid text-white' : 'border border-line bg-surface-field text-muted hover:bg-surface-hover'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        <SelectBox label="Focus" value={focus} onChange={(value) => setFocus(value as typeof focus)} options={focusOptions} />
        <SelectBox label="Difficulty" value={difficulty} onChange={(value) => setDifficulty(value as typeof difficulty)} options={difficultyOptions} />
        <NumberBox label="Minutes" value={targetMinutes} onChange={setTargetMinutes} min={5} max={240} />
        <NumberBox label="Questions" value={questionCount} onChange={setQuestionCount} min={1} max={50} />
      </section>

      <div className="grid gap-4 xl:grid-cols-[300px_minmax(0,1fr)_330px]">
        <aside className="space-y-4">
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Assessment List</h3>
            <div className="mt-3 space-y-2">
              {sessions.length ? sessions.slice(0, 8).map((item) => (
                <button
                  key={item.assessment_id}
                  type="button"
                  onClick={() => selectSession(item.assessment_id)}
                  className={`w-full rounded-lg border p-3 text-left text-sm transition-colors ${
                    session?.assessment_id === item.assessment_id ? 'border-accent bg-accent-soft' : 'border-line bg-surface-field hover:bg-surface-hover'
                  }`}
                >
                  <span className="block font-semibold">{item.title}</span>
                  <span className="mt-1 block text-xs text-muted">{item.status} / {item.question_ids.length} questions</span>
                </button>
              )) : <p className="text-sm text-muted">No assessments yet.</p>}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Recommended Modes</h3>
            <div className="mt-3 space-y-2 text-sm">
              {(recommendations?.recommended_modes || []).map((item: string) => (
                <div key={item} className="rounded-lg border border-line bg-surface-field px-3 py-2 text-muted">
                  {labelize(item)}
                </div>
              ))}
            </div>
          </section>
        </aside>

        <main className="space-y-4">
          {session ? (
            <>
              <section className="grid gap-3 sm:grid-cols-4">
                <Metric icon={ClipboardCheck} label="Status" value={session.status} />
                <Metric icon={BarChart3} label="Questions" value={`${answeredQuestionIds.size}/${session.question_ids.length}`} />
                <Metric icon={CheckCircle2} label="Score" value={`${scorePct}%`} />
                <Metric icon={GitBranch} label="Gaps" value={String(session.summary?.transfer_gaps_created || retro?.transfer_gaps_created || 0)} />
              </section>

              {currentQuestion ? (
                <section className="rounded-lg border border-line bg-surface-raised">
                  <div className="flex flex-col gap-3 border-b border-line px-4 py-3 lg:flex-row lg:items-center lg:justify-between">
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="rounded border border-accent-soft bg-accent-soft px-2 py-0.5 text-xs font-semibold text-accent">
                          {currentIndex + 1} / {session.questions.length}
                        </span>
                        <span className="rounded border border-line bg-surface-field px-2 py-0.5 text-xs font-semibold text-muted">
                          {labelize(currentQuestion.question_type)}
                        </span>
                        <span className="rounded border border-line bg-surface-field px-2 py-0.5 text-xs font-semibold text-muted">
                          {currentQuestion.category}
                        </span>
                      </div>
                      <h3 className="mt-3 text-base font-semibold">{currentQuestion.prompt}</h3>
                    </div>
                    {session.status === 'draft' && (
                      <button type="button" onClick={start} disabled={busy} className="btn-secondary inline-flex items-center gap-2">
                        <CirclePlay size={14} />
                        Start
                      </button>
                    )}
                  </div>

                  <div className="space-y-4 p-4">
                    <div>
                      <label className="mb-2 block text-xs font-semibold text-muted" htmlFor="confidence-before">
                        Confidence before
                      </label>
                      <input
                        id="confidence-before"
                        type="range"
                        min={0}
                        max={1}
                        step={0.1}
                        value={confidenceBefore}
                        onChange={(event) => setConfidenceBefore(Number(event.target.value))}
                        className="w-full"
                      />
                    </div>

                    {currentQuestion.choices.length ? (
                      <div className="grid gap-2">
                        {currentQuestion.choices.map((choice) => (
                          <label key={choice} className="flex cursor-pointer items-start gap-2 rounded-lg border border-line bg-surface-field p-3 text-sm">
                            <input
                              type="radio"
                              name="assessment-choice"
                              checked={selectedChoice === choice}
                              onChange={() => setSelectedChoice(choice)}
                              className="mt-1"
                            />
                            <span>{choice}</span>
                          </label>
                        ))}
                      </div>
                    ) : (
                      <textarea
                        aria-label="Write assessment answer before feedback"
                        value={answer}
                        onChange={(event) => setAnswer(event.target.value)}
                        placeholder="Write your answer before revealing correct feedback."
                        className="min-h-[130px] w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
                      />
                    )}

                    <div className="flex flex-wrap gap-2">
                      <button
                        type="button"
                        onClick={submit}
                        disabled={busy || (!answer.trim() && !selectedChoice)}
                        className="btn-primary inline-flex items-center gap-2"
                      >
                        {busy ? <Loader2 size={15} className="animate-spin" /> : <CheckCircle2 size={15} />}
                        Submit answer
                      </button>
                      <button type="button" onClick={nextQuestion} disabled={!session.questions[currentIndex + 1]} className="btn-secondary inline-flex items-center gap-2">
                        Next question
                        <ArrowRight size={14} />
                      </button>
                      <button type="button" onClick={complete} disabled={busy || session.status === 'completed'} className="btn-secondary inline-flex items-center gap-2">
                        Complete assessment
                      </button>
                    </div>

                    {response && (
                      <FeedbackPanel
                        question={currentQuestion}
                        response={response}
                        confidenceAfter={confidenceAfter}
                        setConfidenceAfter={setConfidenceAfter}
                        selfGrade={selfGrade}
                        busy={busy}
                      />
                    )}
                  </div>
                </section>
              ) : (
                <section className="rounded-lg border border-line bg-surface-raised p-8 text-center text-sm text-muted">
                  No questions available from confirmed sources yet.
                </section>
              )}
            </>
          ) : (
            <section className="rounded-lg border border-line bg-surface-raised p-8 text-center text-sm text-muted">
              Generate an assessment to begin.
            </section>
          )}
        </main>

        <aside className="space-y-4">
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Source Mix</h3>
            <div className="mt-3 space-y-2 text-sm">
              {Object.entries(session?.summary?.category_counts || session?.source_signals?.category_counts || {}).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between gap-3 rounded-lg border border-line bg-surface-field px-3 py-2">
                  <span className="text-muted">{labelize(key)}</span>
                  <span className="font-semibold">{String(value)}</span>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Retro</h3>
            {retro || session?.retro?.score !== undefined ? (
              <RetroPanel retro={retro || session?.retro} />
            ) : (
              <p className="mt-3 text-sm text-muted">Complete the assessment to generate retro.</p>
            )}
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Links</h3>
            <div className="mt-3 grid grid-cols-2 gap-2">
              {systemLinks.map(({ href, label, icon: Icon }) => (
                <Link key={href} href={href} className="btn-secondary inline-flex items-center gap-2">
                  <Icon size={14} />
                  {label}
                </Link>
              ))}
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}

function FeedbackPanel({
  question,
  response,
  confidenceAfter,
  setConfidenceAfter,
  selfGrade,
  busy,
}: {
  question: AssessmentQuestion;
  response: any;
  confidenceAfter: number;
  setConfidenceAfter: (value: number) => void;
  selfGrade: (grade: 'correct' | 'partial' | 'incorrect') => void;
  busy: boolean;
}) {
  const feedback = response.feedback || {};
  return (
    <section className="rounded-lg border border-success-soft bg-success-soft p-4 text-sm">
      <div className="flex items-center justify-between gap-3">
        <h4 className="font-semibold text-success">Correct Feedback</h4>
        <span className="rounded border border-success bg-surface-raised px-2 py-0.5 text-xs font-semibold text-success">
          Score {Math.round(Number(response.score || 0) * 100)}%
        </span>
      </div>
      <div className="mt-3 grid gap-3 lg:grid-cols-2">
        <Info label="Correct Answer" value={feedback.correct_answer || question.correct_answer} />
        <Info label="Correct Rule" value={feedback.correct_rule || question.correct_rule} />
        <Info label="Correct Reasoning" value={feedback.correct_reasoning || question.correct_reasoning} />
        <Info label="Next Action" value={feedback.next_action || 'advance'} />
      </div>
      {feedback.ba_ii_plus_steps?.length > 0 && (
        <div className="mt-3 rounded-lg border border-line bg-surface-raised p-3">
          <p className="text-xs font-semibold text-muted">BA II Plus</p>
          <ol className="mt-2 list-decimal pl-4">
            {feedback.ba_ii_plus_steps.map((step: string) => <li key={step}>{step}</li>)}
          </ol>
        </div>
      )}
      <div className="mt-4">
        <label className="mb-2 block text-xs font-semibold text-muted" htmlFor="confidence-after">
          Confidence after
        </label>
        <input
          id="confidence-after"
          type="range"
          min={0}
          max={1}
          step={0.1}
          value={confidenceAfter}
          onChange={(event) => setConfidenceAfter(Number(event.target.value))}
          className="w-full"
        />
      </div>
      <div className="mt-3 flex flex-wrap gap-2">
        <button type="button" onClick={() => selfGrade('correct')} disabled={busy} className="btn-secondary">Self-grade correct</button>
        <button type="button" onClick={() => selfGrade('partial')} disabled={busy} className="btn-secondary">Self-grade partial</button>
        <button type="button" onClick={() => selfGrade('incorrect')} disabled={busy} className="btn-secondary">Self-grade incorrect</button>
      </div>
    </section>
  );
}

function RetroPanel({ retro }: { retro: any }) {
  return (
    <div className="mt-3 space-y-3 text-sm">
      <div className="grid grid-cols-2 gap-2">
        <Info label="Score" value={`${Math.round(Number(retro.score || 0) * 100)}%`} />
        <Info label="Transfer Gaps" value={String(retro.transfer_gaps_created || 0)} />
        <Info label="Calibration" value={`${Math.round(Number(retro.confidence_calibration?.calibration_error || 0) * 100)}%`} />
        <Info label="Answered" value={`${retro.answered_count || 0}/${retro.question_count || 0}`} />
      </div>
      <div className="rounded-lg border border-line bg-surface-field p-3">
        <p className="text-xs font-semibold text-muted">Correct Rules To Review</p>
        <div className="mt-2 space-y-2">
          {(retro.correct_rules_to_review || []).slice(0, 4).map((item: any) => (
            <p key={item.question_id} className="leading-5">{item.correct_rule || item.correct_answer}</p>
          ))}
          {!(retro.correct_rules_to_review || []).length && <p className="text-muted">No rules queued.</p>}
        </div>
      </div>
      <div className="space-y-2">
        {(retro.recommended_next_actions || []).map((item: any) => (
          <Link key={item.title} href={item.href} className="flex items-center justify-between gap-3 rounded-lg border border-line bg-surface-field px-3 py-2">
            <span>{item.title}</span>
            <ArrowRight size={14} />
          </Link>
        ))}
      </div>
    </div>
  );
}

function SelectBox({ label, value, onChange, options }: { label: string; value: string; onChange: (value: string) => void; options: readonly string[] }) {
  return (
    <label className="rounded-lg border border-line bg-surface-raised p-3 text-xs font-semibold text-muted">
      {label}
      <select value={value} onChange={(event) => onChange(event.target.value)} className="mt-2 w-full rounded-lg border border-line bg-surface-field px-2 py-2 text-sm text-foreground">
        {options.map((option) => <option key={option} value={option}>{labelize(option)}</option>)}
      </select>
    </label>
  );
}

function NumberBox({ label, value, onChange, min, max }: { label: string; value: number; onChange: (value: number) => void; min: number; max: number }) {
  return (
    <label className="rounded-lg border border-line bg-surface-raised p-3 text-xs font-semibold text-muted">
      {label}
      <input
        type="number"
        min={min}
        max={max}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        className="mt-2 w-full rounded-lg border border-line bg-surface-field px-2 py-2 text-sm text-foreground"
      />
    </label>
  );
}

function Metric({ icon: Icon, label, value }: { icon: typeof CheckCircle2; label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-surface-raised p-4">
      <div className="flex items-center justify-between gap-3">
        <Icon size={18} className="text-accent" />
        <span className="text-lg font-bold">{value}</span>
      </div>
      <p className="mt-2 text-xs font-semibold text-muted">{label}</p>
    </div>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-surface-raised p-3">
      <p className="text-xs font-semibold text-muted">{label}</p>
      <p className="mt-1 leading-5">{value}</p>
    </div>
  );
}

function labelize(value: string) {
  return value.replace(/_/g, ' ').replace(/\b\w/g, (match) => match.toUpperCase());
}
