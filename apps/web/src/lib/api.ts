/** API client for OpenExam backend. */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || '';

async function request<T = any>(path: string, options?: RequestInit): Promise<T> {
  const headers = options?.body
    ? { 'Content-Type': 'application/json', ...options?.headers }
    : options?.headers;
  const res = await fetch(`${API_BASE}${path}`, {
    headers,
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

/** Daily Review */
export const reviewApi = {
  getToday: (params?: Record<string, string>) => {
    const qs = new URLSearchParams(params || {}).toString();
    return request(`/api/daily-review/today${qs ? `?${qs}` : ''}`);
  },

  listDue: () => request('/api/daily-review/due'),

  complete: (reviewId: string) =>
    request(`/api/daily-review/${reviewId}/complete`, { method: 'POST' }),
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

  getWeeklyFocus: () => request('/api/study-plan/weekly-focus'),
};

/** Todo */
export interface TodoTask {
  task_id: string;
  text: string;
  deadline: string;
  progress: number;
  status: 'pending' | 'completed';
  source: string;
}

export interface TodoState {
  date: string;
  title: string;
  focus: string;
  tasks: TodoTask[];
  revision: number;
}

export const todosApi = {
  getToday: (date = '') =>
    request<TodoState>(`/api/todos/today${date ? `?date=${encodeURIComponent(date)}` : ''}`),

  create: (data: { text: string; deadline?: string; progress?: number; expected_revision: number; date?: string }) =>
    request<TodoState>('/api/todos/tasks', { method: 'POST', body: JSON.stringify(data) }),

  update: (taskId: string, data: { text?: string; deadline?: string; progress?: number; status?: TodoTask['status']; expected_revision: number }) =>
    request<TodoState>(`/api/todos/tasks/${taskId}`, { method: 'PATCH', body: JSON.stringify(data) }),

  toggle: (taskId: string, expectedRevision: number) =>
    request<TodoState>(`/api/todos/tasks/${taskId}/toggle`, { method: 'POST', body: JSON.stringify({ expected_revision: expectedRevision }) }),

  remove: (taskId: string, expectedRevision: number) =>
    request<TodoState>(`/api/todos/tasks/${taskId}?expected_revision=${expectedRevision}`, { method: 'DELETE' }),

  importStudyPlan: (plan: Record<string, unknown>, confirmed: boolean) =>
    request<TodoState>('/api/todos/import-study-plan', { method: 'POST', body: JSON.stringify({ plan, confirmed }) }),
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
};

/** Dashboard */
export const dashboardApi = {
  getEffectiveness: (days = 30) =>
    request(`/api/dashboard/effectiveness?days=${days}`),

  getSummary: () => request('/api/dashboard/summary'),

  getMastery: () => request('/api/dashboard/mastery'),

  getCalendarData: (month = '') =>
    request(`/api/dashboard/calendar${month ? `?month=${encodeURIComponent(month)}` : ''}`),

  getCalibrationWarnings: () => request('/api/dashboard/calibration-warnings'),

  getStreaks: () => request('/api/dashboard/streaks'),

  getWeeklyTrend: () => request('/api/dashboard/weekly-trend'),

  updateCalendarSettings: (examDate: string) =>
    request('/api/dashboard/calendar/settings', { method: 'PUT', body: JSON.stringify({ exam_date: examDate }) }),

  runWhatIf: (adjustments: Record<string, number>) =>
    request('/api/dashboard/what-if', { method: 'POST', body: JSON.stringify(adjustments) }),
};

/** Institution */
export const institutionApi = {
  createCohort: (data: Record<string, unknown>) =>
    request('/api/institution/cohorts', { method: 'POST', body: JSON.stringify(data) }),

  getRiskReport: (cohortId: string) =>
    request(`/api/institution/cohorts/${cohortId}/risk-report`),

  listCohorts: () => request('/api/institution/cohorts'),

  getCohortWeaknesses: (cohortId: string) =>
    request(`/api/institution/cohorts/${cohortId}/weaknesses`),
};

/** Profiles */
export const profilesApi = {
  list: () => request('/api/profiles'),
  getActive: () => request('/api/profiles/active'),
  setActive: (profileName: string) =>
    request('/api/profiles/active', { method: 'PUT', body: JSON.stringify({ profile_name: profileName }) }),
};

/** Private question banks */
export const questionBanksApi = {
  importStructured: (data: { source_file: string; questions: Record<string, unknown>[] }) =>
    request('/api/question-banks/import', { method: 'POST', body: JSON.stringify(data) }),
  listQuarantine: () => request('/api/question-banks/quarantine'),
  review: (questionId: string, action: 'approve' | 'reject', patch: Record<string, unknown> = {}) =>
    request(`/api/question-banks/${questionId}/review`, { method: 'POST', body: JSON.stringify({ action, patch }) }),
};

/** LanguageOS */
export interface LanguageProfile {
  profile_id: string;
  target_language: string;
  native_language: string;
  level_target: string;
  domains: string[];
}

export interface LanguageSource {
  source_id: string;
  source_type: string;
  title: string;
  language: string;
  content_hash: string;
  url: string;
}

export interface LanguageSegment {
  segment_id: string;
  source_id: string;
  text: string;
  locator: string;
  start_time?: number | null;
  end_time?: number | null;
}

export interface LanguageItem {
  item_id: string;
  item_type: string;
  canonical_form: string;
  language: string;
  context_window: string[];
  source_segment_ids: string[];
}

export interface LanguageCard {
  card_id: string;
  item_id: string;
  card_type: string;
  front_payload: { prompt: string };
  back_payload: { answer: string; gloss?: string };
  context_window: string[];
  fsrs_state: Record<string, unknown>;
  due_at: string;
}

export const languageApi = {
  profiles: () => request<{ active_profile_id: string; profiles: LanguageProfile[] }>('/api/language/profiles'),
  selectProfile: (profileId: string) =>
    request<LanguageProfile>('/api/language/profiles/select', { method: 'POST', body: JSON.stringify({ profile_id: profileId }) }),
  settings: () => request<Record<string, boolean>>('/api/language/settings'),
  stats: () => request<Record<string, number | string>>('/api/language/stats'),
  sources: () => request<{ sources: LanguageSource[] }>('/api/language/sources'),
  createSource: (data: Record<string, unknown>) =>
    request<{ duplicate: boolean; source: LanguageSource; segments: LanguageSegment[] }>('/api/language/sources', { method: 'POST', body: JSON.stringify(data) }),
  segments: (sourceId = '') =>
    request<{ segments: LanguageSegment[] }>(`/api/language/segments${sourceId ? `?source_id=${encodeURIComponent(sourceId)}` : ''}`),
  items: () => request<{ items: LanguageItem[] }>('/api/language/items'),
  collectItem: (data: Record<string, unknown>) =>
    request<{ merged: boolean; item: LanguageItem }>('/api/language/items', { method: 'POST', body: JSON.stringify(data) }),
  dueCards: () => request<{ count: number; cards: LanguageCard[] }>('/api/language/cards/due'),
  generateCards: (itemId: string, cardTypes?: string[]) =>
    request<{ cards: LanguageCard[] }>('/api/language/cards/generate', { method: 'POST', body: JSON.stringify({ item_id: itemId, card_types: cardTypes }) }),
  reviewCard: (cardId: string, rating: 'again' | 'hard' | 'good' | 'easy') =>
    request<LanguageCard>(`/api/language/cards/${cardId}/review`, { method: 'POST', body: JSON.stringify({ rating }) }),
  analyzeGrammar: (segmentId: string) =>
    request<Record<string, any>>('/api/language/grammar/analyze', { method: 'POST', body: JSON.stringify({ segment_id: segmentId }) }),
  graph: () => request<{ edges: Record<string, any>[] }>('/api/language/intuition/graph'),
  rebuildGraph: () => request<{ count: number; edges: Record<string, any>[] }>('/api/language/intuition/rebuild', { method: 'POST' }),
  searchGraph: (query: string) =>
    request<{ items: LanguageItem[] }>(`/api/language/intuition/search?q=${encodeURIComponent(query)}`),
  createSession: (data: Record<string, unknown>) =>
    request('/api/language/sessions', { method: 'POST', body: JSON.stringify(data) }),
  export: (format: 'anki' | 'csv' | 'markdown' | 'obsidian') =>
    request<{ format: string; content: string; item_count: number }>(`/api/language/exports/${format}`),
};
