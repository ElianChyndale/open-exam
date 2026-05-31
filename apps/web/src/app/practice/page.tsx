'use client';

import { useEffect, useState } from 'react';
import { AlertTriangle, Check, FileQuestion, Play, ShieldCheck, X } from 'lucide-react';
import { practiceApi, questionBanksApi, type PracticeDrill, type PracticeQuestion } from '@/lib/api';
import { Alert, Badge, Button, EmptyState, Field, Select, Surface, TextArea } from '@/components/ui/ui';

export default function PracticePage() {
  const [sessionId, setSessionId] = useState('');
  const [items, setItems] = useState<PracticeQuestion[]>([]);
  const [drills, setDrills] = useState<PracticeDrill[]>([]);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [confidence, setConfidence] = useState(2);
  const [explanation, setExplanation] = useState('');
  const [result, setResult] = useState<any>(null);
  const [quarantine, setQuarantine] = useState<PracticeQuestion[]>([]);

  const refreshQuarantine = () => questionBanksApi.quarantine().then(({ questions }) => setQuarantine(questions));
  useEffect(() => { refreshQuarantine(); }, []);
  const item = items[index];

  const start = () => practiceApi.start().then((session) => {
    setSessionId(session.session_id); setItems(session.items); setDrills(session.drills); setIndex(0); setAnswer(''); setResult(null);
  });
  const submit = () => item && practiceApi.answer(sessionId, {
    question_id: item.question_id, answer, confidence, elapsed_seconds: 60, self_explanation: explanation,
  }).then(setResult);

  return (
    <div className="mx-auto max-w-6xl space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="metric-label">Verified evidence only</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight">Practice</h1>
          <p className="mt-2 text-sm text-muted">Mix private verified imports with targeted remediation without grading uncertain OCR.</p>
        </div>
        <Button onClick={start}><Play size={15} /> Start mixed session</Button>
      </header>

      <div className="grid gap-4 lg:grid-cols-[1fr_22rem]">
        <Surface className="space-y-4">
          {!item ? <EmptyState title={items.length ? 'Practice session complete' : 'Start a verified mixed session'} detail="Only reviewed question records enter grading." /> : (
            <>
              <div className="flex flex-wrap items-center justify-between gap-2"><Badge tone="accent">{item.topic}</Badge><span className="text-xs text-muted">{index + 1} / {items.length}</span></div>
              <div><p className="metric-label">{item.module} · {item.los}</p><h2 className="mt-2 text-xl font-semibold tracking-tight">{item.prompt}</h2></div>
              <fieldset className="space-y-2">
                <legend className="sr-only">Answer choices</legend>
                {item.choices.map((choice) => <label key={choice} className="flex cursor-pointer gap-2 rounded-xl border border-line p-3 text-sm hover:bg-surface-hover/70"><input type="radio" name="practice-answer" value={choice.slice(0, 1)} checked={answer === choice.slice(0, 1)} onChange={(event) => setAnswer(event.target.value)} />{choice}</label>)}
              </fieldset>
              <label className="block space-y-1 text-xs font-semibold text-muted"><span>Confidence</span><Select value={confidence} onChange={(event) => setConfidence(Number(event.target.value))}><option value={0}>Guess</option><option value={1}>Unsure</option><option value={2}>Moderate</option><option value={3}>Confident</option><option value={4}>Very confident</option></Select></label>
              <label className="block space-y-1 text-xs font-semibold text-muted"><span>Brief self-explanation</span><TextArea value={explanation} onChange={(event) => setExplanation(event.target.value)} placeholder="What rule decides this?" /></label>
              <Button disabled={!answer} onClick={submit}><Check size={15} /> Grade verified answer</Button>
              {result ? <Remediation result={result} onNext={() => { setIndex((current) => current + 1); setAnswer(''); setExplanation(''); setResult(null); }} /> : null}
            </>
          )}
        </Surface>

        <Surface className="space-y-3">
          <div className="flex items-center gap-2"><ShieldCheck size={16} className="text-accent" /><h2 className="text-sm font-semibold">Import review console</h2></div>
          <p className="text-xs text-muted">Quarantined extraction records stay outside grading until reviewed.</p>
          {quarantine.length === 0 ? <EmptyState title="Quarantine empty" detail="No uncertain OCR records await review." /> : quarantine.map((question) => <QuarantineRow key={question.question_id} question={question} refresh={refreshQuarantine} />)}
        </Surface>
      </div>
      {drills.length ? (
        <Surface className="space-y-3">
          <div className="flex items-center gap-2"><FileQuestion size={16} className="text-accent" /><h2 className="text-sm font-semibold">Personalized mistake-card drills</h2></div>
          <div className="grid gap-2 md:grid-cols-2">
            {drills.map((drill) => <details key={drill.drill_id} className="rounded-xl border border-line p-3 text-sm"><summary className="cursor-pointer font-medium">{drill.topic} · {drill.los}</summary><p className="mt-2 text-xs text-muted">{drill.prompt}</p><p className="mt-2 border-t border-line pt-2 text-xs">{drill.answer_text}</p></details>)}
          </div>
        </Surface>
      ) : null}
    </div>
  );
}

function Remediation({ result, onNext }: { result: any; onNext: () => void }) {
  return (
    <div className="space-y-3 rounded-xl border border-line bg-surface-sunken p-4">
      <Alert tone={result.is_correct ? 'success' : 'danger'}>{result.is_correct ? 'Correct. Keep the evidence trail.' : `Review answer ${result.correct_answer}: ${result.explanation}`}</Alert>
      {result.calibration_warning ? <Alert>{result.calibration_warning}</Alert> : null}
      <p className="text-xs text-muted">{result.self_explanation_prompt}</p>
      <div className="flex items-center justify-between gap-2"><Badge tone="accent">Remediation: {result.worked_example_stage}</Badge><Button variant="secondary" onClick={onNext}>Next question</Button></div>
    </div>
  );
}

function QuarantineRow({ question, refresh }: { question: PracticeQuestion; refresh: () => Promise<void> }) {
  const [correctAnswer, setCorrectAnswer] = useState(question.correct_answer || '');
  const [explanation, setExplanation] = useState(question.explanation || '');
  return (
    <div className="space-y-2 rounded-xl border border-warning/25 bg-warning/10 p-3">
      <div className="flex gap-2"><AlertTriangle size={14} className="mt-0.5 shrink-0 text-warning" /><p className="text-xs">{question.prompt || 'Missing extracted stem'}</p></div>
      <label className="block space-y-1 text-xs font-semibold text-muted"><span>Correct option</span><Field value={correctAnswer} onChange={(event) => setCorrectAnswer(event.target.value)} placeholder="A / B / C" /></label>
      <label className="block space-y-1 text-xs font-semibold text-muted"><span>Verified explanation</span><TextArea value={explanation} onChange={(event) => setExplanation(event.target.value)} /></label>
      <div className="flex gap-2">
        <Button variant="secondary" onClick={() => questionBanksApi.review(question.question_id, 'approve', { correct_answer: correctAnswer, explanation }).then(refresh)}><Check size={14} /> Approve</Button>
        <Button variant="danger" onClick={() => questionBanksApi.review(question.question_id, 'reject').then(refresh)}><X size={14} /> Reject</Button>
      </div>
    </div>
  );
}
