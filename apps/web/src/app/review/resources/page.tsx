'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  BookOpenCheck,
  Brain,
  Calculator,
  Check,
  FileCheck2,
  FileText,
  GitBranch,
  Loader2,
  RefreshCw,
  ShieldCheck,
  Upload,
  X,
} from 'lucide-react';

import { reviewLabApi } from '@/lib/api';

type LearningResource = {
  resource_id: string;
  title: string;
  resource_type: string;
  origin: string;
  source_refs: string[];
  quality_score: number;
  quality_status: string;
  validation_status: string;
  duplicate_of?: string | null;
  warnings?: string[];
  quality_dimensions?: Record<string, number>;
};

type EvidenceSegment = {
  segment_id: string;
  source_ref: string;
  heading?: string | null;
  text: string;
  evidence_type: string;
  confidence: number;
};

type ResourceAsset = {
  asset_id: string;
  asset_type: string;
  title: string;
  correct_rule: string;
  formula_latex?: string;
  source_refs: string[];
  source_quality: number;
  validation_status: string;
  resource_quality_status?: string;
  resource_match_reasons?: string[];
  resource_conflicts?: string[];
};

const sampleResource = [
  '# ResourceOS WACC',
  'LOS: CI-RES-001',
  'WACC = w_d r_d (1 - t) + w_e r_e.',
  'Use when valuing a firm with a target capital structure.',
  'Source: curriculum reading note.',
].join('\n');

const resourceTypes = [
  'text_note',
  'pdf_note',
  'web_article',
  'official_syllabus',
  'textbook',
  'lecture_slide',
  'dictionary',
  'manual',
  'unknown',
];

