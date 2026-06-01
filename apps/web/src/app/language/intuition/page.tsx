'use client';

import { useEffect, useState } from 'react';

import { languageApi, LanguageItem } from '@/lib/api';
import { IntuitionGraph } from '@/components/language/IntuitionGraph';
import { LanguageShell } from '@/components/language/LanguageShell';

export default function LanguageIntuition() {
  const [edges, setEdges] = useState<Record<string, any>[]>([]);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<LanguageItem[]>([]);
  const refresh = () => languageApi.graph().then((result) => setEdges(result.edges));
  useEffect(() => { void refresh(); }, []);
  const rebuild = async () => setEdges((await languageApi.rebuildGraph()).edges);
  const search = async (event: React.FormEvent) => { event.preventDefault(); if (query) setResults((await languageApi.searchGraph(query)).items); };
  return (
    <LanguageShell title="See where expressions reinforce or confuse each other." eyebrow="Intuition network">
      <div className="grid gap-4 lg:grid-cols-[0.7fr_1.3fr]">
        <section className="motion-reveal card space-y-4">
          <form onSubmit={search} className="flex gap-2"><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search meaning or expression" className="min-w-0 flex-1 rounded-lg border border-line bg-surface-field px-3 py-2 text-sm" /><button className="rounded-lg border border-accent px-3 text-sm text-accent">Search</button></form>
          <button type="button" onClick={rebuild} className="text-sm text-accent">Rebuild deterministic graph</button>
          <div className="space-y-2">{results.map((item) => <div key={item.item_id} className="rounded-xl border border-line p-3 text-sm">{item.canonical_form}</div>)}</div>
        </section>
        <section className="motion-reveal card"><IntuitionGraph edges={edges} /></section>
      </div>
    </LanguageShell>
  );
}
