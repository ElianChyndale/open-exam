'use client';

import { createContext, useContext, useEffect, useMemo, useState } from 'react';

import { languageApi } from '@/lib/api';
import { useReducedMotionSafe } from '@/lib/motion/useReducedMotionSafe';

const MotionContext = createContext({ enabled: false, reduced: false });

export function MotionProvider({ children }: { children: React.ReactNode }) {
  const reduced = useReducedMotionSafe();
  const [enabled, setEnabled] = useState(false);

  useEffect(() => {
    languageApi.settings()
      .then((settings) => setEnabled(Boolean(settings.gsap_motion_enabled)))
      .catch(() => setEnabled(false));
  }, []);

  const value = useMemo(() => ({ enabled: enabled && !reduced, reduced }), [enabled, reduced]);
  return <MotionContext.Provider value={value}>{children}</MotionContext.Provider>;
}

export function useMotionSettings() {
  return useContext(MotionContext);
}
