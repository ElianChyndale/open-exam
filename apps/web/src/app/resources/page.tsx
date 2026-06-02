'use client';

import { FormEvent, useCallback, useEffect, useState } from 'react';
import { AlertTriangle, Database, FileSearch, Globe2, Play, RefreshCw, ShieldCheck } from 'lucide-react';

import {
  ResourceAuditFinding,
  ResourceDocument,
  ResourceInboxItem,
  ResourceJob,
  ResourceProvider,
  ResourceSettings,
  ResourceSubscription,
  resourcesApi,
} from '@/lib/api';

export default function ResourceCenter() {
  const [providers, setProviders] = useState<ResourceProvider[]>([]);
  const [subscriptions, setSubscriptions] = useState<ResourceSubscription[]>([]);
  const [documents, setDocuments] = useState<ResourceDocument[]>([]);
  const [jobs, setJobs] = useState<ResourceJob[]>([]);
  const [inbox, setInbox] = useState<ResourceInboxItem[]>([]);
  const [findings, setFindings] = useState<ResourceAuditFinding[]>([]);
  const [settings, setSettings] = useState<ResourceSettings | null>(null);
  const [scheduler, setScheduler] = useState({ task_name: 'OpenExam-ResourceOS', installed: false, status: 'loading' });
  const [lane, setLane] = useState<'language' | 'cfa'>('language');
  const [url, setUrl] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<{ document_id: string; title: string; excerpt: string; topic: string }[]>([]);
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);

  const refresh = useCallback(async () => {
    const [providerData, subscriptionData, documentData, jobData, inboxData, auditData, schedulerData, settingsData] = await Promise.all([
      resourcesApi.providers(),
      resourcesApi.subscriptions(),
      resourcesApi.documents(),
      resourcesApi.jobs(),
      resourcesApi.inbox(),
      resourcesApi.audits(),
      resourcesApi.scheduler(),
      resourcesApi.settings(),
    ]);
    setProviders(providerData.providers);
    setSubscriptions(subscriptionData.subscriptions);
    setDocuments(documentData.documents);
    setJobs(jobData.jobs);
    setInbox(inboxData.items);
    setFindings(auditData.findings);
    setScheduler(schedulerData);
    setSettings(settingsData);
  }, []);

  useEffect(() => {
    refresh().catch(() => setMessage('资源中心无法连接本地 API。'));
  }, [refresh]);

  const crawl = async (event: FormEvent) => {
    event.preventDefault();
    if (!url.trim()) return;
    setBusy(true);
    setMessage('');
    try {
      await resourcesApi.crawl({ lane, url: url.trim() });
      setUrl('');
      setMessage('抓取完成。未知版权内容只保留 metadata 和短摘录。');
      await refresh();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : '抓取失败。');
    } finally {
      setBusy(false);
    }
  };

  const subscribe = async () => {
    if (!url.trim()) return;
    setBusy(true);
    try {
      await resourcesApi.createSubscription({ lane, provider: 'rss_atom', target: url.trim() });
      setUrl('');
      setMessage('RSS / Atom 订阅已保存。');
      await refresh();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : '订阅失败。');
    } finally {
      setBusy(false);
    }
  };

  const search = async (event: FormEvent) => {
    event.preventDefault();
    if (!query.trim()) return;
    const data = await resourcesApi.search(query.trim(), lane);
    setResults(data.results);
    setMessage(`找到 ${data.count} 个私有索引片段。`);
  };

  const runAudit = async () => {
    setBusy(true);
    try {
      await resourcesApi.runAudit('content');
      setMessage('内容审计完成。');
      await refresh();
    } finally {
      setBusy(false);
    }
  };

  const runDue = async () => {
    setBusy(true);
    try {
      await resourcesApi.runDue();
      setMessage('到期订阅执行完成。');
      await refresh();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : '订阅执行失败。');
    } finally {
      setBusy(false);
    }
  };

  const resolveInbox = async (inboxId: string, action: 'approve' | 'reject') => {
    setBusy(true);
    try {
      await resourcesApi.resolveInbox(inboxId, action);
      setMessage(action === 'approve' ? '资源已批准。' : '资源已拒绝。');
      await refresh();
    } finally {
      setBusy(false);
    }
  };

  const toggleSubscription = async (subscription: ResourceSubscription) => {
    setBusy(true);
    try {
      await resourcesApi.updateSubscription(subscription.subscription_id, { enabled: !subscription.enabled });
      setMessage(subscription.enabled ? '订阅已暂停。' : '订阅已启用。');
      await refresh();
    } finally {
      setBusy(false);
    }
  };

  const toggleAiConsent = async () => {
    setBusy(true);
    try {
      const granted = !settings?.consent.openai_web_search;
      await resourcesApi.setAiDiscoveryConsent(granted);
      setMessage(granted ? '已授权 OpenAI Web Search 主动发现。' : '已撤销 OpenAI Web Search 主动发现授权。');
      await refresh();
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="metric-label text-accent">Resource Ingestion Kernel</p>
          <h2 className="mt-1 text-2xl font-bold">资源中心</h2>
          <p className="mt-1 text-sm text-muted">公开网络资源经过政策守卫、hash manifest 和私有全文索引，再进入 LanguageOS 或 CFA 审核链。</p>
        </div>
        <button type="button" onClick={() => refresh()} className="btn-secondary flex items-center gap-2">
          <RefreshCw size={15} /> 刷新状态
        </button>
      </header>

      {message ? <div className="rounded-lg border border-line bg-surface-raised px-4 py-3 text-sm">{message}</div> : null}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Metric icon={<Globe2 size={17} />} label="Providers" value={providers.filter((item) => item.configured).length} />
        <Metric icon={<Database size={17} />} label="Private documents" value={documents.length} />
        <Metric icon={<AlertTriangle size={17} />} label="Review inbox" value={inbox.length} />
        <Metric icon={<ShieldCheck size={17} />} label="Open findings" value={findings.length} />
      </div>

      <div className="grid gap-4 lg:grid-cols-[1fr_0.8fr]">
        <section className="card">
          <h3 className="font-semibold">立即抓取或订阅</h3>
          <p className="mt-1 text-xs text-muted">首期仅接受公开 URL，不使用登录态、浏览器 cookie 或本地文件协议。</p>
          <form onSubmit={crawl} className="mt-4 space-y-3">
            <div className="flex gap-2">
              {(['language', 'cfa'] as const).map((item) => (
                <button key={item} type="button" onClick={() => setLane(item)} className={lane === item ? 'btn-primary' : 'btn-secondary'}>
                  {item === 'language' ? 'LanguageOS' : 'CFA'}
                </button>
              ))}
            </div>
            <label className="block text-xs font-medium text-muted" htmlFor="resource-url">公开 URL 或 RSS / Atom 地址</label>
            <input id="resource-url" value={url} onChange={(event) => setUrl(event.target.value)} className="input w-full" placeholder="https://example.com/article" />
            <div className="flex flex-wrap gap-2">
              <button disabled={busy} className="btn-primary flex items-center gap-2"><Play size={14} /> 立即抓取</button>
              <button disabled={busy} type="button" onClick={subscribe} className="btn-secondary">保存 RSS 订阅</button>
            </div>
          </form>
        </section>

        <section className="card">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold">运行状态</h3>
            <div className="flex gap-3">
              <button type="button" disabled={busy} onClick={runDue} className="text-xs text-accent">运行到期订阅</button>
              <button type="button" disabled={busy} onClick={runAudit} className="text-xs text-accent">运行内容审计</button>
            </div>
          </div>
          <dl className="mt-4 space-y-3 text-sm">
            <Status label="Scheduler" value={scheduler.installed ? '已安装，每 6 小时' : '未安装，需要显式安装'} />
            <Status label="Task name" value={scheduler.task_name} />
            <Status label="Providers ready" value={`${providers.filter((item) => item.configured).length} / ${providers.length}`} />
            <Status label="Subscriptions" value={String(subscriptions.length)} />
            <Status label="每订阅抓取预算" value={`${settings?.subscription_resource_limit ?? 50} resources`} />
            <Status label="单域并发" value={String(settings?.per_domain_concurrency ?? 2)} />
          </dl>
          <div className="mt-4 flex items-center justify-between gap-3 rounded-lg border border-line p-3 text-xs">
            <span>OpenAI Web Search consent：{settings?.consent.openai_web_search ? '已授权' : '未授权'}</span>
            <button type="button" disabled={busy} onClick={toggleAiConsent} className="text-accent">
              {settings?.consent.openai_web_search ? '撤销' : '显式授权'}
            </button>
          </div>
          <p className="mt-4 text-xs text-muted">安装命令：<code>.\scripts\install-resource-scheduler.ps1</code></p>
        </section>
      </div>

      <section className="card">
        <form onSubmit={search} className="flex flex-col gap-3 sm:flex-row sm:items-end">
          <label className="flex-1 text-xs font-medium text-muted">
            私有全文搜索
            <input value={query} onChange={(event) => setQuery(event.target.value)} className="input mt-2 w-full" placeholder="duration sensitivity" />
          </label>
          <button className="btn-secondary flex items-center gap-2"><FileSearch size={15} /> 搜索</button>
        </form>
        <div className="mt-4 space-y-2">
          {results.map((item) => <div key={item.document_id + item.excerpt} className="rounded-lg border border-line p-3"><p className="text-sm font-medium">{item.title}</p><p className="mt-1 text-xs text-muted">{item.excerpt}</p></div>)}
          {query && results.length === 0 ? <p className="text-sm text-muted">当前 lane 没有命中结果。</p> : null}
        </div>
      </section>

      <div className="grid gap-4 lg:grid-cols-2">
        <List title="审核箱" empty="没有待审核资源。">{inbox.map((item) => <Row key={item.inbox_id} title={item.title || item.source_url || item.document_id} detail={`${item.lane} · ${item.reason}`}><button type="button" disabled={busy} onClick={() => resolveInbox(item.inbox_id, 'approve')} className="text-xs text-accent">批准</button><button type="button" disabled={busy} onClick={() => resolveInbox(item.inbox_id, 'reject')} className="text-xs text-danger">拒绝</button></Row>)}</List>
        <List title="Provider health" empty="没有 provider 状态。">{providers.map((item) => <Row key={item.provider_id} title={item.label} detail={`${item.health} · ${item.default_license_mode}`} />)}</List>
        <List title="订阅" empty="尚未保存订阅。">{subscriptions.map((item) => <Row key={item.subscription_id} title={item.target} detail={`${item.lane} · ${item.provider} · budget ${item.budget} · ${item.enabled ? 'enabled' : 'paused'}`}><button type="button" disabled={busy} onClick={() => toggleSubscription(item)} className="text-xs text-accent">{item.enabled ? '暂停' : '启用'}</button></Row>)}</List>
        <List title="任务队列" empty="还没有抓取任务。">{jobs.map((item) => <Row key={item.job_id} title={`${item.trigger} · ${item.status}`} detail={`budget ${item.budget_usage} · findings ${item.audit_summary.finding_count ?? 0}${item.retry_state.reason ? ` · ${item.retry_state.reason}` : ''}`} />)}</List>
        <List title="来源目录" empty="还没有资源文档。">{documents.map((item) => <Row key={item.document_id} title={item.title} detail={`${item.lane} · ${item.provider} · ${item.license_mode}${item.answer_bearing ? ' · answer-bearing' : ''}`} />)}</List>
        <List title="审计中心" empty="没有开放 finding。">{findings.map((item) => <Row key={item.finding_id} title={`${item.severity} · ${item.check_id}`} detail={item.remediation} />)}</List>
      </div>
    </div>
  );
}

function Metric({ icon, label, value }: { icon: React.ReactNode; label: string; value: number }) {
  return <div className="card"><div className="flex items-center gap-2 text-accent">{icon}<span className="metric-label">{label}</span></div><p className="metric-value mt-3">{value}</p></div>;
}

function Status({ label, value }: { label: string; value: string }) {
  return <div className="flex justify-between gap-3"><dt className="text-muted">{label}</dt><dd className="text-right font-medium">{value}</dd></div>;
}

function List({ title, empty, children }: { title: string; empty: string; children: React.ReactNode }) {
  return <section className="card"><h3 className="font-semibold">{title}</h3><div className="mt-4 space-y-2">{children || <p className="text-sm text-muted">{empty}</p>}</div></section>;
}

function Row({ title, detail, children }: { title: string; detail: string; children?: React.ReactNode }) {
  return <div className="rounded-lg border border-line p-3"><div className="flex items-start justify-between gap-3"><div className="min-w-0"><p className="truncate text-sm font-medium">{title}</p><p className="mt-1 text-xs text-muted">{detail}</p></div>{children ? <div className="flex shrink-0 gap-3">{children}</div> : null}</div></div>;
}
