'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  BookOpenCheck,
  Calculator,
  CheckCircle2,
  FileText,
  Loader2,
  RefreshCw,
  Upload,
} from 'lucide-react';

import { reviewLabApi } from '@/lib/api';

type CoverageRecord = {
  topic_id: string;
  confirmed_asset_count: number;
  draft_asset_count: number;
  rejected_asset_count: number;
  formula_asset_count: number;
  decision_rule_asset_count: number;
  mistake_link_count: number;
  mastery_state: string;
  coverage_status: 'covered' | 'partial' | 'draft_only' | 'missing' | 'weak' | 'stale' | string;
  coverage_score: number;
  missing_asset_types: string[];
  recommended_actions: string[];
  next_review_at?: string | null;
  topic: {
    topic_id: string;
    subject: string;
    module: string;
    los?: string | null;
    title: string;
    description?: string | null;
    exam_weight: number;
    importance: number;
    expected_asset_types: string[];
    formula_expected: boolean;
    decision_rule_expected: boolean;
    source_refs: string[];
  };
  links: Array<{ asset_id: string; match_reason: string; confidence: number; created_by: string }>;
  linked_assets: Array<{
    asset_id: string;
    asset_type: string;
    title: string;
    validation_status: string;
    formula_latex?: string;
    source_refs?: string[];
  }>;
};

type CoveragePayload = {
  topic_count: number;
  asset_count: number;
  link_count: number;
  summary: Record<string, number>;
  records: CoverageRecord[];
  coverage_scoring_formula: string;
};

const sampleSyllabus = [
  'CI-001 | Corporate Issuers | Cost of Capital | Calculate and interpret WACC | definition, formula, decision_rule | 0.9',
  'EQ-001 | Equity | Equity Valuation | Apply the Gordon growth model | formula, decision_rule | 0.8',
  'FI-001 | Fixed Income | Duration and Convexity | Choose effective duration for option-sensitive bonds | definition, formula, decision_rule | 0.78',
].join('\n');

const statusOrder = ['missing', 'draft_only', 'partial', 'weak', 'stale', 'covered'];

