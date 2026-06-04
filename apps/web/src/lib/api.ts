/** API client for OpenExam backend. */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || '';

async function request<T = any>(path: string, options?: RequestInit): Promise<T> {
  const isFormData = typeof FormData !== 'undefined' && options?.body instanceof FormData;
  const headers = options?.body && !isFormData
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

  getProactive: () =>
    request<{ questions: any[] }>('/api/daily-review/proactive'),

  getCoverage: () =>
    request<Record<string, { captured: number; total: number; examWeight: number }>>('/api/daily-review/coverage'),
};

/** Energy */
export const energyApi = {
  checkIn: (data: { energy_level: number; mental_clarity: number; physical_fatigue: number; motivation: number; sleep_hours?: number; stress_level?: number; notes?: string }) =>
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

export type StudyEnergyMode = 'low' | 'normal' | 'high';

export interface StudyPlanBlock {
  block_id: string;
  plan_id: string;
  block_type:
    | 'review_lab'
    | 'formula_lab'
    | 'lexical_review'
    | 'coverage_gap'
    | 'mock_transfer_drill'
    | 'resource_confirmation'
    | 'asset_confirmation'
    | 'file_ingestion_cleanup'
    | 'mission_control_review'
    | 'reflection';
  title: string;
  description: string;
  target_minutes: number;
  priority: number;
  launch_route: string;
  due_reason: string;
  linked_asset_ids: string[];
  linked_topic_ids: string[];
  linked_gap_ids: string[];
  linked_resource_ids: string[];
  linked_lexical_ids: string[];
  prerequisites: string[];
  blocked_reason: string | null;
  status: 'pending' | 'in_progress' | 'completed' | 'skipped' | 'blocked';
  completion_outcome: string | null;
}

export interface AdaptiveStudyPlan {
  plan_id: string;
  profile_id: string;
  plan_date: string;
  energy_mode: StudyEnergyMode;
  available_minutes: number;
  goal: string | null;
  generated_at: string;
  status: 'draft' | 'active' | 'completed' | 'archived';
  blocks: StudyPlanBlock[];
  summary: Record<string, any>;
  source_signals: Record<string, any>;
  recommended_next_actions: string[];
}

/** Adaptive Study Planner */
export const studyPlannerApi = {
  generate: (data: { profile_id?: string; plan_date?: string; energy_mode: StudyEnergyMode; available_minutes: number; goal?: string }) =>
    request<AdaptiveStudyPlan>('/api/study-planner/generate', { method: 'POST', body: JSON.stringify(data) }),

  getToday: (params?: { profile_id?: string; date?: string }) => {
    const qs = new URLSearchParams();
    if (params?.profile_id) qs.set('profile_id', params.profile_id);
    if (params?.date) qs.set('date', params.date);
    return request<AdaptiveStudyPlan>(`/api/study-planner/today${qs.size ? `?${qs.toString()}` : ''}`);
  },

  getPlan: (planId: string) =>
    request<AdaptiveStudyPlan>(`/api/study-planner/plans/${planId}`),

  activate: (planId: string) =>
    request<AdaptiveStudyPlan>(`/api/study-planner/plans/${planId}/activate`, { method: 'POST' }),

  startBlock: (blockId: string) =>
    request<{ plan: AdaptiveStudyPlan; block: StudyPlanBlock }>(`/api/study-planner/blocks/${blockId}/start`, { method: 'POST' }),

  completeBlock: (blockId: string, data: { outcome?: string; actual_minutes?: number }) =>
    request<{ plan: AdaptiveStudyPlan; block: StudyPlanBlock }>(`/api/study-planner/blocks/${blockId}/complete`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  skipBlock: (blockId: string, reason: string) =>
    request<{ plan: AdaptiveStudyPlan; block: StudyPlanBlock }>(`/api/study-planner/blocks/${blockId}/skip`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
    }),

  completePlan: (planId: string) =>
    request<AdaptiveStudyPlan>(`/api/study-planner/plans/${planId}/complete`, { method: 'POST' }),

  history: (profileId = 'default', limit = 50) =>
    request<{ count: number; plans: AdaptiveStudyPlan[] }>(`/api/study-planner/history?profile_id=${encodeURIComponent(profileId)}&limit=${limit}`),
};

export type FocusStepType =
  | 'review_lab'
  | 'formula_lab'
  | 'lexical_review'
  | 'assessment'
  | 'tutor_hint'
  | 'coverage_confirmation'
  | 'resource_confirmation'
  | 'reflection';

export interface FocusStep {
  step_id: string;
  focus_id: string;
  step_type: FocusStepType;
  title: string;
  description: string;
  target_minutes: number;
  launch_route: string | null;
  embedded_payload: Record<string, any>;
  source_refs: string[];
  linked_asset_ids: string[];
  linked_topic_ids: string[];
  linked_lexical_ids: string[];
  linked_gap_ids: string[];
  status: 'pending' | 'in_progress' | 'completed' | 'skipped' | 'blocked';
  blocked_reason: string | null;
  correct_only_warning: string | null;
  completed_at?: string | null;
  completion_outcome?: string | null;
}

export interface FocusSession {
  focus_id: string;
  profile_id: string;
  plan_id: string | null;
  source: string;
  status: 'active' | 'completed' | 'abandoned';
  current_step_id: string | null;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
  total_target_minutes: number;
  steps: FocusStep[];
  summary: Record<string, any>;
}

export const focusApi = {
  start: (data?: { profile_id?: string; plan_id?: string | null; source?: string; force_new?: boolean }) =>
    request<FocusSession>('/api/focus/start', { method: 'POST', body: JSON.stringify(data || {}) }),

  current: (profileId = 'default') =>
    request<{ focus_session: FocusSession | null }>(`/api/focus/current?profile_id=${encodeURIComponent(profileId)}`),

  get: (focusId: string) =>
    request<FocusSession>(`/api/focus/${encodeURIComponent(focusId)}`),

  startStep: (focusId: string, stepId: string) =>
    request<FocusSession>(`/api/focus/${encodeURIComponent(focusId)}/steps/${encodeURIComponent(stepId)}/start`, { method: 'POST' }),

  completeStep: (focusId: string, stepId: string, data?: { outcome?: string; actual_minutes?: number; notes?: string }) =>
    request<FocusSession>(`/api/focus/${encodeURIComponent(focusId)}/steps/${encodeURIComponent(stepId)}/complete`, {
      method: 'POST',
      body: JSON.stringify(data || {}),
    }),

  skipStep: (focusId: string, stepId: string, reason = '') =>
    request<FocusSession>(`/api/focus/${encodeURIComponent(focusId)}/steps/${encodeURIComponent(stepId)}/skip`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
    }),

  complete: (focusId: string) =>
    request<FocusSession>(`/api/focus/${encodeURIComponent(focusId)}/complete`, { method: 'POST' }),

  abandon: (focusId: string, reason = '') =>
    request<FocusSession>(`/api/focus/${encodeURIComponent(focusId)}/abandon`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
    }),
};

/** Learning Analytics */
export type LearningAnalyticsRange = 'today' | '7d' | '30d' | 'all';

export interface LearningAnalyticsEvent {
  event_id: string;
  profile_id: string;
  event_type: string;
  occurred_at: string;
  subsystem: string;
  asset_id?: string | null;
  topic_id?: string | null;
  lexical_id?: string | null;
  formula_family?: string | null;
  plan_id?: string | null;
  block_id?: string | null;
  outcome?: string | null;
  confidence_before?: number | null;
  confidence_after?: number | null;
  time_spent_seconds?: number | null;
  source_refs: string[];
  metadata: Record<string, any>;
}

