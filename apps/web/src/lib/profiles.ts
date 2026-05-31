'use client';

import { useEffect, useState } from 'react';
import { profilesApi } from '@/lib/api';

export const CFA_SUBJECTS = [
  'Quantitative Methods', 'Economics', 'Financial Statement Analysis',
  'Corporate Issuers', 'Equity', 'Fixed Income', 'Derivatives',
  'Alternative Investments', 'Portfolio Management', 'Ethical and Professional Standards',
];

export function useProfileSubjects() {
  const [subjects, setSubjects] = useState(CFA_SUBJECTS);
  useEffect(() => {
    profilesApi.getActive().then(({ profile }: any) => {
      const next = (profile.subjects || []).map((subject: any) => subject.name).filter(Boolean);
      if (next.length) setSubjects(next);
    }).catch(() => undefined);
  }, []);
  return subjects;
}
