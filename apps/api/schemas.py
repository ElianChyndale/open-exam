"""Pydantic request/response schemas for ExamOS API."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


# ── Attempts ─────────────────────────────────────────────────────────────────

class QuestionAttemptRequest(BaseModel):
    """Record a question attempt."""
    topic: str = Field(..., description="Subject area, e.g. 'Fixed Income'")
    los: str = Field(..., description="Learning Outcome Statement code")
    prompt_or_question: str = Field(..., description="Question text")
    wrong_choice_or_output: str = Field("", description="User's wrong answer")
    correct_resolution: str = Field(..., description="Correct answer/explanation")
    error_type: str = Field("concept_confusion", description="Error category")
    confidence: int = Field(1, ge=0, le=4, description="Confidence 0-4")
    time_spent: int = Field(0, description="Time spent in seconds")
    evidence_refs: list[str] = Field(default_factory=list)
    question_source: str = Field("", description="e.g. 'official_mock'")
    source_type: str = Field("", description="e.g. 'screenshot', 'manual'")
    evidence_assets: list[str] = Field(default_factory=list)
    moc_target: str = Field("", description="MOC file path")
    question_format: str = Field("", description="'multiple_choice' or 'constructed_response'")
    choices: list[str] = Field(default_factory=list)
    is_correct: bool = Field(False, description="Correct attempts are stored without creating mistake cards")


class ScreenshotUploadRequest(BaseModel):
    """Upload a screenshot for structured extraction."""
    topic: str = Field(...)
    los: str = Field(default="")
    image_data: str = Field(..., description="Base64-encoded image")
    filename: str = Field("screenshot.png")


class AttemptResponse(BaseModel):
    """Response after recording an attempt."""
    attempt_id: str
    event_id: str
    card_id: str
    error_type: str
    fix_rule: str
    next_drill: str
    review_due_at: str


# ── Diagnosis ────────────────────────────────────────────────────────────────

class DiagnosisRequest(BaseModel):
    """Request error diagnosis for an attempt."""
    attempt_id: str
    error_type: str = ""
    user_notes: str = ""


class DiagnosisResponse(BaseModel):
    """Structured error diagnosis."""
    diagnosis_id: str
    attempt_id: str
    error_category: str
    error_summary: str
    fix_rule: str
    next_drill: str
    linked_los: list[str]
    linked_moc_node: str
    review_due_at: str
    pattern_candidate: bool
    pattern_key: str
    spacing_interval_days: int


# ── Review Pack ──────────────────────────────────────────────────────────────

class ReviewPackRequest(BaseModel):
    """Request a daily review pack."""
    date: str = Field(default="", description="YYYY-MM-DD, defaults to today")
    days_back: int = Field(7, ge=1, le=90)
    max_items: int = Field(20, ge=1, le=100)
    focus_topic: str = Field("")
    knowledge_depth: str = Field("standard", pattern="^(standard|expanded)$")


class ReviewPackResponse(BaseModel):
    """Daily review pack output."""
    generated_for: str
    focus_topic: str
    review_item_count: int
    warm_start_item_count: int
    source_event_count: int
    markdown_content: str
    items: list[dict] = Field(default_factory=list)


# ── Energy ───────────────────────────────────────────────────────────────────

class EnergyCheckInRequest(BaseModel):
    """Record an energy check-in."""
    energy_level: int = Field(2, ge=0, le=4)
    mental_clarity: int = Field(5, ge=1, le=10)
    physical_fatigue: int = Field(5, ge=1, le=10)
    motivation: int = Field(5, ge=1, le=10)
    notes: str = Field("")
    session_id: str = Field("")


class EnergyCheckInResponse(BaseModel):
    """Energy check-in result."""
    check_in_id: str
    energy_level: int
    recommended_task_order: list[str]
    warnings: list[str]


# ── Study Plan ───────────────────────────────────────────────────────────────

class StudyPlanRequest(BaseModel):
    """Request today's study plan."""
    date: str = Field(default="")
    energy_level: int = Field(2, ge=0, le=4)
    available_minutes: int = Field(120, ge=10)
    focus_topic: str = Field("")


class StudyPlanResponse(BaseModel):
    """Today's study plan."""
    plan_id: str
    date: str
    energy_level: int
    available_minutes: int
    focus_topic: str
    focus_reason: str
    high_energy_tasks: list[dict]
    moderate_energy_tasks: list[dict]
    low_energy_tasks: list[dict]
    danger_los_list: list[str]
    warnings: list[str]


# ── Mock ─────────────────────────────────────────────────────────────────────

class MockSessionCreate(BaseModel):
    """Create a mock exam session."""
    session_id: str = Field(...)
    exam_name: str = Field("CFA Level I")
    session_label: str = Field("Mock 1")
    scheduled_date: str = Field("")
    total_minutes: int = Field(180)
    total_questions: int = Field(0)
    correct_count: int = Field(0)


class MockRetroRequest(BaseModel):
    """Request post-mock retro."""
    session_id: str = Field(...)


class MockRetroResponse(BaseModel):
    """Post-mock retro result."""
    session_id: str
    question_count: int
    bias_count: int
    agent_count: int
    markdown_content: str
    stop_doing: list[str]
    next_strategy: str


# ── Dashboard ────────────────────────────────────────────────────────────────

class EffectivenessResponse(BaseModel):
    """Learning effectiveness dashboard."""
    report_id: str
    period_start: str
    period_end: str
    due_review_completion_rate: float
    high_confidence_error_count: int
    interleaving_accuracy: float
    same_error_recurrence_rate: float
    los_risk_heatmap: dict[str, float]
    danger_top_3: list[str]
    predicted_pass_probability: float
    confidence_band_low: float
    confidence_band_high: float
    calibration_trend: str
    error_count_trend: list[int]


