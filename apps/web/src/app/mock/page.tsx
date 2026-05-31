'use client';

import { useEffect, useState } from 'react';
import { mockApi, profilesApi } from '@/lib/api';
import { FileText, Play, RotateCcw, AlertTriangle, BarChart3, Plus } from 'lucide-react';

interface MockSession {
  session_id: string;
  session_label: string;
  exam_name: string;
  total_minutes: number;
  total_questions: number;
  correct_count: number;
  scheduled_date: string;
  created_at: string;
}

interface RetroData {
  session_id: string;
  question_count: number;
  bias_count: number;
  agent_count: number;
  markdown_content: string;
  stop_doing: string[];
  next_strategy: string;
}

export default function MockCenter() {
  const [sessions, setSessions] = useState<MockSession[]>([]);
  const [selectedSession, setSelectedSession] = useState('');
  const [retro, setRetro] = useState<RetroData | null>(null);
  const [brief, setBrief] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [examName, setExamName] = useState('');
  const [newMock, setNewMock] = useState({
    session_id: '',
    session_label: '',
    total_minutes: 180,
    total_questions: 90,
    correct_count: 0,
  });

  useEffect(() => {
    mockApi.listHistory().then((data: any) => {
      setSessions(data.sessions || []);
    }).finally(() => setLoading(false));
    profilesApi.getActive().then(({ profile }: any) => setExamName(profile.name)).catch(() => undefined);
  }, []);

  const createMock = async () => {
    await mockApi.create({
      ...newMock,
      exam_name: examName,
      scheduled_date: new Date().toISOString().slice(0, 10),
    });
    setShowCreate(false);
    // Refresh
    const data: any = await mockApi.listHistory();
    setSessions(data.sessions || []);
  };

  const runRetro = async (sessionId: string) => {
    setSelectedSession(sessionId);
    setRetro(null);
    try {
      const data = await mockApi.getRetro(sessionId);
      setRetro(data as RetroData);
    } catch (err: any) {
      setRetro({
        session_id: sessionId,
        question_count: 0,
        bias_count: 0,
        agent_count: 0,
        markdown_content: '',
        stop_doing: [],
        next_strategy: err.message,
      });
    }
  };

  const getBrief = async (sessionId: string) => {
    try {
      const data = await mockApi.getBrief(sessionId);
      setBrief(data);
    } catch {}
  };

  if (loading) {
    return <div className="text-muted animate-pulse">加载模拟中心...</div>;
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">模拟中心</h2>
          <p className="text-muted text-sm mt-1">Pre-mock brief · Mock 记录 · Post-mock retro · 停止做清单</p>
        </div>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="flex items-center gap-2 px-4 py-2 bg-accent-solid hover:bg-accent-strong rounded-lg text-sm transition-colors"
        >
          <Plus size={14} /> 新模拟
        </button>
      </div>

      {/* Create form */}
      {showCreate && (
        <div className="card space-y-3">
          <h3 className="text-sm font-semibold">创建模拟记录</h3>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <input
              value={newMock.session_id}
              onChange={(e) => setNewMock({ ...newMock, session_id: e.target.value })}
              className="bg-surface-field border border-line rounded-lg px-3 py-2 text-sm"
              placeholder="Session ID (e.g. mock-1)"
            />
            <input
              value={newMock.session_label}
              onChange={(e) => setNewMock({ ...newMock, session_label: e.target.value })}
              className="bg-surface-field border border-line rounded-lg px-3 py-2 text-sm"
              placeholder="标签 (e.g. Mock 1 AM)"
            />
            <input
              type="number"
              value={newMock.total_questions}
              onChange={(e) => setNewMock({ ...newMock, total_questions: Number(e.target.value) })}
              className="bg-surface-field border border-line rounded-lg px-3 py-2 text-sm"
              placeholder="总题数"
            />
          </div>
          <button onClick={createMock} className="px-4 py-1.5 bg-success-soft text-success rounded-lg text-sm">
            创建
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Session list */}
        <div className="card">
          <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <FileText size={14} className="text-accent" /> 模拟记录
          </h3>
          {sessions.length === 0 ? (
            <p className="text-xs text-muted">暂无模拟记录</p>
          ) : (
            <div className="space-y-1 max-h-80 overflow-auto">
              {sessions.map((s) => (
                <div key={s.session_id} className="space-y-0.5">
                  <button
                    onClick={() => { setSelectedSession(s.session_id); runRetro(s.session_id); getBrief(s.session_id); }}
                    className={`w-full text-left px-3 py-2 rounded-lg text-xs transition-colors ${
                      selectedSession === s.session_id
                        ? 'bg-accent-soft border border-accent-soft'
                        : 'hover:bg-surface-hover'
                    }`}
                  >
                    <div className="font-medium">{s.session_label}</div>
                    <div className="text-muted">
                      {s.total_questions} 题 · {s.correct_count} 对
                      {s.total_questions > 0 && ` · ${Math.round(s.correct_count / s.total_questions * 100)}%`}
                    </div>
                    <div className="text-[10px] text-muted">{s.created_at?.slice(0, 10)}</div>
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Pre-mock brief */}
        <div className="card">
          <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <Play size={14} className="text-success" /> Pre-Mock Brief
          </h3>
          {brief ? (
            <div className="space-y-3 text-xs">
              <div>
                <div className="text-muted mb-1">触发条件</div>
                <div>{brief.trigger}</div>
              </div>
              <div>
                <div className="text-muted mb-1">决策</div>
                <div className="font-medium">{brief.decision}</div>
              </div>
              <div>
                <div className="text-muted mb-1">为什么有效</div>
                <div>{brief.why_it_works}</div>
              </div>
            </div>
          ) : (
            <p className="text-xs text-muted">选择一个模拟查看 pre-mock brief</p>
          )}
        </div>

        {/* Post-mock retro */}
        <div className="card">
          <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <RotateCcw size={14} className="text-warning" /> Post-Mock Retro
          </h3>
          {retro ? (
            <div className="space-y-3 text-xs">
              <div className="grid grid-cols-3 gap-2">
                <div className="bg-surface-field rounded p-2 text-center">
                  <div className="text-lg font-bold text-danger">{retro.question_count}</div>
                  <div className="text-[10px] text-muted">题目错</div>
                </div>
                <div className="bg-surface-field rounded p-2 text-center">
                  <div className="text-lg font-bold text-warning">{retro.bias_count}</div>
                  <div className="text-[10px] text-muted">偏差信号</div>
                </div>
                <div className="bg-surface-field rounded p-2 text-center">
                  <div className="text-lg font-bold text-accent">{retro.agent_count}</div>
                  <div className="text-[10px] text-muted">Agent 失误</div>
                </div>
              </div>

              {retro.stop_doing.length > 0 && (
                <div>
                  <div className="text-muted mb-1 flex items-center gap-1">
                    <AlertTriangle size={10} /> 停止做的事
                  </div>
                  {retro.stop_doing.map((s, i) => (
                    <p key={i} className="text-danger text-[11px]">• {s}</p>
                  ))}
                </div>
              )}

              <div>
                <div className="text-muted mb-1">下次策略</div>
                <p>{retro.next_strategy}</p>
              </div>
            </div>
          ) : (
            <p className="text-xs text-muted">选择一个模拟查看 retro</p>
          )}
        </div>
      </div>
    </div>
  );
}
