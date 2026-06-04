'use client';

import { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import { BookOpen, Filter, Search, Upload } from 'lucide-react';

import { dictionaryApi, DictionaryResult } from '@/lib/api';
import { DictionaryReviewCard, collectCefrLevels, normalizeDictionaryEntry } from '@/components/language/DictionaryReviewCard';
import { LanguageShell } from '@/components/language/LanguageShell';

const POS_OPTIONS = ['', 'noun', 'verb', 'adj', 'adv', 'phrase'];
const CEFR_OPTIONS = ['', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'];

export default function DictionaryBrowser() {
  const [query, setQuery] = useState('');
  const [pos, setPos] = useState('');
  const [cefr, setCefr] = useState('');
  const [results, setResults] = useState<DictionaryResult[]>([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const search = useCallback(async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const data = await dictionaryApi.search(query, { language: '', pos, limit: 50 });
      let filtered = data.results;
      if (cefr) {
        filtered = filtered.filter((r: DictionaryResult) => {
          const entry = normalizeDictionaryEntry(r);
          return collectCefrLevels(entry).includes(cefr);
        });
      }
      setResults(filtered);
      setMessage(`Found ${filtered.length} result(s)`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Search failed');
    } finally {
      setLoading(false);
    }
  }, [query, pos, cefr]);

  useEffect(() => {
    const t = setTimeout(() => {
      if (query.trim()) void search();
    }, 300);
    return () => clearTimeout(t);
  }, [query, pos, cefr, search]);

  return (
    <LanguageShell title="Dictionary — the lexical source of truth." eyebrow="DictionaryOS">
      <div className="motion-reveal card space-y-4">
        <div className="flex items-center gap-2">
          <BookOpen size={18} className="text-accent" />
          <h3 className="font-semibold">Search dictionary</h3>
          <Link
            href="/language/dictionary/import"
            className="ml-auto flex items-center gap-1 rounded-lg border border-line px-3 py-1.5 text-xs text-muted hover:text-ink"
          >
            <Upload size={13} /> Import
          </Link>
        </div>
        <div className="flex flex-col gap-3 sm:flex-row">
          <div className="relative flex-1">
            <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Lemma, definition, or translation..."
              className="w-full rounded-lg border border-line bg-surface-field py-2 pl-9 pr-3 text-sm"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter size={14} className="text-muted" />
            <select
              value={pos}
              onChange={(e) => setPos(e.target.value)}
              className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
            >
              <option value="">All POS</option>
              {POS_OPTIONS.filter(Boolean).map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
            <select
              value={cefr}
              onChange={(e) => setCefr(e.target.value)}
              className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
            >
              <option value="">All CEFR</option>
              {CEFR_OPTIONS.filter(Boolean).map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>
        </div>
        {message ? <p role="status" className="text-xs text-muted">{message}</p> : null}
        <div className="space-y-2">
          {loading ? (
            <p className="text-sm text-muted">Searching...</p>
          ) : results.length === 0 && query.trim() ? (
            <p className="text-sm text-muted">No dictionary entries matched this query.</p>
          ) : (
            results.map((r, idx) => (
              <DictionaryReviewCard key={`${r.source_id}-${r.lemma}-${idx}`} item={r} />
            ))
          )}
        </div>
      </div>
    </LanguageShell>
  );
}
