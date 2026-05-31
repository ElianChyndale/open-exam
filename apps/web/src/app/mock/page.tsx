'use client';

import { useEffect, useState } from 'react';
import { Clock3, FileUp, Pause, Play, Square } from 'lucide-react';
import { mockApi, MockRun } from '@/lib/api';
import { Badge, Button, EmptyState, Field, Metric, Sheet, Surface } from '@/components/ui/ui';

export default function MockCenter() {
  const [runs, setRuns] = useState<MockRun[]>([]);
  const [selected, setSelected] = useState<MockRun | null>(null);
  const [label, setLabel] = useState('CFA Level I timed mock');
  const [elapsed, setElapsed] = useState(0);

  const refresh = () => mockApi.listRuns().then((data) => {
    setRuns(data.runs);
    setSelected((current) => data.runs.find((run) => run.run_id === current?.run_id) ?? data.runs[0] ?? null);
  });
  useEffect(() => { refresh(); }, []);

  const start = async () => {
    const { run } = await mockApi.startRun({ session_label: label, total_minutes: 135, total_questions: 90 });
    setSelected(run);
    await refresh();
  };
  const transition = async (action: 'pause' | 'resume' | 'complete') => {
    if (!selected) return;
    const { run } = await mockApi.setRunState(selected.run_id, action, elapsed);
    setSelected(run);
    await refresh();
  };
  const importSample = async () => {
    const { run } = await mockApi.importResults({
      source_name: 'manual-score-entry',
      session_label: 'Imported mock result',
      total_questions: 2,
      answers: [{ question_id: 'manual-1', is_correct: true, topic: 'Ethics', los: 'ETH.I' }, { question_id: 'manual-2', is_correct: false, topic: 'Fixed Income', los: 'FI.Duration' }],
    });
    setSelected(run);
    await refresh();
  };

  return (
    <div className="mx-auto max-w-6xl space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="metric-label">Timed checkpoints + append-only results</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight">Mock center</h1>
          <p className="mt-2 text-sm text-muted">Run timed sessions, pause deliberately, inspect pacing, and import external scores.</p>
        </div>
        <Button variant="secondary" onClick={importSample}><FileUp size={15} /> Import external result</Button>
      </header>

      <div className="grid gap-4 lg:grid-cols-[19rem_minmax(0,1fr)]">
        <aside className="space-y-4">
          <Sheet title="Start timed mock">
            <div className="space-y-3">
              <Field value={label} onChange={(event) => setLabel(event.target.value)} aria-label="Mock run label" />
              <Button className="w-full" onClick={start}><Play size={15} /> Start 90-question run</Button>
            </div>
          </Sheet>
          <Sheet title="Run history">
            {runs.length === 0 ? <EmptyState title="No mock runs yet" /> : (
              <div className="space-y-2">
                {runs.map((run) => <button key={run.run_id} onClick={() => setSelected(run)} className="w-full rounded-xl border border-line p-3 text-left hover:bg-surface-hover/70"><p className="text-sm font-semibold">{run.session_label}</p><p className="mt-1 text-xs text-muted">{run.status} · {run.answered_count}/{run.total_questions}</p></button>)}
              </div>
            )}
          </Sheet>
        </aside>

        <section className="space-y-4">
          {!selected ? <EmptyState title="Start or import a mock run" detail="The timed workspace will show section pacing checkpoints here." /> : (
            <>
              <Surface className="space-y-4">
                <div className="flex flex-wrap items-center justify-between gap-3"><div><h2 className="font-semibold">{selected.session_label}</h2><p className="mt-1 text-xs text-muted">{selected.source_kind}</p></div><Badge tone={selected.status === 'completed' ? 'success' : selected.status === 'paused' ? 'warning' : 'accent'}>{selected.status}</Badge></div>
                <div className="grid gap-3 sm:grid-cols-3"><Metric label="Answered" value={`${selected.answered_count}/${selected.total_questions}`} /><Metric label="Correct" value={selected.correct_count} /><Metric label="Elapsed" value={`${Math.round(selected.elapsed_seconds / 60)}m`} /></div>
                <div className="flex flex-wrap gap-2">
                  <Field className="max-w-40" type="number" value={elapsed} onChange={(event) => setElapsed(Number(event.target.value))} aria-label="Elapsed seconds" />
                  {selected.status === 'active' ? <Button variant="secondary" onClick={() => transition('pause')}><Pause size={15} /> Pause</Button> : null}
                  {selected.status === 'paused' ? <Button onClick={() => transition('resume')}><Play size={15} /> Resume</Button> : null}
                  {selected.status !== 'completed' ? <Button variant="danger" onClick={() => transition('complete')}><Square size={14} /> Complete</Button> : null}
                </div>
              </Surface>
              <Sheet title="Pacing checkpoints">
                <div className="grid gap-2 sm:grid-cols-3">
                  {selected.checkpoints.map((checkpoint) => <div key={checkpoint.question_number} className="rounded-xl border border-line bg-surface-sunken/60 p-3"><Clock3 size={15} className="text-accent" /><p className="mt-2 text-sm font-semibold">Question {checkpoint.question_number}</p><p className="mt-1 text-xs text-muted">Target {Math.round(checkpoint.target_elapsed_seconds / 60)} minutes</p></div>)}
                </div>
              </Sheet>
            </>
          )}
        </section>
      </div>
    </div>
  );
}
