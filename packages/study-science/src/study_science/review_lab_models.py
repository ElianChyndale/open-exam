"""Review Lab 2.0 — per-unit interactive review models.

Replaces batch-marking daily review with recall-first, individually-scored
review units. Each unit is a self-contained learning atom with prompt,
recall instruction, and hidden answer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class SyllabusTopic:
    """Exam syllabus topic or LOS target used for coverage auditing."""

    topic_id: str
    profile_id: str
    exam: str | None
    subject: str
    module: str
    los: str | None
    title: str
    description: str | None
    parent_topic_id: str | None
    exam_weight: float
    importance: float
    expected_asset_types: list[str] = field(default_factory=list)
    formula_expected: bool = False
    decision_rule_expected: bool = False
    source_refs: list[str] = field(default_factory=list)
    active: bool = True

    def as_dict(self) -> dict:
        return {
            "topic_id": self.topic_id,
            "profile_id": self.profile_id,
            "exam": self.exam,
            "subject": self.subject,
            "module": self.module,
            "los": self.los,
            "title": self.title,
            "description": self.description,
            "parent_topic_id": self.parent_topic_id,
            "exam_weight": self.exam_weight,
            "importance": self.importance,
            "expected_asset_types": self.expected_asset_types,
            "formula_expected": self.formula_expected,
            "decision_rule_expected": self.decision_rule_expected,
            "source_refs": self.source_refs,
            "active": self.active,
        }


@dataclass
class AssetSyllabusLink:
    """Inspectable deterministic link between a CorrectKnowledgeAsset and topic."""

    asset_id: str
    topic_id: str
    match_reason: str
    confidence: float
    created_by: Literal["exact_los", "module_match", "keyword_match", "manual"]

    def as_dict(self) -> dict:
        return {
            "asset_id": self.asset_id,
            "topic_id": self.topic_id,
            "match_reason": self.match_reason,
            "confidence": self.confidence,
            "created_by": self.created_by,
        }


@dataclass
class SyllabusCoverageRecord:
    """Coverage state for one syllabus topic."""

    record_id: str
    profile_id: str
    topic_id: str
    confirmed_asset_count: int
    draft_asset_count: int
    rejected_asset_count: int
    formula_asset_count: int
    decision_rule_asset_count: int
    mistake_link_count: int
    mastery_state: str
    coverage_status: Literal["covered", "partial", "draft_only", "missing", "weak", "stale"]
    coverage_score: float
    missing_asset_types: list[str] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    last_reviewed_at: str | None = None
    next_review_at: str | None = None

    def as_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "profile_id": self.profile_id,
            "topic_id": self.topic_id,
            "confirmed_asset_count": self.confirmed_asset_count,
            "draft_asset_count": self.draft_asset_count,
            "rejected_asset_count": self.rejected_asset_count,
            "formula_asset_count": self.formula_asset_count,
            "decision_rule_asset_count": self.decision_rule_asset_count,
            "mistake_link_count": self.mistake_link_count,
            "mastery_state": self.mastery_state,
            "coverage_status": self.coverage_status,
            "coverage_score": self.coverage_score,
            "missing_asset_types": self.missing_asset_types,
            "recommended_actions": self.recommended_actions,
            "last_reviewed_at": self.last_reviewed_at,
            "next_review_at": self.next_review_at,
        }


@dataclass
class MockSession:
    """A local mock/practice evidence bundle imported for transfer-gap retro."""

    mock_id: str
    profile_id: str
    title: str
    exam: str | None
    started_at: str | None
    completed_at: str | None
    source_type: Literal["manual", "import_text", "quiz", "mock", "existing_attempts"]
    total_questions: int
    correct_count: int
    score: float | None
    time_spent_seconds: int | None
    source_refs: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "mock_id": self.mock_id,
            "profile_id": self.profile_id,
            "title": self.title,
            "exam": self.exam,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "source_type": self.source_type,
            "total_questions": self.total_questions,
            "correct_count": self.correct_count,
            "score": self.score,
            "time_spent_seconds": self.time_spent_seconds,
            "source_refs": self.source_refs,
        }


@dataclass
class MockQuestionEvidence:
    """One sanitized/correct-rule projection of a mock question."""

    evidence_id: str
    mock_id: str
    profile_id: str
    question_number: int | None
    topic_id: str | None
    asset_id: str | None
    subject: str | None
    module: str | None
    los: str | None
    is_correct: bool
    confidence_before: float | None
    time_spent_seconds: int | None
    correct_rule: str
    tested_skill: str | None
    tested_formula: str | None
    boundary_rule: str | None
    correct_steps: list[str] = field(default_factory=list)
    ba_ii_plus_steps: list[str] = field(default_factory=list)
    wrong_choice_or_output: str | None = None
    wrong_reasoning: str | None = None
    wrong_formula: str | None = None
    source_refs: list[str] = field(default_factory=list)
    created_at: str = ""

    def as_dict(self, *, include_internal: bool = False) -> dict:
        payload = {
            "evidence_id": self.evidence_id,
            "mock_id": self.mock_id,
            "profile_id": self.profile_id,
            "question_number": self.question_number,
            "topic_id": self.topic_id,
            "asset_id": self.asset_id,
            "subject": self.subject,
            "module": self.module,
            "los": self.los,
            "is_correct": self.is_correct,
            "confidence_before": self.confidence_before,
            "time_spent_seconds": self.time_spent_seconds,
            "correct_rule": self.correct_rule,
            "tested_skill": self.tested_skill,
            "tested_formula": self.tested_formula,
            "boundary_rule": self.boundary_rule,
            "correct_steps": self.correct_steps,
            "ba_ii_plus_steps": self.ba_ii_plus_steps,
            "source_refs": self.source_refs,
            "created_at": self.created_at,
        }
        if include_internal:
            payload.update(
                {
                    "wrong_choice_or_output": self.wrong_choice_or_output,
                    "wrong_reasoning": self.wrong_reasoning,
                    "wrong_formula": self.wrong_formula,
                }
            )
        return payload


@dataclass
class TransferGapRecord:
    """Open weakness signal inferred from mock/practice evidence."""

    gap_id: str
    profile_id: str
    topic_id: str | None
    asset_id: str | None
    formula_family: str | None
    gap_type: Literal[
        "concept_gap",
        "formula_recall_gap",
        "variable_confusion",
        "boundary_confusion",
        "procedure_gap",
        "calculator_procedure_gap",
        "time_pressure",
        "confidence_mismatch",
        "interleaving_failure",
    ]
    severity: float
    evidence_count: int
    last_seen_at: str
    recommended_actions: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)
    status: Literal["open", "improving", "resolved"] = "open"

    def as_dict(self) -> dict:
        return {
            "gap_id": self.gap_id,
            "profile_id": self.profile_id,
            "topic_id": self.topic_id,
            "asset_id": self.asset_id,
            "formula_family": self.formula_family,
            "gap_type": self.gap_type,
            "severity": self.severity,
            "evidence_count": self.evidence_count,
            "last_seen_at": self.last_seen_at,
            "recommended_actions": self.recommended_actions,
            "source_refs": self.source_refs,
            "status": self.status,
        }


@dataclass
class KnowledgeSourceDocument:
    """A local note/PDF source imported for candidate asset extraction."""

    source_id: str
    profile_id: str
    title: str
    source_type: Literal["pdf_note", "markdown_note", "text_note", "manual"]
    file_path: str | None
    content_hash: str
    imported_at: str
    page_count: int | None
    extraction_status: Literal["pending", "extracted", "failed"]
    extraction_error: str | None
    source_refs: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "profile_id": self.profile_id,
            "title": self.title,
            "source_type": self.source_type,
            "file_path": self.file_path,
            "content_hash": self.content_hash,
            "imported_at": self.imported_at,
            "page_count": self.page_count,
            "extraction_status": self.extraction_status,
            "extraction_error": self.extraction_error,
            "source_refs": self.source_refs,
        }


@dataclass
class LearningResource:
    """ResourceOS quality-gated wrapper around a local source document."""

    resource_id: str
    profile_id: str
    title: str
    resource_type: Literal[
        "text_note",
        "pdf_note",
        "web_article",
        "official_syllabus",
        "textbook",
        "lecture_slide",
        "dictionary",
        "manual",
        "unknown",
    ]
    origin: Literal["manual", "import_text", "file", "url", "system_seed"]
    url: str | None
    file_path: str | None
    content_hash: str
    imported_at: str
    source_refs: list[str]
    quality_score: float = 0.0
    quality_status: Literal["unscored", "low", "medium", "high", "trusted", "rejected"] = "unscored"
    validation_status: Literal["draft", "needs_review", "confirmed", "rejected"] = "draft"
    notes: str | None = None
    source_id: str = ""
    duplicate_of: str | None = None
    warnings: list[str] = field(default_factory=list)
    quality_dimensions: dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "resource_id": self.resource_id,
            "profile_id": self.profile_id,
            "title": self.title,
            "resource_type": self.resource_type,
            "origin": self.origin,
            "url": self.url,
            "file_path": self.file_path,
            "content_hash": self.content_hash,
            "imported_at": self.imported_at,
            "source_refs": self.source_refs,
            "quality_score": self.quality_score,
            "quality_status": self.quality_status,
            "validation_status": self.validation_status,
            "notes": self.notes,
            "source_id": self.source_id,
            "duplicate_of": self.duplicate_of,
            "warnings": self.warnings,
            "quality_dimensions": self.quality_dimensions,
        }


@dataclass
class KnowledgeSourceSegment:
    """A source-backed text span used to justify generated assets."""

    segment_id: str
    source_id: str
    page: int | None
    heading: str | None
    text: str
    char_start: int | None
    char_end: int | None
    source_ref: str
    evidence_type: Literal[
        "definition",
        "formula",
        "rule",
        "boundary",
        "example",
        "procedure",
        "citation",
        "dictionary_entry",
        "other",
    ] = "other"
    confidence: float = 0.5

    def as_dict(self) -> dict:
        return {
            "segment_id": self.segment_id,
            "source_id": self.source_id,
            "page": self.page,
            "heading": self.heading,
            "text": self.text,
            "char_start": self.char_start,
            "char_end": self.char_end,
            "source_ref": self.source_ref,
            "evidence_type": self.evidence_type,
            "confidence": self.confidence,
        }


@dataclass
class FormulaMetadata:
    """Formula-specific metadata for Formula Lab assets."""

    formula_latex: str
    plain_formula: str | None = None
    variables: list[dict] = field(default_factory=list)
    applies_when: list[str] = field(default_factory=list)
    not_when: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    common_correct_boundary_rules: list[str] = field(default_factory=list)
    worked_example: str | None = None
    ba_ii_plus_steps: list[str] = field(default_factory=list)
    formula_family: str | None = None
    difficulty: Literal["basic", "intermediate", "advanced"] = "basic"

    def as_dict(self) -> dict:
        return {
            "formula_latex": self.formula_latex,
            "plain_formula": self.plain_formula,
            "variables": self.variables,
            "applies_when": self.applies_when,
            "not_when": self.not_when,
            "assumptions": self.assumptions,
            "common_correct_boundary_rules": self.common_correct_boundary_rules,
            "worked_example": self.worked_example,
            "ba_ii_plus_steps": self.ba_ii_plus_steps,
            "formula_family": self.formula_family,
            "difficulty": self.difficulty,
        }


@dataclass
class CorrectKnowledgeAsset:
    """Correct-answer-centered asset selected for Review Lab."""

    asset_id: str
    asset_type: Literal[
        "syllabus_core",
        "mistake_corrected",
        "formula_lab",
        "transfer_or_interleaving",
        "definition",
        "formula",
        "decision_rule",
        "exam_boundary",
        "procedure",
        "concept_comparison",
        "worked_example",
    ]
    profile_id: str = "default"
    subject: str = ""
    module: str = ""
    los: str = ""
    title: str = ""
    trigger: str = ""
    correct_rule: str = ""
    formula_latex: str = ""
    plain_formula: str = ""
    variables: list[dict] = field(default_factory=list)
    applies_when: list[str] = field(default_factory=list)
    not_when: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    common_correct_boundary_rules: list[str] = field(default_factory=list)
    example: str = ""
    correct_steps: list[str] = field(default_factory=list)
    ba_ii_plus_steps: list[str] = field(default_factory=list)
    formula_family: str = ""
    syllabus_topic_id: str = ""
    difficulty: Literal["basic", "intermediate", "advanced"] = "basic"
    source_refs: list[str] = field(default_factory=list)
    source_quality: float = 0.7
    resource_id: str = ""
    resource_quality_status: str = ""
    resource_validation_status: str = ""
    resource_match_reasons: list[str] = field(default_factory=list)
    resource_conflicts: list[str] = field(default_factory=list)
    resource_promoted_at: str = ""
    exam_weight: float = 0.5
    mistake_link_count: int = 0
    decay_risk: float = 0.5
    mastery_state: str = "New"
    next_review_at: str = ""
    created_from: Literal[
        "syllabus",
        "mistake",
        "formula",
        "transfer",
        "pdf_note",
        "markdown_note",
        "text_note",
        "manual",
    ] = "syllabus"
    validation_status: Literal["validated", "derived", "draft", "needs_review", "confirmed", "rejected"] = "derived"

    def as_dict(self) -> dict:
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "profile_id": self.profile_id,
            "subject": self.subject,
            "module": self.module,
            "los": self.los,
            "title": self.title,
            "trigger": self.trigger,
            "correct_rule": self.correct_rule,
            "formula_latex": self.formula_latex,
            "plain_formula": self.plain_formula,
            "variables": self.variables,
            "applies_when": self.applies_when,
            "not_when": self.not_when,
            "assumptions": self.assumptions,
            "common_correct_boundary_rules": self.common_correct_boundary_rules,
            "example": self.example,
            "correct_steps": self.correct_steps,
            "ba_ii_plus_steps": self.ba_ii_plus_steps,
            "formula_family": self.formula_family,
            "syllabus_topic_id": self.syllabus_topic_id,
            "difficulty": self.difficulty,
            "source_refs": self.source_refs,
            "source_quality": self.source_quality,
            "resource_id": self.resource_id,
            "resource_quality_status": self.resource_quality_status,
            "resource_validation_status": self.resource_validation_status,
            "resource_match_reasons": self.resource_match_reasons,
            "resource_conflicts": self.resource_conflicts,
            "resource_promoted_at": self.resource_promoted_at,
            "exam_weight": self.exam_weight,
            "mistake_link_count": self.mistake_link_count,
            "decay_risk": self.decay_risk,
            "mastery_state": self.mastery_state,
            "next_review_at": self.next_review_at,
            "created_from": self.created_from,
            "validation_status": self.validation_status,
        }


@dataclass
class DailyReviewUnit:
    """A single reviewable unit in the Daily Review Lab.

    The answer and worked example are NEVER rendered in the DOM until
    the learner explicitly reveals them. This enforces recall-first
    pedagogy.
    """

    unit_id: str
    unit_type: Literal[
        "knowledge_point",
        "mistake_card",
        "formula_lab",
        "concept_discrimination",
        "syllabus_core",
        "mistake_corrected",
        "transfer_or_interleaving",
        "definition",
        "formula",
        "decision_rule",
        "exam_boundary",
        "procedure",
        "concept_comparison",
        "worked_example",
    ]
    prompt: str
    review_id: str = ""
    asset_id: str = ""
    asset_type: str = ""
    display_mode: Literal[
        "recall_reveal",
        "formula_input",
        "interleaving",
        "derive_formula",
        "recall_formula",
        "identify_variables",
        "choose_applicability",
        "solve_formula_mini_case",
        "ba_ii_plus_procedure",
    ] = "recall_reveal"
    front_prompt: str = ""
    correct_answer: str = ""
    correct_reasoning: str = ""
    correct_steps: list[str] = field(default_factory=list)
    ba_ii_plus_steps: list[str] = field(default_factory=list)
    boundary_rules: list[str] = field(default_factory=list)
    variables: list[dict] = field(default_factory=list)
    applies_when: list[str] = field(default_factory=list)
    not_when: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    formula_family: str = ""
    difficulty: str = ""
    recall_instruction: str = ""
    answer: str = ""
    formula_latex: str = ""
    worked_example: str = ""
    common_wrong_path: str = ""
    exam_trap: str = ""
    source_refs: list[str] = field(default_factory=list)
    source_spans: list[dict] = field(default_factory=list)
    due_reason: str = ""
    memory_state: str = "New"
    priority: int = 50
    interaction_mode: Literal[
        "recall_reveal",
        "formula_input",
        "multiple_choice",
        "derive_formula",
        "recall_formula",
        "identify_variables",
        "choose_applicability",
        "solve_formula_mini_case",
        "ba_ii_plus_procedure",
    ] = "recall_reveal"

    # Linked entities
    knowledge_id: str = ""
    card_id: str = ""
    subject: str = ""
    heading: str = ""
    los: str = ""

    def as_dict(self) -> dict:
        front_prompt = self.front_prompt or self.prompt
        correct_answer = self.correct_answer or self.answer
        correct_reasoning = self.correct_reasoning or self.worked_example or correct_answer
        display_mode = self.display_mode or self.interaction_mode
        return {
            "unit_id": self.unit_id,
            "review_id": self.review_id,
            "asset_id": self.asset_id or self.knowledge_id or self.card_id,
            "asset_type": self.asset_type or self.unit_type,
            "unit_type": self.unit_type,
            "display_mode": display_mode,
            "front_prompt": front_prompt,
            "correct_answer": correct_answer,
            "correct_reasoning": correct_reasoning,
            "correct_steps": self.correct_steps,
            "ba_ii_plus_steps": self.ba_ii_plus_steps,
            "boundary_rules": self.boundary_rules,
            "variables": self.variables,
            "applies_when": self.applies_when,
            "not_when": self.not_when,
            "assumptions": self.assumptions,
            "formula_family": self.formula_family,
            "difficulty": self.difficulty,
            "memory_state_before": self.memory_state,
            "prompt": self.prompt,
            "recall_instruction": self.recall_instruction,
            "answer": self.answer,
            "formula_latex": self.formula_latex,
            "worked_example": self.worked_example,
            # Kept only as a legacy UI key. It is intentionally blank so Review
            # Lab never re-exposes the learner's previous wrong answer.
            "common_wrong_path": "",
            "exam_trap": self.exam_trap,
            "source_refs": self.source_refs,
            "source_spans": self.source_spans,
            "due_reason": self.due_reason,
            "memory_state": self.memory_state,
            "priority": self.priority,
            "interaction_mode": self.interaction_mode,
            "knowledge_id": self.knowledge_id,
            "card_id": self.card_id,
            "subject": self.subject,
            "heading": self.heading,
            "los": self.los,
        }


@dataclass
class ReviewUnitOutcome:
    """Learner's self-assessed outcome for a single review unit.

    Captures metacognitive data (confidence_before/after) and behavioral
    signals (time_spent, needed_hint) for calibration and scheduling.
    """

    unit_id: str
    confidence_before: int = 2          # 0-4
    time_spent_seconds: int = 0
    needed_hint: bool = False
    outcome: Literal["recalled", "partial", "forgot", "skipped"] = "recalled"
    confidence_after: int = 2           # 0-4
    answer_quality: Literal["perfect", "minor_gap", "major_gap", "blank"] = "perfect"
    fix_rule_helpful: bool | None = None
    next_action: Literal["advance", "stay", "drill", "revisit_source"] = "advance"

    def as_dict(self) -> dict:
        return {
            "unit_id": self.unit_id,
            "confidence_before": self.confidence_before,
            "time_spent_seconds": self.time_spent_seconds,
            "needed_hint": self.needed_hint,
            "outcome": self.outcome,
            "confidence_after": self.confidence_after,
            "answer_quality": self.answer_quality,
            "fix_rule_helpful": self.fix_rule_helpful,
            "next_action": self.next_action,
        }


@dataclass
class ReviewLabSession:
    """An active recall-first review session.

    Sessions are persisted as JSON so they survive page reloads.
    """

    session_id: str
    review_id: str
    status: Literal["active", "paused", "completed", "abandoned"] = "active"
    units: list[DailyReviewUnit] = field(default_factory=list)
    current_unit_index: int = 0
    completed_unit_ids: list[str] = field(default_factory=list)
    outcomes: list[ReviewUnitOutcome] = field(default_factory=list)
    energy_level: int = 2
    focus_topic: str = ""
    started_at: str = ""
    completed_at: str = ""
    paused_at: str = ""
    resumed_at: str = ""

    def as_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "review_id": self.review_id,
            "status": self.status,
            "units": [u.as_dict() for u in self.units],
            "current_unit_index": self.current_unit_index,
            "completed_unit_ids": self.completed_unit_ids,
            "outcomes": [o.as_dict() for o in self.outcomes],
            "energy_level": self.energy_level,
            "focus_topic": self.focus_topic,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "paused_at": self.paused_at,
            "resumed_at": self.resumed_at,
        }

    @property
    def current_unit(self) -> DailyReviewUnit | None:
        if 0 <= self.current_unit_index < len(self.units):
            return self.units[self.current_unit_index]
        return None

    @property
    def progress_pct(self) -> float:
        if not self.units:
            return 0.0
        return len(self.completed_unit_ids) / len(self.units)

    @property
    def is_complete(self) -> bool:
        return len(self.completed_unit_ids) >= len(self.units)
