'use client';

import { useEffect, useState } from 'react';
import { AlertTriangle, Building2, Download, Plus, UserRoundCheck, Users } from 'lucide-react';
import { institutionApi, Intervention, transferApi, type DeliveryProof } from '@/lib/api';
import { Badge, Button, EmptyState, Field, Metric, Sheet, Surface } from '@/components/ui/ui';

interface Cohort {
  cohort_id: string;
  cohort_name: string;
  exam_target: string;
  exam_date: string;
  learner_ids: string[];
}

export default function InstitutionConsole() {
  const [cohorts, setCohorts] = useState<Cohort[]>([]);
  const [interventions, setInterventions] = useState<Intervention[]>([]);
  const [proof, setProof] = useState<DeliveryProof | null>(null);
  const [cohortName, setCohortName] = useState('');
  const [learnerIds, setLearnerIds] = useState('');
  const [learnerId, setLearnerId] = useState('');
  const [reason, setReason] = useState('');

  const refresh = () => Promise.all([
    institutionApi.listCohorts().then((data: any) => setCohorts(data.cohorts ?? [])),
    institutionApi.listInterventions().then((data) => setInterventions(data.interventions)),
    institutionApi.deliveryProof().then(setProof),
  ]);
  useEffect(() => { refresh(); }, []);

  const createCohort = async () => {
    await institutionApi.createCohort({ institution_id: 'local-institution', cohort_name: cohortName, learner_ids: learnerIds.split(',').map((item) => item.trim()).filter(Boolean) });
    setCohortName(''); setLearnerIds(''); await refresh();
  };
  const createIntervention = async () => {
    await institutionApi.createIntervention({ learner_id: learnerId, reason });
    setLearnerId(''); setReason(''); await refresh();
  };

  return (
    <div className="mx-auto max-w-6xl space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="metric-label">Optional tenant workspace</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight">Institution console</h1>
          <p className="mt-2 text-sm text-muted">Cohorts, intervention queues, inactivity follow-up, and delivery-proof exports.</p>
        </div>
        <a className="button-secondary" href={transferApi.exportUrl()}><Download size={15} /> Export local bundle</a>
      </header>

      <section className="grid gap-3 sm:grid-cols-3">
        <Surface><Metric label="Cohorts" value={proof?.cohort_count ?? 0} /></Surface>
        <Surface><Metric label="Open interventions" value={proof?.intervention_count ?? 0} /></Surface>
        <Surface><Metric label="Weekly attempts" value={proof?.weekly_report.attempt_count ?? 0} /></Surface>
      </section>

      <div className="grid gap-4 lg:grid-cols-2">
        <Sheet title="Create cohort">
          <div className="space-y-3">
            <Field value={cohortName} onChange={(event) => setCohortName(event.target.value)} aria-label="Cohort name" placeholder="Cohort name" />
            <Field value={learnerIds} onChange={(event) => setLearnerIds(event.target.value)} aria-label="Learner IDs" placeholder="Learner IDs, comma separated" />
            <Button onClick={createCohort}><Plus size={15} /> Add cohort</Button>
          </div>
        </Sheet>
        <Sheet title="Queue intervention">
          <div className="space-y-3">
            <Field value={learnerId} onChange={(event) => setLearnerId(event.target.value)} aria-label="Learner ID" placeholder="Learner ID" />
            <Field value={reason} onChange={(event) => setReason(event.target.value)} aria-label="Intervention reason" placeholder="Evidence-linked reason" />
            <Button onClick={createIntervention}><UserRoundCheck size={15} /> Queue follow-up</Button>
          </div>
        </Sheet>
      </div>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_22rem]">
        <Sheet title="Intervention queue">
          {interventions.length === 0 ? <EmptyState title="No interventions queued" /> : (
            <div className="space-y-2">
              {interventions.map((item) => <div key={item.intervention_id} className="rounded-xl border border-line bg-surface-raised/70 p-3"><div className="flex flex-wrap items-center gap-2"><AlertTriangle size={15} className="text-warning" /><p className="text-sm font-semibold">{item.learner_id}</p><Badge tone="warning">{item.status}</Badge></div><p className="mt-2 text-xs text-muted">{item.reason}</p></div>)}
            </div>
          )}
        </Sheet>
        <Sheet title="Cohorts">
          {cohorts.length === 0 ? <EmptyState title="No cohorts yet" /> : (
            <div className="space-y-2">
              {cohorts.map((cohort) => <div key={cohort.cohort_id} className="rounded-xl border border-line p-3"><div className="flex items-center gap-2"><Building2 size={15} className="text-accent" /><p className="text-sm font-semibold">{cohort.cohort_name}</p></div><p className="mt-2 flex items-center gap-1 text-xs text-muted"><Users size={13} /> {cohort.learner_ids.length} learners</p></div>)}
            </div>
          )}
        </Sheet>
      </div>
    </div>
  );
}
