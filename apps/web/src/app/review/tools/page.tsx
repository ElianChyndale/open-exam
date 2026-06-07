'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import {
  ArrowRight,
  Brain,
  Database,
  FileDown,
  Library,
  Loader2,
  Network,
  Search,
  Settings2,
  ShieldCheck,
  Target,
  Wrench,
} from 'lucide-react';

import { NavigationSurface, navigationApi } from '@/lib/api';

const groupIcons: Record<string, any> = {
  library_sources: Library,
  intelligence: Brain,
  system_portability: ShieldCheck,
  advanced_diagnostics: Settings2,
};

const routeIcons: Record<string, any> = {
  '/review/data': Database,
  '/review/interop': FileDown,
  '/review/knowledge-map': Network,
  '/review/search': Search,
};

export default function ReviewToolsPage() {
  const [groups, setGroups] = useState<Array<{ group_id: string; label: string; items: NavigationSurface[] }>>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const payload = await navigationApi.tools();
      setGroups(payload.groups || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Tools load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  return (
    <div className="mx-auto max-w-6xl pb-12">
      <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-surface-raised px-3 py-1 text-xs font-medium text-muted">
            <Wrench size={13} />
            Tool library
          </div>
          <h2 className="mt-4 text-3xl font-semibold tracking-normal">Tools</h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-muted">
            Advanced study surfaces, diagnostics, and system utilities.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/review" className="btn-primary inline-flex w-fit items-center gap-2">
            <ArrowRight size={15} />
            Back to Daily Review
          </Link>
          <Link href="/today" className="btn-secondary inline-flex w-fit items-center gap-2">
            <ArrowRight size={15} />
            Today
          </Link>
        </div>
      </div>

      {error && <div className="mb-4 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">{error}</div>}

      {loading ? (
        <div className="rounded-lg bg-surface-raised p-8 text-sm text-muted">
          <Loader2 size={15} className="mr-2 inline animate-spin" />
          Loading tools...
        </div>
      ) : (
        <div className="grid min-w-0 gap-4 md:grid-cols-2">
          {/* Static question-bank tools */}
          <section className="min-w-0 rounded-lg bg-surface-raised p-5">
            <div className="flex items-center gap-2">
              <Database size={18} className="text-accent" />
              <h3 className="font-semibold">Question Banks</h3>
            </div>
            <div className="mt-4 grid gap-2">
              <Link href="/review/wrongbook" className="group flex min-w-0 items-center justify-between gap-3 rounded-lg bg-surface-field px-3 py-3 transition-colors hover:bg-surface-hover">
                <span className="flex min-w-0 items-center gap-3">
                  <Search size={15} className="shrink-0 text-muted" />
                  <span className="min-w-0">
                    <span className="block truncate text-sm font-medium">📕 错题本</span>
                    <span className="mt-0.5 block truncate text-xs text-muted">按优先级复习错题，查看答题记录</span>
                  </span>
                </span>
                <ArrowRight size={14} className="shrink-0 text-muted transition-colors group-hover:text-accent" />
              </Link>
              <Link href="/review/practice" className="group flex min-w-0 items-center justify-between gap-3 rounded-lg bg-surface-field px-3 py-3 transition-colors hover:bg-surface-hover">
                <span className="flex min-w-0 items-center gap-3">
                  <Target size={15} className="shrink-0 text-muted" />
                  <span className="min-w-0">
                    <span className="block truncate text-sm font-medium">📝 章节练习</span>
                    <span className="mt-0.5 block truncate text-xs text-muted">选题生成练习，答题卡逐题作答</span>
                  </span>
                </span>
                <ArrowRight size={14} className="shrink-0 text-muted transition-colors group-hover:text-accent" />
              </Link>
              <Link href="/capture" className="group flex min-w-0 items-center justify-between gap-3 rounded-lg bg-surface-field px-3 py-3 transition-colors hover:bg-surface-hover">
                <span className="flex min-w-0 items-center gap-3">
                  <Database size={15} className="shrink-0 text-muted" />
                  <span className="min-w-0">
                    <span className="block truncate text-sm font-medium">📥 导入题库</span>
                    <span className="mt-0.5 block truncate text-xs text-muted">导入审核 / 批量导入</span>
                  </span>
                </span>
                <ArrowRight size={14} className="shrink-0 text-muted transition-colors group-hover:text-accent" />
              </Link>
              <Link href="/review/admin-auth" className="group flex min-w-0 items-center justify-between gap-3 rounded-lg bg-surface-field px-3 py-3 transition-colors hover:bg-surface-hover">
                <span className="flex min-w-0 items-center gap-3">
                  <ShieldCheck size={15} className="shrink-0 text-muted" />
                  <span className="min-w-0">
                    <span className="block truncate text-sm font-medium">🔐 管理员会话</span>
                    <span className="mt-0.5 block truncate text-xs text-muted">本地 bootstrap / login / protected import</span>
                  </span>
                </span>
                <ArrowRight size={14} className="shrink-0 text-muted transition-colors group-hover:text-accent" />
              </Link>
              <Link href="/review/security" className="group flex min-w-0 items-center justify-between gap-3 rounded-lg bg-surface-field px-3 py-3 transition-colors hover:bg-surface-hover">
                <span className="flex min-w-0 items-center gap-3">
                  <ShieldCheck size={15} className="shrink-0 text-muted" />
                  <span className="min-w-0">
                    <span className="block truncate text-sm font-medium">🛡️ 安全审计</span>
                    <span className="mt-0.5 block truncate text-xs text-muted">查看 bootstrap / login / access-control 事件</span>
                  </span>
                </span>
                <ArrowRight size={14} className="shrink-0 text-muted transition-colors group-hover:text-accent" />
              </Link>
            </div>
          </section>
          {groups.map((group) => {
            const Icon = groupIcons[group.group_id] || Wrench;
            return (
              <section key={group.group_id} className="min-w-0 rounded-lg bg-surface-raised p-5">
                <div className="flex items-center gap-2">
                  <Icon size={18} className="text-accent" />
                  <h3 className="font-semibold">{group.label}</h3>
                </div>
                <div className="mt-4 grid gap-2">
                  {group.items.map((item) => {
                    const ItemIcon = routeIcons[item.route] || Wrench;
                    return (
                      <Link key={item.surface_id} href={item.route} className="group flex min-w-0 items-center justify-between gap-3 rounded-lg bg-surface-field px-3 py-3 transition-colors hover:bg-surface-hover">
                        <span className="flex min-w-0 items-center gap-3">
                          <ItemIcon size={15} className="shrink-0 text-muted" />
                          <span className="min-w-0">
                            <span className="block truncate text-sm font-medium">{item.label}</span>
                            <span className="mt-0.5 block truncate text-xs text-muted">{item.reason}</span>
                          </span>
                        </span>
                        <ArrowRight size={14} className="shrink-0 text-muted transition-colors group-hover:text-accent" />
                      </Link>
                    );
                  })}
                </div>
              </section>
            );
          })}
        </div>
      )}
    </div>
  );
}
