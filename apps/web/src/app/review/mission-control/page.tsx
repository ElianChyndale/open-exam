'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  BookOpenCheck,
  Brain,
  CalendarCheck2,
  Gauge,
  Languages,
  Loader2,
  RefreshCw,
  Rocket,
  ShieldCheck,
  Sparkles,
  Wrench,
} from 'lucide-react';

import { reviewLabApi } from '@/lib/api';

type MissionSummary = {
  profile_id: string;
  generated_at: string;
  review_lab: Record<string, any>;
  assets: Record<string, any>;
  formulas: Record<string, any>;
  coverage: Record<string, any>;
  mock_retro: Record<string, any>;
  resources: Record<string, any>;
  language: Record<string, any>;
  data_governance: Record<string, any>;
  tutor: Record<string, any>;
  active_goal: Record<string, any> | null;
  onboarding: Record<string, any>;
  goals: Record<string, any>;
  system_health: Record<string, any>;
  recommended_actions: Array<{ priority: number; action_id: string; title: string; href: string; reason: string }>;
};

const subsystemLinks = [
  { href: '/review/focus', label: 'Focus Session', icon: CalendarCheck2 },
  { href: '/onboarding', label: 'Onboarding', icon: Rocket },
  { href: '/review/goals', label: 'Goals', icon: Gauge },
  { href: '/review/study-planner', label: 'Study Planner', icon: CalendarCheck2 },
  { href: '/review/lab', label: 'Review Lab', icon: Brain },
  { href: '/review/tutor', label: 'Tutor Copilot', icon: Sparkles },
  { href: '/language/dictionaries', label: 'Dictionaries', icon: Languages },
  { href: '/review/tools', label: 'More Tools', icon: Wrench },
];

