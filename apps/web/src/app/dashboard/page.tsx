'use client';

import { useEffect, useState } from 'react';
import { dashboardApi } from '@/lib/api';
import {
  BarChart3, TrendingUp, TrendingDown, Minus,
  CheckCircle2, AlertTriangle, Brain, Target, Award,
} from 'lucide-react';
import WeeklyTrend from '@/components/dashboard/WeeklyTrend';

interface EffectivenessData {
  report_id: string;
  period_start: string;
  period_end: string;
  due_review_completion_rate: number;
  high_confidence_error_count: number;
  interleaving_accuracy: number;
  same_error_recurrence_rate: number;
  los_risk_heatmap: Record<string, number>;
  danger_top_3: string[];
  predicted_pass_probability: number;
  confidence_band_low: number;
  confidence_band_high: number;
  calibration_trend: string;
  error_count_trend: number[];
}

export default function EffectivenessDashboard() {
  const [data, setData] = useState<EffectivenessData | null>(null);
  const [summary, setSummary] = useState<any>(null);
  const [calibrationWarnings, setCalibrationWarnings] = useState<any[]>([]);
  const [streakData, setStreakData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      dashboardApi.getEffectiveness(30),
      dashboardApi.getSummary(),
    ]).then(([eff, sum]: [any, any]) => {
      setData(eff);
      setSummary(sum);
    }).finally(() => setLoading(false));

    dashboardApi.getCalibrationWarnings?.().then((data: any) => {
      setCalibrationWarnings(data.warnings || []);
    }).catch(() => {});

    dashboardApi.getStreaks?.().then(setStreakData).catch(() => {});
  }, []);

  const TrendIcon = data?.calibration_trend === 'improving'
    ? TrendingUp : data?.calibration_trend === 'worsening'
    ? TrendingDown : Minus;

  const trendColor = data?.calibration_trend === 'improving'
    ? 'text-success' : data?.calibration_trend === 'worsening'
    ? 'text-danger' : 'text-muted';

  if (loading) {
    return <div className="text-muted animate-pulse">加载有效性仪表盘...</div>;
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold">有效性仪表盘</h2>
        <p className="text-muted text-sm mt-1">不止看学习时长——看学习动作是否真的提高通过概率</p>
      </div>

      {/* Summary strip */}
      {summary && (
        <div className="grid grid-cols-4 gap-3">
          <MetricCard
            icon={<BarChart3 size={16} className="text-accent" />}
            label="总题目记录"
            value={String(summary.total_questions_recorded || 0)}
          />
          <MetricCard
            icon={<AlertTriangle size={16} className="text-warning" />}
            label="到期复习"
            value={String(summary.due_review_items || 0)}
          />
          <MetricCard
            icon={<Brain size={16} className="text-accent" />}
            label="活跃模式"
            value={String(summary.active_patterns || 0)}
          />
          <MetricCard
            icon={<Target size={16} className="text-success" />}
            label="预测通过率"
            value={`${((data?.predicted_pass_probability || 0) * 100).toFixed(0)}%`}
            subtitle={`${((data?.confidence_band_low || 0) * 100).toFixed(0)}% - ${((data?.confidence_band_high || 0) * 100).toFixed(0)}%`}
          />
        </div>
      )}

      {streakData && (
        <div className="grid grid-cols-4 gap-3">
          <div className="card flex items-center gap-3">
            <span className="text-2xl">{streakData.current_streak > 0 ? '🔥' : '🌱'}</span>
            <div>
              <div className="metric-label">连续学习</div>
              <div className="metric-value">{streakData.current_streak} 天</div>
            </div>
          </div>
          <div className="card flex items-center gap-3">
            <span className="text-2xl">{streakData.active_today ? '✅' : '⏳'}</span>
            <div>
              <div className="metric-label">今日</div>
              <div className="metric-value">{streakData.active_today ? '已学习' : '未学习'}</div>
            </div>
          </div>
          <div className="card col-span-2 flex items-center gap-3">
            <span className="text-2xl">📊</span>
            <div className="flex-1">
              <div className="metric-label">本周复习包进度 ({streakData.weekly_goal.completed_reviews}/{streakData.weekly_goal.goal})</div>
              <div className="w-full h-2 bg-[#0a0a0f] rounded-full mt-1 overflow-hidden">
                <div className="h-full bg-[#6366f1] rounded-full transition-all"
                  style={{ width: `${streakData.weekly_goal.progress_pct}%` }} />
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-2 gap-6">
        {/* Key metrics */}
        <div className="card space-y-4">
          <h3 className="text-sm font-semibold flex items-center gap-2">
            <Award size={14} className="text-accent" /> 核心指标 (30 天)
          </h3>
          <div className="space-y-3">
            <MetricRow
              label="到期错题完成率"
              value={`${((data?.due_review_completion_rate || 0) * 100).toFixed(0)}%`}
              target=">70%"
            />
            <MetricRow
              label="高信心错误"
              value={String(data?.high_confidence_error_count || 0)}
              target="<5"
              danger={(data?.high_confidence_error_count || 0) > 5}
            />
            <MetricRow
              label="交错练习正确率"
              value={`${((data?.interleaving_accuracy || 0) * 100).toFixed(0)}%`}
              target=">60%"
            />
            <MetricRow
              label="同类错误复发率"
              value={`${((data?.same_error_recurrence_rate || 0) * 100).toFixed(1)}%`}
              target="<20%"
              danger={(data?.same_error_recurrence_rate || 0) > 0.2}
            />
          </div>

          <div className="flex items-center gap-2 text-xs pt-2 border-t border-[#1e1e2e]">
            <span className="text-muted">校准趋势:</span>
            <TrendIcon size={14} className={trendColor} />
            <span className={trendColor}>
              {data?.calibration_trend === 'improving' ? '改善中'
               : data?.calibration_trend === 'worsening' ? '恶化中'
               : '稳定'}
            </span>
          </div>
        </div>

        {/* Calibration warnings */}
        {calibrationWarnings.length > 0 && (
          <div className="card col-span-2 border-[#ef4444]/30">
            <h3 className="text-sm font-semibold flex items-center gap-2 mb-3">
              <AlertTriangle size={14} className="text-danger" />
              信心校准警告 — 你以为你会了，其实不会
            </h3>
            <div className="space-y-2">
              {calibrationWarnings.slice(0, 5).map((w: any, i: number) => (
                <div key={i} className="text-sm bg-[#0a0a0f] rounded-lg px-3 py-2">
                  <span className="font-medium">{w.topic}</span>
                  <span className="text-muted"> / {w.los}</span>
                  <span className="text-danger ml-2">信心 {w.confidence}/4 但做错</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* LOS risk heatmap */}
        <div className="card">
          <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <Target size={14} className="text-danger" /> LOS 风险热力图
          </h3>
          {data?.los_risk_heatmap && Object.keys(data.los_risk_heatmap).length > 0 ? (
            <div className="space-y-2 max-h-72 overflow-auto">
              {Object.entries(data.los_risk_heatmap)
                .sort(([, a], [, b]) => b - a)
                .slice(0, 15)
                .map(([los, risk]) => (
                  <div key={los} className="flex items-center gap-2">
                    <span className="text-xs w-40 truncate">{los}</span>
                    <div className="flex-1 h-4 bg-[#0a0a0f] rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${
                          risk > 0.7 ? 'bg-[#ef4444]'
                          : risk > 0.4 ? 'bg-[#f59e0b]'
                          : 'bg-[#22c55e]'
                        }`}
                        style={{ width: `${(risk * 100).toFixed(0)}%` }}
                      />
                    </div>
                    <span className="text-xs text-muted w-10 text-right">
                      {(risk * 100).toFixed(0)}%
                    </span>
                  </div>
                ))}
            </div>
          ) : (
            <p className="text-xs text-muted">暂无足够数据生成风险热力图</p>
          )}

          {data?.danger_top_3 && data.danger_top_3.length > 0 && (
            <div className="mt-4 pt-3 border-t border-[#1e1e2e]">
              <div className="text-xs text-muted mb-2">⚠️ 最危险 3 个 LOS</div>
              {data.danger_top_3.map((d, i) => (
                <p key={i} className="text-xs text-danger">• {d}</p>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Weekly Trend Report */}
      <WeeklyTrend />

      {/* Error trend mini chart */}
      {data?.error_count_trend && data.error_count_trend.length > 1 && (
        <div className="card">
          <h3 className="text-sm font-semibold mb-3">每日错题趋势</h3>
          <div className="flex items-end gap-1 h-24">
            {data.error_count_trend.slice(-30).map((count, i) => {
              const maxCount = Math.max(...data.error_count_trend, 1);
              const height = (count / maxCount) * 100;
              return (
                <div key={i} className="flex-1 flex flex-col items-center gap-1">
                  <div
                    className="w-full bg-[#6366f1]/60 hover:bg-[#6366f1] rounded-t transition-colors"
                    style={{ height: `${Math.max(height, 2)}%` }}
                    title={`${count} errors`}
                  />
                </div>
              );
            })}
          </div>
          <div className="flex justify-between text-[10px] text-muted mt-1">
            <span>{data.period_start}</span>
            <span>{data.period_end}</span>
          </div>
        </div>
      )}
    </div>
  );
}

function MetricCard({ icon, label, value, subtitle }: {
  icon: React.ReactNode; label: string; value: string; subtitle?: string;
}) {
  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-2">{icon}<span className="metric-label">{label}</span></div>
      <div className="metric-value">{value}</div>
      {subtitle && <div className="text-xs text-muted mt-0.5">{subtitle}</div>}
    </div>
  );
}

function MetricRow({ label, value, target, danger }: {
  label: string; value: string; target: string; danger?: boolean;
}) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm">{label}</span>
      <div className="flex items-center gap-2">
        <span className={`text-sm font-semibold ${danger ? 'text-danger' : ''}`}>{value}</span>
        <span className="text-[10px] text-muted">目标 {target}</span>
      </div>
    </div>
  );
}