export default function ReviewResourcesPage() {
  const [title, setTitle] = useState('ResourceOS WACC Note');
  const [resourceType, setResourceType] = useState('text_note');
  const [text, setText] = useState(sampleResource);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileRecord, setFileRecord] = useState<any>(null);
  const [fileWarnings, setFileWarnings] = useState<string[]>([]);
  const [resources, setResources] = useState<LearningResource[]>([]);
  const [selectedResourceId, setSelectedResourceId] = useState('');
  const [evidence, setEvidence] = useState<EvidenceSegment[]>([]);
  const [assets, setAssets] = useState<ResourceAsset[]>([]);
  const [report, setReport] = useState<any>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const selected = resources.find((resource) => resource.resource_id === selectedResourceId) || resources[0];

  const counts = useMemo(() => {
    return resources.reduce<Record<string, number>>((acc, resource) => {
      acc[resource.quality_status] = (acc[resource.quality_status] || 0) + 1;
      return acc;
    }, {});
  }, [resources]);

  const loadResourceDetail = async (resourceId: string) => {
    if (!resourceId) return;
    const detail = await reviewLabApi.getResource(resourceId);
    setSelectedResourceId(resourceId);
    setEvidence(detail.evidence || []);
    setAssets(detail.candidate_assets || []);
  };

  const load = async (resourceId = selectedResourceId) => {
    const [listed, qualityReport] = await Promise.all([
      reviewLabApi.listResources(),
      reviewLabApi.getResourceQualityReport(),
    ]);
    setResources(listed.resources || []);
    setReport(qualityReport);
    const nextId = resourceId || listed.resources?.[0]?.resource_id || '';
    if (nextId) {
      await loadResourceDetail(nextId);
    } else {
      setEvidence([]);
      setAssets([]);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const runAction = async (action: () => Promise<unknown>, failure: string) => {
    setBusy(true);
    setError('');
    try {
      await action();
      await load(selectedResourceId);
    } catch (err) {
      setError(err instanceof Error ? err.message : failure);
    } finally {
      setBusy(false);
    }
  };

  const importResource = async () => {
    if (!title.trim() || !text.trim()) return;
    setBusy(true);
    setError('');
    try {
      const imported = await reviewLabApi.importResourceText({
        title,
        text,
        resource_type: resourceType as any,
      });
      setSelectedResourceId(imported.resource.resource_id);
      await load(imported.resource.resource_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Resource import failed');
    } finally {
      setBusy(false);
    }
  };

  const importResourceFile = async () => {
    if (!selectedFile) return;
    setBusy(true);
    setError('');
    try {
      const imported = await reviewLabApi.importResourceFile({
        file: selectedFile,
        title: title.trim() || selectedFile.name,
        resource_type: resourceType,
      });
      setFileRecord(imported.file);
      setFileWarnings(imported.warnings || []);
      if (imported.resource?.resource_id) {
        setSelectedResourceId(imported.resource.resource_id);
        setEvidence(imported.evidence || []);
        setAssets(imported.candidate_assets || []);
        await load(imported.resource.resource_id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Resource file import failed');
    } finally {
      setBusy(false);
    }
  };

  const scoreSelected = () =>
    selected && runAction(() => reviewLabApi.scoreResource(selected.resource_id), 'Resource scoring failed');

  const extractSelected = () =>
    selected && runAction(() => reviewLabApi.extractResourceEvidence(selected.resource_id), 'Evidence extraction failed');

  const confirmSelected = () =>
    selected && runAction(() => reviewLabApi.confirmResource(selected.resource_id), 'Resource confirmation failed');

  const rejectSelected = () =>
    selected && runAction(() => reviewLabApi.rejectResource(selected.resource_id), 'Resource rejection failed');

  const promoteAssets = () =>
    selected && runAction(
      () => reviewLabApi.promoteResourceAssets(selected.resource_id, assets.map((asset) => asset.asset_id)),
      'Asset promotion failed',
    );

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-2">
          <ShieldCheck size={21} className="text-accent" />
          <h2 className="text-xl font-bold">ResourceOS Quality Gate</h2>
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
          <Link href="/review/coverage" className="btn-secondary inline-flex items-center gap-2">
            <BookOpenCheck size={15} />
            Coverage
          </Link>
          <Link href="/review/mock-retro" className="btn-secondary inline-flex items-center gap-2">
            <GitBranch size={15} />
            Mock Retro
          </Link>
          <Link href="/review/lab" className="btn-secondary inline-flex items-center gap-2">
            <Brain size={15} />
            Review Lab
          </Link>
        </div>
      </div>

      <div className="mb-4 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
        Low, draft, and rejected resources do not enter normal Review Lab.
      </div>

      {error && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="mb-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-6">
        {['unscored', 'low', 'medium', 'high', 'trusted', 'rejected'].map((status) => (
          <div key={status} className="rounded-lg border border-line bg-surface-raised p-3">
            <p className="text-xs font-semibold uppercase text-muted">{status}</p>
            <p className="mt-1 text-2xl font-bold">{counts[status] || 0}</p>
          </div>
        ))}
      </div>

      <div className="grid gap-4 xl:grid-cols-[minmax(280px,0.72fr)_minmax(0,1.28fr)]">
        <section className="space-y-4">
          <div className="rounded-lg border border-line bg-surface-raised p-4">
            <label htmlFor="resource-title" className="block text-xs font-semibold uppercase text-muted">
              Resource title
            </label>
            <input
              id="resource-title"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              className="input mt-2 w-full"
            />

            <label htmlFor="resource-type" className="mt-4 block text-xs font-semibold uppercase text-muted">
              Resource type
            </label>
            <select
              id="resource-type"
              value={resourceType}
              onChange={(event) => setResourceType(event.target.value)}
              className="input mt-2 w-full"
            >
              {resourceTypes.map((type) => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>

            <label htmlFor="resource-text" className="mt-4 block text-xs font-semibold uppercase text-muted">
              Resource text
            </label>
            <textarea
              id="resource-text"
              value={text}
              onChange={(event) => setText(event.target.value)}
              rows={11}
              className="input mt-2 w-full resize-none text-sm leading-6"
            />

            <button
              type="button"
              onClick={importResource}
              disabled={busy || !title.trim() || !text.trim()}
              className="btn-primary mt-4 inline-flex items-center gap-2"
            >
              {busy ? <Loader2 size={15} className="animate-spin" /> : <Upload size={15} />}
              Import resource
            </button>

            <div className="mt-5 border-t border-line pt-4">
              <label htmlFor="resource-file" className="block text-xs font-semibold uppercase text-muted">
                Resource file
              </label>
              <input
                id="resource-file"
                type="file"
                accept=".txt,.md,.markdown,.pdf"
                onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
                className="input mt-2 w-full text-sm"
              />
              <p className="mt-2 text-xs text-muted">Supported: PDF, TXT, MD</p>
              <button
                type="button"
                onClick={importResourceFile}
                disabled={busy || !selectedFile}
                className="btn-secondary mt-3 inline-flex items-center gap-2"
              >
                {busy ? <Loader2 size={15} className="animate-spin" /> : <FileCheck2 size={15} />}
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

          <div className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="mb-3 flex items-center justify-between gap-3">
              <h3 className="font-semibold">Resources</h3>
              <button type="button" onClick={() => load()} className="btn-secondary inline-flex items-center gap-2">
                <RefreshCw size={14} />
                Refresh
              </button>
            </div>
            {resources.length === 0 ? (
              <p className="text-sm text-muted">No resources imported.</p>
            ) : (
              <div className="space-y-2">
                {resources.map((resource) => (
                  <button
                    key={resource.resource_id}
                    type="button"
                    onClick={() => loadResourceDetail(resource.resource_id).catch(() => undefined)}
                    className={`w-full rounded-lg border p-3 text-left text-sm ${
                      selected?.resource_id === resource.resource_id ? 'border-accent bg-accent-soft' : 'border-line bg-surface-field'
                    }`}
                  >
                    <span className="block font-semibold">{resource.title}</span>
                    <span className="mt-1 block text-xs text-muted">
                      {Math.round((resource.quality_score || 0) * 100)}% / {resource.quality_status} / {resource.validation_status}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </section>

        <section className="space-y-4">
          <div className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
              <div>
                <p className="text-xs font-semibold uppercase text-muted">Selected Resource</p>
                <h3 className="mt-1 text-lg font-bold">{selected?.title || 'No resource selected'}</h3>
                {selected && (
                  <p className="mt-1 text-sm text-muted">
                    {selected.resource_type} / {selected.origin} / {selected.resource_id}
                  </p>
                )}
              </div>
              {selected && <StatusPair resource={selected} />}
            </div>

            {selected && (
              <>
                <div className="mt-4 grid gap-3 sm:grid-cols-3">
                  <Metric label="Quality" value={`${Math.round((selected.quality_score || 0) * 100)}%`} />
                  <Metric label="Evidence" value={String(evidence.length)} />
                  <Metric label="Candidates" value={String(assets.length)} />
                </div>

                <div className="mt-4 flex flex-wrap gap-2">
                  <button type="button" onClick={scoreSelected} disabled={busy} className="btn-secondary inline-flex items-center gap-2">
                    <ShieldCheck size={14} />
                    Score resource
                  </button>
                  <button type="button" onClick={extractSelected} disabled={busy} className="btn-secondary inline-flex items-center gap-2">
                    <FileCheck2 size={14} />
                    Extract evidence
                  </button>
                  <button type="button" onClick={confirmSelected} disabled={busy || selected.validation_status === 'confirmed'} className="btn-secondary inline-flex items-center gap-2">
                    <Check size={14} />
                    Confirm resource
                  </button>
                  <button type="button" onClick={rejectSelected} disabled={busy || selected.validation_status === 'rejected'} className="btn-secondary inline-flex items-center gap-2">
                    <X size={14} />
                    Reject resource
                  </button>
                  <button type="button" onClick={promoteAssets} disabled={busy || assets.length === 0} className="btn-primary inline-flex items-center gap-2">
                    {busy ? <Loader2 size={14} className="animate-spin" /> : <Upload size={14} />}
                    Promote assets
                  </button>
                </div>

                {selected.duplicate_of && (
                  <p className="mt-3 text-sm text-warning">Duplicate hash: {selected.duplicate_of}</p>
                )}

                {selected.quality_dimensions && (
                  <div className="mt-4 grid gap-2 sm:grid-cols-2 xl:grid-cols-4">
                    {Object.entries(selected.quality_dimensions).map(([key, value]) => (
                      <div key={key} className="rounded-lg border border-line bg-surface-field p-2">
                        <p className="text-xs font-semibold uppercase text-muted">{key}</p>
                        <p className="mt-1 font-semibold">{Math.round(value * 100)}%</p>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>

          <div className="grid gap-4 2xl:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
            <EvidencePanel evidence={evidence} />
            <CandidatePanel assets={assets} />
          </div>

          {report && (
            <div className="rounded-lg border border-line bg-surface-raised p-4 text-sm">
              <p className="font-semibold">Quality report</p>
              <p className="mt-2 text-muted">
                {report.resource_count} resources / {report.candidate_asset_count} candidates / {report.promoted_asset_count} promoted / {report.conflict_count} conflicts
              </p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

function StatusPair({ resource }: { resource: LearningResource }) {
  return (
    <div className="flex flex-wrap gap-2">
      <StatusBadge status={resource.quality_status} />
      <StatusBadge status={resource.validation_status} />
    </div>
  );
}

function EvidencePanel({ evidence }: { evidence: EvidenceSegment[] }) {
  return (
    <section className="rounded-lg border border-line bg-surface-raised">
      <div className="border-b border-line px-4 py-3">
        <h3 className="font-semibold">Evidence Segments</h3>
      </div>
      <div className="max-h-[520px] overflow-y-auto p-4">
        {evidence.length === 0 ? (
          <p className="text-sm text-muted">No evidence extracted.</p>
        ) : (
          <div className="space-y-3">
            {evidence.map((segment) => (
              <article key={segment.segment_id} className="rounded-lg border border-line bg-surface-field p-3">
                <div className="flex flex-wrap items-center gap-2">
                  <StatusBadge status={segment.evidence_type} />
                  <span className="rounded border border-line px-2 py-0.5 text-xs text-muted">
                    {Math.round(segment.confidence * 100)}%
                  </span>
                  <span className="rounded border border-line px-2 py-0.5 text-xs text-muted">
                    {segment.source_ref}
                  </span>
                </div>
                <p className="mt-3 text-sm leading-6">{segment.text}</p>
              </article>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

function CandidatePanel({ assets }: { assets: ResourceAsset[] }) {
  return (
    <section className="rounded-lg border border-line bg-surface-raised">
      <div className="border-b border-line px-4 py-3">
        <h3 className="font-semibold">Candidate Assets</h3>
      </div>
      <div className="max-h-[520px] overflow-y-auto p-4">
        {assets.length === 0 ? (
          <p className="text-sm text-muted">No candidates yet.</p>
        ) : (
          <div className="space-y-3">
            {assets.map((asset) => (
              <article key={asset.asset_id} className="rounded-lg border border-line bg-surface-field p-3">
                <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h4 className="font-semibold">{asset.title}</h4>
                      <StatusBadge status={asset.validation_status} />
                    </div>
                    <p className="mt-1 text-xs uppercase text-muted">
                      {asset.asset_type} / {Math.round((asset.source_quality || 0) * 100)}% source
                    </p>
                  </div>
                  {asset.resource_quality_status && <StatusBadge status={asset.resource_quality_status} />}
                </div>
                <p className="mt-3 text-sm leading-6">{asset.correct_rule}</p>
                {asset.formula_latex && (
                  <p className="mt-2 rounded-lg bg-surface-raised p-2 font-mono text-xs">{asset.formula_latex}</p>
                )}
                <TagList title="Source refs" items={asset.source_refs} />
                <TagList title="Match reasons" items={asset.resource_match_reasons || []} />
                <TagList title="Conflicts" items={asset.resource_conflicts || []} warning />
              </article>
            ))}
          </div>
        )}
      </div>
    </section>
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

function TagList({ title, items, warning = false }: { title: string; items: string[]; warning?: boolean }) {
  if (!items.length) return null;
  return (
    <div className="mt-3">
      <p className="text-xs font-semibold uppercase text-muted">{title}</p>
      <div className="mt-2 flex flex-wrap gap-2">
        {items.map((item) => (
          <span
            key={item}
            className={`rounded border px-2 py-0.5 text-xs ${
              warning ? 'border-warning-soft bg-warning-soft text-warning' : 'border-line bg-surface-raised text-muted'
            }`}
          >
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const className =
    status === 'confirmed' || status === 'high' || status === 'trusted' || status === 'formula'
      ? 'border-success-soft bg-success-soft text-success'
      : status === 'rejected' || status === 'low'
        ? 'border-danger-soft bg-danger-soft text-danger'
        : status === 'needs_review' || status === 'draft' || status === 'medium' || status === 'unscored'
          ? 'border-warning-soft bg-warning-soft text-warning'
          : 'border-accent-soft bg-accent-soft text-accent';
  return (
    <span className={`inline-flex rounded border px-2 py-0.5 text-xs font-semibold ${className}`}>
      {status}
    </span>
  );
}
