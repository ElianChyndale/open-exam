'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { ArrowRight, Languages, LibraryBig, Repeat2 } from 'lucide-react';

import { languageApi, LanguageItem, LanguageProfile } from '@/lib/api';
import { LanguageShell } from '@/components/language/LanguageShell';
import { MotionNumber } from '@/components/motion/MotionNumber';

export default function LanguageCockpit() {
  const [stats, setStats] = useState<Record<string, number | string>>({});
  const [profiles, setProfiles] = useState<LanguageProfile[]>([]);
  const [items, setItems] = useState<LanguageItem[]>([]);

  useEffect(() => {
    Promise.all([languageApi.stats(), languageApi.profiles(), languageApi.items()])
      .then(([nextStats, profileData, itemData]) => {
        setStats(nextStats);
        setProfiles(profileData.profiles);
        setItems(itemData.items.slice(-4).reverse());
      })
      .catch(() => undefined);
  }, []);

  return (
    <LanguageShell title="Your language encounters, organized into practice." eyebrow="LanguageOS cockpit">
      <div className="grid gap-4 sm:grid-cols-3">
        <Metric label="Corpus sources" value={Number(stats.source_count || 0)} icon={<LibraryBig size={17} />} />
        <Metric label="Saved items" value={Number(stats.item_count || 0)} icon={<Languages size={17} />} />
        <Metric label="Due cards" value={Number(stats.due_count || 0)} icon={<Repeat2 size={17} />} />
      </div>
      <div className="grid gap-4 lg:grid-cols-[1.15fr_0.85fr]">
        <section className="motion-reveal card">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold">Recent expressions</h3>
            <Link href="/language/corpus" className="text-xs text-accent">Open corpus</Link>
          </div>
          <div className="mt-4 space-y-3">
            {items.map((item) => <div key={item.item_id} className="rounded-xl border border-line p-3"><p className="font-medium">{item.canonical_form}</p><p className="mt-1 text-xs text-muted">{item.item_type} · {item.language}</p></div>)}
            {items.length === 0 ? <p className="text-sm text-muted">Import a sentence and collect the first phrase.</p> : null}
          </div>
        </section>
        <section className="motion-reveal card">
          <h3 className="font-semibold">Profiles</h3>
          <div className="mt-4 space-y-2">{profiles.map((profile) => <div key={profile.profile_id} className="rounded-xl border border-line p-3 text-sm"><strong>{profile.profile_id}</strong><p className="mt-1 text-xs text-muted">{profile.level_target} · {profile.domains.join(', ')}</p></div>)}</div>
          <Link href="/language/import" className="mt-4 flex items-center gap-2 text-sm text-accent">Capture context <ArrowRight size={15} /></Link>
        </section>
      </div>
    </LanguageShell>
  );
}

function Metric({ label, value, icon }: { label: string; value: number; icon: React.ReactNode }) {
  return <div className="motion-reveal card"><div className="flex items-center gap-2 text-accent">{icon}<span className="metric-label">{label}</span></div><div className="metric-value mt-3"><MotionNumber value={value} /></div></div>;
}
