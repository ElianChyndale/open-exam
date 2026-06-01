'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BarChart3, BookOpenText, BrainCircuit, Ear, FileInput, LibraryBig, Settings2, Sparkles } from 'lucide-react';

import { AnimatedPage } from '@/components/motion/AnimatedPage';

const tabs = [
  { href: '/language', label: 'Cockpit', icon: Sparkles },
  { href: '/language/import', label: 'Import', icon: FileInput },
  { href: '/language/corpus', label: 'Corpus', icon: LibraryBig },
  { href: '/language/review', label: 'Review', icon: BookOpenText },
  { href: '/language/listening', label: 'Listening', icon: Ear },
  { href: '/language/grammar', label: 'Grammar', icon: BrainCircuit },
  { href: '/language/intuition', label: 'Intuition', icon: Sparkles },
  { href: '/language/stats', label: 'Stats', icon: BarChart3 },
  { href: '/language/settings', label: 'Settings', icon: Settings2 },
];

export function LanguageShell({ title, eyebrow, children }: { title: string; eyebrow: string; children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <AnimatedPage className="language-lab mx-auto max-w-6xl space-y-6">
      <header className="motion-reveal language-hero rounded-3xl border border-line p-6 sm:p-8">
        <p className="text-xs font-semibold uppercase tracking-[0.22em] text-accent">{eyebrow}</p>
        <h2 className="mt-3 max-w-3xl text-3xl font-bold tracking-tight sm:text-4xl">{title}</h2>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-muted">
          Context first. Every phrase stays attached to the moment where it became worth learning.
        </p>
      </header>
      <nav className="motion-reveal flex gap-2 overflow-x-auto pb-1" aria-label="LanguageOS sections">
        {tabs.map(({ href, label, icon: Icon }) => {
          const active = pathname === href;
          return (
            <Link key={href} href={href} className={`flex shrink-0 items-center gap-2 rounded-full border px-3 py-2 text-xs transition-colors ${
              active ? 'border-accent bg-accent-soft text-accent' : 'border-line bg-surface-raised text-muted hover:text-ink'
            }`}>
              <Icon size={14} /> {label}
            </Link>
          );
        })}
      </nav>
      {children}
    </AnimatedPage>
  );
}
