'use client';

export function CoverageRadar({
  subjectCoverage,
}: {
  subjectCoverage: Record<string, { captured: number; total: number; examWeight: number }>;
}) {
  const subjects = Object.entries(subjectCoverage);
  if (subjects.length === 0) return null;

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold">科目覆盖率</h3>
      <div className="space-y-2">
        {subjects.map(([subject, data]) => {
          const coverage = data.total > 0 ? (data.captured / data.total) : 0;
          const expected = data.examWeight;
          const danger = coverage < expected * 0.5;

          return (
            <div key={subject} className="flex items-center gap-3">
              <span className="w-24 text-xs text-muted truncate" title={subject}>{subject}</span>
              <div className="flex-1 h-3 rounded-full bg-line overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all ${
                    danger ? 'bg-red-400' : coverage > expected ? 'bg-green-400' : 'bg-yellow-400'
                  }`}
                  style={{ width: `${Math.min(100, coverage * 100)}%` }}
                />
              </div>
              <span className="w-16 text-right text-xs text-muted">
                {data.captured}/{data.total}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
