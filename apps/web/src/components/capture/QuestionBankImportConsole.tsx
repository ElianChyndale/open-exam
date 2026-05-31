'use client';

import { useEffect, useState } from 'react';
import { questionBanksApi } from '@/lib/api';

export default function QuestionBankImportConsole() {
  const [sourceFile, setSourceFile] = useState('private-bank.pdf');
  const [records, setRecords] = useState('[]');
  const [quarantine, setQuarantine] = useState<any[]>([]);
  const [edits, setEdits] = useState<Record<string, string>>({});
  const [message, setMessage] = useState('');

  const refresh = () => questionBanksApi.listQuarantine().then((data: any) => {
    setQuarantine(data.questions || []);
    setEdits((current) => {
      const next = { ...current };
      for (const question of data.questions || []) {
        next[question.question_id] ||= JSON.stringify(question, null, 2);
      }
      return next;
    });
  });

  useEffect(() => { refresh(); }, []);

  const importRecords = async () => {
    try {
      const questions = JSON.parse(records);
      const result: any = await questionBanksApi.importStructured({ source_file: sourceFile, questions });
      setMessage(`Imported ${result.imported_count}; quarantined ${result.quarantined_count}.`);
      await refresh();
    } catch (error: any) {
      setMessage(`Import failed: ${error.message}`);
    }
  };

  const review = async (questionId: string, action: 'approve' | 'reject') => {
    try {
      const patch = action === 'approve' ? JSON.parse(edits[questionId] || '{}') : {};
      await questionBanksApi.review(questionId, action, patch);
      setMessage(`${action === 'approve' ? 'Approved' : 'Rejected'} ${questionId}.`);
      await refresh();
    } catch (error: any) {
      setMessage(`Review failed: ${error.message}`);
    }
  };

  return (
    <section className="card space-y-4">
      <div>
        <h3 className="text-lg font-semibold">Private import review</h3>
        <p className="mt-1 text-xs text-muted">Paste structured OCR records from a private PDF. Incomplete records stay quarantined and cannot be graded.</p>
      </div>
      <input value={sourceFile} onChange={(event) => setSourceFile(event.target.value)}
        className="w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm" aria-label="Private source filename" />
      <textarea value={records} onChange={(event) => setRecords(event.target.value)}
        className="min-h-28 w-full rounded-lg border border-line bg-surface-field px-3 py-2 font-mono text-xs"
        aria-label="Structured OCR records" />
      <button onClick={importRecords} className="rounded-lg bg-accent-solid px-4 py-2 text-sm text-white hover:bg-accent-strong">
        Import structured records
      </button>
      {message && <p className="text-xs text-success">{message}</p>}
      {quarantine.map((question) => (
        <div key={question.question_id} className="space-y-2 rounded-xl border border-warning-soft bg-warning-soft p-3">
          <p className="text-xs font-semibold">{question.source_file} / page {question.page || '?'}</p>
          <textarea value={edits[question.question_id] || ''} onChange={(event) => setEdits({ ...edits, [question.question_id]: event.target.value })}
            className="min-h-36 w-full rounded-lg border border-line bg-surface-field px-3 py-2 font-mono text-xs" />
          <div className="flex gap-2">
            <button onClick={() => review(question.question_id, 'approve')} className="rounded-lg bg-accent-solid px-3 py-1.5 text-xs text-white">Approve edited record</button>
            <button onClick={() => review(question.question_id, 'reject')} className="rounded-lg border border-danger-soft px-3 py-1.5 text-xs text-danger">Reject</button>
          </div>
        </div>
      ))}
    </section>
  );
}
