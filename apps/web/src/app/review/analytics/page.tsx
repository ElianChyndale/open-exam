'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  BarChart3,
  BookOpenCheck,
  Brain,
  CalendarCheck2,
  Calculator,
  CheckCircle2,
  ClipboardCheck,
  Database,
  FileText,
  Gauge,
  GitBranch,
  Languages,
  LineChart,
  Loader2,
  Map,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  Target,
  TrendingUp,
} from 'lucide-react';

import {
  LearningAnalyticsRange,
  LearningAnalyticsSummary,
  learningAnalyticsApi,
} from '@/lib/api';

type AnalyticsData = {
  summary: LearningAnalyticsSummary;
  events: any[];
  calibration: any[];
  trends: any[];
  plan: Record<string, any>;
  resources: Record<string, any>;
  coverage: Record<string, any>;
  formulas: Record<string, any>;
  language: Record<string, any>;
};

const rangeOptions: Array<{ value: LearningAnalyticsRange; label: string }> = [
  { value: 'today', label: 'Today' },
  { value: '7d', label: '7 days' },
  { value: '30d', label: '30 days' },
  { value: 'all', label: 'All' },
];

const quickLinks = [
  { href: '/review/tutor', label: 'Tutor', icon: Sparkles },
  { href: '/review/search', label: 'Search', icon: Search },
  { href: '/review/knowledge-map', label: 'Map', icon: Map },
  { href: '/review/data', label: 'Data', icon: Database },
  { href: '/review/assessments', label: 'Assessments', icon: ClipboardCheck },
  { href: '/review/study-planner', label: 'Planner', icon: CalendarCheck2 },
  { href: '/review/mission-control', label: 'Mission', icon: Gauge },
  { href: '/review/coverage', label: 'Coverage', icon: BookOpenCheck },
  { href: '/review/formulas', label: 'Formula', icon: Calculator },
  { href: '/review/mock-retro', label: 'Mock', icon: GitBranch },
  { href: '/review/resources', label: 'Resources', icon: ShieldCheck },
  { href: '/language/review', label: 'Language', icon: Languages },
  { href: '/review/lab', label: 'Review', icon: Brain },
];

