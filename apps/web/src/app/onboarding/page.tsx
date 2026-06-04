'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  BookOpenCheck,
  CalendarCheck2,
  CheckCircle2,
  ClipboardCheck,
  Database,
  Gauge,
  Languages,
  Loader2,
  PackageCheck,
  RefreshCw,
  Rocket,
  ShieldCheck,
  SlidersHorizontal,
} from 'lucide-react';

import {
  CoursePack,
  Day1Plan,
  GoalEnergyMode,
  GoalProfile,
  GoalType,
  OnboardingState,
  goalsApi,
  onboardingApi,
} from '@/lib/api';

const goalTypes: Array<{ value: GoalType; label: string; icon: any }> = [
  { value: 'exam', label: 'Exam', icon: ClipboardCheck },
  { value: 'language', label: 'Language', icon: Languages },
  { value: 'course', label: 'Course', icon: BookOpenCheck },
  { value: 'career', label: 'Career', icon: Rocket },
  { value: 'project', label: 'Project', icon: PackageCheck },
  { value: 'custom', label: 'Custom', icon: SlidersHorizontal },
];

const stepLabels: Record<string, string> = {
  choose_goal: 'Choose Goal',
  choose_course_pack: 'Course Pack',
  set_time_budget: 'Time Budget',
  import_syllabus_or_seed_demo: 'Scope',
  import_resources_or_files: 'Resources',
  import_dictionary_if_language: 'Dictionary',
  confirm_initial_assets: 'Confirm',
  generate_first_plan: 'Day-1 Plan',
  start_first_review_or_assessment: 'Review',
  backup_reminder: 'Backup',
};

