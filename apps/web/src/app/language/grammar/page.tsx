'use client';

import { useEffect, useState } from 'react';

import { languageApi, LanguageSegment } from '@/lib/api';
import { GrammarTreeMotion } from '@/components/language/GrammarTreeMotion';
import { LanguageShell } from '@/components/language/LanguageShell';

export default function LanguageGrammar() {
  const [segments, setSegments] = useState<LanguageSegment[]>([]);
  const [segmentId, setSegmentId] = useState('');
  const [analysis, setAnalysis] = useState<Record<string, any> | null>(null);
  const [message, setMessage] = useState('');
  useEffect(() => { languageApi.segments().then(({ segments: rows }) => { setSegments(rows); setSegmentId(rows[0]?.segment_id || ''); }); }, []);
  const analyze = async () => {
    if (!segmentId) return setMessage('Import a sentence first.');
    const result = await languageApi.analyzeGrammar(segmentId);
    setAnalysis(result); setMessage(result.cache_hit ? 'Loaded cached editable analysis.' : 'Created deterministic baseline analysis.');
  };
  return (
    <LanguageShell title="Make sentence structure visible." eyebrow="Grammar lens">
      <section className="motion-reveal card space-y-4">
        <div className="flex flex-col gap-3 sm:flex-row">
          <select value={segmentId} onChange={(event) => setSegmentId(event.target.value)} className="min-w-0 flex-1 rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"><option value="">Choose segment</option>{segments.map((segment) => <option key={segment.segment_id} value={segment.segment_id}>{segment.text}</option>)}</select>
          <button type="button" onClick={analyze} className="rounded-lg bg-accent-solid px-4 py-2 text-sm text-white">Analyze sentence</button>
        </div>
        {message ? <p role="status" className="text-xs text-muted">{message}</p> : null}
        <GrammarTreeMotion analysis={analysis} />
      </section>
    </LanguageShell>
  );
}
