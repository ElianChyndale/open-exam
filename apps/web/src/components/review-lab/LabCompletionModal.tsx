'use client';

import { useEffect, useState } from 'react';
import { X, Trophy, Clock, Brain, TrendingUp, AlertTriangle } from 'lucide-react';

interface SubjectBreakdown {
  total: number;
  recalled: number;
  partial: number;
  forgot: number;
  skipped: number;
}

interface LabReport {
  session_id: string;
  total_units: number;
  completed_units: number;
  recalled: number;
  partial: number;
  forgot: number;
  skipped: number;
  recall_rate: number;
  avg_confidence_before: number;
  avg_confidence_after: number;
  total_time_seconds: number;
  subject_breakdown: Record<string, SubjectBreakdown>;
  started_at: string;
  completed_at: string;
}

interface LabCompletionModalProps {
  report: LabReport | null;
  onClose: () => void;
  onStartNew: () => void;
}

/**
 * LabCompletionModal — quality report after a review lab session.
 *
 * Shows recall rate, confidence delta, per-subject breakdown,
 * and recommended next actions.
 */
export function LabCompletionModal({ report, onClose, onStartNew }: LabCompletionModalProps) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (report) {
      const timer = setTimeout(() => setVisible(true), 50);
      return () => clearTimeout(timer);
    }
    setVisible(false);
  }, [report]);

  if (!report) return null;

  const total = report.completed_units || 1;
  const recallRate = Math.round(report.recall_rate * 100);
  const confidenceDelta = report.avg_confidence_after - report.avg_confidence_before;
  const minutes = Math.round(report.total_time_seconds / 60);

  // Determine quality tier
  let tier = 'needs-work';
  let tierLabel = 'Keep drilling';
  let tierColor = 'text-danger';
  let tierBg = 'bg-danger-soft';
  if (recallRate >= 90) {
    tier = 'excellent';
    tierLabel = 'Excellent';
    tierColor = 'text-success';
    tierBg = 'bg-success-soft';
  } else if (recallRate >= 70) {
    tier = 'good';
    tierLabel = 'Good progress';
    tierColor = 'text-accent';
    tierBg = 'bg-accent-soft';
  } else if (recallRate >= 50) {
    tier = 'fair';
    tierLabel = 'Fair — review gaps';
    tierColor = 'text-warning';
    tierBg = 'bg-warning-soft';
  }

  const subjects = Object.entries(report.subject_breakdown).sort(
    (a, b) => b[1].total - a[1].total
  );

  return (
    <div
      className={`fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm transition-opacity duration-300 ${
        visible ? 'opacity-100' : 'opacity-0'
      }`}
      onClick={onClose}
    >
      <div
        className={`relative w-full max-w-lg mx-4 rounded-2xl border border-line bg-surface-raised p-6 shadow-2xl transition-all duration-300 ${
          visible ? 'translate-y-0 scale-100' : 'translate-y-4 scale-95'
        }`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close button */}
        <button
          type="button"
          onClick={onClose}
          className="absolute top-4 right-4 text-muted hover:text-foreground transition-colors"
          aria-label="Close session completion report"
          title="Close"
        >
          <X size={18} />
        </button>

        {/* Header */}
        <div className="text-center mb-6">
          <div className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-sm font-semibold ${tierBg} ${tierColor}`}>
            <Trophy size={14} />
            {tierLabel}
          </div>
          <h2 className="text-2xl font-bold mt-3">Session Complete</h2>
          <p className="text-sm text-muted mt-1">
            {report.completed_units} units reviewed in {minutes} min
          </p>
        </div>

        {/* Key metrics */}
        <div className="grid grid-cols-3 gap-3 mb-6">
          <MetricCard
            icon={<Brain size={16} className={tierColor} />}
            label="Recall Rate"
            value={`${recallRate}%`}
            color={tierColor}
          />
          <MetricCard
            icon={<TrendingUp size={16} className={confidenceDelta >= 0 ? 'text-success' : 'text-danger'} />}
            label="Confidence"
            value={`${confidenceDelta >= 0 ? '+' : ''}${confidenceDelta.toFixed(1)}`}
            color={confidenceDelta >= 0 ? 'text-success' : 'text-danger'}
          />
          <MetricCard
            icon={<Clock size={16} className="text-muted" />}
            label="Time"
            value={`${minutes}m`}
            color="text-muted"
          />
        </div>

        {/* Outcome breakdown */}
        <div className="rounded-xl bg-surface-field border border-line p-4 mb-6">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-muted mb-3">
            Outcome Breakdown
          </h3>
          <div className="space-y-2">
            <OutcomeBar label="Recalled" count={report.recalled} total={total} color="bg-success" />
            <OutcomeBar label="Partial" count={report.partial} total={total} color="bg-warning" />
            <OutcomeBar label="Forgot" count={report.forgot} total={total} color="bg-danger" />
            {report.skipped > 0 && (
              <OutcomeBar label="Skipped" count={report.skipped} total={total} color="bg-muted" />
            )}
          </div>
        </div>

        {/* Subject breakdown */}
        {subjects.length > 0 && (
          <div className="rounded-xl bg-surface-field border border-line p-4 mb-6">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-muted mb-3">
              By Subject
            </h3>
            <div className="space-y-2 max-h-40 overflow-auto">
              {subjects.map(([name, stats]) => (
                <div key={name} className="flex items-center justify-between text-sm">
                  <span className="truncate max-w-[140px]" title={name}>{name}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-success text-xs">{stats.recalled}</span>
                    <span className="text-warning text-xs">{stats.partial}</span>
                    <span className="text-danger text-xs">{stats.forgot}</span>
                    <span className="text-muted text-xs w-8 text-right">{stats.total}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations */}
        <div className="mb-6">
          {report.forgot > 0 && (
            <div className="flex items-start gap-2 text-sm text-danger mb-2">
              <AlertTriangle size={14} className="mt-0.5 shrink-0" />
              <span>{report.forgot} item(s) marked forgot — schedule a drill session.</span>
            </div>
          )}
          {report.partial > 0 && (
            <div className="flex items-start gap-2 text-sm text-warning mb-2">
              <AlertTriangle size={14} className="mt-0.5 shrink-0" />
              <span>{report.partial} item(s) marked partial — revisit worked examples.</span>
            </div>
          )}
          {recallRate >= 80 && (
            <div className="flex items-start gap-2 text-sm text-success">
              <Trophy size={14} className="mt-0.5 shrink-0" />
              <span>Strong recall — these items are consolidating well.</span>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          <button
            type="button"
            onClick={onStartNew}
            className="flex-1 rounded-xl bg-accent-solid hover:bg-accent-strong px-4 py-2.5 text-sm font-semibold text-white transition-colors"
          >
            Start New Session
          </button>
          <button
            type="button"
            onClick={onClose}
            className="rounded-xl border border-line bg-surface-field hover:bg-surface px-4 py-2.5 text-sm font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function MetricCard({
  icon,
  label,
  value,
  color,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  color: string;
}) {
  return (
    <div className="rounded-xl bg-surface-field border border-line p-3 text-center">
      <div className="flex justify-center mb-1">{icon}</div>
      <div className={`text-xl font-bold ${color}`}>{value}</div>
      <div className="text-[10px] text-muted uppercase tracking-wider">{label}</div>
    </div>
  );
}

function OutcomeBar({
  label,
  count,
  total,
  color,
}: {
  label: string;
  count: number;
  total: number;
  color: string;
}) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs w-16 text-right text-muted">{label}</span>
      <div className="flex-1 h-2 rounded-full bg-surface-raised overflow-hidden">
        <div
          className={`h-full rounded-full ${color} transition-all duration-500`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-xs w-8 text-right font-medium">{count}</span>
    </div>
  );
}
