'use client';

import { useEffect, useMemo, useState } from 'react';
import { Calculator, Check, Eye, Loader2, Play, Upload, X } from 'lucide-react';

import { reviewLabApi } from '@/lib/api';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';
import { EmptyState, ShortcutHelp, SourceRefsPanel, StatusBadge } from '@/components/ux/UXStates';

type FormulaAsset = {
  asset_id: string;
  asset_type: string;
  title: string;
  module?: string;
  formula_latex?: string;
  plain_formula?: string;
  variables?: Array<{ symbol: string; meaning?: string; unit?: string }>;
  applies_when?: string[];
  not_when?: string[];
  assumptions?: string[];
  ba_ii_plus_steps?: string[];
  formula_family?: string;
  difficulty?: string;
  source_refs?: string[];
  validation_status: string;
  mastery_state?: string;
};

type FormulaSession = {
  session_id: string;
  units: any[];
  current_unit: any | null;
  current_unit_index: number;
  completed_unit_ids: string[];
  progress_pct: number;
  is_complete: boolean;
};

const sampleFormula = [
  'WACC = w_d r_d (1 - t) + w_e r_e.',
  'w_d = debt weight; r_d = pre-tax cost of debt; t = tax rate; w_e = equity weight; r_e = cost of equity.',
  'Use when valuing the firm with a target capital structure.',
  'BA II Plus: enter cash flows, press NPV, enter WACC as I/Y, then CPT NPV.',
].join('\n');

