'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { questionBanksApi } from '@/lib/api';

export default function WrongbookQuestionPage() {
  const { question_id } = useParams<{ question_id: string }>();
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [note, setNote] = useState('');
  const [isFavorite, setIsFavorite] = useState(false);
  const [savingNote, setSavingNote] = useState(false);
  const [noteSaved, setNoteSaved] = useState(false);
  const [answerResult, setAnswerResult] = useState<any>(null);
  const [sessionId, setSessionId] = useState('');

  useEffect(() => {
    if (!question_id) return;
    questionBanksApi.getWrongbookQuestion(question_id).then((res) => {
      setData(res);
      setIsFavorite(res.question?.favorite || false);
      setLoading(false);
    });
  }, [question_id]);

  const submitAnswerToApi = useCallback(async () => {
    if (!data || !selected) return;
    setSubmitting(true);
    try {
      // Create a quick practice session for this subject/chapter
      const q = data.question;
      const session = await questionBanksApi.createPracticeSession({
        topic: q.subject || q.topic,
        count: 5,
      });
      setSessionId(session.session_id);

      // Check if our question is in the session
      if (session.question_ids?.includes(question_id)) {
        // Submit via API — this persists wrongbook/notes/favorites
        const result = await questionBanksApi.submitAnswer(session.session_id, {
          question_id,
          selected_answer: selected,
          time_spent: 0,
          note: note || undefined,
          favorite: isFavorite,
        });
        setAnswerResult(result);
        // Refresh data to show updated wrongbook + attempts
        const fresh = await questionBanksApi.getWrongbookQuestion(question_id);
        setData(fresh);
      } else {
        // Fallback: client-side check (question not in generated session)
        setAnswerResult({
          feedback: { is_correct: selected === q.answer, correct_answer: q.answer }
        });
      }
    } catch (err: any) {
      // Fallback: client-side check
      setAnswerResult({
        feedback: { is_correct: selected === data.question.answer, correct_answer: data.question.answer }
      });
    }
    setSubmitted(true);
    setSubmitting(false);
  }, [data, selected, note, isFavorite, question_id]);

  const handleRetry = () => {
    setSelected('');
    setSubmitted(false);
    setAnswerResult(null);
  };

  const handleToggleFavorite = async () => {
    // Toggle UI immediately, will persist via API on next submit
    setIsFavorite(!isFavorite);
    // Also try to persist if we have a session
    if (sessionId) {
      try {
        await questionBanksApi.submitAnswer(sessionId, {
          question_id,
          selected_answer: selected || 'A',
          favorite: !isFavorite,
        });
      } catch { /* silent */ }
    }
  };

  const handleSaveNote = async () => {
    setSavingNote(true);
    if (sessionId) {
      try {
        await questionBanksApi.submitAnswer(sessionId, {
          question_id,
          selected_answer: selected || 'A',
          note: note,
        });
        setNoteSaved(true);
      } catch { /* silent */ }
    } else {
      setNoteSaved(true);
    }
    setSavingNote(false);
    setTimeout(() => setNoteSaved(false), 2000);
  };

  const startPracticeSession = () => {
    const q = data?.question;
    const params = new URLSearchParams();
    if (q?.subject) params.set('topic', q.subject);
    if (q?.chapter) params.set('chapter', q.chapter);
    router.push(`/review/practice?${params.toString()}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-200 p-6 flex items-center justify-center">
        <p className="text-slate-500">加载中…</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-200 p-6">
        <div className="max-w-3xl mx-auto text-center py-16 text-slate-500">题目未找到</div>
      </div>
    );
  }

  const q = data.question;
  const wb = data.wrongbook || {};
  const choices: string[] = q.choices || [];
  const isCorrect = answerResult?.feedback?.is_correct;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-200 p-6">
      <div className="max-w-3xl mx-auto">
        {/* Back */}
        <button onClick={() => router.push('/review/wrongbook')} className="text-sm text-slate-500 hover:text-slate-300 mb-4">
          ← 返回错题本
        </button>

        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span className="text-xs bg-red-900/40 text-red-300 px-2 py-0.5 rounded-full">
                错 {wb.wrong_count || 0} 次
              </span>
              <span className="text-xs bg-emerald-900/40 text-emerald-300 px-2 py-0.5 rounded-full">
                对 {wb.correct_retry_count || 0} 次
              </span>
              <span className="text-xs text-slate-500">{q.subject}</span>
              <span className="text-xs text-slate-600">·</span>
              <span className="text-xs text-slate-500">{q.chapter}</span>
            </div>
            <h1 className="text-lg font-semibold text-white leading-relaxed">{q.prompt}</h1>
          </div>
          <button
            onClick={handleToggleFavorite}
            className={`shrink-0 text-xl ${isFavorite ? 'text-amber-400' : 'text-slate-600 hover:text-slate-400'}`}
            title={isFavorite ? '取消收藏' : '收藏'}
          >
            {isFavorite ? '★' : '☆'}
          </button>
        </div>

        {/* Choices */}
        <div className="space-y-2 mb-6">
          {choices.map((choice: string, i: number) => {
            const label = String.fromCharCode(65 + i);
            const isSelected = selected === label;
            const isAnswer = label === (answerResult?.feedback?.correct_answer || q.answer);
            let borderClass = 'border-slate-700/50 hover:border-slate-500';
            if (submitted) {
              if (isAnswer) borderClass = 'border-emerald-500 bg-emerald-900/20';
              else if (isSelected && !isCorrect) borderClass = 'border-red-500 bg-red-900/20';
              else borderClass = 'border-slate-700/30 opacity-60';
            } else if (isSelected) {
              borderClass = 'border-amber-500/60 bg-amber-900/10';
            }
            return (
              <button
                key={i}
                disabled={submitted}
                onClick={() => setSelected(label)}
                className={`w-full text-left p-3 rounded-lg border ${borderClass} transition-all disabled:cursor-default`}
              >
                <span className="font-mono text-sm text-slate-400 mr-3">{label}.</span>
                {choice.replace(/^[A-Z][\.\)]\s*/, '')}
              </button>
            );
          })}
        </div>

        {/* Submit / Retry / Practice buttons */}
        <div className="flex gap-3 mb-8 flex-wrap">
          {!submitted ? (
            <button
              onClick={submitAnswerToApi}
              disabled={!selected || submitting}
              className="px-6 py-2 bg-amber-600 hover:bg-amber-500 disabled:bg-slate-700 disabled:text-slate-500 rounded-lg font-medium transition-all"
            >
              {submitting ? '提交中…' : '提交答案'}
            </button>
          ) : (
            <button onClick={handleRetry} className="px-6 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg font-medium transition-all">
              重新作答
            </button>
          )}
          <button onClick={startPracticeSession} className="px-6 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg font-medium transition-all">
            同类练习 →
          </button>
        </div>

        {/* Result */}
        {submitted && answerResult && (
          <div className={`p-4 rounded-xl mb-6 ${isCorrect ? 'bg-emerald-900/20 border border-emerald-700/30' : 'bg-red-900/20 border border-red-700/30'}`}>
            <p className="font-semibold text-lg mb-1">{isCorrect ? '✅ 正确！' : '❌ 错误'}</p>
            {!isCorrect && (
              <p className="text-sm text-slate-400">
                正确答案：<span className="text-emerald-400 font-mono">{answerResult.feedback.correct_answer}</span>
              </p>
            )}
            {answerResult.wrongbook_record && (
              <p className="text-xs text-amber-400 mt-1">已记入错题本（已错 {answerResult.wrongbook_record.wrong_count} 次）</p>
            )}
            {q.explanation && (
              <div className="mt-3 p-3 bg-slate-800/50 rounded-lg text-sm text-slate-300">
                <p className="font-medium text-slate-400 mb-1">💡 解析</p>
                <p>{q.explanation}</p>
              </div>
            )}
          </div>
        )}

        {/* Past attempts */}
        {data.recent_attempts?.length > 0 && (
          <div className="mb-6">
            <h2 className="text-sm font-medium text-slate-400 mb-2">📋 最近答题记录</h2>
            <div className="space-y-1.5">
              {data.recent_attempts.slice(-5).reverse().map((a: any, i: number) => (
                <div key={i} className="flex items-center gap-3 text-xs text-slate-500 bg-slate-800/30 rounded-lg px-3 py-2">
                  <span>{a.correct ? '✅' : '❌'}</span>
                  <span className="font-mono">{a.selected_answer || '-'}</span>
                  <span className="text-slate-600">·</span>
                  <span>{a.time_spent || '?'}s</span>
                  <span className="text-slate-600">·</span>
                  <span>{(a.answered_at || '').slice(0, 10)}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Notes */}
        <div className="border-t border-slate-700/50 pt-6">
          <h2 className="text-sm font-medium text-slate-400 mb-2">📝 笔记</h2>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="记录你的解题思路…"
            rows={3}
            className="w-full bg-slate-800/50 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-600 resize-none"
          />
          <button
            onClick={handleSaveNote}
            disabled={savingNote || !note.trim()}
            className="mt-2 px-4 py-1.5 text-sm bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:text-slate-600 rounded-lg transition-all"
          >
            {savingNote ? '保存中…' : noteSaved ? '✅ 已保存' : '保存笔记'}
          </button>
        </div>
      </div>
    </div>
  );
}
