"""Pydantic request/response schemas for OpenExam API."""

from __future__ import annotations

from typing import Any
from typing import Literal

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
    review_id: str = ""
    generated_for: str
    focus_topic: str
    review_item_count: int
    warm_start_item_count: int
    source_event_count: int
    markdown_content: str
    items: list[dict] = Field(default_factory=list)


class DailyReviewCompleteResponse(BaseModel):
    """Idempotent Daily Review completion result."""
    review_id: str
    completed: bool
    newly_reviewed_items: int
    knowledge_decisions: list[dict] = Field(default_factory=list, description="KnowledgeMemoryEngine state updates per knowledge point")


class CardReviewRequest(BaseModel):
    """Explicit recall outcome for one mistake card."""
    outcome: Literal["recalled", "struggled", "forgot"]
    confidence_after: int = Field(0, ge=0, le=4)


class FixRuleFeedbackRequest(BaseModel):
    """Learner vote on whether a correction rule changed the next decision."""
    helpful: bool
    note: str = ""


# ── Energy ───────────────────────────────────────────────────────────────────

class EnergyCheckInRequest(BaseModel):
    """Record an energy check-in."""
    energy_level: int = Field(2, ge=0, le=4)
    mental_clarity: int = Field(5, ge=1, le=10)
    physical_fatigue: int = Field(5, ge=1, le=10)
    motivation: int = Field(5, ge=1, le=10)
    sleep_hours: float = Field(0.0, ge=0, le=24, description="Hours of sleep last night (0 = not reported)")
    stress_level: int = Field(0, ge=0, le=10, description="0 = not reported, 1-10 stress level")
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
    interleaving_composition: dict[str, int] = Field(default_factory=dict)


# ── Todo ─────────────────────────────────────────────────────────────────────

class TodoTaskCreate(BaseModel):
    text: str = Field(..., min_length=1)
    deadline: str = ""
    progress: int = Field(0, ge=0, le=100)
    expected_revision: int = Field(..., ge=0)
    date: str = ""


class TodoTaskUpdate(BaseModel):
    text: str | None = None
    deadline: str | None = None
    progress: int | None = Field(default=None, ge=0, le=100)
    status: Literal["pending", "completed"] | None = None
    expected_revision: int = Field(..., ge=0)


class TodoRevisionRequest(BaseModel):
    expected_revision: int = Field(..., ge=0)


class TodoReplaceRequest(BaseModel):
    date: str = ""
    title: str = ""
    focus: str = ""
    tasks: list[Any] = Field(default_factory=list)
    time_blocks: list[str] = Field(default_factory=list)


class TodoStudyPlanImportRequest(BaseModel):
    confirmed: bool = False
    plan: dict[str, Any]


# ── Privacy And Provenance ───────────────────────────────────────────────────

class ProvenanceRecordRequest(BaseModel):
    entity_id: str = Field(..., min_length=1)
    activity_type: str = Field(..., min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    agent_id: str = "local-openexam"
    attributes: dict[str, Any] = Field(default_factory=dict)


class ConsentRecordRequest(BaseModel):
    provider: str = Field(..., min_length=1)
    purpose: str = Field(..., min_length=1)
    granted: bool


class PrivacyPurgeRequest(BaseModel):
    confirmation_token: str = ""


# ── Mock ─────────────────────────────────────────────────────────────────────

class MockSessionCreate(BaseModel):
    """Create a mock exam session."""
    session_id: str = Field(...)
    exam_name: str = Field("")
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
    exam_target: str = Field("")
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
