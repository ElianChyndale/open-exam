'use client';

export type TabOption = 'all' | 'cfa' | 'general';

export function TabFilter({
  active,
  onChange,
  counts,
}: {
  active: TabOption;
  onChange: (tab: TabOption) => void;
  counts?: Partial<Record<TabOption, number>>;
}) {
  const tabs: { key: TabOption; label: string }[] = [
    { key: 'all', label: `All${counts?.all != null ? ` (${counts.all})` : ''}` },
    { key: 'cfa', label: `CFA${counts?.cfa != null ? ` (${counts.cfa})` : ''}` },
    { key: 'general', label: `General${counts?.general != null ? ` (${counts.general})` : ''}` },
  ];
  return (
    <nav className="flex gap-2" aria-label="Domain filter">
      {tabs.map(({ key, label }) => (
        <button
          key={key}
          type="button"
          onClick={() => onChange(key)}
          className={`rounded-full border px-3 py-1.5 text-xs transition-colors ${
            active === key
              ? 'border-accent bg-accent-soft text-accent'
              : 'border-line bg-surface-raised text-muted hover:text-ink'
          }`}
        >
          {label}
        </button>
      ))}
    </nav>
  );
}
