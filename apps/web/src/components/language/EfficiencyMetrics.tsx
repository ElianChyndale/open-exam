'use client';

export function EfficiencyMetrics({
  passRate,
  trend,
  dueCards,
  reviewedToday,
  avgTimePerCard,
}: {
  passRate: number;
  trend: 'up' | 'down' | 'stable';
  dueCards: number;
  reviewedToday: number;
  avgTimePerCard?: number;
}) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <MetricCard label="Pass Rate" value={`${(passRate * 100).toFixed(0)}%`} trend={trend} />
      <MetricCard label="Due Cards" value={String(dueCards)} />
      <MetricCard label="Reviewed Today" value={String(reviewedToday)} />
      {avgTimePerCard != null && (
        <MetricCard label="Avg Time" value={`${avgTimePerCard.toFixed(1)}s`} />
      )}
    </div>
  );
}

function MetricCard({ label, value, trend }: { label: string; value: string; trend?: 'up' | 'down' | 'stable' }) {
  return (
    <div className="rounded-xl border border-line bg-surface-raised p-4">
      <p className="text-xs text-muted">{label}</p>
      <p className="mt-1 text-2xl font-bold">{value}</p>
      {trend && (
        <p className={`mt-1 text-xs ${trend === 'up' ? 'text-green-600' : trend === 'down' ? 'text-red-600' : 'text-muted'}`}>
          {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'} {trend}
        </p>
      )}
    </div>
  );
}
