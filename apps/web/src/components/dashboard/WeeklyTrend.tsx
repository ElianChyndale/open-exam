'use client';

import { useEffect, useState } from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { dashboardApi } from '@/lib/api';

export default function WeeklyTrend() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardApi.getWeeklyTrend().then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-xs text-muted animate-pulse">加载趋势...</div>;
  if (!data) return null;

  const TrendIcon = ({ trend }: { trend: string }) => {
    if (trend === 'improving') return <TrendingUp size={14} className="text-success" />;
    if (trend === 'worsening') return <TrendingDown size={14} className="text-danger" />;
    return <Minus size={14} className="text-muted" />;
  };

  const metrics = [
    { label: '错题数', key: 'errors', format: (v: any) => `${v.current} (${v.change_pct > 0 ? '+' : ''}${v.change_pct}%)` },
    { label: '高信心错误', key: 'high_confidence_errors', format: (v: any) => `${v.current} (${v.change_pct > 0 ? '+' : ''}${v.change_pct}%)` },
    { label: '覆盖 Topic', key: 'topics_covered', format: (v: any) => `${v.current}` },
    { label: '复习完成', key: 'reviews_completed', format: (v: any) => `${v.current}` },
  ];

  return (
    <div className="card">
      <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
        周趋势对比
        <span className="text-[10px] text-muted font-normal">
          {data.this_week.start} ~ {data.this_week.end}
        </span>
      </h3>
      <div className="space-y-2">
        {metrics.map((m) => {
          const v = data[m.key];
          return (
            <div key={m.key} className="flex items-center justify-between text-sm bg-surface-field rounded-lg px-3 py-2">
              <span>{m.label}</span>
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted">上周 {v.previous}</span>
                <span className="font-medium">{m.format(v)}</span>
                <TrendIcon trend={v.trend} />
              </div>
            </div>
          );
        })}
      </div>
      <div className="mt-3 text-xs text-muted">
        vs 上周 ({data.last_week.start} ~ {data.last_week.end})
      </div>
    </div>
  );
}