export default function ReviewCoveragePage() {
  const [coverage, setCoverage] = useState<CoveragePayload | null>(null);
  const [selectedTopicId, setSelectedTopicId] = useState('');
  const [syllabusText, setSyllabusText] = useState(sampleSyllabus);
  const [statusFilter, setStatusFilter] = useState('all');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const loadCoverage = async (recompute = false) => {
    setBusy(true);
    setError('');
    try {
      const result = recompute
        ? await reviewLabApi.recomputeSyllabusCoverage()
        : await reviewLabApi.getSyllabusCoverage();
      setCoverage(result);
      setSelectedTopicId((current) => current || result.records?.[0]?.topic_id || '');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Coverage load failed');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    loadCoverage().catch(() => undefined);
  }, []);

  const records = coverage?.records || [];
  const filteredRecords = useMemo(() => {
    return records.filter((record) => statusFilter === 'all' || record.coverage_status === statusFilter);
  }, [records, statusFilter]);
  const selected = records.find((record) => record.topic_id === selectedTopicId) || filteredRecords[0] || records[0];

  const seedDemo = async () => {
    setBusy(true);
    setError('');
    try {
      await reviewLabApi.seedDemoSyllabus();
      await loadCoverage(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Demo seed failed');
    } finally {
      setBusy(false);
    }
  };

  const importText = async () => {
    if (!syllabusText.trim()) return;
    setBusy(true);
    setError('');
    try {
      await reviewLabApi.importSyllabusText({ text: syllabusText });
      await loadCoverage(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Syllabus import failed');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-2">
          <BookOpenCheck size={21} className="text-accent" />
          <h2 className="text-xl font-bold">Coverage Audit</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/review/assets" className="btn-secondary inline-flex items-center gap-2">
            <FileText size={15} />
            Review Assets
          </Link>
          <Link href="/review/formulas" className="btn-secondary inline-flex items-center gap-2">
            <Calculator size={15} />
            Formula Lab
          </Link>
          <button
            type="button"
            onClick={() => loadCoverage(true)}
            disabled={busy}
            className="btn-primary inline-flex items-center gap-2"
          >
            {busy ? <Loader2 size={15} className="animate-spin" /> : <RefreshCw size={15} />}
            Recompute coverage
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
        {statusOrder.map((status) => (
          <button
            key={status}
            type="button"
            onClick={() => setStatusFilter(statusFilter === status ? 'all' : status)}
            className={`rounded-lg border p-3 text-left transition-colors ${
              statusFilter === status ? 'border-accent bg-accent-soft' : 'border-line bg-surface-raised'
            }`}
          >
            <p className="text-xs font-semibold uppercase text-muted">{status}</p>
            <p className="mt-1 text-2xl font-bold">{coverage?.summary?.[status] || 0}</p>
          </button>
        ))}
      </div>

      <div className="grid gap-4 xl:grid-cols-[minmax(260px,0.65fr)_minmax(0,1.35fr)]">
        <section className="space-y-4">
          <div className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex items-center justify-between gap-3">
              <h3 className="font-semibold">Syllabus Import</h3>
              <button type="button" onClick={seedDemo} disabled={busy} className="btn-secondary inline-flex items-center gap-2">
                <CheckCircle2 size={15} />
                Seed demo syllabus
              </button>
            </div>
            <label htmlFor="coverage-syllabus-text" className="mt-4 block text-xs font-semibold uppercase text-muted">
              Pasted syllabus
            </label>
            <textarea
              id="coverage-syllabus-text"
              value={syllabusText}
              onChange={(event) => setSyllabusText(event.target.value)}
              rows={9}
              className="input mt-2 w-full resize-none text-sm leading-6"
            />
            <button
              type="button"
              onClick={importText}
              disabled={busy || !syllabusText.trim()}
              className="btn-primary mt-4 inline-flex items-center gap-2"
            >
              {busy ? <Loader2 size={15} className="animate-spin" /> : <Upload size={15} />}
              Import syllabus
            </button>
          </div>

          <div className="rounded-lg border border-line bg-surface-raised p-4 text-sm">
            <div className="grid grid-cols-3 gap-3">
              <Metric label="Topics" value={coverage?.topic_count || 0} />
              <Metric label="Assets" value={coverage?.asset_count || 0} />
              <Metric label="Links" value={coverage?.link_count || 0} />
            </div>
            <p className="mt-4 text-xs leading-5 text-muted">{coverage?.coverage_scoring_formula}</p>
          </div>
        </section>

        <section className="grid gap-4 2xl:grid-cols-[minmax(0,1.15fr)_minmax(320px,0.85fr)]">
          <div className="overflow-hidden rounded-lg border border-line bg-surface-raised">
            <div className="flex items-center justify-between border-b border-line px-4 py-3">
              <h3 className="font-semibold">Topics</h3>
              <span className="text-xs text-muted">{filteredRecords.length} shown</span>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-line text-sm">
                <thead className="bg-surface-field text-left text-xs uppercase text-muted">
                  <tr>
                    <th className="px-3 py-2 font-semibold">Subject / Module / LOS</th>
                    <th className="px-3 py-2 font-semibold">Weight</th>
                    <th className="px-3 py-2 font-semibold">Status</th>
                    <th className="px-3 py-2 font-semibold">Score</th>
                    <th className="px-3 py-2 font-semibold">Counts</th>
                    <th className="px-3 py-2 font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-line">
                  {filteredRecords.map((record) => (
                    <tr key={record.topic_id} className={selected?.topic_id === record.topic_id ? 'bg-accent-soft' : ''}>
                      <td className="px-3 py-3 align-top">
                        <button
                          type="button"
                          onClick={() => setSelectedTopicId(record.topic_id)}
                          className="text-left"
                        >
                          <span className="block font-semibold">{record.topic.title}</span>
                          <span className="mt-1 block text-xs text-muted">
                            {record.topic.subject} / {record.topic.module} / {record.topic.los || 'no LOS'}
                          </span>
                        </button>
                      </td>
                      <td className="px-3 py-3 align-top">{Math.round(record.topic.exam_weight * 100)}%</td>
                      <td className="px-3 py-3 align-top"><StatusBadge status={record.coverage_status} /></td>
                      <td className="px-3 py-3 align-top">{Math.round(record.coverage_score * 100)}%</td>
                      <td className="px-3 py-3 align-top text-xs text-muted">
                        C {record.confirmed_asset_count} / D {record.draft_asset_count} / F {record.formula_asset_count} / R {record.decision_rule_asset_count}
                      </td>
                      <td className="px-3 py-3 align-top text-xs">
                        {record.recommended_actions.slice(0, 2).join(', ')}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <TopicDetail record={selected} />
        </section>
      </div>
    </div>
  );
}

function TopicDetail({ record }: { record?: CoverageRecord }) {
  if (!record) {
    return (
      <aside className="rounded-lg border border-line bg-surface-raised p-5 text-sm text-muted">
        No coverage record selected.
      </aside>
    );
  }

  return (
    <aside className="rounded-lg border border-line bg-surface-raised p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase text-muted">{record.topic.subject}</p>
          <h3 className="mt-1 text-lg font-bold">{record.topic.title}</h3>
        </div>
        <StatusBadge status={record.coverage_status} />
      </div>
      <p className="mt-2 text-sm text-muted">{record.topic.module} / {record.topic.los || 'no LOS'}</p>
      {record.topic.description && <p className="mt-3 text-sm leading-6">{record.topic.description}</p>}

      <DetailList title="Recommended Actions" items={record.recommended_actions} />
      <DetailList title="Missing Asset Types" items={record.missing_asset_types} empty="Expected types are covered." />
      <DetailList title="Source Refs" items={record.topic.source_refs} empty="No syllabus source refs." />

      <div className="mt-4">
        <p className="text-xs font-semibold uppercase text-muted">Linked Assets</p>
        <div className="mt-2 space-y-2">
          {record.linked_assets.length === 0 ? (
            <p className="text-sm text-muted">No linked assets yet.</p>
          ) : (
            record.linked_assets.map((asset) => (
              <div key={asset.asset_id} className="rounded-lg border border-line bg-surface-field p-3 text-sm">
                <div className="flex items-center justify-between gap-2">
                  <p className="font-semibold">{asset.title || asset.asset_id}</p>
                  <span className="rounded border border-line px-2 py-0.5 text-xs text-muted">{asset.validation_status}</span>
                </div>
                <p className="mt-1 text-xs uppercase text-muted">{asset.asset_type}</p>
                {asset.formula_latex && <p className="mt-2 font-mono text-xs">{asset.formula_latex}</p>}
              </div>
            ))
          )}
        </div>
      </div>

      <div className="mt-4 space-y-2">
        {record.links.map((link) => (
          <p key={`${link.asset_id}-${link.created_by}`} className="text-xs text-muted">
            {link.created_by} / {Math.round(link.confidence * 100)}% / {link.match_reason}
          </p>
        ))}
      </div>

      <div className="mt-5 flex flex-wrap gap-2">
        <Link href="/review/assets" className="btn-secondary inline-flex items-center gap-2">
          Import notes
          <ArrowRight size={14} />
        </Link>
        <Link href="/review/formulas" className="btn-secondary inline-flex items-center gap-2">
          Formula gaps
          <ArrowRight size={14} />
        </Link>
      </div>
    </aside>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase text-muted">{label}</p>
      <p className="mt-1 text-xl font-bold">{value}</p>
    </div>
  );
}

function DetailList({ title, items, empty }: { title: string; items: string[]; empty?: string }) {
  return (
    <div className="mt-4">
      <p className="text-xs font-semibold uppercase text-muted">{title}</p>
      {items.length ? (
        <ul className="mt-2 space-y-1 text-sm">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="mt-2 text-sm text-muted">{empty || 'None'}</p>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const className =
    status === 'covered'
      ? 'border-success-soft bg-success-soft text-success'
      : status === 'missing'
        ? 'border-danger-soft bg-danger-soft text-danger'
        : status === 'weak' || status === 'stale'
          ? 'border-warning-soft bg-warning-soft text-warning'
          : 'border-accent-soft bg-accent-soft text-accent';
  return (
    <span className={`inline-flex rounded border px-2 py-0.5 text-xs font-semibold ${className}`}>
      {status}
    </span>
  );
}
