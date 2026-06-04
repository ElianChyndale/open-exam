'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { AlertTriangle, Check, FileText, Loader2, RefreshCw, ShieldCheck, Upload, X } from 'lucide-react';

import { languageOsApi } from '@/lib/api';
import { LanguageShell } from '@/components/language/LanguageShell';

type DictionarySource = {
  dictionary_id: string;
  title: string;
  dictionary_type: string;
  source_language: string;
  target_language?: string | null;
  quality_score: number;
  quality_status: string;
  validation_status: string;
  source_refs: string[];
  quality_dimensions?: Record<string, number>;
};

type LexicalAsset = {
  lexical_id: string;
  dictionary_id?: string | null;
  headword: string;
  language: string;
  target_language?: string | null;
  part_of_speech?: string | null;
  definition: string;
  translation?: string | null;
  example_sentence?: string | null;
  example_translation?: string | null;
  collocations: string[];
  synonyms: string[];
  usage_notes: string[];
  source_refs: string[];
  quality_score: number;
  validation_status: string;
  mastery_state: string;
};

const sampleSpanishJson = JSON.stringify(
  [
    {
      headword: 'aprovechar',
      language: 'es',
      target_language: 'en',
      part_of_speech: 'verb',
      definition: 'to take advantage of; to make use of',
      translation: 'take advantage of, make use of',
      example_sentence: 'Debemos aprovechar esta oportunidad.',
      example_translation: 'We should take advantage of this opportunity.',
      collocations: ['aprovechar una oportunidad', 'aprovechar el tiempo'],
      usage_notes: ['Often used with opportunities, time, or resources.'],
    },
  ],
  null,
  2,
);

const dictionaryTypes = ['english_english', 'spanish_english', 'english_spanish', 'custom_bilingual', 'custom_monolingual'];
const importModes = ['json', 'csv', 'text'] as const;

