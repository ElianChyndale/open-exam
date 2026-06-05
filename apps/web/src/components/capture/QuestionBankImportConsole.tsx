'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { authApi, questionBanksApi } from '@/lib/api';

const STATUS_COLORS: Record<string, string> = {
  quarantined: 'bg-amber-900/40 text-amber-300 border-amber-700/30',
  verified: 'bg-emerald-900/40 text-emerald-300 border-emerald-700/30',
  rejected: 'bg-red-900/40 text-red-300 border-red-700/30',
  published: 'bg-blue-900/40 text-blue-300 border-blue-700/30',
};

export default function QuestionBankImportConsole() {
  // Import tab
  const [sourceFile, setSourceFile] = useState('private-bank');
  const [records, setRecords] = useState('[]');
  const [selectedImportFile, setSelectedImportFile] = useState('');
  const [message, setMessage] = useState('');

  // Browse tab
  const [allQuestions, setAllQuestions] = useState<any[]>([]);
  const [filteredQuestions, setFilteredQuestions] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [edits, setEdits] = useState<Record<string, string>>({});
  const [activeTab, setActiveTab] = useState<'import' | 'browse'>('browse');
  const [loadingList, setLoadingList] = useState(false);
  const [authRequired, setAuthRequired] = useState(false);

  const isAuthError = (error: unknown) => {
    const text = error instanceof Error ? error.message : String(error || '');
    return text.includes('401') || text.includes('403');
  };

  const requireAdminMessage = () => {
    setAuthRequired(true);
    setMessage('管理员会话未建立或已失效。先到 /review/admin-auth 完成本地 bootstrap / login，再回来继续导入和审核。');
  };

  const loadAllQuestions = async () => {
    setLoadingList(true);
    try {
      const data = await questionBanksApi.listAll();
      setAllQuestions(data.questions || []);
      setAuthRequired(false);
      setMessage((current) => (current.includes('管理员会话未建立') ? '' : current));
    } catch (error) {
      if (isAuthError(error)) {
        setAllQuestions([]);
        requireAdminMessage();
      } else {
        setMessage(`加载题库失败: ${error instanceof Error ? error.message : String(error)}`);
      }
    } finally {
      setLoadingList(false);
    }
  };

  useEffect(() => {
    loadAllQuestions().catch(() => setLoadingList(false));
  }, []);

  // Filter & search
  useEffect(() => {
    let items = [...allQuestions];
    if (statusFilter !== 'all') {
      items = items.filter((q) => q.verification_status === statusFilter);
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      items = items.filter(
        (item) =>
          (item.prompt || '').toLowerCase().includes(q) ||
          (item.subject || '').toLowerCase().includes(q) ||
          (item.chapter || '').toLowerCase().includes(q) ||
          (item.question_id || '').toLowerCase().includes(q)
      );
    }
    setFilteredQuestions(items);
    setPage(1);
    setSelectedIds(new Set());
  }, [allQuestions, statusFilter, searchQuery]);

  const totalPages = Math.max(1, Math.ceil(filteredQuestions.length / pageSize));
  const paged = filteredQuestions.slice((page - 1) * pageSize, page * pageSize);

  const toggleSelect = (id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleSelectAll = () => {
    if (selectedIds.size === paged.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(paged.map((q) => q.question_id)));
    }
  };

  const bulkReview = async (action: 'approve' | 'reject') => {
    for (const id of selectedIds) {
      try {
        const patch = action === 'approve' ? JSON.parse(edits[id] || '{}') : {};
        await questionBanksApi.review(id, action, patch);
      } catch (error) {
        if (isAuthError(error)) {
          requireAdminMessage();
          break;
        }
      }
    }
    setMessage(`${action === 'approve' ? 'Approved' : 'Rejected'} ${selectedIds.size} questions.`);
    setSelectedIds(new Set());
    await loadAllQuestions();
  };

  const reviewOne = async (questionId: string, action: 'approve' | 'reject') => {
    try {
      const patch = action === 'approve' ? JSON.parse(edits[questionId] || '{}') : {};
      await questionBanksApi.review(questionId, action, patch);
      setMessage(`${action === 'approve' ? '✅ Approved' : '❌ Rejected'} ${questionId}.`);
      await loadAllQuestions();
    } catch (error: any) {
      if (isAuthError(error)) {
        requireAdminMessage();
      } else {
        setMessage(`Review failed: ${error.message}`);
      }
    }
  };

  const importRecordsFn = async () => {
    try {
      const questions = JSON.parse(records);
      const result: any = await questionBanksApi.importStructured({ source_file: sourceFile, questions });
      setMessage(`✅ Imported ${result.imported_count}; verified ${result.verified_count}; quarantined ${result.quarantined_count}.`);
      setAuthRequired(false);
      await loadAllQuestions();
    } catch (error: any) {
      if (isAuthError(error)) {
        requireAdminMessage();
      } else {
        setMessage(`❌ Import failed: ${error.message}`);
      }
    }
  };

  const importCommand = selectedImportFile
    ? `python scripts/import_qbank_excel.py "${selectedImportFile}" --source "${sourceFile || selectedImportFile}"`
    : `python scripts/import_qbank_excel.py "<你的题库文件.csv|xlsx>" --source "${sourceFile || 'private-bank'}"`;

  return (
    <section className="card space-y-4">
      {/* Tabs */}
      <div className="flex items-center gap-1 border-b border-line pb-3">
        <button
          onClick={() => setActiveTab('browse')}
          className={`px-4 py-1.5 text-sm rounded-lg transition-colors ${activeTab === 'browse' ? 'bg-accent-solid text-white' : 'text-muted hover:text-foreground'}`}
        >
          题库管理
        </button>
        <button
          onClick={() => setActiveTab('import')}
          className={`px-4 py-1.5 text-sm rounded-lg transition-colors ${activeTab === 'import' ? 'bg-accent-solid text-white' : 'text-muted hover:text-foreground'}`}
        >
          导入题目
        </button>
      </div>

      <div className={`rounded-lg border px-3 py-3 text-xs ${authRequired ? 'border-warning-soft bg-warning-soft text-warning' : 'border-line bg-surface-field text-muted'}`}>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="min-w-0 space-y-1">
            <p className="font-medium text-foreground">管理员会话要求</p>
            <p>题库导入、全量浏览、隔离审核需要本地管理员会话；练习和错题本不受影响。</p>
          </div>
          <Link href="/review/admin-auth" className="shrink-0 rounded-lg border border-line px-3 py-2 text-xs font-medium text-accent transition-colors hover:bg-surface-hover">
            前往管理员会话
          </Link>
        </div>
      </div>

      {/* Browse tab */}
      {activeTab === 'browse' && (
        <div className="space-y-3">
          <div className="flex items-center gap-3 flex-wrap">
            {/* Search */}
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="搜索题干 / 科目 / 章节…"
              className="flex-1 min-w-[200px] bg-surface-field border border-line rounded-lg px-3 py-1.5 text-sm"
            />
            {/* Status filter */}
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-surface-field border border-line rounded-lg px-3 py-1.5 text-sm"
            >
              <option value="all">全部状态</option>
              <option value="quarantined">待审核</option>
              <option value="verified">已通过</option>
              <option value="rejected">已拒绝</option>
            </select>
            {/* Bulk actions */}
            {selectedIds.size > 0 && (
              <div className="flex gap-2">
                <button onClick={() => bulkReview('approve')} className="px-3 py-1.5 text-xs bg-emerald-700 hover:bg-emerald-600 rounded-lg text-white transition-colors">
                  批量通过 ({selectedIds.size})
                </button>
                <button onClick={() => bulkReview('reject')} className="px-3 py-1.5 text-xs bg-red-700 hover:bg-red-600 rounded-lg text-white transition-colors">
                  批量拒绝 ({selectedIds.size})
                </button>
              </div>
            )}
          </div>

          {loadingList && <p className="text-xs text-muted py-4 text-center">加载中…</p>}

          {!loadingList && filteredQuestions.length === 0 && (
            <div className="text-center py-8 text-muted text-sm">
              {allQuestions.length === 0 ? '题库为空，去"导入题目"标签导入' : '没有匹配的题目'}
            </div>
          )}

          {/* Pagination */}
          {filteredQuestions.length > 0 && (
            <div className="flex items-center justify-between text-xs text-muted">
              <span>共 {filteredQuestions.length} 题，第 {page}/{totalPages} 页</span>
              <div className="flex gap-2">
                <button disabled={page <= 1} onClick={() => setPage(page - 1)} className="px-2 py-1 rounded bg-surface-field hover:bg-surface-hover disabled:opacity-30">←</button>
                <button disabled={page >= totalPages} onClick={() => setPage(page + 1)} className="px-2 py-1 rounded bg-surface-field hover:bg-surface-hover disabled:opacity-30">→</button>
              </div>
            </div>
          )}

          {/* Question list */}
          <div className="space-y-2 max-h-[600px] overflow-y-auto">
            {paged.map((question) => (
              <div key={question.question_id} className={`rounded-xl border p-3 transition-colors ${selectedIds.has(question.question_id) ? 'border-accent-soft bg-accent-soft/10' : 'border-line'}`}>
                <div className="flex items-start gap-3">
                  <input type="checkbox" checked={selectedIds.has(question.question_id)} onChange={() => toggleSelect(question.question_id)} className="mt-1" />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className={`text-xs px-1.5 py-0.5 rounded-full border ${STATUS_COLORS[question.verification_status] || 'bg-slate-700/30 text-slate-400'}`}>
                        {question.verification_status || 'unknown'}
                      </span>
                      <span className="text-xs text-muted">{question.subject}</span>
                      <span className="text-xs text-muted">· {question.chapter}</span>
                      {question.difficulty && (
                        <span className="text-xs text-muted">· {question.difficulty}</span>
                      )}
                    </div>
                    <p className="text-sm line-clamp-2">{question.prompt || '(no prompt)'}</p>
                    {question.validation_warnings?.length > 0 && (
                      <p className="text-xs text-warning mt-1">{question.validation_warnings.join('; ')}</p>
                    )}
                    {question.validation_errors?.length > 0 && (
                      <p className="text-xs text-danger mt-1">{question.validation_errors.join('; ')}</p>
                    )}
                    {question.verification_status === 'quarantined' && (
                      <div className="mt-2 space-y-1">
                        <textarea
                          value={edits[question.question_id] || JSON.stringify(question, null, 2)}
                          onChange={(e) => setEdits({ ...edits, [question.question_id]: e.target.value })}
                          className="w-full min-h-[80px] bg-surface-field border border-line rounded px-2 py-1 font-mono text-xs"
                        />
                        <div className="flex gap-2">
                          <button onClick={() => reviewOne(question.question_id, 'approve')} className="px-2.5 py-1 text-xs bg-emerald-700 hover:bg-emerald-600 rounded text-white transition-colors">通过</button>
                          <button onClick={() => reviewOne(question.question_id, 'reject')} className="px-2.5 py-1 text-xs bg-red-700 hover:bg-red-600 rounded text-white transition-colors">拒绝</button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Bottom pagination */}
          {filteredQuestions.length > pageSize && (
            <div className="flex items-center justify-between text-xs text-muted pt-2">
              <span>{filteredQuestions.length} 题</span>
              <div className="flex gap-2">
                {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                  const start = Math.max(1, Math.min(page - 2, totalPages - 4));
                  const p = start + i;
                  if (p > totalPages) return null;
                  return (
                    <button key={p} onClick={() => setPage(p)} className={`px-2 py-1 rounded ${page === p ? 'bg-accent-solid text-white' : 'bg-surface-field hover:bg-surface-hover'}`}>
                      {p}
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Import tab */}
      {activeTab === 'import' && (
        <div className="space-y-3">
          <div className="rounded-lg border border-line bg-surface-field p-3 text-xs text-muted">
            <p className="font-medium text-foreground">CSV / XLSX 文件桥接</p>
            <p className="mt-1">
              这是本地优先导入流程。当前前端不会把题库文件上传到远端，而是帮你生成准确的本地导入命令，再由现有脚本执行验证、锁定和写入。
            </p>
          </div>
          <div>
            <label className="text-xs text-muted block mb-1">选择题库文件（CSV / XLSX）</label>
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={(e) => {
                const file = e.target.files?.[0];
                setSelectedImportFile(file?.name || '');
                if (file?.name && sourceFile === 'private-bank') {
                  setSourceFile(file.name);
                }
              }}
              className="w-full bg-surface-field border border-line rounded-lg px-3 py-2 text-sm file:mr-3 file:rounded-md file:border-0 file:bg-surface-hover file:px-3 file:py-1.5 file:text-xs"
            />
            <p className="mt-1 text-xs text-muted">
              {selectedImportFile ? `已选择: ${selectedImportFile}` : '未选择文件时，仍可继续使用下面的 JSON 导入方式。'}
            </p>
          </div>
          <div>
            <label className="text-xs text-muted block mb-1">来源标签</label>
            <input
              value={sourceFile}
              onChange={(e) => setSourceFile(e.target.value)}
              className="w-full bg-surface-field border border-line rounded-lg px-3 py-2 text-sm"
              placeholder="例如: cfa-l1-mock-2024"
            />
          </div>
          <div>
            <label className="text-xs text-muted block mb-1">JSON 题目数据</label>
            <textarea
              value={records}
              onChange={(e) => setRecords(e.target.value)}
              className="min-h-28 w-full bg-surface-field border border-line rounded-lg px-3 py-2 font-mono text-xs"
              placeholder='[{"prompt": "...", "choices": [...], "answer": "A", ...}]'
            />
          </div>
          <button
            onClick={importRecordsFn}
            disabled={authRequired && !authApi.hasStoredSession()}
            className="px-4 py-2 bg-accent-solid hover:bg-accent-strong rounded-lg text-sm text-white transition-colors"
          >
            导入
          </button>
          <div className="rounded-lg border border-line bg-surface-field p-3 text-xs text-muted">
            <p className="font-medium text-foreground">本地导入命令</p>
            <code className="mt-2 block overflow-x-auto rounded bg-slate-950/60 px-2 py-2 font-mono text-[11px] text-slate-200">
              {importCommand}
            </code>
            <p className="mt-2">
              如果你已经启动了 API，也可以在命令末尾加 <code className="bg-surface-hover px-1 rounded">--api</code>，走受保护的导入接口。
            </p>
          </div>
        </div>
      )}

      {/* Global message */}
      {message && (
        <div className="text-xs text-success bg-success-soft/20 rounded-lg px-3 py-2 border border-success-soft/30">
          {message}
          <button onClick={() => setMessage('')} className="ml-2 text-muted hover:text-foreground">✕</button>
        </div>
      )}
    </section>
  );
}