export default function OnboardingPage() {
  const [packs, setPacks] = useState<CoursePack[]>([]);
  const [activeGoal, setActiveGoal] = useState<GoalProfile | null>(null);
  const [state, setState] = useState<OnboardingState | null>(null);
  const [day1, setDay1] = useState<Day1Plan | null>(null);
  const [goalType, setGoalType] = useState<GoalType>('exam');
  const [packId, setPackId] = useState('cfa_finance');
  const [title, setTitle] = useState('CFA Level I');
  const [targetDate, setTargetDate] = useState('');
  const [weeklyMinutes, setWeeklyMinutes] = useState(600);
  const [energyMode, setEnergyMode] = useState<GoalEnergyMode>('normal');
  const [enabledModules, setEnabledModules] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const selectedPack = useMemo(() => packs.find((pack) => pack.pack_id === packId) || packs[0], [packs, packId]);
  const readiness = state?.readiness_score || 0;
  const currentStep = state?.current_step || 'choose_goal';
  const completedSteps = state?.completed_steps || [];
  const skippedSteps = state?.skipped_steps || [];

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const [packPayload, goalPayload, onboarding] = await Promise.all([
        goalsApi.packs(),
        goalsApi.list(),
        onboardingApi.state(),
      ]);
      setPacks(packPayload.packs || []);
      setActiveGoal(goalPayload.active_goal);
      setState(onboarding);
      const firstPack = packPayload.packs?.find((pack) => pack.pack_id === packId) || packPayload.packs?.[0];
      if (firstPack && enabledModules.length === 0) {
        setEnabledModules(firstPack.default_modules || []);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Onboarding load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  useEffect(() => {
    if (!selectedPack) return;
    setEnabledModules(selectedPack.default_modules || []);
    if (selectedPack.pack_type === 'language') {
      setGoalType('language');
      if (!title || title === 'CFA Level I') setTitle(selectedPack.title);
      setWeeklyMinutes(Number(selectedPack.planner_defaults?.weekly_minutes || 210));
      setEnergyMode((selectedPack.planner_defaults?.default_energy_mode as GoalEnergyMode) || 'low');
    } else if (selectedPack.pack_type === 'exam') {
      setGoalType('exam');
      setWeeklyMinutes(Number(selectedPack.planner_defaults?.weekly_minutes || 600));
      setEnergyMode((selectedPack.planner_defaults?.default_energy_mode as GoalEnergyMode) || 'normal');
    }
  }, [selectedPack?.pack_id]);

  const toggleModule = (moduleName: string) => {
    setEnabledModules((current) =>
      current.includes(moduleName)
        ? current.filter((item) => item !== moduleName)
        : [...current, moduleName],
    );
  };

  const createGoal = async () => {
    setBusy(true);
    setError('');
    try {
      const created = await goalsApi.create({
        profile_id: 'default',
        title,
        goal_type: goalType,
        target_date: targetDate || null,
        weekly_minutes: weeklyMinutes,
        default_energy_mode: energyMode,
        enabled_modules: enabledModules,
        pack_id: packId,
      });
      const activated = await goalsApi.activate(created.goal.goal_id);
      setActiveGoal(activated.goal);
      setState(activated.onboarding);
      setDay1(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Goal creation failed');
    } finally {
      setBusy(false);
    }
  };

  const generatePlan = async () => {
    setBusy(true);
    setError('');
    try {
      const plan = await onboardingApi.generateDay1Plan({
        profile_id: activeGoal?.profile_id || 'default',
        goal_id: activeGoal?.goal_id,
      });
      setDay1(plan);
      setState(plan.readiness);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Day-1 plan failed');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Rocket size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Onboarding</h2>
          </div>
          <p className="mt-1 text-sm text-muted">
            {activeGoal ? `${activeGoal.title} / ${state?.readiness_status || 'loading'}` : 'Choose a goal profile'}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/review/goals" className="btn-secondary inline-flex items-center gap-2">
            <Gauge size={14} />
            Goals
          </Link>
          <Link href="/review/mission-control" className="btn-secondary inline-flex items-center gap-2">
            <ShieldCheck size={14} />
            Mission
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

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_380px]">
        <main className="space-y-4">
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex items-center justify-between gap-3">
              <h3 className="font-semibold">Goal Type</h3>
              <span className="text-xs font-semibold text-muted">{stepLabels[currentStep] || currentStep}</span>
            </div>
            <div className="mt-3 grid gap-2 sm:grid-cols-3 xl:grid-cols-6">
              {goalTypes.map(({ value, label, icon: Icon }) => (
                <button
                  key={value}
                  type="button"
                  onClick={() => setGoalType(value)}
                  className={`inline-flex min-h-11 items-center justify-center gap-2 rounded-lg border px-3 text-sm font-semibold transition-colors ${
                    goalType === value ? 'border-accent bg-accent-soft text-accent' : 'border-line bg-surface-field text-muted hover:bg-surface-hover'
                  }`}
                >
                  <Icon size={15} />
                  {label}
                </button>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex items-center gap-2">
              <PackageCheck size={18} className="text-accent" />
              <h3 className="font-semibold">Course Pack</h3>
            </div>
            <div className="mt-3 grid gap-3 lg:grid-cols-2">
              {packs.map((pack) => (
                <button
                  key={pack.pack_id}
                  type="button"
                  onClick={() => setPackId(pack.pack_id)}
                  className={`rounded-lg border p-4 text-left transition-colors ${
                    packId === pack.pack_id ? 'border-accent bg-accent-soft' : 'border-line bg-surface-field hover:bg-surface-hover'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-semibold">{pack.title}</p>
                      <p className="mt-2 text-sm leading-5 text-muted">{pack.description}</p>
                    </div>
                    <span className="rounded border border-line bg-surface-raised px-2 py-0.5 text-xs font-semibold text-muted">
                      {pack.pack_type}
                    </span>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-1">
                    {pack.default_modules.slice(0, 5).map((moduleName) => (
                      <span key={moduleName} className="rounded border border-line bg-surface-raised px-2 py-0.5 text-xs text-muted">
                        {moduleName}
                      </span>
                    ))}
                  </div>
                </button>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="grid gap-3 lg:grid-cols-3">
              <label className="text-xs font-semibold text-muted lg:col-span-3">
                Goal title
                <input
                  value={title}
                  onChange={(event) => setTitle(event.target.value)}
                  className="mt-2 w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm text-foreground"
                />
              </label>
              <label className="text-xs font-semibold text-muted">
                Target date
                <input
                  type="date"
                  value={targetDate}
                  onChange={(event) => setTargetDate(event.target.value)}
                  className="mt-2 w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm text-foreground"
                />
              </label>
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
              <p className="text-xs font-semibold text-muted">Enabled modules</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {(selectedPack?.default_modules || enabledModules).map((moduleName) => (
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

            <button type="button" onClick={createGoal} disabled={busy || !title.trim()} className="btn-primary mt-4 inline-flex items-center gap-2">
              {busy ? <Loader2 size={15} className="animate-spin" /> : <Rocket size={15} />}
              Create and activate goal
            </button>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <h3 className="font-semibold">Day-1 Plan</h3>
                <p className="mt-1 text-sm text-muted">{day1 ? `${day1.blocks.length} blocks generated` : 'Generate after setting the active goal'}</p>
              </div>
              <button type="button" onClick={generatePlan} disabled={busy || !activeGoal} className="btn-primary inline-flex items-center gap-2">
                {busy ? <Loader2 size={15} className="animate-spin" /> : <CalendarCheck2 size={15} />}
                Generate Day-1 plan
              </button>
            </div>
            <div className="mt-3 grid gap-2 md:grid-cols-2">
              {(day1?.blocks || []).map((block) => (
                <Link key={block.block_id} href={block.launch_route} className="rounded-lg border border-line bg-surface-field p-3 transition-colors hover:bg-surface-hover">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <span className="rounded border border-accent-soft bg-accent-soft px-2 py-0.5 text-xs font-semibold text-accent">
                        {block.block_type.replace(/_/g, ' ')}
                      </span>
                      <p className="mt-2 font-semibold">{block.title}</p>
                      <p className="mt-1 text-sm leading-5 text-muted">{block.description}</p>
                    </div>
                    <ArrowRight size={15} className="mt-1 shrink-0 text-muted" />
                  </div>
                </Link>
              ))}
              {!day1 && <p className="rounded-lg border border-line bg-surface-field p-3 text-sm text-muted">No Day-1 plan generated yet.</p>}
            </div>
          </section>
        </main>

        <aside className="space-y-4">
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex items-center justify-between gap-3">
              <h3 className="font-semibold">Readiness</h3>
              <span className="text-2xl font-bold">{Math.round(readiness * 100)}</span>
            </div>
            <div className="mt-3 h-2 rounded-full bg-surface-field">
              <div className="h-2 rounded-full bg-accent-solid" style={{ width: `${Math.round(readiness * 100)}%` }} />
            </div>
            <p className="mt-2 text-sm font-semibold">{state?.readiness_status || 'loading'}</p>
            <div className="mt-3 space-y-2">
              {(state?.blockers || []).map((blocker) => (
                <Link key={blocker.blocker_id} href={blocker.launch_route} className="block rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
                  <span className="font-semibold">{blocker.severity}</span>
                  <span className="mt-1 block leading-5">{blocker.message}</span>
                </Link>
              ))}
              {state && state.blockers.length === 0 && <p className="text-sm text-muted">No readiness blockers.</p>}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Progress</h3>
            <div className="mt-3 space-y-2">
              {Object.entries(stepLabels).map(([step, label]) => {
                const complete = completedSteps.includes(step);
                const skipped = skippedSteps.includes(step);
                const active = currentStep === step;
                return (
                  <div key={step} className={`flex items-center justify-between gap-3 rounded-lg border px-3 py-2 text-sm ${
                    active ? 'border-accent bg-accent-soft' : 'border-line bg-surface-field'
                  }`}>
                    <span>{label}</span>
                    <span className="text-xs font-semibold text-muted">{complete ? 'done' : skipped ? 'skipped' : active ? 'now' : 'open'}</span>
                  </div>
                );
              })}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Launch</h3>
            <div className="mt-3 grid grid-cols-2 gap-2">
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
              <Link href="/review/goals" className="btn-secondary inline-flex items-center gap-2">
                <Gauge size={14} />
                Goals
              </Link>
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}