export default function LanguageDictionariesPage() {
  const [title, setTitle] = useState('Spanish-English Core');
  const [dictionaryType, setDictionaryType] = useState('spanish_english');
  const [mode, setMode] = useState<(typeof importModes)[number]>('json');
  const [content, setContent] = useState(sampleSpanishJson);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileRecord, setFileRecord] = useState<any>(null);
  const [fileWarnings, setFileWarnings] = useState<string[]>([]);
  const [dictionaries, setDictionaries] = useState<DictionarySource[]>([]);
  const [selectedDictionaryId, setSelectedDictionaryId] = useState('');
  const [assets, setAssets] = useState<LexicalAsset[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const selected = dictionaries.find((item) => item.dictionary_id === selectedDictionaryId) || dictionaries[0];
  const counts = useMemo(() => assets.reduce<Record<string, number>>((acc, asset) => {
    acc[asset.validation_status] = (acc[asset.validation_status] || 0) + 1;
    return acc;
  }, {}), [assets]);

  const loadDictionary = async (dictionaryId: string) => {
    if (!dictionaryId) return;
    const detail = await languageOsApi.getDictionary(dictionaryId);
    setSelectedDictionaryId(dictionaryId);
    setAssets(detail.lexical_assets || []);
  };

  const load = async (dictionaryId = selectedDictionaryId) => {
    const listed = await languageOsApi.listDictionaries();
    setDictionaries(listed.dictionaries || []);
    const nextId = dictionaryId || listed.dictionaries?.[0]?.dictionary_id || '';
    if (nextId) {
      await loadDictionary(nextId);
    } else {
      setAssets([]);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const importDictionary = async () => {
    setBusy(true);
    setError('');
    try {
      const payload =
        mode === 'json'
          ? await languageOsApi.importDictionaryJson({ title, dictionary_type: dictionaryType, entries: JSON.parse(content) })
          : mode === 'csv'
            ? await languageOsApi.importDictionaryCsv({ title, dictionary_type: dictionaryType, csv_text: content })
            : await languageOsApi.importDictionaryText({ title, dictionary_type: dictionaryType, text: content });
      setSelectedDictionaryId(payload.dictionary.dictionary_id);
      await load(payload.dictionary.dictionary_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Dictionary import failed');
    } finally {
      setBusy(false);
    }
  };

  const importDictionaryFile = async () => {
    if (!selectedFile) return;
    setBusy(true);
    setError('');
    try {
      const imported = await languageOsApi.importDictionaryFile({
        file: selectedFile,
        title: title.trim() || selectedFile.name,
        dictionary_type: dictionaryType,
      });
      setFileRecord(imported.file);
      setFileWarnings(imported.warnings || []);
      if (imported.dictionary?.dictionary_id) {
        setSelectedDictionaryId(imported.dictionary.dictionary_id);
        setAssets(imported.lexical_assets || []);
        await load(imported.dictionary.dictionary_id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Dictionary file import failed');
    } finally {
      setBusy(false);
    }
  };

  const run = async (action: () => Promise<unknown>, failure: string) => {
    setBusy(true);
    setError('');
    try {
      await action();
      await load(selectedDictionaryId);
    } catch (err) {
      setError(err instanceof Error ? err.message : failure);
    } finally {
      setBusy(false);
    }
  };

  const updateAsset = (lexicalId: string, action: 'confirm' | 'reject') =>
    run(
      () => action === 'confirm' ? languageOsApi.confirmLexicalAsset(lexicalId) : languageOsApi.rejectLexicalAsset(lexicalId),
      'Lexical asset update failed',
    );

  return (
    <LanguageShell title="Dictionary Kernel" eyebrow="Lexical source of truth">
      <div className="rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
        Draft lexical assets are not used in review until confirmed.
      </div>

      {error && (
        <div className="flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="grid gap-4 xl:grid-cols-[minmax(280px,0.72fr)_minmax(0,1.28fr)]">
        <section className="space-y-4">
          <div className="card space-y-4">
            <div className="flex items-center gap-2">
              <Upload size={18} className="text-accent" />
              <h3 className="font-semibold">Import dictionary</h3>
            </div>
            <label htmlFor="dictionary-title" className="block text-xs font-semibold uppercase text-muted">
              Dictionary title
            </label>
            <input id="dictionary-title" value={title} onChange={(event) => setTitle(event.target.value)} className="input w-full" />

            <div className="grid gap-3 sm:grid-cols-2">
              <div>
                <label htmlFor="dictionary-type" className="block text-xs font-semibold uppercase text-muted">
                  Dictionary type
                </label>
                <select id="dictionary-type" value={dictionaryType} onChange={(event) => setDictionaryType(event.target.value)} className="input mt-2 w-full">
                  {dictionaryTypes.map((type) => <option key={type} value={type}>{type}</option>)}
                </select>
              </div>
              <div>
                <label htmlFor="dictionary-format" className="block text-xs font-semibold uppercase text-muted">
                  Import format
                </label>
                <select id="dictionary-format" value={mode} onChange={(event) => setMode(event.target.value as typeof mode)} className="input mt-2 w-full">
                  {importModes.map((item) => <option key={item} value={item}>{item}</option>)}
                </select>
              </div>
            </div>

            <label htmlFor="dictionary-content" className="block text-xs font-semibold uppercase text-muted">
              Dictionary content
            </label>
            <textarea
              id="dictionary-content"
              value={content}
              onChange={(event) => setContent(event.target.value)}
              rows={13}
              className="input w-full resize-none font-mono text-xs leading-5"
            />

            <button type="button" onClick={importDictionary} disabled={busy || !title.trim() || !content.trim()} className="btn-primary inline-flex items-center gap-2">
              {busy ? <Loader2 size={15} className="animate-spin" /> : <Upload size={15} />}
              Import dictionary
            </button>

            <div className="border-t border-line pt-4">
              <label htmlFor="dictionary-file" className="block text-xs font-semibold uppercase text-muted">
                Dictionary file
              </label>
              <input
                id="dictionary-file"
                type="file"
                accept=".json,.csv,.txt,.md,.markdown"
                onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
                className="input mt-2 w-full text-sm"
              />
              <p className="mt-2 text-xs text-muted">Supported: JSON, CSV, TXT, MD</p>
              <button type="button" onClick={importDictionaryFile} disabled={busy || !selectedFile} className="btn-secondary mt-3 inline-flex items-center gap-2">
                {busy ? <Loader2 size={15} className="animate-spin" /> : <FileText size={15} />}
                Import file
              </button>
              {fileRecord && (
                <div className="mt-3 rounded-lg border border-line bg-surface-field p-3 text-xs">
                  <div className="flex flex-wrap items-center gap-2">
                    <StatusBadge status={fileRecord.extraction_status} />
                    {fileRecord.duplicate_of && <StatusBadge status="duplicate" />}
                    <span className="text-muted">{fileRecord.filename}</span>
                  </div>
                  {fileWarnings.length > 0 && (
                    <ul className="mt-2 space-y-1 text-warning">
                      {fileWarnings.map((warning) => <li key={warning}>{warning}</li>)}
                    </ul>
                  )}
                </div>
              )}
            </div>
          </div>

          <div className="card">
            <div className="mb-3 flex items-center justify-between">
              <h3 className="font-semibold">Dictionaries</h3>
              <button type="button" onClick={() => load()} className="btn-secondary inline-flex items-center gap-2">
                <RefreshCw size={14} />
                Refresh
              </button>
            </div>
            <div className="space-y-2">
              {dictionaries.length === 0 ? (
                <p className="text-sm text-muted">No dictionaries imported.</p>
              ) : dictionaries.map((dictionary) => (
                <button
                  key={dictionary.dictionary_id}
                  type="button"
                  onClick={() => loadDictionary(dictionary.dictionary_id)}
                  className={`w-full rounded-lg border p-3 text-left text-sm ${
                    selected?.dictionary_id === dictionary.dictionary_id ? 'border-accent bg-accent-soft' : 'border-line bg-surface-field'
                  }`}
                >
                  <span className="block font-semibold">{dictionary.title}</span>
                  <span className="mt-1 block text-xs text-muted">
                    {Math.round((dictionary.quality_score || 0) * 100)}% / {dictionary.quality_status} / {dictionary.validation_status}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <div className="card">
            <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
              <div>
                <p className="text-xs font-semibold uppercase text-muted">Selected dictionary</p>
                <h3 className="mt-1 text-lg font-bold">{selected?.title || 'No dictionary selected'}</h3>
                {selected && (
                  <p className="mt-1 text-sm text-muted">
                    {selected.dictionary_type} / {selected.source_language || 'any'} {selected.target_language ? `to ${selected.target_language}` : ''}
                  </p>
                )}
              </div>
              {selected && (
                <div className="flex flex-wrap gap-2">
                  <StatusBadge status={selected.quality_status} />
                  <StatusBadge status={selected.validation_status} />
                </div>
              )}
            </div>

            {selected && (
              <>
                <div className="mt-4 grid gap-3 sm:grid-cols-3">
                  <Metric label="Quality" value={`${Math.round((selected.quality_score || 0) * 100)}%`} />
                  <Metric label="Assets" value={String(assets.length)} />
                  <Metric label="Confirmed" value={String(counts.confirmed || 0)} />
                </div>

                <div className="mt-4 flex flex-wrap gap-2">
                  <button type="button" onClick={() => run(() => languageOsApi.scoreDictionary(selected.dictionary_id), 'Scoring failed')} className="btn-secondary inline-flex items-center gap-2">
                    <ShieldCheck size={14} />
                    Score dictionary
                  </button>
                  <button type="button" onClick={() => run(() => languageOsApi.confirmDictionary(selected.dictionary_id), 'Confirm failed')} disabled={selected.validation_status === 'confirmed'} className="btn-secondary inline-flex items-center gap-2">
                    <Check size={14} />
                    Confirm dictionary
                  </button>
                  <button type="button" onClick={() => run(() => languageOsApi.rejectDictionary(selected.dictionary_id), 'Reject failed')} disabled={selected.validation_status === 'rejected'} className="btn-secondary inline-flex items-center gap-2">
                    <X size={14} />
                    Reject dictionary
                  </button>
                  <Link href="/language/review" className="btn-primary inline-flex items-center gap-2">
                    <FileText size={14} />
                    Lexical review
                  </Link>
                </div>

                {selected.quality_dimensions && (
                  <div className="mt-4 grid gap-2 sm:grid-cols-2 xl:grid-cols-3">
                    {Object.entries(selected.quality_dimensions).map(([key, value]) => (
                      <Metric key={key} label={key} value={`${Math.round(value * 100)}%`} />
                    ))}
                  </div>
                )}
              </>
            )}
          </div>

          <section className="card">
            <div className="mb-3 flex items-center gap-2">
              <FileText size={18} className="text-accent" />
              <h3 className="font-semibold">Lexical assets</h3>
            </div>
            <div className="space-y-3">
              {assets.length === 0 ? (
                <p className="text-sm text-muted">No lexical assets parsed.</p>
              ) : assets.map((asset) => (
                <article key={asset.lexical_id} className="rounded-lg border border-line bg-surface-field p-4">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <h4 className="font-semibold">{asset.headword}</h4>
                        <StatusBadge status={asset.validation_status} />
                      </div>
                      <p className="mt-1 text-xs uppercase text-muted">
                        {asset.language}{asset.target_language ? ` to ${asset.target_language}` : ''} / {asset.part_of_speech || 'any POS'} / {Math.round(asset.quality_score * 100)}%
                      </p>
                    </div>
                    <div className="flex gap-2">
                      <button type="button" onClick={() => updateAsset(asset.lexical_id, 'confirm')} disabled={asset.validation_status === 'confirmed'} className="btn-secondary inline-flex items-center gap-1.5">
                        <Check size={14} />
                        Confirm
                      </button>
                      <button type="button" onClick={() => updateAsset(asset.lexical_id, 'reject')} disabled={asset.validation_status === 'rejected'} className="btn-secondary inline-flex items-center gap-1.5">
                        <X size={14} />
                        Reject
                      </button>
                    </div>
                  </div>
                  <p className="mt-3 text-sm leading-6">{asset.definition}</p>
                  {asset.translation && <p className="mt-2 text-sm text-accent">{asset.translation}</p>}
                  {asset.example_sentence && <p className="mt-2 text-sm italic">{asset.example_sentence}</p>}
                  <TagList title="Collocations" items={asset.collocations} />
                  <TagList title="Usage notes" items={asset.usage_notes} />
                  <TagList title="Source refs" items={asset.source_refs} />
                </article>
              ))}
            </div>
          </section>
        </section>
      </div>
    </LanguageShell>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-surface-field p-3">
      <p className="text-xs font-semibold uppercase text-muted">{label}</p>
      <p className="mt-1 text-xl font-bold">{value}</p>
    </div>
  );
}

function TagList({ title, items }: { title: string; items: string[] }) {
  if (!items.length) return null;
  return (
    <div className="mt-3">
      <p className="text-xs font-semibold uppercase text-muted">{title}</p>
      <div className="mt-2 flex flex-wrap gap-2">
        {items.map((item) => (
          <span key={item} className="rounded border border-line bg-surface-raised px-2 py-0.5 text-xs text-muted">{item}</span>
        ))}
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const className =
    status === 'confirmed' || status === 'high' || status === 'trusted'
      ? 'border-success-soft bg-success-soft text-success'
      : status === 'rejected' || status === 'low'
        ? 'border-danger-soft bg-danger-soft text-danger'
        : 'border-warning-soft bg-warning-soft text-warning';
  return <span className={`rounded border px-2 py-0.5 text-xs font-semibold ${className}`}>{status}</span>;
}
