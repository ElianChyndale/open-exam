'use client';

import { useEffect, useState } from 'react';
import { profileApi, type LearnerProfile } from '@/lib/api';
import { Alert, Button, Field, Select, Surface } from '@/components/ui/ui';

const defaults: LearnerProfile = {
  exam_date: '',
  current_phase: 'foundation',
  target_score_percentile: 70,
  daily_minutes_available: 120,
  weekly_study_days: 6,
  preferred_session_minutes: 50,
  peak_energy_window: '09:00-12:00',
  moderate_energy_window: '14:00-18:00',
  low_energy_window: '20:00-22:00',
};

export function ProfileForm({ heading, detail }: { heading: string; detail: string }) {
  const [profile, setProfile] = useState(defaults);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    profileApi.get().then(({ profile }) => setProfile(profile)).catch(() => undefined);
  }, []);

  const set = <K extends keyof LearnerProfile>(key: K, value: LearnerProfile[K]) =>
    setProfile((current) => ({ ...current, [key]: value }));

  return (
    <div className="mx-auto max-w-3xl space-y-5">
      <header>
        <p className="metric-label">Learner configuration</p>
        <h1 className="mt-1 text-3xl font-semibold tracking-tight">{heading}</h1>
        <p className="mt-2 text-sm text-muted">{detail}</p>
      </header>
      {saved ? <Alert tone="success">Your study profile has been saved to the local event ledger.</Alert> : null}
      {error ? <Alert tone="danger">{error}</Alert> : null}
      <Surface>
        <form
          className="grid gap-4 md:grid-cols-2"
          onSubmit={(event) => {
            event.preventDefault();
            setSaved(false);
            setError('');
            profileApi.update(profile).then(({ profile: next }) => {
              setProfile(next);
              setSaved(true);
            }).catch((reason: Error) => setError(reason.message));
          }}
        >
          <Label text="Exam date"><Field type="date" value={profile.exam_date} onChange={(event) => set('exam_date', event.target.value)} /></Label>
          <Label text="Study phase">
            <Select value={profile.current_phase} onChange={(event) => set('current_phase', event.target.value)}>
              <option value="foundation">Foundation</option><option value="review">Review</option><option value="mock">Mock intensive</option>
            </Select>
          </Label>
          <Label text="Target percentile"><Field type="number" min={1} max={100} value={profile.target_score_percentile} onChange={(event) => set('target_score_percentile', Number(event.target.value))} /></Label>
          <Label text="Available minutes per day"><Field type="number" min={10} value={profile.daily_minutes_available} onChange={(event) => set('daily_minutes_available', Number(event.target.value))} /></Label>
          <Label text="Study days per week"><Field type="number" min={1} max={7} value={profile.weekly_study_days} onChange={(event) => set('weekly_study_days', Number(event.target.value))} /></Label>
          <Label text="Preferred session minutes"><Field type="number" min={10} value={profile.preferred_session_minutes} onChange={(event) => set('preferred_session_minutes', Number(event.target.value))} /></Label>
          <Label text="Peak energy window"><Field value={profile.peak_energy_window} onChange={(event) => set('peak_energy_window', event.target.value)} /></Label>
          <Label text="Moderate energy window"><Field value={profile.moderate_energy_window} onChange={(event) => set('moderate_energy_window', event.target.value)} /></Label>
          <Label text="Low energy window"><Field value={profile.low_energy_window} onChange={(event) => set('low_energy_window', event.target.value)} /></Label>
          <div className="flex items-end md:justify-end"><Button type="submit">Save profile</Button></div>
        </form>
      </Surface>
    </div>
  );
}

function Label({ text, children }: { text: string; children: React.ReactElement }) {
  return <label className="space-y-1.5 text-xs font-semibold text-muted"><span>{text}</span>{children}</label>;
}
