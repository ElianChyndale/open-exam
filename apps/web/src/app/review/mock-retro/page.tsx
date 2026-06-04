'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  BarChart3,
  Brain,
  Calculator,
  CheckCircle2,
  FileText,
  Loader2,
  Play,
  RefreshCw,
  Upload,
} from 'lucide-react';

import { reviewLabApi } from '@/lib/api';

type MockSession = {
  mock_id: string;
  title: string;
  exam?: string | null;
  total_questions: number;
  correct_count: number;
  score?: number | null;
  completed_at?: string | null;
};

type TransferGap = {
  gap_id: string;
  topic_id?: string | null;
  asset_id?: string | null;
  formula_family?: string | null;
  gap_type: string;
  severity: number;
  evidence_count: number;
  last_seen_at: string;
  recommended_actions: string[];
  source_refs: string[];
  status: string;
};

const sampleRetro = [
  'Q1 Corporate Issuers WACC',
  'LOS: CI-001',
  'Result: incorrect',
  'Confidence: high',
  'Time: 240s',
  'Wrong Output: used pretax cost of debt',
  'Correct Rule: WACC uses after-tax cost of debt: w_d * r_d * (1 - t) + w_e * r_e.',
  'Tested Formula: WACC',
  'BA II Plus: store weights and component costs, calculate weighted sum.',
  '',
  'Q2 Fixed Income Duration',
  'Result: incorrect',
  'Confidence: medium',
  'Boundary Rule: Use effective duration when cash flows can change.',
  'Correct Rule: Use effective duration for option-sensitive bonds.',
].join('\n');

const gapTypes = [
  'concept_gap',
  'formula_recall_gap',
  'boundary_confusion',
  'calculator_procedure_gap',
  'confidence_mismatch',
  'time_pressure',
];

