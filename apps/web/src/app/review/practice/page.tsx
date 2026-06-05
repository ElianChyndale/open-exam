'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { questionBanksApi } from '@/lib/api';
import { useProfileSubjects } from '@/lib/profiles';

type Phase = 'config' | 'session' | 'result';

interface SessionData {
  session_id: string;
  question_count: number;
  question_ids: string[];
  question_refs: { question_id: string; topic: string; module: string; los: string }[];
}

interface QuestionDisplay {
  session_id: string;
  question_id: string;
  state: string;
  prompt: string;
  choices: string[];
  exam: string;
  topic: string;
  module: string;
  los: string;
  note_count: number;
  favorite: boolean;
}

interface AnswerResult {
  attempt: any;
  wrongbook_record: any;
  note: any;
  favorite: any;
  feedback: { is_correct: boolean; correct_answer: string };
}

export default function PracticePage() {
  const router = useRouter();
  const subjects = useProfileSubjects();
  const [phase, setPhase] = useState<Phase>('config');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Config
  const [config, setConfig] = useState({
    subject: '',
    chapter: '',
    difficulty: '',
    count: 10,
  });

  // Session
  const [session, setSession] = useState<SessionData | null>(null);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [question, setQuestion] = useState<QuestionDisplay | null>(null);
  const [selected, setSelected] = useState('');
  const [answerResult, setAnswerResult] = useState<AnswerResult | null>(null);
  const [results, setResults] = useState<AnswerResult[]>([]);
  const [note, setNote] = useState('');
  const [isFavorite, setIsFavorite] = useState(false);
  const [timer, setTimer] = useState(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Load question when index changes
  const loadQuestion = useCallback(async (sessionId: string, qid: string) => {
    try {
      const q = await questionBanksApi.getPracticeSessionQuestion(sessionId, qid);
      setQuestion(q);
      setSelected('');
      setAnswerResult(null);
      setIsFavorite(q.favorite || false);
      setNote('');
    } catch (err: any) {
      setError(err.message);
    }
  }, []);

  // Start session
  const startSession = async () => {
    setLoading(true);
    setError('');
    try {
      const payload: any = { count: config.count };
      if (config.subject) payload.topic = config.subject;
      if (config.chapter) payload.chapter = config.chapter;
      if (config.difficulty) payload.difficulty = config.difficulty;
      const data = await questionBanksApi.createPracticeSession(payload);
      setSession(data);
      setResults([]);
      setCurrentIdx(0);
      setPhase('session');
      if (data.question_ids?.length > 0) {
        await loadQuestion(data.session_id, data.question_ids[0]);
      }
      // Start timer
      timerRef.current = setInterval(() => setTimer((t) => t + 1), 1000);
    } catch (err: any) {
      setError(err.message);
    }
    setLoading(false);
  };

  // Submit answer
  const submitAnswer = async () => {
    if (!session || !question || !selected) return;
    try {
      const result = await questionBanksApi.submitAnswer(session.session_id, {
        question_id: question.question_id,
        selected_answer: selected,
        time_spent: timer,
        note: note || undefined,
        favorite: isFavorite,
      });
      setAnswerResult(result);
      setResults((prev) => [...prev, result]);
    } catch (err: any) {
      setError(err.message);
    }
  };

  // Next question
  const nextQuestion = async () => {
    if (!session) return;
    const nextIdx = currentIdx + 1;
    if (nextIdx >= session.question_ids.length) {
      // End of session
      if (timerRef.current) clearInterval(timerRef.current);
      setPhase('result');
      return;
    }
    setCurrentIdx(nextIdx);
    setTimer(0);
    await loadQuestion(session.session_id, session.question_ids[nextIdx]);
  };

  // Cleanup timer
  useEffect(() => {
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, []);

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, '0')}`;
  };

  const correctCount = results.filter((r) => r.feedback?.is_correct).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-200">
      {/* ─── CONFIG SCREEN ─── */}
      {phase === 'config' && (
        <div className="max-w-2xl mx-auto p-6 pt-12">
          <h1 className="text-2xl font-bold text-white mb-2">📝 章节练习</h1>
          <p className="text-slate-400 text-sm mb-8">选择科目和参数，生成个性化练习</p>

          <div className="space-y-5">
            <div>
              <label className="text-xs text-slate-400 block mb-1.5">科目</label>
              <select
                value={config.subject}
                onChange={(e) => setConfig({ ...config, subject: e.target.value })}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
              >
                <option value="">全部科目</option>
                {subjects.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs text-slate-400 block mb-1.5">章节</label>
              <input
                type="text"
                value={config.chapter}
                onChange={(e) => setConfig({ ...config, chapter: e.target.value })}
                placeholder="例如: M01 或 Time Value (留空=全部)"
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-slate-400 block mb-1.5">难度</label>
                <select
                  value={config.difficulty}
                  onChange={(e) => setConfig({ ...config, difficulty: e.target.value })}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
                >
                  <option value="">全部</option>
                  <option value="easy">简单</option>
                  <option value="medium">中等</option>
                  <option value="hard">困难</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-slate-400 block mb-1.5">题目数</label>
                <input
                  type="number"
                  value={config.count}
                  onChange={(e) => setConfig({ ...config, count: Math.max(1, Math.min(100, Number(e.target.value))) })}
                  min={1}
                  max={100}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
                />
              </div>
            </div>

            {error && (
              <div className="bg-red-900/20 border border-red-700/30 rounded-lg p-3 text-sm text-red-300">{error}</div>
            )}

            <button
              onClick={startSession}
              disabled={loading}
              className="w-full py-3 bg-amber-600 hover:bg-amber-500 disabled:bg-slate-700 disabled:text-slate-500 rounded-xl font-medium text-base transition-all"
            >
              {loading ? '生成练习中…' : '开始练习'}
            </button>
          </div>
        </div>
      )}

      {/* ─── SESSION SCREEN ─── */}
      {phase === 'session' && session && (
        <div className="flex h-screen flex-col">
          {/* Top bar */}
          <div className="flex items-center justify-between px-4 py-2 bg-slate-900/80 border-b border-slate-700/50 shrink-0">
            <div className="flex items-center gap-3 text-sm">
              <span className="text-slate-400">
                {currentIdx + 1} / {session.question_ids.length}
              </span>
              <span className="text-slate-600">·</span>
              <span className="text-slate-400">{question?.topic || ''}</span>
              <span className="text-slate-600">·</span>
              <span className="text-slate-500">{question?.module || ''}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-sm font-mono text-slate-400">{formatTime(timer)}</span>
              <button
                onClick={() => router.push('/review')}
                className="text-xs text-slate-500 hover:text-slate-300"
              >
                退出
              </button>
            </div>
          </div>

          {/* Main area */}
          <div className="flex flex-1 overflow-hidden">
            {/* Answer card sidebar */}
            <div className="w-16 bg-slate-900/50 border-r border-slate-700/30 p-2 flex flex-col items-center gap-1 overflow-y-auto shrink-0">
              {session.question_ids.map((qid, i) => {
                const res = results.find((r) => r.attempt?.question_id === qid);
                let bg = 'bg-slate-700/50';
                if (res?.feedback?.is_correct) bg = 'bg-emerald-700/60';
                else if (res && !res.feedback?.is_correct) bg = 'bg-red-700/60';
                return (
                  <button
                    key={qid}
                    onClick={() => {
                      if (answerResult) {
                        setCurrentIdx(i);
                        setTimer(0);
                        loadQuestion(session.session_id, qid);
                      }
                    }}
                    className={`w-10 h-10 rounded-lg text-xs font-medium transition-colors ${i === currentIdx ? 'ring-2 ring-amber-500' : ''} ${bg} ${answerResult ? 'cursor-pointer' : 'cursor-default'}`}
                  >
                    {i + 1}
                  </button>
                );
              })}
            </div>

            {/* Question area */}
            <div className="flex-1 overflow-y-auto p-6">
              {question && (
                <div className="max-w-3xl">
                  <p className="text-lg leading-relaxed mb-6 text-white">{question.prompt}</p>

                  <div className="space-y-2.5 mb-6">
                    {question.choices.map((choice: string, i: number) => {
                      const label = String.fromCharCode(65 + i);
                      const isSelected = selected === label;
                      let borderClass = 'border-slate-700/50 hover:border-slate-500';
                      if (answerResult) {
                        if (label === answerResult.feedback.correct_answer) {
                          borderClass = 'border-emerald-500 bg-emerald-900/20';
                        } else if (isSelected && !answerResult.feedback.is_correct) {
                          borderClass = 'border-red-500 bg-red-900/20';
                        } else {
                          borderClass = 'border-slate-700/30 opacity-50';
                        }
                      } else if (isSelected) {
                        borderClass = 'border-amber-500/60 bg-amber-900/10';
                      }

                      return (
                        <button
                          key={i}
                          disabled={!!answerResult}
                          onClick={() => setSelected(label)}
                          className={`w-full text-left p-3.5 rounded-xl border ${borderClass} transition-all disabled:cursor-default`}
                        >
                          <span className="font-mono text-sm text-slate-400 mr-3">{label}.</span>
                          {choice.replace(/^[A-Z][\.\)]\s*/, '')}
                        </button>
                      );
                    })}
                  </div>

                  {/* Feedback */}
                  {answerResult && (
                    <div className={`p-4 rounded-xl mb-6 ${answerResult.feedback.is_correct ? 'bg-emerald-900/20 border border-emerald-700/30' : 'bg-red-900/20 border border-red-700/30'}`}>
                      <p className="font-semibold text-lg mb-1">
                        {answerResult.feedback.is_correct ? '✅ 正确！' : '❌ 错误'}
                      </p>
                      <p className="text-sm text-slate-400">
                        正确答案：<span className="text-emerald-400 font-mono">{answerResult.feedback.correct_answer}</span>
                      </p>
                      {answerResult.wrongbook_record && (
                        <p className="text-xs text-slate-500 mt-1">
                          已记入错题本（已错 {answerResult.wrongbook_record.wrong_count} 次）
                        </p>
                      )}
                    </div>
                  )}

                  {/* Notes & Favorite */}
                  {answerResult && (
                    <div className="border-t border-slate-700/30 pt-4 space-y-3 mb-6">
                      <div className="flex items-center gap-4">
                        <button
                          onClick={() => setIsFavorite(!isFavorite)}
                          className={`text-lg ${isFavorite ? 'text-amber-400' : 'text-slate-600 hover:text-slate-400'}`}
                        >
                          {isFavorite ? '★' : '☆'}
                        </button>
                        <span className="text-xs text-slate-500">{isFavorite ? '已收藏' : '收藏本题'}</span>
                      </div>
                      <div>
                        <textarea
                          value={note}
                          onChange={(e) => setNote(e.target.value)}
                          placeholder="记录解题思路…"
                          rows={2}
                          className="w-full bg-slate-800/50 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-600 resize-none"
                        />
                        {answerResult.note && (
                          <p className="text-xs text-emerald-400 mt-1">✅ 笔记已保存</p>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Action buttons */}
                  <div className="flex gap-3 pb-8">
                    {!answerResult ? (
                      <button
                        onClick={submitAnswer}
                        disabled={!selected}
                        className="px-8 py-2.5 bg-amber-600 hover:bg-amber-500 disabled:bg-slate-700 disabled:text-slate-500 rounded-xl font-medium transition-all"
                      >
                        提交答案
                      </button>
                    ) : (
                      <button
                        onClick={nextQuestion}
                        className="px-8 py-2.5 bg-slate-700 hover:bg-slate-600 rounded-xl font-medium transition-all"
                      >
                        {currentIdx + 1 >= session.question_ids.length ? '查看结果' : '下一题 →'}
                      </button>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ─── RESULT SCREEN ─── */}
      {phase === 'result' && (
        <div className="max-w-3xl mx-auto p-6 pt-12">
          <h1 className="text-2xl font-bold text-white mb-2">📊 练习结果</h1>
          <p className="text-slate-400 text-sm mb-8">
            共 {session?.question_ids.length || 0} 题 · 正确 {correctCount} 题 · 正确率{' '}
            {session ? Math.round((correctCount / session.question_ids.length) * 100) : 0}%
          </p>

          <div className="space-y-2 mb-8">
            {results.map((r, i) => (
              <div
                key={i}
                className={`flex items-center gap-4 p-3 rounded-xl border ${
                  r.feedback.is_correct ? 'bg-emerald-900/10 border-emerald-700/20' : 'bg-red-900/10 border-red-700/20'
                }`}
              >
                <span className="text-lg">{r.feedback.is_correct ? '✅' : '❌'}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm truncate">{r.attempt?.question_id || `第 ${i + 1} 题`}</p>
                  <p className="text-xs text-slate-500">
                    你的答案: {r.attempt?.selected_answer || '-'} · 正确答案: {r.feedback.correct_answer}
                    {r.attempt?.time_spent ? ` · ${r.attempt.time_spent}s` : ''}
                  </p>
                </div>
                {r.wrongbook_record && (
                  <span className="text-xs text-slate-500 shrink-0">错 {r.wrongbook_record.wrong_count} 次</span>
                )}
              </div>
            ))}
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => { setPhase('config'); setSession(null); setResults([]); }}
              className="px-6 py-2.5 bg-slate-700 hover:bg-slate-600 rounded-xl font-medium transition-all"
            >
              再做一组
            </button>
            <button
              onClick={() => router.push('/review/wrongbook')}
              className="px-6 py-2.5 bg-slate-700 hover:bg-slate-600 rounded-xl font-medium transition-all"
            >
              查看错题本
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
