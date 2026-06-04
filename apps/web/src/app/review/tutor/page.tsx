'use client';

import Link from 'next/link';
import { FormEvent, Suspense, useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  AlertTriangle,
  Archive,
  ArrowRight,
  BarChart3,
  BookOpenCheck,
  Brain,
  CalendarCheck2,
  Calculator,
  ClipboardCheck,
  Database,
  FileSearch,
  Gauge,
  GitBranch,
  Languages,
  Lightbulb,
  LineChart,
  Loader2,
  Map,
  MessageSquareText,
  Network,
  RefreshCw,
  Rocket,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  Wrench,
} from 'lucide-react';

import {
  TutorAskResponse,
  TutorConversation,
  TutorMode,
  TutorSourceContext,
  tutorApi,
} from '@/lib/api';

const modeOptions: Array<{ value: TutorMode; label: string; icon: any }> = [
  { value: 'explain', label: 'Explain', icon: MessageSquareText },
  { value: 'hint', label: 'Hint', icon: Lightbulb },
  { value: 'formula_help', label: 'Formula Help', icon: Calculator },
  { value: 'study_strategy', label: 'Study Strategy', icon: CalendarCheck2 },
  { value: 'language_help', label: 'Language Help', icon: Languages },
  { value: 'trace_source', label: 'Trace Source', icon: Network },
  { value: 'assessment_retro', label: 'Assessment Retro', icon: ClipboardCheck },
];

const systemLinks = [
  { href: '/onboarding', label: 'Onboard', icon: Rocket },
  { href: '/review/goals', label: 'Goals', icon: Gauge },
  { href: '/review/search', label: 'Search', icon: Search },
  { href: '/review/knowledge-map', label: 'Map', icon: Map },
  { href: '/review/lab', label: 'Review', icon: Brain },
  { href: '/review/formulas', label: 'Formula', icon: Calculator },
  { href: '/review/assessments', label: 'Assessments', icon: ClipboardCheck },
  { href: '/review/analytics', label: 'Analytics', icon: LineChart },
  { href: '/review/study-planner', label: 'Planner', icon: CalendarCheck2 },
  { href: '/review/resources', label: 'Resources', icon: ShieldCheck },
  { href: '/review/assets', label: 'Assets', icon: FileSearch },
  { href: '/language/review', label: 'Language', icon: Languages },
  { href: '/review/data', label: 'Data', icon: Database },
  { href: '/review/tools', label: 'Tools', icon: Wrench },
  { href: '/review/mission-control', label: 'Mission', icon: Gauge },
];

export default function TutorPage() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-7xl p-6 text-sm text-muted">Loading Tutor...</div>}>
      <TutorPageContent />
    </Suspense>
  );
}

