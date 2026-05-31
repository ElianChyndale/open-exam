/** API client for ExamOS backend. */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function request<T = any>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const error = await res.text();
    throw new Error(`API ${res.status}: ${error}`);
  }
  return res.json();
}

/** Attempts */
export const attemptsApi = {
  record: (data: Record<string, unknown>) =>
    request('/api/attempts', { method: 'POST', body: JSON.stringify(data) }),

  uploadScreenshot: (data: { topic: string; los?: string; image_data: string; filename: string }) =>
    request('/api/attempts/screenshot', { method: 'POST', body: JSON.stringify(data) }),

  listRecent: (limit = 20) =>
    request(`/api/attempts/recent?limit=${limit}`),
};

/** Diagnosis */
export const diagnosisApi = {
  diagnose: (data: { attempt_id: string; error_type?: string; user_notes?: string }) =>
    request('/api/diagnose', { method: 'POST', body: JSON.stringify(data) }),

  listPatterns: () =>
    request('/api/diagnose/patterns'),
};

/** Review Pack */
export const reviewApi = {
  getToday: (params?: Record<string, string>) => {
    const qs = new URLSearchParams(params || {}).toString();
    return request(`/api/review-pack/today${qs ? `?${qs}` : ''}`);
  },

  listDue: () => request('/api/review-pack/due'),
};

/** Energy */
export const energyApi = {
  checkIn: (data: { energy_level: number; mental_clarity: number; physical_fatigue: number; motivation: number; notes?: string }) =>
    request('/api/energy/check-in', { method: 'POST', body: JSON.stringify(data) }),

  history: (limit = 30) =>
    request(`/api/energy/history?limit=${limit}`),
};

/** Study Plan */
export const studyPlanApi = {
  getToday: (params?: Record<string, string>) => {
    const qs = new URLSearchParams(params || {}).toString();
    return request(`/api/study-plan/today${qs ? `?${qs}` : ''}`);
  },
};

/** Mock */
export const mockApi = {
  create: (data: Record<string, unknown>) =>
    request('/api/mock/create', { method: 'POST', body: JSON.stringify(data) }),

  getRetro: (sessionId: string) =>
    request(`/api/mock/${sessionId}/retro`, { method: 'POST' }),

  getBrief: (sessionId: string) =>
    request(`/api/mock/${sessionId}/brief`),

  listHistory: () => request('/api/mock/history'),

  startRun: (data: { session_label: string; total_minutes: number; total_questions: number }) =>
    request<{ run: MockRun }>('/api/mock/runs', { method: 'POST', body: JSON.stringify(data) }),

  listRuns: () => request<{ runs: MockRun[] }>('/api/mock/runs'),

  setRunState: (runId: string, action: 'pause' | 'resume' | 'complete', elapsedSeconds: number) =>
    request<{ run: MockRun }>(`/api/mock/runs/${runId}/state`, { method: 'POST', body: JSON.stringify({ action, elapsed_seconds: elapsedSeconds }) }),

  importResults: (data: Record<string, unknown>) =>
    request<{ run: MockRun }>('/api/mock/import-results', { method: 'POST', body: JSON.stringify(data) }),
};

/** Dashboard */
export const dashboardApi = {
  getEffectiveness: (days = 30) =>
    request(`/api/dashboard/effectiveness?days=${days}`),

  getSummary: () => request('/api/dashboard/summary'),
};

/** Institution */
export const institutionApi = {
  createCohort: (data: Record<string, unknown>) =>
    request('/api/institution/cohorts', { method: 'POST', body: JSON.stringify(data) }),

  getRiskReport: (cohortId: string) =>
    request(`/api/institution/cohorts/${cohortId}/risk-report`),

  listCohorts: () => request('/api/institution/cohorts'),

  listInterventions: () => request<{ interventions: Intervention[] }>('/api/institution/interventions'),

  createIntervention: (data: { learner_id: string; reason: string; owner_id?: string }) =>
    request<{ intervention: Intervention }>('/api/institution/interventions', { method: 'POST', body: JSON.stringify(data) }),

  deliveryProof: () => request<DeliveryProof>('/api/institution/delivery-proof'),
};

export interface Intervention {
  intervention_id: string;
  learner_id: string;
  reason: string;
  owner_id: string;
  status: string;
  created_at: string;
}

export interface DeliveryProof {
  cohort_count: number;
  intervention_count: number;
  weekly_report: WeeklyReport;
}

/** Daily learner loop */
export interface LearnerProfile {
  exam_date: string;
  current_phase: string;
  target_score_percentile: number;
  daily_minutes_available: number;
  weekly_study_days: number;
  preferred_session_minutes: number;
  peak_energy_window: string;
  moderate_energy_window: string;
  low_energy_window: string;
}

export interface DailyTask {
  task_id: string;
  title: string;
  topic: string;
  task_type: string;
  estimated_minutes: number;
  priority: number;
  energy_fit: string;
  status: 'pending' | 'completed' | 'skipped' | 'deferred';
}

export const profileApi = {
  get: () => request<{ profile: LearnerProfile }>('/api/profile'),
  update: (profile: LearnerProfile) =>
    request<{ profile: LearnerProfile }>('/api/profile', { method: 'PUT', body: JSON.stringify(profile) }),
};

export const curriculumApi = {
  get: () => request<{ subject_count: number; module_count: number; subjects: any[] }>('/api/curriculum'),
};

export const tasksApi = {
  getToday: (focusTopic = '') =>
    request<{ tasks: DailyTask[] }>(`/api/tasks/today${focusTopic ? `?focus_topic=${encodeURIComponent(focusTopic)}` : ''}`),
  setStatus: (taskId: string, status: DailyTask['status']) =>
    request<{ task: DailyTask }>(`/api/tasks/${taskId}/status`, { method: 'POST', body: JSON.stringify({ status }) }),
};

