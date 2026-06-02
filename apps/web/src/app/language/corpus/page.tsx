'use client';

import { useCallback, useEffect, useState } from 'react';

import { languageApi, LanguageItem, LanguageSegment, LanguageSource } from '@/lib/api';
import { LanguageShell } from '@/components/language/LanguageShell';

export default function LanguageCorpus() {
  const [sources, setSources] = useState<LanguageSource[]>([]);
  const [segments, setSegments] = useState<LanguageSegment[]>([]);
  const [items, setItems] = useState<LanguageItem[]>([]);
  const [form, setForm] = useState({ item_type: 'phrase', canonical_form: '', language: 'en', segment_id: '' });
  const [message, setMessage] = useState('');

  const refresh = useCallback(() => Promise.all([languageApi.sources(), languageApi.segments(), languageApi.items()]).then(([sourceData, segmentData, itemData]) => {
    setSources(sourceData.sources); setSegments(segmentData.segments); setItems(itemData.items);
    if (segmentData.segments[0]) setForm((value) => value.segment_id ? value : ({ ...value, segment_id: segmentData.segments[0].segment_id, language: sourceData.sources.find((source) => source.source_id === segmentData.segments[0].source_id)?.language || 'en' }));
  }), []);
  useEffect(() => { void refresh(); }, [refresh]);

  const collect = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const result = await languageApi.collectItem(form);
      setMessage(result.merged ? 'Merged with the historical item.' : 'Collected with source context.');
      setForm({ ...form, canonical_form: '' });
      await refresh();
    } catch (error) { setMessage(error instanceof Error ? error.message : 'Collection failed.'); }
  };

  return (
    <LanguageShell title="A corpus you can trace back to the sentence." eyebrow="Personal corpus">
      <form onSubmit={collect} className="motion-reveal card grid gap-3 sm:grid-cols-[140px_1fr_1fr_auto]">
        <select value={form.item_type} onChange={(event) => setForm({ ...form, item_type: event.target.value })} className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"><option>word</option><option>phrase</option><option>sentence</option><option>grammar_pattern</option><option>idiom</option><option>collocation</option></select>
        <input required value={form.canonical_form} onChange={(event) => setForm({ ...form, canonical_form: event.target.value })} placeholder="Expression to collect" className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm" />
        <select required value={form.segment_id} onChange={(event) => setForm({ ...form, segment_id: event.target.value })} className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"><option value="">Choose source segment</option>{segments.map((segment) => <option key={segment.segment_id} value={segment.segment_id}>{segment.text.slice(0, 56)}</option>)}</select>
        <button className="rounded-lg bg-accent-solid px-4 py-2 text-sm text-white">Collect</button>
        {message ? <p role="status" className="text-xs text-muted sm:col-span-4">{message}</p> : null}
      </form>
      <div className="grid gap-4 lg:grid-cols-[0.85fr_1.15fr]">
        <section className="motion-reveal card"><h3 className="font-semibold">Sources ({sources.length})</h3><div className="mt-4 space-y-2">{sources.map((source) => <div key={source.source_id} className="rounded-xl border border-line p-3"><p className="text-sm font-medium">{source.title}</p><p className="mt-1 text-xs text-muted">{source.source_type} · {source.language}</p></div>)}</div></section>
        <section className="motion-reveal card"><h3 className="font-semibold">Collected items ({items.length})</h3><div className="mt-4 grid gap-2 sm:grid-cols-2">{items.map((item) => <div key={item.item_id} className="rounded-xl border border-line p-3"><p className="text-sm font-medium">{item.canonical_form}</p><p className="mt-1 text-xs text-muted">{item.item_type} · {item.language}</p></div>)}</div></section>
      </div>
    </LanguageShell>
  );
}