function TutorPageContent() {
  const searchParams = useSearchParams();
  const initialMode = normalizeMode(searchParams.get('mode')) || 'formula_help';
  const initialQuery = searchParams.get('q') || searchParams.get('query') || 'Explain WACC and the calculator steps';
  const contextNodeId = searchParams.get('node_id');

  const [mode, setMode] = useState<TutorMode>(initialMode);
  const [query, setQuery] = useState(initialQuery);
  const [answer, setAnswer] = useState<TutorAskResponse | null>(null);
  const [conversation, setConversation] = useState<TutorConversation | null>(null);
  const [conversations, setConversations] = useState<TutorConversation[]>([]);
  const [suggestions, setSuggestions] = useState<Array<{ mode: TutorMode; title: string; query: string; launch_route: string }>>([]);
  const [contextPreview, setContextPreview] = useState<TutorSourceContext[]>([]);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const [suggestionPayload, conversationPayload, contextPayload] = await Promise.all([
        tutorApi.suggestions(),
        tutorApi.listConversations(),
        tutorApi.searchContext({ q: query, mode, limit: 5 }),
      ]);
      setSuggestions(suggestionPayload.suggestions || []);
      setConversations(conversationPayload.conversations || []);
      setContextPreview(contextPayload.source_context || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Tutor load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const ask = async (event?: FormEvent, override?: { mode?: TutorMode; query?: string }) => {
    event?.preventDefault();
    const nextMode = override?.mode || mode;
    const nextQuery = override?.query || query;
    if (!nextQuery.trim()) return;
    setMode(nextMode);
    setQuery(nextQuery);
    setBusy(true);
    setError('');
    try {
      const active =
        conversation?.mode === nextMode
          ? conversation
          :
        (await tutorApi.createConversation({
          mode: nextMode,
          title: nextQuery.length > 52 ? `${nextQuery.slice(0, 49)}...` : nextQuery,
        })).conversation;
      const result = await tutorApi.sendMessage(active.conversation_id, nextQuery);
      setConversation(result.conversation);
      setAnswer(result.answer);
      setContextPreview(result.answer.source_context || []);
      const latest = await tutorApi.listConversations();
      setConversations(latest.conversations || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Tutor request failed');
    } finally {
      setBusy(false);
    }
  };

  const archive = async () => {
    if (!conversation) return;
    setBusy(true);
    try {
      await tutorApi.archiveConversation(conversation.conversation_id);
      setConversation(null);
      const latest = await tutorApi.listConversations();
      setConversations(latest.conversations || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Archive failed');
    } finally {
      setBusy(false);
    }
  };

  const activeContexts = answer?.source_context?.length ? answer.source_context : contextPreview;
  const actions = answer?.recommended_actions || [];
  const messages = conversation?.messages || [];
  const citedRefs = useMemo(() => answer?.cited_source_refs || [], [answer]);

  return (
    <div className="mx-auto max-w-7xl pb-12">
      <div className="mb-5 flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles size={22} className="text-accent" />
            <h2 className="text-xl font-bold">Tutor Copilot</h2>
          </div>
          <p className="mt-1 text-sm text-muted">
            {answer ? `${answer.source_context.length} sources / ${answer.recommended_actions.length} actions` : `${contextPreview.length} context candidates`}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link href="/onboarding" className="btn-secondary inline-flex items-center gap-2">
            <Rocket size={14} />
            Onboarding
          </Link>
          <Link href="/review/goals" className="btn-secondary inline-flex items-center gap-2">
            <Gauge size={14} />
            Goals
          </Link>
          <Link href="/review/search" className="btn-secondary inline-flex items-center gap-2">
            <Search size={14} />
            Search
          </Link>
          <Link href="/review/knowledge-map" className="btn-secondary inline-flex items-center gap-2">
            <Map size={14} />
            Knowledge Map
          </Link>
          <Link href="/review/tools" className="btn-secondary inline-flex items-center gap-2">
            <Wrench size={14} />
            Tools
          </Link>
          <button type="button" onClick={load} disabled={loading || busy} className="btn-primary inline-flex items-center gap-2">
            {loading ? <Loader2 size={15} className="animate-spin" /> : <RefreshCw size={15} />}
            Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-danger-soft bg-danger-soft p-3 text-sm text-danger">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {answer?.missing_evidence && (
        <div className="mb-4 flex items-start gap-2 rounded-lg border border-warning-soft bg-warning-soft p-3 text-sm text-warning">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>Missing evidence: import or confirm local source-backed material before treating this answer as review content.</span>
        </div>
      )}

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_390px]">
        <main className="space-y-4">
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="grid gap-2 md:grid-cols-4 xl:grid-cols-7">
              {modeOptions.map(({ value, label, icon: Icon }) => (
                <button
                  key={value}
                  type="button"
                  onClick={() => setMode(value)}
                  className={`inline-flex min-h-10 items-center justify-center gap-2 rounded-lg border px-3 text-xs font-semibold transition-colors ${
                    mode === value ? 'border-accent bg-accent-soft text-accent' : 'border-line bg-surface-field text-muted hover:bg-surface-hover'
                  }`}
                >
                  <Icon size={14} />
                  {label}
                </button>
              ))}
            </div>

            <form onSubmit={ask} className="mt-4 grid gap-3 lg:grid-cols-[minmax(0,1fr)_auto]">
              <label className="text-xs font-semibold text-muted">
                Ask
                <textarea
                  aria-label="Tutor question"
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  className="mt-2 min-h-24 w-full resize-y rounded-lg border border-line bg-surface-field px-3 py-2 text-sm text-foreground"
                />
              </label>
              <button type="submit" disabled={busy || !query.trim()} className="btn-primary inline-flex items-center justify-center gap-2 self-end px-5">
                {busy ? <Loader2 size={15} className="animate-spin" /> : <Send size={15} />}
                Ask
              </button>
            </form>

            {suggestions.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2">
                {suggestions.slice(0, 5).map((item) => (
                  <button
                    key={`${item.mode}:${item.query}`}
                    type="button"
                    onClick={() => ask(undefined, { mode: item.mode, query: item.query })}
                    className="btn-secondary inline-flex items-center gap-2"
                  >
                    <ArrowRight size={14} />
                    {item.title}
                  </button>
                ))}
              </div>
            )}
          </section>

          <section className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_320px]">
            <div className="rounded-lg border border-line bg-surface-raised">
              <div className="flex items-center justify-between gap-3 border-b border-line px-4 py-3">
                <h3 className="font-semibold">Conversation</h3>
                {conversation && (
                  <button type="button" onClick={archive} disabled={busy} className="btn-secondary inline-flex items-center gap-2">
                    <Archive size={14} />
                    Archive
                  </button>
                )}
              </div>
              <div className="min-h-80 space-y-3 p-4">
                {messages.length === 0 && !answer ? (
                  <div className="rounded-lg border border-line bg-surface-field p-5 text-sm text-muted">
                    Select a mode and ask a grounded question.
                  </div>
                ) : (
                  messages.map((message) => (
                    <div
                      key={message.message_id}
                      className={`rounded-lg border p-3 ${
                        message.role === 'assistant' ? 'border-accent-soft bg-accent-soft' : 'border-line bg-surface-field'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-3">
                        <span className="text-xs font-semibold uppercase text-muted">{message.role}</span>
                        <span className="text-xs text-muted">{new Date(message.created_at).toLocaleTimeString()}</span>
                      </div>
                      <div className="mt-2 space-y-2 text-sm leading-6">
                        {message.content.split(/\n+/).map((line) => <p key={line}>{line}</p>)}
                      </div>
                      {message.cited_source_refs.length > 0 && (
                        <div className="mt-3 flex flex-wrap gap-1">
                          {message.cited_source_refs.slice(0, 5).map((ref) => <SourceRef key={ref} refText={ref} />)}
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>

            <aside className="rounded-lg border border-line bg-surface-raised p-4">
              <h3 className="font-semibold">Recent</h3>
              <div className="mt-3 space-y-2">
                {conversations.slice(0, 6).map((item) => (
                  <button
                    key={item.conversation_id}
                    type="button"
                    onClick={() => {
                      setConversation(item);
                      setMode(item.mode);
                      setContextPreview(item.source_context || []);
                    }}
                    className={`w-full rounded-lg border p-3 text-left text-sm transition-colors ${
                      conversation?.conversation_id === item.conversation_id ? 'border-accent bg-accent-soft' : 'border-line bg-surface-field hover:bg-surface-hover'
                    }`}
                  >
                    <p className="truncate font-semibold">{item.title}</p>
                    <p className="mt-1 text-xs text-muted">{labelize(item.mode)} / {item.messages.length} messages</p>
                  </button>
                ))}
                {!conversations.length && <p className="text-sm text-muted">No saved conversations.</p>}
              </div>
            </aside>
          </section>
        </main>

        <aside className="space-y-4">
          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <div className="flex items-center justify-between gap-3">
              <h3 className="font-semibold">Source Context</h3>
              <span className="text-xs font-semibold text-muted">{activeContexts.length}</span>
            </div>
            <div className="mt-3 space-y-3">
              {activeContexts.map((context) => <ContextCard key={context.context_id} context={context} />)}
              {!activeContexts.length && <p className="rounded-lg border border-line bg-surface-field p-3 text-sm text-muted">No source context.</p>}
            </div>
          </section>

          <section className="rounded-lg border border-line bg-surface-raised p-4">
            <h3 className="font-semibold">Recommended Actions</h3>
            <div className="mt-3 space-y-2">
              {actions.map((action) => (
                <Link key={`${action.title}:${action.launch_route}`} href={action.launch_route} className="block rounded-lg border border-line bg-surface-field p-3 transition-colors hover:bg-surface-hover">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-semibold">{action.title}</p>
                      <p className="mt-1 text-xs leading-5 text-muted">{action.reason}</p>
                    </div>
                    <ArrowRight size={15} className="mt-1 shrink-0 text-muted" />
                  </div>
                </Link>
              ))}
              {!actions.length && <p className="text-sm text-muted">Ask a question to generate actions.</p>}
            </div>
          </section>

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

          {citedRefs.length > 0 && (
            <section className="rounded-lg border border-line bg-surface-raised p-4">
              <h3 className="font-semibold">Citations</h3>
              <div className="mt-3 flex flex-wrap gap-1">
                {citedRefs.map((ref) => <SourceRef key={ref} refText={ref} />)}
              </div>
            </section>
          )}
        </aside>
      </div>
    </div>
  );
}

function ContextCard({ context }: { context: TutorSourceContext }) {
  return (
    <div className="rounded-lg border border-line bg-surface-field p-3">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-1">
            <span className="rounded border border-accent-soft bg-accent-soft px-2 py-0.5 text-xs font-semibold text-accent">
              {labelize(context.context_type)}
            </span>
            {context.validation_status && <StatusPill value={context.validation_status} />}
            {context.quality_status && <StatusPill value={context.quality_status} />}
          </div>
          <p className="mt-2 break-anywhere font-semibold">{context.title}</p>
        </div>
        <span className="text-xs font-semibold text-muted">{Math.round(context.relevance_score * 100)}</span>
      </div>
      <p className="mt-2 break-anywhere text-sm leading-5 text-muted">{context.excerpt}</p>
      <div className="mt-3 flex flex-wrap gap-1">
        {context.source_refs.slice(0, 4).map((ref) => <SourceRef key={ref} refText={ref} />)}
      </div>
      <div className="mt-3 flex flex-wrap gap-2">
        {context.launch_route && (
          <Link href={context.launch_route} className="text-xs font-semibold text-accent hover:underline">
            Open route
          </Link>
        )}
        {context.node_id && (
          <Link href={`/review/search?q=${encodeURIComponent(context.title)}`} className="text-xs font-semibold text-accent hover:underline">
            Trace
          </Link>
        )}
      </div>
    </div>
  );
}

function SourceRef({ refText }: { refText: string }) {
  return <span className="source-ref-token rounded border border-line bg-surface-raised px-2 py-0.5 text-xs text-muted">{refText}</span>;
}

function StatusPill({ value }: { value: string }) {
  return <span className="rounded border border-line bg-surface-raised px-2 py-0.5 text-xs font-semibold text-muted">{value}</span>;
}

function normalizeMode(value: string | null): TutorMode | null {
  const modes = new Set(modeOptions.map((item) => item.value));
  return value && modes.has(value as TutorMode) ? (value as TutorMode) : null;
}

function labelize(value: string) {
  return value.replace(/_/g, ' ').replace(/\b\w/g, (match) => match.toUpperCase());
}