export default function LearningAnalyticsPage() {
  const [range, setRange] = useState<LearningAnalyticsRange>('30d');
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [busy, setBusy] = useState(true);
  const [recomputing, setRecomputing] = useState(false);
  const [error, setError] = useState('');

  const load = async (nextRange = range) => {
    setBusy(true);
    setError('');
    try {
      const [summary, events, calibration, trends, plan, resources, coverage, formulas, language] = await Promise.all([
        learningAnalyticsApi.summary('default', nextRange),
        learningAnalyticsApi.events('default', nextRange),
        learningAnalyticsApi.calibration('default', nextRange),
        learningAnalyticsApi.masteryTrends('default', nextRange),
        learningAnalyticsApi.planEffectiveness('default', nextRange),
        learningAnalyticsApi.resourceUsefulness('default', nextRange),
        learningAnalyticsApi.coverageMomentum('default', nextRange),
        learningAnalyticsApi.formulaOutcomes('default', nextRange),
        learningAnalyticsApi.languageOutcomes('default', nextRange),
      ]);
      setData({
        summary,
        events: events.events || [],
        calibration: calibration.records || [],
        trends: trends.records || [],
        plan,
        resources,
        coverage,
        formulas,
        language,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Learning analytics load failed');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    load(range).catch(() => undefined);
  }, []);

  const changeRange = (nextRange: LearningAnalyticsRange) => {
    setRange(nextRange);
    load(nextRange).catch(() => undefined);
  };

  const recompute = async () => {
    setRecomputing(true);
    setError('');
    try {
      await learningAnalyticsApi.recompute('default', range);
      await load(range);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Learning analytics recompute failed');
    } finally {
      setRecomputing(false);
    }
  };

  const cards = useMemo(() => {
    if (!data) return [];
    const calibration = data.summary.calibration || {};
    const plan = data.plan || {};
    const coverage = data.coverage || {};
    const formulas = data.formulas || {};
    const language = data.language || {};
    const resources = data.resources || {};
    const productionGap = pct(language.recognition_success_rate) - pct(language.production_success_rate);
    return [
      {
        label: 'Mastery Trend',
        value: titleCase(data.summary.overall?.mastery_trend || 'unknown'),
        meta: `${data.summary.overall?.event_count || 0} events`,
        icon: TrendingUp,
      },
      {
        label: 'Confidence Calibration',
        value: formatPct(calibration.average_calibration_error),
        meta: `${calibration.overconfidence_count || 0} over / ${calibration.underconfidence_count || 0} under`,
        icon: Gauge,
      },
      {
        label: 'Plan Adherence',
        value: formatPct(plan.block_completion_rate),
        meta: `${plan.completed_blocks || 0}/${plan.block_count || 0} blocks`,
        icon: CalendarCheck2,
      },
      {
        label: 'Coverage Momentum',
        value: String(coverage.coverage_gap_count || 0),
        meta: `${coverage.topic_count || 0} topics / ${coverage.covered || 0} covered`,
        icon: BookOpenCheck,
      },
      {
        label: 'Formula Weakness',
        value: String((formulas.ba_ii_plus_step_weakness_count || 0) + (formulas.variable_confusion_count || 0)),
        meta: `${formatPct(formulas.recall_success_rate)} recall`,
        icon: Calculator,
      },
      {
        label: 'Language Production Gap',
        value: `${Math.max(0, Math.round(productionGap))}%`,
        meta: `${language.production_attempts || 0} production attempts`,
        icon: Languages,
      },
      {
        label: 'Resource Usefulness',
        value: formatPct(resources.average_resource_usefulness),
        meta: `${resources.promoted_assets || 0} promoted / ${resources.reviewed_promoted_assets || 0} reviewed`,
        icon: ShieldCheck,
      },
    ];
  }, [data]);

  const subsystemCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const event of data?.events || []) counts[event.subsystem] = (counts[event.subsystem] || 0) + 1;
    return Object.entries(counts).sort((a, b) => b[1] - a[1]);
  }, [data]);

  const trendRows = useMemo(() => {
    return [...(data?.trends || [])]
      .sort((a, b) => (b.overconfidence_count || 0) - (a.overconfidence_count || 0) || (b.recall_attempts || 0) - (a.recall_attempts || 0))
      .slice(0, 8);
  }, [data]);

  const formulaRows = objectEntries(data?.formulas?.by_formula_family || {}).slice(0, 6);
  const lexicalRows = objectEntries(data?.language?.weakness_tags || {}).slice(0, 6);
  const resourceRows = [...(data?.resources?.resources || [])].slice(0, 6);
  const planRows = objectEntries(data?.plan?.block_completion_by_type || {});
  const gapRows = data?.summary?.mock_retro?.top_gap_types || [];

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <LineChart size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Learning Analytics</h2>
          </div>
          <p className="mt-1 text-sm text-muted">
            {data ? `${data.summary.profile_id} / ${new Date(data.summary.generated_at).toLocaleString()}` : 'Loading outcome intelligence'}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="grid grid-cols-4 gap-1 rounded-lg border border-line bg-surface-field p-1">
            {rangeOptions.map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => changeRange(option.value)}
                className={`rounded-md px-2 py-1.5 text-xs font-semibold transition-colors ${
                  range === option.value ? 'bg-accent-solid text-white' : 'text-muted hover:bg-surface-hover'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
          <button type="button" onClick={recompute} disabled={busy || recomputing} className="btn-primary inline-flex items-center gap-2">
            {recomputing ? <Loader2 size={15} className="animate-spin" /> : <RefreshCw size={15} />}
            Recompute
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="mb-4 flex items-start gap-2 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
        <ShieldCheck size={16} className="mt-0.5 shrink-0" />
        <span>Correct-only analytics: raw wrong outputs, wrong formulas, wrong reasoning, and rejected content are excluded from this view.</span>
      </div>

      {busy && !data ? (
        <div className="rounded-lg border border-line bg-surface-raised p-8 text-center text-sm text-muted">Loading Learning Analytics...</div>
      ) : data ? (
        <>
          <section className="mb-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-7">
            {cards.map(({ label, value, meta, icon: Icon }) => (
              <div key={label} className="rounded-lg border border-line bg-surface-raised p-4">
                <div className="flex items-center justify-between gap-3">
                  <Icon size={18} className="text-accent" />
                  <span className="text-xl font-bold">{value}</span>
                </div>
                <p className="mt-3 text-xs font-semibold text-muted">{label}</p>
                <p className="mt-1 text-xs text-muted">{meta}</p>
              </div>
            ))}
          </section>

          <div className="mb-4 grid gap-4 xl:grid-cols-[minmax(0,1.15fr)_minmax(320px,0.85fr)]">
            <section className="rounded-lg border border-line bg-surface-raised">
              <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-3">
                <h3 className="font-semibold">Recommended Strategy Adjustments</h3>
                <Target size={16} className="text-accent" />
              </div>
              <div className="divide-y divide-line">
                {data.summary.recommended_strategy_adjustments.map((action) => (
                  <Link key={action.action_id} href={action.href} className="flex items-start justify-between gap-4 p-4 transition-colors hover:bg-surface-hover">
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="rounded border border-accent-soft bg-accent-soft px-2 py-0.5 text-xs font-semibold text-accent">
                          P{action.priority}
                        </span>
                        <h4 className="font-semibold">{action.title}</h4>
                      </div>
                      {action.reason && <p className="mt-2 text-sm text-muted">{action.reason}</p>}
                    </div>
                    <ArrowRight size={16} className="mt-1 shrink-0 text-muted" />
                  </Link>
                ))}
              </div>
            </section>

            <section className="rounded-lg border border-line bg-surface-raised p-4">
              <h3 className="font-semibold">Subsystem Event Mix</h3>
              <div className="mt-3 space-y-3">
                {subsystemCounts.length ? subsystemCounts.map(([label, count]) => (
                  <BarRow key={label} label={subsystemLabel(label)} value={count} max={Math.max(...subsystemCounts.map((item) => item[1]), 1)} />
                )) : <p className="text-sm text-muted">No analytics events in range.</p>}
              </div>
            </section>
          </div>

          <div className="grid gap-4 xl:grid-cols-3">
            <Panel title="Topic Mastery Trends" icon={TrendingUp}>
              <div className="space-y-2">
                {trendRows.length ? trendRows.map((record) => (
                  <TrendRow key={record.record_id} record={record} />
                )) : <EmptyText text="No scoped mastery records yet." />}
              </div>
            </Panel>

            <Panel title="Plan Block Completion" icon={CalendarCheck2}>
              <div className="space-y-2">
                {planRows.length ? planRows.map(([type, counts]) => (
                  <CompletionRow key={type} label={blockTypeLabel(type)} counts={counts} />
                )) : <EmptyText text="No completed planner blocks yet." />}
              </div>
            </Panel>

            <Panel title="Transfer Gap Trend" icon={GitBranch}>
              <div className="space-y-2">
                {gapRows.length ? gapRows.map((gap: any) => (
                  <BarRow key={gap.gap_type} label={gap.gap_type || 'unknown'} value={gap.count || 0} max={Math.max(...gapRows.map((item: any) => item.count || 0), 1)} />
                )) : <EmptyText text="No open transfer gap events." />}
              </div>
            </Panel>

            <Panel title="Formula Weakness" icon={Calculator}>
              <div className="space-y-3">
                <MiniStats
                  items={[
                    ['Attempts', data.formulas.attempts || 0],
                    ['Recall', formatPct(data.formulas.recall_success_rate)],
                    ['BA II Plus', data.formulas.ba_ii_plus_step_weakness_count || 0],
                    ['Variables', data.formulas.variable_confusion_count || 0],
                  ]}
                />
                {formulaRows.length ? formulaRows.map(([family, stats]) => (
                  <BarRow key={family} label={family || 'unknown'} value={Math.round(pct(stats.success_rate))} max={100} suffix="%" />
                )) : <EmptyText text="No formula family outcome records." />}
              </div>
            </Panel>

            <Panel title="Lexical Weakness" icon={Languages}>
              <div className="space-y-3">
                <MiniStats
                  items={[
                    ['Attempts', data.language.attempts || 0],
                    ['Recognition', formatPct(data.language.recognition_success_rate)],
                    ['Production', formatPct(data.language.production_success_rate)],
                    ['Translation', data.language.translation_gap_count || 0],
                  ]}
                />
                {lexicalRows.length ? lexicalRows.map(([tag, count]) => (
                  <BarRow key={tag} label={tag} value={Number(count) || 0} max={Math.max(...lexicalRows.map((item) => Number(item[1]) || 0), 1)} />
                )) : <EmptyText text="No lexical weakness tags yet." />}
              </div>
            </Panel>

            <Panel title="Resource Usefulness" icon={ShieldCheck}>
              <div className="space-y-2">
                {resourceRows.length ? resourceRows.map((resource: any) => (
                  <div key={resource.resource_id} className="rounded-lg border border-line bg-surface-field p-3">
                    <div className="flex items-center justify-between gap-3">
                      <span className="truncate text-sm font-semibold">{resource.resource_id}</span>
                      <span className="text-sm font-semibold">{formatPct(resource.resource_usefulness_score)}</span>
                    </div>
                    <div className="mt-2 grid grid-cols-3 gap-2 text-xs text-muted">
                      <span>{resource.promoted_assets || 0} promoted</span>
                      <span>{resource.reviewed_promoted_assets || 0} reviewed</span>
                      <span>{formatPct(resource.average_recall_success)} recall</span>
                    </div>
                  </div>
                )) : <EmptyText text="No resource usefulness records yet." />}
              </div>
            </Panel>
          </div>

          <section className="mt-4 rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
              <div>
                <h3 className="font-semibold">Learning System Links</h3>
                <p className="mt-1 text-sm text-muted">{data.events.length} correct-only events in the selected range.</p>
              </div>
              <div className="flex flex-wrap gap-2">
                {quickLinks.map(({ href, label, icon: Icon }) => (
                  <Link key={href} href={href} className="btn-secondary inline-flex items-center gap-2">
                    <Icon size={14} />
                    {label}
                  </Link>
                ))}
              </div>
            </div>
          </section>
        </>
      ) : null}
    </div>
  );
}

function Panel({
  title,
  icon: Icon,
  children,
}: {
  title: string;
  icon: typeof BarChart3;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-lg border border-line bg-surface-raised">
      <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-3">
        <h3 className="font-semibold">{title}</h3>
        <Icon size={16} className="text-accent" />
      </div>
      <div className="p-4">{children}</div>
    </section>
  );
}

function TrendRow({ record }: { record: any }) {
  return (
    <div className="rounded-lg border border-line bg-surface-field p-3">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold">{record.scope_type}: {record.scope_id}</p>
          <p className="mt-1 text-xs text-muted">{record.recall_attempts || 0} attempts / {record.mastery_trend || 'unknown'}</p>
        </div>
        <span className="rounded border border-line bg-surface-raised px-2 py-0.5 text-xs font-semibold text-muted">
          {formatPct(record.calibration_error)}
        </span>
      </div>
      <div className="mt-2 grid grid-cols-4 gap-2 text-xs text-muted">
        <span>{record.recalled_count || 0} recalled</span>
        <span>{record.partial_count || 0} partial</span>
        <span>{record.forgot_count || 0} forgot</span>
        <span>{record.overconfidence_count || 0} over</span>
      </div>
    </div>
  );
}

function CompletionRow({ label, counts }: { label: string; counts: any }) {
  const total = Number(counts.total || 0);
  const completed = Number(counts.completed || 0);
  const skipped = Number(counts.skipped || 0);
  const blocked = Number(counts.blocked || 0);
  return (
    <div className="rounded-lg border border-line bg-surface-field p-3">
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm font-semibold">{label}</span>
        <span className="text-sm text-muted">{completed}/{total}</span>
      </div>
      <div className="mt-2 h-2 overflow-hidden rounded bg-surface-raised">
        <div className="h-full bg-success" style={{ width: `${percentWidth(completed, total)}%` }} />
      </div>
      <div className="mt-2 grid grid-cols-3 gap-2 text-xs text-muted">
        <span>{completed} done</span>
        <span>{skipped} skipped</span>
        <span>{blocked} blocked</span>
      </div>
    </div>
  );
}

function BarRow({ label, value, max, suffix = '' }: { label: string; value: number; max: number; suffix?: string }) {
  return (
    <div>
      <div className="mb-1 flex items-center justify-between gap-3 text-sm">
        <span className="truncate text-muted">{label}</span>
        <span className="font-semibold">{value}{suffix}</span>
      </div>
      <div className="h-2 overflow-hidden rounded bg-surface-field">
        <div className="h-full bg-accent-solid" style={{ width: `${percentWidth(value, max)}%` }} />
      </div>
    </div>
  );
}

function MiniStats({ items }: { items: Array<[string, string | number]> }) {
  return (
    <div className="grid grid-cols-2 gap-2">
      {items.map(([label, value]) => (
        <div key={label} className="rounded-lg border border-line bg-surface-field p-2">
          <p className="text-xs text-muted">{label}</p>
          <p className="mt-1 font-semibold">{value}</p>
        </div>
      ))}
    </div>
  );
}

function EmptyText({ text }: { text: string }) {
  return <p className="text-sm text-muted">{text}</p>;
}

function objectEntries(value: Record<string, any>) {
  return Object.entries(value || {}).sort((a, b) => {
    const aValue = typeof a[1] === 'number' ? a[1] : Number(a[1]?.attempts || a[1]?.count || 0);
    const bValue = typeof b[1] === 'number' ? b[1] : Number(b[1]?.attempts || b[1]?.count || 0);
    return bValue - aValue;
  });
}

function pct(value: any) {
  const number = Number(value || 0);
  return number <= 1 ? number * 100 : number;
}

function formatPct(value: any) {
  return `${Math.round(pct(value))}%`;
}

function percentWidth(value: number, max: number) {
  if (!max) return 0;
  return Math.min(100, Math.max(4, Math.round((value / max) * 100)));
}

function titleCase(value: string) {
  return value.replace(/_/g, ' ').replace(/\b\w/g, (match) => match.toUpperCase());
}

function subsystemLabel(value: string) {
  return titleCase(value || 'unknown');
}

function blockTypeLabel(value: string) {
  return titleCase(value || 'unknown');
}
