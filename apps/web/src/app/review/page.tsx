'use client';

import { useState } from 'react';
import { BookOpen, Check, Eye, RotateCcw } from 'lucide-react';
import { retrievalApi, type RetrievalItem } from '@/lib/api';
import { Alert, Badge, Button, EmptyState, Select, Surface, TextArea } from '@/components/ui/ui';

export default function RetrievalReviewPage() {
  const [sessionId, setSessionId] = useState('');
  const [items, setItems] = useState<RetrievalItem[]>([]);
  const [index, setIndex] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [score, setScore] = useState(2);
  const [explanation, setExplanation] = useState('');
  const [message, setMessage] = useState('');

  const item = items[index];
  const start = () => retrievalApi.start().then((session) => {
    setSessionId(session.session_id);
    setItems(session.items);
    setIndex(0);
    setRevealed(false);
    setMessage('');
  });

  const submit = () => retrievalApi.respond(sessionId, { prompt_id: item.prompt_id, score, self_explanation: explanation }).then((result) => {
    setMessage(`Next review: ${result.next_review_date}`);
    setExplanation('');
    setRevealed(false);
    setIndex((current) => Math.min(current + 1, items.length));
  });

  return (
    <div className="mx-auto max-w-4xl space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="metric-label">Active recall before passive review</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight">Retrieval review</h1>
          <p className="mt-2 text-sm text-muted">Answer from memory, reveal the evidence, then score the quality of recall.</p>
        </div>
        <Button onClick={start}><RotateCcw size={15} /> Start session</Button>
      </header>

      {message ? <Alert tone="success">{message}</Alert> : null}
      {!item ? (
        <Surface><EmptyState title={items.length ? 'Session complete' : 'Start a retrieval session'} detail="Recent mistakes become concealed prompts with spaced follow-up dates." /></Surface>
      ) : (
        <Surface className="space-y-4">
          <div className="flex items-center justify-between gap-2"><Badge tone="accent">{item.topic}</Badge><span className="text-xs text-muted">{index + 1} / {items.length}</span></div>
          <div>
            <p className="metric-label">Closed-book prompt</p>
            <h2 className="mt-2 text-xl font-semibold tracking-tight">{item.prompt_text}</h2>
            <p className="mt-2 text-xs text-muted">{item.los}</p>
          </div>
          {!revealed ? (
            <Button onClick={() => setRevealed(true)}><Eye size={15} /> Reveal answer</Button>
          ) : (
            <>
              <div className="rounded-xl border border-success/25 bg-success/10 p-4">
                <p className="metric-label text-success">Evidence-backed answer</p>
                <p className="mt-2 text-sm">{item.answer_text}</p>
              </div>
              <label className="block space-y-1 text-xs font-semibold text-muted"><span>Recall score</span><Select value={score} onChange={(event) => setScore(Number(event.target.value))}><option value={0}>0 · No recall</option><option value={1}>1 · Fragmentary</option><option value={2}>2 · Partial</option><option value={3}>3 · Mostly correct</option><option value={4}>4 · Precise</option></Select></label>
              <label className="block space-y-1 text-xs font-semibold text-muted"><span>Self-explanation</span><TextArea value={explanation} onChange={(event) => setExplanation(event.target.value)} placeholder="What rule changes your next decision?" /></label>
              <Button onClick={submit}><Check size={15} /> Save response</Button>
            </>
          )}
        </Surface>
      )}

      <Surface>
        <div className="flex items-center gap-2"><BookOpen size={15} className="text-accent" /><h2 className="text-sm font-semibold">Legacy review pack</h2></div>
        <p className="mt-2 text-xs text-muted">The generated markdown review pack remains available through the CLI and `/api/review-pack/today` compatibility endpoint.</p>
      </Surface>
    </div>
  );
}
