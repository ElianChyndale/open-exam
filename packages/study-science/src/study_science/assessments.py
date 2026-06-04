"""Adaptive assessment and interleaving drill engine.

The engine is deterministic and local-first. It generates correct-only
practice questions from confirmed learning assets and persists raw learner
answers only as internal fields that are never returned by public payloads.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from hashlib import sha1
import json
import re
from pathlib import Path
from typing import Any, Literal

from study_science.data_governance import FORBIDDEN_SAFE_PAYLOAD_KEYS, sanitize_payload

WRONG_KEYS = FORBIDDEN_SAFE_PAYLOAD_KEYS
AssessmentMode = Literal[
    "quick_check",
    "interleaving_drill",
    "formula_drill",
    "coverage_gap_drill",
    "mock_transfer_drill",
    "lexical_drill",
    "mixed_exam_drill",
]
QuestionType = Literal[
    "short_answer",
    "multiple_choice",
    "formula_setup",
    "calculator_steps",
    "boundary_choice",
    "mini_case",
    "lexical_production",
    "cloze",
    "collocation",
]


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _stable_id(prefix: str, *parts: Any) -> str:
    text = "|".join(str(part) for part in parts)
    return f"{prefix}-{sha1(text.encode('utf-8')).hexdigest()[:16]}"


def _tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_+-]{2,}", text.lower()) if token not in {"the", "and", "for", "with", "when", "into"}}


@dataclass(slots=True)
class AssessmentQuestion:
    question_id: str
    assessment_id: str
    profile_id: str
    question_type: QuestionType
    prompt: str
    choices: list[str]
    correct_answer: str
    correct_reasoning: str
    correct_rule: str
    formula_latex: str | None
    ba_ii_plus_steps: list[str]
    boundary_rules: list[str]
    source_refs: list[str]
    linked_asset_ids: list[str]
    linked_topic_ids: list[str]
    linked_gap_ids: list[str]
    linked_lexical_ids: list[str]
    difficulty: Literal["easy", "medium", "hard"]
    interleaving_tags: list[str]
    validation_status: Literal["generated", "confirmed", "rejected"] = "generated"
    category: str = "asset"

    def as_dict(self) -> dict[str, Any]:
        return strip_wrong_fields(
            {
                "question_id": self.question_id,
                "assessment_id": self.assessment_id,
                "profile_id": self.profile_id,
                "question_type": self.question_type,
                "prompt": self.prompt,
                "choices": self.choices,
                "correct_answer": self.correct_answer,
                "correct_reasoning": self.correct_reasoning,
                "correct_rule": self.correct_rule,
                "formula_latex": self.formula_latex,
                "ba_ii_plus_steps": self.ba_ii_plus_steps,
                "boundary_rules": self.boundary_rules,
                "source_refs": self.source_refs,
                "linked_asset_ids": self.linked_asset_ids,
                "linked_topic_ids": self.linked_topic_ids,
                "linked_gap_ids": self.linked_gap_ids,
                "linked_lexical_ids": self.linked_lexical_ids,
                "difficulty": self.difficulty,
                "interleaving_tags": self.interleaving_tags,
                "validation_status": self.validation_status,
                "category": self.category,
            }
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> AssessmentQuestion:
        return cls(
            question_id=str(payload.get("question_id", "")),
            assessment_id=str(payload.get("assessment_id", "")),
            profile_id=str(payload.get("profile_id", "default")),
            question_type=payload.get("question_type", "short_answer"),
            prompt=str(payload.get("prompt", "")),
            choices=list(payload.get("choices") or []),
            correct_answer=str(payload.get("correct_answer", "")),
            correct_reasoning=str(payload.get("correct_reasoning", "")),
            correct_rule=str(payload.get("correct_rule", "")),
            formula_latex=payload.get("formula_latex") or None,
            ba_ii_plus_steps=list(payload.get("ba_ii_plus_steps") or []),
            boundary_rules=list(payload.get("boundary_rules") or []),
            source_refs=list(payload.get("source_refs") or []),
            linked_asset_ids=list(payload.get("linked_asset_ids") or []),
            linked_topic_ids=list(payload.get("linked_topic_ids") or []),
            linked_gap_ids=list(payload.get("linked_gap_ids") or []),
            linked_lexical_ids=list(payload.get("linked_lexical_ids") or []),
            difficulty=payload.get("difficulty", "medium"),
            interleaving_tags=list(payload.get("interleaving_tags") or []),
            validation_status=payload.get("validation_status", "generated"),
            category=str(payload.get("category", "asset")),
        )


@dataclass(slots=True)
class AssessmentResponse:
    response_id: str
    assessment_id: str
    question_id: str
    profile_id: str
    answer_text: str | None
    selected_choice: str | None
    confidence_before: float | None
    confidence_after: float | None
    time_spent_seconds: int | None
    is_correct: bool | None
    score: float | None
    feedback: dict[str, Any]
    created_at: str
    internal_answer_text: str | None = None
    internal_selected_choice: str | None = None

    def as_dict(self, *, include_internal: bool = False) -> dict[str, Any]:
        payload = {
            "response_id": self.response_id,
            "assessment_id": self.assessment_id,
            "question_id": self.question_id,
            "profile_id": self.profile_id,
            "answer_text": self.answer_text if include_internal else None,
            "selected_choice": self.selected_choice if include_internal else None,
            "confidence_before": self.confidence_before,
            "confidence_after": self.confidence_after,
            "time_spent_seconds": self.time_spent_seconds,
            "is_correct": self.is_correct,
            "score": self.score,
            "feedback": self.feedback,
            "created_at": self.created_at,
        }
        if include_internal:
            payload["internal_answer_text"] = self.internal_answer_text
            payload["internal_selected_choice"] = self.internal_selected_choice
        return strip_wrong_fields(payload)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> AssessmentResponse:
        return cls(
            response_id=str(payload.get("response_id", "")),
            assessment_id=str(payload.get("assessment_id", "")),
            question_id=str(payload.get("question_id", "")),
            profile_id=str(payload.get("profile_id", "default")),
            answer_text=payload.get("answer_text"),
            selected_choice=payload.get("selected_choice"),
            confidence_before=_float_or_none(payload.get("confidence_before")),
            confidence_after=_float_or_none(payload.get("confidence_after")),
            time_spent_seconds=_int_or_none(payload.get("time_spent_seconds")),
            is_correct=payload.get("is_correct"),
            score=_float_or_none(payload.get("score")),
            feedback=dict(payload.get("feedback") or {}),
            created_at=str(payload.get("created_at") or _now()),
            internal_answer_text=payload.get("internal_answer_text"),
            internal_selected_choice=payload.get("internal_selected_choice"),
        )


@dataclass(slots=True)
class AssessmentSession:
    assessment_id: str
    profile_id: str
    title: str
    mode: AssessmentMode
    generated_at: str
    status: Literal["draft", "active", "completed", "archived"]
    target_minutes: int
    source_signals: dict[str, Any]
    question_ids: list[str]
    summary: dict[str, Any]
    questions: list[AssessmentQuestion] = field(default_factory=list)
    responses: list[AssessmentResponse] = field(default_factory=list)
    retro: dict[str, Any] = field(default_factory=dict)

    def as_dict(self, *, include_internal: bool = False) -> dict[str, Any]:
        return strip_wrong_fields(
            {
                "assessment_id": self.assessment_id,
                "profile_id": self.profile_id,
                "title": self.title,
                "mode": self.mode,
                "generated_at": self.generated_at,
                "status": self.status,
                "target_minutes": self.target_minutes,
                "source_signals": self.source_signals,
                "question_ids": self.question_ids,
                "summary": self.summary,
                "questions": [question.as_dict() for question in self.questions],
                "responses": [response.as_dict(include_internal=include_internal) for response in self.responses],
                "retro": self.retro,
            }
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> AssessmentSession:
        return cls(
            assessment_id=str(payload.get("assessment_id", "")),
            profile_id=str(payload.get("profile_id", "default")),
            title=str(payload.get("title", "Assessment")),
            mode=payload.get("mode", "quick_check"),
            generated_at=str(payload.get("generated_at") or _now()),
            status=payload.get("status", "draft"),
            target_minutes=int(payload.get("target_minutes", 20) or 20),
            source_signals=dict(payload.get("source_signals") or {}),
            question_ids=list(payload.get("question_ids") or []),
            summary=dict(payload.get("summary") or {}),
            questions=[AssessmentQuestion.from_dict(item) for item in payload.get("questions", [])],
            responses=[AssessmentResponse.from_dict(item) for item in payload.get("responses", [])],
            retro=dict(payload.get("retro") or {}),
        )


class AssessmentService:
    """Generate, grade, and complete correct-only adaptive assessments."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.root = self.repo_root / ".system" / "memory" / "assessments"
        self.session_root = self.root / "sessions"
        self.session_root.mkdir(parents=True, exist_ok=True)
        self.review_root = self.repo_root / ".system" / "memory" / "review"
        self.language_root = self.repo_root / ".system" / "memory" / "language" / "dictionary-kernel"

    def generate(
        self,
        *,
        profile_id: str = "default",
        mode: AssessmentMode = "quick_check",
        target_minutes: int = 20,
        question_count: int = 5,
        difficulty: str = "medium",
        focus: str = "mixed",
    ) -> AssessmentSession:
        profile_id = profile_id or "default"
        generated_at = _now()
        assessment_id = _stable_id("assessment", profile_id, mode, generated_at)
        candidates = self._candidate_questions(
            assessment_id=assessment_id,
            profile_id=profile_id,
            difficulty=difficulty if difficulty in {"easy", "medium", "hard"} else "medium",
        )
        selected = self._select_questions(candidates, mode=mode, focus=focus, question_count=question_count)
        for index, question in enumerate(selected):
            question.assessment_id = assessment_id
            question.question_id = _stable_id("aq", assessment_id, question.category, question.question_id, index)
        session = AssessmentSession(
            assessment_id=assessment_id,
            profile_id=profile_id,
            title=self._title_for_mode(mode),
            mode=mode,
            generated_at=generated_at,
            status="draft",
            target_minutes=target_minutes,
            source_signals=self._source_signals(candidates),
            question_ids=[question.question_id for question in selected],
            summary={
                "available_question_count": len(candidates),
                "question_count": len(selected),
                "category_counts": dict(Counter(question.category for question in selected)),
                "question_type_counts": dict(Counter(question.question_type for question in selected)),
                "focus": focus,
                "difficulty": difficulty,
            },
            questions=selected,
        )
        self._persist(session)
        return session

    def list_sessions(self, *, profile_id: str = "default", limit: int = 50) -> list[dict[str, Any]]:
        sessions = [session for session in self._load_all() if session.profile_id in {profile_id or "default", "default"}]
        sessions.sort(key=lambda item: item.generated_at, reverse=True)
        return [session.as_dict() for session in sessions[:limit]]

    def get(self, assessment_id: str) -> AssessmentSession | None:
        path = self._session_path(assessment_id)
        if not path.exists():
            return None
        return AssessmentSession.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def start(self, assessment_id: str) -> AssessmentSession:
        session = self._require_session(assessment_id)
        if session.status == "draft":
            session.status = "active"
            self._persist(session)
        return session

    def answer_question(
        self,
        question_id: str,
        *,
        answer_text: str | None = None,
        selected_choice: str | None = None,
        confidence_before: float | None = None,
        time_spent_seconds: int | None = None,
    ) -> AssessmentResponse:
        session, question = self._find_question(question_id)
        score = self._score_answer(question, answer_text=answer_text, selected_choice=selected_choice)
        response = AssessmentResponse(
            response_id=_stable_id("ar", session.assessment_id, question_id, len(session.responses), _now()),
            assessment_id=session.assessment_id,
            question_id=question_id,
            profile_id=session.profile_id,
            answer_text=None,
            selected_choice=None,
            confidence_before=confidence_before,
            confidence_after=None,
            time_spent_seconds=time_spent_seconds,
            is_correct=score >= 0.75,
            score=score,
            feedback=self._feedback(question, score=score),
            created_at=_now(),
            internal_answer_text=answer_text,
            internal_selected_choice=selected_choice,
        )
        session.responses = [item for item in session.responses if item.question_id != question_id] + [response]
        session.status = "active" if session.status == "draft" else session.status
        self._persist(session)
        return response

    def self_grade(self, question_id: str, *, grade: str, confidence_after: float | None = None) -> AssessmentResponse:
        session, question = self._find_question(question_id)
        response = next((item for item in session.responses if item.question_id == question_id), None)
        if response is None:
            response = AssessmentResponse(
                response_id=_stable_id("ar", session.assessment_id, question_id, "self", _now()),
                assessment_id=session.assessment_id,
                question_id=question_id,
                profile_id=session.profile_id,
                answer_text=None,
                selected_choice=None,
                confidence_before=None,
                confidence_after=confidence_after,
                time_spent_seconds=None,
                is_correct=None,
                score=None,
                feedback=self._feedback(question, score=0.0),
                created_at=_now(),
            )
        mapping = {"correct": 1.0, "partial": 0.5, "incorrect": 0.0}
        response.score = mapping.get(grade, 0.0)
        response.is_correct = response.score >= 0.75
        response.confidence_after = confidence_after
        response.feedback = self._feedback(question, score=response.score)
        session.responses = [item for item in session.responses if item.question_id != question_id] + [response]
        self._persist(session)
        return response

    def complete(self, assessment_id: str) -> AssessmentSession:
        session = self._require_session(assessment_id)
        gaps_created = self._create_transfer_gaps_for_misses(session)
        session.status = "completed"
        session.retro = self._retro(session, gaps_created=gaps_created)
        session.summary.update(
            {
                "answered_count": len(session.responses),
                "score": session.retro["score"],
                "transfer_gaps_created": gaps_created,
                "completed_at": _now(),
            }
        )
        self._persist(session)
        return session

    def retro(self, assessment_id: str) -> dict[str, Any]:
        session = self._require_session(assessment_id)
        if not session.retro:
            session.retro = self._retro(session, gaps_created=0)
            self._persist(session)
        return strip_wrong_fields(session.retro)

    def recommendations(self, *, profile_id: str = "default") -> dict[str, Any]:
        questions = self._candidate_questions(assessment_id="recommendation-preview", profile_id=profile_id or "default", difficulty="medium")
        counts = Counter(question.category for question in questions)
        modes = ["interleaving_drill"]
        if counts["formula"]:
            modes.append("formula_drill")
        if counts["lexical"]:
            modes.append("lexical_drill")
        if counts["transfer"]:
            modes.append("mock_transfer_drill")
        if counts["coverage"]:
            modes.append("coverage_gap_drill")
        return {
            "profile_id": profile_id or "default",
            "available_question_count": len(questions),
            "category_counts": dict(counts),
            "recommended_modes": modes,
            "recommended_actions": [
                {"priority": 92, "title": "Generate interleaving drill", "href": "/review/assessments", "reason": "Mix confirmed assets, formulas, lexical items, coverage gaps, and transfer gaps."},
                {"priority": 80, "title": "Review assessment analytics", "href": "/review/analytics", "reason": "Use completed drills to check calibration and transfer."},
            ],
        }

    def _candidate_questions(self, *, assessment_id: str, profile_id: str, difficulty: str) -> list[AssessmentQuestion]:
        questions: list[AssessmentQuestion] = []
        questions.extend(self._asset_questions(assessment_id, profile_id, difficulty))
        questions.extend(self._coverage_questions(assessment_id, profile_id, difficulty))
        questions.extend(self._transfer_gap_questions(assessment_id, profile_id, difficulty))
        questions.extend(self._lexical_questions(assessment_id, profile_id, difficulty))
        seen: set[tuple[str, str]] = set()
        unique: list[AssessmentQuestion] = []
        for question in questions:
            key = (question.category, "|".join(question.linked_asset_ids + question.linked_gap_ids + question.linked_lexical_ids + question.linked_topic_ids) or question.prompt)
            if key in seen:
                continue
            seen.add(key)
            unique.append(question)
        return unique

    def _asset_questions(self, assessment_id: str, profile_id: str, difficulty: str) -> list[AssessmentQuestion]:
        questions: list[AssessmentQuestion] = []
        for path in (self.review_root / "asset-candidates").glob("*.json"):
            asset = self._read_json(path)
            if not self._is_confirmed_asset(asset, profile_id):
                continue
            asset_type = str(asset.get("asset_type") or "")
            if asset_type in {"formula", "formula_lab"} or asset.get("formula_latex") or asset.get("plain_formula"):
                question_type: QuestionType = "calculator_steps" if asset.get("ba_ii_plus_steps") else "formula_setup"
                category = "formula"
            elif asset_type in {"exam_boundary", "decision_rule"} or asset.get("not_when") or asset.get("common_correct_boundary_rules"):
                question_type = "boundary_choice"
                category = "asset"
            elif asset_type == "procedure":
                question_type = "calculator_steps"
                category = "formula"
            else:
                question_type = "short_answer"
                category = "asset"
            title = asset.get("title") or asset.get("trigger") or asset.get("correct_rule") or "confirmed asset"
            correct_rule = self._safe_text(asset.get("correct_rule") or asset.get("definition") or asset.get("decision") or title)
            correct_answer = self._safe_text(asset.get("plain_formula") or asset.get("formula_latex") or asset.get("canonical_answer") or correct_rule)
            prompt = self._prompt_for_asset(asset, question_type=question_type)
            questions.append(
                AssessmentQuestion(
                    question_id=_stable_id("candidate", path.stem, question_type),
                    assessment_id=assessment_id,
                    profile_id=asset.get("profile_id") or profile_id,
                    question_type=question_type,
                    prompt=prompt,
                    choices=self._choices(correct_answer) if question_type in {"multiple_choice", "boundary_choice"} else [],
                    correct_answer=correct_answer,
                    correct_reasoning=self._safe_text(asset.get("correct_reasoning") or f"Apply the confirmed rule for {title}."),
                    correct_rule=correct_rule,
                    formula_latex=asset.get("formula_latex") or asset.get("plain_formula") or None,
                    ba_ii_plus_steps=list(asset.get("ba_ii_plus_steps") or []),
                    boundary_rules=list(asset.get("common_correct_boundary_rules") or asset.get("boundary_rules") or []),
                    source_refs=list(asset.get("source_refs") or []),
                    linked_asset_ids=[asset.get("asset_id")] if asset.get("asset_id") else [],
                    linked_topic_ids=[asset.get("syllabus_topic_id") or asset.get("los")] if (asset.get("syllabus_topic_id") or asset.get("los")) else [],
                    linked_gap_ids=[],
                    linked_lexical_ids=[],
                    difficulty=difficulty,  # type: ignore[arg-type]
                    interleaving_tags=[category, asset_type],
                    category=category,
                )
            )
        return questions

    def _coverage_questions(self, assessment_id: str, profile_id: str, difficulty: str) -> list[AssessmentQuestion]:
        questions: list[AssessmentQuestion] = []
        for path in (self.review_root / "syllabus").glob("coverage-*.json"):
            payload = self._read_json(path)
            if payload and payload.get("profile_id", profile_id) not in {profile_id, "default"}:
                continue
            for record in payload.get("records", [])[:20]:
                status = record.get("coverage_status")
                if status not in {"missing", "partial", "weak", "draft_only", "stale"}:
                    continue
                topic = record.get("topic") or {}
                title = topic.get("title") or record.get("topic_id") or "coverage gap"
                questions.append(
                    AssessmentQuestion(
                        question_id=_stable_id("coverage", record.get("record_id"), status),
                        assessment_id=assessment_id,
                        profile_id=payload.get("profile_id") or profile_id,
                        question_type="mini_case",
                        prompt=f"Apply a confirmed rule to this coverage gap topic: {title}.",
                        choices=[],
                        correct_answer=f"Use the source-backed rule for {title}.",
                        correct_reasoning=f"This topic is currently {status}; practice should close the coverage gap with confirmed evidence.",
                        correct_rule=f"Review confirmed evidence and state the correct rule for {title}.",
                        formula_latex=None,
                        ba_ii_plus_steps=[],
                        boundary_rules=[],
                        source_refs=[],
                        linked_asset_ids=[],
                        linked_topic_ids=[record.get("topic_id")] if record.get("topic_id") else [],
                        linked_gap_ids=[],
                        linked_lexical_ids=[],
                        difficulty=difficulty,  # type: ignore[arg-type]
                        interleaving_tags=["coverage", status],
                        category="coverage",
                    )
                )
        return questions

    def _transfer_gap_questions(self, assessment_id: str, profile_id: str, difficulty: str) -> list[AssessmentQuestion]:
        questions: list[AssessmentQuestion] = []
        for path in (self.review_root / "mock-retro" / "transfer-gaps").glob("transfer-gap-*.json"):
            gap = self._read_json(path)
            if not gap or gap.get("profile_id", profile_id) not in {profile_id, "default"} or gap.get("status") != "open":
                continue
            gap_type = gap.get("gap_type") or "transfer_gap"
            formula_family = gap.get("formula_family") or ""
            questions.append(
                AssessmentQuestion(
                    question_id=_stable_id("gapq", gap.get("gap_id"), gap_type),
                    assessment_id=assessment_id,
                    profile_id=gap.get("profile_id") or profile_id,
                    question_type="mini_case" if gap_type != "boundary_confusion" else "boundary_choice",
                    prompt=f"Transfer drill: apply the correct rule for {formula_family or gap_type} in a new context.",
                    choices=self._choices(f"Apply the correct {formula_family or gap_type} rule.") if gap_type == "boundary_confusion" else [],
                    correct_answer=f"Apply the correct {formula_family or gap_type} rule.",
                    correct_reasoning="A transfer drill tests whether the confirmed rule can be applied without relying on the prior miss.",
                    correct_rule=f"Use the confirmed source-backed rule for {formula_family or gap_type}.",
                    formula_latex=None,
                    ba_ii_plus_steps=[],
                    boundary_rules=[],
                    source_refs=list(gap.get("source_refs") or []),
                    linked_asset_ids=[gap.get("asset_id")] if gap.get("asset_id") else [],
                    linked_topic_ids=[gap.get("topic_id")] if gap.get("topic_id") else [],
                    linked_gap_ids=[gap.get("gap_id")] if gap.get("gap_id") else [],
                    linked_lexical_ids=[],
                    difficulty=difficulty,  # type: ignore[arg-type]
                    interleaving_tags=["transfer", gap_type],
                    category="transfer",
                )
            )
        return questions

    def _lexical_questions(self, assessment_id: str, profile_id: str, difficulty: str) -> list[AssessmentQuestion]:
        questions: list[AssessmentQuestion] = []
        for path in (self.language_root / "lexical-assets").glob("*.json"):
            asset = self._read_json(path)
            if not asset or asset.get("profile_id", profile_id) not in {profile_id, "default"} or asset.get("validation_status") != "confirmed":
                continue
            headword = asset.get("headword") or "lexical item"
            collocations = list(asset.get("collocations") or [])
            question_type: QuestionType = "collocation" if collocations else "lexical_production"
            correct_answer = collocations[0] if collocations else (asset.get("translation") or asset.get("definition") or headword)
            questions.append(
                AssessmentQuestion(
                    question_id=_stable_id("lexq", asset.get("lexical_id"), question_type),
                    assessment_id=assessment_id,
                    profile_id=asset.get("profile_id") or profile_id,
                    question_type=question_type,
                    prompt=f"Produce a correct use of '{headword}' in context.",
                    choices=[],
                    correct_answer=self._safe_text(correct_answer),
                    correct_reasoning=f"Use {headword} for: {asset.get('definition') or asset.get('translation') or 'the confirmed sense'}.",
                    correct_rule=f"{headword}: {asset.get('definition') or asset.get('translation') or 'confirmed lexical sense'}.",
                    formula_latex=None,
                    ba_ii_plus_steps=[],
                    boundary_rules=[],
                    source_refs=list(asset.get("source_refs") or []),
                    linked_asset_ids=[],
                    linked_topic_ids=[],
                    linked_gap_ids=[],
                    linked_lexical_ids=[asset.get("lexical_id")] if asset.get("lexical_id") else [],
                    difficulty=difficulty,  # type: ignore[arg-type]
                    interleaving_tags=["lexical", asset.get("language") or ""],
                    category="lexical",
                )
            )
        return questions

    def _select_questions(self, questions: list[AssessmentQuestion], *, mode: str, focus: str, question_count: int) -> list[AssessmentQuestion]:
        if not questions:
            return []
        groups: dict[str, list[AssessmentQuestion]] = defaultdict(list)
        for question in questions:
            groups[question.category].append(question)

        if mode == "formula_drill" or focus == "formula":
            return (groups["formula"] + groups["transfer"] + groups["asset"])[:question_count]
        if mode == "lexical_drill" or focus == "lexical":
            return (groups["lexical"] + groups["asset"])[:question_count]
        if mode == "mock_transfer_drill" or focus == "transfer":
            return (groups["transfer"] + groups["formula"] + groups["asset"])[:question_count]
        if mode == "coverage_gap_drill" or focus == "coverage":
            return (groups["coverage"] + groups["asset"] + groups["formula"])[:question_count]

        if mode in {"interleaving_drill", "mixed_exam_drill"}:
            plan = [("asset", 0.35), ("coverage", 0.25), ("formula", 0.20), ("lexical", 0.10), ("transfer", 0.10)]
            selected: list[AssessmentQuestion] = []
            selected_ids: set[str] = set()
            for category, _ratio in plan:
                if len(selected) >= question_count:
                    break
                if groups[category]:
                    question = groups[category][0]
                    selected.append(question)
                    selected_ids.add(question.question_id)
            for category, ratio in plan:
                take = max(1 if groups[category] else 0, int(round(question_count * ratio)))
                current = sum(1 for question in selected if question.category == category)
                for question in groups[category][current:take]:
                    if len(selected) >= question_count:
                        break
                    if question.question_id in selected_ids:
                        continue
                    selected.append(question)
                    selected_ids.add(question.question_id)
            for question in questions:
                if len(selected) >= question_count:
                    break
                if question.question_id not in selected_ids:
                    selected.append(question)
                    selected_ids.add(question.question_id)
            return selected[:question_count]
        return questions[:question_count]

    def _score_answer(self, question: AssessmentQuestion, *, answer_text: str | None, selected_choice: str | None) -> float:
        submitted = (selected_choice or answer_text or "").strip()
        if not submitted:
            return 0.0
        if question.choices:
            return 1.0 if submitted.lower() == question.correct_answer.strip().lower() else 0.0
        reference = f"{question.correct_answer} {question.correct_rule} {question.correct_reasoning}"
        if submitted.lower() in reference.lower() or question.correct_answer.lower() in submitted.lower():
            return 1.0
        expected = _tokens(reference)
        actual = _tokens(submitted)
        if not expected:
            return 0.0
        overlap = len(expected.intersection(actual))
        return round(min(1.0, overlap / max(2, min(len(expected), 6))), 4)

    def _feedback(self, question: AssessmentQuestion, *, score: float) -> dict[str, Any]:
        next_action = "advance" if score >= 0.75 else "create_transfer_drill"
        return strip_wrong_fields(
            {
                "correct_answer": question.correct_answer,
                "correct_rule": question.correct_rule,
                "correct_reasoning": question.correct_reasoning,
                "formula_latex": question.formula_latex,
                "ba_ii_plus_steps": question.ba_ii_plus_steps,
                "boundary_rules": question.boundary_rules,
                "source_refs": question.source_refs,
                "next_action": next_action,
                "recommended_review_asset_ids": question.linked_asset_ids,
            }
        )

    def _create_transfer_gaps_for_misses(self, session: AssessmentSession) -> int:
        response_by_question = {response.question_id: response for response in session.responses}
        created = 0
        for question in session.questions:
            response = response_by_question.get(question.question_id)
            if response is None:
                continue
            confidence = response.confidence_before or 0.0
            score = response.score or 0.0
            if score >= 0.75 and confidence < 0.85:
                continue
            gap_type = "confidence_mismatch" if confidence >= 0.75 and score < 1.0 else self._gap_type_for_question(question)
            gap_id = _stable_id("transfer-gap-assessment", session.assessment_id, question.question_id, gap_type)
            payload = {
                "gap_id": gap_id,
                "profile_id": session.profile_id,
                "topic_id": question.linked_topic_ids[0] if question.linked_topic_ids else None,
                "asset_id": question.linked_asset_ids[0] if question.linked_asset_ids else None,
                "formula_family": question.interleaving_tags[1] if question.category == "formula" and len(question.interleaving_tags) > 1 else None,
                "gap_type": gap_type,
                "severity": round(max(0.35, confidence - score + 0.35), 4),
                "evidence_count": 1,
                "last_seen_at": _now(),
                "recommended_actions": ["Review the correct rule, then retry an interleaved assessment item."],
                "source_refs": [f"assessment:{session.assessment_id}:{question.question_id}", *question.source_refs],
                "status": "open",
            }
            gap_root = self.review_root / "mock-retro" / "transfer-gaps"
            gap_root.mkdir(parents=True, exist_ok=True)
            (gap_root / f"{gap_id}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            created += 1
        return created

    def _retro(self, session: AssessmentSession, *, gaps_created: int) -> dict[str, Any]:
        response_by_question = {response.question_id: response for response in session.responses}
        scores = [response.score or 0.0 for response in session.responses]
        topic_counts = Counter(topic_id for question in session.questions for topic_id in question.linked_topic_ids)
        category_scores: dict[str, list[float]] = defaultdict(list)
        correct_rules: list[dict[str, Any]] = []
        for question in session.questions:
            response = response_by_question.get(question.question_id)
            if response is not None:
                category_scores[question.category].append(response.score or 0.0)
            if response is None or (response.score or 0.0) < 0.75:
                correct_rules.append(
                    {
                        "question_id": question.question_id,
                        "correct_rule": question.correct_rule,
                        "correct_answer": question.correct_answer,
                        "source_refs": question.source_refs,
                        "linked_asset_ids": question.linked_asset_ids,
                    }
                )
        confidence_pairs = [
            ((response.confidence_before or 0.0), (response.score or 0.0))
            for response in session.responses
            if response.confidence_before is not None and response.score is not None
        ]
        calibration_error = 0.0
        if confidence_pairs:
            calibration_error = round(sum(abs(before - score) for before, score in confidence_pairs) / len(confidence_pairs), 4)
        return strip_wrong_fields(
            {
                "assessment_id": session.assessment_id,
                "profile_id": session.profile_id,
                "status": session.status,
                "score": round(sum(scores) / max(1, len(scores)), 4),
                "answered_count": len(session.responses),
                "question_count": len(session.questions),
                "topic_breakdown": dict(topic_counts),
                "formula_procedure_breakdown": self._category_breakdown(category_scores, ["formula", "transfer"]),
                "lexical_breakdown": self._category_breakdown(category_scores, ["lexical"]),
                "confidence_calibration": {"calibration_error": calibration_error, "pair_count": len(confidence_pairs)},
                "transfer_gaps_created": gaps_created,
                "correct_rules_to_review": correct_rules[:20],
                "recommended_next_actions": self._next_actions(session, gaps_created=gaps_created),
            }
        )

    @staticmethod
    def _category_breakdown(groups: dict[str, list[float]], keys: list[str]) -> dict[str, Any]:
        return {
            key: {"attempts": len(groups.get(key, [])), "score": round(sum(groups.get(key, [])) / max(1, len(groups.get(key, []))), 4)}
            for key in keys
        }

    @staticmethod
    def _next_actions(session: AssessmentSession, *, gaps_created: int) -> list[dict[str, Any]]:
        actions = [{"priority": 80, "title": "Review assessment analytics", "href": "/review/analytics"}]
        if gaps_created:
            actions.insert(0, {"priority": 92, "title": "Resolve new transfer gaps", "href": "/review/mock-retro"})
        if any(question.category == "formula" for question in session.questions):
            actions.append({"priority": 76, "title": "Run Formula Lab follow-up", "href": "/review/formulas"})
        return actions

    @staticmethod
    def _gap_type_for_question(question: AssessmentQuestion) -> str:
        if question.question_type in {"formula_setup", "calculator_steps"}:
            return "procedure_gap"
        if question.question_type in {"boundary_choice", "mini_case"}:
            return "interleaving_failure"
        return "concept_gap"

    @staticmethod
    def _source_signals(questions: list[AssessmentQuestion]) -> dict[str, Any]:
        return {
            "available_question_count": len(questions),
            "category_counts": dict(Counter(question.category for question in questions)),
            "question_type_counts": dict(Counter(question.question_type for question in questions)),
        }

    @staticmethod
    def _title_for_mode(mode: str) -> str:
        return {
            "quick_check": "Quick Check",
            "interleaving_drill": "Interleaving Drill",
            "formula_drill": "Formula Drill",
            "coverage_gap_drill": "Coverage Gap Drill",
            "mock_transfer_drill": "Mock Transfer Drill",
            "lexical_drill": "Lexical Drill",
            "mixed_exam_drill": "Mixed Exam Drill",
        }.get(mode, "Assessment")

    @staticmethod
    def _is_confirmed_asset(asset: dict[str, Any], profile_id: str) -> bool:
        if not asset or asset.get("profile_id", profile_id) not in {profile_id, "default"}:
            return False
        if asset.get("validation_status") not in {"confirmed", "validated", "derived"}:
            return False
        if asset.get("resource_quality_status") in {"low", "rejected"} or asset.get("quality_status") in {"low", "rejected"}:
            return False
        return True

    @staticmethod
    def _prompt_for_asset(asset: dict[str, Any], *, question_type: str) -> str:
        title = asset.get("title") or asset.get("trigger") or asset.get("subject") or "confirmed concept"
        if question_type == "formula_setup":
            return f"Set up the formula for {title} and name the key variables."
        if question_type == "calculator_steps":
            return f"List the correct calculation/procedure steps for {title}."
        if question_type == "boundary_choice":
            return f"Choose the correct boundary rule for this case: {title}."
        return f"State the correct rule for: {title}."

    @staticmethod
    def _choices(correct_answer: str) -> list[str]:
        safe_correct = correct_answer.strip() or "Use the confirmed source-backed rule."
        return [
            safe_correct,
            "Use a rule only after checking the stated boundary.",
            "Prioritize confirmed evidence before calculating.",
            "Revisit the source-backed definition before applying it.",
        ]

    @staticmethod
    def _safe_text(value: Any) -> str:
        return str(value or "").strip() or "Use the confirmed source-backed rule."

    def _find_question(self, question_id: str) -> tuple[AssessmentSession, AssessmentQuestion]:
        for session in self._load_all():
            for question in session.questions:
                if question.question_id == question_id:
                    return session, question
        raise KeyError(question_id)

    def _require_session(self, assessment_id: str) -> AssessmentSession:
        session = self.get(assessment_id)
        if session is None:
            raise KeyError(assessment_id)
        return session

    def _load_all(self) -> list[AssessmentSession]:
        sessions: list[AssessmentSession] = []
        for path in self.session_root.glob("assessment-*.json"):
            sessions.append(AssessmentSession.from_dict(json.loads(path.read_text(encoding="utf-8"))))
        return sessions

    def _persist(self, session: AssessmentSession) -> None:
        self._session_path(session.assessment_id).write_text(
            json.dumps(session.as_dict(include_internal=True), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _session_path(self, assessment_id: str) -> Path:
        return self.session_root / f"{assessment_id}.json"

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}


def assessment_outcome(score: float | None) -> str:
    if score is None:
        return "skipped"
    if score >= 0.75:
        return "recalled"
    if score >= 0.4:
        return "partial"
    return "forgot"


def strip_wrong_fields(payload: Any) -> Any:
    sanitized, _ = sanitize_payload(payload)
    return sanitized


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