export interface LearningAnalyticsSummary {
  profile_id: string;
  generated_at: string;
  date_range: { range: string; start: string | null; end: string };
  overall: Record<string, any>;
  review_lab: Record<string, any>;
  formula_lab: Record<string, any>;
  language_os: Record<string, any>;
  study_planner: Record<string, any>;
  coverage: Record<string, any>;
  mock_retro: Record<string, any>;
  resource_os: Record<string, any>;
  file_ingestion: Record<string, any>;
  calibration: Record<string, any>;
  recommended_strategy_adjustments: Array<{ priority: number; action_id: string; title: string; href: string; reason?: string }>;
}

function analyticsQuery(profileId = 'default', range: LearningAnalyticsRange = '30d') {
  const qs = new URLSearchParams();
  qs.set('profile_id', profileId);
  qs.set('range', range);
  return qs.toString();
}

export const learningAnalyticsApi = {
  summary: (profileId = 'default', range: LearningAnalyticsRange = '30d') =>
    request<LearningAnalyticsSummary>(`/api/learning-analytics/summary?${analyticsQuery(profileId, range)}`),

  events: (profileId = 'default', range: LearningAnalyticsRange = '30d') =>
    request<{ profile_id: string; count: number; events: LearningAnalyticsEvent[] }>(`/api/learning-analytics/events?${analyticsQuery(profileId, range)}`),

  recompute: (profileId = 'default', range: LearningAnalyticsRange = '30d') =>
    request<{ profile_id: string; generated_at: string; event_count: number; summary: LearningAnalyticsSummary }>(
      '/api/learning-analytics/recompute',
      { method: 'POST', body: JSON.stringify({ profile_id: profileId, range }) },
    ),

  calibration: (profileId = 'default', range: LearningAnalyticsRange = '30d') =>
    request<{ profile_id: string; count: number; records: any[] }>(`/api/learning-analytics/calibration?${analyticsQuery(profileId, range)}`),

  masteryTrends: (profileId = 'default', range: LearningAnalyticsRange = '30d') =>
    request<{ profile_id: string; count: number; records: any[] }>(`/api/learning-analytics/mastery-trends?${analyticsQuery(profileId, range)}`),

  planEffectiveness: (profileId = 'default', range: LearningAnalyticsRange = '30d') =>
    request<Record<string, any>>(`/api/learning-analytics/plan-effectiveness?${analyticsQuery(profileId, range)}`),

  resourceUsefulness: (profileId = 'default', range: LearningAnalyticsRange = '30d') =>
    request<Record<string, any>>(`/api/learning-analytics/resource-usefulness?${analyticsQuery(profileId, range)}`),

  coverageMomentum: (profileId = 'default', range: LearningAnalyticsRange = '30d') =>
    request<Record<string, any>>(`/api/learning-analytics/coverage-momentum?${analyticsQuery(profileId, range)}`),

  formulaOutcomes: (profileId = 'default', range: LearningAnalyticsRange = '30d') =>
    request<Record<string, any>>(`/api/learning-analytics/formula-outcomes?${analyticsQuery(profileId, range)}`),

  languageOutcomes: (profileId = 'default', range: LearningAnalyticsRange = '30d') =>
    request<Record<string, any>>(`/api/learning-analytics/language-outcomes?${analyticsQuery(profileId, range)}`),
};

/** Adaptive Assessments */
export type AssessmentMode =
  | 'quick_check'
  | 'interleaving_drill'
  | 'formula_drill'
  | 'coverage_gap_drill'
  | 'mock_transfer_drill'
  | 'lexical_drill'
  | 'mixed_exam_drill';

export interface AssessmentQuestion {
  question_id: string;
  assessment_id: string;
  profile_id: string;
  question_type: string;
  prompt: string;
  choices: string[];
  correct_answer: string;
  correct_reasoning: string;
  correct_rule: string;
  formula_latex: string | null;
  ba_ii_plus_steps: string[];
  boundary_rules: string[];
  source_refs: string[];
  linked_asset_ids: string[];
  linked_topic_ids: string[];
  linked_gap_ids: string[];
  linked_lexical_ids: string[];
  difficulty: 'easy' | 'medium' | 'hard';
  interleaving_tags: string[];
  validation_status: string;
  category: string;
}

export interface AssessmentSession {
  assessment_id: string;
  profile_id: string;
  title: string;
  mode: AssessmentMode;
  generated_at: string;
  status: 'draft' | 'active' | 'completed' | 'archived';
  target_minutes: number;
  source_signals: Record<string, any>;
  question_ids: string[];
  summary: Record<string, any>;
  questions: AssessmentQuestion[];
  responses: any[];
  retro: Record<string, any>;
}

export const assessmentsApi = {
  generate: (data: {
    profile_id?: string;
    mode: AssessmentMode;
    target_minutes: number;
    question_count: number;
    difficulty?: 'easy' | 'medium' | 'hard';
    focus?: 'coverage' | 'formula' | 'transfer' | 'lexical' | 'mixed';
  }) =>
    request<AssessmentSession>('/api/assessments/generate', { method: 'POST', body: JSON.stringify(data) }),

  list: (profileId = 'default', limit = 50) =>
    request<{ profile_id: string; count: number; assessments: AssessmentSession[] }>(`/api/assessments?profile_id=${encodeURIComponent(profileId)}&limit=${limit}`),

  get: (assessmentId: string) =>
    request<AssessmentSession>(`/api/assessments/${assessmentId}`),

  start: (assessmentId: string) =>
    request<AssessmentSession>(`/api/assessments/${assessmentId}/start`, { method: 'POST' }),

  answer: (questionId: string, data: { answer_text?: string; selected_choice?: string; confidence_before?: number; time_spent_seconds?: number }) =>
    request<any>(`/api/assessments/questions/${questionId}/answer`, { method: 'POST', body: JSON.stringify(data) }),

  selfGrade: (questionId: string, data: { grade: 'correct' | 'partial' | 'incorrect'; confidence_after?: number }) =>
    request<any>(`/api/assessments/questions/${questionId}/self-grade`, { method: 'POST', body: JSON.stringify(data) }),

  complete: (assessmentId: string) =>
    request<AssessmentSession>(`/api/assessments/${assessmentId}/complete`, { method: 'POST' }),

  retro: (assessmentId: string) =>
    request<Record<string, any>>(`/api/assessments/${assessmentId}/retro`),

  recommendations: (profileId = 'default') =>
    request<Record<string, any>>(`/api/assessments/recommendations?profile_id=${encodeURIComponent(profileId)}`),
};

/** Knowledge Graph / Global Search */
export type KnowledgeGraphNodeType =
  | 'source_file'
  | 'source_document'
  | 'source_segment'
  | 'resource'
  | 'asset'
  | 'formula'
  | 'syllabus_topic'
  | 'coverage_record'
  | 'transfer_gap'
  | 'assessment'
  | 'assessment_question'
  | 'lexical_asset'
  | 'study_plan'
  | 'study_plan_block'
  | 'analytics_record'
  | 'mission_action';

export interface KnowledgeGraphNode {
  node_id: string;
  profile_id: string;
  node_type: KnowledgeGraphNodeType;
  title: string;
  subtitle: string | null;
  status: string | null;
  quality_score: number | null;
  validation_status: string | null;
  source_refs: string[];
  launch_route: string | null;
  metadata: Record<string, any>;
}

export interface KnowledgeGraphEdge {
  edge_id: string;
  profile_id: string;
  from_node_id: string;
  to_node_id: string;
  edge_type: string;
  confidence: number;
  reason: string;
  source_refs: string[];
  created_at: string;
}

