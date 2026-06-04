'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  Archive,
  ArrowRight,
  CalendarCheck2,
  CheckCircle2,
  Database,
  Gauge,
  Languages,
  Loader2,
  PackageCheck,
  RefreshCw,
  Rocket,
  Save,
  ShieldCheck,
  Sparkles,
  Wrench,
} from 'lucide-react';

import {
  CoursePack,
  GoalEnergyMode,
  GoalProfile,
  OnboardingState,
  goalsApi,
  onboardingApi,
} from '@/lib/api';

export default function GoalsPage() {
  const [packs, setPacks] = useState<CoursePack[]>([]);
  const [goals, setGoals] = useState<GoalProfile[]>([]);
  const [activeGoal, setActiveGoal] = useState<GoalProfile | null>(null);
  const [state, setState] = useState<OnboardingState | null>(null);
  const [selectedGoalId, setSelectedGoalId] = useState('');
  const [weeklyMinutes, setWeeklyMinutes] = useState(300);
  const [energyMode, setEnergyMode] = useState<GoalEnergyMode>('normal');
  const [enabledModules, setEnabledModules] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const selectedGoal = useMemo(
    () => goals.find((goal) => goal.goal_id === selectedGoalId) || activeGoal || goals[0] || null,
    [goals, selectedGoalId, activeGoal],
  );
  const selectedPack = useMemo(
    () => packs.find((pack) => pack.pack_id === selectedGoal?.pack_id) || null,
    [packs, selectedGoal],
  );

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const [packPayload, goalPayload, onboarding] = await Promise.all([
        goalsApi.packs(),
        goalsApi.list({ include_archived: true }),
        onboardingApi.state(),
      ]);
      setPacks(packPayload.packs || []);
      setGoals(goalPayload.goals || []);
      setActiveGoal(goalPayload.active_goal);
      setState(onboarding);
      const goal = goalPayload.active_goal || goalPayload.goals?.[0] || null;
      if (goal) {
        setSelectedGoalId(goal.goal_id);
        setWeeklyMinutes(goal.weekly_minutes);
        setEnergyMode(goal.default_energy_mode);
        setEnabledModules(goal.enabled_modules || []);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Goals load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  useEffect(() => {
    if (!selectedGoal) return;
    setWeeklyMinutes(selectedGoal.weekly_minutes);
    setEnergyMode(selectedGoal.default_energy_mode);
    setEnabledModules(selectedGoal.enabled_modules || []);
  }, [selectedGoal?.goal_id]);

  const activate = async (goalId: string) => {
    setBusy(true);
    setError('');
    try {
      const payload = await goalsApi.activate(goalId);
      setActiveGoal(payload.goal);
      setState(payload.onboarding);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Activate failed');
    } finally {
      setBusy(false);
    }
  };

  const archive = async (goalId: string) => {
    setBusy(true);
    setError('');
    try {
      await goalsApi.archive(goalId);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Archive failed');
    } finally {
      setBusy(false);
    }
  };

  const save = async () => {
    if (!selectedGoal) return;
    setBusy(true);
    setError('');
    try {
      const payload = await goalsApi.patch(selectedGoal.goal_id, {
        weekly_minutes: weeklyMinutes,
        default_energy_mode: energyMode,
        enabled_modules: enabledModules,
      });
      setState(payload.onboarding);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Save failed');
    } finally {
      setBusy(false);
    }
  };

  const toggleModule = (moduleName: string) => {
    setEnabledModules((current) =>
      current.includes(moduleName)
        ? current.filter((item) => item !== moduleName)
        : [...current, moduleName],
    );
  };

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Gauge size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Goal Profiles</h2>
          </div>
          <p className="mt-1 text-sm text-muted">
            {activeGoal ? `${activeGoal.title} / ${state?.readiness_status || 'loading'}` : 'No active goal'}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/onboarding" className="btn-secondary inline-flex items-center gap-2">
            <Rocket size={14} />
            Onboarding
          </Link>
          <Link href="/review/mission-control" className="btn-secondary inline-flex items-center gap-2">
            <ShieldCheck size={14} />
            Mission
          </Link>
          <Link href="/review/tools" className="btn-secondary inline-flex items-center gap-2">
            <Wrench size={14} />
            Tools
          </Link>
          <button type="button" onClick={load} disabled={loading || busy} className="btn-primary inline-flex items-center gap-2">
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

      {!loading && goals.length === 0 && (
        <div className="mb-4 rounded-lg border border-warning-soft bg-warning-soft p-4 text-sm text-warning">
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="font-semibold">No goal profile exists</p>
              <p className="mt-1">Start onboarding to create a first active goal and Day-1 plan.</p>
            </div>
            <Link href="/onboarding" className="btn-primary inline-flex shrink-0 items-center gap-2">
              <ArrowRight size={14} />
              Start
            </Link>
          </div>
        </div>
      )}

      <div className="grid gap-4 xl:grid-cols-[360px_minmax(0,1fr)_340px]">
        <aside className="rounded-lg border border-line bg-surface-raised p-4">
          <h3 className="font-semibold">Profiles</h3>
          <div className="mt-3 space-y-2">
            {goals.map((goal) => (
              <button
                key={goal.goal_id}
                type="button"
                onClick={() => setSelectedGoalId(goal.goal_id)}
                className={`w-full rounded-lg border p-3 text-left transition-colors ${
                  selectedGoal?.goal_id === goal.goal_id ? 'border-accent bg-accent-soft' : 'border-line bg-surface-field hover:bg-surface-hover'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate font-semibold">{goal.title}</p>
                    <p className="mt-1 text-xs text-muted">{goal.goal_type} / {goal.status}</p>
                  </div>
                  {goal.status === 'active' && <CheckCircle2 size={16} className="shrink-0 text-accent" />}
                </div>
              </button>
            ))}
            {!goals.length && <p className="text-sm text-muted">No profiles.</p>}
          </div>
        </aside>

        <main className="space-y-4">
          {selectedGoal ? (
            <>
              <section className="rounded-lg border border-line bg-surface-raised p-4">
                <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded border border-accent-soft bg-accent-soft px-2 py-0.5 text-xs font-semibold text-accent">
                        {selectedGoal.goal_type}
                      </span>
                      <span className="rounded border border-line bg-surface-field px-2 py-0.5 text-xs font-semibold text-muted">
                        {selectedGoal.status}
                      </span>
                    </div>
                    <h3 className="mt-3 text-lg font-bold">{selectedGoal.title}</h3>
                    <p className="mt-1 text-sm text-muted">
                      {selectedGoal.target_exam || selectedGoal.target_language || selectedPack?.title || 'Custom target'}
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {selectedGoal.status !== 'active' && (
                      <button type="button" onClick={() => activate(selectedGoal.goal_id)} disabled={busy} className="btn-primary inline-flex items-center gap-2">
                        <CheckCircle2 size={14} />
                        Activate
                      </button>
                    )}
                    <button type="button" onClick={() => archive(selectedGoal.goal_id)} disabled={busy} className="btn-secondary inline-flex items-center gap-2">
                      <Archive size={14} />
                      Archive
                    </button>
                  </div>
                </div>
              </section>

              <section className="rounded-lg border border-line bg-surface-raised p-4">
                <div className="grid gap-3 md:grid-cols-2">
                  <label className="text-xs font-semibold text-muted">
                    Weekly minutes
                    <input
                      type="number"
                      min={30}
                      max={6000}
                      value={weeklyMinutes}
                      onChange={(event) => setWeeklyMinutes(Number(event.target.value))}
                      className="mt-2 w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm text-foreground"
                    />
                  </label>
                  <label className="text-xs font-semibold text-muted">
                    Energy mode
                    <select
                      value={energyMode}
                      onChange={(event) => setEnergyMode(event.target.value as GoalEnergyMode)}
                      className="mt-2 w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm text-foreground"
                    >
                      <option value="low">Low</option>
                      <option value="normal">Normal</option>
                      <option value="high">High</option>
                    </select>
                  </label>
                </div>
                <div className="mt-4">
                  <p className="text-xs font-semibold text-muted">Modules</p>
                  <div className="mt-2 flex flex-wrap gap-2">
                    {(selectedPack?.default_modules || selectedGoal.enabled_modules).map((moduleName) => (
                      <button
                        key={moduleName}
                        type="button"
                        onClick={() => toggleModule(moduleName)}
                        className={`inline-flex items-center gap-2 rounded-lg border px-3 py-2 text-xs font-semibold transition-colors ${
                          enabledModules.includes(moduleName) ? 'border-accent bg-accent-soft text-accent' : 'border-line bg-surface-field text-muted'
                        }`}
                      >
                        {enabledModules.includes(moduleName) ? <CheckCircle2 size={14} /> : <span className="h-3.5 w-3.5 rounded border border-line" />}
                        {moduleName}
                      </button>
                    ))}
                  </div>
                </div>
                <button type="button" onClick={save} disabled={busy} className="btn-primary mt-4 inline-flex items-center gap-2">
                  {busy ? <Loader2 size={15} className="animate-spin" /> : <Save size={15} />}
                  Save settings
                </button>
              </section>

              {selectedPack && (
                <section className="rounded-lg border border-line bg-surface-raised p-4">
                  <div className="flex items-center gap-2">
                    <PackageCheck size={18} className="text-accent" />
                    <h3 className="font-semibold">{selectedPack.title}</h3>
                  </div>
                  <p className="mt-2 text-sm leading-5 text-muted">{selectedPack.description}</p>
                  <div className="mt-3 grid gap-3 md:grid-cols-2">
                    <div className="rounded-lg border border-line bg-surface-field p-3">
                      <p className="text-xs font-semibold text-muted">Suggested imports</p>
                      <div className="mt-2 space-y-2">
                        {selectedPack.suggested_imports.map((item) => (
                          <p key={item.label} className="text-sm">{item.label}</p>
                        ))}
                      </div>
                    </div>
                    <div className="rounded-lg border border-line bg-surface-field p-3">
                      <p className="text-xs font-semibold text-muted">Quality gate</p>
                      <p className="mt-2 text-sm">{selectedPack.quality_gate_policy.manual_confirm_required ? 'Manual confirmation required' : 'Manual confirmation optional'}</p>
                    </div>
                  </div>
                </section>
              )}
            </>
          ) : (
            <section className="rounded-lg border border-line bg-surface-raised p-8 text-center text-sm text-muted">
              Select or create a goal profile.
            </section>
          )}
        </main>

        <aside className="space-y-4">
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex items-center justify-between gap-3">
              <h3 className="font-semibold">Onboarding</h3>
              <span className="text-2xl font-bold">{Math.round((state?.readiness_score || 0) * 100)}</span>
            </div>
            <div className="mt-3 h-2 rounded-full bg-surface-field">
              <div className="h-2 rounded-full bg-accent-solid" style={{ width: `${Math.round((state?.readiness_score || 0) * 100)}%` }} />
            </div>
            <p className="mt-2 text-sm font-semibold">{state?.readiness_status || 'loading'}</p>
            <div className="mt-3 space-y-2">
              {(state?.blockers || []).slice(0, 4).map((blocker) => (
                <Link key={blocker.blocker_id} href={blocker.launch_route} className="block rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
                  {blocker.message}
                </Link>
              ))}
              {state && state.blockers.length === 0 && <p className="text-sm text-muted">No readiness blockers.</p>}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Subsystems</h3>
            <div className="mt-3 grid grid-cols-2 gap-2">
              <Link href="/onboarding" className="btn-secondary inline-flex items-center gap-2">
                <Rocket size={14} />
                Onboard
              </Link>
              <Link href="/review/mission-control" className="btn-secondary inline-flex items-center gap-2">
                <ShieldCheck size={14} />
                Mission
              </Link>
              <Link href="/review/study-planner" className="btn-secondary inline-flex items-center gap-2">
                <CalendarCheck2 size={14} />
                Planner
              </Link>
              <Link href="/review/data" className="btn-secondary inline-flex items-center gap-2">
                <Database size={14} />
                Backup
              </Link>
              <Link href="/review/tools" className="btn-secondary inline-flex items-center gap-2">
                <Wrench size={14} />
                Tools
              </Link>
              <Link href="/review/tutor" className="btn-secondary inline-flex items-center gap-2">
                <Sparkles size={14} />
                Tutor
              </Link>
              <Link href="/language/dictionaries" className="btn-secondary inline-flex items-center gap-2">
                <Languages size={14} />
                Dictionary
              </Link>
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}
