'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  BarChart3,
  BookOpen,
  Bot,
  Building2,
  FileText,
  GitBranch,
  Library,
  Menu,
  PenLine,
  Search,
  Settings,
  Stethoscope,
  Target,
  X,
  Zap,
} from 'lucide-react';
import { cn } from '@/components/ui/ui';

const desktopGroups = [
  {
    label: 'Study',
    items: [
      { href: '/today', label: 'Today', icon: Zap },
      { href: '/practice', label: 'Practice', icon: Target },
      { href: '/review', label: 'Retrieval review', icon: BookOpen },
      { href: '/map', label: 'Curriculum map', icon: Library },
      { href: '/graph', label: 'Knowledge graph', icon: GitBranch },
    ],
  },
  {
    label: 'Evidence',
    items: [
      { href: '/capture', label: 'Capture mistake', icon: PenLine },
      { href: '/diagnosis', label: 'Diagnosis', icon: Stethoscope },
      { href: '/mock', label: 'Mock center', icon: FileText },
      { href: '/coach', label: 'Coach center', icon: Bot },
    ],
  },
  {
    label: 'Progress',
    items: [
      { href: '/dashboard', label: 'Effectiveness', icon: BarChart3 },
      { href: '/institution', label: 'Institution', icon: Building2 },
      { href: '/settings', label: 'Settings', icon: Settings },
    ],
  },
];

const mobileTabs = [
  { href: '/today', label: 'Today', icon: Zap },
  { href: '/practice', label: 'Practice', icon: Target },
  { href: '/coach', label: 'Coach', icon: Bot },
];

function NavLink({ href, label, icon: Icon, compact = false }: {
  href: string;
  label: string;
  icon: typeof Zap;
  compact?: boolean;
}) {
  const pathname = usePathname();
  const isActive = pathname === href || pathname.startsWith(`${href}/`);

  return (
    <Link
      href={href}
      className={cn(
        'flex items-center rounded-xl text-sm transition-colors',
        compact ? 'flex-col gap-1 px-3 py-2 text-[11px]' : 'gap-3 px-3 py-2',
        isActive
          ? 'bg-accent/10 font-semibold text-accent'
          : 'text-muted hover:bg-surface-hover/80 hover:text-ink',
      )}
    >
      <Icon size={compact ? 18 : 16} strokeWidth={isActive ? 2.4 : 1.9} />
      <span>{label}</span>
    </Link>
  );
}

export function Sidebar() {
  const [moreOpen, setMoreOpen] = useState(false);

  return (
    <>
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 border-r border-line/80 bg-surface-sidebar/80 px-3 py-4 backdrop-blur-2xl lg:flex lg:flex-col">
        <Link href="/today" className="mb-6 flex items-center gap-3 px-2 py-1">
          <div className="grid h-9 w-9 place-items-center rounded-xl bg-accent-action text-sm font-bold text-white shadow-sm">O</div>
          <div>
            <p className="text-sm font-semibold tracking-tight">OpenExam</p>
            <p className="text-[10px] uppercase tracking-[0.16em] text-muted">CFA Level I workspace</p>
          </div>
        </Link>

        <Link href="/search" className="mb-4 flex items-center gap-2 rounded-xl border border-line bg-surface-raised/60 px-3 py-2 text-xs text-muted hover:bg-surface-raised">
          <Search size={14} />
          <span>Search knowledge</span>
          <kbd className="ml-auto rounded border border-line px-1.5 py-0.5 text-[10px]">/</kbd>
        </Link>

        <nav className="flex-1 space-y-5 overflow-y-auto">
          {desktopGroups.map((group) => (
            <section key={group.label}>
              <p className="mb-1 px-3 text-[10px] font-semibold uppercase tracking-[0.15em] text-muted">{group.label}</p>
              <div className="space-y-0.5">
                {group.items.map((item) => <NavLink key={item.href} {...item} />)}
              </div>
            </section>
          ))}
        </nav>

        <div className="mt-4 border-t border-line/80 px-2 pt-4 text-[10px] leading-5 text-muted">
          <p>CFA Level I · local-first</p>
          <p>Evidence before strategy</p>
        </div>
      </aside>

      <nav className="fixed inset-x-0 bottom-0 z-50 flex h-[4.6rem] items-center justify-around border-t border-line/80 bg-surface-sidebar/90 px-2 pb-[env(safe-area-inset-bottom)] backdrop-blur-2xl lg:hidden">
        {mobileTabs.map((item) => <NavLink key={item.href} {...item} compact />)}
        <button
          type="button"
          className={cn('flex flex-col items-center gap-1 rounded-xl px-3 py-2 text-[11px] text-muted', moreOpen && 'bg-accent/10 text-accent')}
          onClick={() => setMoreOpen((current) => !current)}
          aria-expanded={moreOpen}
          aria-controls="mobile-more-menu"
        >
          <Menu size={18} />
          <span>More</span>
        </button>
      </nav>

      {moreOpen ? (
        <div id="mobile-more-menu" className="fixed inset-0 z-40 bg-ink/15 backdrop-blur-sm lg:hidden" onClick={() => setMoreOpen(false)}>
          <section
            className="absolute inset-x-3 bottom-20 rounded-2xl border border-line bg-surface-sidebar/95 p-3 shadow-window"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="mb-2 flex items-center justify-between px-2">
              <p className="text-sm font-semibold">OpenExam modules</p>
              <button className="button-ghost p-2" onClick={() => setMoreOpen(false)} aria-label="Close module menu">
                <X size={16} />
              </button>
            </div>
            <div className="grid grid-cols-2 gap-1">
              {desktopGroups.flatMap((group) => group.items).map((item) => <NavLink key={item.href} {...item} />)}
            </div>
          </section>
        </div>
      ) : null}
    </>
  );
}
