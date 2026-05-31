'use client';

import { useState } from 'react';
import { FileSearch } from 'lucide-react';
import { searchApi, SearchResult } from '@/lib/api';
import { Badge, EmptyState, SearchField, Surface } from '@/components/ui/ui';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searched, setSearched] = useState(false);

  const search = async () => {
    if (!query.trim()) return;
    setSearched(true);
    setResults((await searchApi.search(query)).results);
  };

  return (
    <div className="mx-auto max-w-4xl space-y-5">
      <header>
        <p className="metric-label">SQLite FTS5</p>
        <h1 className="mt-1 text-3xl font-semibold tracking-tight">Search knowledge</h1>
        <p className="mt-2 text-sm text-muted">Search curriculum, verified private questions, and evidence-derived mistake cards.</p>
      </header>
      <SearchField value={query} onChange={(event) => setQuery(event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter') search(); }} placeholder="Search duration, FX quotes, ethics..." autoFocus />
      {searched && results.length === 0 ? <EmptyState title="No matching evidence" detail="Try a module name, LOS keyword, or formula concept." /> : null}
      <section className="space-y-2">
        {results.map((result) => (
          <Surface key={`${result.kind}-${result.document_id}`} className="space-y-2">
            <div className="flex items-center gap-2"><FileSearch size={15} className="text-accent" /><Badge>{result.kind}</Badge></div>
            <h2 className="text-sm font-semibold">{result.title}</h2>
            <p className="text-xs text-muted">{result.snippet}</p>
          </Surface>
        ))}
      </section>
    </div>
  );
}
