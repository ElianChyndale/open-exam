'use client';

import { useMemo, useState } from 'react';
import { AlertTriangle, Check, FileText, Loader2, Upload, X } from 'lucide-react';

import { reviewLabApi } from '@/lib/api';

type CandidateAsset = {
  asset_id: string;
  asset_type: string;
  title: string;
  correct_rule: string;
  formula_latex?: string;
  source_refs: string[];
  validation_status: 'draft' | 'needs_review' | 'confirmed' | 'rejected' | string;
};

const sampleNote = [
  'Gordon growth model is a dividend discount model for stable perpetual dividend growth.',
  'Intrinsic value = D1 / (r - g).',
  'Use Gordon growth only if dividends grow at a stable rate and required return is greater than growth.',
].join('\n');

export default function ReviewAssetsPage() {
  const [title, setTitle] = useState('CFA note import');
  const [text, setText] = useState(sampleNote);
  const [sourceId, setSourceId] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileRecord, setFileRecord] = useState<any>(null);
  const [fileSegments, setFileSegments] = useState<any[]>([]);
  const [fileWarnings, setFileWarnings] = useState<string[]>([]);
  const [assets, setAssets] = useState<CandidateAsset[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const counts = useMemo(() => {
    return assets.reduce<Record<string, number>>((acc, asset) => {
      acc[asset.validation_status] = (acc[asset.validation_status] || 0) + 1;
      return acc;
    }, {});
  }, [assets]);

  const importAndExtract = async () => {
    setBusy(true);
    setError('');
    try {
      const imported = await reviewLabApi.importTextSource({
        title,
        text,
        source_type: 'text_note',
      });
      const sid = imported.source.source_id;
      setSourceId(sid);
      const extracted = await reviewLabApi.extractAssets(sid);
      setAssets(extracted.assets || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Import failed');
    } finally {
      setBusy(false);
    }
  };

  const importFileAndExtract = async () => {
    if (!selectedFile) return;
    setBusy(true);
    setError('');
    try {
      const imported = await reviewLabApi.importSourceFile({
        file: selectedFile,
        title: title.trim() || selectedFile.name,
        source_type: selectedFile.name.toLowerCase().endsWith('.pdf')
          ? 'pdf_note'
          : selectedFile.name.toLowerCase().endsWith('.md')
            ? 'markdown_note'
            : 'text_note',
      });
      setFileRecord(imported.file);
      setFileSegments(imported.segments || []);
      setFileWarnings(imported.warnings || []);
      setSourceId(imported.source?.source_id || imported.file?.source_id || '');
      setAssets(imported.assets || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'File import failed');
    } finally {
      setBusy(false);
    }
  };

  const updateAsset = async (assetId: string, action: 'confirm' | 'reject') => {
    setError('');
    try {
      const result =
        action === 'confirm'
          ? await reviewLabApi.confirmAsset(assetId)
          : await reviewLabApi.rejectAsset(assetId);
      setAssets((current) =>
        current.map((asset) => (asset.asset_id === assetId ? result.asset : asset)),
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Asset update failed');
    }
  };

  return (
    <div className="mx-auto max-w-5xl pb-12">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2">
          <FileText size={20} className="text-accent" />
          <h2 className="text-xl font-bold">Review Assets</h2>
        </div>
        <div className="flex gap-2 text-xs text-muted">
          <span>Draft {counts.draft || 0}</span>
          <span>Needs review {counts.needs_review || 0}</span>
          <span>Confirmed {counts.confirmed || 0}</span>
          <span>Rejected {counts.rejected || 0}</span>
        </div>
      </div>

      <div className="mb-4 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
        Draft assets are not used in normal Review Lab until confirmed.
      </div>

      {error && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="grid gap-4 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
        <section className="rounded-lg border border-line bg-surface-raised p-4">
          <label htmlFor="asset-source-title" className="block text-xs font-semibold uppercase text-muted">
            Source title
          </label>
          <input
            id="asset-source-title"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            className="input mt-2 w-full"
          />

          <label htmlFor="asset-source-text" className="mt-4 block text-xs font-semibold uppercase text-muted">
            Note text
          </label>
          <textarea
            id="asset-source-text"
            value={text}
            onChange={(event) => setText(event.target.value)}
            rows={12}
            className="input mt-2 w-full resize-none text-sm leading-6"
          />

          <button
            type="button"
            onClick={importAndExtract}
            disabled={busy || !title.trim() || !text.trim()}
            className="btn-primary mt-4 inline-flex items-center gap-2"
          >
            {busy ? <Loader2 size={15} className="animate-spin" /> : <Upload size={15} />}
            Generate candidates
          </button>

          <div className="mt-5 border-t border-line pt-4">
            <label htmlFor="asset-source-file" className="block text-xs font-semibold uppercase text-muted">
              Source file
            </label>
            <input
              id="asset-source-file"
              type="file"
              accept=".txt,.md,.markdown,.pdf"
              onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
              className="input mt-2 w-full text-sm"
            />
            <p className="mt-2 text-xs text-muted">Supported: PDF, TXT, MD</p>
            <button
              type="button"
              onClick={importFileAndExtract}
              disabled={busy || !selectedFile}
              className="btn-secondary mt-3 inline-flex items-center gap-2"
            >
              {busy ? <Loader2 size={15} className="animate-spin" /> : <FileText size={15} />}
              Import file
            </button>
          </div>

          {sourceId && (
            <p className="mt-3 break-all text-xs text-muted">
              Source {sourceId}
            </p>
          )}

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
              {fileSegments.length > 0 && (
                <div className="mt-3 space-y-2">
                  {fileSegments.slice(0, 3).map((segment) => (
                    <div key={segment.source_ref} className="rounded border border-line bg-surface-raised p-2">
                      <p className="break-all font-mono text-[11px] text-muted">{segment.source_ref}</p>
                      <p className="mt-1 line-clamp-3 text-sm leading-5">{segment.text}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </section>

        <section className="space-y-3">
          {assets.length === 0 ? (
            <div className="rounded-lg border border-line bg-surface-raised p-6 text-sm text-muted">
              No candidates yet.
            </div>
          ) : (
            assets.map((asset) => (
              <article key={asset.asset_id} className="rounded-lg border border-line bg-surface-raised p-4">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="font-semibold">{asset.title}</h3>
                      <StatusBadge status={asset.validation_status} />
                    </div>
                    <p className="mt-1 text-xs uppercase text-muted">{asset.asset_type}</p>
                  </div>
                  <div className="flex gap-2">
                    <button
                      type="button"
                      onClick={() => updateAsset(asset.asset_id, 'confirm')}
                      disabled={asset.validation_status === 'confirmed'}
                      className="btn-secondary inline-flex items-center gap-1.5"
                    >
                      <Check size={14} />
                      Confirm
                    </button>
                    <button
                      type="button"
                      onClick={() => updateAsset(asset.asset_id, 'reject')}
                      disabled={asset.validation_status === 'rejected'}
                      className="btn-secondary inline-flex items-center gap-1.5"
                    >
                      <X size={14} />
                      Reject
                    </button>
                  </div>
                </div>

                <p className="mt-3 text-sm leading-6">{asset.correct_rule}</p>
                {asset.formula_latex && (
                  <p className="mt-2 rounded-lg bg-surface-field p-2 font-mono text-xs">
                    {asset.formula_latex}
                  </p>
                )}
                <div className="mt-3 flex flex-wrap gap-2">
                  {asset.source_refs.map((ref) => (
                    <span key={ref} className="rounded bg-surface-field px-2 py-1 text-xs text-muted">
                      {ref}
                    </span>
                  ))}
                </div>
              </article>
            ))
          )}
        </section>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const className =
    status === 'confirmed'
      ? 'border-success-soft bg-success-soft text-success'
      : status === 'rejected'
        ? 'border-danger-soft bg-danger-soft text-danger'
        : status === 'needs_review'
          ? 'border-warning-soft bg-warning-soft text-warning'
          : 'border-accent-soft bg-accent-soft text-accent';
  return (
    <span className={`rounded border px-2 py-0.5 text-xs font-semibold ${className}`}>
      {status}
    </span>
  );
}
