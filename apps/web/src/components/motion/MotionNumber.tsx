'use client';

import { useRef } from 'react';

import { gsap, useGSAP } from '@/lib/motion/gsap';
import { useMotionSettings } from './MotionProvider';

export function MotionNumber({ value }: { value: number }) {
  const node = useRef<HTMLSpanElement>(null);
  const { enabled } = useMotionSettings();

  useGSAP(() => {
    if (!node.current || !enabled) return;
    const counter = { value: 0 };
    gsap.to(counter, {
      value,
      duration: 0.45,
      onUpdate: () => {
        if (node.current) node.current.textContent = String(Math.round(counter.value));
      },
    });
  }, { dependencies: [enabled, value], revertOnUpdate: true });

  return <span ref={node}>{value}</span>;
}
