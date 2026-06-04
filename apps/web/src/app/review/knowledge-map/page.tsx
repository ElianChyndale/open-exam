'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  BarChart3,
  BookOpenCheck,
  Brain,
  CalendarCheck2,
  ClipboardCheck,
  Database,
  FileSearch,
  Gauge,
  GitBranch,
  Languages,
  LineChart,
  Loader2,
  Map,
  Network,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  Target,
  Wrench,
} from 'lucide-react';

import {
  KnowledgeGraphNode,
  knowledgeGraphApi,
} from '@/lib/api';

const links = [
  { href: '/review/tutor', label: 'Tutor', icon: Sparkles },
  { href: '/review/search', label: 'Search', icon: Search },
  { href: '/review/data', label: 'Data', icon: Database },
  { href: '/review/tools', label: 'Tools', icon: Wrench },
  { href: '/review/lab', label: 'Review Lab', icon: Brain },
  { href: '/review/assets', label: 'Assets', icon: FileSearch },
  { href: '/review/formulas', label: 'Formulas', icon: BarChart3 },
  { href: '/review/coverage', label: 'Coverage', icon: BookOpenCheck },
  { href: '/review/mock-retro', label: 'Mock Retro', icon: GitBranch },
  { href: '/review/resources', label: 'Resources', icon: ShieldCheck },
  { href: '/language/review', label: 'Language', icon: Languages },
  { href: '/review/assessments', label: 'Assessments', icon: ClipboardCheck },
  { href: '/review/analytics', label: 'Analytics', icon: LineChart },
  { href: '/review/study-planner', label: 'Planner', icon: CalendarCheck2 },
  { href: '/review/mission-control', label: 'Mission', icon: Gauge },
];

