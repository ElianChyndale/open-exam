'use client';

import { useEffect, useState } from 'react';
import { dashboardApi } from '@/lib/api';
import { Calendar, ChevronLeft, ChevronRight, AlertTriangle } from 'lucide-react';

export default function CalendarPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [examDate, setExamDate] = useState('');
  const [currentMonth, setCurrentMonth] = useState(() => {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
  });

  useEffect(() => {
    dashboardApi.getCalendarData(currentMonth).then((next: any) => {
      setData(next);
      setExamDate(next.exam_date || '');
    }).finally(() => setLoading(false));
  }, [currentMonth]);

  const [year, month] = currentMonth.split('-').map(Number);
  const daysInMonth = new Date(year, month, 0).getDate();
  const firstDay = new Date(year, month - 1, 1).getDay();
  const today = new Date().toISOString().slice(0, 10);

  if (loading) return <div className="text-muted animate-pulse">加载日历...</div>;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">学习日历</h2>
          <p className="text-muted text-sm mt-1">查看每日学习活动和考试倒计时</p>
        </div>
        {data?.countdown_days > 0 && (
          <div className="card flex items-center gap-3 px-4 py-3">
            <AlertTriangle size={18} className={data.countdown_days < 30 ? 'text-danger' : 'text-warning'} />
            <div>
              <div className="metric-label">距离考试</div>
              <div className="metric-value text-lg">{data.countdown_days} 天</div>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <button onClick={() => {
            const d = new Date(year, month - 2, 1);
            setCurrentMonth(`${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`);
          }} className="p-2 hover:bg-surface-hover rounded-lg transition-colors">
            <ChevronLeft size={18} />
          </button>
          <span className="text-lg font-semibold">{year}年{month}月</span>
          <button onClick={() => {
            const d = new Date(year, month, 1);
            setCurrentMonth(`${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`);
          }} className="p-2 hover:bg-surface-hover rounded-lg transition-colors">
            <ChevronRight size={18} />
          </button>
        </div>

        <div className="grid grid-cols-7 gap-1 mb-2">
          {['日', '一', '二', '三', '四', '五', '六'].map(d => (
            <div key={d} className="text-center text-xs text-muted py-1">{d}</div>
          ))}
        </div>

        <div className="grid grid-cols-7 gap-1">
          {Array.from({ length: firstDay }, (_, i) => (
            <div key={`empty-${i}`} className="aspect-square" />
          ))}
          {Array.from({ length: daysInMonth }, (_, i) => {
            const day = i + 1;
            const dateStr = `${currentMonth}-${String(day).padStart(2, '0')}`;
            const isToday = dateStr === today;
            const errors = data?.daily_errors?.[dateStr] || 0;
            const reviewed = data?.review_days?.includes(dateStr);

            return (
              <div key={day} className={`aspect-square rounded-lg p-1 flex flex-col items-center justify-center text-sm border transition-colors ${
                isToday ? 'border-accent bg-accent-soft' : 'border-transparent hover:border-line'
              }`}>
                <span className={isToday ? 'text-accent font-bold' : ''}>{day}</span>
                <div className="flex gap-0.5 mt-0.5">
                  {errors > 0 && <span className="w-1.5 h-1.5 rounded-full bg-danger-solid" title={`${errors} 错题`} />}
                  {reviewed && <span className="w-1.5 h-1.5 rounded-full bg-success-solid" title="已复习" />}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="card flex items-center gap-6 text-xs text-muted">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-danger-solid" /> 有错题
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-success-solid" /> 已完成复习
        </div>
        {data?.exam_date && (
          <div>
            考试日: {data.exam_date} ({data.countdown_days} 天后)
          </div>
        )}
      </div>

      <div className="card flex flex-wrap items-end gap-3">
        <label className="space-y-1 text-xs text-muted">
          <span className="block">考试日期</span>
          <input type="date" value={examDate} onChange={(event) => setExamDate(event.target.value)}
            className="rounded-lg border border-line bg-surface-field px-3 py-2 text-sm text-ink" />
        </label>
        <button onClick={() => dashboardApi.updateCalendarSettings(examDate).then(() => {
          setLoading(true);
          return dashboardApi.getCalendarData(currentMonth).then(setData).finally(() => setLoading(false));
        })} className="rounded-lg bg-accent-solid px-4 py-2 text-sm text-white hover:bg-accent-strong">
          保存日历设置
        </button>
      </div>
    </div>
  );
}
