'use client';

import { useRef } from 'react';

import { gsap, useGSAP } from '@/lib/motion/gsap';
import { useMotionSettings } from '@/components/motion/MotionProvider';

export function IntuitionGraph({ edges }: { edges: Record<string, any>[] }) {
  const root = useRef<HTMLDivElement>(null);
  const { enabled } = useMotionSettings();

  useGSAP(() => {
    if (!enabled) return;
    gsap.from('.intuition-node', { opacity: 0, scale: 0.96, stagger: 0.035, duration: 0.24, clearProps: 'transform' });
  }, { scope: root, dependencies: [enabled, edges.length], revertOnUpdate: true });

  return (
    <div ref={root} className="grid gap-3 sm:grid-cols-2">
      {edges.map((edge) => (
        <div key={edge.edge_id} className="intuition-node rounded-xl border border-line bg-surface-field p-4">
          <span className="metric-label">{edge.edge_type}</span>
          <p className="mt-2 break-all text-xs text-muted">{edge.source_item_id} → {edge.target_item_id}</p>
        </div>
      ))}
      {edges.length === 0 ? <p className="text-sm text-muted">Collect related expressions, then rebuild the graph.</p> : null}
    </div>
  );
}