export default function MissionControlPage() {
  const [summary, setSummary] = useState<MissionSummary | null>(null);
  const [registry, setRegistry] = useState<any>(null);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  const [advancedOpen, setAdvancedOpen] = useState(false);

  const load = async () => {
    setBusy(true);
    setError('');
    try {
      const [mission, routeRegistry] = await Promise.all([
        reviewLabApi.getMissionControl(),
        reviewLabApi.getRouteRegistry(),
      ]);
      setSummary(mission as MissionSummary);
      setRegistry(routeRegistry);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Mission Control load failed');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const cards = useMemo(() => {
    if (!summary) return [];
    const coverageGaps =
      (summary.coverage.missing || 0) +
      (summary.coverage.partial || 0) +
      (summary.coverage.weak || 0) +
      (summary.coverage.stale || 0) +
      (summary.coverage.draft_only || 0);
    return [
      {
        title: 'Goal Readiness',
        value: Math.round(Number(summary.onboarding?.readiness_score || 0) * 100),
        meta: summary.active_goal?.title || summary.onboarding?.readiness_status || 'not started',
        href: summary.active_goal ? '/review/goals' : '/onboarding',
        icon: Gauge,
      },
      {
        title: 'Review Today',
        value: summary.review_lab.due_count || 0,
        meta: summary.review_lab.next_session_available ? 'ready' : 'empty',
        href: '/review/lab',
        icon: Brain,
      },
      {
        title: 'Coverage Gaps',
        value: coverageGaps,
        meta: `${summary.coverage.covered || 0} covered`,
        href: '/review/coverage',
        icon: BookOpenCheck,
      },
      {
        title: 'Language Review',
        value: summary.language.due_lexical_count || 0,
        meta: `${summary.language.draft_lexical_count || 0} drafts`,
        href: '/language/review',
        icon: Languages,
      },
      {
        title: 'Tutor',
        value: summary.tutor?.active_conversation_count || 0,
        meta: `${summary.tutor?.conversation_count || 0} conversations`,
        href: '/review/tutor',
        icon: Sparkles,
      },
    ];
  }, [summary]);

  const warnings = useMemo(() => {
    if (!summary) return [];
    const items = [];
    if (!summary.active_goal) {
      items.push({ title: 'No active goal', body: 'Create a goal profile before generating the first reliable Day-1 path.', href: '/onboarding' });
    }
    if (summary.onboarding?.blockers?.length) {
      const blocker = summary.onboarding.blockers[0];
      items.push({ title: 'Onboarding blocker', body: blocker.message || 'Goal setup has an unresolved readiness blocker.', href: blocker.launch_route || '/onboarding' });
    }
    const draftAssets = (summary.assets.draft || 0) + (summary.assets.needs_review || 0);
    if (draftAssets) {
      items.push({ title: 'Draft assets blocked', body: `${draftAssets} review assets need confirmation before Review Lab selection.`, href: '/review/assets' });
    }
    if ((summary.resources.low || 0) || (summary.resources.unscored || 0)) {
      items.push({ title: 'Resource quality gate', body: `${summary.resources.low || 0} low and ${summary.resources.unscored || 0} unscored resources need review.`, href: '/review/resources' });
    }
    if (summary.language.draft_lexical_count) {
      items.push({ title: 'Lexical confirmation needed', body: `${summary.language.draft_lexical_count} lexical assets are excluded until confirmed.`, href: '/language/dictionaries' });
    }
    if (summary.data_governance.backup_health === 'never_backed_up') {
      items.push({ title: 'No backup yet', body: 'Create a safe local backup before more learning state accumulates.', href: '/review/data' });
    }
    if (summary.system_health.test_status_hook !== 'runtime_green') {
      items.push({ title: 'Test health is validated outside runtime', body: summary.system_health.test_status_hook || 'not_runtime_evaluated', href: '/review/mission-control' });
    }
    return items;
  }, [summary]);

  const topRecommendations = useMemo(() => {
    if (!summary) return [];
    const focus = {
      priority: 1,
      action_id: 'start_focus_session',
      title: 'Start Focus Session',
      href: '/review/focus',
      reason: 'Run today as one guided task at a time using confirmed local learning signals.',
    };
    return [focus, ...summary.recommended_actions.filter((action) => action.action_id !== focus.action_id)].slice(0, 3);
  }, [summary]);

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <ShieldCheck size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Mission Control</h2>
          </div>
          <p className="mt-1 text-sm text-muted">
            {summary ? `${summary.profile_id} / ${new Date(summary.generated_at).toLocaleString()}` : 'Loading system state'}
          </p>
        </div>
        <button type="button" onClick={load} disabled={busy} className="btn-primary inline-flex items-center gap-2">
          {busy ? <Loader2 size={15} className="animate-spin" /> : <RefreshCw size={15} />}
          Refresh
        </button>
      </div>

      {error && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="mb-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        {cards.map(({ title, value, meta, href, icon: Icon }) => (
          <Link key={title} href={href} className="rounded-lg border border-line bg-surface-raised p-4 transition-colors hover:border-accent">
            <div className="flex items-center justify-between gap-3">
              <Icon size={18} className="text-accent" />
              <span className="text-2xl font-bold">{value}</span>
            </div>
            <p className="mt-3 text-sm font-semibold">{title}</p>
            <p className="mt-1 text-xs text-muted">{meta}</p>
          </Link>
        ))}
      </div>

      {busy && !summary ? (
        <div className="rounded-lg border border-line bg-surface-raised p-8 text-center text-sm text-muted">Loading Mission Control...</div>
      ) : (
        <div className="grid gap-4 xl:grid-cols-[minmax(0,1.1fr)_minmax(320px,0.9fr)]">
          <section className="space-y-4">
            <div className="rounded-lg border border-line bg-surface-raised">
              <div className="border-b border-line px-4 py-3">
                <h3 className="font-semibold">Top Recommendations</h3>
              </div>
              <div className="divide-y divide-line">
                {topRecommendations.map((action) => (
                  <Link key={action.action_id} href={action.href} className="flex items-start justify-between gap-4 p-4 transition-colors hover:bg-surface-hover">
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="rounded border border-accent-soft bg-accent-soft px-2 py-0.5 text-xs font-semibold text-accent">
                          P{action.priority}
                        </span>
                        <h4 className="font-semibold">{action.title}</h4>
                      </div>
                      <p className="mt-2 text-sm text-muted">{action.reason}</p>
                    </div>
                    <ArrowRight size={16} className="mt-1 shrink-0 text-muted" />
                  </Link>
                ))}
              </div>
            </div>

            <div className="rounded-lg border border-line bg-surface-raised p-4">
              <h3 className="font-semibold">Context Routes</h3>
              <div className="mt-3 grid gap-2 sm:grid-cols-2 xl:grid-cols-4">
                {subsystemLinks.map(({ href, label, icon: Icon }) => (
                  <Link key={href} href={href} className="btn-secondary inline-flex items-center gap-2">
                    <Icon size={14} />
                    {label}
                  </Link>
                ))}
              </div>
            </div>
          </section>

          <aside className="space-y-4">
            <div className="rounded-lg border border-line bg-surface-raised p-4">
              <h3 className="font-semibold">Warnings</h3>
              <div className="mt-3 space-y-3">
                {warnings.length === 0 ? (
                  <p className="text-sm text-muted">No blocking warnings.</p>
                ) : warnings.map((warning) => (
                  <Link key={warning.title} href={warning.href} className="block rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
                    <span className="font-semibold">{warning.title}</span>
                    <span className="mt-1 block leading-5">{warning.body}</span>
                  </Link>
                ))}
              </div>
            </div>

            <div className="rounded-lg border border-line bg-surface-raised p-4">
              <button
                type="button"
                onClick={() => setAdvancedOpen((current) => !current)}
                className="flex w-full items-center justify-between gap-3 text-left font-semibold"
              >
                <span>Advanced diagnostics</span>
                <Wrench size={15} className="text-muted" />
              </button>
              {advancedOpen && (
                <div className="mt-4 border-t border-line pt-4">
                  <h3 id="route-registry" className="font-semibold">Route Registry</h3>
                  <div className="mt-3 space-y-2 text-sm">
                    {(registry?.expected_api_routes || []).map((route: any) => (
                      <div key={route.path} className="flex items-center justify-between gap-3">
                        <span className="truncate text-muted">{route.path}</span>
                        <span className={`rounded border px-2 py-0.5 text-xs font-semibold ${
                          route.mounted ? 'border-success-soft bg-success-soft text-success' : 'border-danger-soft bg-danger-soft text-danger'
                        }`}>
                          {route.mounted ? 'mounted' : 'missing'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </aside>
        </div>
      )}
    </div>
  );
}
