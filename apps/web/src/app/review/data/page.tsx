'use client';

import Link from 'next/link';
import type { ReactNode } from 'react';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  Archive,
  ArrowRight,
  CheckCircle2,
  Database,
  Download,
  FileWarning,
  HardDrive,
  KeyRound,
  Loader2,
  RefreshCw,
  RotateCcw,
  ShieldCheck,
  Trash2,
  Upload,
} from 'lucide-react';

import { BackupSnapshot, DataInventoryItem, dataGovernanceApi } from '@/lib/api';
import { EmptyState, ErrorState, LoadingState, QualityGateWarning, StatusBadge } from '@/components/ux/UXStates';

const links = [
  { href: '/onboarding', label: 'Onboarding' },
  { href: '/review/goals', label: 'Goals' },
  { href: '/review/mission-control', label: 'Mission Control' },
  { href: '/review/analytics', label: 'Analytics' },
  { href: '/review/knowledge-map', label: 'Knowledge Map' },
  { href: '/review/interop', label: 'Interop' },
  { href: '/review/resources', label: 'Resources' },
  { href: '/language/dictionaries', label: 'LanguageOS' },
];

export default function DataGovernancePage() {
  const [inventory, setInventory] = useState<DataInventoryItem[]>([]);
  const [summary, setSummary] = useState<Record<string, any>>({});
  const [snapshots, setSnapshots] = useState<BackupSnapshot[]>([]);
  const [privacy, setPrivacy] = useState<Record<string, any> | null>(null);
  const [busy, setBusy] = useState(true);
  const [working, setWorking] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<'all' | 'raw' | 'source' | 'resettable'>('all');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [includeRaw, setIncludeRaw] = useState(false);
  const [restorePath, setRestorePath] = useState('');
  const [dryRun, setDryRun] = useState<Record<string, any> | null>(null);
  const [resetCategory, setResetCategory] = useState('knowledge_graph');
  const [resetConfirmation, setResetConfirmation] = useState('');

  const load = async () => {
    setBusy(true);
    setError('');
    try {
      const [inventoryPayload, snapshotPayload, privacyPayload] = await Promise.all([
        dataGovernanceApi.inventory(),
        dataGovernanceApi.snapshots(),
        dataGovernanceApi.privacyReport(),
      ]);
      setInventory(inventoryPayload.items || []);
      setSummary(inventoryPayload.summary || {});
      setSnapshots(snapshotPayload.snapshots || []);
      setPrivacy(privacyPayload);
      setSelectedCategories((inventoryPayload.items || []).filter((item) => item.exportable).slice(0, 3).map((item) => item.category));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Data governance load failed');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const filteredInventory = useMemo(() => {
    return inventory.filter((item) => {
      if (categoryFilter === 'raw') return item.contains_raw_diagnostics;
      if (categoryFilter === 'source') return item.contains_source_files;
      if (categoryFilter === 'resettable') return item.resettable;
      return true;
    });
  }, [categoryFilter, inventory]);

  const resettable = inventory.filter((item) => item.resettable);
  const resetExpected = `RESET ${resetCategory}`;
  const restoreReady = Boolean(dryRun?.valid && restorePath);

  const exportBackup = async (mode: 'safe' | 'full' | 'category') => {
    setWorking(`export-${mode}`);
    setError('');
    setMessage('');
    try {
      const payload = await dataGovernanceApi.exportBackup({
        mode,
        categories: mode === 'category' ? selectedCategories : undefined,
        include_raw_diagnostics: mode === 'full' ? includeRaw : false,
        label: `${mode} export`,
      });
      setMessage(`Export created: ${payload.snapshot.file_path}`);
      setRestorePath(payload.snapshot.file_path);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Export failed');
    } finally {
      setWorking('');
    }
  };

  const runDryRun = async () => {
    setWorking('dry-run');
    setError('');
    setDryRun(null);
    try {
      const payload = await dataGovernanceApi.restoreDryRun({ file_path: restorePath, mode: 'dry_run' });
      setDryRun(payload);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Restore dry run failed');
    } finally {
      setWorking('');
    }
  };

  const restore = async () => {
    setWorking('restore');
    setError('');
    try {
      const payload = await dataGovernanceApi.restore({ file_path: restorePath, mode: 'merge' });
      setMessage(`Restore ${payload.restored ? 'completed' : 'blocked'}: ${(payload.restored_categories || []).join(', ')}`);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Restore failed');
    } finally {
      setWorking('');
    }
  };

  const reset = async () => {
    setWorking('reset');
    setError('');
    try {
      const payload = await dataGovernanceApi.reset({ category: resetCategory, confirmation: resetConfirmation });
      setMessage(`Reset ${payload.category}; snapshot ${payload.snapshot?.file_path}`);
      setRestorePath(payload.snapshot?.file_path || '');
      setResetConfirmation('');
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Reset failed');
    } finally {
      setWorking('');
    }
  };

  const rollback = async (snapshot: BackupSnapshot) => {
    setWorking(snapshot.snapshot_id);
    setError('');
    try {
      const payload = await dataGovernanceApi.rollback(snapshot.snapshot_id, { categories: snapshot.categories });
      setMessage(`Rollback restored: ${(payload.restored_categories || []).join(', ')}`);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Rollback failed');
    } finally {
      setWorking('');
    }
  };

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Database size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Data Governance</h2>
          </div>
          <p className="mt-1 text-sm text-muted">
            {inventory.length} categories / {formatBytes(summary.size_bytes || 0)} local state / {snapshots.length} snapshots
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {links.map((link) => (
            <Link key={link.href} href={link.href} className="btn-secondary inline-flex items-center gap-2">
              {link.label}
            </Link>
          ))}
          <button type="button" onClick={load} disabled={busy} className="btn-primary inline-flex items-center gap-2">
            {busy ? <Loader2 size={15} className="animate-spin" /> : <RefreshCw size={15} />}
            Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4">
          <ErrorState message={error} />
        </div>
      )}
      {message && (
        <p role="status" className="mb-4 rounded-lg border border-success-soft bg-success-soft p-3 text-sm text-success">
          {message}
        </p>
      )}

      <div className="mb-4 grid gap-3 md:grid-cols-4">
        <Metric icon={HardDrive} label="State Size" value={formatBytes(summary.size_bytes || 0)} />
        <Metric icon={FileWarning} label="Raw Categories" value={String((summary.raw_diagnostic_categories || []).length)} />
        <Metric icon={Archive} label="Snapshots" value={String(snapshots.length)} />
        <Metric icon={ShieldCheck} label="Safe Export" value="Redacted" />
      </div>

      <div className="mb-4">
        <QualityGateWarning>
          <p className="font-semibold">Full export includes raw local diagnostics</p>
          <p>Safe export redacts raw wrong-answer fields and internal diagnostics. Full export requires explicit raw diagnostic consent.</p>
        </QualityGateWarning>
      </div>

      {busy ? (
        <LoadingState title="Loading governed local state" detail="Scanning inventory, snapshots, and privacy report." />
      ) : (
        <div className="grid gap-4 xl:grid-cols-[minmax(0,1.15fr)_minmax(360px,0.85fr)]">
          <section className="space-y-4">
            <div className="rounded-lg border border-line bg-surface-raised">
              <div className="flex flex-col gap-3 border-b border-line p-4 md:flex-row md:items-center md:justify-between">
                <h3 className="font-semibold">Inventory</h3>
                <div className="flex flex-wrap gap-2">
                  {(['all', 'raw', 'source', 'resettable'] as const).map((filter) => (
                    <button
                      key={filter}
                      type="button"
                      onClick={() => setCategoryFilter(filter)}
                      className={categoryFilter === filter ? 'btn-primary' : 'btn-secondary'}
                    >
                      {labelize(filter)}
                    </button>
                  ))}
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="border-b border-line text-xs uppercase text-muted">
                    <tr>
                      <th className="px-4 py-3">Category</th>
                      <th className="px-4 py-3">Records</th>
                      <th className="px-4 py-3">Size</th>
                      <th className="px-4 py-3">Signals</th>
                      <th className="px-4 py-3">Path</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-line">
                    {filteredInventory.map((item) => (
                      <tr key={item.category}>
                        <td className="px-4 py-3 font-semibold">{labelize(item.category)}</td>
                        <td className="px-4 py-3">{item.record_count}</td>
                        <td className="px-4 py-3">{formatBytes(item.size_bytes)}</td>
                        <td className="px-4 py-3">
                          <div className="flex flex-wrap gap-1.5">
                            {item.contains_raw_diagnostics && <StatusBadge status="raw" />}
                            {item.contains_source_files && <StatusBadge status="files" />}
                            {item.resettable && <StatusBadge status="resettable" />}
                          </div>
                        </td>
                        <td className="max-w-xs px-4 py-3 text-xs text-muted break-anywhere">{item.path || 'not present'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="rounded-lg border border-line bg-surface-raised p-4">
              <h3 className="font-semibold">Privacy Report</h3>
              {privacy ? (
                <div className="mt-3 grid gap-3 md:grid-cols-3">
                  <Metric icon={KeyRound} label="Fields Redacted" value={String(privacy.redacted_fields_count || 0)} />
                  <Metric icon={AlertTriangle} label="Raw Categories" value={String((privacy.raw_diagnostic_categories || []).length)} />
                  <Metric icon={ShieldCheck} label="Safe Mode" value={privacy.safe_export?.includes_raw_diagnostics ? 'Raw' : 'No raw'} />
                </div>
              ) : (
                <EmptyState title="No privacy report" detail="Privacy report is unavailable." />
              )}
              <div className="mt-3 flex flex-wrap gap-2">
                {(privacy?.raw_diagnostic_categories || []).map((category: string) => (
                  <span key={category} className="rounded border border-warning-soft bg-warning-soft px-2 py-1 text-xs font-semibold text-warning">
                    {labelize(category)}
                  </span>
                ))}
              </div>
            </div>
          </section>

          <aside className="space-y-4">
            <Panel title="Backup / Export" icon={Download}>
              <div className="grid gap-2">
                <button type="button" onClick={() => exportBackup('safe')} disabled={Boolean(working)} className="btn-primary inline-flex items-center justify-center gap-2">
                  {working === 'export-safe' ? <Loader2 size={15} className="animate-spin" /> : <ShieldCheck size={15} />}
                  Create safe export
                </button>
                <div className="rounded-lg border border-line bg-surface-field p-3">
                  <p className="text-xs font-semibold uppercase text-muted">Category export</p>
                  <div className="mt-2 grid max-h-40 gap-1 overflow-y-auto">
                    {inventory.filter((item) => item.exportable).map((item) => (
                      <label key={item.category} className="flex items-center gap-2 text-sm">
                        <input
                          type="checkbox"
                          checked={selectedCategories.includes(item.category)}
                          onChange={(event) => {
                            setSelectedCategories((current) =>
                              event.target.checked ? [...current, item.category] : current.filter((category) => category !== item.category),
                            );
                          }}
                        />
                        {labelize(item.category)}
                      </label>
                    ))}
                  </div>
                  <button type="button" onClick={() => exportBackup('category')} disabled={Boolean(working) || !selectedCategories.length} className="btn-secondary mt-3 w-full">
                    Export selected categories
                  </button>
                </div>
                <div className="rounded-lg border border-danger-soft bg-danger-soft p-3">
                  <label className="flex items-center gap-2 text-sm font-semibold text-danger">
                    <input type="checkbox" checked={includeRaw} onChange={(event) => setIncludeRaw(event.target.checked)} />
                    Include raw diagnostics
                  </label>
                  <button type="button" onClick={() => exportBackup('full')} disabled={Boolean(working) || !includeRaw} className="btn-secondary mt-3 w-full">
                    Create full export
                  </button>
                </div>
              </div>
            </Panel>

            <Panel title="Restore Dry Run" icon={Upload}>
              <label className="text-xs font-semibold uppercase text-muted">
                Backup relative path
                <input
                  value={restorePath}
                  onChange={(event) => {
                    setRestorePath(event.target.value);
                    setDryRun(null);
                  }}
                  placeholder=".system/memory/backups/backup-id.zip"
                  className="input mt-2 w-full normal-case"
                />
              </label>
              <div className="mt-3 grid grid-cols-2 gap-2">
                <button type="button" onClick={runDryRun} disabled={Boolean(working) || !restorePath} className="btn-secondary inline-flex items-center justify-center gap-2">
                  {working === 'dry-run' ? <Loader2 size={15} className="animate-spin" /> : <CheckCircle2 size={15} />}
                  Dry run
                </button>
                <button type="button" onClick={restore} disabled={Boolean(working) || !restoreReady} className="btn-primary inline-flex items-center justify-center gap-2">
                  Restore merge
                </button>
              </div>
              {dryRun && (
                <div className={`mt-3 rounded-lg border p-3 text-sm ${dryRun.valid ? 'border-success-soft bg-success-soft text-success' : 'border-danger-soft bg-danger-soft text-danger'}`}>
                  <p className="font-semibold">{dryRun.valid ? 'Dry run valid' : 'Dry run blocked'}</p>
                  <p className="mt-1">{(dryRun.planned_changes || []).length} planned changes / {(dryRun.conflicts || []).length} conflicts</p>
                  {(dryRun.errors || []).map((item: string) => <p key={item} className="mt-1 break-anywhere">{item}</p>)}
                </div>
              )}
            </Panel>

            <Panel title="Snapshots / Rollback" icon={RotateCcw}>
              <div className="space-y-2">
                {snapshots.slice(0, 6).map((snapshot) => (
                  <div key={snapshot.snapshot_id} className="rounded-lg border border-line bg-surface-field p-3">
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <p className="truncate text-sm font-semibold">{snapshot.snapshot_id}</p>
                        <p className="mt-1 text-xs text-muted">{snapshot.mode} / {formatBytes(snapshot.size_bytes)}</p>
                      </div>
                      <button type="button" onClick={() => rollback(snapshot)} disabled={Boolean(working)} className="btn-secondary inline-flex items-center gap-1.5">
                        <ArrowRight size={14} />
                        Rollback
                      </button>
                    </div>
                    <p className="mt-2 text-xs text-muted break-anywhere">{snapshot.file_path}</p>
                  </div>
                ))}
                {!snapshots.length && <EmptyState title="No snapshots yet" detail="Create a safe export or reset snapshot first." />}
              </div>
            </Panel>

            <Panel title="Reset Controls" icon={Trash2}>
              <label className="text-xs font-semibold uppercase text-muted">
                Category
                <select value={resetCategory} onChange={(event) => setResetCategory(event.target.value)} className="input mt-2 w-full normal-case">
                  {resettable.map((item) => <option key={item.category} value={item.category}>{labelize(item.category)}</option>)}
                  <option value="all">All resettable local state</option>
                </select>
              </label>
              <label className="mt-3 block text-xs font-semibold uppercase text-muted">
                Confirmation
                <input
                  value={resetConfirmation}
                  onChange={(event) => setResetConfirmation(event.target.value)}
                  placeholder={resetExpected}
                  className="input mt-2 w-full normal-case"
                />
              </label>
              <button type="button" onClick={reset} disabled={Boolean(working) || resetConfirmation !== resetExpected} className="btn-secondary mt-3 inline-flex w-full items-center justify-center gap-2">
                <Trash2 size={15} />
                Reset category
              </button>
            </Panel>
          </aside>
        </div>
      )}
    </div>
  );
}

function Panel({ title, icon: Icon, children }: { title: string; icon: any; children: ReactNode }) {
  return (
    <section className="rounded-lg border border-line bg-surface-raised p-4">
      <div className="mb-3 flex items-center gap-2">
        <Icon size={17} className="text-accent" />
        <h3 className="font-semibold">{title}</h3>
      </div>
      {children}
    </section>
  );
}

function Metric({ icon: Icon, label, value }: { icon: any; label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-surface-raised p-4">
      <div className="flex items-center justify-between gap-3">
        <Icon size={18} className="text-accent" />
        <span className="text-lg font-bold">{value}</span>
      </div>
      <p className="mt-2 text-xs font-semibold uppercase text-muted">{label}</p>
    </div>
  );
}

function formatBytes(value: number) {
  if (!value) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  let next = value;
  let unit = 0;
  while (next >= 1024 && unit < units.length - 1) {
    next /= 1024;
    unit += 1;
  }
  return `${next >= 10 || unit === 0 ? Math.round(next) : next.toFixed(1)} ${units[unit]}`;
}

function labelize(value: string) {
  return value.replace(/_/g, ' ').replace(/\b\w/g, (match) => match.toUpperCase());
}
