'use client';

import { useState } from 'react';
import { AlertTriangle, BrainCircuit, CheckCircle2, FileQuestion, HelpCircle, Lightbulb, XCircle } from 'lucide-react';

interface ProactiveQuestion {
  question_id: string;
  subject_name: string;
  question_text: string;
  difficulty_guess: string;
  source: 'mock' | 'generated';
  exam_weight: number;
}

interface AnswerResult {
  correct: boolean;
  explanation?: string;
}

export function ProactiveReviewSection({
  questions,
  onAnswer,
}: {
  questions: ProactiveQuestion[];
  onAnswer: (questionId: string, correct: boolean) => void;
}) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answered, setAnswered] = useState<Record<string, AnswerResult>>({});

  if (questions.length === 0) {
    return (
      <div className="rounded-xl border border-line bg-surface-raised p-6 text-center">
        <CheckCircle2 size={32} className="mx-auto text-green-500" />
        <p className="mt-3 text-sm font-medium">今日无主动检测题目</p>
        <p className="mt-1 text-xs text-muted">所有科目覆盖率充足，继续维持当前复习节奏。</p>
      </div>
    );
  }

  const q = questions[currentIndex];
  const isAnswered = answered[q.question_id] !== undefined;
  const result = answered[q.question_id];
  const correctCount = Object.values(answered).filter(r => r.correct).length;

  const handleAnswer = (correct: boolean) => {
    setAnswered(prev => ({ ...prev, [q.question_id]: { correct } }));
    onAnswer(q.question_id, correct);
  };

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold flex items-center gap-2">
          <BrainCircuit size={17} className="text-accent" />
          今日主动检测
          <span className="text-xs text-muted font-normal">
            ({correctCount}/{Object.keys(answered).length} 正确)
          </span>
        </h3>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted">
            {currentIndex + 1} / {questions.length}
          </span>
          <span className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${
            q.difficulty_guess === 'hard' ? 'bg-red-100 text-red-700' :
            q.difficulty_guess === 'medium' ? 'bg-yellow-100 text-yellow-700' :
            'bg-green-100 text-green-700'
          }`}>
            {q.difficulty_guess === 'hard' ? '困难' : q.difficulty_guess === 'medium' ? '中等' : '容易'}
          </span>
          <span className="text-[10px] rounded-full bg-accent-soft text-accent px-2 py-0.5">
            {q.source === 'mock' ? 'Mock题' : 'AI生成'}
          </span>
        </div>
      </div>

      <div className="rounded-xl border border-line bg-surface-raised p-5">
        <div className="mb-3 flex items-center gap-2">
          <FileQuestion size={14} className="text-muted" />
          <span className="text-xs text-muted">{q.subject_name}</span>
          <span className="text-[10px] text-muted">考试权重: {(q.exam_weight * 100).toFixed(0)}%</span>
        </div>
        <p className="text-sm leading-relaxed">{q.question_text}</p>

        {!isAnswered ? (
          <div className="mt-4 flex gap-3">
            <button onClick={() => handleAnswer(true)} className="btn-primary flex items-center gap-2 text-sm">
              <CheckCircle2 size={15} /> 回答正确
            </button>
            <button onClick={() => handleAnswer(false)} className="btn-secondary flex items-center gap-2 text-sm">
              <XCircle size={15} /> 回答错误/不确定
            </button>
            <button onClick={() => handleAnswer(false)} className="btn-secondary text-sm flex items-center gap-2">
              <HelpCircle size={15} /> 跳过
            </button>
          </div>
        ) : (
          <div className={`mt-4 rounded-lg p-3 flex items-start gap-3 ${
            result.correct ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
          }`}>
            {result.correct ? <CheckCircle2 size={18} className="text-green-600 mt-0.5" /> : <XCircle size={18} className="text-red-600 mt-0.5" />}
            <div>
              <p className="text-sm font-medium">{result.correct ? '正确' : '需加强'}</p>
              <p className="text-xs text-muted mt-1">{result.correct ? '该知识点掌握良好。' : '该知识点需要更多练习。将在后续复习中加强。'}</p>
            </div>
          </div>
        )}
      </div>

      <div className="flex justify-between">
        <button
          onClick={() => setCurrentIndex(Math.max(0, currentIndex - 1))}
          disabled={currentIndex === 0}
          className="btn-secondary text-sm disabled:opacity-30"
        >
          上一题
        </button>
        <button
          onClick={() => setCurrentIndex(Math.min(questions.length - 1, currentIndex + 1))}
          disabled={currentIndex >= questions.length - 1}
          className="btn-secondary text-sm disabled:opacity-30"
        >
          下一题
        </button>
      </div>
    </section>
  );
}