# ── Institution ──────────────────────────────────────────────────────────────

class CohortCreate(BaseModel):
    """Create an institution cohort."""
    institution_id: str = Field(...)
    cohort_name: str = Field(...)
    exam_target: str = Field("CFA Level I")
    exam_date: str = Field("")
    learner_ids: list[str] = Field(default_factory=list)


class CohortRiskResponse(BaseModel):
    """Institutional risk report."""
    report_id: str
    cohort_id: str
    cohort_name: str
    total_learners: int
    at_risk_count: int
    dropout_warning_count: int
    avg_review_completion: float
    avg_accuracy: float
    at_risk_learners: list[dict]
    dropout_warnings: list[dict]
    instructor_recommendations: list[str]
    generated_at: str


# ── Daily Learner Loop ───────────────────────────────────────────────────────

class ProfileUpdate(BaseModel):
    """Persisted learner setup and settings."""
    exam_date: str = Field(default="")
    current_phase: str = Field(default="foundation")
    target_score_percentile: int = Field(default=70, ge=1, le=100)
    daily_minutes_available: int = Field(default=120, ge=10)
    weekly_study_days: int = Field(default=6, ge=1, le=7)
    preferred_session_minutes: int = Field(default=50, ge=10)
    peak_energy_window: str = Field(default="09:00-12:00")
    moderate_energy_window: str = Field(default="14:00-18:00")
    low_energy_window: str = Field(default="20:00-22:00")


class TaskStatusUpdate(BaseModel):
    """Allowed learner task transitions."""
    status: str = Field(pattern="^(pending|completed|skipped|deferred)$")


class ReviewSessionCreate(BaseModel):
    """Start an active-recall review session."""
    max_items: int = Field(default=10, ge=1, le=50)


class ReviewResponseSubmit(BaseModel):
    """Record the learner's self-rated retrieval result."""
    prompt_id: str
    score: int = Field(ge=0, le=4)
    self_explanation: str = Field(default="")


# ── Practice And Private Question Banks ──────────────────────────────────────

class ImportedQuestion(BaseModel):
    """Normalized private import record. Missing fields stay quarantined."""
    source_file: str = Field(default="")
    source_page: int = Field(default=0, ge=0)
    prompt: str = Field(default="")
    choices: list[str] = Field(default_factory=list)
    correct_answer: str = Field(default="")
    explanation: str = Field(default="")
    topic: str = Field(default="")
    module: str = Field(default="")
    los: str = Field(default="")
    error_type: str = Field(default="concept_confusion")


class QuestionBankImport(BaseModel):
    source_name: str
    questions: list[ImportedQuestion]


class QuestionReview(BaseModel):
    action: str = Field(pattern="^(approve|reject)$")
    corrections: dict[str, Any] = Field(default_factory=dict)


class PracticeSessionCreate(BaseModel):
    max_items: int = Field(default=10, ge=1, le=100)
    topic: str = Field(default="")


class PracticeAnswer(BaseModel):
    question_id: str
    answer: str
    confidence: int = Field(default=1, ge=0, le=4)
    elapsed_seconds: int = Field(default=0, ge=0)
    self_explanation: str = Field(default="")


# ── Mock Runs, Coach, And Knowledge Graph ───────────────────────────────────

class MockRunCreate(BaseModel):
    session_label: str = Field(default="Mock run")
    total_minutes: int = Field(default=135, ge=1)
    total_questions: int = Field(default=90, ge=1)


class MockRunStateUpdate(BaseModel):
    action: str = Field(pattern="^(pause|resume|complete)$")
    elapsed_seconds: int = Field(default=0, ge=0)


class MockRunAnswer(BaseModel):
    question_id: str
    prompt: str = Field(default="")
    answer: str = Field(default="")
    correct_answer: str = Field(default="")
    explanation: str = Field(default="")
    is_correct: bool
    topic: str = Field(default="")
    los: str = Field(default="")
    elapsed_seconds: int = Field(default=0, ge=0)
    confidence: int = Field(default=1, ge=0, le=4)


class ExternalMockImport(BaseModel):
    source_name: str
    session_label: str = Field(default="External mock")
    total_questions: int = Field(default=0, ge=0)
    answers: list[MockRunAnswer]


class CoachRetroRequest(BaseModel):
    summary: str
    source_refs: list[str] = Field(min_length=1)
    biases: list[str] = Field(default_factory=list)


class CoachAgentAuditRequest(BaseModel):
    summary: str
    source_refs: list[str] = Field(min_length=1)
    risk_kind: str = Field(default="unsupported_claim")


class GraphNode(BaseModel):
    id: str
    label: str
    source_kind: str = Field(pattern="^(official|evidence|personal)$")
    node_type: str
    x: float = 0
    y: float = 0
    notes: str = Field(default="")
    color: str = Field(default="")
    locked: bool = False


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    source_kind: str = Field(pattern="^(official|evidence|personal)$")
    label: str = Field(default="")
    locked: bool = False


class GraphOverlayUpdate(BaseModel):
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)


# ── Explicit Transfer And Institution Delivery ──────────────────────────────

class TransferImportRequest(BaseModel):
    bundle: dict[str, Any] = Field(default_factory=dict)
    dry_run: bool = True
    direction: str = Field(default="cloud-to-local", pattern="^(cloud-to-local|local-to-cloud)$")
    organization_id: str = Field(default="")


class InterventionCreate(BaseModel):
    learner_id: str
    reason: str
    owner_id: str = Field(default="")