export default function MockRetroPage() {
  const router = useRouter();
  const [title, setTitle] = useState('Mock Retro Import');
  const [text, setText] = useState(sampleRetro);
  const [sessions, setSessions] = useState<MockSession[]>([]);
  const [selectedMockId, setSelectedMockId] = useState('');
  const [gaps, setGaps] = useState<TransferGap[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const load = async () => {
    const [sessionPayload, gapPayload] = await Promise.all([
      reviewLabApi.listMockRetroSessions(),
      reviewLabApi.listTransferGaps({ status: 'open' }),
    ]);
    setSessions(sessionPayload.sessions || []);
    setGaps(gapPayload.gaps || []);
    setSelectedMockId((current) => current || sessionPayload.sessions?.[0]?.mock_id || '');
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const summary = useMemo(() => {
    return gaps.reduce<Record<string, number>>((acc, gap) => {
      acc[gap.gap_type] = (acc[gap.gap_type] || 0) + 1;
      return acc;
    }, {});
  }, [gaps]);

  const selectedSession = sessions.find((session) => session.mock_id === selectedMockId) || sessions[0];

  const importRetro = async () => {
    if (!text.trim()) return;
    setBusy(true);
    setError('');
    try {
      const imported = await reviewLabApi.importMockRetroText({ title, text });
      setSelectedMockId(imported.session.mock_id);
      setText('');
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Mock retro import failed');
    } finally {
      setBusy(false);
    }
  };

  const analyzeSelected = async () => {
    if (!selectedMockId) return;
    setBusy(true);
    setError('');
    try {
      await reviewLabApi.analyzeMockRetroSession(selectedMockId);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Mock retro analysis failed');
    } finally {
      setBusy(false);
    }
  };

  const resolveGap = async (gapId: string) => {
    setError('');
    try {
      await reviewLabApi.resolveTransferGap(gapId);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Resolve failed');
    }
  };

  const generateReview = async () => {
    setBusy(true);
    setError('');
    try {
      const session = await reviewLabApi.generateMockRetroReview({ max_units: 8 });
      router.push(`/review/lab?session=${session.session_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Review generation failed');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-2">
          <BarChart3 size={21} className="text-accent" />
          <h2 className="text-xl font-bold">Mock Retro</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/review/coverage" className="btn-secondary inline-flex items-center gap-2">
            <FileText size={15} />
            Coverage
          </Link>
          <Link href="/review/formulas" className="btn-secondary inline-flex items-center gap-2">
            <Calculator size={15} />
            Formula Lab
          </Link>
          <Link href="/review/lab" className="btn-secondary inline-flex items-center gap-2">
            <Brain size={15} />
            Review Lab
          </Link>
          <button type="button" onClick={generateReview} disabled={busy || gaps.length === 0} className="btn-primary inline-flex items-center gap-2">
            {busy ? <Loader2 size={15} className="animate-spin" /> : <Play size={15} />}
            Generate Review Lab
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="mb-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-6">
        {gapTypes.map((gapType) => (
          <div key={gapType} className="rounded-lg border border-line bg-surface-raised p-3">
            <p className="text-xs font-semibold uppercase text-muted">{gapType}</p>
            <p className="mt-1 text-2xl font-bold">{summary[gapType] || 0}</p>
          </div>
        ))}
      </div>

      <div className="grid gap-4 xl:grid-cols-[minmax(280px,0.7fr)_minmax(0,1.3fr)]">
        <section className="space-y-4">
          <div className="rounded-lg border border-line bg-surface-raised p-4">
            <label htmlFor="mock-retro-title" className="block text-xs font-semibold uppercase text-muted">
              Retro title
            </label>
            <input
              id="mock-retro-title"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              className="input mt-2 w-full"
            />
            <label htmlFor="mock-retro-text" className="mt-4 block text-xs font-semibold uppercase text-muted">
              Mock retro text
            </label>
            <textarea
              id="mock-retro-text"
              value={text}
              onChange={(event) => setText(event.target.value)}
              rows={12}
              className="input mt-2 w-full resize-none text-sm leading-6"
            />
            <button
              type="button"
              onClick={importRetro}
              disabled={busy || !title.trim() || !text.trim()}
              className="btn-primary mt-4 inline-flex items-center gap-2"
            >
              {busy ? <Loader2 size={15} className="animate-spin" /> : <Upload size={15} />}
              Import retro
            </button>
          </div>

          <div className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="mb-3 flex items-center justify-between">
              <h3 className="font-semibold">Mock Sessions</h3>
              <button type="button" onClick={() => load()} className="btn-secondary inline-flex items-center gap-2">
                <RefreshCw size={14} />
                Refresh
              </button>
            </div>
            {sessions.length === 0 ? (
              <p className="text-sm text-muted">No mock retro sessions yet.</p>
            ) : (
              <div className="space-y-2">
                {sessions.map((session) => (
                  <button
                    key={session.mock_id}
                    type="button"
                    onClick={() => setSelectedMockId(session.mock_id)}
                    className={`w-full rounded-lg border p-3 text-left text-sm ${
                      selectedSession?.mock_id === session.mock_id ? 'border-accent bg-accent-soft' : 'border-line bg-surface-field'
                    }`}
                  >
                    <span className="block font-semibold">{session.title}</span>
                    <span className="mt-1 block text-xs text-muted">
                      {session.correct_count} / {session.total_questions} correct
                      {typeof session.score === 'number' ? ` · ${Math.round(session.score * 100)}%` : ''}
                    </span>
                  </button>
                ))}
              </div>
            )}
            <button
              type="button"
              onClick={analyzeSelected}
              disabled={busy || !selectedMockId}
              className="btn-primary mt-4 inline-flex items-center gap-2"
            >
              {busy ? <Loader2 size={15} className="animate-spin" /> : <CheckCircle2 size={15} />}
              Analyze session
            </button>
          </div>
        </section>

        <section className="overflow-hidden rounded-lg border border-line bg-surface-raised">
          <div className="flex items-center justify-between border-b border-line px-4 py-3">
            <h3 className="font-semibold">Transfer Gaps</h3>
            <span className="text-xs text-muted">{gaps.length} open</span>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-line text-sm">
              <thead className="bg-surface-field text-left text-xs uppercase text-muted">
                <tr>
                  <th className="px-3 py-2 font-semibold">Topic / Asset</th>
                  <th className="px-3 py-2 font-semibold">Gap</th>
                  <th className="px-3 py-2 font-semibold">Severity</th>
                  <th className="px-3 py-2 font-semibold">Evidence</th>
                  <th className="px-3 py-2 font-semibold">Actions</th>
                  <th className="px-3 py-2 font-semibold">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {gaps.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-3 py-8 text-center text-muted">
                      No open transfer gaps.
                    </td>
                  </tr>
                ) : (
                  gaps.map((gap) => (
                    <tr key={gap.gap_id}>
                      <td className="px-3 py-3 align-top">
                        <span className="block font-semibold">{gap.topic_id || gap.formula_family || 'unmapped topic'}</span>
                        <span className="mt-1 block text-xs text-muted">{gap.asset_id || 'no linked asset'}</span>
                      </td>
                      <td className="px-3 py-3 align-top">{gap.gap_type}</td>
                      <td className="px-3 py-3 align-top">{Math.round(gap.severity * 100)}%</td>
                      <td className="px-3 py-3 align-top">{gap.evidence_count}</td>
                      <td className="px-3 py-3 align-top text-xs">{gap.recommended_actions.join(', ')}</td>
                      <td className="px-3 py-3 align-top">
                        <div className="flex flex-col gap-2">
                          <span className="rounded border border-warning-soft bg-warning-soft px-2 py-0.5 text-xs font-semibold text-warning">
                            {gap.status}
                          </span>
                          <button type="button" onClick={() => resolveGap(gap.gap_id)} className="btn-secondary text-xs">
                            Resolve
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}
