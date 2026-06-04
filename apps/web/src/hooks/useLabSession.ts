'use client';

import { useState, useCallback, useRef, useEffect } from 'react';

export type UnitOutcome = 'recalled' | 'partial' | 'forgot' | 'skipped';

export interface ReviewLabUnit {
  unit_id: string;
  unit_type: string;
  prompt: string;
  recall_instruction?: string;
  answer?: string;
  formula_latex?: string;
  worked_example?: string;
  common_wrong_path?: string;
  exam_trap?: string;
  variables?: Array<{ symbol: string; meaning?: string; unit?: string; description?: string }>;
  applies_when?: string[];
  boundary_rules?: string[];
  ba_ii_plus_steps?: string[];
  source_refs?: string[];
  due_reason?: string;
  memory_state?: string;
  priority?: number;
  interaction_mode?: string;
  knowledge_id?: string;
  card_id?: string;
  subject?: string;
  heading?: string;
  los?: string;
}

export interface LabSession {
  session_id: string;
  review_id: string;
  status: 'active' | 'paused' | 'completed' | 'abandoned';
  units: ReviewLabUnit[];
  current_unit_index: number;
  current_unit: ReviewLabUnit | null;
  completed_unit_ids: string[];
  outcomes: Array<{
    unit_id: string;
    outcome: UnitOutcome;
    confidence_after: number;
    time_spent_seconds: number;
    needed_hint: boolean;
  }>;
  progress_pct: number;
  is_complete: boolean;
  energy_level: number;
  focus_topic: string;
  started_at: string;
}

interface UseLabSessionOptions {
  sessionId?: string;
}

/**
 * Manages Review Lab session state, including timing, outcomes,
 * and optimistic UI updates.
 */
export function useLabSession({ sessionId }: UseLabSessionOptions = {}) {
  const [session, setSession] = useState<LabSession | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [revealed, setRevealed] = useState(false);
  const [paused, setPaused] = useState(false);
  const [hintVisible, setHintVisible] = useState(false);
  const [hintText, setHintText] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const unitStartTime = useRef<number>(0);
  const hintUsed = useRef(false);

  // Reset per-unit state when current unit changes
  useEffect(() => {
    setRevealed(false);
    setHintVisible(false);
    setHintText('');
    hintUsed.current = false;
    unitStartTime.current = Date.now();
  }, [session?.current_unit_index]);

  const loadSession = useCallback(async (sid: string) => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`/api/review-lab/sessions/${sid}`);
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setSession(data);
      setPaused(data.status === 'paused');
    } catch (err: any) {
      setError(err.message || 'Failed to load session');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!sessionId || session || loading || error) return;
    loadSession(sessionId);
  }, [sessionId, session, loading, error, loadSession]);

  const createSession = useCallback(async (opts?: {
    review_id?: string;
    energy_level?: number;
    focus_topic?: string;
    max_units?: number;
  }) => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/review-lab/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          review_id: opts?.review_id || '',
          energy_level: opts?.energy_level ?? 2,
          focus_topic: opts?.focus_topic || '',
          max_units: opts?.max_units ?? 20,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setSession(data);
      setPaused(false);
      return data.session_id as string;
    } catch (err: any) {
      setError(err.message || 'Failed to create session');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const reveal = useCallback(() => {
    if (!session || paused) return;
    setRevealed(true);
  }, [session, paused]);

  const requestHint = useCallback(async () => {
    if (!session?.current_unit || paused) return;
    const unitId = session.current_unit.unit_id;
    try {
      const res = await fetch(`/api/review-lab/sessions/${session.session_id}/units/${unitId}/hint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hint_level: 1 }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setHintText(data.hint || '');
      setHintVisible(true);
      hintUsed.current = true;
    } catch (err: any) {
      setError(err.message || 'Failed to load hint');
    }
  }, [session, paused]);

  const submitOutcome = useCallback(async (outcome: UnitOutcome, confidenceAfter: number) => {
    if (!session?.current_unit || submitting) return;
    const unitId = session.current_unit.unit_id;
    const timeSpent = Math.round((Date.now() - unitStartTime.current) / 1000);

    setSubmitting(true);
    setError('');
    try {
      const res = await fetch(`/api/review-lab/sessions/${session.session_id}/units/${unitId}/outcome`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          confidence_before: 2,
          time_spent_seconds: timeSpent,
          needed_hint: hintUsed.current,
          outcome,
          confidence_after: confidenceAfter,
          answer_quality: outcome === 'recalled' ? 'perfect' : outcome === 'partial' ? 'minor_gap' : 'blank',
          next_action: outcome === 'recalled' ? 'advance' : 'drill',
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();

      // Optimistically update session
      setSession((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          current_unit_index: data.is_complete ? prev.units.length : prev.current_unit_index + (data.progress_pct > prev.progress_pct ? 1 : 0),
          current_unit: data.is_complete ? null : prev.units[data.is_complete ? prev.units.length : prev.current_unit_index + 1] || null,
          completed_unit_ids: [...prev.completed_unit_ids, unitId],
          outcomes: [...prev.outcomes, { unit_id: unitId, outcome, confidence_after: confidenceAfter, time_spent_seconds: timeSpent, needed_hint: hintUsed.current }],
          progress_pct: data.progress_pct,
          is_complete: data.is_complete,
        };
      });
      setRevealed(false);
      setHintVisible(false);
      setHintText('');
      hintUsed.current = false;
    } catch (err: any) {
      setError(err.message || 'Failed to submit outcome');
    } finally {
      setSubmitting(false);
    }
  }, [session, submitting]);

  const togglePause = useCallback(async () => {
    if (!session) return;
    const action = paused ? 'resume' : 'pause';
    try {
      const res = await fetch(`/api/review-lab/sessions/${session.session_id}/${action}`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setSession(data);
      setPaused(data.status === 'paused');
    } catch (err: any) {
      setError(err.message || `Failed to ${action} session`);
    }
  }, [session, paused]);

  const completeSession = useCallback(async () => {
    if (!session) return;
    try {
      const res = await fetch(`/api/review-lab/sessions/${session.session_id}/complete`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setSession(data);
      setPaused(false);
    } catch (err: any) {
      setError(err.message || 'Failed to complete session');
    }
  }, [session]);

  const fetchReport = useCallback(async () => {
    if (!session) return null;
    try {
      const res = await fetch(`/api/review-lab/sessions/${session.session_id}/report`);
      if (!res.ok) throw new Error(await res.text());
      return await res.json();
    } catch (err: any) {
      setError(err.message || 'Failed to load report');
      return null;
    }
  }, [session]);

  return {
    session,
    loading,
    error,
    revealed,
    paused,
    hintVisible,
    hintText,
    submitting,
    loadSession,
    createSession,
    reveal,
    requestHint,
    submitOutcome,
    togglePause,
    completeSession,
    fetchReport,
  };
}
