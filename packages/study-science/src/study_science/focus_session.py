"""Unified focus session orchestration.

Focus sessions turn the adaptive study plan into one calm task at a time.
They reuse existing review, formula, lexical, planner, and tutor services
while keeping draft or raw diagnostic content out of review steps.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from hashlib import sha1
import json
from pathlib import Path
from typing import Any, Literal

from study_science.data_governance import sanitize_payload
from study_science.review_lab import ReviewLabEngine
from study_science.study_planner import StudyPlan, StudyPlanBlock, StudyPlannerService


FocusStatus = Literal["active", "completed", "abandoned"]
FocusStepStatus = Literal["pending", "in_progress", "completed", "skipped", "blocked"]
FocusStepType = Literal[
    "review_lab",
    "formula_lab",
    "lexical_review",
    "assessment",
    "tutor_hint",
    "coverage_confirmation",
    "resource_confirmation",
    "reflection",
]

TRUSTED_ASSET_STATUSES = {"confirmed", "validated", "derived"}


@dataclass
class FocusStep:
    step_id: str
    focus_id: str
    step_type: FocusStepType
    title: str
    description: str
    target_minutes: int
    launch_route: str | None = None
    embedded_payload: dict[str, Any] = field(default_factory=dict)
    source_refs: list[str] = field(default_factory=list)
    linked_asset_ids: list[str] = field(default_factory=list)
    linked_topic_ids: list[str] = field(default_factory=list)
    linked_lexical_ids: list[str] = field(default_factory=list)
    linked_gap_ids: list[str] = field(default_factory=list)
    status: FocusStepStatus = "pending"
    blocked_reason: str | None = None
    correct_only_warning: str | None = None
    completed_at: str | None = None
    completion_outcome: str | None = None

    def as_dict(self) -> dict[str, Any]:
        sanitized, _ = sanitize_payload(asdict(self))
        return sanitized

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> FocusStep:
        return cls(
            step_id=str(payload.get("step_id") or ""),
            focus_id=str(payload.get("focus_id") or ""),
            step_type=str(payload.get("step_type") or "reflection"),  # type: ignore[arg-type]
            title=str(payload.get("title") or ""),
            description=str(payload.get("description") or ""),
            target_minutes=int(payload.get("target_minutes") or 0),
            launch_route=payload.get("launch_route"),
            embedded_payload=dict(payload.get("embedded_payload") or {}),
            source_refs=list(payload.get("source_refs") or []),
            linked_asset_ids=list(payload.get("linked_asset_ids") or []),
            linked_topic_ids=list(payload.get("linked_topic_ids") or []),
            linked_lexical_ids=list(payload.get("linked_lexical_ids") or []),
            linked_gap_ids=list(payload.get("linked_gap_ids") or []),
            status=str(payload.get("status") or "pending"),  # type: ignore[arg-type]
            blocked_reason=payload.get("blocked_reason"),
            correct_only_warning=payload.get("correct_only_warning"),
            completed_at=payload.get("completed_at"),
            completion_outcome=payload.get("completion_outcome"),
        )


@dataclass
class FocusSession:
    focus_id: str
    profile_id: str
    plan_id: str | None
    source: str
    status: FocusStatus
    current_step_id: str | None
    created_at: str
    updated_at: str
    completed_at: str | None
    total_target_minutes: int
    steps: list[FocusStep]
    summary: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "focus_id": self.focus_id,
            "profile_id": self.profile_id,
            "plan_id": self.plan_id,
            "source": self.source,
            "status": self.status,
            "current_step_id": self.current_step_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
            "total_target_minutes": self.total_target_minutes,
            "steps": [step.as_dict() for step in self.steps],
            "summary": self.summary,
        }
        sanitized, _ = sanitize_payload(payload)
        return sanitized

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> FocusSession:
        steps = [FocusStep.from_dict(step) for step in payload.get("steps", [])]
        return cls(
            focus_id=str(payload.get("focus_id") or ""),
            profile_id=str(payload.get("profile_id") or "default"),
            plan_id=payload.get("plan_id"),
            source=str(payload.get("source") or "today_plan"),
            status=str(payload.get("status") or "active"),  # type: ignore[arg-type]
            current_step_id=payload.get("current_step_id"),
            created_at=str(payload.get("created_at") or _now()),
            updated_at=str(payload.get("updated_at") or _now()),
            completed_at=payload.get("completed_at"),
            total_target_minutes=int(payload.get("total_target_minutes") or sum(step.target_minutes for step in steps)),
            steps=steps,
            summary=dict(payload.get("summary") or {}),
        )


class FocusSessionService:
    """Build and advance a one-path guided study session."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.root = self.repo_root / ".system" / "memory" / "focus"
        self.session_root = self.root / "sessions"
        self.latest_root = self.root / "latest"
        for path in (self.session_root, self.latest_root):
            path.mkdir(parents=True, exist_ok=True)
        self.planner = StudyPlannerService(self.repo_root)
        self.review = ReviewLabEngine(self.repo_root)

    def start(
        self,
        *,
        profile_id: str = "default",
        plan_id: str | None = None,
        source: str = "today_plan",
        force_new: bool = False,
    ) -> FocusSession:
        profile_id = profile_id or "default"
        existing = self.current(profile_id=profile_id)
        if existing and not force_new and (not plan_id or existing.plan_id == plan_id):
            return existing

        plan = self.planner.get_plan(plan_id) if plan_id else self.planner.today(profile_id=profile_id)
        if plan is None:
            plan = self.planner.today(profile_id=profile_id)

        created_at = _now()
        focus_id = _stable_id("focus", profile_id, plan.plan_id, created_at)
        steps = self._steps_from_plan(focus_id=focus_id, profile_id=profile_id, plan=plan)
        if not steps:
            steps = self._fallback_steps(focus_id=focus_id, profile_id=profile_id, plan=plan)
        if not any(step.step_type == "reflection" for step in steps):
            steps.append(self._reflection_step(focus_id=focus_id, profile_id=profile_id, target_minutes=8))
        steps = _balance_step_sequence(steps)
        _fit_focus_minutes(steps, plan.available_minutes)

        session = FocusSession(
            focus_id=focus_id,
            profile_id=profile_id,
            plan_id=plan.plan_id,
            source=source or "today_plan",
            status="active",
            current_step_id=_next_step_id(steps),
            created_at=created_at,
            updated_at=created_at,
            completed_at=None,
            total_target_minutes=sum(step.target_minutes for step in steps),
            steps=steps,
            summary=self._summary(steps),
        )
        self._persist(session)
        self._write_latest(session)
        return session

    def current(self, *, profile_id: str = "default") -> FocusSession | None:
        latest_path = self._latest_path(profile_id or "default")
        if latest_path.exists():
            focus_id = latest_path.read_text(encoding="utf-8").strip()
            session = self.get(focus_id)
            if session and session.status == "active":
                return session
        sessions = [
            session
            for session in self._read_sessions()
            if session.profile_id == (profile_id or "default") and session.status == "active"
        ]
        sessions.sort(key=lambda item: item.updated_at, reverse=True)
        return sessions[0] if sessions else None

    def get(self, focus_id: str) -> FocusSession | None:
        path = self._session_path(focus_id)
        if not path.exists():
            return None
        return FocusSession.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def start_step(self, focus_id: str, step_id: str) -> FocusSession:
        session = self._require_session(focus_id)
        step = _require_step(session, step_id)
        if step.status == "blocked":
            raise ValueError(step.blocked_reason or "Focus step is blocked.")
        if step.status == "pending":
            step.status = "in_progress"
        session.current_step_id = step.step_id
        return self._touch_and_persist(session)

    def complete_step(
        self,
        focus_id: str,
        step_id: str,
        *,
        outcome: str = "recalled",
        actual_minutes: int | None = None,
        notes: str = "",
    ) -> FocusSession:
        session = self._require_session(focus_id)
        step = _require_step(session, step_id)
        if step.status == "blocked":
            raise ValueError(step.blocked_reason or "Focus step is blocked.")
        if step.status in {"completed", "skipped"}:
            return self._touch_and_persist(session)
        step.status = "completed"
        step.completed_at = _now()
        step.completion_outcome = notes.strip() or _outcome_label(outcome)
        self._complete_embedded_adapter(step, outcome=outcome, actual_minutes=actual_minutes)
        session.current_step_id = _next_step_id(session.steps, after_step_id=step.step_id)
        self._maybe_complete_session(session)
        return self._touch_and_persist(session)

    def skip_step(self, focus_id: str, step_id: str, *, reason: str = "") -> FocusSession:
        session = self._require_session(focus_id)
        step = _require_step(session, step_id)
        if step.status in {"completed", "skipped"}:
            return self._touch_and_persist(session)
        step.status = "skipped"
        step.completed_at = _now()
        step.completion_outcome = f"Skipped: {reason.strip() or 'No reason provided.'}"
        self._skip_plan_block(step, reason=reason)
        session.current_step_id = _next_step_id(session.steps, after_step_id=step.step_id)
        self._maybe_complete_session(session)
        return self._touch_and_persist(session)

    def complete(self, focus_id: str) -> FocusSession:
        session = self._require_session(focus_id)
        session.status = "completed"
        session.current_step_id = None
        session.completed_at = session.completed_at or _now()
        return self._touch_and_persist(session)

    def abandon(self, focus_id: str, *, reason: str = "") -> FocusSession:
        session = self._require_session(focus_id)
        session.status = "abandoned"
        session.current_step_id = None
        session.summary = self._summary(session.steps)
        session.summary["abandon_reason"] = reason.strip() or "No reason provided."
        self._persist_latest_if_current_abandoned(session)
        return self._touch_and_persist(session)

    def _steps_from_plan(self, *, focus_id: str, profile_id: str, plan: StudyPlan) -> list[FocusStep]:
        steps: list[FocusStep] = []
        pending_blocks = [block for block in plan.blocks if block.status != "completed"]
        for index, block in enumerate(pending_blocks, start=1):
            step_type = _step_type_for_block(block.block_type)
            step_id = _stable_id("focus-step", focus_id, index, block.block_id, step_type)
            embedded = self._embedded_payload(profile_id=profile_id, block=block, step_type=step_type)
            blocked_reason = block.blocked_reason or embedded.pop("_blocked_reason", None)
            status: FocusStepStatus = "blocked" if blocked_reason or block.status == "blocked" else "pending"
            launch_route = _launch_route_for_step(step_type, block.launch_route)
            step = FocusStep(
                step_id=step_id,
                focus_id=focus_id,
                step_type=step_type,
                title=_step_title(block, step_type),
                description=_step_description(block, step_type),
                target_minutes=max(5, int(block.target_minutes or 5)),
                launch_route=launch_route,
                embedded_payload={
                    **embedded,
                    "study_block_id": block.block_id,
                    "plan_id": block.plan_id,
                },
                source_refs=_unique(list(embedded.get("source_refs") or [])),
                linked_asset_ids=_trusted_asset_ids(block.linked_asset_ids, self.review),
                linked_topic_ids=list(block.linked_topic_ids),
                linked_lexical_ids=list(block.linked_lexical_ids),
                linked_gap_ids=list(block.linked_gap_ids),
                status=status,
                blocked_reason=blocked_reason,
                correct_only_warning=_correct_only_warning(step_type),
            )
            if step_type == "coverage_confirmation":
                step.linked_asset_ids = list(block.linked_asset_ids)
            if step_type == "resource_confirmation":
                step.linked_asset_ids = list(block.linked_asset_ids)
            if step_type == "lexical_review":
                step.linked_lexical_ids = _unique([*step.linked_lexical_ids, *list(embedded.get("linked_lexical_ids") or [])])
            if step_type in {"review_lab", "formula_lab"}:
                step.linked_asset_ids = _unique([*step.linked_asset_ids, *list(embedded.get("linked_asset_ids") or [])])
            steps.append(step)
        return steps

    def _fallback_steps(self, *, focus_id: str, profile_id: str, plan: StudyPlan) -> list[FocusStep]:
        return [
            FocusStep(
                step_id=_stable_id("focus-step", focus_id, "fallback", "mission"),
                focus_id=focus_id,
                step_type="tutor_hint",
                title="Pick the safest next action",
                description="No confirmed recall work is ready, so inspect the local study state before adding content.",
                target_minutes=min(max(5, plan.available_minutes // 3), 20),
                launch_route="/review/mission-control",
                embedded_payload={
                    "adapter": "tutor_hint",
                    "prompt": "Ask for a grounded next action from confirmed local evidence.",
                    "next_action": "Open Mission Control or ask Tutor for a source-backed plan.",
                },
                status="pending",
                correct_only_warning=_correct_only_warning("tutor_hint"),
            ),
            self._reflection_step(focus_id=focus_id, profile_id=profile_id, target_minutes=8),
        ]

    def _reflection_step(self, *, focus_id: str, profile_id: str, target_minutes: int) -> FocusStep:
        return FocusStep(
            step_id=_stable_id("focus-step", focus_id, "reflection", profile_id),
            focus_id=focus_id,
            step_type="reflection",
            title="Session reflection",
            description="Record what moved, what stayed blocked, and the next safe action.",
            target_minutes=max(5, target_minutes),
            launch_route="/review/mission-control",
            embedded_payload={
                "adapter": "reflection",
                "prompt": "What improved, what remains blocked, and what should the next session do first?",
                "fields": ["moved", "blocked", "next_action"],
            },
            status="pending",
            correct_only_warning=_correct_only_warning("reflection"),
        )

    def _embedded_payload(self, *, profile_id: str, block: StudyPlanBlock, step_type: FocusStepType) -> dict[str, Any]:
        if step_type == "review_lab":
            return self._review_payload(block)
        if step_type == "formula_lab":
            return self._formula_payload(profile_id, block)
        if step_type == "lexical_review":
            return self._lexical_payload(profile_id, block)
        if step_type == "assessment":
            return {
                "adapter": "assessment",
                "prompt": block.description or block.title,
                "next_action": "Use Assessment Lab when you want a timed transfer check.",
                "source_refs": [],
            }
        if step_type == "tutor_hint":
            return {
                "adapter": "tutor_hint",
                "prompt": block.description or block.title,
                "next_action": "Ask Tutor for a hint grounded in confirmed local evidence.",
                "source_refs": [],
            }
        if step_type == "coverage_confirmation":
            return {
                "adapter": "coverage_confirmation",
                "prompt": block.due_reason or block.description,
                "next_action": block.launch_route or "/review/assets",
                "source_refs": [],
            }
        if step_type == "resource_confirmation":
            return {
                "adapter": "resource_confirmation",
                "prompt": block.due_reason or block.description,
                "next_action": block.launch_route or "/review/resources",
                "source_refs": [],
            }
        return {
            "adapter": "reflection",
            "prompt": "What moved, what stayed blocked, and what should happen next?",
            "source_refs": [],
        }

    def _review_payload(self, block: StudyPlanBlock) -> dict[str, Any]:
        try:
            preview = self.review.get_today_units(max_units=1)
            review_id = str(preview.get("review_id") or "")
            session = self.review.create_session(review_id=review_id, max_units=1)
            unit = session.current_unit or (session.units[0] if session.units else None)
            if unit is None:
                raise ValueError("No confirmed Review Lab units are ready.")
            unit_payload = unit.as_dict()
            return _safe_payload(
                _local_reveal_payload(
                    {
                        "adapter": "review_lab",
                        "session_id": session.session_id,
                        "unit_id": unit.unit_id,
                        "prompt": unit_payload.get("front_prompt") or unit_payload.get("prompt"),
                        "display_mode": unit_payload.get("display_mode"),
                        "correct_answer": unit_payload.get("correct_answer"),
                        "correct_reasoning": unit_payload.get("correct_reasoning"),
                        "source_refs": unit_payload.get("source_refs") or block.due_reason and [block.due_reason] or [],
                        "linked_asset_ids": [unit_payload.get("asset_id")] if unit_payload.get("asset_id") else [],
                    },
                    reveal_keys=["correct_answer", "correct_reasoning"],
                )
            )
        except Exception as exc:
            return {
                "adapter": "review_lab",
                "prompt": block.description or block.title,
                "next_action": "Confirm source-backed assets or generate a daily review before starting Review Lab.",
                "_blocked_reason": f"No confirmed Review Lab unit is ready: {exc}",
                "source_refs": [],
            }

    def _formula_payload(self, profile_id: str, block: StudyPlanBlock) -> dict[str, Any]:
        try:
            session = self.review.generate_formula_lab_session(profile_id=profile_id, max_units=1)
            unit = session.current_unit or (session.units[0] if session.units else None)
            if unit is None:
                raise ValueError("No confirmed formula assets are ready.")
            payload = unit.as_dict()
            return _safe_payload(
                _local_reveal_payload(
                    {
                        "adapter": "formula_lab",
                        "session_id": session.session_id,
                        "unit_id": unit.unit_id,
                        "prompt": payload.get("front_prompt") or payload.get("prompt"),
                        "display_mode": payload.get("display_mode"),
                        "correct_answer": payload.get("correct_answer"),
                        "correct_reasoning": payload.get("correct_reasoning"),
                        "formula_latex": payload.get("formula_latex"),
                        "variables": payload.get("variables") or [],
                        "ba_ii_plus_steps": payload.get("ba_ii_plus_steps") or [],
                        "source_refs": payload.get("source_refs") or [],
                        "linked_asset_ids": [payload.get("asset_id")] if payload.get("asset_id") else block.linked_asset_ids[:1],
                    },
                    reveal_keys=["correct_answer", "correct_reasoning", "formula_latex", "variables", "ba_ii_plus_steps"],
                )
            )
        except Exception as exc:
            return {
                "adapter": "formula_lab",
                "prompt": block.description or block.title,
                "next_action": "Confirm a formula asset with source refs before using Formula Lab.",
                "_blocked_reason": f"No confirmed formula unit is ready: {exc}",
                "source_refs": [],
            }

    def _lexical_payload(self, profile_id: str, block: StudyPlanBlock) -> dict[str, Any]:
        try:
            from language_science.lexical_kernel import LexicalKernel

            kernel = LexicalKernel(self.repo_root)
            session = kernel.generate_review_session(profile_id=profile_id, max_units=1)
            unit = session.units[0] if session.units else None
            if unit is None:
                raise ValueError("No confirmed lexical assets are ready.")
            payload = unit.as_dict()
            return _safe_payload(
                _local_reveal_payload(
                    {
                        "adapter": "lexical_review",
                        "session_id": session.session_id,
                        "unit_id": unit.unit_id,
                        "prompt": payload.get("front_prompt"),
                        "display_mode": payload.get("display_mode"),
                        "correct_answer": payload.get("correct_answer"),
                        "correct_reasoning": payload.get("correct_reasoning"),
                        "headword": payload.get("headword"),
                        "translation": payload.get("translation"),
                        "example_sentence": payload.get("example_sentence"),
                        "collocations": payload.get("collocations") or [],
                        "source_refs": payload.get("source_refs") or [],
                        "linked_lexical_ids": [payload.get("lexical_id")] if payload.get("lexical_id") else block.linked_lexical_ids[:1],
                    },
                    reveal_keys=["correct_answer", "correct_reasoning", "translation", "example_sentence", "collocations"],
                )
            )
        except Exception as exc:
            return {
                "adapter": "lexical_review",
                "prompt": block.description or block.title,
                "next_action": "Confirm a dictionary and lexical asset before using LanguageOS review.",
                "_blocked_reason": f"No confirmed lexical unit is ready: {exc}",
                "source_refs": [],
            }

    def _complete_embedded_adapter(self, step: FocusStep, *, outcome: str, actual_minutes: int | None) -> None:
        payload = step.embedded_payload
        adapter = str(payload.get("adapter") or "")
        normalized = _normalize_outcome(outcome)
        if payload.get("study_block_id"):
            try:
                self.planner.complete_block(
                    str(payload["study_block_id"]),
                    outcome=step.completion_outcome or _outcome_label(normalized),
                    actual_minutes=actual_minutes,
                )
            except Exception:
                pass
        if adapter in {"review_lab", "formula_lab"} and payload.get("unit_id"):
            try:
                from study_science.review_lab_models import ReviewUnitOutcome

                review_outcome = ReviewUnitOutcome(
                    unit_id=str(payload["unit_id"]),
                    outcome=normalized,  # type: ignore[arg-type]
                    time_spent_seconds=max(0, int(actual_minutes or step.target_minutes) * 60),
                    confidence_after=3 if normalized == "recalled" else 2,
                    answer_quality="perfect" if normalized == "recalled" else "minor_gap",
                )
                self.review.submit_unit_completion(
                    str(payload["unit_id"]),
                    review_outcome,
                    session_id=str(payload.get("session_id") or ""),
                )
            except Exception:
                pass
        if adapter == "lexical_review" and payload.get("unit_id"):
            try:
                from language_science.lexical_kernel import LexicalKernel

                LexicalKernel(self.repo_root).complete_review_unit(
                    str(payload["unit_id"]),
                    session_id=str(payload.get("session_id") or ""),
                    outcome=normalized,
                    time_spent_seconds=max(0, int(actual_minutes or step.target_minutes) * 60),
                )
            except Exception:
                pass

    def _skip_plan_block(self, step: FocusStep, *, reason: str) -> None:
        block_id = step.embedded_payload.get("study_block_id")
        if not block_id:
            return
        try:
            self.planner.skip_block(str(block_id), reason=reason)
        except Exception:
            pass

    def _summary(self, steps: list[FocusStep]) -> dict[str, Any]:
        statuses = {status: sum(1 for step in steps if step.status == status) for status in ["pending", "in_progress", "completed", "skipped", "blocked"]}
        types: dict[str, int] = {}
        for step in steps:
            types[step.step_type] = types.get(step.step_type, 0) + 1
        return {
            "total_steps": len(steps),
            "completed_steps": statuses["completed"],
            "skipped_steps": statuses["skipped"],
            "blocked_steps": statuses["blocked"],
            "pending_steps": statuses["pending"],
            "in_progress_steps": statuses["in_progress"],
            "target_minutes": sum(step.target_minutes for step in steps),
            "completed_minutes": sum(step.target_minutes for step in steps if step.status == "completed"),
            "status_counts": statuses,
            "step_type_counts": types,
            "correct_only": True,
        }

    def _maybe_complete_session(self, session: FocusSession) -> None:
        if not session.current_step_id and all(step.status in {"completed", "skipped", "blocked"} for step in session.steps):
            session.status = "completed"
            session.completed_at = session.completed_at or _now()

    def _touch_and_persist(self, session: FocusSession) -> FocusSession:
        session.updated_at = _now()
        session.total_target_minutes = sum(step.target_minutes for step in session.steps)
        session.summary = self._summary(session.steps) | {
            key: value
            for key, value in session.summary.items()
            if key in {"abandon_reason"}
        }
        self._persist(session)
        if session.status == "active":
            self._write_latest(session)
        return session

    def _persist(self, session: FocusSession) -> None:
        self._session_path(session.focus_id).write_text(
            json.dumps(session.as_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _write_latest(self, session: FocusSession) -> None:
        self._latest_path(session.profile_id).write_text(session.focus_id, encoding="utf-8")

    def _persist_latest_if_current_abandoned(self, session: FocusSession) -> None:
        latest = self._latest_path(session.profile_id)
        if latest.exists() and latest.read_text(encoding="utf-8").strip() == session.focus_id:
            latest.unlink()

    def _read_sessions(self) -> list[FocusSession]:
        sessions = []
        for path in self.session_root.glob("*.json"):
            try:
                sessions.append(FocusSession.from_dict(json.loads(path.read_text(encoding="utf-8"))))
            except Exception:
                continue
        return sessions

    def _session_path(self, focus_id: str) -> Path:
        return self.session_root / f"{focus_id}.json"

    def _latest_path(self, profile_id: str) -> Path:
        return self.latest_root / f"{_stable_id('latest-focus', profile_id)}.txt"

    def _require_session(self, focus_id: str) -> FocusSession:
        session = self.get(focus_id)
        if session is None:
            raise KeyError(focus_id)
        return session


def _step_type_for_block(block_type: str) -> FocusStepType:
    return {
        "review_lab": "review_lab",
        "formula_lab": "formula_lab",
        "lexical_review": "lexical_review",
        "coverage_gap": "coverage_confirmation",
        "mock_transfer_drill": "assessment",
        "resource_confirmation": "resource_confirmation",
        "asset_confirmation": "coverage_confirmation",
        "file_ingestion_cleanup": "resource_confirmation",
        "mission_control_review": "tutor_hint",
        "reflection": "reflection",
    }.get(str(block_type), "reflection")  # type: ignore[return-value]


def _step_title(block: StudyPlanBlock, step_type: FocusStepType) -> str:
    if step_type == "coverage_confirmation" and block.block_type == "asset_confirmation":
        return "Confirm assets before recall"
    if step_type == "resource_confirmation":
        return "Confirm resources before recall"
    return block.title or {
        "review_lab": "Review Lab recall",
        "formula_lab": "Formula recall",
        "lexical_review": "Lexical recall",
        "assessment": "Transfer check",
        "tutor_hint": "Tutor hint",
        "coverage_confirmation": "Coverage confirmation",
        "resource_confirmation": "Resource confirmation",
        "reflection": "Reflection",
    }[step_type]


def _step_description(block: StudyPlanBlock, step_type: FocusStepType) -> str:
    if step_type == "coverage_confirmation" and block.block_type == "asset_confirmation":
        return "Confirm draft or needs-review assets before they can be used as recall content."
    if step_type == "resource_confirmation":
        return "Confirm resources and quality gates before promotion into review."
    return block.description


def _launch_route_for_step(step_type: FocusStepType, fallback: str) -> str | None:
    return {
        "review_lab": "/review/lab",
        "formula_lab": "/review/formulas",
        "lexical_review": "/language/review",
        "assessment": "/review/assessments",
        "tutor_hint": "/review/tutor",
        "coverage_confirmation": fallback or "/review/assets",
        "resource_confirmation": fallback or "/review/resources",
        "reflection": "/review/mission-control",
    }[step_type]


def _correct_only_warning(step_type: FocusStepType) -> str:
    return {
        "review_lab": "Recall first. The correct answer is hidden until reveal; prior wrong answers are never shown.",
        "formula_lab": "Formula feedback is correct-only and calculator steps stay hidden until reveal.",
        "lexical_review": "Lexical review uses confirmed dictionary assets only.",
        "assessment": "Assessment feedback should use correct rules only.",
        "tutor_hint": "Tutor hints cite confirmed local evidence and avoid raw diagnostics.",
        "coverage_confirmation": "Draft or unconfirmed assets must be confirmed before recall.",
        "resource_confirmation": "Resources must pass quality gates before promotion.",
        "reflection": "Reflection records outcomes without exposing raw wrong-answer text.",
    }[step_type]


def _trusted_asset_ids(asset_ids: list[str], engine: ReviewLabEngine) -> list[str]:
    asset_index = {
        str(asset.get("asset_id")): asset
        for asset in engine.list_ingested_assets()
        if asset.get("asset_id")
    }
    trusted = []
    for asset_id in asset_ids:
        asset = asset_index.get(asset_id)
        if asset is None:
            trusted.append(asset_id)
            continue
        if str(asset.get("validation_status") or "") in TRUSTED_ASSET_STATUSES:
            trusted.append(asset_id)
    return _unique(trusted)


def _next_step_id(steps: list[FocusStep], *, after_step_id: str | None = None) -> str | None:
    start_index = 0
    if after_step_id:
        for index, step in enumerate(steps):
            if step.step_id == after_step_id:
                start_index = index + 1
                break
    for step in steps[start_index:]:
        if step.status in {"pending", "in_progress"}:
            return step.step_id
    for step in steps:
        if step.status in {"pending", "in_progress"}:
            return step.step_id
    return None


def _fit_focus_minutes(steps: list[FocusStep], available_minutes: int) -> None:
    total = sum(step.target_minutes for step in steps)
    if not available_minutes or total <= available_minutes:
        return
    overflow = total - available_minutes
    for step in sorted(steps, key=lambda item: item.target_minutes, reverse=True):
        reducible = max(0, step.target_minutes - 5)
        reduction = min(reducible, overflow)
        step.target_minutes -= reduction
        overflow -= reduction
        if overflow <= 0:
            break


def _balance_step_sequence(steps: list[FocusStep]) -> list[FocusStep]:
    remaining = list(steps)
    balanced: list[FocusStep] = []
    while remaining:
        blocked_type = None
        if len(balanced) >= 2 and balanced[-1].step_type == balanced[-2].step_type:
            blocked_type = balanced[-1].step_type
        index = 0
        if blocked_type is not None:
            index = next(
                (candidate_index for candidate_index, step in enumerate(remaining) if step.step_type != blocked_type),
                0,
            )
        balanced.append(remaining.pop(index))
    return balanced


def _require_step(session: FocusSession, step_id: str) -> FocusStep:
    step = next((item for item in session.steps if item.step_id == step_id), None)
    if step is None:
        raise KeyError(step_id)
    return step


def _normalize_outcome(outcome: str) -> str:
    return outcome if outcome in {"recalled", "partial", "forgot", "skipped"} else "recalled"


def _outcome_label(outcome: str) -> str:
    return {
        "recalled": "Completed with recall",
        "partial": "Completed with a partial gap",
        "forgot": "Completed after reveal",
        "skipped": "Skipped",
    }.get(_normalize_outcome(outcome), "Completed")


def _safe_payload(payload: dict[str, Any]) -> dict[str, Any]:
    sanitized, _ = sanitize_payload(payload)
    return sanitized


def _local_reveal_payload(payload: dict[str, Any], *, reveal_keys: list[str]) -> dict[str, Any]:
    reveal_payload: dict[str, Any] = {}
    for key in reveal_keys:
        if key in payload:
            value = payload.pop(key)
            if value not in (None, "", [], {}):
                reveal_payload[key] = value
    if payload.get("source_refs"):
        reveal_payload["source_refs"] = list(payload.get("source_refs") or [])
    payload["answer_hidden_until_reveal"] = True
    payload["local_reveal_available"] = True
    payload["reveal_payload"] = _safe_payload(reveal_payload)
    return payload


def _unique(items: list[Any]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item is None:
            continue
        text = str(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return ordered


def _stable_id(prefix: str, *parts: Any) -> str:
    text = "|".join(str(part) for part in parts)
    return f"{prefix}-{sha1(text.encode('utf-8')).hexdigest()[:16]}"


def _now() -> str:
    return datetime.now(UTC).isoformat()
