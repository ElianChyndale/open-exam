'use client';

import { useCallback, useEffect, useState } from 'react';
import { reviewApi } from '@/lib/api';
import { BookOpen, Calendar, Filter, ChevronDown } from 'lucide-react';
import { useProfileSubjects } from '@/lib/profiles';

export default function ReviewPackPage() {
  const [markdown, setMarkdown] = useState('');
  const [reviewId, setReviewId] = useState('');
  const [completed, setCompleted] = useState(false);
  const subjects = useProfileSubjects();
  const [loading, setLoading] = useState(true);
  const [focusTopic, setFocusTopic] = useState('');
  const [daysBack, setDaysBack] = useState(7);
  const [depth, setDepth] = useState('standard');
  const [error, setError] = useState('');

  const fetchPack = useCallback((params?: Record<string, string>) => {
    setLoading(true);
    setError('');
    reviewApi.getToday({
      days_back: String(daysBack),
      focus_topic: focusTopic,
      knowledge_depth: depth,
      ...params,
    }).then((data: any) => {
      setMarkdown(data.markdown_content || '');
      setReviewId(data.review_id || '');
      setCompleted(false);
    }).catch(() => {
      setError('复习包刷新失败，请确认本地 API 已启动。');
    }).finally(() => setLoading(false));
  }, [daysBack, depth, focusTopic]);

  useEffect(() => {
    fetchPack();
  }, [fetchPack]);

  // Simple markdown renderer
  const renderMarkdown = (md: string) => {
    const lines = md.split('\n');
    const elements: React.ReactNode[] = [];
    let inCodeBlock = false;

    for (let i = 0; i < lines.length; i += 1) {
      const line = lines[i];
      if (line.startsWith('```')) {
        inCodeBlock = !inCodeBlock;
        continue;
      }
      if (inCodeBlock) {
        elements.push(
          <pre key={i} className="bg-surface-field p-3 rounded-lg text-xs overflow-auto my-2">
            {line}
          </pre>
        );
        continue;
      }

      if (line.startsWith('> [!answer]-')) {
        const answerLines: string[] = [];
        let next = i + 1;
        while (next < lines.length && lines[next].startsWith('>')) {
          answerLines.push(lines[next].replace(/^>\s?/, ''));
          next += 1;
        }
        const label = line.replace('> [!answer]-', '').trim() || 'Reveal correct solution';
        elements.push(
          <details key={i} className="my-3 rounded-lg border border-accent-soft bg-surface-field p-3">
            <summary className="flex cursor-pointer items-center gap-2 text-sm font-medium text-accent">
              <ChevronDown size={14} />
              {label}
            </summary>
            <div className="mt-3 border-t border-line pt-2">
              {renderMarkdown(answerLines.join('\n'))}
            </div>
          </details>
        );
        i = next - 1;
        continue;
      }

      if (line.startsWith('# ')) {
        elements.push(<h1 key={i} className="text-2xl font-bold mt-6 mb-3">{line.slice(2)}</h1>);
      } else if (line.startsWith('## ')) {
        elements.push(<h2 key={i} className="text-xl font-bold mt-5 mb-2 text-accent">{line.slice(3)}</h2>);
      } else if (line.startsWith('### ')) {
        elements.push(<h3 key={i} className="text-lg font-semibold mt-4 mb-2">{line.slice(4)}</h3>);
      } else if (line.startsWith('#### ')) {
        elements.push(<h4 key={i} className="text-base font-semibold mt-3 mb-1 text-muted">{line.slice(5)}</h4>);
      } else if (line.startsWith('> ')) {
        elements.push(
          <blockquote key={i} className="border-l-2 border-accent-soft pl-3 my-1 text-sm text-muted">
            {line.slice(2)}
          </blockquote>
        );
      } else if (line.startsWith('- ')) {
        elements.push(<li key={i} className="text-sm ml-4 list-disc my-0.5">{line.slice(2)}</li>);
      } else if (line.startsWith('---')) {
        elements.push(<hr key={i} className="my-3 border-line" />);
      } else if (line.trim() === '') {
        elements.push(<div key={i} className="h-2" />);
      } else {
        elements.push(<p key={i} className="text-sm my-1">{line}</p>);
      }
    }

    return elements;
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Daily Review</h2>
          <p className="text-muted text-sm mt-1">到期错题、低信心题、交错题组、公式/概念热身</p>
        </div>
        <button
          onClick={() => fetchPack()}
          disabled={loading}
          className="px-4 py-2 bg-accent-solid hover:bg-accent-strong disabled:opacity-50 rounded-lg text-sm transition-colors"
        >
          刷新 Daily Review
        </button>
      </div>

      {error && <div className="rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">{error}</div>}

      {/* Filters */}
      <div className="card flex items-center gap-4 flex-wrap">
        <div className="flex items-center gap-2">
          <Filter size={14} className="text-muted" />
          <span className="text-xs text-muted">过滤:</span>
        </div>
        <select
          value={focusTopic}
          onChange={(e) => { setFocusTopic(e.target.value); fetchPack({ focus_topic: e.target.value }); }}
          className="bg-surface-field border border-line rounded-lg px-3 py-1.5 text-xs"
        >
          <option value="">所有科目</option>
          {subjects.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <select
          value={daysBack}
          onChange={(e) => { setDaysBack(Number(e.target.value)); fetchPack({ days_back: e.target.value }); }}
          className="bg-surface-field border border-line rounded-lg px-3 py-1.5 text-xs"
        >
          <option value={1}>1 天</option>
          <option value={3}>3 天</option>
          <option value={7}>7 天</option>
          <option value={14}>14 天</option>
          <option value={30}>30 天</option>
        </select>
        <select
          value={depth}
          onChange={(e) => { setDepth(e.target.value); fetchPack({ knowledge_depth: e.target.value }); }}
          className="bg-surface-field border border-line rounded-lg px-3 py-1.5 text-xs"
        >
          <option value="standard">标准深度</option>
          <option value="expanded">扩展深度</option>
        </select>
        <div className="flex items-center gap-1 text-xs text-muted">
          <Calendar size={12} />
          <span>回顾 {daysBack} 天</span>
        </div>
      </div>

      {/* Review content */}
      {loading ? (
        <div className="card text-center py-12 text-muted animate-pulse">生成复习包中...</div>
      ) : markdown ? (
        <div className="space-y-3">
          <div className="card">
            <div className="prose prose-invert max-w-none">
              {renderMarkdown(markdown)}
            </div>
          </div>
          <button
            onClick={() => reviewId && reviewApi.complete(reviewId).then(() => setCompleted(true))}
            disabled={!reviewId || completed}
            className="px-4 py-2 bg-accent-solid hover:bg-accent-strong disabled:opacity-50 rounded-lg text-sm transition-colors"
          >
            {completed ? 'Reviewed once' : '完成 Daily Review'}
          </button>
        </div>
      ) : (
        <div className="card text-center py-12 text-muted">
          <BookOpen size={32} className="mx-auto mb-3 opacity-50" />
          <p>暂无复习内容</p>
          <p className="text-xs mt-1">记录错题后，系统会自动生成复习包</p>
        </div>
      )}
    </div>
  );
}