export default function KnowledgeMapPage() {
  const [summary, setSummary] = useState<Record<string, any> | null>(null);
  const [nodes, setNodes] = useState<KnowledgeGraphNode[]>([]);
  const [selected, setSelected] = useState<KnowledgeGraphNode | null>(null);
  const [trace, setTrace] = useState<Record<string, any> | null>(null);
  const [impact, setImpact] = useState<Record<string, any> | null>(null);
  const [nodeType, setNodeType] = useState('');
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');

  const load = async (recompute = false, nextNodeType = nodeType) => {
    setBusy(true);
    setError('');
    try {
      const summaryPayload = recompute ? (await knowledgeGraphApi.recompute()).summary : await knowledgeGraphApi.summary();
      const nodePayload = await knowledgeGraphApi.nodes({ node_type: nextNodeType, limit: 120 });
      setSummary(summaryPayload);
      setNodes(nodePayload.nodes || []);
      const first = nodePayload.nodes?.[0] || null;
      setSelected(first);
      if (first) {
        setTrace(await knowledgeGraphApi.trace(first.node_id));
        setImpact(await knowledgeGraphApi.impact(first.node_id));
      } else {
        setTrace(null);
        setImpact(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Knowledge map load failed');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const selectNode = async (node: KnowledgeGraphNode) => {
    setSelected(node);
    setBusy(true);
    setError('');
    try {
      const [nextTrace, nextImpact] = await Promise.all([
        knowledgeGraphApi.trace(node.node_id),
        knowledgeGraphApi.impact(node.node_id),
      ]);
      setTrace(nextTrace);
      setImpact(nextImpact);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Trace load failed');
    } finally {
      setBusy(false);
    }
  };

  const typeRows = useMemo(() => objectEntries(summary?.nodes_by_type || {}).slice(0, 12), [summary]);
  const edgeRows = useMemo(() => objectEntries(summary?.edges_by_type || {}).slice(0, 12), [summary]);

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Map size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Knowledge Map</h2>
          </div>
          <p className="mt-1 text-sm text-muted">{summary ? `${summary.node_count} nodes / ${summary.edge_count} edges` : 'Loading graph projection'}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/review/search" className="btn-secondary inline-flex items-center gap-2">
            <Search size={14} />
            Global Search
          </Link>
          <Link href="/review/tutor" className="btn-secondary inline-flex items-center gap-2">
            <Sparkles size={14} />
            Tutor
          </Link>
          <Link href="/review/tools" className="btn-secondary inline-flex items-center gap-2">
            <Wrench size={14} />
            Tools
          </Link>
          <button type="button" onClick={() => load(true)} disabled={busy} className="btn-primary inline-flex items-center gap-2">
            {busy ? <Loader2 size={15} className="animate-spin" /> : <RefreshCw size={15} />}
            Recompute
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="mb-4 flex items-start gap-2 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
        <ShieldCheck size={16} className="mt-0.5 shrink-0" />
        <span>Correct-only traceability map hides wrong outputs and internal raw responses.</span>
      </div>

      <section className="mb-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        <Metric icon={Network} label="Nodes" value={String(summary?.node_count || 0)} />
        <Metric icon={GitBranch} label="Edges" value={String(summary?.edge_count || 0)} />
        <Metric icon={AlertTriangle} label="Unconfirmed" value={String(summary?.unconfirmed_islands || 0)} />
        <Metric icon={FileSearch} label="Missing Sources" value={String(summary?.missing_source_assets || 0)} />
        <Metric icon={Target} label="High-Value Topics" value={String(summary?.high_value_connected_topics || 0)} />
      </section>

      <div className="grid gap-4 xl:grid-cols-[280px_minmax(0,1fr)_390px]">
        <aside className="space-y-4">
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Nodes By Type</h3>
            <div className="mt-3 space-y-2">
              {typeRows.map(([type, count]) => (
                <button key={type} type="button" onClick={() => { setNodeType(type); load(false, type).catch(() => undefined); }} className="flex w-full items-center justify-between gap-3 rounded-lg border border-line bg-surface-field px-3 py-2 text-left text-sm">
                  <span className="text-muted">{labelize(type)}</span>
                  <span className="font-semibold">{String(count)}</span>
                </button>
              ))}
            </div>
          </section>
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Edges By Type</h3>
            <div className="mt-3 space-y-2">
              {edgeRows.map(([type, count]) => (
                <div key={type} className="flex items-center justify-between gap-3 rounded-lg border border-line bg-surface-field px-3 py-2 text-sm">
                  <span className="text-muted">{labelize(type)}</span>
                  <span className="font-semibold">{String(count)}</span>
                </div>
              ))}
            </div>
          </section>
        </aside>

        <main className="rounded-lg border border-line bg-surface-raised">
          <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-3">
            <h3 className="font-semibold">Graph Nodes</h3>
            <button type="button" onClick={() => { setNodeType(''); load(false, '').catch(() => undefined); }} className="text-xs font-semibold text-accent">
              All
            </button>
          </div>
          <div className="max-h-[720px] divide-y divide-line overflow-auto">
            {nodes.map((node) => (
              <button
                key={node.node_id}
                type="button"
                onClick={() => selectNode(node)}
                className={`grid w-full gap-3 px-4 py-3 text-left transition-colors lg:grid-cols-[150px_minmax(0,1fr)_110px] ${
                  selected?.node_id === node.node_id ? 'bg-accent-soft' : 'hover:bg-surface-hover'
                }`}
              >
                <span className="text-xs font-semibold text-accent">{labelize(node.node_type)}</span>
                <span className="min-w-0">
                  <span className="block truncate text-sm font-semibold">{node.title}</span>
                  <span className="mt-1 block truncate text-xs text-muted">{node.subtitle || node.source_refs[0] || node.node_id}</span>
                </span>
                <span className="text-xs text-muted">{node.validation_status || node.status || 'open'}</span>
              </button>
            ))}
            {!nodes.length && <div className="p-8 text-center text-sm text-muted">No nodes.</div>}
          </div>
        </main>

        <aside className="space-y-4">
          <TracePanel trace={trace} impact={impact} />
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Subsystem Links</h3>
            <div className="mt-3 grid grid-cols-2 gap-2">
              {links.map(({ href, label, icon: Icon }) => (
                <Link key={href} href={href} className="btn-secondary inline-flex items-center gap-2">
                  <Icon size={14} />
                  {label}
                </Link>
              ))}
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}

function TracePanel({ trace, impact }: { trace: Record<string, any> | null; impact: Record<string, any> | null }) {
  if (!trace) return <section className="rounded-lg border border-line bg-surface-raised p-4 text-sm text-muted">No node selected.</section>;
  return (
    <section className="rounded-lg border border-line bg-surface-raised p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="truncate font-semibold">{trace.node.title}</h3>
          <p className="mt-1 text-xs text-muted">{labelize(trace.node.node_type)}</p>
        </div>
        {trace.node.launch_route && (
          <Link href={trace.node.launch_route} className="btn-secondary inline-flex items-center gap-2">
            <ArrowRight size={14} />
          </Link>
        )}
      </div>
      <NodeGroup title="Upstream Lineage" nodes={trace.upstream_lineage || []} />
      <NodeGroup title="Downstream Usage" nodes={trace.downstream_usage || []} />
      <NodeGroup title="Related Nodes" nodes={trace.related_nodes || []} />
      <div className="mt-3 rounded-lg border border-line bg-surface-field p-3">
        <p className="text-xs font-semibold text-muted">Impact Analysis</p>
        <p className="mt-2 text-sm font-semibold">{impact?.affected_count || 0} affected nodes</p>
        <div className="mt-2 space-y-1 text-xs text-muted">
          {(impact?.impact_notes || []).map((note: string) => <p key={note}>{note}</p>)}
        </div>
      </div>
    </section>
  );
}

function NodeGroup({ title, nodes }: { title: string; nodes: KnowledgeGraphNode[] }) {
  return (
    <div className="mt-3">
      <p className="text-xs font-semibold text-muted">{title}</p>
      <div className="mt-2 space-y-2">
        {nodes.slice(0, 4).map((node) => (
          <div key={node.node_id} className="rounded-lg border border-line bg-surface-field p-2">
            <p className="truncate text-sm font-semibold">{node.title}</p>
            <p className="mt-1 text-xs text-muted">{labelize(node.node_type)}</p>
          </div>
        ))}
        {!nodes.length && <p className="text-sm text-muted">None.</p>}
      </div>
    </div>
  );
}

function Metric({ icon: Icon, label, value }: { icon: typeof Network; label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-surface-raised p-4">
      <div className="flex items-center justify-between gap-3">
        <Icon size={18} className="text-accent" />
        <span className="text-xl font-bold">{value}</span>
      </div>
      <p className="mt-2 text-xs font-semibold text-muted">{label}</p>
    </div>
  );
}

function objectEntries(value: Record<string, any>) {
  return Object.entries(value || {}).sort((a, b) => Number(b[1] || 0) - Number(a[1] || 0));
}

function labelize(value: string) {
  return value.replace(/_/g, ' ').replace(/\b\w/g, (match) => match.toUpperCase());
}
