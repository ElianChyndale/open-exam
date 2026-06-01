'use client';

import { useState } from 'react';
import { Mic, X, Upload } from 'lucide-react';
import { attemptsApi } from '@/lib/api';
import { queueAttempt } from '@/lib/offline';
import { useProfileSubjects } from '@/lib/profiles';

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
  const [queued, setQueued] = useState(false);
  const [voiceMessage, setVoiceMessage] = useState('');
  const subjects = useProfileSubjects();

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic || !wrong || !correct) return;
    setSubmitting(true);
    const payload = {
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
      };
    try {
      await attemptsApi.record(payload);
      setTopic(''); setLos(''); setWrong(''); setCorrect('');
      onClose();
    } catch {
      await queueAttempt(payload);
      setQueued(true);
    }
    setSubmitting(false);
  };

  const captureVoice = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setVoiceMessage('当前浏览器不支持语音录入，请直接键入答案。');
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'zh-CN';
    recognition.onstart = () => setVoiceMessage('正在听，请说出你的错误答案...');
    recognition.onresult = (event: any) => {
      setWrong(event.results[0][0].transcript);
      setVoiceMessage('已写入语音内容。');
    };
    recognition.onerror = () => setVoiceMessage('语音识别失败，请重试或直接键入。');
    recognition.start();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-surface-raised border border-line rounded-xl w-full max-w-md mx-4 p-6 shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Upload size={16} className="text-accent" /> 快速录入
          </h3>
          <button onClick={onClose} className="text-muted hover:text-white transition-colors">
            <X size={20} />
          </button>
        </div>
        {queued && <p className="mb-3 text-xs text-warning">当前离线，已加入本地待同步队列。</p>}
        {voiceMessage && <p className="mb-3 text-xs text-muted" role="status">{voiceMessage}</p>}
        <form onSubmit={handleSubmit} className="space-y-3">
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <select value={topic} onChange={e => setTopic(e.target.value)}
              className="bg-surface-field border border-line rounded-lg px-3 py-2 text-sm" required>
              <option value="">科目</option>
              {subjects.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
            <input value={los} onChange={e => setLos(e.target.value)}
              className="bg-surface-field border border-line rounded-lg px-3 py-2 text-sm"
              placeholder="LOS (可选)" />
          </div>
          <div className="flex gap-2">
            <input value={wrong} onChange={e => setWrong(e.target.value)}
              className="w-full bg-surface-field border border-line rounded-lg px-3 py-2 text-sm"
              placeholder="你的错误答案" required />
            <button type="button" onClick={captureVoice} className="rounded-lg border border-line px-3 text-muted hover:bg-surface-hover" aria-label="语音录入错误答案" title="语音录入错误答案">
              <Mic size={16} />
            </button>
          </div>
          <input value={correct} onChange={e => setCorrect(e.target.value)}
            className="w-full bg-surface-field border border-line rounded-lg px-3 py-2 text-sm"
            placeholder="正确答案" required />
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <select value={errorType} onChange={e => setErrorType(e.target.value)}
              className="bg-surface-field border border-line rounded-lg px-3 py-2 text-sm text-xs">
              {ERROR_TYPES.map(et => <option key={et.value} value={et.value}>{et.label}</option>)}
            </select>
            <button type="submit" disabled={submitting}
              className="bg-accent-solid hover:bg-accent-strong disabled:opacity-50 rounded-lg text-sm font-medium transition-colors">
              {submitting ? '...' : '保存'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
