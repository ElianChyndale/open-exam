'use client';

import { useState } from 'react';
import { X, Upload } from 'lucide-react';
import { attemptsApi } from '@/lib/api';

const SUBJECTS = [
  'Quantitative Methods', 'Economics', 'Financial Statement Analysis',
  'Corporate Issuers', 'Equity', 'Fixed Income', 'Derivatives',
  'Alternative Investments', 'Portfolio Management', 'Ethical and Professional Standards',
];

const ERROR_TYPES = [
  { value: 'concept_confusion', label: '概念混淆' },
  { value: 'formula_misuse', label: '公式误用' },
  { value: 'careless_reading', label: '粗心读题' },
  { value: 'knowledge_gap', label: '知识空缺' },
  { value: 'time_pressure', label: '时间压力' },
];

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function QuickCapture({ isOpen, onClose }: Props) {
  const [topic, setTopic] = useState('');
  const [los, setLos] = useState('');
  const [wrong, setWrong] = useState('');
  const [correct, setCorrect] = useState('');
  const [errorType, setErrorType] = useState('concept_confusion');
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic || !wrong || !correct) return;
    setSubmitting(true);
    try {
      await attemptsApi.record({
        topic, los,
        prompt_or_question: `Quick: ${topic}/${los}`,
        wrong_choice_or_output: wrong,
        correct_resolution: correct,
        error_type: errorType,
        confidence: 2,
        time_spent: 60,
        evidence_refs: [`quick-${Date.now()}`],
        question_source: 'quick_capture',
        source_type: 'manual',
      });
      setTopic(''); setLos(''); setWrong(''); setCorrect('');
      onClose();
    } catch { /* ignore */ }
    setSubmitting(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-[#0d0d1a] border border-[#1e1e2e] rounded-xl w-full max-w-md mx-4 p-6 shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Upload size={16} className="text-accent" /> 快速录入
          </h3>
          <button onClick={onClose} className="text-muted hover:text-white transition-colors">
            <X size={20} />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <select value={topic} onChange={e => setTopic(e.target.value)}
              className="bg-[#0a0a0f] border border-[#1e1e2e] rounded-lg px-3 py-2 text-sm" required>
              <option value="">科目</option>
              {SUBJECTS.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
            <input value={los} onChange={e => setLos(e.target.value)}
              className="bg-[#0a0a0f] border border-[#1e1e2e] rounded-lg px-3 py-2 text-sm"
              placeholder="LOS (可选)" />
          </div>
          <input value={wrong} onChange={e => setWrong(e.target.value)}
            className="w-full bg-[#0a0a0f] border border-[#1e1e2e] rounded-lg px-3 py-2 text-sm"
            placeholder="你的错误答案" required />
          <input value={correct} onChange={e => setCorrect(e.target.value)}
            className="w-full bg-[#0a0a0f] border border-[#1e1e2e] rounded-lg px-3 py-2 text-sm"
            placeholder="正确答案" required />
          <div className="grid grid-cols-2 gap-3">
            <select value={errorType} onChange={e => setErrorType(e.target.value)}
              className="bg-[#0a0a0f] border border-[#1e1e2e] rounded-lg px-3 py-2 text-sm text-xs">
              {ERROR_TYPES.map(et => <option key={et.value} value={et.value}>{et.label}</option>)}
            </select>
            <button type="submit" disabled={submitting}
              className="bg-[#6366f1] hover:bg-[#5558e6] disabled:opacity-50 rounded-lg text-sm font-medium transition-colors">
              {submitting ? '...' : '保存'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