export const notificationsApi = {
  list: () => request<{ notifications: Array<{ notification_id: string; kind: string; title: string; detail: string }> }>('/api/notifications'),
};

export interface RetrievalItem {
  prompt_id: string;
  prompt_text: string;
  answer_text: string;
  topic: string;
  los: string;
}

export const retrievalApi = {
  start: (maxItems = 10) =>
    request<{ session_id: string; items: RetrievalItem[] }>('/api/review-sessions', { method: 'POST', body: JSON.stringify({ max_items: maxItems }) }),
  respond: (sessionId: string, payload: { prompt_id: string; score: number; self_explanation: string }) =>
    request<{ next_review_date: string; interval_days: number }>(`/api/review-sessions/${sessionId}/responses`, { method: 'POST', body: JSON.stringify(payload) }),
};

/** Verified private question banks and practice */
export interface PracticeQuestion {
  question_id: string;
  prompt: string;
  choices: string[];
  topic: string;
  module: string;
  los: string;
  verification_status: 'verified' | 'quarantined' | 'rejected';
  explanation?: string;
  correct_answer?: string;
  source_file?: string;
  source_page?: number;
}

export interface PracticeDrill {
  drill_id: string;
  source_kind: 'mistake_card' | 'weak_los' | 'adjacent_concept' | 'formula_recall' | 'concept_discrimination' | 'maintenance';
  topic: string;
  los: string;
  prompt: string;
  answer_text: string;
  fix_rule: string;
}

export const questionBanksApi = {
  quarantine: () => request<{ questions: PracticeQuestion[] }>('/api/question-banks/quarantine'),
  review: (questionId: string, action: 'approve' | 'reject', corrections: Record<string, unknown> = {}) =>
    request<{ question: PracticeQuestion }>(`/api/question-banks/${questionId}/review`, { method: 'POST', body: JSON.stringify({ action, corrections }) }),
};

export const practiceApi = {
  start: (maxItems = 10, topic = '') =>
    request<{ session_id: string; items: PracticeQuestion[]; drills: PracticeDrill[] }>('/api/practice-sessions', { method: 'POST', body: JSON.stringify({ max_items: maxItems, topic }) }),
  answer: (sessionId: string, payload: { question_id: string; answer: string; confidence: number; elapsed_seconds: number; self_explanation: string }) =>
    request<{ is_correct: boolean; correct_answer: string; explanation: string; calibration_state: string; calibration_warning?: string; self_explanation_prompt: string; explanation_quality: number; worked_example_stage: string }>(`/api/practice-sessions/${sessionId}/answers`, { method: 'POST', body: JSON.stringify(payload) }),
};

/** Offline mock, deterministic coach, FTS search, graph, and reports */
export interface MockRun {
  run_id: string;
  session_label: string;
  source_kind: 'local' | 'external_import';
  status: 'active' | 'paused' | 'completed';
  total_minutes: number;
  total_questions: number;
  elapsed_seconds: number;
  answered_count: number;
  correct_count: number;
  checkpoints: Array<{ question_number: number; target_elapsed_seconds: number }>;
  answers?: Array<{ question_id: string; answer?: string; correct_answer?: string; is_correct: boolean; topic?: string; los?: string }>;
}

export interface CoachBrief {
  brief_id: string;
  kind: string;
  summary: string;
  recommendations: string[];
  evidence_refs: string[];
  validated: boolean;
  created_at: string;
}

export const coachApi = {
  briefs: () => request<{ briefs: CoachBrief[] }>('/api/coach/briefs'),
  retro: (summary: string, sourceRefs: string[], biases: string[] = []) =>
    request<{ brief: CoachBrief }>('/api/coach/session-retro', { method: 'POST', body: JSON.stringify({ summary, source_refs: sourceRefs, biases }) }),
  auditAgent: (summary: string, sourceRefs: string[]) =>
    request<{ brief: CoachBrief }>('/api/coach/audit-agent', { method: 'POST', body: JSON.stringify({ summary, source_refs: sourceRefs }) }),
};

export interface SearchResult {
  document_id: string;
  kind: string;
  title: string;
  snippet: string;
  source_ref: string;
}

export const searchApi = {
  search: (query: string) => request<{ results: SearchResult[] }>(`/api/search?q=${encodeURIComponent(query)}`),
};

export interface GraphRecord {
  id: string;
  label: string;
  source_kind: 'official' | 'evidence' | 'personal';
  node_type?: string;
  source?: string;
  target?: string;
  x?: number;
  y?: number;
  notes?: string;
  locked?: boolean;
}

export const graphApi = {
  get: () => request<{ nodes: GraphRecord[]; edges: GraphRecord[] }>('/api/knowledge-graph'),
  updateOverlay: (nodes: GraphRecord[], edges: GraphRecord[]) =>
    request('/api/knowledge-graph/overlay', { method: 'PUT', body: JSON.stringify({ nodes, edges }) }),
};

export interface WeeklyReport {
  report_id: string;
  attempt_count: number;
  mock_run_count: number;
  coach_brief_count: number;
  evidence_refs: string[];
  markdown_content: string;
}

export const reportsApi = {
  weekly: () => request<WeeklyReport>('/api/reports/weekly'),
  weeklyMarkdownUrl: () => `${API_BASE}/api/reports/weekly?format=markdown`,
};

export const transferApi = {
  exportUrl: () => `${API_BASE}/api/export`,
  dryRunCloudTransfer: (organizationId: string) =>
    request('/api/import', { method: 'POST', body: JSON.stringify({ direction: 'local-to-cloud', organization_id: organizationId, dry_run: true }) }),
};
