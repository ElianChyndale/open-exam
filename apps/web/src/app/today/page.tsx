'use client';

import { useEffect, useState } from 'react';
import { studyPlanApi, energyApi } from '@/lib/api';
import {
  Zap, Clock, Target, AlertTriangle, CheckCircle2, Brain, Battery, BatteryLow, BatteryMedium, BatteryFull,
} from 'lucide-react';

interface PlanData {
  plan_id: string;
  date: string;
  energy_level: number;
  available_minutes: number;
  focus_topic: string;
  focus_reason: string;
  high_energy_tasks: Task[];
  moderate_energy_tasks: Task[];
  low_energy_tasks: Task[];
  danger_los_list: string[];
  warnings: string[];
}

interface Task {
  task_type: string;
  description: string;
  fit: number;
}

const taskLabels: Record<string, string> = {
  new_knowledge: '新知识',
  difficult_practice: '高难练习',
  interleaved_set: '交错题组',
  mock_exam: '模拟考试',
  mistake_review: '错题复盘',
  formula_drill: '公式练习',
  worked_example_fading: '例题渐隐',
  active_recall: '主动回忆',
  concept_discrimination: '概念判断',
  light_review: '轻量复习',
};

export default function TodayCockpit() {
  const [plan, setPlan] = useState<PlanData | null>(null);
  const [loading, setLoading] = useState(true);
  const [weeklyFocus, setWeeklyFocus] = useState('');

  useEffect(() => {
    studyPlanApi.getToday().then(setPlan).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    studyPlanApi.getWeeklyFocus().then((data: any) => {
      setWeeklyFocus(data.recommendation || '');
    }).catch(() => {});
  }, []);

  const EnergyIcon = plan
    ? plan.energy_level >= 3 ? BatteryFull
    : plan.energy_level >= 1 ? BatteryMedium
    : BatteryLow
    : Battery;

  if (loading) {
    return <div className="text-muted animate-pulse">加载今日驾驶舱...</div>;
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">今日驾驶舱</h2>
          <p className="text-muted text-sm mt-1">{plan?.date}</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="card flex items-center gap-3">
            <Clock size={18} className="text-accent" />
            <div>
              <div className="metric-label">可用时间</div>
              <div className="metric-value text-lg">{plan?.available_minutes} min</div>
            </div>
          </div>
        </div>
      </div>

      {/* Warnings */}
      {plan?.warnings && plan.warnings.length > 0 && (
        <div className="bg-[#f59e0b]/10 border border-[#f59e0b]/30 rounded-lg p-4">
          {plan.warnings.map((w, i) => (
            <p key={i} className="text-sm text-[#f59e0b] flex items-center gap-2">
              <AlertTriangle size={14} /> {w}
            </p>
          ))}
        </div>
      )}

      {/* Focus + Danger */}
      <div className="grid grid-cols-2 gap-4">
        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <Target size={16} className="text-accent" />
            <span className="metric-label">今日主线</span>
          </div>
          <p className="text-lg font-semibold">{plan?.focus_topic || '按到期错题安排'}</p>
          <p className="text-xs text-muted mt-1">{plan?.focus_reason}</p>
        </div>

        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle size={16} className="text-danger" />
            <span className="metric-label">最危险 3 个 LOS</span>
          </div>
          {plan?.danger_los_list.map((los, i) => (
            <p key={i} className="text-sm text-danger">• {los}</p>
          ))}
          {(!plan?.danger_los_list || plan.danger_los_list.length === 0) && (
            <p className="text-sm text-muted">暂无高危 LOS</p>
          )}
        </div>
      </div>

      {/* Weekly Focus */}
      {weeklyFocus && (
        <div className="card col-span-2">
          <h3 className="text-sm font-semibold mb-2">📋 本周重点建议</h3>
          <pre className="text-xs text-muted whitespace-pre-wrap font-sans leading-relaxed">
            {weeklyFocus.split('\n').slice(4, 12).join('\n')}
          </pre>
        </div>
      )}

      {/* Tasks by energy tier */}
      <div className="grid grid-cols-3 gap-4">
        <TaskColumn
          title="高精力任务"
          icon={<BatteryFull size={16} className="text-success" />}
          tasks={plan?.high_energy_tasks || []}
          color="success"
        />
        <TaskColumn
          title="中精力任务"
          icon={<BatteryMedium size={16} className="text-warning" />}
          tasks={plan?.moderate_energy_tasks || []}
          color="warning"
        />
        <TaskColumn
          title="低精力任务"
          icon={<BatteryLow size={16} className="text-muted" />}
          tasks={plan?.low_energy_tasks || []}
          color="muted"
        />
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
          <Zap size={16} className="text-accent" /> 快速操作
        </h3>
        <div className="flex gap-3 flex-wrap">
          <QuickAction href="/capture" label="录入错题" />
          <QuickAction href="/review" label="打开今日复习包" />
          <QuickAction href="/diagnosis" label="错因诊断" />
          <QuickAction href="/mock" label="模拟中心" />
        </div>
      </div>
    </div>
  );
}

function TaskColumn({
  title, icon, tasks, color,
}: {
  title: string; icon: React.ReactNode; tasks: Task[]; color: string;
}) {
  if (tasks.length === 0) {
    return (
      <div className="card">
        <div className="flex items-center gap-2 mb-3">
          {icon}
          <span className="metric-label">{title}</span>
        </div>
        <p className="text-xs text-muted">暂无</p>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-3">
        {icon}
        <span className="metric-label">{title} ({tasks.length})</span>
      </div>
      <ul className="space-y-2">
        {tasks.map((task, i) => (
          <li key={i} className="text-sm flex items-start gap-2">
            <CheckCircle2 size={14} className="mt-0.5 shrink-0 text-muted" />
            <span>{taskLabels[task.task_type] || task.task_type}: {task.description.slice(0, 40)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function QuickAction({ href, label }: { href: string; label: string }) {
  return (
    <a
      href={href}
      className="px-4 py-2 rounded-lg bg-[#6366f1]/10 border border-[#6366f1]/30 text-sm text-[#818cf8] hover:bg-[#6366f1]/20 transition-colors"
    >
      {label}
    </a>
  );
}
