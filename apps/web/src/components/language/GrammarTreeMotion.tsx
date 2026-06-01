'use client';

import { useRef } from 'react';

import { gsap, useGSAP } from '@/lib/motion/gsap';
import { useMotionSettings } from '@/components/motion/MotionProvider';

export function GrammarTreeMotion({ analysis }: { analysis: Record<string, any> | null }) {
  const root = useRef<HTMLDivElement>(null);
  const { enabled } = useMotionSettings();

  useGSAP(() => {
    if (!enabled) return;
    gsap.timeline().from('.grammar-node', { opacity: 0, x: -10, stagger: 0.07, duration: 0.28, clearProps: 'transform' });
  }, { scope: root, dependencies: [enabled, analysis?.analysis_id], revertOnUpdate: true });

  if (!analysis) return <p className="text-sm text-muted">Choose a segment to open the Grammar Lens.</p>;
  return (
    <div ref={root} className="space-y-3">
      {(analysis.clauses || []).map((clause: Record<string, string>, index: number) => (
        <div key={`${clause.text}-${index}`} className="grammar-node rounded-xl border border-line bg-surface-field p-4">
          <span className="metric-label">{clause.clause_type}</span>
          <p className="mt-1 text-sm leading-6">{clause.text}</p>
        </div>
      ))}
      {(analysis.spanish_features || []).length > 0 ? (
        <div className="grammar-node rounded-xl border border-accent-soft bg-accent-soft p-4 text-sm">
          Spanish features: {(analysis.spanish_features || []).map((feature: Record<string, string>) => feature.surface).join(', ')}
        </div>
      ) : null}
    </div>
  );
}
