'use client';

import { useEffect, useState } from 'react';
import { Battery, Bell, Check, Clock, RotateCcw, Sparkles, Target, Zap } from 'lucide-react';
import { energyApi, notificationsApi, tasksApi, type DailyTask } from '@/lib/api';
import { Alert, Badge, Button, EmptyState, Metric, Select, Surface } from '@/components/ui/ui';

export default function TodayPage() {
  const [tasks, setTasks] = useState<DailyTask[]>([]);
  const [notifications, setNotifications] = useState<Array<{ notification_id: string; kind: string; title: string; detail: string }>>([]);
  const [energy, setEnergy] = useState(2);
  const [warnings, setWarnings] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = () => Promise.all([tasksApi.getToday(), notificationsApi.list()])
    .then(([taskData, notificationData]) => {
      setTasks(taskData.tasks);
      setNotifications(notificationData.notifications);
    }).finally(() => setLoading(false));

  useEffect(() => { refresh(); }, []);

  const updateStatus = (task: DailyTask, status: DailyTask['status']) =>
    tasksApi.setStatus(task.task_id, status).then(refresh);

  const completed = tasks.filter((task) => task.status === 'completed').length;
  const minutes = tasks.filter((task) => task.status === 'pending').reduce((total, task) => total + task.estimated_minutes, 0);

  return (
    <div className="mx-auto max-w-6xl space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="metric-label">Daily execution</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight">Today</h1>
          <p className="mt-2 text-sm text-muted">Turn evidence into the next small set of deliberate actions.</p>
        </div>
        <a className="button-secondary" href="/settings">Adjust study settings</a>
      </header>

      <div className="grid gap-3 sm:grid-cols-3">
        <Surface><Metric label="Open work" value={`${minutes} min`} detail={`${tasks.length - completed} tasks remaining`} /></Surface>
        <Surface><Metric label="Completed" value={`${completed}/${tasks.length}`} detail="Persisted to your local ledger" /></Surface>
        <Surface><Metric label="Notifications" value={notifications.length} detail="Due work and deadlines" /></Surface>
      </div>

      <Surface className="grid gap-4 md:grid-cols-[1fr_auto] md:items-end">
        <div>
          <div className="mb-2 flex items-center gap-2"><Battery size={16} className="text-accent" /><h2 className="text-sm font-semibold">Readiness check-in</h2></div>
          <p className="text-xs text-muted">Update the plan when your actual energy differs from the schedule.</p>
          <label className="mt-3 block max-w-xs space-y-1 text-xs font-semibold text-muted">
            <span>Current energy</span>
            <Select value={energy} onChange={(event) => setEnergy(Number(event.target.value))}>
              <option value={0}>Depleted</option><option value={1}>Low</option><option value={2}>Moderate</option><option value={3}>High</option><option value={4}>Peak</option>
            </Select>
          </label>
        </div>
        <Button onClick={() => energyApi.checkIn({ energy_level: energy, mental_clarity: 6, physical_fatigue: 4, motivation: 6 }).then((result: any) => { setWarnings(result.warnings || []); return refresh(); })}>
          <RotateCcw size={15} /> Refit today
        </Button>
      </Surface>

      {warnings.map((warning) => <Alert key={warning}>{warning}</Alert>)}

      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2"><Target size={16} className="text-accent" /><h2 className="text-sm font-semibold">Execution queue</h2></div>
          <Badge tone="accent">Local event ledger</Badge>
        </div>
        {loading ? <Surface className="animate-pulse text-sm text-muted">Loading today plan...</Surface> : null}
        {!loading && tasks.length === 0 ? <EmptyState title="Nothing planned yet" detail="Add a focus topic or capture a mistake to build the next queue." /> : null}
        {tasks.map((task) => (
          <Surface key={task.task_id} className="flex flex-wrap items-center gap-3">
            <div className="grid h-9 w-9 place-items-center rounded-xl bg-accent/10 text-accent"><Sparkles size={16} /></div>
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2"><h3 className="text-sm font-semibold">{task.title}</h3><Badge tone={task.status === 'completed' ? 'success' : 'neutral'}>{task.status}</Badge></div>
              <p className="mt-1 text-xs text-muted">{task.topic} · {task.estimated_minutes} min · {task.energy_fit} energy</p>
            </div>
            <div className="flex gap-1">
              <Button variant="ghost" onClick={() => updateStatus(task, 'deferred')}>Defer</Button>
              <Button variant="secondary" onClick={() => updateStatus(task, 'skipped')}>Skip</Button>
              <Button onClick={() => updateStatus(task, 'completed')}><Check size={15} /> Complete</Button>
            </div>
          </Surface>
        ))}
      </section>

      {notifications.length ? (
        <Surface>
          <div className="mb-3 flex items-center gap-2"><Bell size={15} className="text-accent" /><h2 className="text-sm font-semibold">Notification center</h2></div>
          <div className="space-y-2">{notifications.map((item) => <p key={item.notification_id} className="text-xs text-muted"><span className="font-semibold text-ink">{item.title}</span> · {item.detail}</p>)}</div>
        </Surface>
      ) : null}

      <Surface className="flex flex-wrap gap-2">
        <a className="button-secondary" href="/review"><Zap size={15} /> Start retrieval</a>
        <a className="button-secondary" href="/practice">Open practice</a>
        <a className="button-secondary" href="/map">Browse curriculum</a>
      </Surface>
    </div>
  );
}
