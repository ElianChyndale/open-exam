'use client';

import { useEffect, useState } from 'react';
import { diagnosisApi, attemptsApi } from '@/lib/api';
import { Stethoscope, Lightbulb, Repeat, Link2, AlertTriangle, TrendingUp } from 'lucide-react';

interface Attempt {
  attempt_id: string;
  event_id?: string;
  topic: string;
  los: string;
  error_type: string;
  confidence: number;
  created_at: string;
}

interface Pattern {
  pattern_id: string;
  pattern_key: string;
  recurrence: number;
  severity: string;
}

const errorLabels: Record<string, string> = {
  concept_confusion: '概念混淆',
  formula_misuse: '公式误用',
  knowledge_gap: '知识空缺',
  careless_reading: '粗心读题',
  time_pressure: '时间压力',
  confidence_calibration_failure: '信心校准失败',
  fatigue_energy_mismatch: '精力不足',
  agent_failure: 'Agent 失误',
};

const severityColors: Record<string, string> = {
  high: 'text-danger',
  medium: 'text-warning',
  low: 'text-muted',
};

export default function DiagnosisPage() {
  const [attempts, setAttempts] = useState<Attempt[]>([]);
  const [patterns, setPatterns] = useState<Pattern[]>([]);
  const [selectedId, setSelectedId] = useState('');
  const [diagnosis, setDiagnosis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [diagLoading, setDiagLoading] = useState(false);

  useEffect(() => {
    Promise.all([
      attemptsApi.listRecent(50),
      diagnosisApi.listPatterns(),
    ]).then(([attData, patData]: [any, any]) => {
      setAttempts(attData.attempts || []);
      setPatterns(patData.patterns || []);
    }).finally(() => setLoading(false));
  }, []);

  const runDiagnosis = async () => {
    if (!selectedId) return;
    setDiagLoading(true);
    setDiagnosis(null);
    try {
      const result = await diagnosisApi.diagnose({
        attempt_id: selectedId,
        error_type: '',
      });
      setDiagnosis(result);
    } catch (err: any) {
      setDiagnosis({ error: err.message });
    } finally {
      setDiagLoading(false);
    }
  };

  if (loading) {
    return <div className="text-muted animate-pulse">加载诊断数据...</div>;
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold">错因诊断</h2>
        <p className="text-muted text-sm mt-1">真正的错因、纠偏规则和下一步练习——每道题转成下一次行动</p>
      </div>

      {/* Pattern summary */}
      {patterns.length > 0 && (
        <div className="card">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp size={16} className="text-warning" />
            <span className="text-sm font-semibold">活跃错误模式 ({patterns.length})</span>
          </div>
          <div className="space-y-2">
            {patterns.map((p) => {
              const [topic, los, error] = p.pattern_key.split('::');
              return (
                <div key={p.pattern_id} className="flex items-center justify-between text-sm bg-surface-field rounded-lg px-3 py-2">
                  <div>
                    <span className="font-medium">{topic}</span>
                    <span className="text-muted"> / {los} / {errorLabels[error] || error}</span>
                  </div>
                  <div className="flex items-center gap-3 text-xs">
                    <span>重复 {p.recurrence} 次</span>
                    <span className={severityColors[p.severity] || 'text-muted'}>
                      {p.severity === 'high' ? '高危' : p.severity === 'medium' ? '中危' : '低危'}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Attempt selector + diagnose */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Attempt list */}
        <div className="card">
          <h3 className="text-sm font-semibold mb-3">最近错题</h3>
          <div className="space-y-1 max-h-96 overflow-auto">
            {attempts.slice(0, 20).map((a, index) => {
              const attemptKey = a.attempt_id || a.event_id || `attempt-${index}`;
              const attemptId = a.attempt_id || a.event_id || '';
              return (
                <button
                  key={attemptKey}
                  onClick={() => setSelectedId(attemptId)}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                    selectedId === attemptId
                      ? 'bg-accent-soft border border-accent-soft'
                      : 'hover:bg-surface-hover'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{a.topic}</span>
                    <span className="text-xs text-muted">{a.created_at?.slice(0, 10)}</span>
                  </div>
                  <div className="text-xs text-muted mt-0.5">
                    {a.los} · {errorLabels[a.error_type] || a.error_type} · 信心 {a.confidence}/4
                  </div>
                </button>
              );
            })}
          </div>
          <button
            onClick={runDiagnosis}
            disabled={!selectedId || diagLoading}
            className="mt-3 w-full py-2 bg-accent-solid hover:bg-accent-strong disabled:opacity-50 rounded-lg text-sm transition-colors"
          >
            {diagLoading ? '诊断中...' : '诊断选中错题'}
          </button>
        </div>

        {/* Diagnosis result */}
        <div className="card">
          <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <Stethoscope size={16} className="text-accent" /> 诊断结果
          </h3>

          {diagnosis?.error ? (
            <p className="text-sm text-danger">{diagnosis.error}</p>
          ) : diagnosis ? (
            <div className="space-y-4">
              <div className="bg-surface-field rounded-lg p-3">
                <div className="text-xs text-muted mb-1">错因</div>
                <div className="text-sm font-semibold">
                  {errorLabels[diagnosis.error_category] || diagnosis.error_category}
                </div>
                <div className="text-xs text-muted mt-1">{diagnosis.error_summary}</div>
              </div>

              <div className="bg-surface-field rounded-lg p-3">
                <div className="text-xs text-muted mb-1 flex items-center gap-1">
                  <Lightbulb size={12} /> 纠偏规则
                </div>
                <div className="text-sm">{diagnosis.fix_rule}</div>
              </div>

              <div className="bg-surface-field rounded-lg p-3">
                <div className="text-xs text-muted mb-1 flex items-center gap-1">
                  <Repeat size={12} /> 下一步练习
                </div>
                <div className="text-sm">{diagnosis.next_drill}</div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs text-muted">
                <div>间隔: {diagnosis.spacing_interval_days} 天</div>
                <div>复习日: {diagnosis.review_due_at}</div>
                <div>模式候选: {diagnosis.pattern_candidate ? '是' : '否'}</div>
                <div className="flex items-center gap-1">
                  <Link2 size={10} /> {diagnosis.linked_los?.[0] || '-'}
                </div>
              </div>

              {diagnosis.pattern_candidate && (
                <div className="flex items-center gap-2 text-xs text-warning">
                  <AlertTriangle size={12} />
                  此错误已形成重复模式，建议优先处理
                </div>
              )}
            </div>
          ) : (
            <p className="text-sm text-muted">选择一道错题，点击诊断</p>
          )}
        </div>
      </div>
    </div>
  );
}
