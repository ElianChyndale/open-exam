'use client';

import Link from 'next/link';
import type { ReactNode } from 'react';
import { AlertTriangle, ArrowRight, Keyboard, Loader2, ShieldCheck } from 'lucide-react';

export type ShortcutItem = {
  keys: string;
  action: string;
};

const defaultShortcuts: ShortcutItem[] = [
  { keys: 'R / Space', action: 'Reveal answer or feedback' },
  { keys: 'Ctrl/⌘ + Enter', action: 'Submit the primary action' },
  { keys: '1', action: 'Forgot or incorrect' },
  { keys: '2', action: 'Partial' },
  { keys: '3', action: 'Recalled or correct' },
  { keys: 'S', action: 'Skip' },
  { keys: 'N', action: 'Next' },
  { keys: '?', action: 'Show or hide this help' },
];

export function ShortcutHelp({
  open,
  onToggle,
  shortcuts = defaultShortcuts,
  className = '',
}: {
  open: boolean;
  onToggle: () => void;
  shortcuts?: ShortcutItem[];
  className?: string;
}) {
  return (
    <section className={`rounded-lg border border-line bg-surface-raised p-3 ${className}`} aria-labelledby="keyboard-shortcuts-title">
      <button type="button" onClick={onToggle} className="flex w-full items-center justify-between gap-3 text-left" aria-expanded={open} aria-controls="keyboard-shortcuts-panel">
        <span className="inline-flex items-center gap-2 text-sm font-semibold">
          <Keyboard size={15} className="text-accent" />
          <span id="keyboard-shortcuts-title">Keyboard shortcuts</span>
        </span>
        <span className="text-xs font-semibold text-accent">{open ? 'Hide' : 'Show'}</span>
      </button>
      {open && (
        <div id="keyboard-shortcuts-panel" className="mt-3 grid gap-2 sm:grid-cols-2" role="region" aria-label="Keyboard shortcuts">
          {shortcuts.map((shortcut) => (
            <div key={`${shortcut.keys}-${shortcut.action}`} className="flex items-center justify-between gap-3 rounded-lg border border-line bg-surface-field px-3 py-2 text-xs">
              <kbd className="rounded border border-line bg-surface-raised px-2 py-1 font-semibold text-foreground">{shortcut.keys}</kbd>
              <span className="text-right text-muted">{shortcut.action}</span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export function LoadingState({ title = 'Loading', detail }: { title?: string; detail?: string }) {
  return (
    <section className="rounded-lg border border-line bg-surface-raised p-8 text-center text-sm text-muted" role="status" aria-live="polite">
      <Loader2 size={28} className="mx-auto mb-3 animate-spin text-accent" />
      <p className="font-semibold text-foreground">{title}</p>
      {detail && <p className="mt-1">{detail}</p>}
    </section>
  );
}

export function EmptyState({ title, detail, actionHref, actionLabel }: { title: string; detail: string; actionHref?: string; actionLabel?: string }) {
  return (
    <section className="rounded-lg border border-line bg-surface-raised p-6 text-sm text-muted">
      <p className="font-semibold text-foreground">{title}</p>
      <p className="mt-1 leading-6">{detail}</p>
      {actionHref && actionLabel && (
        <Link href={actionHref} className="btn-secondary mt-4 inline-flex items-center gap-2">
          {actionLabel}
          <ArrowRight size={14} />
        </Link>
      )}
    </section>
  );
}

export function ErrorState({ message, actionLabel = 'Retry', onAction }: { message: string; actionLabel?: string; onAction?: () => void }) {
  return (
    <section className="rounded-lg border border-danger-soft bg-danger-soft p-4 text-sm text-danger" role="alert">
      <div className="flex items-start gap-2">
        <AlertTriangle size={16} className="mt-0.5 shrink-0" />
        <div>
          <p className="font-semibold">Action needed</p>
          <p className="mt-1 leading-6">{message}</p>
          {onAction && (
            <button type="button" onClick={onAction} className="btn-secondary mt-3">
              {actionLabel}
            </button>
          )}
        </div>
      </div>
    </section>
  );
}

export function QualityGateWarning({ children }: { children: ReactNode }) {
  return (
    <section className="flex items-start gap-2 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning" role="note">
      <ShieldCheck size={16} className="mt-0.5 shrink-0" />
      <div className="leading-6">{children}</div>
    </section>
  );
}

export function StatusBadge({ status }: { status: string }) {
  const normalized = String(status || 'unknown').toLowerCase();
  const className =
    normalized.includes('confirm') || normalized.includes('complete') || normalized.includes('ready')
      ? 'border-success-soft bg-success-soft text-success'
      : normalized.includes('reject') || normalized.includes('fail') || normalized.includes('blocked')
        ? 'border-danger-soft bg-danger-soft text-danger'
        : normalized.includes('draft') || normalized.includes('review') || normalized.includes('weak')
          ? 'border-warning-soft bg-warning-soft text-warning'
          : 'border-line bg-surface-field text-muted';
  return <span className={`rounded border px-2 py-0.5 text-xs font-semibold ${className}`}>{status || 'unknown'}</span>;
}

export function SourceRefsPanel({ refs }: { refs: string[] }) {
  if (!refs.length) return null;
  return (
    <div className="mt-3 flex flex-wrap gap-2" aria-label="Source references">
      {refs.map((ref) => (
        <span key={ref} className="source-ref-token rounded border border-line bg-surface-field px-2 py-1 text-xs text-muted">
          {ref}
        </span>
      ))}
    </div>
  );
}
