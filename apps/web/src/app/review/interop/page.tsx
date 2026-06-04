'use client';

import Link from 'next/link';
import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  Archive,
  ArrowRight,
  Brain,
  CalendarCheck2,
  CheckCircle2,
  ClipboardCheck,
  Database,
  Download,
  FileDown,
  FileText,
  FileUp,
  Gauge,
  Languages,
  Loader2,
  Map,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  Upload,
} from 'lucide-react';

import {
  AdaptiveStudyPlan,
  GoalProfile,
  InteropArtifact,
  InteropImportPreview,
  goalsApi,
  interopApi,
  studyPlannerApi,
} from '@/lib/api';

type InteropTab = 'anki' | 'markdown' | 'calendar' | 'records';

type ExportResult = {
  kind: string;
  artifact?: InteropArtifact;
  payload: Record<string, any>;
};

const tabs: Array<{ key: InteropTab; label: string; icon: any }> = [
  { key: 'anki', label: 'Anki', icon: ClipboardCheck },
  { key: 'markdown', label: 'Markdown / Obsidian', icon: Archive },
  { key: 'calendar', label: 'Calendar', icon: CalendarCheck2 },
  { key: 'records', label: 'Learning Records', icon: FileText },
];

const quickLinks = [
  { href: '/review/data', label: 'Data Governance', icon: Database },
  { href: '/review/knowledge-map', label: 'Knowledge Map', icon: Map },
  { href: '/review/goals', label: 'Goals', icon: Gauge },
  { href: '/review/lab', label: 'Review Lab', icon: Brain },
  { href: '/language/dictionaries', label: 'LanguageOS', icon: Languages },
  { href: '/review/mission-control', label: 'Mission', icon: ShieldCheck },
  { href: '/review/tutor', label: 'Tutor', icon: Sparkles },
];

const forbiddenKeys = new Set([
  'wrong_choice_or_output',
  'wrong_formula',
  'wrong_reasoning',
  'answer_text',
  'selected_choice',
  'common_wrong_path',
  'internal_secret',
]);

