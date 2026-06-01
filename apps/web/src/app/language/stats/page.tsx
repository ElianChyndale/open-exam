'use client';

import { useEffect, useState } from 'react';

import { languageApi } from '@/lib/api';
import { LanguageShell } from '@/components/language/LanguageShell';
import { MotionNumber } from '@/components/motion/MotionNumber';

export default function LanguageStats() {
  const [stats, setStats] = useState<Record<string, number | string>>({});
  const [message, setMessage] = useState('');
  useEffect(() => { languageApi.stats().then(setStats); }, []);
  const exportData = async (format: 'anki' | 'csv' | 'markdown' | 'obsidian') => {
    const result = await languageApi.export(format);
    setMessage(`${format.toUpperCase()} projection ready: ${result.item_count} item(s), ${result.content.length} characters.`);
  };
  return (
    <LanguageShell title="Measure the practice, not just the pile of cards." eyebrow="Language metrics">
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{Object.entries(stats).filter(([, value]) => typeof value === 'number').map(([key, value]) => <div key={key} className="motion-reveal card"><span className="metric-label">{key.replaceAll('_', ' ')}</span><div className="metric-value mt-3"><MotionNumber value={Number(value)} /></div></div>)}</div>
      <section className="motion-reveal card"><h3 className="font-semibold">Projection exports</h3><div className="mt-4 flex flex-wrap gap-2">{(['anki', 'csv', 'markdown', 'obsidian'] as const).map((format) => <button key={format} type="button" onClick={() => exportData(format)} className="rounded-full border border-line px-3 py-2 text-xs uppercase text-muted hover:text-accent">{format}</button>)}</div>{message ? <p role="status" className="mt-4 text-sm text-muted">{message}</p> : null}</section>
    </LanguageShell>
  );
}