export default function ReviewFormulasPage() {
  const [title, setTitle] = useState('CFA formula note');
  const [text, setText] = useState(sampleFormula);
  const [assets, setAssets] = useState<FormulaAsset[]>([]);
  const [statusFilter, setStatusFilter] = useState('all');
  const [moduleFilter, setModuleFilter] = useState('');
  const [familyFilter, setFamilyFilter] = useState('all');
  const [masteryFilter, setMasteryFilter] = useState('all');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [session, setSession] = useState<FormulaSession | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [recallDraft, setRecallDraft] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [showShortcuts, setShowShortcuts] = useState(false);

  const loadFormulas = async () => {
    const result = await reviewLabApi.listFormulas();
    setAssets(result.assets || []);
  };

  useEffect(() => {
    loadFormulas().catch(() => undefined);
  }, []);

  const families = useMemo(() => {
    return Array.from(
      new Set(assets.map((asset) => asset.formula_family).filter((family): family is string => Boolean(family))),
    ).sort();
  }, [assets]);

  const filteredAssets = useMemo(() => {
    return assets.filter((asset) => {
      if (statusFilter !== 'all' && asset.validation_status !== statusFilter) return false;
      if (familyFilter !== 'all' && asset.formula_family !== familyFilter) return false;
      if (masteryFilter !== 'all' && asset.mastery_state !== masteryFilter) return false;
      if (moduleFilter && !(asset.module || '').toLowerCase().includes(moduleFilter.toLowerCase())) return false;
      return true;
    });
  }, [assets, familyFilter, masteryFilter, moduleFilter, statusFilter]);

  const importFormula = async () => {
    setBusy(true);
    setError('');
    try {
      const imported = await reviewLabApi.importFormulaText({ title, text });
      setAssets((current) => mergeAssets(current, imported.assets || []));
      setStatusFilter('all');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Formula import failed');
    } finally {
      setBusy(false);
    }
  };

  const updateAsset = async (assetId: string, action: 'confirm' | 'reject' | 'enrich') => {
    setError('');
    try {
      const result =
        action === 'confirm'
          ? await reviewLabApi.confirmFormula(assetId)
          : action === 'reject'
            ? await reviewLabApi.rejectFormula(assetId)
            : await reviewLabApi.enrichFormula(assetId);
      setAssets((current) => mergeAssets(current, [result.asset]));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Formula update failed');
    }
  };

  const startFormulaLab = async () => {
    setBusy(true);
    setError('');
    setRevealed(false);
    setRecallDraft('');
    try {
      const created = await reviewLabApi.generateFormulaSession({ max_units: 8 });
      setSession(created);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Formula Lab session failed');
    } finally {
      setBusy(false);
    }
  };

  const completeCurrent = async (outcome: 'recalled' | 'partial' | 'forgot' | 'skipped') => {
    if (!session?.current_unit || submitting) return;
    setSubmitting(true);
    try {
      await reviewLabApi.completeFormulaUnit(session.current_unit.unit_id, {
        session_id: session.session_id,
        outcome,
        confidence_after: outcome === 'recalled' ? 3 : outcome === 'partial' ? 2 : 0,
        answer_quality: outcome === 'recalled' ? 'perfect' : outcome === 'partial' ? 'minor_gap' : 'blank',
        next_action: outcome === 'recalled' ? 'advance' : 'drill',
      });
      const fresh = await reviewLabApi.getSession(session.session_id);
      setSession(fresh);
      setRevealed(false);
      setRecallDraft('');
      await loadFormulas();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Formula completion failed');
    } finally {
      setSubmitting(false);
    }
  };

  const current = session?.current_unit;
  const progress = session ? Math.round(session.progress_pct * 100) : 0;

  useKeyboardShortcuts({
    enabled: Boolean(session?.current_unit),
    revealed,
    onAction: (action) => {
      if (!current) return;
      if (action === 'help') {
        setShowShortcuts((value) => !value);
      } else if (action === 'reveal') {
        setRevealed(true);
      } else if (action === 'submit') {
        if (revealed) completeCurrent('recalled');
        else setRevealed(true);
      } else if (action === 'rate-forgot') {
        completeCurrent('forgot');
      } else if (action === 'rate-partial') {
        completeCurrent('partial');
      } else if (action === 'rate-recalled') {
        completeCurrent('recalled');
      } else if (action === 'rate-skipped' || action === 'next') {
        completeCurrent('skipped');
      }
    },
  });

  return (
    <div className="mx-auto max-w-6xl pb-12">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2">
          <Calculator size={20} className="text-accent" />
          <h2 className="text-xl font-bold">Formula Lab</h2>
        </div>
        <button
          type="button"
          onClick={startFormulaLab}
          disabled={busy}
          className="btn-primary inline-flex items-center gap-2"
        >
          {busy ? <Loader2 size={15} className="animate-spin" /> : <Play size={15} />}
          Start Formula Lab
        </button>
      </div>

      <ShortcutHelp open={showShortcuts} onToggle={() => setShowShortcuts((value) => !value)} className="mb-4" />

      {error && (
        <div className="mb-4 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          {error}
        </div>
      )}

      <div className="grid gap-4 xl:grid-cols-[minmax(0,0.8fr)_minmax(0,1.2fr)]">
        <section className="space-y-4">
          <div className="rounded-lg border border-line bg-surface-raised p-4">
            <label htmlFor="formula-title" className="block text-xs font-semibold uppercase text-muted">
              Source title
            </label>
            <input
              id="formula-title"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              className="input mt-2 w-full"
            />
            <label htmlFor="formula-text" className="mt-4 block text-xs font-semibold uppercase text-muted">
              Formula text
            </label>
            <textarea
              id="formula-text"
              value={text}
              onChange={(event) => setText(event.target.value)}
              rows={9}
              className="input mt-2 w-full resize-none text-sm leading-6"
            />
            <button
              type="button"
              onClick={importFormula}
              disabled={busy || !title.trim() || !text.trim()}
              className="btn-primary mt-4 inline-flex items-center gap-2"
            >
              {busy ? <Loader2 size={15} className="animate-spin" /> : <Upload size={15} />}
              Import formula
            </button>
          </div>

          <div className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="grid grid-cols-2 gap-3">
              <Select label="Status" value={statusFilter} onChange={setStatusFilter} options={['all', 'draft', 'needs_review', 'confirmed', 'rejected']} />
              <Select label="Family" value={familyFilter} onChange={setFamilyFilter} options={['all', ...families]} />
              <Select label="Mastery" value={masteryFilter} onChange={setMasteryFilter} options={['all', 'new', 'New', 'Learning', 'Practiced']} />
              <label className="block text-xs font-semibold uppercase text-muted">
                Module
                <input
                  value={moduleFilter}
                  onChange={(event) => setModuleFilter(event.target.value)}
                  className="input mt-2 w-full normal-case"
                />
              </label>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          {session && (
            <div data-testid="formula-session-panel" className="rounded-lg border border-accent-soft bg-surface-raised p-4">
              <div className="mb-3 flex items-center justify-between">
                <h3 className="font-semibold">Formula Review</h3>
                <span className="text-xs text-muted">
                  {session.completed_unit_ids.length} / {session.units.length}
                </span>
              </div>
              <div className="mb-4 h-1.5 overflow-hidden rounded-full bg-surface-field">
                <div className="h-full rounded-full bg-accent" style={{ width: `${progress}%` }} />
              </div>

              {!current && (
                <div className="py-6 text-sm text-muted">Formula session complete.</div>
              )}

              {current && (
                <div>
                  <p className="text-sm font-semibold">{current.front_prompt || current.prompt}</p>
                  {!revealed && (
                    <textarea
                      aria-label="Write formula recall before reveal"
                      value={recallDraft}
                      onChange={(event) => setRecallDraft(event.target.value)}
                      rows={4}
                      placeholder="Write the formula and variables before reveal."
                      className="input mt-3 w-full resize-none text-sm"
                    />
                  )}
                  {!revealed ? (
                    <button
                      type="button"
                      onClick={() => setRevealed(true)}
                      className="btn-primary mt-3 inline-flex items-center gap-2"
                    >
                      <Eye size={15} />
                      Reveal formula
                    </button>
                  ) : (
                    <div className="mt-4 space-y-3">
                      <p className="rounded-lg bg-surface-field p-3 font-mono text-sm">{current.formula_latex || current.answer}</p>
                      <MetadataList title="Variables" items={(current.variables || []).map((item: any) => `${item.symbol}: ${item.meaning || 'meaning pending'}`)} />
                      <MetadataList title="Applies when" items={current.applies_when || []} />
                      <MetadataList title="Boundaries" items={current.boundary_rules || current.not_when || []} />
                      <MetadataList title="BA II Plus" items={current.ba_ii_plus_steps || []} empty="No BA II Plus steps captured." />
                      <SourceRefsPanel refs={current.source_refs || []} />
                      <div className="flex flex-wrap gap-2 pt-2">
                        {(['forgot', 'partial', 'recalled', 'skipped'] as const).map((outcome) => (
                          <button
                            key={outcome}
                            type="button"
                            onClick={() => completeCurrent(outcome)}
                            disabled={submitting}
                            className="btn-secondary capitalize"
                          >
                            {outcome}
                          </button>
                        ))}
                      </div>
                      <p className="text-xs text-muted">1 Forgot · 2 Partial · 3 Recalled · S Skip · ? Shortcuts</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          <div className="space-y-3">
            {filteredAssets.length === 0 ? (
              <EmptyState title="No formula assets" detail="Import or confirm formula notes before starting a targeted formula drill." actionHref="/review/assets" actionLabel="Review assets" />
            ) : (
              filteredAssets.map((asset) => (
                <article key={asset.asset_id} className="rounded-lg border border-line bg-surface-raised p-4">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <h3 className="font-semibold">{asset.title}</h3>
                        <StatusBadge status={asset.validation_status} />
                      </div>
                      <p className="mt-1 text-xs uppercase text-muted">
                        {asset.formula_family || 'general'} · {asset.difficulty || 'basic'} · {asset.mastery_state || 'new'}
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <button type="button" onClick={() => updateAsset(asset.asset_id, 'enrich')} className="btn-secondary">
                        Enrich
                      </button>
                      <button type="button" onClick={() => updateAsset(asset.asset_id, 'confirm')} className="btn-secondary inline-flex items-center gap-1.5">
                        <Check size={14} />
                        Confirm
                      </button>
                      <button type="button" onClick={() => updateAsset(asset.asset_id, 'reject')} className="btn-secondary inline-flex items-center gap-1.5">
                        <X size={14} />
                        Reject
                      </button>
                    </div>
                  </div>
                  <p className="mt-3 rounded-lg bg-surface-field p-3 font-mono text-sm">
                    {asset.formula_latex || asset.plain_formula || asset.title}
                  </p>
                  <MetadataList title="Variables" items={(asset.variables || []).map((item) => `${item.symbol}: ${item.meaning || 'meaning pending'}`)} />
                  <MetadataList title="Applies when" items={asset.applies_when || []} />
                  <MetadataList title="Not when" items={asset.not_when || []} />
                  <MetadataList title="BA II Plus" items={asset.ba_ii_plus_steps || []} empty="No BA II Plus steps captured." />
                  <SourceRefsPanel refs={asset.source_refs || []} />
                </article>
              ))
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

function mergeAssets(current: FormulaAsset[], incoming: FormulaAsset[]) {
  const map = new Map(current.map((asset) => [asset.asset_id, asset]));
  for (const asset of incoming) {
    map.set(asset.asset_id, asset);
  }
  return Array.from(map.values());
}

function Select({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: string[];
}) {
  return (
    <label className="block text-xs font-semibold uppercase text-muted">
      {label}
      <select value={value} onChange={(event) => onChange(event.target.value)} className="input mt-2 w-full normal-case">
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}

function MetadataList({ title, items, empty }: { title: string; items: string[]; empty?: string }) {
  if (!items.length && !empty) return null;
  return (
    <div className="mt-3">
      <p className="text-xs font-semibold uppercase text-muted">{title}</p>
      {items.length ? (
        <ul className="mt-1 space-y-1 text-sm">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="mt-1 text-sm text-muted">{empty}</p>
      )}
    </div>
  );
}
