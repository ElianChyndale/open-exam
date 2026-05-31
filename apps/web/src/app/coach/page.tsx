'use client';

import { useEffect, useState } from 'react';
import { Download, ShieldCheck, Sparkles } from 'lucide-react';
import { coachApi, CoachBrief, reportsApi, WeeklyReport } from '@/lib/api';
import { Alert, Badge, Button, EmptyState, Field, Sheet, Surface, TextArea } from '@/components/ui/ui';

export default function CoachPage() {
  const [briefs, setBriefs] = useState<CoachBrief[]>([]);
  const [report, setReport] = useState<WeeklyReport | null>(null);
  const [summary, setSummary] = useState('');
  const [sourceRefs, setSourceRefs] = useState('');
  const [error, setError] = useState('');

  const refresh = () => Promise.all([coachApi.briefs().then((data) => setBriefs(data.briefs)), reportsApi.weekly().then(setReport)]);
  useEffect(() => { refresh(); }, []);

  const addRetro = async () => {
    setError('');
    try {
      await coachApi.retro(summary, sourceRefs.split(',').map((item) => item.trim()).filter(Boolean));
      setSummary('');
      setSourceRefs('');
      await refresh();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Unable to validate retro.');
    }
  };

  return (
    <div className="mx-auto max-w-6xl space-y-5">
      <header>
        <p className="metric-label">Deterministic offline coach</p>
        <h1 className="mt-1 text-3xl font-semibold tracking-tight">Coach center</h1>
        <p className="mt-2 text-sm text-muted">Turn evidence into a short next action. Unsupported claims never enter the brief stream.</p>
      </header>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_22rem]">
        <section className="space-y-3">
          {error ? <Alert tone="danger">{error}</Alert> : null}
          {briefs.length === 0 ? <EmptyState title="No validated briefs yet" detail="Add a session retro with at least one evidence reference." /> : null}
          {briefs.map((brief) => (
            <Surface key={brief.brief_id} className="space-y-3">
              <div className="flex flex-wrap items-center gap-2">
                <Badge tone="success">Validated</Badge><Badge>{brief.kind}</Badge>
              </div>
              <h2 className="font-semibold">{brief.summary}</h2>
              <ul className="space-y-1 text-sm text-muted">{brief.recommendations.map((item) => <li key={item}>- {item}</li>)}</ul>
              <p className="text-xs text-muted">Evidence: {brief.evidence_refs.join(', ')}</p>
            </Surface>
          ))}
        </section>

        <aside className="space-y-4">
          <Sheet title="Capture session retro">
            <div className="space-y-3">
              <TextArea value={summary} onChange={(event) => setSummary(event.target.value)} placeholder="What changed your next study decision?" rows={4} />
              <Field value={sourceRefs} onChange={(event) => setSourceRefs(event.target.value)} placeholder="Evidence refs, comma separated" />
              <Button className="w-full" onClick={addRetro}><Sparkles size={15} /> Validate brief</Button>
            </div>
          </Sheet>
          <Surface className="space-y-3">
            <div className="flex items-center gap-2"><ShieldCheck size={16} className="text-success" /><h2 className="text-sm font-semibold">Weekly report</h2></div>
            <p className="text-xs text-muted">{report?.attempt_count ?? 0} attempts · {report?.mock_run_count ?? 0} mock runs · {report?.coach_brief_count ?? 0} briefs</p>
            <a className="button-secondary w-full" href={reportsApi.weeklyMarkdownUrl()}><Download size={15} /> Export markdown</a>
          </Surface>
        </aside>
      </div>
    </div>
  );
}
