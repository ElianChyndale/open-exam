'use client';

import { useRef, useState } from 'react';

import { gsap, useGSAP } from '@/lib/motion/gsap';
import { motionTokens } from '@/lib/motion/motion-tokens';
import { useMotionSettings } from './MotionProvider';

export function FlipReviewCard({ front, back }: { front: React.ReactNode; back: React.ReactNode }) {
  const card = useRef<HTMLButtonElement>(null);
  const [revealed, setRevealed] = useState(false);
  const { enabled } = useMotionSettings();

  useGSAP(() => {
    if (!enabled || !card.current) return;
    gsap.fromTo(card.current, { rotateY: revealed ? -10 : 10 }, {
      rotateY: 0,
      duration: motionTokens.duration.fast,
      ease: motionTokens.ease.standard,
      clearProps: 'transform',
    });
  }, { scope: card, dependencies: [enabled, revealed], revertOnUpdate: true });

  return (
    <button
      ref={card}
      type="button"
      onClick={() => setRevealed((value) => !value)}
      aria-pressed={revealed}
      className="language-review-card min-h-56 w-full rounded-2xl border border-line p-6 text-left"
    >
      <span className="metric-label">{revealed ? 'Answer' : 'Recall first'}</span>
      <div className="mt-6 text-xl font-semibold leading-relaxed">{revealed ? back : front}</div>
      <span className="mt-8 block text-xs text-muted">{revealed ? 'Tap to hide answer' : 'Tap to reveal answer'}</span>
    </button>
  );
}
