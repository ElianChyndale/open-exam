'use client';

import { useEffect, useState } from 'react';

import { languageApi, LanguageProfile } from '@/lib/api';
import { LanguageShell } from '@/components/language/LanguageShell';

export default function LanguageSettings() {
  const [flags, setFlags] = useState<Record<string, boolean>>({});
  const [profiles, setProfiles] = useState<LanguageProfile[]>([]);
  const [active, setActive] = useState('');
  const [message, setMessage] = useState('');
  useEffect(() => { Promise.all([languageApi.settings(), languageApi.profiles()]).then(([settings, profileData]) => { setFlags(settings); setProfiles(profileData.profiles); setActive(profileData.active_profile_id); }); }, []);
  const select = async (profileId: string) => { await languageApi.selectProfile(profileId); setActive(profileId); setMessage(`Active profile: ${profileId}`); };
  return (
    <LanguageShell title="Keep optional intelligence explicit." eyebrow="LanguageOS settings">
      <div className="grid gap-4 lg:grid-cols-2">
        <section className="motion-reveal card"><h3 className="font-semibold">Profiles</h3><div className="mt-4 space-y-2">{profiles.map((profile) => <button type="button" key={profile.profile_id} onClick={() => select(profile.profile_id)} className={`w-full rounded-xl border p-3 text-left text-sm ${active === profile.profile_id ? 'border-accent bg-accent-soft' : 'border-line'}`}><strong>{profile.profile_id}</strong><span className="ml-2 text-xs text-muted">{profile.level_target}</span></button>)}</div></section>
        <section className="motion-reveal card"><h3 className="font-semibold">Rollout flags</h3><div className="mt-4 space-y-2">{Object.entries(flags).map(([key, enabled]) => <div key={key} className="flex items-center justify-between rounded-xl border border-line p-3 text-xs"><span>{key}</span><span className={enabled ? 'text-success' : 'text-muted'}>{enabled ? 'enabled' : 'disabled'}</span></div>)}</div></section>
      </div>
      {message ? <p role="status" className="text-sm text-muted">{message}</p> : null}
    </LanguageShell>
  );
}
