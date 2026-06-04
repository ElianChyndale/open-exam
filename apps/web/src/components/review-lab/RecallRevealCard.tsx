'use client';

import { useRef, useState } from 'react';

interface RecallRevealCardProps {
  prompt: string;
  recallInstruction?: string;
  answer?: string;
  workedExample?: string;
  commonWrongPath?: string;
  examTrap?: string;
  revealed: boolean;
  onReveal: () => void;
  unitType?: string;
  subject?: string;
  dueReason?: string;
  memoryState?: string;
}

/**
 * RecallRevealCard — shows prompt, hides answer until revealed.
 *
 * The answer is NEVER rendered in the DOM until revealed=true.
 * This prevents accidental spoilers from screen readers, find-in-page,
 * or dev tools inspection before the learner attempts recall.
 */
export function RecallRevealCard({
  prompt,
  recallInstruction,
  answer,
  workedExample,
  commonWrongPath,
  examTrap,
  revealed,
  onReveal,
  unitType,
  subject,
  dueReason,
  memoryState,
}: RecallRevealCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [showWork, setShowWork] = useState(false);

  return (
    <div
      ref={cardRef}
      className="w-full rounded-2xl border border-line bg-surface-raised p-6 text-left"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="metric-label text-[10px] uppercase tracking-wider">
            {unitType?.replace('_', ' ') || 'Recall'}
          </span>
          {subject && (
            <span className="text-[10px] text-muted bg-surface-field px-2 py-0.5 rounded-full">
              {subject}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {memoryState && (
            <span className="text-[10px] text-muted">
              {memoryState}
            </span>
          )}
          {dueReason && (
            <span className="text-[10px] text-warning">
              {dueReason}
            </span>
          )}
        </div>
      </div>

      {/* Prompt */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold leading-relaxed">{prompt}</h3>
        {recallInstruction && !revealed && (
          <p className="mt-2 text-sm text-muted">{recallInstruction}</p>
        )}
      </div>

      {/* Reveal button or answer */}
      {!revealed ? (
        <button
          type="button"
          onClick={onReveal}
          className="w-full rounded-xl border-2 border-dashed border-accent-soft bg-surface-field py-8 text-sm font-medium text-accent hover:bg-accent-soft transition-colors"
        >
          <span className="block text-lg mb-1">Reveal Answer</span>
          <span className="text-xs text-muted">Space to reveal</span>
        </button>
      ) : (
        <div className="space-y-4 animate-in fade-in duration-200">
          {/* Answer */}
          {answer && (
            <div className="rounded-xl bg-success-soft border border-success-soft p-4">
              <span className="text-[10px] uppercase tracking-wider text-success font-semibold">Answer</span>
              <p className="mt-1 text-sm leading-relaxed whitespace-pre-wrap">{answer}</p>
            </div>
          )}

          {/* Worked example toggle */}
          {workedExample && (
            <div>
              <button
                type="button"
                onClick={() => setShowWork((s) => !s)}
                className="text-xs text-accent hover:underline"
              >
                {showWork ? 'Hide worked example' : 'Show worked example'}
              </button>
              {showWork && (
                <div className="mt-2 rounded-lg bg-surface-field border border-line p-3 text-sm leading-relaxed whitespace-pre-wrap">
                  {workedExample}
                </div>
              )}
            </div>
          )}

          {/* Common wrong path */}
          {commonWrongPath && (
            <div className="rounded-lg bg-danger-soft border border-danger-soft p-3">
              <span className="text-[10px] uppercase tracking-wider text-danger font-semibold">Common Mistake</span>
              <p className="mt-1 text-xs leading-relaxed">{commonWrongPath}</p>
            </div>
          )}

          {/* Exam trap */}
          {examTrap && (
            <div className="rounded-lg bg-warning-soft border border-warning-soft p-3">
              <span className="text-[10px] uppercase tracking-wider text-warning font-semibold">Exam Trap</span>
              <p className="mt-1 text-xs leading-relaxed">{examTrap}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
