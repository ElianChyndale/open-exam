'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import { CheckCircle2, RefreshCw, ShieldAlert, XCircle } from 'lucide-react';

import {
  ResourceCandidate,
  ResourceDocument,
  resourceCandidatesApi,
  resourcesApi,
} from '@/lib/api';

export default function ResourceCandidatesPage() {
  const [candidates, setCandidates] = useState<ResourceCandidate[]>([]);
  const [documents, setDocuments] = useState<ResourceDocument[]>([]);
  const [message, setMessage] = useState('');
  const [busyId, setBusyId] = useState('');

  const refresh = useCallback(async () => {
    const [candidateData, documentData] = await Promise.all([
      resourceCandidatesApi.list(),
      resourcesApi.documents(),
    ]);
    setCandidates(candidateData.candidates);
    setDocuments(documentData.documents);
  }, []);

  useEffect(() => {
    refresh().catch((error) => {
      if (error instanceof Error && error.message.includes('403')) {
        setMessage('Resource candidate queue 当前未启用。请先开启 resource_quality_gate 和 resource_candidate_queue。');
        return;
      }
      setMessage('无法加载 ResourceOS candidate queue。');
    });
  }, [refresh]);

  const queuedDocumentIds = useMemo(() => new Set(candidates.map((item) => item.document_id)), [candidates]);
  const queueableDocuments = useMemo(
    () => documents.filter((item) => !queuedDocumentIds.has(item.document_id)).slice(0, 12),
    [documents, queuedDocumentIds],
  );

  const runAction = async (key: string, action: () => Promise<unknown>, success: string) => {
    setBusyId(key);
    setMessage('');
    try {
      await action();
      setMessage(success);
      await refresh();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : '操作失败。');
    } finally {
      setBusyId('');
    }
  };

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="metric-label text-accent">Wave 6 ResourceOS</p>
          <h1 className="mt-1 text-2xl font-bold">Resource Candidates</h1>
          <p className="mt-1 text-sm text-muted">
            文档先过质量门控，再进入人工审批和 promotion。这里展示评分、原因和审批动作。
          </p>
        </div>
        <button type="button" onClick={() => refresh()} className="btn-secondary flex items-center gap-2">
          <RefreshCw size={15} />
          刷新
        </button>
      </header>

      {message ? <div className="card text-sm">{message}</div> : null}

      <div className="grid gap-4 lg:grid-cols-[1.3fr_0.9fr]">
        <section className="card">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h2 className="font-semibold">候选队列</h2>
              <p className="mt-1 text-xs text-muted">按最新更新时间排序。`promote` 代表质量门建议可直接晋升，`review` 需要人工判断。</p>
            </div>
            <div className="text-sm text-muted">{candidates.length} items</div>
          </div>

          <div className="mt-4 space-y-3">
            {candidates.length === 0 ? <p className="text-sm text-muted">还没有候选项。</p> : null}
            {candidates.map((candidate) => {
              const score = candidate.score;
              const topReasons = [
                ...(score.strengths || []).slice(0, 2),
                ...(score.concerns || []).slice(0, 2),
              ].slice(0, 3);
              return (
                <article key={candidate.candidate_id} className="rounded-lg border border-line p-4">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div className="min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-sm font-semibold">{candidate.title || candidate.url}</span>
                        <Badge label={candidate.status} tone={candidate.status === 'approved' ? 'success' : candidate.status === 'rejected' ? 'danger' : 'muted'} />
                        <Badge label={score.recommendation || 'review'} tone={score.pass_gate ? 'success' : 'warning'} />
                      </div>
                      <p className="mt-1 text-xs text-muted">{candidate.lane} · {candidate.provider} · {candidate.url}</p>
                      <p className="mt-2 text-xs text-muted">{score.summary}</p>
                    </div>
                    <div className="rounded-lg border border-line px-3 py-2 text-right">
                      <div className="metric-label">Quality</div>
                      <div className="text-xl font-bold">{score.normalized_score ?? '--'}</div>
                    </div>
                  </div>

                  <div className="mt-3 grid gap-2 md:grid-cols-2">
                    {(score.dimensions || []).map((dimension: { dimension: string; score: number; reasons: string[] }) => (
                      <div key={dimension.dimension} className="rounded-md bg-surface-raised px-3 py-2 text-xs">
                        <div className="flex items-center justify-between gap-3">
                          <span className="font-medium">{dimension.dimension}</span>
                          <span>{Math.round((dimension.score || 0) * 100)}</span>
                        </div>
                        <p className="mt-1 text-muted">{dimension.reasons?.[0] || 'No detail.'}</p>
                      </div>
                    ))}
                  </div>

                  {topReasons.length > 0 ? (
                    <ul className="mt-3 space-y-1 text-xs text-muted">
                      {topReasons.map((reason) => <li key={reason}>• {reason}</li>)}
                    </ul>
                  ) : null}

                  <div className="mt-4 flex flex-wrap gap-2">
                    <button
                      type="button"
                      disabled={busyId === candidate.candidate_id}
                      onClick={() => runAction(candidate.candidate_id, () => resourceCandidatesApi.rescore(candidate.candidate_id), '已重新评分。')}
                      className="btn-secondary text-xs"
                    >
                      重新评分
                    </button>
                    <button
                      type="button"
                      disabled={busyId === candidate.candidate_id || candidate.status === 'approved'}
                      onClick={() => runAction(candidate.candidate_id, () => resourceCandidatesApi.approve(candidate.candidate_id), '候选项已批准并写入 promotion 事件。')}
                      className="btn-primary flex items-center gap-1 text-xs"
                    >
                      <CheckCircle2 size={14} />
                      批准
                    </button>
                    <button
                      type="button"
                      disabled={busyId === candidate.candidate_id || candidate.status === 'rejected'}
                      onClick={() => runAction(candidate.candidate_id, () => resourceCandidatesApi.reject(candidate.candidate_id), '候选项已拒绝。')}
                      className="btn-secondary flex items-center gap-1 text-xs text-danger"
                    >
                      <XCircle size={14} />
                      拒绝
                    </button>
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        <section className="card">
          <div className="flex items-start gap-2">
            <ShieldAlert size={18} className="mt-0.5 text-accent" />
            <div>
              <h2 className="font-semibold">待入队文档</h2>
              <p className="mt-1 text-xs text-muted">从现有 ResourceDocument 手动生成质量候选。这里只展示最近尚未入队的文档。</p>
            </div>
          </div>

          <div className="mt-4 space-y-3">
            {queueableDocuments.length === 0 ? <p className="text-sm text-muted">没有新的文档需要入队。</p> : null}
            {queueableDocuments.map((document) => (
              <div key={document.document_id} className="rounded-lg border border-line p-3">
                <p className="text-sm font-medium">{document.title || document.url}</p>
                <p className="mt-1 text-xs text-muted">{document.lane} · {document.provider} · {document.license_mode}</p>
                <p className="mt-2 line-clamp-3 text-xs text-muted">{document.excerpt || 'No excerpt.'}</p>
                <button
                  type="button"
                  disabled={busyId === document.document_id}
                  onClick={() => runAction(document.document_id, () => resourceCandidatesApi.enqueue(document.document_id), '文档已进入 candidate queue。')}
                  className="btn-secondary mt-3 text-xs"
                >
                  加入候选队列
                </button>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

function Badge({ label, tone }: { label: string; tone: 'success' | 'danger' | 'warning' | 'muted' }) {
  const className = {
    success: 'border-success-soft text-success',
    danger: 'border-danger-soft text-danger',
    warning: 'border-accent-soft text-accent',
    muted: 'border-line text-muted',
  }[tone];
  return <span className={`rounded-full border px-2 py-0.5 text-[10px] uppercase tracking-wide ${className}`}>{label}</span>;
}
