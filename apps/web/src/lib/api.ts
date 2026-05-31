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
