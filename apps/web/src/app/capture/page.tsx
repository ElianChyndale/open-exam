'use client';

import { useState } from 'react';
import { attemptsApi } from '@/lib/api';
import { Upload, Camera, Check, AlertCircle } from 'lucide-react';

const SUBJECTS = [
  'Quantitative Methods', 'Economics', 'Financial Statement Analysis',
  'Corporate Issuers', 'Equity', 'Fixed Income', 'Derivatives',
  'Alternative Investments', 'Portfolio Management', 'Ethical and Professional Standards',
];

const ERROR_TYPES = [
  { value: 'concept_confusion', label: '概念混淆' },
  { value: 'formula_misuse', label: '公式误用' },
  { value: 'knowledge_gap', label: '知识空缺' },
  { value: 'careless_reading', label: '粗心读题' },
  { value: 'time_pressure', label: '时间压力' },
  { value: 'confidence_calibration_failure', label: '信心校准失败' },
  { value: 'fatigue_energy_mismatch', label: '精力不足' },
  { value: 'agent_failure', label: 'Agent 失误' },
];

const CONFIDENCE_LEVELS = [
  { value: 0, label: '猜的' },
  { value: 1, label: '不确定' },
  { value: 2, label: '较确定' },
  { value: 3, label: '确定' },
  { value: 4, label: '非常确定' },
];

export default function QuestionCapture() {
  const [form, setForm] = useState({
    topic: '',
    los: '',
    prompt_or_question: '',
    wrong_choice_or_output: '',
    correct_resolution: '',
    error_type: 'concept_confusion',
    confidence: 1,
    time_spent: 120,
    question_source: 'manual_entry',
    source_type: 'manual',
    choices: [] as string[],
  });

  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setResult(null);
    try {
      const payload = {
        ...form,
        evidence_refs: [`manual-${Date.now()}`],
      };
      const res = await attemptsApi.record(payload);
      setResult(res);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleScreenshotUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !form.topic) return;

    const reader = new FileReader();
    reader.onload = async () => {
      const base64 = (reader.result as string).split(',')[1];
      try {
        await attemptsApi.uploadScreenshot({
          topic: form.topic,
          los: form.los,
          image_data: base64,
          filename: file.name,
        });
        setResult({ status: 'screenshot_uploaded', filename: file.name });
      } catch (err: any) {
        setError(err.message);
      }
    };
    reader.readAsDataURL(file);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold">题目录入</h2>
        <p className="text-muted text-sm mt-1">记录错题或上传截图——每道错题都会转成下一次的行动</p>
      </div>

      {/* Screenshot upload zone */}
      <div className="card border-dashed border-2 border-line hover:border-accent/40 transition-colors">
        <label className="flex flex-col items-center gap-3 py-8 cursor-pointer">
          <Camera size={32} className="text-muted" />
          <span className="text-sm text-muted">点击上传错题截图（AI 自动提取结构化信息）</span>
          <input
            type="file"
            accept="image/*"
            onChange={handleScreenshotUpload}
            className="hidden"
          />
        </label>
      </div>

      {/* Manual entry form */}
      <form onSubmit={handleSubmit} className="card space-y-4">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Upload size={18} className="text-accent" /> 手动录入
        </h3>

        {/* Row 1: Topic + LOS */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-xs text-muted block mb-1">科目</label>
            <select
              aria-label="科目"
              value={form.topic}
              onChange={(e) => setForm({ ...form, topic: e.target.value })}
              className="w-full bg-surface-sunken border border-line rounded-lg px-3 py-2 text-sm"
              required
            >
              <option value="">选择科目</option>
              {SUBJECTS.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs text-muted block mb-1">LOS</label>
            <input
              aria-label="LOS"
              type="text"
              value={form.los}
              onChange={(e) => setForm({ ...form, los: e.target.value })}
              className="w-full bg-surface-sunken border border-line rounded-lg px-3 py-2 text-sm"
              placeholder="例如: CI.3, FI.8"
            />
          </div>
        </div>

        {/* Question prompt */}
        <div>
          <label className="text-xs text-muted block mb-1">题目</label>
          <textarea
            aria-label="题目"
            value={form.prompt_or_question}
            onChange={(e) => setForm({ ...form, prompt_or_question: e.target.value })}
            className="w-full bg-surface-sunken border border-line rounded-lg px-3 py-2 text-sm min-h-[80px]"
            placeholder="粘贴题目或简要描述..."
            required
          />
        </div>

        {/* Wrong + Correct */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-xs text-muted block mb-1">你的错误答案</label>
            <input
              aria-label="你的错误答案"
              type="text"
              value={form.wrong_choice_or_output}
              onChange={(e) => setForm({ ...form, wrong_choice_or_output: e.target.value })}
              className="w-full bg-surface-sunken border border-line rounded-lg px-3 py-2 text-sm"
              placeholder="A / B / C / D 或你的答案"
            />
          </div>
          <div>
            <label className="text-xs text-muted block mb-1">正确答案 / 解释</label>
            <input
              aria-label="正确答案或解释"
              type="text"
              value={form.correct_resolution}
              onChange={(e) => setForm({ ...form, correct_resolution: e.target.value })}
              className="w-full bg-surface-sunken border border-line rounded-lg px-3 py-2 text-sm"
              placeholder="正确答案和简要解释"
              required
            />
          </div>
        </div>

        {/* Error type + Confidence + Time */}
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="text-xs text-muted block mb-1">错因</label>
            <select
              aria-label="错因"
              value={form.error_type}
              onChange={(e) => setForm({ ...form, error_type: e.target.value })}
              className="w-full bg-surface-sunken border border-line rounded-lg px-3 py-2 text-sm"
            >
              {ERROR_TYPES.map((et) => (
                <option key={et.value} value={et.value}>{et.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs text-muted block mb-1">信心</label>
            <select
              aria-label="信心"
              value={form.confidence}
              onChange={(e) => setForm({ ...form, confidence: Number(e.target.value) })}
              className="w-full bg-surface-sunken border border-line rounded-lg px-3 py-2 text-sm"
            >
              {CONFIDENCE_LEVELS.map((cl) => (
                <option key={cl.value} value={cl.value}>{cl.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs text-muted block mb-1">耗时（秒）</label>
            <input
              aria-label="耗时秒数"
              type="number"
              value={form.time_spent}
              onChange={(e) => setForm({ ...form, time_spent: Number(e.target.value) })}
              className="w-full bg-surface-sunken border border-line rounded-lg px-3 py-2 text-sm"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full py-2.5 bg-accent-action text-white hover:bg-accent-action-strong disabled:opacity-50 rounded-lg text-sm font-medium transition-colors"
        >
          {submitting ? '提交中...' : '记录错题'}
        </button>
      </form>

      {/* Result */}
      {result && (
        <div className="card border-success/25">
          <div className="flex items-center gap-2 mb-2">
            <Check size={16} className="text-success" />
            <span className="text-sm font-semibold text-success">记录成功</span>
          </div>
          <pre className="text-xs text-muted overflow-auto">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      {error && (
        <div className="card border-danger/25">
          <div className="flex items-center gap-2">
            <AlertCircle size={16} className="text-danger" />
            <span className="text-sm text-danger">{error}</span>
          </div>
        </div>
      )}
    </div>
  );
}
