'use client';

import { useEffect, useState } from 'react';
import { questionBanksApi, type WrongbookEntry } from '@/lib/api';
import Link from 'next/link';

export default function WrongbookPage() {
  const [items, setItems] = useState<WrongbookEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [sort, setSort] = useState('priority');
  const [filter, setFilter] = useState('');

  useEffect(() => {
    setLoading(true);
    questionBanksApi.getWrongbook(sort).then((res) => {
      setItems(res.items);
      setLoading(false);
    });
  }, [sort]);

  const filtered = filter
    ? items.filter(
        (i) =>
          i.subject.toLowerCase().includes(filter.toLowerCase()) ||
          i.chapter.toLowerCase().includes(filter.toLowerCase()) ||
          i.prompt.toLowerCase().includes(filter.toLowerCase())
      )
    : items;

  const totalPriority = items.reduce((s, i) => s + i.priority, 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-200 p-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-white">📕 错题本</h1>
            <p className="text-slate-400 text-sm mt-1">
              {items.length} 道错题 · 优先级总分 {totalPriority}
            </p>
          </div>
          <div className="flex gap-3">
            <Link
              href="/review/practice"
              className="bg-slate-700 hover:bg-slate-600 rounded-lg px-3 py-1.5 text-sm text-slate-300 transition-colors"
            >
              + 章节练习
            </Link>
            <select
              value={sort}
              onChange={(e) => setSort(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-sm text-slate-300"
            >
              <option value="priority">按优先级 ↓</option>
              <option value="-priority">按优先级 ↑</option>
              <option value="wrong_count">按错误次数 ↓</option>
              <option value="subject">按科目</option>
              <option value="last_seen">按最近出错</option>
            </select>
          </div>
        </div>

        {/* Search */}
        <input
          type="text"
          placeholder="搜索科目 / 章节 / 题干…"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 mb-6 text-slate-200 placeholder-slate-500"
        />

        {/* Loading */}
        {loading && (
          <div className="text-center py-12 text-slate-500">加载中…</div>
        )}

        {/* Empty state */}
        {!loading && items.length === 0 && (
          <div className="text-center py-16 text-slate-500">
            <p className="text-5xl mb-4">🎉</p>
            <p className="text-lg">还没有错题！继续保持</p>
          </div>
        )}

        {/* List */}
        {!loading && filtered.length > 0 && (
          <div className="space-y-3">
            {filtered.map((item) => (
              <Link
                key={item.question_id}
                href={`/review/wrongbook/${item.question_id}`}
                className="block bg-slate-800/60 border border-slate-700/50 rounded-xl p-4 hover:border-amber-600/40 transition-all group"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1.5">
                      <span
                        className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                          item.priority >= 70
                            ? 'bg-red-900/50 text-red-300'
                            : item.priority >= 40
                            ? 'bg-amber-900/50 text-amber-300'
                            : 'bg-slate-700/50 text-slate-400'
                        }`}
                      >
                        优先级 {item.priority}
                      </span>
                      <span className="text-xs text-slate-500">{item.subject}</span>
                      <span className="text-xs text-slate-600">·</span>
                      <span className="text-xs text-slate-500">{item.chapter}</span>
                    </div>
                    <p className="text-slate-200 group-hover:text-white transition-colors line-clamp-2">
                      {item.prompt}
                    </p>
                    <div className="flex items-center gap-3 mt-2 text-xs text-slate-500">
                      <span>❌ 错 {item.wrong_count} 次</span>
                      <span>✅ 对 {item.correct_retry_count} 次</span>
                      <span>📊 {item.difficulty}</span>
                      {item.knowledge_tags?.length > 0 && (
                        <span className="truncate">
                          🏷️ {item.knowledge_tags.slice(0, 3).join(', ')}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="shrink-0 text-slate-600 group-hover:text-amber-500 transition-colors">
                    →
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {!loading && filter && filtered.length === 0 && items.length > 0 && (
          <div className="text-center py-8 text-slate-500">没有匹配的错题</div>
        )}
      </div>
    </div>
  );
}
