'use client';

import { useEffect, useState } from 'react';
import { institutionApi } from '@/lib/api';
import {
  Building2, Users, AlertTriangle, GraduationCap,
  UserX, FileText, TrendingDown, Plus,
} from 'lucide-react';

interface Cohort {
  cohort_id: string;
  cohort_name: string;
  exam_target: string;
  exam_date: string;
  learner_ids: string[];
  created_at: string;
}

interface RiskReport {
  report_id: string;
  cohort_id: string;
  cohort_name: string;
  total_learners: number;
  at_risk_count: number;
  dropout_warning_count: number;
  avg_review_completion: number;
  avg_accuracy: number;
  at_risk_learners: Array<{
    learner_id: string;
    risk_score: number;
    total_errors: number;
    days_inactive: number;
  }>;
  dropout_warnings: Array<{
    learner_id: string;
    days_inactive: number;
    warning: string;
  }>;
  instructor_recommendations: string[];
  generated_at: string;
}

export default function InstitutionConsole() {
  const [cohorts, setCohorts] = useState<Cohort[]>([]);
  const [selectedCohort, setSelectedCohort] = useState('');
  const [riskReport, setRiskReport] = useState<RiskReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newCohort, setNewCohort] = useState({
    institution_id: 'inst-001',
    cohort_name: '',
    exam_target: 'CFA Level I',
    exam_date: '',
    learner_ids: '',
  });

  useEffect(() => {
    institutionApi.listCohorts().then((data: any) => {
      setCohorts(data.cohorts || []);
    }).finally(() => setLoading(false));
  }, []);

  const createCohort = async () => {
    await institutionApi.createCohort({
      ...newCohort,
      learner_ids: newCohort.learner_ids.split(',').map((s: string) => s.trim()).filter(Boolean),
    });
    setShowCreate(false);
    const data: any = await institutionApi.listCohorts();
    setCohorts(data.cohorts || []);
  };

  const loadRiskReport = async (cohortId: string) => {
    setSelectedCohort(cohortId);
    const report = await institutionApi.getRiskReport(cohortId);
    setRiskReport(report as RiskReport);
  };

  if (loading) {
    return <div className="text-muted animate-pulse">加载机构控制台...</div>;
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">机构控制台</h2>
          <p className="text-muted text-sm mt-1">班级风险榜 · 掉队预警 · 学员周报 · 老师干预建议 · 续费/交付证明</p>
        </div>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="flex items-center gap-2 px-4 py-2 bg-[#6366f1] hover:bg-[#5558e6] rounded-lg text-sm transition-colors"
        >
          <Plus size={14} /> 新建班级
        </button>
      </div>

      {/* Create cohort form */}
      {showCreate && (
        <div className="card space-y-3">
          <h3 className="text-sm font-semibold">创建班级</h3>
          <div className="grid grid-cols-3 gap-3">
            <input
              value={newCohort.cohort_name}
              onChange={(e) => setNewCohort({ ...newCohort, cohort_name: e.target.value })}
              className="bg-[#0a0a0f] border border-[#1e1e2e] rounded-lg px-3 py-2 text-sm"
              placeholder="班级名称"
            />
            <input
              value={newCohort.exam_date}
              onChange={(e) => setNewCohort({ ...newCohort, exam_date: e.target.value })}
              className="bg-[#0a0a0f] border border-[#1e1e2e] rounded-lg px-3 py-2 text-sm"
              placeholder="考试日期 YYYY-MM-DD"
            />
            <input
              value={newCohort.learner_ids}
              onChange={(e) => setNewCohort({ ...newCohort, learner_ids: e.target.value })}
              className="bg-[#0a0a0f] border border-[#1e1e2e] rounded-lg px-3 py-2 text-sm"
              placeholder="学员 ID (逗号分隔)"
            />
          </div>
          <button onClick={createCohort} className="px-4 py-1.5 bg-[#22c55e]/20 text-success rounded-lg text-sm">
            创建
          </button>
        </div>
      )}

      <div className="grid grid-cols-3 gap-6">
        {/* Cohort list */}
        <div className="card">
          <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <GraduationCap size={14} className="text-accent" /> 班级列表
          </h3>
          {cohorts.length === 0 ? (
            <p className="text-xs text-muted">暂无班级</p>
          ) : (
            <div className="space-y-1 max-h-80 overflow-auto">
              {cohorts.map((c) => (
                <button
                  key={c.cohort_id}
                  onClick={() => loadRiskReport(c.cohort_id)}
                  className={`w-full text-left px-3 py-2 rounded-lg text-xs transition-colors ${
                    selectedCohort === c.cohort_id
                      ? 'bg-[#6366f1]/15 border border-[#6366f1]/30'
                      : 'hover:bg-[#14141f]'
                  }`}
                >
                  <div className="font-medium">{c.cohort_name}</div>
                  <div className="text-muted">
                    {c.learner_ids.length} 学员 · {c.exam_target} · 考试 {c.exam_date}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Risk report */}
        <div className="col-span-2 space-y-4">
          {riskReport ? (
            <>
              {/* Summary metrics */}
              <div className="grid grid-cols-4 gap-3">
                <MiniCard icon={<Users size={14} className="text-accent" />} label="总学员" value={String(riskReport.total_learners)} />
                <MiniCard icon={<AlertTriangle size={14} className="text-danger" />} label="风险学员" value={String(riskReport.at_risk_count)} />
                <MiniCard icon={<UserX size={14} className="text-warning" />} label="掉队预警" value={String(riskReport.dropout_warning_count)} />
                <MiniCard icon={<TrendingDown size={14} className="text-muted" />} label="平均完成率" value={`${(riskReport.avg_review_completion * 100).toFixed(0)}%`} />
              </div>

              {/* At-risk learners */}
              <div className="card">
                <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
                  <AlertTriangle size={14} className="text-danger" /> 风险学员榜
                </h3>
                {riskReport.at_risk_learners.length === 0 ? (
                  <p className="text-xs text-muted">暂无风险学员</p>
                ) : (
                  <div className="space-y-1">
                    {riskReport.at_risk_learners.slice(0, 10).map((l, i) => (
                      <div key={i} className="flex items-center justify-between text-xs bg-[#0a0a0f] rounded-lg px-3 py-2">
                        <span className="font-medium">{l.learner_id}</span>
                        <div className="flex items-center gap-3 text-muted">
                          <span>风险分 {l.risk_score}</span>
                          <span>{l.total_errors} 错题</span>
                          <span className={l.days_inactive >= 7 ? 'text-danger' : ''}>
                            不活跃 {l.days_inactive} 天
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Dropout warnings */}
              {riskReport.dropout_warnings.length > 0 && (
                <div className="card border-[#f59e0b]/30">
                  <h3 className="text-sm font-semibold mb-3 flex items-center gap-2 text-warning">
                    <UserX size={14} /> 掉队预警
                  </h3>
                  {riskReport.dropout_warnings.map((w, i) => (
                    <p key={i} className="text-xs text-warning">• {w.warning}</p>
                  ))}
                </div>
              )}

              {/* Instructor recommendations */}
              {riskReport.instructor_recommendations.length > 0 && (
                <div className="card border-[#6366f1]/30">
                  <h3 className="text-sm font-semibold mb-3 flex items-center gap-2 text-accent">
                    <FileText size={14} /> 老师干预建议
                  </h3>
                  {riskReport.instructor_recommendations.map((r, i) => (
                    <p key={i} className="text-xs">• {r}</p>
                  ))}
                </div>
              )}

              {/* Delivery proof metrics */}
              <div className="card">
                <h3 className="text-sm font-semibold mb-2">交付证明</h3>
                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div>
                    <span className="text-muted">平均复习完成率:</span>{' '}
                    <span className="font-medium">{(riskReport.avg_review_completion * 100).toFixed(0)}%</span>
                  </div>
                  <div>
                    <span className="text-muted">风险学员占比:</span>{' '}
                    <span className="font-medium">
                      {riskReport.total_learners > 0
                        ? `${((riskReport.at_risk_count / riskReport.total_learners) * 100).toFixed(0)}%`
                        : '0%'}
                    </span>
                  </div>
                  <div>
                    <span className="text-muted">生成时间:</span>{' '}
                    <span className="font-medium">{riskReport.generated_at}</span>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="card text-center py-12 text-muted">
              <Building2 size={32} className="mx-auto mb-3 opacity-50" />
              <p>选择一个班级查看风险报告</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function MiniCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-1">{icon}<span className="metric-label">{label}</span></div>
      <div className="metric-value text-lg">{value}</div>
    </div>
  );
}