export default function InteropPage() {
  const [tab, setTab] = useState<InteropTab>('anki');
  const [profileId, setProfileId] = useState('default');
  const [goals, setGoals] = useState<GoalProfile[]>([]);
  const [activeGoal, setActiveGoal] = useState<GoalProfile | null>(null);
  const [todayPlan, setTodayPlan] = useState<AdaptiveStudyPlan | null>(null);
  const [artifacts, setArtifacts] = useState<InteropArtifact[]>([]);
  const [privacy, setPrivacy] = useState<Record<string, any> | null>(null);
  const [confirmedOnly, setConfirmedOnly] = useState(true);
  const [ankiFormat, setAnkiFormat] = useState<'csv' | 'tsv'>('csv');
  const [moduleFilter, setModuleFilter] = useState('');
  const [topicFilter, setTopicFilter] = useState('');
  const [assetTypeFilter, setAssetTypeFilter] = useState('');
  const [ankiImportPath, setAnkiImportPath] = useState('');
  const [markdownImportPath, setMarkdownImportPath] = useState('');
  const [ankiPreview, setAnkiPreview] = useState<InteropImportPreview | null>(null);
  const [markdownPreview, setMarkdownPreview] = useState<InteropImportPreview | null>(null);
  const [planId, setPlanId] = useState('');
  const [startDatetime, setStartDatetime] = useState('');
  const [timezone, setTimezone] = useState('UTC');
  const [includeCompleted, setIncludeCompleted] = useState(false);
  const [lastExport, setLastExport] = useState<ExportResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const refreshArtifacts = useCallback(async () => {
    const payload = await interopApi.artifacts();
    setArtifacts(payload.artifacts || []);
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const [artifactPayload, privacyPayload, goalPayload, planPayload] = await Promise.allSettled([
        interopApi.artifacts(),
        interopApi.privacyReport(),
        goalsApi.list({ include_archived: false }),
        studyPlannerApi.getToday({ profile_id: profileId }),
      ]);
      if (artifactPayload.status === 'fulfilled') setArtifacts(artifactPayload.value.artifacts || []);
      if (privacyPayload.status === 'fulfilled') setPrivacy(privacyPayload.value);
      if (goalPayload.status === 'fulfilled') {
        setGoals(goalPayload.value.goals || []);
        setActiveGoal(goalPayload.value.active_goal || null);
        const nextGoal = goalPayload.value.active_goal || goalPayload.value.goals?.[0] || null;
        if (nextGoal) setProfileId(nextGoal.profile_id || 'default');
      }
      if (planPayload.status === 'fulfilled') {
        setTodayPlan(planPayload.value);
        setPlanId((current) => current || planPayload.value.plan_id || '');
      }
      if (!startDatetime) setStartDatetime(defaultLocalStart());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Interop load failed');
    } finally {
      setLoading(false);
    }
  }, [profileId, startDatetime]);

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const artifactCounts = useMemo(() => {
    return artifacts.reduce<Record<string, number>>((acc, artifact) => {
      acc[artifact.artifact_type] = (acc[artifact.artifact_type] || 0) + 1;
      return acc;
    }, {});
  }, [artifacts]);

  const exportFilters = useCallback(() => ({
    profile_id: profileId || 'default',
    confirmed_only: confirmedOnly,
    source_filters: {
      module: moduleFilter || undefined,
      topic: topicFilter || undefined,
      asset_type: assetTypeFilter || undefined,
    },
  }), [assetTypeFilter, confirmedOnly, moduleFilter, profileId, topicFilter]);

  const run = async (key: string, operation: () => Promise<void>) => {
    setWorking(key);
    setError('');
    setMessage('');
    try {
      await operation();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Interop operation failed');
    } finally {
      setWorking('');
    }
  };

  const exportAnki = () => run('export-anki', async () => {
    const payload = await interopApi.exportAnki({ ...exportFilters(), format: ankiFormat });
    setLastExport({ kind: 'Anki deck', artifact: payload.artifact, payload });
    setAnkiImportPath(payload.artifact.file_path);
    setMessage(`Anki artifact created: ${payload.item_count} notes`);
    await refreshArtifacts();
  });

  const previewAnki = () => run('preview-anki', async () => {
    const payload = await interopApi.previewAnki({ profile_id: profileId, file_path: ankiImportPath });
    setAnkiPreview(payload);
    setMessage(`Anki preview: ${payload.detected_items} detected / ${payload.duplicates} duplicates`);
  });

  const commitAnki = () => run('commit-anki', async () => {
    if (!ankiPreview) return;
    const payload = await interopApi.commitAnki({ preview_id: ankiPreview.preview_id });
    setMessage(`Anki draft import committed: ${payload.committed_count || 0} draft records`);
    setAnkiPreview(null);
  });

  const exportMarkdown = () => run('export-markdown', async () => {
    const payload = await interopApi.exportMarkdown(exportFilters());
    setLastExport({ kind: 'Markdown archive', artifact: payload.artifact, payload });
    setMarkdownImportPath(payload.artifact.file_path);
    setMessage(`Markdown artifact created: ${payload.item_count} notes`);
    await refreshArtifacts();
  });

  const previewMarkdown = () => run('preview-markdown', async () => {
    const payload = await interopApi.previewMarkdown({ profile_id: profileId, file_path: markdownImportPath });
    setMarkdownPreview(payload);
    setMessage(`Markdown preview: ${payload.detected_items} detected / ${payload.duplicates} duplicates`);
  });

  const commitMarkdown = () => run('commit-markdown', async () => {
    if (!markdownPreview) return;
    const payload = await interopApi.commitMarkdown({ preview_id: markdownPreview.preview_id });
    setMessage(`Markdown draft import committed: ${payload.committed_count || 0} draft records`);
    setMarkdownPreview(null);
  });

  const exportCalendar = () => run('export-calendar', async () => {
    const selectedPlan = planId || todayPlan?.plan_id || '';
    if (!selectedPlan) throw new Error('No study plan is available for calendar export');
    const payload = await interopApi.exportCalendar({
      profile_id: profileId,
      plan_id: selectedPlan,
      start_datetime: startDatetime || defaultLocalStart(),
      timezone,
      include_completed: includeCompleted,
    });
    setLastExport({ kind: 'Calendar file', artifact: payload.artifact, payload });
    setMessage(`Calendar artifact created: ${payload.event_count} events`);
    await refreshArtifacts();
  });

  const exportLearningRecords = () => run('export-records', async () => {
    const payload = await interopApi.exportLearningRecords({ profile_id: profileId, safe_mode: true });
    setLastExport({ kind: 'Learning records', artifact: payload.artifact, payload });
    setMessage(`Learning record artifact created: ${payload.statement_count} statements`);
    await refreshArtifacts();
  });

  const latest = artifacts[0] || null;

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <FileDown size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Ecosystem Interop</h2>
          </div>
          <p className="mt-1 text-sm text-muted">
            {latest ? `${artifacts.length} artifacts / latest ${labelize(latest.artifact_type)}` : 'Local safe export bridge'}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {quickLinks.map(({ href, label, icon: Icon }) => (
            <Link key={href} href={href} className="btn-secondary inline-flex items-center gap-2">
              <Icon size={14} />
              {label}
            </Link>
          ))}
          <button type="button" onClick={load} disabled={loading || Boolean(working)} className="btn-primary inline-flex items-center gap-2">
            {loading ? <Loader2 size={15} className="animate-spin" /> : <RefreshCw size={15} />}
            Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}
      {message && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-success-soft bg-success-soft p-3 text-sm text-success">
          <CheckCircle2 size={16} className="mt-0.5 shrink-0" />
          <span>{message}</span>
        </div>
      )}

      <section className="mb-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-6">
        <Metric icon={ShieldCheck} label="Safe Mode" value={privacy?.safe_mode_default === false ? 'off' : 'on'} />
        <Metric icon={ClipboardCheck} label="Anki" value={String((artifactCounts.anki_csv || 0) + (artifactCounts.anki_tsv || 0))} />
        <Metric icon={Archive} label="Markdown" value={String(artifactCounts.markdown_zip || 0)} />
        <Metric icon={CalendarCheck2} label="Calendar" value={String(artifactCounts.ics || 0)} />
        <Metric icon={FileText} label="Records" value={String(artifactCounts.xapi_json || 0)} />
        <Metric icon={Upload} label="Auto Confirm" value={privacy?.will_auto_confirm_imports ? 'on' : 'off'} />
      </section>

      <div className="grid min-w-0 gap-4 xl:grid-cols-[280px_minmax(0,1fr)_390px]">
        <aside className="min-w-0 space-y-4">
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Mode</h3>
            <div className="mt-3 grid gap-2">
              {tabs.map(({ key, label, icon: Icon }) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => setTab(key)}
                  className={`flex items-center justify-between gap-3 rounded-lg border px-3 py-2 text-left text-sm transition-colors ${
                    tab === key ? 'border-accent bg-accent-soft text-accent' : 'border-line bg-surface-field hover:border-accent'
                  }`}
                >
                  <span className="inline-flex items-center gap-2">
                    <Icon size={15} />
                    {label}
                  </span>
                  <ArrowRight size={14} />
                </button>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Scope</h3>
            <div className="mt-3 space-y-3">
              <label className="block text-xs font-medium text-muted">
                Profile
                <input
                  value={profileId}
                  onChange={(event) => setProfileId(event.target.value)}
                  className="mt-1 w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm text-foreground"
                />
              </label>
              <label className="block text-xs font-medium text-muted">
                Goal
                <select
                  value={activeGoal?.goal_id || ''}
                  onChange={(event) => {
                    const next = goals.find((goal) => goal.goal_id === event.target.value) || null;
                    setActiveGoal(next);
                    if (next) setProfileId(next.profile_id || 'default');
                  }}
                  className="mt-1 w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm text-foreground"
                >
                  <option value="">Default profile</option>
                  {goals.map((goal) => (
                    <option key={goal.goal_id} value={goal.goal_id}>{goal.title}</option>
                  ))}
                </select>
              </label>
              <label className="flex items-center justify-between gap-3 rounded-lg border border-line bg-surface-field px-3 py-2 text-sm">
                <span>Confirmed only</span>
                <input type="checkbox" checked={confirmedOnly} onChange={(event) => setConfirmedOnly(event.target.checked)} />
              </label>
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Filters</h3>
            <div className="mt-3 space-y-3">
              <FilterInput label="Module" value={moduleFilter} onChange={setModuleFilter} placeholder="Fixed Income" />
              <FilterInput label="Topic" value={topicFilter} onChange={setTopicFilter} placeholder="duration" />
              <FilterInput label="Asset Type" value={assetTypeFilter} onChange={setAssetTypeFilter} placeholder="formula" />
            </div>
          </section>
        </aside>

        <main className="min-w-0 space-y-4">
          {tab === 'anki' && (
            <section className="rounded-lg border border-line bg-surface-raised p-4">
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div>
                  <h3 className="font-semibold">Anki Deck Exchange</h3>
                  <p className="mt-1 text-sm text-muted">Confirmed recall cards with OpenExam IDs, source refs, and validation status.</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  <select
                    value={ankiFormat}
                    onChange={(event) => setAnkiFormat(event.target.value as 'csv' | 'tsv')}
                    className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm"
                    aria-label="Anki export format"
                  >
                    <option value="csv">CSV</option>
                    <option value="tsv">TSV</option>
                  </select>
                  <button type="button" onClick={exportAnki} disabled={Boolean(working)} className="btn-primary inline-flex items-center gap-2">
                    {working === 'export-anki' ? <Loader2 size={15} className="animate-spin" /> : <Download size={15} />}
                    Export Anki
                  </button>
                </div>
              </div>
              <ImportPreviewPanel
                path={ankiImportPath}
                setPath={setAnkiImportPath}
                preview={ankiPreview}
                previewLabel="Preview Anki Import"
                commitLabel="Commit Draft Import"
                working={working}
                previewKey="preview-anki"
                commitKey="commit-anki"
                onPreview={previewAnki}
                onCommit={commitAnki}
              />
            </section>
          )}

          {tab === 'markdown' && (
            <section className="rounded-lg border border-line bg-surface-raised p-4">
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div>
                  <h3 className="font-semibold">Markdown / Obsidian Archive</h3>
                  <p className="mt-1 text-sm text-muted">ZIP archive with notes, frontmatter, goals, and local source references.</p>
                </div>
                <button type="button" onClick={exportMarkdown} disabled={Boolean(working)} className="btn-primary inline-flex items-center gap-2">
                  {working === 'export-markdown' ? <Loader2 size={15} className="animate-spin" /> : <Download size={15} />}
                  Export Markdown
                </button>
              </div>
              <ImportPreviewPanel
                path={markdownImportPath}
                setPath={setMarkdownImportPath}
                preview={markdownPreview}
                previewLabel="Preview Markdown Import"
                commitLabel="Commit Markdown Drafts"
                working={working}
                previewKey="preview-markdown"
                commitKey="commit-markdown"
                onPreview={previewMarkdown}
                onCommit={commitMarkdown}
              />
            </section>
          )}

          {tab === 'calendar' && (
            <section className="rounded-lg border border-line bg-surface-raised p-4">
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div>
                  <h3 className="font-semibold">Study Calendar Export</h3>
                  <p className="mt-1 text-sm text-muted">
                    {todayPlan ? `${todayPlan.blocks.length} study blocks from ${todayPlan.plan_date}` : 'Study plan blocks export as local .ics events.'}
                  </p>
                </div>
                <button type="button" onClick={exportCalendar} disabled={Boolean(working)} className="btn-primary inline-flex items-center gap-2">
                  {working === 'export-calendar' ? <Loader2 size={15} className="animate-spin" /> : <CalendarCheck2 size={15} />}
                  Export Calendar
                </button>
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <FilterInput label="Plan ID" value={planId} onChange={setPlanId} placeholder={todayPlan?.plan_id || 'plan id'} />
                <FilterInput label="Start Datetime" value={startDatetime} onChange={setStartDatetime} type="datetime-local" />
                <FilterInput label="Timezone" value={timezone} onChange={setTimezone} placeholder="UTC" />
                <label className="flex items-center justify-between gap-3 rounded-lg border border-line bg-surface-field px-3 py-2 text-sm">
                  <span>Include completed blocks</span>
                  <input type="checkbox" checked={includeCompleted} onChange={(event) => setIncludeCompleted(event.target.checked)} />
                </label>
              </div>
            </section>
          )}

          {tab === 'records' && (
            <section className="rounded-lg border border-line bg-surface-raised p-4">
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div>
                  <h3 className="font-semibold">Learning Record Export</h3>
                  <p className="mt-1 text-sm text-muted">Local xAPI-style JSON for study events, completed blocks, and source traceability.</p>
                </div>
                <button type="button" onClick={exportLearningRecords} disabled={Boolean(working)} className="btn-primary inline-flex items-center gap-2">
                  {working === 'export-records' ? <Loader2 size={15} className="animate-spin" /> : <FileText size={15} />}
                  Export Learning Records
                </button>
              </div>
            </section>
          )}

          <ExportPreview result={lastExport} />
        </main>

        <aside className="min-w-0 space-y-4">
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex items-center justify-between gap-3">
              <h3 className="font-semibold">Privacy Report</h3>
              <ShieldCheck size={16} className="text-success" />
            </div>
            <div className="mt-3 space-y-2 text-sm">
              <Fact label="Artifacts" value={String(privacy?.artifact_count ?? artifacts.length)} />
              <Fact label="Safe default" value={privacy?.safe_mode_default === false ? 'false' : 'true'} />
              <Fact label="Import auto-confirm" value={privacy?.will_auto_confirm_imports ? 'true' : 'false'} />
            </div>
            <div className="mt-3 flex flex-wrap gap-1.5">
              {(privacy?.redacted_fields || []).slice(0, 10).map((field: string) => (
                <span key={field} className="rounded border border-line bg-surface-field px-2 py-0.5 text-xs text-muted">
                  {field}
                </span>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex items-center justify-between gap-3">
              <h3 className="font-semibold">Artifact History</h3>
              <button type="button" onClick={refreshArtifacts} className="rounded border border-line bg-surface-field p-1.5 text-muted transition-colors hover:text-foreground" aria-label="Refresh artifacts">
                <RefreshCw size={14} />
              </button>
            </div>
            <div className="mt-3 space-y-3">
              {loading && artifacts.length === 0 ? (
                <div className="rounded-lg border border-line bg-surface-field p-4 text-sm text-muted">Loading artifacts...</div>
              ) : artifacts.length === 0 ? (
                <div className="rounded-lg border border-line bg-surface-field p-4 text-sm text-muted">No artifacts yet.</div>
              ) : artifacts.slice(0, 10).map((artifact) => (
                <article key={artifact.artifact_id} className="rounded-lg border border-line bg-surface-field p-3 text-sm">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-semibold">{labelize(artifact.artifact_type)}</p>
                      <p className="mt-1 max-w-[290px] truncate text-xs text-muted">{artifact.file_path}</p>
                    </div>
                    <span className="rounded border border-success-soft bg-success-soft px-2 py-0.5 text-xs font-semibold text-success">
                      safe
                    </span>
                  </div>
                  <div className="mt-2 grid grid-cols-2 gap-2 text-xs text-muted">
                    <span>{formatBytes(artifact.size_bytes)}</span>
                    <span className="text-right">{new Date(artifact.created_at).toLocaleDateString()}</span>
                  </div>
                  <div className="mt-2 flex flex-wrap gap-1">
                    {artifact.categories.slice(0, 4).map((category) => (
                      <span key={category} className="rounded border border-line px-1.5 py-0.5 text-[11px] text-muted">
                        {category}
                      </span>
                    ))}
                  </div>
                </article>
              ))}
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}

function Metric({ icon: Icon, label, value }: { icon: any; label: string; value: string }) {
  return (
    <div className="min-w-0 rounded-lg border border-line bg-surface-raised p-4">
      <div className="flex items-center justify-between gap-3">
        <Icon size={18} className="text-accent" />
        <span className="text-2xl font-bold">{value}</span>
      </div>
      <p className="mt-3 text-sm font-semibold">{label}</p>
    </div>
  );
}

function FilterInput({
  label,
  value,
  onChange,
  placeholder = '',
  type = 'text',
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: string;
}) {
  return (
    <label className="block min-w-0 text-xs font-medium text-muted">
      {label}
      <input
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="mt-1 w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm text-foreground placeholder:text-muted"
      />
    </label>
  );
}

function ImportPreviewPanel({
  path,
  setPath,
  preview,
  previewLabel,
  commitLabel,
  working,
  previewKey,
  commitKey,
  onPreview,
  onCommit,
}: {
  path: string;
  setPath: (path: string) => void;
  preview: InteropImportPreview | null;
  previewLabel: string;
  commitLabel: string;
  working: string;
  previewKey: string;
  commitKey: string;
  onPreview: () => void;
  onCommit: () => void;
}) {
  return (
    <div className="mt-4 min-w-0 rounded-lg border border-line bg-surface-field p-3">
      <div className="grid gap-3 lg:grid-cols-[minmax(0,1fr)_auto_auto] lg:items-end">
        <FilterInput label="Import File Path" value={path} onChange={setPath} placeholder=".system/memory/interop/exports/..." />
        <button type="button" onClick={onPreview} disabled={!path || Boolean(working)} className="btn-secondary inline-flex items-center justify-center gap-2">
          {working === previewKey ? <Loader2 size={15} className="animate-spin" /> : <FileUp size={15} />}
          {previewLabel}
        </button>
        <button type="button" onClick={onCommit} disabled={!preview || Boolean(working)} className="btn-primary inline-flex items-center justify-center gap-2">
          {working === commitKey ? <Loader2 size={15} className="animate-spin" /> : <Upload size={15} />}
          {commitLabel}
        </button>
      </div>
      {preview && (
        <div className="mt-3 grid gap-3 sm:grid-cols-4">
          <Fact label="Preview ID" value={preview.preview_id} />
          <Fact label="Detected" value={String(preview.detected_items)} />
          <Fact label="Duplicates" value={String(preview.duplicates)} />
          <Fact label="Auto Confirm" value={preview.will_auto_confirm ? 'true' : 'false'} />
        </div>
      )}
    </div>
  );
}

function Fact({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0 rounded-lg border border-line bg-surface-field px-3 py-2">
      <p className="text-[11px] uppercase tracking-normal text-muted">{label}</p>
      <p className="mt-1 break-words text-sm font-semibold">{value}</p>
    </div>
  );
}

function ExportPreview({ result }: { result: ExportResult | null }) {
  if (!result) {
    return (
      <section className="min-w-0 rounded-lg border border-line bg-surface-raised p-4 text-sm text-muted">
        Export preview is empty.
      </section>
    );
  }
  const payload = result.payload;
  const samples = payload.sample_rows || payload.sample_notes || payload.sample_events || payload.sample_statements || [];
  return (
    <section className="min-w-0 rounded-lg border border-line bg-surface-raised p-4">
      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div>
          <h3 className="font-semibold">Export Preview</h3>
          <p className="mt-1 text-sm text-muted">{result.kind}</p>
        </div>
        {result.artifact && (
          <span className="rounded border border-success-soft bg-success-soft px-2 py-1 text-xs font-semibold text-success">
            {labelize(result.artifact.artifact_type)}
          </span>
        )}
      </div>
      {result.artifact && (
        <div className="mt-3 grid gap-3 md:grid-cols-3">
          <Fact label="Artifact" value={result.artifact.artifact_id} />
          <Fact label="File" value={result.artifact.file_path} />
          <Fact label="Hash" value={result.artifact.content_hash.slice(0, 16)} />
        </div>
      )}
      <div className="mt-3 grid gap-3 md:grid-cols-3">
        <Fact label="Items" value={String(payload.item_count ?? payload.event_count ?? payload.statement_count ?? 0)} />
        <Fact label="Redactions" value={String(payload.redaction_report?.fields_removed_count ?? result.artifact?.redaction_report?.fields_removed_count ?? 0)} />
        <Fact label="Safe Mode" value={result.artifact?.safe_mode === false ? 'false' : 'true'} />
      </div>
      {samples.length > 0 && (
        <pre className="mt-3 max-h-72 max-w-full overflow-auto whitespace-pre-wrap break-words rounded-lg border border-line bg-surface-field p-3 text-xs leading-5 text-muted">
          {safeStringify(samples.slice(0, 5))}
        </pre>
      )}
    </section>
  );
}

function safeStringify(value: unknown) {
  return JSON.stringify(value, (key, nestedValue) => {
    if (forbiddenKeys.has(key)) return '[redacted]';
    return nestedValue;
  }, 2);
}

function labelize(value: string) {
  return value.replace(/[_-]+/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatBytes(bytes: number) {
  if (!bytes) return '0 B';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 102.4) / 10} KB`;
  return `${Math.round(bytes / 1024 / 102.4) / 10} MB`;
}

function defaultLocalStart() {
  const value = new Date();
  value.setHours(value.getHours() + 1, 0, 0, 0);
  const pad = (input: number) => String(input).padStart(2, '0');
  return `${value.getFullYear()}-${pad(value.getMonth() + 1)}-${pad(value.getDate())}T${pad(value.getHours())}:${pad(value.getMinutes())}`;
}
