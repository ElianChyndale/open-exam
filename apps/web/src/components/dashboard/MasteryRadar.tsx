'use client';

import { useEffect, useState } from 'react';
import { dashboardApi } from '@/lib/api';

interface TopicMastery {
  topic: string;
  mastery: number;
  errors: number;
  status: string;
}

export default function MasteryRadar() {
  const [data, setData] = useState<{ topics: TopicMastery[]; overall_mastery: number } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardApi.getMastery().then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-xs text-muted animate-pulse">加载掌握度...</div>;
  if (!data?.topics) return null;

  const statusColor = (status: string) => {
    switch (status) {
      case 'critical': return 'bg-danger text-danger';
      case 'needs_work': return 'bg-warning text-warning';
      case 'ready': return 'bg-success text-success';
      default: return 'bg-muted text-muted';
    }
  };

  const statusBg = (status: string) => {
    switch (status) {
      case 'critical': return 'bg-danger/10 border-danger/30';
      case 'needs_work': return 'bg-warning/10 border-warning/30';
      case 'ready': return 'bg-success/10 border-success/30';
      default: return 'bg-[#0a0a0f] border-[#1e1e2e]';
    }
  };

  const statusLabel = (status: string) => {
    switch (status) {
      case 'critical': return '危急';
      case 'needs_work': return '待加强';
      case 'ready': return '就绪';
      default: return '无数据';
    }
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold">Topic 掌握度雷达</h3>
        <div className="text-xs text-muted">
          综合掌握度: <span className="text-lg font-bold text-[#6366f1]">{data.overall_mastery}%</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2">
        {data.topics.map((t) => (
          <div key={t.topic} className={`rounded-lg p-3 border ${statusBg(t.status)}`}>
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-medium truncate mr-2">{t.topic}</span>
              <span className={`text-[10px] px-1.5 py-0.5 rounded-full ${statusColor(t.status)}`}>
                {statusLabel(t.status)}
              </span>
            </div>
            <div className="w-full h-1.5 bg-[#0a0a0f] rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all ${
                  t.mastery >= 60 ? 'bg-success' : t.mastery >= 30 ? 'bg-warning' : 'bg-danger'
                }`}
                style={{ width: `${t.mastery}%` }}
              />
            </div>
            <div className="flex justify-between text-[10px] text-muted mt-1">
              <span>{t.mastery}%</span>
              <span>{t.errors} 错题</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