export interface KnowledgeGraphSearchResult {
  node: KnowledgeGraphNode;
  score: number;
  connected_nodes: KnowledgeGraphNode[];
}

function graphQuery(params: Record<string, string | number | undefined>) {
  const qs = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') qs.set(key, String(value));
  });
  return qs.toString();
}

export const knowledgeGraphApi = {
  recompute: (profileId = 'default') =>
    request<{ profile_id: string; generated_at: string; summary: Record<string, any>; nodes: KnowledgeGraphNode[]; edges: KnowledgeGraphEdge[] }>(
      '/api/knowledge-graph/recompute',
      { method: 'POST', body: JSON.stringify({ profile_id: profileId }) },
    ),

  summary: (profileId = 'default') =>
    request<Record<string, any>>(`/api/knowledge-graph/summary?${graphQuery({ profile_id: profileId })}`),

  nodes: (opts?: { profile_id?: string; node_type?: string; validation_status?: string; quality_status?: string; source_ref?: string; limit?: number }) =>
    request<{ profile_id: string; count: number; nodes: KnowledgeGraphNode[] }>(
      `/api/knowledge-graph/nodes?${graphQuery({ profile_id: opts?.profile_id || 'default', node_type: opts?.node_type, validation_status: opts?.validation_status, quality_status: opts?.quality_status, source_ref: opts?.source_ref, limit: opts?.limit || 200 })}`,
    ),

  getNode: (nodeId: string, profileId = 'default') =>
    request<KnowledgeGraphNode>(`/api/knowledge-graph/nodes/${encodeURIComponent(nodeId)}?${graphQuery({ profile_id: profileId })}`),

  trace: (nodeId: string, profileId = 'default') =>
    request<Record<string, any>>(`/api/knowledge-graph/nodes/${encodeURIComponent(nodeId)}/trace?${graphQuery({ profile_id: profileId })}`),

  edges: (opts?: { profile_id?: string; edge_type?: string; from_node_id?: string; to_node_id?: string; limit?: number }) =>
    request<{ profile_id: string; count: number; edges: KnowledgeGraphEdge[] }>(
      `/api/knowledge-graph/edges?${graphQuery({ profile_id: opts?.profile_id || 'default', edge_type: opts?.edge_type, from_node_id: opts?.from_node_id, to_node_id: opts?.to_node_id, limit: opts?.limit || 500 })}`,
    ),

  search: (opts?: { profile_id?: string; q?: string; node_type?: string; validation_status?: string; quality_status?: string; module?: string; topic?: string; source_ref?: string; limit?: number }) =>
    request<{ profile_id: string; query: string; count: number; results: KnowledgeGraphSearchResult[] }>(
      `/api/knowledge-graph/search?${graphQuery({ profile_id: opts?.profile_id || 'default', q: opts?.q || '', node_type: opts?.node_type, validation_status: opts?.validation_status, quality_status: opts?.quality_status, module: opts?.module, topic: opts?.topic, source_ref: opts?.source_ref, limit: opts?.limit || 25 })}`,
    ),

  impact: (nodeId: string, profileId = 'default') =>
    request<Record<string, any>>(`/api/knowledge-graph/impact/${encodeURIComponent(nodeId)}?${graphQuery({ profile_id: profileId })}`),

  related: (nodeId: string, profileId = 'default', limit = 50) =>
    request<{ profile_id: string; node_id: string; count: number; nodes: KnowledgeGraphNode[] }>(
      `/api/knowledge-graph/related/${encodeURIComponent(nodeId)}?${graphQuery({ profile_id: profileId, limit })}`,
    ),
};

/** Grounded Tutor Copilot */
export type TutorMode =
  | 'explain'
  | 'hint'
  | 'compare'
  | 'formula_help'
  | 'study_strategy'
  | 'language_help'
  | 'trace_source'
  | 'assessment_retro'
  | 'general';

export interface TutorSourceContext {
  context_id: string;
  node_id: string | null;
  source_ref: string | null;
  context_type:
    | 'asset'
    | 'formula'
    | 'syllabus_topic'
    | 'coverage'
    | 'transfer_gap'
    | 'resource'
    | 'source_segment'
    | 'lexical_asset'
    | 'assessment'
    | 'study_plan'
    | 'analytics'
    | 'mission_action';
  title: string;
  excerpt: string;
  validation_status: string | null;
  quality_status: string | null;
  relevance_score: number;
  launch_route: string | null;
  source_refs: string[];
  details: Record<string, any>;
}

export interface TutorRecommendedAction {
  title: string;
  reason: string;
  launch_route: string;
  action_type:
    | 'review'
    | 'formula_practice'
    | 'assessment'
    | 'confirm_asset'
    | 'confirm_resource'
    | 'coverage_gap'
    | 'language_review'
    | 'study_plan'
    | 'analytics'
    | 'search'
    | 'data_backup';
}

export interface TutorMessage {
  message_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
  cited_source_refs: string[];
  linked_node_ids: string[];
  linked_asset_ids: string[];
  linked_topic_ids: string[];
  linked_routes: string[];
  safety_flags: string[];
}

export interface TutorConversation {
  conversation_id: string;
  profile_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  mode: TutorMode;
  messages: TutorMessage[];
  source_context: TutorSourceContext[];
  status: 'active' | 'archived';
}

export interface TutorAskResponse {
  profile_id: string;
  mode: TutorMode;
  query: string;
  answer: string;
  missing_evidence: boolean;
  source_context: TutorSourceContext[];
  recommended_actions: TutorRecommendedAction[];
  cited_source_refs: string[];
  linked_node_ids: string[];
  linked_asset_ids: string[];
  linked_topic_ids: string[];
  linked_routes: string[];
  safety_flags: string[];
  llm_provider: { enabled: boolean; fallback: string };
}

