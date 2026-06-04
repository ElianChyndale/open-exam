'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';
import { AlertTriangle, BookOpenCheck, CheckCircle2, Eye, Loader2, SkipForward, XCircle } from 'lucide-react';

import { languageOsApi } from '@/lib/api';
import { LanguageShell } from '@/components/language/LanguageShell';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';
import { EmptyState, ShortcutHelp, SourceRefsPanel } from '@/components/ux/UXStates';

type LexicalReviewUnit = {
  unit_id: string;
  session_id: string;
  lexical_id: string;
  display_mode: string;
  front_prompt: string;
  correct_answer: string;
  correct_reasoning: string;
  example_sentence?: string | null;
  example_translation?: string | null;
  collocations: string[];
  usage_notes: string[];
  source_refs: string[];
  memory_state_before?: string | null;
  headword: string;
  translation?: string | null;
};

type LexicalSession = {
  session_id: string;
  profile_id: string;
  status: string;
  units: LexicalReviewUnit[];
  current_unit_index: number;
  completed_unit_ids: string[];
  outcomes: any[];
};

const outcomes = [
  { id: 'forgot', label: 'Forgot', icon: XCircle },
  { id: 'partial', label: 'Partial', icon: AlertTriangle },
  { id: 'recalled', label: 'Recalled', icon: CheckCircle2 },
  { id: 'skipped', label: 'Skip', icon: SkipForward },
] as const;

export default function LanguageReview() {
  const [session, setSession] = useState<LexicalSession | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [showShortcuts, setShowShortcuts] = useState(false);

  const unit = session?.units?.[session.current_unit_index] || null;
  const progress = useMemo(() => {
    if (!session?.units?.length) return 0;
    return Math.round((session.completed_unit_ids.length / session.units.length) * 100);
  }, [session]);

  const generate = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    setRevealed(false);
    try {
      const created = await languageOsApi.generateReviewSession({ max_units: 10 });
      setSession(created);
      if (!created.units?.length) {
        setMessage('No confirmed lexical assets are ready for review.');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Lexical review generation failed');
    } finally {
      setBusy(false);
    }
  };

  const complete = async (outcome: typeof outcomes[number]['id']) => {
    if (!unit || !session) return;
    setBusy(true);
    setError('');
    try {
      const result = await languageOsApi.completeReviewUnit(unit.unit_id, {
        session_id: session.session_id,
        outcome,
        time_spent_seconds: 20,
      });
      setSession(result.session);
      setRevealed(false);
      setMessage(result.memory_update?.next_review_at ? `Next review: ${new Date(result.memory_update.next_review_at).toLocaleString()}` : '');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Review completion failed');
    } finally {
      setBusy(false);
    }
  };

  useKeyboardShortcuts({
    enabled: true,
    revealed,
    onAction: (action) => {
      if (action === 'help') {
        setShowShortcuts((value) => !value);
        return;
      }
      if (!unit || busy) return;
      if (action === 'reveal' || (action === 'submit' && !revealed)) {
        setRevealed(true);
      } else if (action === 'rate-forgot') {
        complete('forgot');
      } else if (action === 'rate-partial') {
        complete('partial');
      } else if (action === 'rate-recalled' || action === 'submit') {
        complete('recalled');
      } else if (action === 'rate-skipped' || action === 'next') {
        complete('skipped');
      }
    },
  });

  return (
    <LanguageShell title="Lexical Review" eyebrow="Recall-first vocabulary">
      {error && (
        <div className="flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <section className="mx-auto max-w-3xl space-y-4">
        <div className="card flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase text-muted">Session</p>
            <p className="mt-1 text-sm text-muted">
              {session ? `${session.completed_unit_ids.length} / ${session.units.length} complete · ${progress}%` : 'No active lexical session'}
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link href="/language/dictionaries" className="btn-secondary inline-flex items-center gap-2">
              <BookOpenCheck size={14} />
              Dictionaries
            </Link>
            <button type="button" onClick={generate} disabled={busy} className="btn-primary inline-flex items-center gap-2">
              {busy ? <Loader2 size={15} className="animate-spin" /> : <BookOpenCheck size={15} />}
              Generate lexical review
            </button>
          </div>
        </div>

        <ShortcutHelp open={showShortcuts} onToggle={() => setShowShortcuts((value) => !value)} />

        {message && <p role="status" className="text-sm text-muted">{message}</p>}

        {!unit ? (
          <EmptyState title="No lexical unit active" detail="Confirm dictionary assets, then generate a lexical review session." actionHref="/language/dictionaries" actionLabel="Open dictionaries" />
        ) : (
          <article className="card">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="text-xs font-semibold uppercase text-muted">{unit.display_mode}</p>
                <h3 className="mt-2 text-xl font-bold">{unit.front_prompt}</h3>
                <p className="mt-2 text-sm text-muted">
                  {unit.memory_state_before || 'new'} / {unit.headword}
                </p>
              </div>
              <span className="rounded border border-line bg-surface-field px-2 py-1 text-xs text-muted">
                {session ? `${session.current_unit_index + 1} / ${session.units.length}` : ''}
              </span>
            </div>

            <textarea
              aria-label="Write your lexical answer before reveal"
              className="input mt-5 w-full resize-none text-sm leading-6"
              rows={4}
              placeholder="Write your answer before revealing."
            />

            {!revealed ? (
              <button type="button" onClick={() => setRevealed(true)} className="btn-primary mt-4 inline-flex items-center gap-2">
                <Eye size={15} />
                Reveal answer
              </button>
            ) : (
              <div className="mt-5 space-y-4">
                <div className="rounded-lg border border-line bg-surface-field p-4">
                  <p className="text-xs font-semibold uppercase text-muted">Correct answer</p>
                  <p className="mt-2 text-sm leading-6">{unit.correct_answer}</p>
                  {unit.example_translation && <p className="mt-2 text-sm text-muted">{unit.example_translation}</p>}
                </div>

                {unit.example_sentence && (
                  <Detail title="Example" items={[unit.example_sentence]} />
                )}
                <Detail title="Collocations" items={unit.collocations} />
                <Detail title="Usage notes" items={unit.usage_notes} />
                <SourceRefsPanel refs={unit.source_refs} />

                <div className="grid gap-2 sm:grid-cols-4">
                  {outcomes.map(({ id, label, icon: Icon }) => (
                    <button
                      key={id}
                      type="button"
                      onClick={() => complete(id)}
                      disabled={busy}
                      className="btn-secondary inline-flex items-center justify-center gap-2"
                    >
                      <Icon size={14} />
                      {label}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </article>
        )}
      </section>
    </LanguageShell>
  );
}

function Detail({ title, items }: { title: string; items: string[] }) {
  if (!items.length) return null;
  return (
    <div>
      <p className="text-xs font-semibold uppercase text-muted">{title}</p>
      <div className="mt-2 flex flex-wrap gap-2">
        {items.map((item) => (
          <span key={item} className="rounded border border-line bg-surface-field px-2 py-1 text-xs text-muted">
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}
