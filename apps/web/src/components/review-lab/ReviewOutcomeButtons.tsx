'use client';

import { useEffect, useState } from 'react';

interface ReviewOutcomeButtonsProps {
  onOutcome: (outcome: 'forgot' | 'partial' | 'recalled' | 'skipped') => void;
  disabled?: boolean;
}

/**
 * ReviewOutcomeButtons — 1-4 keys for again/hard/good/easy.
 *
 * 1 = forgot      (Again)
 * 2 = partial     (Hard)
 * 3 = recalled    (Good)
 * 4 = skipped     (Skip)
 */
export function ReviewOutcomeButtons({ onOutcome, disabled }: ReviewOutcomeButtonsProps) {
  const [pressed, setPressed] = useState<string | null>(null);

  useEffect(() => {
    if (!pressed) return;
    const timer = setTimeout(() => setPressed(null), 150);
    return () => clearTimeout(timer);
  }, [pressed]);

  const buttons = [
    {
      key: '1',
      label: 'Forgot',
      sub: 'Again',
      outcome: 'forgot' as const,
      color: 'bg-danger-solid hover:bg-danger-strong',
      ring: 'ring-danger',
    },
    {
      key: '2',
      label: 'Partial',
      sub: 'Hard',
      outcome: 'partial' as const,
      color: 'bg-warning-solid hover:bg-warning-strong',
      ring: 'ring-warning',
    },
    {
      key: '3',
      label: 'Recalled',
      sub: 'Good',
      outcome: 'recalled' as const,
      color: 'bg-success-solid hover:bg-success-strong',
      ring: 'ring-success',
    },
    {
      key: '4',
      label: 'Skip',
      sub: 'Later',
      outcome: 'skipped' as const,
      color: 'bg-surface-field hover:bg-surface text-muted border border-line',
      ring: 'ring-line',
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
      {buttons.map((btn) => (
        <button
          key={btn.key}
          type="button"
          disabled={disabled}
          onClick={() => {
            setPressed(btn.key);
            onOutcome(btn.outcome);
          }}
          className={`
            relative rounded-xl px-3 py-4 text-sm font-semibold text-white
            transition-all duration-100 active:scale-95
            ${btn.color}
            ${disabled ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer'}
            ${pressed === btn.key ? `ring-2 ${btn.ring} ring-offset-2 ring-offset-surface` : ''}
          `}
        >
          <span className="block text-lg">{btn.key}</span>
          <span className="block text-xs mt-0.5">{btn.label}</span>
          <span className="block text-[10px] opacity-70">{btn.sub}</span>
        </button>
      ))}
    </div>
  );
}