export const tutorApi = {
  ask: (data: { profile_id?: string; mode: TutorMode; query: string; context_node_id?: string | null }) =>
    request<TutorAskResponse>('/api/tutor/ask', { method: 'POST', body: JSON.stringify(data) }),

  searchContext: (opts?: { profile_id?: string; q?: string; mode?: TutorMode; limit?: number }) =>
    request<{ profile_id: string; query: string; mode: TutorMode; count: number; source_context: TutorSourceContext[] }>(
      `/api/tutor/search-context?${graphQuery({ profile_id: opts?.profile_id || 'default', q: opts?.q || '', mode: opts?.mode || 'general', limit: opts?.limit || 8 })}`,
    ),

  suggestions: (profileId = 'default') =>
    request<{ profile_id: string; suggestions: Array<{ mode: TutorMode; title: string; query: string; launch_route: string }>; recommended_actions: TutorRecommendedAction[] }>(
      `/api/tutor/suggestions?profile_id=${encodeURIComponent(profileId)}`,
    ),

  createConversation: (data: { profile_id?: string; mode: TutorMode; title?: string }) =>
    request<{ conversation: TutorConversation }>('/api/tutor/conversations', { method: 'POST', body: JSON.stringify(data) }),

  listConversations: (profileId = 'default', includeArchived = false) =>
    request<{ profile_id: string; count: number; conversations: TutorConversation[] }>(
      `/api/tutor/conversations?profile_id=${encodeURIComponent(profileId)}&include_archived=${includeArchived ? 'true' : 'false'}`,
    ),

  getConversation: (conversationId: string) =>
    request<TutorConversation>(`/api/tutor/conversations/${encodeURIComponent(conversationId)}`),

  sendMessage: (conversationId: string, content: string) =>
    request<{ conversation: TutorConversation; answer: TutorAskResponse }>(
      `/api/tutor/conversations/${encodeURIComponent(conversationId)}/message`,
      { method: 'POST', body: JSON.stringify({ content }) },
    ),

  archiveConversation: (conversationId: string) =>
    request<{ conversation: TutorConversation }>(`/api/tutor/conversations/${encodeURIComponent(conversationId)}/archive`, { method: 'POST' }),
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

/** Review Lab */
export const reviewLabApi = {
  createSession: (data: { review_id?: string; energy_level?: number; focus_topic?: string; max_units?: number }) =>
    request('/api/review-lab/sessions', { method: 'POST', body: JSON.stringify(data) }),

  getSession: (sessionId: string) =>
    request(`/api/review-lab/sessions/${sessionId}`),

  submitOutcome: (sessionId: string, unitId: string, data: {
    confidence_before?: number;
    time_spent_seconds?: number;
    needed_hint?: boolean;
    outcome: 'recalled' | 'partial' | 'forgot' | 'skipped';
    confidence_after?: number;
    answer_quality?: 'perfect' | 'minor_gap' | 'major_gap' | 'blank';
    next_action?: 'advance' | 'stay' | 'drill' | 'revisit_source';
  }) =>
    request(`/api/review-lab/sessions/${sessionId}/units/${unitId}/outcome`, { method: 'POST', body: JSON.stringify(data) }),

  requestHint: (sessionId: string, unitId: string, hintLevel = 1) =>
    request(`/api/review-lab/sessions/${sessionId}/units/${unitId}/hint`, { method: 'POST', body: JSON.stringify({ hint_level: hintLevel }) }),

  pause: (sessionId: string) =>
    request(`/api/review-lab/sessions/${sessionId}/pause`, { method: 'POST' }),

  resume: (sessionId: string) =>
    request(`/api/review-lab/sessions/${sessionId}/resume`, { method: 'POST' }),

  complete: (sessionId: string) =>
    request(`/api/review-lab/sessions/${sessionId}/complete`, { method: 'POST' }),

  getReport: (sessionId: string) =>
    request(`/api/review-lab/sessions/${sessionId}/report`),

  getHistory: (limit = 50) =>
    request<{ sessions: any[] }>(`/api/review-lab/history?limit=${limit}`),

  getMissionControl: (profileId = 'default') =>
    request<{ profile_id: string; generated_at: string; review_lab: any; assets: any; formulas: any; coverage: any; mock_retro: any; resources: any; language: any; data_governance: any; tutor: any; system_health: any; recommended_actions: any[] }>(
      `/api/review-lab/mission-control?profile_id=${encodeURIComponent(profileId)}`,
    ),

  getRouteRegistry: () =>
    request<{ feature_groups: Record<string, any>; expected_pages: any[]; expected_api_routes: any[] }>('/api/review-lab/route-registry'),

  importTextSource: (data: { profile_id?: string; title: string; text: string; source_type?: 'pdf_note' | 'markdown_note' | 'text_note' | 'manual' }) =>
    request('/api/review-lab/sources/import-text', { method: 'POST', body: JSON.stringify(data) }),

  importSourceFile: (data: { file: File; profile_id?: string; title?: string; source_type?: 'pdf_note' | 'markdown_note' | 'text_note' | 'manual'; force_reimport?: boolean }) => {
    const form = new FormData();
    form.append('file', data.file);
    if (data.profile_id) form.append('profile_id', data.profile_id);
    if (data.title) form.append('title', data.title);
    if (data.source_type) form.append('source_type', data.source_type);
    if (data.force_reimport) form.append('force_reimport', String(data.force_reimport));
    return request<{ duplicate: boolean; file: any; source?: any; segments: any[]; warnings: string[]; count: number; assets: any[] }>(
      '/api/review-lab/sources/import-file',
      { method: 'POST', body: form },
    );
  },

  listSources: () =>
    request<{ count: number; sources: any[] }>('/api/review-lab/sources'),

  getSource: (sourceId: string) =>
    request(`/api/review-lab/sources/${sourceId}`),

  extractAssets: (sourceId: string) =>
    request<{ count: number; assets: any[] }>(`/api/review-lab/sources/${sourceId}/extract-assets`, { method: 'POST' }),

  importResourceText: (data: {
    profile_id?: string;
    title: string;
    text: string;
    resource_type?: 'text_note' | 'pdf_note' | 'web_article' | 'official_syllabus' | 'textbook' | 'lecture_slide' | 'dictionary' | 'manual' | 'unknown';
    origin?: 'manual' | 'import_text' | 'file' | 'url' | 'system_seed';
    url?: string;
    file_path?: string;
    notes?: string;
  }) =>
    request<{ duplicate: boolean; resource: any; evidence_count: number; evidence: any[] }>('/api/review-lab/resources/import-text', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  importResourceFile: (data: { file: File; profile_id?: string; title?: string; resource_type?: string; notes?: string; force_reimport?: boolean }) => {
    const form = new FormData();
    form.append('file', data.file);
    if (data.profile_id) form.append('profile_id', data.profile_id);
    if (data.title) form.append('title', data.title);
    if (data.resource_type) form.append('resource_type', data.resource_type);
    if (data.notes) form.append('notes', data.notes);
    if (data.force_reimport) form.append('force_reimport', String(data.force_reimport));
    return request<{ duplicate: boolean; file: any; resource?: any; quality_gate?: any; segments: any[]; warnings: string[]; evidence_count: number; evidence: any[]; candidate_count: number; candidate_assets: any[] }>(
      '/api/review-lab/resources/import-file',
      { method: 'POST', body: form },
    );
  },

  listFiles: (profileId = '') =>
    request<{ count: number; files: any[] }>(`/api/review-lab/files${profileId ? `?profile_id=${encodeURIComponent(profileId)}` : ''}`),

  getFile: (fileId: string) =>
    request<{ file: any }>(`/api/review-lab/files/${fileId}`),

  extractFile: (fileId: string) =>
    request<{ duplicate: boolean; file: any; segments: any[]; warnings: string[] }>(`/api/review-lab/files/${fileId}/extract`, { method: 'POST' }),

  listFileSegments: (fileId: string) =>
    request<{ count: number; segments: any[] }>(`/api/review-lab/files/${fileId}/segments`),

  listFileCandidateAssets: (fileId: string) =>
    request<{ count: number; assets: any[] }>(`/api/review-lab/files/${fileId}/candidate-assets`),

  listResources: (profileId = 'default') =>
    request<{ count: number; resources: any[] }>(`/api/review-lab/resources?profile_id=${encodeURIComponent(profileId)}`),

  getResource: (resourceId: string) =>
    request<{ resource: any; evidence_count: number; evidence: any[]; candidate_count: number; candidate_assets: any[] }>(
      `/api/review-lab/resources/${resourceId}`,
    ),

  scoreResource: (resourceId: string) =>
    request<{ resource: any; quality_gate: any }>(`/api/review-lab/resources/${resourceId}/score`, { method: 'POST' }),

  extractResourceEvidence: (resourceId: string) =>
    request<{ resource: any; evidence_count: number; evidence: any[]; candidate_count: number; candidate_assets: any[]; conflicts: string[] }>(
      `/api/review-lab/resources/${resourceId}/extract-evidence`,
      { method: 'POST' },
    ),

  listResourceEvidence: (resourceId: string) =>
    request<{ count: number; evidence: any[] }>(`/api/review-lab/resources/${resourceId}/evidence`),

  listResourceCandidateAssets: (resourceId: string) =>
    request<{ count: number; assets: any[] }>(`/api/review-lab/resources/${resourceId}/candidate-assets`),

  confirmResource: (resourceId: string) =>
    request<{ resource: any; quality_gate: any }>(`/api/review-lab/resources/${resourceId}/confirm`, { method: 'POST' }),

  rejectResource: (resourceId: string) =>
    request<{ resource: any; rejected_assets: any[] }>(`/api/review-lab/resources/${resourceId}/reject`, { method: 'POST' }),

  promoteResourceAssets: (resourceId: string, assetIds?: string[]) =>
    request<{ resource: any; quality_gate: any; promoted_count: number; assets: any[] }>(
      `/api/review-lab/resources/${resourceId}/promote-assets`,
      { method: 'POST', body: JSON.stringify({ asset_ids: assetIds || [] }) },
    ),

  getResourceQualityReport: (profileId = 'default') =>
    request<{ profile_id: string; resource_count: number; summary: Record<string, number>; candidate_asset_count: number; promoted_asset_count: number; conflict_count: number; resources: any[] }>(
      `/api/review-lab/resources/quality-report?profile_id=${encodeURIComponent(profileId)}`,
    ),

  listAssets: (opts?: { validation_status?: string; source_id?: string }) => {
    const params = new URLSearchParams();
    if (opts?.validation_status) params.set('validation_status', opts.validation_status);
    if (opts?.source_id) params.set('source_id', opts.source_id);
    return request<{ count: number; assets: any[] }>(`/api/review-lab/assets${params.size ? `?${params.toString()}` : ''}`);
  },

  confirmAsset: (assetId: string) =>
    request<{ asset: any }>(`/api/review-lab/assets/${assetId}/confirm`, { method: 'POST' }),

  rejectAsset: (assetId: string) =>
    request<{ asset: any }>(`/api/review-lab/assets/${assetId}/reject`, { method: 'POST' }),

  listFormulas: (opts?: { validation_status?: string; profile_id?: string }) => {
    const params = new URLSearchParams();
    if (opts?.validation_status) params.set('validation_status', opts.validation_status);
    if (opts?.profile_id) params.set('profile_id', opts.profile_id);
    return request<{ count: number; assets: any[] }>(`/api/review-lab/formulas${params.size ? `?${params.toString()}` : ''}`);
  },

  importFormulaText: (data: { profile_id?: string; title: string; text: string }) =>
    request<{ source: any; segments: any[]; count: number; assets: any[] }>('/api/review-lab/formulas/import-text', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  enrichFormula: (assetId: string) =>
    request<{ asset: any }>(`/api/review-lab/formulas/${assetId}/enrich`, { method: 'POST' }),

  confirmFormula: (assetId: string) =>
    request<{ asset: any }>(`/api/review-lab/formulas/${assetId}/confirm`, { method: 'POST' }),

  rejectFormula: (assetId: string) =>
    request<{ asset: any }>(`/api/review-lab/formulas/${assetId}/reject`, { method: 'POST' }),

  generateFormulaSession: (data: { profile_id?: string; max_units?: number }) =>
    request('/api/review-lab/formulas/generate-session', { method: 'POST', body: JSON.stringify(data) }),

  completeFormulaUnit: (unitId: string, data: {
    session_id?: string;
    confidence_before?: number;
    time_spent_seconds?: number;
    needed_hint?: boolean;
    outcome: 'recalled' | 'partial' | 'forgot' | 'skipped';
    confidence_after?: number;
    answer_quality?: 'perfect' | 'minor_gap' | 'major_gap' | 'blank';
    next_action?: 'advance' | 'stay' | 'drill' | 'revisit_source';
  }) =>
    request(`/api/review-lab/formulas/units/${unitId}/complete`, { method: 'POST', body: JSON.stringify(data) }),

  importSyllabusText: (data: { profile_id?: string; exam?: string; text: string }) =>
    request<{ created: number; updated: number; count: number; topics: any[] }>('/api/review-lab/syllabus/import-text', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  importSyllabusJson: (data: { profile_id?: string; exam?: string; topics?: any[]; payload?: any }) =>
    request<{ created: number; updated: number; count: number; topics: any[] }>('/api/review-lab/syllabus/import-json', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  seedDemoSyllabus: (profileId = 'default') =>
    request<{ created: number; updated: number; count: number; topics: any[] }>(
      `/api/review-lab/syllabus/seed-demo?profile_id=${encodeURIComponent(profileId)}`,
      { method: 'POST' },
    ),

  listSyllabusTopics: (profileId = 'default') =>
    request<{ count: number; topics: any[] }>(`/api/review-lab/syllabus/topics?profile_id=${encodeURIComponent(profileId)}`),

  getSyllabusCoverage: (profileId = 'default') =>
    request<{
      profile_id: string;
      topic_count: number;
      asset_count: number;
      link_count: number;
      summary: Record<string, number>;
      records: any[];
      links: any[];
      coverage_scoring_formula: string;
    }>(`/api/review-lab/syllabus/coverage?profile_id=${encodeURIComponent(profileId)}`),

  recomputeSyllabusCoverage: (profileId = 'default') =>
    request<{
      profile_id: string;
      topic_count: number;
      asset_count: number;
      link_count: number;
      summary: Record<string, number>;
      records: any[];
      links: any[];
      coverage_scoring_formula: string;
    }>(`/api/review-lab/syllabus/recompute-coverage?profile_id=${encodeURIComponent(profileId)}`, { method: 'POST' }),

  importMockRetroText: (data: { profile_id?: string; title: string; exam?: string; text: string }) =>
    request<{ session: any; evidence_count: number; evidence: any[]; duplicate: boolean }>('/api/review-lab/mock-retro/import-text', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  listMockRetroSessions: (profileId = 'default') =>
    request<{ count: number; sessions: any[] }>(`/api/review-lab/mock-retro/sessions?profile_id=${encodeURIComponent(profileId)}`),

  getMockRetroSession: (mockId: string) =>
    request<{ session: any; evidence_count: number; evidence: any[] }>(`/api/review-lab/mock-retro/sessions/${mockId}`),

  analyzeMockRetroSession: (mockId: string) =>
    request<{ session: any; gap_count: number; gaps: any[] }>(`/api/review-lab/mock-retro/sessions/${mockId}/analyze`, { method: 'POST' }),

  listTransferGaps: (opts?: { profile_id?: string; status?: string }) => {
    const params = new URLSearchParams();
    if (opts?.profile_id) params.set('profile_id', opts.profile_id);
    if (opts?.status) params.set('status', opts.status);
    return request<{ count: number; gaps: any[] }>(`/api/review-lab/mock-retro/transfer-gaps${params.size ? `?${params.toString()}` : ''}`);
  },

  resolveTransferGap: (gapId: string) =>
    request<{ gap: any }>(`/api/review-lab/mock-retro/transfer-gaps/${gapId}/resolve`, { method: 'POST' }),

  generateMockRetroReview: (data: { profile_id?: string; max_units?: number }) =>
    request('/api/review-lab/mock-retro/generate-review', { method: 'POST', body: JSON.stringify(data) }),
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

/** DictionaryOS */
export interface DictionaryResult {
  lemma: string;
  pos: string;
  definition: string;
  translation: string;
  language: string;
  source_id: string;
  entry_json: string;
  rank: number;
}

export const dictionaryApi = {
  importDictionary: (data: {
    title: string;
    language_pair: string;
    content: string;
    filename?: string;
    license_mode?: string;
    priority?: number;
    format?: string;
  }) =>
    request<{ duplicate: boolean; source: any; count: number }>('/api/language/dictionaries/import', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  search: (q: string, opts?: { language?: string; pos?: string; limit?: number; offset?: number }) =>
    request<{ query: string; count: number; results: DictionaryResult[] }>(
      `/api/language/dictionaries/search?q=${encodeURIComponent(q)}${opts?.language ? `&language=${encodeURIComponent(opts.language)}` : ''}${opts?.pos ? `&pos=${encodeURIComponent(opts.pos)}` : ''}${opts?.limit ? `&limit=${opts.limit}` : ''}${opts?.offset ? `&offset=${opts.offset}` : ''}`,
    ),

  lookup: (lemma: string, language = '') =>
    request<{ lemma: string; count: number; results: DictionaryResult[] }>(
      `/api/language/dictionaries/lookup/${encodeURIComponent(lemma)}${language ? `?language=${encodeURIComponent(language)}` : ''}`,
    ),
};

/** LanguageOS Dictionary Kernel */
export const languageOsApi = {
  importDictionaryText: (data: { profile_id?: string; title: string; dictionary_type: string; text: string }) =>
    request<{ duplicate: boolean; dictionary: any; asset_count: number; lexical_assets: any[] }>('/api/language-os/dictionaries/import-text', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  importDictionaryJson: (data: { profile_id?: string; title: string; dictionary_type: string; entries: any[] | string }) =>
    request<{ duplicate: boolean; dictionary: any; asset_count: number; lexical_assets: any[] }>('/api/language-os/dictionaries/import-json', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  importDictionaryCsv: (data: { profile_id?: string; title: string; dictionary_type: string; csv_text: string }) =>
    request<{ duplicate: boolean; dictionary: any; asset_count: number; lexical_assets: any[] }>('/api/language-os/dictionaries/import-csv', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  importDictionaryFile: (data: { file: File; profile_id?: string; title?: string; dictionary_type?: string; force_reimport?: boolean }) => {
    const form = new FormData();
    form.append('file', data.file);
    if (data.profile_id) form.append('profile_id', data.profile_id);
    if (data.title) form.append('title', data.title);
    if (data.dictionary_type) form.append('dictionary_type', data.dictionary_type);
    if (data.force_reimport) form.append('force_reimport', String(data.force_reimport));
    return request<{ duplicate: boolean; file: any; warnings: string[]; dictionary: any; asset_count: number; lexical_assets: any[] }>(
      '/api/language-os/dictionaries/import-file',
      { method: 'POST', body: form },
    );
  },

  listDictionaries: (profileId = 'default') =>
    request<{ count: number; dictionaries: any[] }>(`/api/language-os/dictionaries?profile_id=${encodeURIComponent(profileId)}`),

  getDictionary: (dictionaryId: string) =>
    request<{ dictionary: any; asset_count: number; lexical_assets: any[] }>(`/api/language-os/dictionaries/${dictionaryId}`),

  scoreDictionary: (dictionaryId: string) =>
    request<{ dictionary: any; quality_gate: any }>(`/api/language-os/dictionaries/${dictionaryId}/score`, { method: 'POST' }),

  confirmDictionary: (dictionaryId: string) =>
    request<{ dictionary: any; quality_gate: any }>(`/api/language-os/dictionaries/${dictionaryId}/confirm`, { method: 'POST' }),

  rejectDictionary: (dictionaryId: string) =>
    request<{ dictionary: any; rejected_assets: any[] }>(`/api/language-os/dictionaries/${dictionaryId}/reject`, { method: 'POST' }),

  listLexicalAssets: (opts?: { profile_id?: string; dictionary_id?: string; validation_status?: string }) => {
    const params = new URLSearchParams();
    if (opts?.profile_id) params.set('profile_id', opts.profile_id);
    if (opts?.dictionary_id) params.set('dictionary_id', opts.dictionary_id);
    if (opts?.validation_status) params.set('validation_status', opts.validation_status);
    return request<{ count: number; assets: any[] }>(`/api/language-os/lexical-assets${params.size ? `?${params.toString()}` : ''}`);
  },

  confirmLexicalAsset: (lexicalId: string) =>
    request<{ asset: any }>(`/api/language-os/lexical-assets/${lexicalId}/confirm`, { method: 'POST' }),

  rejectLexicalAsset: (lexicalId: string) =>
    request<{ asset: any }>(`/api/language-os/lexical-assets/${lexicalId}/reject`, { method: 'POST' }),

  generateReviewSession: (data: { profile_id?: string; max_units?: number }) =>
    request<any>('/api/language-os/review/generate-session', { method: 'POST', body: JSON.stringify(data) }),

  getReviewSession: (sessionId: string) =>
    request<any>(`/api/language-os/review/sessions/${sessionId}`),

  completeReviewUnit: (unitId: string, data: { session_id?: string; outcome: 'recalled' | 'partial' | 'forgot' | 'skipped'; time_spent_seconds?: number }) =>
    request<{ session: any; unit_id: string; memory_update: any }>(`/api/language-os/review/units/${unitId}/complete`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

/** ResourceOS */
export interface ResourceProvider {
  provider_id: string;
  label: string;
  modes: string[];
  configured: boolean;
  health: string;
  default_license_mode: string;
}

export interface ResourceSubscription {
  subscription_id: string;
  lane: 'language' | 'cfa';
  provider: string;
  target: string;
  schedule: string;
  budget: number;
  enabled: boolean;
}

export interface ResourceDocument {
  document_id: string;
  lane: 'language' | 'cfa';
  provider: string;
  url: string;
  title: string;
  license_mode: string;
  excerpt: string;
  retrieved_at: string;
  answer_bearing: boolean;
}

export interface ResourceInboxItem {
  inbox_id: string;
  document_id: string;
  lane: 'language' | 'cfa';
  reason: string;
  status: string;
  source_url?: string;
  title?: string;
}

export interface ResourceAuditFinding {
  finding_id: string;
  check_id: string;
  severity: string;
  remediation: string;
}

export interface ResourceJob {
  job_id: string;
  trigger: string;
  status: string;
  budget_usage: number;
  retry_state: { reason?: string };
  audit_summary: { finding_count?: number };
  created_at: string;
}

export interface ResourceQualityDimension {
  dimension: string;
  score: number;
  weight: number;
  reasons: string[];
}

export interface ResourceQualityScore {
  document_id: string;
  lane: 'language' | 'cfa' | string;
  overall_score: number;
  normalized_score: number;
  recommendation: 'promote' | 'review' | 'reject' | string;
  pass_gate: boolean;
  dimensions: ResourceQualityDimension[];
  strengths: string[];
  concerns: string[];
  summary: string;
}

export interface ResourceCandidate {
  candidate_id: string;
  document_id: string;
  lane: 'language' | 'cfa' | string;
  provider: string;
  url: string;
  title: string;
  status: 'pending' | 'approved' | 'rejected' | string;
  score: ResourceQualityScore;
  evidence_refs: string[];
  created_at: string;
  updated_at: string;
  review_note?: string;
  reviewed_at?: string;
  promotion?: Record<string, unknown>;
  document_snapshot: Record<string, unknown>;
}

export interface ResourceSettings {
  robots_cache_hours: number;
  per_domain_concurrency: number;
  subscription_resource_limit: number;
  max_html_bytes: number;
  max_redirects: number;
  ai_discovery_requires_consent: boolean;
  consent: { openai_web_search: boolean };
  features: Record<string, boolean>;
}

export const resourcesApi = {
  providers: () => request<{ providers: ResourceProvider[] }>('/api/resources/providers'),
  subscriptions: () => request<{ subscriptions: ResourceSubscription[] }>('/api/resources/subscriptions'),
  createSubscription: (data: { lane: 'language' | 'cfa'; provider: string; target: string; budget?: number }) =>
    request<ResourceSubscription>('/api/resources/subscriptions', { method: 'POST', body: JSON.stringify(data) }),
  updateSubscription: (subscriptionId: string, data: { enabled?: boolean; budget?: number; schedule?: string }) =>
    request<ResourceSubscription>(`/api/resources/subscriptions/${subscriptionId}`, { method: 'PATCH', body: JSON.stringify(data) }),
  documents: () => request<{ documents: ResourceDocument[] }>('/api/resources/documents'),
  jobs: () => request<{ jobs: ResourceJob[] }>('/api/resources/jobs'),
  crawl: (data: { lane: 'language' | 'cfa'; url: string; provider?: string; license_mode?: string }) =>
    request('/api/resources/jobs/crawl', { method: 'POST', body: JSON.stringify(data) }),
  runDue: () => request('/api/resources/jobs/run-due', { method: 'POST' }),
  search: (query: string, lane = '') =>
    request<{ count: number; results: { document_id: string; title: string; excerpt: string; topic: string }[] }>(
      `/api/resources/search?q=${encodeURIComponent(query)}${lane ? `&lane=${encodeURIComponent(lane)}` : ''}`,
  ),
  inbox: () => request<{ items: ResourceInboxItem[] }>('/api/resources/inbox'),
  resolveInbox: (inboxId: string, action: 'approve' | 'reject') =>
    request(`/api/resources/inbox/${inboxId}/resolve`, { method: 'POST', body: JSON.stringify({ action }) }),
  audits: () => request<{ findings: ResourceAuditFinding[] }>('/api/resources/audits'),
  runAudit: (scope: 'content' | 'runtime' | 'code') =>
    request('/api/resources/audits/run', { method: 'POST', body: JSON.stringify({ scope }) }),
  scheduler: () => request<{ task_name: string; installed: boolean; status: string }>('/api/resources/scheduler/status'),
  settings: () => request<ResourceSettings>('/api/resources/settings'),
  setAiDiscoveryConsent: (granted: boolean) =>
    request('/api/privacy/consent', {
      method: 'POST',
      body: JSON.stringify({ provider: 'openai', purpose: 'resource_ai_discovery', granted }),
    }),
};

export const resourceCandidatesApi = {
  list: (opts?: { status?: string; lane?: string }) => {
    const params = new URLSearchParams();
    if (opts?.status) params.set('status', opts.status);
    if (opts?.lane) params.set('lane', opts.lane);
    return request<{ candidates: ResourceCandidate[] }>(`/api/resources/candidates${params.size ? `?${params.toString()}` : ''}`);
  },
  enqueue: (documentId: string) =>
    request<ResourceCandidate>('/api/resources/candidates/enqueue', {
      method: 'POST',
      body: JSON.stringify({ document_id: documentId }),
    }),
  rescore: (candidateId: string) =>
    request<ResourceCandidate>(`/api/resources/candidates/${candidateId}/rescore`, { method: 'POST' }),
  approve: (candidateId: string, reviewNote = '') =>
    request<{ candidate: ResourceCandidate; promotion: Record<string, unknown> }>(
      `/api/resources/candidates/${candidateId}/approve`,
      { method: 'POST', body: JSON.stringify({ review_note: reviewNote }) },
    ),
  reject: (candidateId: string, reviewNote = '') =>
    request<{ candidate: ResourceCandidate; promotion: Record<string, unknown> }>(
      `/api/resources/candidates/${candidateId}/reject`,
      { method: 'POST', body: JSON.stringify({ review_note: reviewNote }) },
    ),
};

export type GoalType = 'exam' | 'language' | 'course' | 'career' | 'project' | 'custom';
export type GoalEnergyMode = 'low' | 'normal' | 'high';

export interface CoursePack {
  pack_id: string;
  title: string;
  pack_type: 'exam' | 'language' | 'course' | 'custom';
  description: string;
  default_modules: string[];
  suggested_imports: Array<{ import_type: string; label: string; required?: boolean }>;
  syllabus_seed: Array<Record<string, any>>;
  formula_families: string[];
  lexical_config: Record<string, any>;
  planner_defaults: Record<string, any>;
  assessment_defaults: Record<string, any>;
  quality_gate_policy: Record<string, any>;
}

export interface GoalProfile {
  goal_id: string;
  profile_id: string;
  title: string;
  goal_type: GoalType;
  target_exam: string | null;
  target_language: string | null;
  source_language: string | null;
  target_date: string | null;
  weekly_minutes: number;
  default_energy_mode: GoalEnergyMode;
  enabled_modules: string[];
  preferred_review_modes: string[];
  created_at: string;
  updated_at: string;
  status: 'draft' | 'active' | 'archived';
  onboarding_status: Record<string, any>;
  pack_id: string | null;
}

export interface OnboardingState {
  profile_id: string;
  active_goal_id: string | null;
  completed_steps: string[];
  skipped_steps: string[];
  current_step: string;
  readiness_score: number;
  readiness_status: string;
  blockers: Array<{ blocker_id: string; severity: string; message: string; launch_route: string }>;
  recommended_next_action: { action_id: string; title: string; launch_route: string } | null;
  updated_at: string;
}

export interface ReadinessPayload extends OnboardingState {
  components: Record<string, { weight: number; earned: boolean; contribution: number }>;
  signals: Record<string, any>;
}

export interface Day1Plan {
  plan_id: string;
  profile_id: string;
  generated_at: string;
  goal: GoalProfile | null;
  blocks: Array<{ block_id: string; block_type: string; title: string; description: string; target_minutes: number; launch_route: string; due_reason: string }>;
  readiness: ReadinessPayload;
  study_planner_seed: Record<string, any> | null;
  safety: Record<string, any>;
}

export const goalsApi = {
  packs: () => request<{ count: number; packs: CoursePack[] }>('/api/goals/packs'),
  create: (data: Partial<GoalProfile> & { pack_id?: string | null }) =>
    request<{ goal: GoalProfile; course_pack: CoursePack; onboarding: OnboardingState }>('/api/goals', { method: 'POST', body: JSON.stringify(data) }),
  list: (opts?: { profile_id?: string; include_archived?: boolean }) =>
    request<{ count: number; goals: GoalProfile[]; active_goal: GoalProfile | null }>(
      `/api/goals?${graphQuery({ profile_id: opts?.profile_id || '', include_archived: opts?.include_archived ? 'true' : '' })}`,
    ),
  get: (goalId: string) => request<{ goal: GoalProfile; course_pack: CoursePack | null }>(`/api/goals/${encodeURIComponent(goalId)}`),
  activate: (goalId: string) =>
    request<{ goal: GoalProfile; onboarding: OnboardingState }>(`/api/goals/${encodeURIComponent(goalId)}/activate`, { method: 'POST' }),
  archive: (goalId: string) =>
    request<{ goal: GoalProfile; onboarding: OnboardingState }>(`/api/goals/${encodeURIComponent(goalId)}/archive`, { method: 'POST' }),
  patch: (goalId: string, data: Partial<GoalProfile>) =>
    request<{ goal: GoalProfile; onboarding: OnboardingState }>(`/api/goals/${encodeURIComponent(goalId)}`, { method: 'PATCH', body: JSON.stringify(data) }),
};

export const onboardingApi = {
  state: (profileId = '') =>
    request<OnboardingState>(`/api/onboarding/state${profileId ? `?profile_id=${encodeURIComponent(profileId)}` : ''}`),
  readiness: (profileId = '') =>
    request<ReadinessPayload>(`/api/onboarding/readiness${profileId ? `?profile_id=${encodeURIComponent(profileId)}` : ''}`),
  completeStep: (data: { profile_id?: string; step_id: string }) =>
    request<OnboardingState>('/api/onboarding/step', { method: 'POST', body: JSON.stringify(data) }),
  skipStep: (data: { profile_id?: string; step_id: string }) =>
    request<OnboardingState>('/api/onboarding/skip-step', { method: 'POST', body: JSON.stringify(data) }),
  generateDay1Plan: (data: { profile_id?: string; goal_id?: string }) =>
    request<Day1Plan>('/api/onboarding/generate-day1-plan', { method: 'POST', body: JSON.stringify(data) }),
  reset: (profileId = '') =>
    request<OnboardingState>('/api/onboarding/reset', { method: 'POST', body: JSON.stringify({ profile_id: profileId }) }),
};

export interface DataInventoryItem {
  category: string;
  path: string | null;
  record_count: number;
  size_bytes: number;
  last_modified_at: string | null;
  contains_raw_diagnostics: boolean;
  contains_source_files: boolean;
  exportable: boolean;
  resettable: boolean;
  notes?: string | null;
}

export interface BackupSnapshot {
  snapshot_id: string;
  profile_id: string;
  created_at: string;
  label?: string | null;
  mode: 'safe' | 'full' | 'category' | string;
  categories: string[];
  file_path: string;
  size_bytes: number;
  content_hash: string;
  manifest: Record<string, any>;
  redaction_policy: Record<string, any>;
  app_version?: string | null;
  schema_version: string;
}

export const dataGovernanceApi = {
  inventory: () => request<{ items: DataInventoryItem[]; summary: Record<string, any> }>('/api/data-governance/inventory'),
  snapshots: () => request<{ snapshots: BackupSnapshot[] }>('/api/data-governance/snapshots'),
  exportBackup: (data: { mode: 'safe' | 'full' | 'category'; categories?: string[]; include_raw_diagnostics?: boolean; label?: string }) =>
    request<{ snapshot: BackupSnapshot; redaction_report: Record<string, any>; warning: Record<string, any> }>(
      '/api/data-governance/export',
      { method: 'POST', body: JSON.stringify(data) },
    ),
  restoreDryRun: (data: { file_path: string; categories?: string[]; mode?: string }) =>
    request<Record<string, any>>('/api/data-governance/restore/dry-run', { method: 'POST', body: JSON.stringify(data) }),
  restore: (data: { file_path: string; categories?: string[]; mode?: 'merge' | 'replace_category' | 'full_replace' }) =>
    request<Record<string, any>>('/api/data-governance/restore', { method: 'POST', body: JSON.stringify(data) }),
  rollback: (snapshotId: string, data: { categories?: string[] }) =>
    request<Record<string, any>>(`/api/data-governance/rollback/${snapshotId}`, { method: 'POST', body: JSON.stringify(data) }),
  reset: (data: { category: string; confirmation: string }) =>
    request<Record<string, any>>('/api/data-governance/reset', { method: 'POST', body: JSON.stringify(data) }),
  privacyReport: () => request<Record<string, any>>('/api/data-governance/privacy-report'),
};

export interface InteropArtifact {
  artifact_id: string;
  profile_id: string;
  artifact_type: 'anki_csv' | 'anki_tsv' | 'markdown_zip' | 'ics' | 'xapi_json' | 'import_preview';
  created_at: string;
  file_path: string;
  size_bytes: number;
  content_hash: string;
  categories: string[];
  source_filters: Record<string, any>;
  safe_mode: boolean;
  redaction_report: Record<string, any>;
}

export interface InteropImportPreview {
  preview_id: string;
  artifact_type: string;
  filename: string;
  detected_items: number;
  duplicates: number;
  warnings: Array<Record<string, any>>;
  proposed_records: Array<Record<string, any>>;
  will_auto_confirm: boolean;
  created_at?: string;
}

export const interopApi = {
  artifacts: () => request<{ count: number; artifacts: InteropArtifact[] }>('/api/interop/artifacts'),
  artifact: (artifactId: string) => request<InteropArtifact>(`/api/interop/artifacts/${encodeURIComponent(artifactId)}`),
  exportAnki: (data: Record<string, any>) =>
    request<{ artifact: InteropArtifact; item_count: number; sample_rows: Array<Record<string, any>>; redaction_report: Record<string, any> }>(
      '/api/interop/export/anki',
      { method: 'POST', body: JSON.stringify(data) },
    ),
  previewAnki: (data: Record<string, any>) =>
    request<InteropImportPreview>('/api/interop/import/anki/preview', { method: 'POST', body: JSON.stringify(data) }),
  commitAnki: (data: Record<string, any>) =>
    request<Record<string, any>>('/api/interop/import/anki/commit', { method: 'POST', body: JSON.stringify(data) }),
  exportMarkdown: (data: Record<string, any>) =>
    request<{ artifact: InteropArtifact; item_count: number; sample_notes: string[]; redaction_report: Record<string, any> }>(
      '/api/interop/export/markdown',
      { method: 'POST', body: JSON.stringify(data) },
    ),
  previewMarkdown: (data: Record<string, any>) =>
    request<InteropImportPreview>('/api/interop/import/markdown/preview', { method: 'POST', body: JSON.stringify(data) }),
  commitMarkdown: (data: Record<string, any>) =>
    request<Record<string, any>>('/api/interop/import/markdown/commit', { method: 'POST', body: JSON.stringify(data) }),
  exportCalendar: (data: Record<string, any>) =>
    request<{ artifact: InteropArtifact; event_count: number; sample_events: Array<Record<string, any>> }>(
      '/api/interop/export/calendar',
      { method: 'POST', body: JSON.stringify(data) },
    ),
  exportLearningRecords: (data: Record<string, any>) =>
    request<{ artifact: InteropArtifact; statement_count: number; sample_statements: Array<Record<string, any>>; redaction_report: Record<string, any> }>(
      '/api/interop/export/learning-records',
      { method: 'POST', body: JSON.stringify(data) },
    ),
  privacyReport: () => request<Record<string, any>>('/api/interop/privacy-report'),
};

export interface NavigationSurface {
  surface_id: string;
  label: string;
  route: string;
  tier: 'primary' | 'secondary' | 'advanced' | 'hidden';
  audience_label: 'learner' | 'power_user' | 'system';
  frequency: 'daily' | 'weekly' | 'occasional' | 'rare';
  product_role: 'learn' | 'plan' | 'reflect' | 'library' | 'tools' | 'settings' | 'system';
  visible_on_main: boolean;
  more_group: string | null;
  reason: string;
}

export interface CockpitSummary {
  profile_id: string;
  generated_at: string;
  active_goal: Record<string, any> | null;
  primary_action: { label: string; href: string; reason: string };
  supporting_actions: Array<{ label: string; href: string; role: string }>;
  today_plan_preview: Array<Record<string, any>>;
  learning_health: Record<string, any>;
}

export const navigationApi = {
  summary: () => request<{ generated_at: string; surfaces: NavigationSurface[]; main_visible_count: number; primary_count: number }>('/api/navigation/summary'),
  tools: () => request<{ generated_at: string; groups: Array<{ group_id: string; label: string; items: NavigationSurface[] }> }>('/api/navigation/tools'),
  cockpit: (profileId = 'default') =>
    request<CockpitSummary>(`/api/navigation/cockpit?profile_id=${encodeURIComponent(profileId)}`),
};
