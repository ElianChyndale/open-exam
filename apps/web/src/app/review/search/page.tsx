'use client';

import Link from 'next/link';
import { FormEvent, useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  ArrowRight,
  BarChart3,
  BookOpenCheck,
  Brain,
  CalendarCheck2,
  ClipboardCheck,
  FileSearch,
  Filter,
  Gauge,
  GitBranch,
  Languages,
  LineChart,
  Loader2,
  Map,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';

import {
  KnowledgeGraphNode,
  KnowledgeGraphSearchResult,
  knowledgeGraphApi,
} from '@/lib/api';

const nodeTypes = [
  '',
  'asset',
  'formula',
  'lexical_asset',
  'syllabus_topic',
  'coverage_record',
  'source_document',
  'source_segment',
  'resource',
  'transfer_gap',
  'assessment',
  'assessment_question',
  'study_plan',
  'analytics_record',
  'mission_action',
];

const validationOptions = ['', 'confirmed', 'validated', 'derived', 'draft', 'needs_review', 'rejected', 'generated'];
const qualityOptions = ['', 'trusted', 'high', 'medium', 'low', 'rejected'];

const systemLinks = [
  { href: '/review/tutor', label: 'Tutor', icon: Sparkles },
  { href: '/review/knowledge-map', label: 'Map', icon: Map },
  { href: '/review/lab', label: 'Review', icon: Brain },
  { href: '/review/assets', label: 'Assets', icon: FileSearch },
  { href: '/review/formulas', label: 'Formula', icon: BarChart3 },
  { href: '/review/coverage', label: 'Coverage', icon: BookOpenCheck },
  { href: '/review/mock-retro', label: 'Gaps', icon: GitBranch },
  { href: '/language/review', label: 'Language', icon: Languages },
  { href: '/review/assessments', label: 'Assessments', icon: ClipboardCheck },
  { href: '/review/analytics', label: 'Analytics', icon: LineChart },
  { href: '/review/study-planner', label: 'Planner', icon: CalendarCheck2 },
  { href: '/review/mission-control', label: 'Mission', icon: Gauge },
];

export default function ReviewSearchPage() {
  const [query, setQuery] = useState('WACC');
  const [nodeType, setNodeType] = useState('');
  const [validationStatus, setValidationStatus] = useState('');
  const [qualityStatus, setQualityStatus] = useState('');
  const [sourceRef, setSourceRef] = useState('');
  const [results, setResults] = useState<KnowledgeGraphSearchResult[]>([]);
  const [trace, setTrace] = useState<Record<string, any> | null>(null);
  const [impact, setImpact] = useState<Record<string, any> | null>(null);
  const [selected, setSelected] = useState<KnowledgeGraphNode | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const runSearch = async (event?: FormEvent) => {
    event?.preventDefault();
    setBusy(true);
    setError('');
    try {
      const payload = await knowledgeGraphApi.search({
        q: query,
        node_type: nodeType,
        validation_status: validationStatus,
        quality_status: qualityStatus,
        source_ref: sourceRef,
        limit: 40,
      });
      setResults(payload.results || []);
      setSelected(payload.results?.[0]?.node || null);
      if (payload.results?.[0]?.node) {
        const [nextTrace, nextImpact] = await Promise.all([
          knowledgeGraphApi.trace(payload.results[0].node.node_id),
          knowledgeGraphApi.impact(payload.results[0].node.node_id),
        ]);
        setTrace(nextTrace);
        setImpact(nextImpact);
      } else {
        setTrace(null);
        setImpact(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    runSearch().catch(() => undefined);
  }, []);

  const openTrace = async (node: KnowledgeGraphNode) => {
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

  const counts = useMemo(() => {
    const map: Record<string, number> = {};
    for (const item of results) map[item.node.node_type] = (map[item.node.node_type] || 0) + 1;
    return Object.entries(map).sort((a, b) => b[1] - a[1]);
  }, [results]);

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Search size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Global Search</h2>
          </div>
          <p className="mt-1 text-sm text-muted">{results.length} graph results / {selected?.node_type || 'no selection'}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/review/knowledge-map" className="btn-secondary inline-flex items-center gap-2">
            <Map size={14} />
            Knowledge Map
          </Link>
          <Link href={`/review/tutor?q=${encodeURIComponent(query)}`} className="btn-secondary inline-flex items-center gap-2">
            <Sparkles size={14} />
            Tutor
          </Link>
          <button type="button" onClick={() => runSearch()} disabled={busy} className="btn-primary inline-flex items-center gap-2">
            {busy ? <Loader2 size={15} className="animate-spin" /> : <RefreshCw size={15} />}
            Search
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
        <span>Correct-only graph search excludes raw wrong answers and internal submitted responses.</span>
      </div>

      <form onSubmit={runSearch} className="mb-4 grid gap-3 xl:grid-cols-[minmax(0,1fr)_180px_170px_150px_190px_auto]">
        <label className="rounded-lg border border-line bg-surface-raised p-3 text-xs font-semibold text-muted">
          Query
          <div className="mt-2 flex items-center gap-2 rounded-lg border border-line bg-surface-field px-3 py-2">
            <Search size={15} />
            <input
              aria-label="Search graph query"
              placeholder="Search graph"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className="min-w-0 flex-1 bg-transparent text-sm text-foreground outline-none"
            />
          </div>
        </label>
        <SelectFilter label="Node type" value={nodeType} onChange={setNodeType} options={nodeTypes} />
        <SelectFilter label="Validation" value={validationStatus} onChange={setValidationStatus} options={validationOptions} />
        <SelectFilter label="Quality" value={qualityStatus} onChange={setQualityStatus} options={qualityOptions} />
        <label className="rounded-lg border border-line bg-surface-raised p-3 text-xs font-semibold text-muted">
          Source ref
          <input
            aria-label="Filter by source reference"
            placeholder="ksource...#seg-1"
            value={sourceRef}
            onChange={(event) => setSourceRef(event.target.value)}
            className="mt-2 w-full rounded-lg border border-line bg-surface-field px-2 py-2 text-sm text-foreground"
          />
        </label>
        <button type="submit" disabled={busy} className="btn-primary inline-flex items-center justify-center gap-2 px-4">
          <Filter size={15} />
          Apply
        </button>
      </form>

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_390px]">
        <main className="space-y-3">
          <section className="grid gap-3 sm:grid-cols-3 xl:grid-cols-6">
            {counts.slice(0, 6).map(([type, count]) => (
              <div key={type} className="rounded-lg border border-line bg-surface-raised p-3">
                <p className="text-lg font-bold">{count}</p>
                <p className="mt-1 text-xs font-semibold text-muted">{labelize(type)}</p>
              </div>
            ))}
          </section>

          <section className="space-y-2">
            {results.map((item) => (
              <button
                key={item.node.node_id}
                type="button"
                onClick={() => openTrace(item.node)}
                className={`w-full rounded-lg border p-4 text-left transition-colors ${
                  selected?.node_id === item.node.node_id ? 'border-accent bg-accent-soft' : 'border-line bg-surface-raised hover:bg-surface-hover'
                }`}
              >
                <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded border border-accent-soft bg-accent-soft px-2 py-0.5 text-xs font-semibold text-accent">
                        {labelize(item.node.node_type)}
                      </span>
                      {item.node.validation_status && <StatusPill value={item.node.validation_status} />}
                      {item.node.status && <StatusPill value={item.node.status} />}
                    </div>
                    <h3 className="mt-2 truncate text-base font-semibold">{item.node.title}</h3>
                    {item.node.subtitle && <p className="mt-1 truncate text-sm text-muted">{item.node.subtitle}</p>}
                  </div>
                  <div className="text-right text-xs text-muted">
                    <p className="font-semibold text-foreground">{Math.round(item.score)}</p>
                    <p>{item.connected_nodes.length} links</p>
                  </div>
                </div>
                <div className="mt-3 flex flex-wrap gap-1">
                  {item.node.source_refs.slice(0, 3).map((ref) => <SourceRef key={ref} refText={ref} />)}
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  {item.node.launch_route && (
                    <Link href={item.node.launch_route} className="text-xs font-semibold text-accent hover:underline" onClick={(event) => event.stopPropagation()}>
                      Open route
                    </Link>
                  )}
                  {item.connected_nodes.slice(0, 3).map((node) => (
                    <span key={node.node_id} className="text-xs text-muted">{labelize(node.node_type)}: {node.title}</span>
                  ))}
                </div>
              </button>
            ))}
            {!results.length && <div className="rounded-lg border border-line bg-surface-raised p-8 text-center text-sm text-muted">No graph results.</div>}
          </section>
        </main>

        <aside className="space-y-4">
          <TracePanel trace={trace} impact={impact} />
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Links</h3>
            <div className="mt-3 grid grid-cols-2 gap-2">
              {systemLinks.map(({ href, label, icon: Icon }) => (
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
  if (!trace) {
    return <section className="rounded-lg border border-line bg-surface-raised p-4 text-sm text-muted">No trace selected.</section>;
  }
  return (
    <section className="rounded-lg border border-line bg-surface-raised p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="truncate font-semibold">{trace.node.title}</h3>
          <p className="mt-1 text-xs text-muted">{labelize(trace.node.node_type)} / {trace.node.status || trace.node.validation_status || 'open'}</p>
        </div>
        {trace.node.launch_route && (
          <Link
            href={trace.node.launch_route}
            aria-label="Open selected node route"
            title="Open route"
            className="btn-secondary inline-flex items-center gap-2"
          >
            <ArrowRight size={14} />
          </Link>
        )}
      </div>
      <TraceGroup title="Upstream" nodes={trace.upstream_lineage || []} />
      <TraceGroup title="Downstream" nodes={trace.downstream_usage || []} />
      <TraceGroup title="Related" nodes={trace.related_nodes || []} />
      <div className="mt-3 rounded-lg border border-line bg-surface-field p-3 text-sm">
        <p className="text-xs font-semibold text-muted">Quality Gates</p>
        <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
          <span>Status: {trace.quality_gates?.status || 'none'}</span>
          <span>Validation: {trace.quality_gates?.validation_status || 'none'}</span>
          <span>Quality: {trace.quality_gates?.quality_status || 'none'}</span>
          <span>Score: {trace.quality_gates?.quality_score ?? 'none'}</span>
        </div>
      </div>
      <div className="mt-3 rounded-lg border border-line bg-surface-field p-3 text-sm">
        <p className="text-xs font-semibold text-muted">Impact Analysis</p>
        <p className="mt-2 font-semibold">{impact?.affected_count || 0} affected nodes</p>
        <div className="mt-2 space-y-1 text-xs text-muted">
          {(impact?.impact_notes || []).slice(0, 4).map((note: string) => <p key={note}>{note}</p>)}
        </div>
      </div>
    </section>
  );
}

function TraceGroup({ title, nodes }: { title: string; nodes: KnowledgeGraphNode[] }) {
  return (
    <div className="mt-3">
      <p className="text-xs font-semibold text-muted">{title}</p>
      <div className="mt-2 space-y-2">
        {nodes.slice(0, 5).map((node) => (
          <div key={node.node_id} className="rounded-lg border border-line bg-surface-field p-2 text-sm">
            <p className="truncate font-semibold">{node.title}</p>
            <p className="mt-1 text-xs text-muted">{labelize(node.node_type)}</p>
          </div>
        ))}
        {!nodes.length && <p className="text-sm text-muted">None.</p>}
      </div>
    </div>
  );
}

function SelectFilter({ label, value, onChange, options }: { label: string; value: string; onChange: (value: string) => void; options: string[] }) {
  return (
    <label className="rounded-lg border border-line bg-surface-raised p-3 text-xs font-semibold text-muted">
      {label}
      <select value={value} onChange={(event) => onChange(event.target.value)} className="mt-2 w-full rounded-lg border border-line bg-surface-field px-2 py-2 text-sm text-foreground">
        {options.map((option) => <option key={option || 'all'} value={option}>{option ? labelize(option) : 'All'}</option>)}
      </select>
    </label>
  );
}

function StatusPill({ value }: { value: string }) {
  return <span className="rounded border border-line bg-surface-field px-2 py-0.5 text-xs font-semibold text-muted">{value}</span>;
}

function SourceRef({ refText }: { refText: string }) {
  return <span className="rounded border border-line bg-surface-field px-2 py-0.5 text-xs text-muted">{refText}</span>;
}

function labelize(value: string) {
  return value.replace(/_/g, ' ').replace(/\b\w/g, (match) => match.toUpperCase());
}
