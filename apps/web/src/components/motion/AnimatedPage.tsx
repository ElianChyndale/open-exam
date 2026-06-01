'use client';

import { useRef } from 'react';

import { gsap, useGSAP } from '@/lib/motion/gsap';
import { motionTokens } from '@/lib/motion/motion-tokens';
import { useMotionSettings } from './MotionProvider';

export function AnimatedPage({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  const root = useRef<HTMLDivElement>(null);
  const { enabled } = useMotionSettings();

  useGSAP(() => {
    if (!enabled) return;
    gsap.from('.motion-reveal', {
      opacity: 0,
      y: 14,
      duration: motionTokens.duration.normal,
      ease: motionTokens.ease.enter,
      stagger: motionTokens.stagger.list,
      clearProps: 'transform',
    });
  }, { scope: root, dependencies: [enabled], revertOnUpdate: true });

  return <div ref={root} data-motion-enabled={enabled ? 'true' : 'false'} className={className}>{children}</div>;
}
