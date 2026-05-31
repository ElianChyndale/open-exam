'use client';

import { useEffect, useState } from 'react';
import { profilesApi } from '@/lib/api';

interface ExamProfileSummary {
  name: string;
  short_name: string;
}

export default function ProfileSwitcher() {
  const [profiles, setProfiles] = useState<ExamProfileSummary[]>([]);
  const [active, setActive] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    Promise.all([profilesApi.list(), profilesApi.getActive()])
      .then(([available, current]: [any, any]) => {
        setProfiles(available.profiles || []);
        setActive(current.profile?.short_name || '');
      })
      .catch(() => undefined);
  }, []);

  if (!profiles.length) return null;

  const updateProfile = async (profileName: string) => {
    setSaving(true);
    setActive(profileName);
    try {
      await profilesApi.setActive(profileName);
      window.location.reload();
    } finally {
      setSaving(false);
    }
  };

  return (
    <label className="block text-[10px] text-muted">
      <span className="mb-1 block uppercase">Exam profile</span>
      <select
        aria-label="Active exam profile"
        className="w-full rounded-lg border border-line bg-surface-field px-2 py-1.5 text-xs text-ink"
        disabled={saving}
        value={active}
        onChange={(event) => updateProfile(event.target.value)}
      >
        {profiles.map((profile) => (
          <option key={profile.short_name} value={profile.short_name}>
            {profile.name}
          </option>
        ))}
      </select>
    </label>
  );
}
