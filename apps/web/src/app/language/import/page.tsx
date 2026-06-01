'use client';

import { useState } from 'react';
import { FileInput } from 'lucide-react';

import { languageApi } from '@/lib/api';
import { LanguageShell } from '@/components/language/LanguageShell';

export default function LanguageImport() {
  const [form, setForm] = useState({ title: '', language: 'en', source_type: 'manual', import_format: 'text', content: '', url: '' });
  const [message, setMessage] = useState('');

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const result = await languageApi.createSource(form);
      setMessage(result.duplicate ? `Already captured: ${result.source.title}` : `Captured ${result.segments.length} context segment(s).`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Import failed.');
    }
  };

  return (
    <LanguageShell title="Bring real language into the lab." eyebrow="Context capture">
      <form onSubmit={submit} className="motion-reveal card space-y-4">
        <div className="flex items-center gap-2"><FileInput size={18} className="text-accent" /><h3 className="font-semibold">Local-first import</h3></div>
        <div className="grid gap-3 sm:grid-cols-2">
          <input required placeholder="Source title" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm" />
          <select value={form.language} onChange={(event) => setForm({ ...form, language: event.target.value })} className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"><option value="en">English</option><option value="es">Spanish</option></select>
          <select value={form.source_type} onChange={(event) => setForm({ ...form, source_type: event.target.value, import_format: event.target.value === 'subtitle' ? 'srt' : event.target.value })} className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"><option value="manual">Manual text</option><option value="subtitle">SRT / VTT subtitle</option><option value="pdf">PDF extracted text</option><option value="epub">EPUB extracted text</option><option value="audio">Audio manifest</option><option value="web">Web metadata</option></select>
          <input placeholder="Optional URL" value={form.url} onChange={(event) => setForm({ ...form, url: event.target.value })} className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm" />
        </div>
        <textarea required value={form.content} onChange={(event) => setForm({ ...form, content: event.target.value })} placeholder="Paste text, subtitle content, extracted document text, or local audio placeholder." className="min-h-44 w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm" />
        <button className="rounded-lg bg-accent-solid px-4 py-2 text-sm text-white">Capture source</button>
        {message ? <p role="status" className="text-sm text-muted">{message}</p> : null}
      </form>
    </LanguageShell>
  );
}
