'use client';

import { useState } from 'react';
import { Upload, FileText } from 'lucide-react';

import { dictionaryApi } from '@/lib/api';
import { LanguageShell } from '@/components/language/LanguageShell';

const FORMATS = ['auto', 'csv', 'tsv', 'json', 'tei', 'wordnet', 'freedict', 'stardict'];

export default function DictionaryImport() {
  const [form, setForm] = useState({
    title: '',
    language_pair: 'en-zh',
    content: '',
    filename: '',
    license_mode: 'unknown',
    priority: 0,
    format: 'auto',
  });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      const result = await dictionaryApi.importDictionary({
        ...form,
        priority: Number(form.priority),
      });
      if (result.duplicate) {
        setMessage(`Duplicate detected: already imported as ${result.source.title}`);
      } else {
        setMessage(`Imported ${result.count} entries from ${result.source.title}`);
      }
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Import failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <LanguageShell title="Import a dictionary into the lexical index." eyebrow="Dictionary import">
      <form onSubmit={submit} className="motion-reveal card space-y-4">
        <div className="flex items-center gap-2">
          <FileText size={18} className="text-accent" />
          <h3 className="font-semibold">Dictionary upload</h3>
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          <input
            required
            placeholder="Dictionary title"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
          />
          <input
            required
            placeholder="Language pair (e.g. en-zh, es-en)"
            value={form.language_pair}
            onChange={(e) => setForm({ ...form, language_pair: e.target.value })}
            className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
          />
          <input
            placeholder="Original filename (optional)"
            value={form.filename}
            onChange={(e) => setForm({ ...form, filename: e.target.value })}
            className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
          />
          <select
            value={form.license_mode}
            onChange={(e) => setForm({ ...form, license_mode: e.target.value })}
            className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
          >
            <option value="unknown">Unknown license</option>
            <option value="cc-by-sa">CC BY-SA</option>
            <option value="cc-by">CC BY</option>
            <option value="gpl">GPL</option>
            <option value="public_domain">Public domain</option>
            <option value="proprietary">Proprietary</option>
          </select>
          <select
            value={form.format}
            onChange={(e) => setForm({ ...form, format: e.target.value })}
            className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
          >
            {FORMATS.map((f) => (
              <option key={f} value={f}>
                {f === 'auto' ? 'Auto-detect format' : f.toUpperCase()}
              </option>
            ))}
          </select>
          <input
            type="number"
            min={0}
            max={10}
            placeholder="Priority (0-10)"
            value={form.priority}
            onChange={(e) => setForm({ ...form, priority: Number(e.target.value) })}
            className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
          />
        </div>
        <textarea
          required
          value={form.content}
          onChange={(e) => setForm({ ...form, content: e.target.value })}
          placeholder="Paste dictionary content here (CSV, TSV, JSON, TEI XML, WordNet, etc.)"
          className="min-h-56 w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
        />
        <button
          disabled={loading}
          className="flex items-center gap-2 rounded-lg bg-accent-solid px-4 py-2 text-sm text-white disabled:opacity-50"
        >
          <Upload size={15} />
          {loading ? 'Importing...' : 'Import dictionary'}
        </button>
        {message ? <p role="status" className="text-sm text-muted">{message}</p> : null}
      </form>
    </LanguageShell>
  );
}
