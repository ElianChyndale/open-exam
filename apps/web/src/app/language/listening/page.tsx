'use client';

import { useState } from 'react';
import { Ear } from 'lucide-react';

import { languageApi } from '@/lib/api';
import { LanguageShell } from '@/components/language/LanguageShell';

export default function LanguageListening() {
  const [form, setForm] = useState({ session_type: 'dictation', language: 'en', score: 0.7, output_gap: false, recognition_gap: false });
  const [message, setMessage] = useState('');
  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    await languageApi.createSession(form);
    setMessage('Session recorded. Recognition and output gaps remain separate.');
  };
  return (
    <LanguageShell title="Train the gap between hearing and producing." eyebrow="Skill transfer">
      <form onSubmit={submit} className="motion-reveal card max-w-2xl space-y-4">
        <div className="flex items-center gap-2"><Ear size={18} className="text-accent" /><h3 className="font-semibold">Record practice session</h3></div>
        <div className="grid gap-3 sm:grid-cols-3">
          <select value={form.session_type} onChange={(event) => setForm({ ...form, session_type: event.target.value })} className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"><option>listening</option><option>dictation</option><option>shadowing</option><option>translation</option><option>writing</option><option>reading_speed</option></select>
          <select value={form.language} onChange={(event) => setForm({ ...form, language: event.target.value })} className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"><option value="en">English</option><option value="es">Spanish</option></select>
          <input type="number" min="0" max="1" step="0.1" value={form.score} onChange={(event) => setForm({ ...form, score: Number(event.target.value) })} aria-label="Session score from zero to one" className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm" />
        </div>
        <label className="flex gap-2 text-sm"><input type="checkbox" checked={form.recognition_gap} onChange={(event) => setForm({ ...form, recognition_gap: event.target.checked })} /> Recognition gap</label>
        <label className="flex gap-2 text-sm"><input type="checkbox" checked={form.output_gap} onChange={(event) => setForm({ ...form, output_gap: event.target.checked })} /> Output gap</label>
        <button className="rounded-lg bg-accent-solid px-4 py-2 text-sm text-white">Record session</button>
        {message ? <p role="status" className="text-sm text-muted">{message}</p> : null}
      </form>
    </LanguageShell>
  );
}
