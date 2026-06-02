"""Complete exam domain models.

All core types from PLAN.md plus supporting enums and helpers.
Designed to be exam-agnostic — CFA specifics live in the adapter layer.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, IntEnum
from hashlib import sha1
from typing import Any


# ── Helpers ──────────────────────────────────────────────────────────────────

def utc_now() -> datetime:
    return datetime.now(UTC)


def stable_id(prefix: str, *parts: str) -> str:
    raw = "||".join(parts).encode("utf-8")
    return f"{prefix}-{sha1(raw, usedforsecurity=False).hexdigest()[:12]}"


def new_uuid() -> str:
    return uuid.uuid4().hex[:12]


# ── Enums ────────────────────────────────────────────────────────────────────


class ConfidenceLevel(IntEnum):
    """User confidence when submitting an answer."""
    GUESS = 0          # 猜的
    UNSURE = 1         # 不确定
    MODERATE = 2       # 较确定
    CONFIDENT = 3      # 确定
    VERY_CONFIDENT = 4 # 非常确定


class EnergyLevel(IntEnum):
    """Self-reported energy/alertness level."""
    DEPLETED = 0       # 精疲力竭
    LOW = 1            # 低精力
    MODERATE = 2       # 中等
    HIGH = 3           # 高精力
    PEAK = 4           # 巅峰


class ErrorCategory(str, Enum):
    """Root-cause error taxonomy."""
    KNOWLEDGE_GAP = "knowledge_gap"
    CONCEPT_CONFUSION = "concept_confusion"
    FORMULA_MISUSE = "formula_misuse"
    CARELESS_READING = "careless_reading"
    TIME_PRESSURE = "time_pressure"
    CONFIDENCE_CALIBRATION_FAILURE = "confidence_calibration_failure"
    FATIGUE_ENERGY_MISMATCH = "fatigue_energy_mismatch"
    AGENT_FAILURE = "agent_failure"


class TaskType(str, Enum):
    """Study task classification for energy-aware planning."""
    NEW_KNOWLEDGE = "new_knowledge"
    DIFFICULT_PRACTICE = "difficult_practice"
    INTERLEAVED_SET = "interleaved_set"
    MOCK_EXAM = "mock_exam"
    MISTAKE_REVIEW = "mistake_review"
    FORMULA_DRILL = "formula_drill"
    WORKED_EXAMPLE_FADING = "worked_example_fading"
    ACTIVE_RECALL = "active_recall"
    CONCEPT_DISCRIMINATION = "concept_discrimination"
    LIGHT_REVIEW = "light_review"


class QuestionFormat(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    CONSTRUCTED_RESPONSE = "constructed_response"
    NUMERIC_ENTRY = "numeric_entry"


class QuestionSource(str, Enum):
    OFFICIAL_MOCK = "official_mock"
    OFFICIAL_QBANK = "official_qbank"
    OFFICIAL_PRACTICE_PACK = "official_practice_pack"
    THIRD_PARTY_MOCK = "third_party_mock"
    THIRD_PARTY_QBANK = "third_party_qbank"
    SCREENSHOT = "screenshot"
    MANUAL_ENTRY = "manual_entry"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ── Exam Configuration ───────────────────────────────────────────────────────


@dataclass(slots=True)
class ExamConfig:
    """Learner profile and exam configuration."""
    exam_name: str
    exam_date: str                          # ISO date
    current_phase: str                      # e.g. "foundation", "review", "mock"
    daily_minutes_available: int = 120
    peak_energy_window: str = "09:00-12:00" # e.g. morning
    moderate_energy_window: str = "14:00-18:00"
    low_energy_window: str = "20:00-22:00"
    target_score_percentile: int = 70
    weekly_study_days: int = 6
    preferred_session_minutes: int = 50


# ── Exam Adapter (abstract) ─────────────────────────────────────────────────


@dataclass(slots=True)
class ExamAdapter:
    """Abstract exam adapter.

    Concrete adapters (CFAAdapter, FRMAdapter, etc.) provide:
    - syllabus tree
    - LOS definitions
    - topic → module mapping
    - formula registry
    - trap registry
    """
    exam_id: str
    exam_name: str
    version: str
    subjects: list[str] = field(default_factory=list)


# ── Syllabus Node ────────────────────────────────────────────────────────────


@dataclass(slots=True)
class SyllabusNode:
    """A node in the exam syllabus tree."""
    node_id: str
    path: str                               # e.g. "CFA.Quant.M01.TVM"
    title: str
    los_code: str                           # e.g. "QM.1.a"
    los_description: str = ""
    parent_path: str = ""
    depth: int = 0
    weight_percent: float = 0.0
    is_exam_core: bool = False
    formula_ids: list[str] = field(default_factory=list)
    trap_ids: list[str] = field(default_factory=list)
    module_number: str = ""                 # e.g. "M01"
    children: list[SyllabusNode] = field(default_factory=list)


# ── Question Attempt ─────────────────────────────────────────────────────────


@dataclass(slots=True)
class QuestionAttempt:
    """A single question attempt — the atomic learning event."""
    attempt_id: str = field(default_factory=lambda: stable_id("qa", new_uuid()))
    # Identity
    topic: str = ""
    los: str = ""
    module_number: str = ""
    syllabus_path: str = ""
    # Question
    prompt: str = ""
    choices: list[str] = field(default_factory=list)
    question_format: QuestionFormat = QuestionFormat.MULTIPLE_CHOICE
    question_source: QuestionSource = QuestionSource.MANUAL_ENTRY
    source_detail: str = ""                 # e.g. "Mock 3, Q18"
    # Response
    user_answer: str = ""
    correct_answer: str = ""
    is_correct: bool = False
    confidence: ConfidenceLevel = ConfidenceLevel.UNSURE
    time_spent_seconds: int = 0
    # Evidence
    evidence_refs: list[str] = field(default_factory=list)
    evidence_assets: list[str] = field(default_factory=list)
    screenshot_path: str = ""
    # Metadata
    created_at: str = field(default_factory=lambda: utc_now().isoformat())
    session_id: str = ""
    energy_at_time: EnergyLevel | None = None


# ── Error Diagnosis ──────────────────────────────────────────────────────────


@dataclass(slots=True)
class ErrorDiagnosis:
    """Structured diagnosis of why a question was answered incorrectly."""
    diagnosis_id: str = field(default_factory=lambda: stable_id("dx", new_uuid()))
    attempt_id: str = ""
    # Root cause
    error_category: ErrorCategory = ErrorCategory.CONCEPT_CONFUSION
    error_subcategory: str = ""             # finer-grained e.g. "NPV_vs_IRR"
    error_summary: str = ""                 # one-line human summary
    # Fix
    fix_rule: str = ""                      # executable correction rule
    next_drill: str = ""                    # next practice instruction
    # Links
    linked_los: list[str] = field(default_factory=list)
    linked_moc_node: str = ""               # path to MOC node
    linked_formula_ids: list[str] = field(default_factory=list)
    linked_trap_ids: list[str] = field(default_factory=list)
    # Scheduling
    review_due_at: str = ""                 # next review date (ISO)
    spacing_interval_days: int = 1
    # Pattern detection
    pattern_candidate: bool = False
    pattern_key: str = ""
    # Agent trace
    agent_audit_trail: str = ""
    created_at: str = field(default_factory=lambda: utc_now().isoformat())


# ── Review Task ──────────────────────────────────────────────────────────────


@dataclass(slots=True)
class ReviewTask:
    """A single review item in the daily review pack."""
    task_id: str = field(default_factory=lambda: stable_id("rt", new_uuid()))
    task_type: TaskType = TaskType.MISTAKE_REVIEW
    # Source
    source_attempt_id: str = ""
    source_card_id: str = ""
    source_pattern_id: str = ""
    # Content
    topic: str = ""
    los: str = ""
    error_category: ErrorCategory | None = None
    prompt_preview: str = ""                # truncated for display
    # Instructions
    retrieval_prompt: str = ""              # what to recall before seeing answer
    fix_rule: str = ""
    next_drill: str = ""
    correct_resolution: str = ""
    # Scheduling
    due_date: str = ""
    priority: int = 50                      # 0-100, higher = more urgent
    reasons: list[str] = field(default_factory=list)
    # Energy fit
    energy_fit: EnergyLevel = EnergyLevel.MODERATE


# ── Energy Check-In ──────────────────────────────────────────────────────────


@dataclass(slots=True)
class EnergyCheckIn:
    """User energy/readiness check-in."""
    check_in_id: str = field(default_factory=lambda: stable_id("en", new_uuid()))
    energy_level: EnergyLevel = EnergyLevel.MODERATE
    mental_clarity: int = 5                 # 1-10
    physical_fatigue: int = 5               # 1-10, higher = more tired
    motivation: int = 5                     # 1-10
    notes: str = ""
    created_at: str = field(default_factory=lambda: utc_now().isoformat())
    session_id: str = ""


# ── Study Plan ───────────────────────────────────────────────────────────────


@dataclass(slots=True)
class StudyPlan:
    """A daily study plan generated by the system."""
    plan_id: str = field(default_factory=lambda: stable_id("sp", new_uuid()))
    date: str = ""
    # Energy budget
    energy_level: EnergyLevel = EnergyLevel.MODERATE
    available_minutes: int = 120
    # Tasks by energy tier
    high_energy_tasks: list[ReviewTask] = field(default_factory=list)
    moderate_energy_tasks: list[ReviewTask] = field(default_factory=list)
    low_energy_tasks: list[ReviewTask] = field(default_factory=list)
    # Meta
    focus_topic: str = ""
    focus_reason: str = ""
    danger_los_list: list[str] = field(default_factory=list)
    expected_completion_pct: float = 0.0
    created_at: str = field(default_factory=lambda: utc_now().isoformat())


# ── Mock Session ─────────────────────────────────────────────────────────────


@dataclass(slots=True)
class MockSession:
    """A full mock exam session."""
    session_id: str = field(default_factory=lambda: stable_id("mock", new_uuid()))
    exam_name: str = ""
    session_label: str = ""                 # e.g. "Mock 1", "Half Mock AM"
    # Timing
    scheduled_date: str = ""
    actual_date: str = ""
    total_minutes_allocated: int = 180
    total_minutes_actual: int = 0
    # Results
    total_questions: int = 0
    correct_count: int = 0
    incorrect_count: int = 0
    score_percent: float = 0.0
    # Sections
    section_results: list[dict] = field(default_factory=list)
    # Pre/Post
    pre_mock_brief: str = ""
    post_mock_retro: str = ""
    stop_doing_list: list[str] = field(default_factory=list)
    next_mock_strategy: str = ""
    # Evidence
    attempt_ids: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: utc_now().isoformat())


# ── Learner Progress Report ─────────────────────────────────────────────────


@dataclass(slots=True)
class LearnerProgressReport:
    """Effectiveness dashboard metrics for a single learner."""
    report_id: str = field(default_factory=lambda: stable_id("lpr", new_uuid()))
    learner_id: str = ""
    period_start: str = ""
    period_end: str = ""
    # Core metrics
    due_review_completion_rate: float = 0.0
    high_confidence_error_count: int = 0
    interleaving_accuracy: float = 0.0
    same_error_recurrence_rate: float = 0.0
    # Trends
    error_count_trend: list[int] = field(default_factory=list)    # daily error counts
    accuracy_trend: list[float] = field(default_factory=list)     # daily accuracy
    review_completion_trend: list[float] = field(default_factory=list)
    # LOS risk
    los_risk_heatmap: dict[str, float] = field(default_factory=dict)  # los_code -> risk score
    danger_top_3: list[str] = field(default_factory=list)            # worst 3 LOS codes
    # Predicted
    predicted_pass_probability: float = 0.0
    confidence_band_low: float = 0.0
    confidence_band_high: float = 0.0
    # Generated
    created_at: str = field(default_factory=lambda: utc_now().isoformat())


# ── Institution Models ───────────────────────────────────────────────────────


@dataclass(slots=True)
class InstitutionCohort:
    """A class/cohort of learners at an institution."""
    cohort_id: str = field(default_factory=lambda: stable_id("cohort", new_uuid()))
    institution_id: str = ""
    cohort_name: str = ""
    exam_target: str = ""
    exam_date: str = ""
    learner_ids: list[str] = field(default_factory=list)
    instructor_ids: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: utc_now().isoformat())


@dataclass(slots=True)
class CohortRiskReport:
    """Institutional risk report for a cohort."""
    report_id: str = field(default_factory=lambda: stable_id("crr", new_uuid()))
    cohort_id: str = ""
    cohort_name: str = ""
    generated_at: str = field(default_factory=lambda: utc_now().isoformat())
    # Rankings
    at_risk_learners: list[dict] = field(default_factory=list)      # top N at risk
    dropout_warnings: list[dict] = field(default_factory=list)      # inactivity flags
    # Aggregates
    avg_review_completion: float = 0.0
    avg_accuracy: float = 0.0
    avg_high_confidence_errors: float = 0.0
    # Interventions
    instructor_recommendations: list[str] = field(default_factory=list)
    # Delivery proof
    delivery_proof_metrics: dict[str, Any] = field(default_factory=dict)


# ── Pattern Insight (from existing system, extended) ─────────────────────────


@dataclass(slots=True)
class PatternInsight:
    """A detected error pattern across multiple attempts."""
    pattern_id: str = field(default_factory=lambda: stable_id("ptrn", new_uuid()))
    pattern_key: str = ""                   # "topic::los::error_category"
    recurrence: int = 0
    severity: Severity = Severity.MEDIUM
    affected_topics: list[str] = field(default_factory=list)
    affected_los_list: list[str] = field(default_factory=list)
    recommended_intervention: str = ""
    first_seen: str = ""
    last_seen: str = ""
    trend_direction: str = ""               # "rising", "stable", "falling"
