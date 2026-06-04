"""Adaptive study planner and session orchestrator.

The planner converts existing correct-only learning signals into a local,
time-boxed plan. It stores plans as JSON under `.system/memory/study-planner`
and deliberately avoids raw wrong-answer fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from hashlib import sha1
import json
from pathlib import Path
from typing import Any, Callable, Literal

from study_science.mission_control import MissionControlService
from study_science.review_lab import ReviewLabEngine


EnergyMode = Literal["low", "normal", "high"]
PlanStatus = Literal["draft", "active", "completed", "archived"]
BlockStatus = Literal["pending", "in_progress", "completed", "skipped", "blocked"]
BlockType = Literal[
    "review_lab",
    "formula_lab",
    "lexical_review",
    "coverage_gap",
    "mock_transfer_drill",
    "resource_confirmation",
    "asset_confirmation",
    "file_ingestion_cleanup",
    "mission_control_review",
    "reflection",
]


ENERGY_MIX: dict[EnergyMode, list[tuple[str, float, int]]] = {
    "low": [
        ("review_lab", 0.40, 1),
        ("recall_light", 0.20, 1),
        ("cleanup", 0.20, 1),
        ("reflection", 0.20, 1),
    ],
    "normal": [
        ("review_lab", 0.35, 1),
        ("formula_lab", 0.20, 1),
        ("coverage_gap", 0.15, 1),
        ("mock_transfer_drill", 0.15, 1),
        ("lexical_review", 0.10, 1),
        ("confirmation", 0.05, 1),
    ],
    "high": [
        ("review_lab", 0.25, 1),
        ("formula_lab", 0.20, 1),
        ("coverage_gap", 0.20, 2),
        ("mock_transfer_drill", 0.15, 1),
        ("lexical_review", 0.10, 1),
        ("cleanup", 0.10, 2),
    ],
}

CATEGORY_TYPES: dict[str, set[str]] = {
    "review_lab": {"review_lab"},
    "recall_light": {"formula_lab", "lexical_review"},
    "formula_lab": {"formula_lab"},
    "coverage_gap": {"coverage_gap"},
    "mock_transfer_drill": {"mock_transfer_drill"},
    "lexical_review": {"lexical_review"},
    "confirmation": {"resource_confirmation", "asset_confirmation"},
    "cleanup": {"resource_confirmation", "asset_confirmation", "file_ingestion_cleanup"},
    "reflection": {"reflection"},
}

WRONG_FIELD_NAMES = {"wrong_choice_or_output", "wrong_formula", "wrong_reasoning"}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _today() -> str:
    return date.today().isoformat()


def _stable_id(prefix: str, *parts: Any) -> str:
    text = "|".join(str(part) for part in parts)
    return f"{prefix}-{sha1(text.encode('utf-8')).hexdigest()[:16]}"


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


@dataclass
class StudyPlanBlock:
    block_id: str
    plan_id: str
    block_type: BlockType
    title: str
    description: str
    target_minutes: int
    priority: float
    launch_route: str
    due_reason: str
    linked_asset_ids: list[str] = field(default_factory=list)
    linked_topic_ids: list[str] = field(default_factory=list)
    linked_gap_ids: list[str] = field(default_factory=list)
    linked_resource_ids: list[str] = field(default_factory=list)
    linked_lexical_ids: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    blocked_reason: str | None = None
    status: BlockStatus = "pending"
    completion_outcome: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "block_id": self.block_id,
            "plan_id": self.plan_id,
            "block_type": self.block_type,
            "title": self.title,
            "description": self.description,
            "target_minutes": self.target_minutes,
            "priority": self.priority,
            "launch_route": self.launch_route,
            "due_reason": self.due_reason,
            "linked_asset_ids": self.linked_asset_ids,
            "linked_topic_ids": self.linked_topic_ids,
            "linked_gap_ids": self.linked_gap_ids,
            "linked_resource_ids": self.linked_resource_ids,
            "linked_lexical_ids": self.linked_lexical_ids,
            "prerequisites": self.prerequisites,
            "blocked_reason": self.blocked_reason,
            "status": self.status,
            "completion_outcome": self.completion_outcome,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> StudyPlanBlock:
        return cls(
            block_id=str(payload.get("block_id", "")),
            plan_id=str(payload.get("plan_id", "")),
            block_type=str(payload.get("block_type", "reflection")),  # type: ignore[arg-type]
            title=str(payload.get("title", "")),
            description=str(payload.get("description", "")),
            target_minutes=int(payload.get("target_minutes", 0) or 0),
            priority=float(payload.get("priority", 0.0) or 0.0),
            launch_route=str(payload.get("launch_route", "")),
            due_reason=str(payload.get("due_reason", "")),
            linked_asset_ids=list(payload.get("linked_asset_ids") or []),
            linked_topic_ids=list(payload.get("linked_topic_ids") or []),
            linked_gap_ids=list(payload.get("linked_gap_ids") or []),
            linked_resource_ids=list(payload.get("linked_resource_ids") or []),
            linked_lexical_ids=list(payload.get("linked_lexical_ids") or []),
            prerequisites=list(payload.get("prerequisites") or []),
            blocked_reason=payload.get("blocked_reason"),
            status=str(payload.get("status", "pending")),  # type: ignore[arg-type]
            completion_outcome=payload.get("completion_outcome"),
        )


@dataclass
class StudyPlan:
    plan_id: str
    profile_id: str
    plan_date: str
    energy_mode: EnergyMode
    available_minutes: int
    goal: str | None
    generated_at: str
    status: PlanStatus
    blocks: list[StudyPlanBlock]
    summary: dict[str, Any]
    source_signals: dict[str, Any]
    recommended_next_actions: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "profile_id": self.profile_id,
            "plan_date": self.plan_date,
            "energy_mode": self.energy_mode,
            "available_minutes": self.available_minutes,
            "goal": self.goal,
            "generated_at": self.generated_at,
            "status": self.status,
            "blocks": [block.as_dict() for block in self.blocks],
            "summary": self.summary,
            "source_signals": self.source_signals,
            "recommended_next_actions": self.recommended_next_actions,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> StudyPlan:
        return cls(
            plan_id=str(payload.get("plan_id", "")),
            profile_id=str(payload.get("profile_id", "default")),
            plan_date=str(payload.get("plan_date", _today())),
            energy_mode=str(payload.get("energy_mode", "normal")),  # type: ignore[arg-type]
            available_minutes=int(payload.get("available_minutes", 0) or 0),
            goal=payload.get("goal"),
            generated_at=str(payload.get("generated_at", "")),
            status=str(payload.get("status", "draft")),  # type: ignore[arg-type]
            blocks=[StudyPlanBlock.from_dict(block) for block in payload.get("blocks", [])],
            summary=dict(payload.get("summary") or {}),
            source_signals=dict(payload.get("source_signals") or {}),
            recommended_next_actions=list(payload.get("recommended_next_actions") or []),
        )


class StudyPlannerService:
    """Build and manage executable daily study plans."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.root = self.repo_root / ".system" / "memory" / "study-planner"
        self.plan_root = self.root / "plans"
        self.latest_root = self.root / "latest"
        for path in (self.plan_root, self.latest_root):
            path.mkdir(parents=True, exist_ok=True)
        self.engine = ReviewLabEngine(self.repo_root)

    def generate_plan(
        self,
        *,
        profile_id: str = "default",
        energy_mode: EnergyMode = "normal",
        available_minutes: int = 90,
        goal: str | None = None,
        plan_date: str | None = None,
    ) -> StudyPlan:
        profile_id = profile_id or "default"
        plan_date = plan_date or _today()
        if energy_mode not in ENERGY_MIX:
            raise ValueError(f"Unsupported energy mode: {energy_mode}")
        if available_minutes < 10:
            raise ValueError("available_minutes must be at least 10.")

        plan_id = _stable_id("study-plan", profile_id, plan_date, energy_mode, available_minutes, goal or "")
        source_signals, candidates = self._collect_candidates(
            profile_id=profile_id,
            plan_id=plan_id,
            goal=goal or "",
        )
        blocks = self._compose_blocks(
            plan_id=plan_id,
            candidates=candidates,
            energy_mode=energy_mode,
            available_minutes=available_minutes,
        )
        if not blocks:
            blocks = self._default_blocks(plan_id=plan_id, available_minutes=available_minutes)

        plan = StudyPlan(
            plan_id=plan_id,
            profile_id=profile_id,
            plan_date=plan_date,
            energy_mode=energy_mode,
            available_minutes=available_minutes,
            goal=goal.strip() if isinstance(goal, str) and goal.strip() else None,
            generated_at=_now(),
            status="draft",
            blocks=blocks,
            summary=self._summarize(blocks, available_minutes=available_minutes),
            source_signals=source_signals,
            recommended_next_actions=self._next_actions(blocks, completed=False),
        )
        self._persist_plan(plan)
        self._write_latest(profile_id, plan_date, plan.plan_id)
        return plan

    def today(self, *, profile_id: str = "default", plan_date: str | None = None) -> StudyPlan:
        profile_id = profile_id or "default"
        plan_date = plan_date or _today()
        latest = self._latest_path(profile_id, plan_date)
        if latest.exists():
            plan_id = latest.read_text(encoding="utf-8").strip()
            loaded = self.get_plan(plan_id)
            if loaded is not None:
                return loaded
        return self.generate_plan(profile_id=profile_id, plan_date=plan_date, energy_mode="normal", available_minutes=90)

    def get_plan(self, plan_id: str) -> StudyPlan | None:
        path = self._plan_path(plan_id)
        if not path.exists():
            return None
        return StudyPlan.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def activate_plan(self, plan_id: str) -> StudyPlan:
        plan = self._require_plan(plan_id)
        if plan.status not in {"completed", "archived"}:
            plan.status = "active"
        plan.summary = self._summarize(plan.blocks, available_minutes=plan.available_minutes)
        self._persist_plan(plan)
        return plan

    def start_block(self, block_id: str) -> tuple[StudyPlan, StudyPlanBlock]:
        plan, block = self._require_block(block_id)
        if block.status == "blocked":
            raise ValueError(block.blocked_reason or "Block is blocked.")
        if block.status == "pending":
            block.status = "in_progress"
            if plan.status == "draft":
                plan.status = "active"
        plan.summary = self._summarize(plan.blocks, available_minutes=plan.available_minutes)
        self._persist_plan(plan)
        return plan, block

    def complete_block(self, block_id: str, *, outcome: str = "", actual_minutes: int | None = None) -> tuple[StudyPlan, StudyPlanBlock]:
        plan, block = self._require_block(block_id)
        if block.status == "blocked":
            raise ValueError(block.blocked_reason or "Block is blocked.")
        block.status = "completed"
        minutes_note = f" ({actual_minutes} actual minutes)" if actual_minutes is not None else ""
        block.completion_outcome = (outcome.strip() or "completed") + minutes_note
        plan.summary = self._summarize(plan.blocks, available_minutes=plan.available_minutes)
        plan.recommended_next_actions = self._next_actions(plan.blocks, completed=False)
        self._persist_plan(plan)
        return plan, block

    def skip_block(self, block_id: str, *, reason: str = "") -> tuple[StudyPlan, StudyPlanBlock]:
        plan, block = self._require_block(block_id)
        block.status = "skipped"
        block.completion_outcome = f"Skipped: {reason.strip() or 'No reason provided.'}"
        plan.summary = self._summarize(plan.blocks, available_minutes=plan.available_minutes)
        plan.recommended_next_actions = self._next_actions(plan.blocks, completed=False)
        self._persist_plan(plan)
        return plan, block

    def complete_plan(self, plan_id: str) -> StudyPlan:
        plan = self._require_plan(plan_id)
        plan.status = "completed"
        plan.summary = self._summarize(plan.blocks, available_minutes=plan.available_minutes)
        plan.summary["retro"] = {
            "completed_at": _now(),
            "follow_up_count": sum(1 for block in plan.blocks if block.status in {"skipped", "blocked"}),
            "outcomes": [
                {"block_id": block.block_id, "status": block.status, "outcome": block.completion_outcome}
                for block in plan.blocks
                if block.completion_outcome
            ],
        }
        plan.recommended_next_actions = self._next_actions(plan.blocks, completed=True)
        self._persist_plan(plan)
        return plan

    def history(self, *, profile_id: str = "default", limit: int = 50) -> list[dict[str, Any]]:
        plans: list[StudyPlan] = []
        for path in self.plan_root.glob("*.json"):
            try:
                plan = StudyPlan.from_dict(json.loads(path.read_text(encoding="utf-8")))
            except Exception:
                continue
            if plan.profile_id in {profile_id or "default", "default"}:
                plans.append(plan)
        plans.sort(key=lambda plan: plan.generated_at, reverse=True)
        return [plan.as_dict() for plan in plans[:limit]]

    def _collect_candidates(
        self,
        *,
        profile_id: str,
        plan_id: str,
        goal: str,
    ) -> tuple[dict[str, Any], list[StudyPlanBlock]]:
        mission = MissionControlService(self.repo_root)
        has_syllabus_topics = bool(self._safe(lambda: self.engine.list_syllabus_topics(profile_id=profile_id), []))
        mission_summary = self._safe(lambda: mission.summary(profile_id=profile_id), {})
        candidates: list[StudyPlanBlock] = []

        review_payload = self._safe(lambda: self.engine.get_today_units(max_units=30), {"units": []})
        review_units = list(review_payload.get("units") or [])
        if review_units:
            candidates.append(
                self._candidate(
                    plan_id=plan_id,
                    block_type="review_lab",
                    title="Review Lab correct-only recall",
                    description="Run today's recall-first Review Lab units.",
                    launch_route="/review/lab",
                    due_reason=f"{len(review_units)} correct-only units are due from DailyReview and confirmed assets.",
                    linked_asset_ids=self._ids(review_units, "asset_id", 12),
                    priority=self._priority(
                        urgency=1.0,
                        exam_weight=0.75,
                        memory_decay=0.9,
                        source_quality=1.0,
                        user_goal_alignment=self._goal_alignment(goal, "review recall daily"),
                    ),
                )
            )

        self._add_asset_and_formula_candidates(candidates, plan_id=plan_id, profile_id=profile_id, goal=goal)
        self._add_coverage_candidates(
            candidates,
            plan_id=plan_id,
            profile_id=profile_id,
            goal=goal,
            has_syllabus_topics=has_syllabus_topics,
        )
        self._add_transfer_gap_candidates(candidates, plan_id=plan_id, profile_id=profile_id, goal=goal)
        self._add_resource_candidates(candidates, plan_id=plan_id, profile_id=profile_id, goal=goal)
        self._add_language_candidates(candidates, plan_id=plan_id, profile_id=profile_id, goal=goal)
        self._add_file_cleanup_candidates(candidates, plan_id=plan_id, profile_id=profile_id)

        source_signals = {
            "mission_control": self._sanitize_mission_summary(mission_summary),
            "candidate_block_count": len(candidates),
            "priority_formula": (
                "0.24*urgency + 0.18*exam_weight + 0.16*memory_decay + "
                "0.14*transfer_gap_severity + 0.10*coverage_gap_value + "
                "0.08*formula_or_language_value + 0.06*source_quality + 0.04*user_goal_alignment"
            ),
            "safety": {
                "correct_only": True,
                "draft_content_enters_review": False,
                "ocr_enabled": False,
            },
        }
        return source_signals, candidates

    def _add_asset_and_formula_candidates(
        self,
        candidates: list[StudyPlanBlock],
        *,
        plan_id: str,
        profile_id: str,
        goal: str,
    ) -> None:
        assets = self._safe(lambda: self.engine.list_ingested_assets(profile_id=profile_id), [])
        draft_assets = [
            asset for asset in assets
            if asset.get("validation_status") in {"draft", "needs_review"}
        ]
        if draft_assets:
            candidates.append(
                self._candidate(
                    plan_id=plan_id,
                    block_type="asset_confirmation",
                    title="Confirm source-backed draft assets",
                    description="Review draft candidates before they can enter recall.",
                    launch_route="/review/assets",
                    due_reason=(
                        f"{len(draft_assets)} draft/needs-review assets are not used as review content "
                        "until manually confirmed."
                    ),
                    linked_asset_ids=self._ids(draft_assets, "asset_id", 12),
                    prerequisites=["Manual confirmation", "Source refs required"],
                    priority=self._priority(
                        urgency=0.72,
                        coverage_gap_value=0.45,
                        source_quality=0.55,
                        user_goal_alignment=self._goal_alignment(goal, "asset confirm source"),
                    ),
                )
            )

        formulas = self._safe(lambda: self.engine.list_formula_assets(profile_id=profile_id), [])
        confirmed = [
            item for item in formulas
            if item.get("validation_status") in {"confirmed", "validated", "derived"}
            and item.get("source_refs")
        ]
        if confirmed:
            weak_count = sum(1 for item in confirmed if str(item.get("mastery_state", "")).lower() in {"", "new", "learning", "weak"})
            candidates.append(
                self._candidate(
                    plan_id=plan_id,
                    block_type="formula_lab",
                    title="Formula Lab and calculator drill",
                    description="Recall formulas and reinforce BA II Plus procedure gaps.",
                    launch_route="/review/formulas",
                    due_reason=f"{len(confirmed)} confirmed formula assets are eligible; {weak_count} look weak or new.",
                    linked_asset_ids=self._ids(confirmed, "asset_id", 10),
                    priority=self._priority(
                        urgency=0.78,
                        exam_weight=0.8,
                        memory_decay=0.75,
                        formula_or_language_value=1.0,
                        source_quality=self._avg(confirmed, "source_quality", default=0.8),
                        user_goal_alignment=self._goal_alignment(goal, "formula wacc calculator"),
                    ),
                )
            )

        draft_formula_ids = [
            str(item.get("asset_id"))
            for item in formulas
            if item.get("validation_status") in {"draft", "needs_review"}
        ]
        if draft_formula_ids:
            candidates.append(
                self._candidate(
                    plan_id=plan_id,
                    block_type="asset_confirmation",
                    title="Confirm draft formula candidates",
                    description="Validate formula metadata, source refs, and calculator steps.",
                    launch_route="/review/formulas",
                    due_reason="Draft formula assets are not used as review content until confirmed.",
                    linked_asset_ids=draft_formula_ids[:10],
                    prerequisites=["Confirm source-backed formula"],
                    priority=self._priority(
                        urgency=0.65,
                        formula_or_language_value=0.9,
                        source_quality=0.45,
                        user_goal_alignment=self._goal_alignment(goal, "formula confirm"),
                    ),
                )
            )

    def _add_coverage_candidates(
        self,
        candidates: list[StudyPlanBlock],
        *,
        plan_id: str,
        profile_id: str,
        goal: str,
        has_syllabus_topics: bool,
    ) -> None:
        if not has_syllabus_topics:
            return
        coverage = self._safe(lambda: self.engine.recompute_syllabus_coverage(profile_id=profile_id), {"records": []})
        gap_records = [
            record for record in coverage.get("records", [])
            if record.get("coverage_status") in {"missing", "partial", "weak", "stale", "draft_only"}
        ]
        non_draft_gaps = [record for record in gap_records if record.get("coverage_status") != "draft_only"]
        if non_draft_gaps:
            top = non_draft_gaps[:5]
            candidates.append(
                self._candidate(
                    plan_id=plan_id,
                    block_type="coverage_gap",
                    title="Close highest-value coverage gaps",
                    description="Use the coverage audit to create or import source-backed assets.",
                    launch_route="/review/coverage",
                    due_reason=f"{len(non_draft_gaps)} syllabus gaps are missing, partial, weak, or stale.",
                    linked_topic_ids=self._ids(top, "topic_id", 5),
                    priority=self._priority(
                        urgency=0.7,
                        exam_weight=self._avg([record.get("topic", {}) for record in top], "exam_weight", default=0.6),
                        coverage_gap_value=1.0,
                        source_quality=0.6,
                        user_goal_alignment=self._goal_alignment(goal, "coverage syllabus topic"),
                    ),
                )
            )

        draft_only = [record for record in gap_records if record.get("coverage_status") == "draft_only"]
        if draft_only:
            asset_ids = []
            for record in draft_only[:5]:
                asset_ids.extend(self._ids(record.get("linked_assets", []), "asset_id", 5))
            candidates.append(
                self._candidate(
                    plan_id=plan_id,
                    block_type="asset_confirmation",
                    title="Unblock draft-only coverage",
                    description="Confirm or reject draft assets behind draft-only syllabus coverage.",
                    launch_route="/review/assets",
                    due_reason="Draft-only coverage is blocked and not used as review content.",
                    linked_topic_ids=self._ids(draft_only, "topic_id", 5),
                    linked_asset_ids=asset_ids[:10],
                    prerequisites=["Manual confirmation"],
                    priority=self._priority(
                        urgency=0.62,
                        exam_weight=0.7,
                        coverage_gap_value=0.85,
                        source_quality=0.45,
                        user_goal_alignment=self._goal_alignment(goal, "coverage confirm draft"),
                    ),
                )
            )

    def _add_transfer_gap_candidates(
        self,
        candidates: list[StudyPlanBlock],
        *,
        plan_id: str,
        profile_id: str,
        goal: str,
    ) -> None:
        gaps = self._safe(lambda: self.engine.list_transfer_gaps(profile_id=profile_id, status="open"), [])
        if not gaps:
            return
        severity = max(float(gap.get("severity", 0.0) or 0.0) for gap in gaps)
        candidates.append(
            self._candidate(
                plan_id=plan_id,
                block_type="mock_transfer_drill",
                title="Mock transfer gap drill",
                description="Practice the open transfer gaps created from sanitized mock retro evidence.",
                launch_route="/review/mock-retro",
                due_reason=f"{len(gaps)} open transfer gaps remain; highest severity {severity:.2f}.",
                linked_gap_ids=self._ids(gaps, "gap_id", 8),
                priority=self._priority(
                    urgency=0.78,
                    exam_weight=0.82,
                    transfer_gap_severity=severity,
                    formula_or_language_value=0.5,
                    source_quality=0.8,
                    user_goal_alignment=self._goal_alignment(goal, "mock transfer drill"),
                ),
            )
        )

    def _add_resource_candidates(
        self,
        candidates: list[StudyPlanBlock],
        *,
        plan_id: str,
        profile_id: str,
        goal: str,
    ) -> None:
        resources = self._safe(lambda: self.engine.list_resources(profile_id=profile_id), [])
        pending = [
            resource for resource in resources
            if resource.get("validation_status") in {"draft", "needs_review"}
            or resource.get("quality_status") in {"unscored", "low", "medium"}
        ]
        if not pending:
            return
        blocked = [resource for resource in pending if resource.get("quality_status") in {"unscored", "low"}]
        candidates.append(
            self._candidate(
                plan_id=plan_id,
                block_type="resource_confirmation",
                title="ResourceOS confirmation and quality gate",
                description="Score, confirm, or fix resources before promoting candidates.",
                launch_route="/review/resources",
                due_reason=f"{len(pending)} resources need quality-gate or confirmation work.",
                linked_resource_ids=self._ids(pending, "resource_id", 8),
                prerequisites=["Resource quality gate must pass before review promotion"],
                blocked_reason=(
                    f"{len(blocked)} resources have unscored/low quality gates."
                    if blocked else None
                ),
                priority=self._priority(
                    urgency=0.58,
                    coverage_gap_value=0.4,
                    source_quality=0.35 if blocked else 0.6,
                    user_goal_alignment=self._goal_alignment(goal, "resource confirm quality"),
                ),
            )
        )

    def _add_language_candidates(
        self,
        candidates: list[StudyPlanBlock],
        *,
        plan_id: str,
        profile_id: str,
        goal: str,
    ) -> None:
        try:
            from language_science.lexical_kernel import LexicalKernel
        except ImportError:
            return
        kernel = LexicalKernel(self.repo_root)
        lexical = self._safe(lambda: kernel.list_lexical_assets(profile_id=profile_id), [])
        confirmed = [
            item for item in lexical
            if item.get("validation_status") == "confirmed"
        ]
        if confirmed:
            candidates.append(
                self._candidate(
                    plan_id=plan_id,
                    block_type="lexical_review",
                    title="LanguageOS lexical recall",
                    description="Run due confirmed lexical items through the LanguageOS review loop.",
                    launch_route="/language/review",
                    due_reason=f"{len(confirmed)} confirmed lexical items are eligible for review.",
                    linked_lexical_ids=self._ids(confirmed, "lexical_id", 10),
                    priority=self._priority(
                        urgency=0.62,
                        memory_decay=0.65,
                        formula_or_language_value=1.0,
                        source_quality=0.8,
                        user_goal_alignment=self._goal_alignment(goal, "language lexical dictionary"),
                    ),
                )
            )
        draft = [
            item for item in lexical
            if item.get("validation_status") in {"draft", "needs_review"}
        ]
        if draft:
            candidates.append(
                self._candidate(
                    plan_id=plan_id,
                    block_type="asset_confirmation",
                    title="Confirm LanguageOS lexical assets",
                    description="Confirm dictionary-backed lexical items before review.",
                    launch_route="/language/dictionaries",
                    due_reason="Draft lexical assets are not used as review content until confirmed.",
                    linked_lexical_ids=self._ids(draft, "lexical_id", 10),
                    prerequisites=["Confirm dictionary or lexical asset"],
                    priority=self._priority(
                        urgency=0.5,
                        formula_or_language_value=0.8,
                        source_quality=0.5,
                        user_goal_alignment=self._goal_alignment(goal, "language confirm dictionary"),
                    ),
                )
            )

    def _add_file_cleanup_candidates(
        self,
        candidates: list[StudyPlanBlock],
        *,
        plan_id: str,
        profile_id: str,
    ) -> None:
        try:
            from study_science.file_ingestion import FileIngestionService
        except ImportError:
            return
        service = FileIngestionService(self.repo_root)
        files = self._safe(lambda: service.list_files(profile_id=profile_id), [])
        needs_cleanup = [
            file for file in files
            if file.get("extraction_status") in {"failed", "extracted_no_text", "unsupported"}
        ]
        if not needs_cleanup:
            return
        candidates.append(
            self._candidate(
                plan_id=plan_id,
                block_type="file_ingestion_cleanup",
                title="Clean up file ingestion failures",
                description="Resolve failed, unsupported, or no-text local imports.",
                launch_route="/review/assets",
                due_reason=f"{len(needs_cleanup)} uploaded files need cleanup or replacement; OCR remains disabled.",
                prerequisites=["Replace unsupported files or provide extractable text"],
                priority=self._priority(urgency=0.55, coverage_gap_value=0.35, source_quality=0.2),
            )
        )

    def _compose_blocks(
        self,
        *,
        plan_id: str,
        candidates: list[StudyPlanBlock],
        energy_mode: EnergyMode,
        available_minutes: int,
    ) -> list[StudyPlanBlock]:
        selected: list[StudyPlanBlock] = []
        used_ids: set[str] = set()
        candidates = sorted(candidates, key=lambda block: block.priority, reverse=True)

        for category, ratio, max_count in ENERGY_MIX[energy_mode]:
            matching = [
                block for block in candidates
                if block.block_id not in used_ids and block.block_type in CATEGORY_TYPES[category]
            ]
            matching = sorted(matching, key=lambda block: (block.status == "blocked", -block.priority))
            if not matching and category == "reflection":
                matching = self._default_blocks(plan_id=plan_id, available_minutes=available_minutes)[:1]
            if not matching:
                continue
            if category == "cleanup":
                matching = sorted(
                    matching,
                    key=lambda block: (block.block_type != "file_ingestion_cleanup", block.status == "blocked", -block.priority),
                )
            budget = max(5, round(available_minutes * ratio))
            count = min(max_count, len(matching))
            per_block = max(5, budget // count)
            for block in matching[:count]:
                selected_block = self._clone_block(block, target_minutes=per_block)
                selected.append(selected_block)
                used_ids.add(block.block_id)

        if not selected:
            selected = self._default_blocks(plan_id=plan_id, available_minutes=available_minutes)
        if not any(block.block_type == "reflection" for block in selected):
            remaining = max(0, available_minutes - sum(block.target_minutes for block in selected))
            if remaining >= 5:
                selected.append(self._reflection_block(plan_id=plan_id, target_minutes=min(remaining, 10)))

        self._fit_minutes(selected, available_minutes)
        for index, block in enumerate(selected, start=1):
            block.block_id = _stable_id("block", plan_id, index, block.block_type, block.title)
            block.plan_id = plan_id
        return selected

    def _default_blocks(self, *, plan_id: str, available_minutes: int) -> list[StudyPlanBlock]:
        review_minutes = min(max(10, available_minutes // 3), available_minutes)
        reflection_minutes = min(max(5, available_minutes // 6), max(5, available_minutes - review_minutes))
        return [
            self._candidate(
                plan_id=plan_id,
                block_type="mission_control_review",
                title="Mission Control review",
                description="Check system status and pick the next import or confirmation action.",
                target_minutes=review_minutes,
                launch_route="/review/mission-control",
                due_reason="No urgent confirmed review work is ready; inspect Mission Control safely.",
                priority=10.0,
            ),
            self._reflection_block(plan_id=plan_id, target_minutes=reflection_minutes),
        ]

    def _reflection_block(self, *, plan_id: str, target_minutes: int) -> StudyPlanBlock:
        return self._candidate(
            plan_id=plan_id,
            block_type="reflection",
            title="Session reflection and tomorrow setup",
            description="Record what moved, what stayed blocked, and the next safe study action.",
            target_minutes=target_minutes,
            launch_route="/review/mission-control",
            due_reason="Every study session should end with measurable outcomes and next actions.",
            priority=8.0,
        )

    def _candidate(
        self,
        *,
        plan_id: str,
        block_type: BlockType,
        title: str,
        description: str,
        launch_route: str,
        due_reason: str,
        priority: float,
        target_minutes: int = 0,
        linked_asset_ids: list[str] | None = None,
        linked_topic_ids: list[str] | None = None,
        linked_gap_ids: list[str] | None = None,
        linked_resource_ids: list[str] | None = None,
        linked_lexical_ids: list[str] | None = None,
        prerequisites: list[str] | None = None,
        blocked_reason: str | None = None,
    ) -> StudyPlanBlock:
        return StudyPlanBlock(
            block_id=_stable_id("candidate", plan_id, block_type, title, priority),
            plan_id=plan_id,
            block_type=block_type,
            title=title,
            description=description,
            target_minutes=target_minutes,
            priority=round(priority, 2),
            launch_route=launch_route,
            due_reason=due_reason,
            linked_asset_ids=linked_asset_ids or [],
            linked_topic_ids=linked_topic_ids or [],
            linked_gap_ids=linked_gap_ids or [],
            linked_resource_ids=linked_resource_ids or [],
            linked_lexical_ids=linked_lexical_ids or [],
            prerequisites=prerequisites or [],
            blocked_reason=blocked_reason,
            status="blocked" if blocked_reason else "pending",
        )

    def _priority(
        self,
        *,
        urgency: float = 0.0,
        exam_weight: float = 0.0,
        memory_decay: float = 0.0,
        transfer_gap_severity: float = 0.0,
        coverage_gap_value: float = 0.0,
        formula_or_language_value: float = 0.0,
        source_quality: float = 0.0,
        user_goal_alignment: float = 0.0,
    ) -> float:
        score = (
            0.24 * _clamp(urgency)
            + 0.18 * _clamp(exam_weight)
            + 0.16 * _clamp(memory_decay)
            + 0.14 * _clamp(transfer_gap_severity)
            + 0.10 * _clamp(coverage_gap_value)
            + 0.08 * _clamp(formula_or_language_value)
            + 0.06 * _clamp(source_quality)
            + 0.04 * _clamp(user_goal_alignment)
        )
        return round(score * 100, 2)

    def _summarize(self, blocks: list[StudyPlanBlock], *, available_minutes: int) -> dict[str, Any]:
        statuses: dict[str, int] = {"pending": 0, "in_progress": 0, "completed": 0, "skipped": 0, "blocked": 0}
        for block in blocks:
            statuses[block.status] = statuses.get(block.status, 0) + 1
        completed_minutes = sum(block.target_minutes for block in blocks if block.status == "completed")
        return {
            "total_minutes": sum(block.target_minutes for block in blocks),
            "available_minutes": available_minutes,
            "block_count": len(blocks),
            "completed_blocks": statuses.get("completed", 0),
            "skipped_blocks": statuses.get("skipped", 0),
            "blocked_blocks": statuses.get("blocked", 0),
            "pending_blocks": statuses.get("pending", 0),
            "in_progress_blocks": statuses.get("in_progress", 0),
            "completed_minutes": completed_minutes,
            "status_counts": statuses,
            "block_type_counts": self._count_by(blocks, "block_type"),
        }

    def _next_actions(self, blocks: list[StudyPlanBlock], *, completed: bool) -> list[str]:
        actions: list[str] = []
        blocked = [block for block in blocks if block.status == "blocked"]
        skipped = [block for block in blocks if block.status == "skipped"]
        pending = [block for block in blocks if block.status in {"pending", "in_progress"}]
        if pending:
            actions.append(f"Continue with {pending[0].title}.")
            actions.append("Generate an adaptive assessment after the next recall block to test transfer.")
        if blocked:
            actions.append("Unblock draft, low-quality, or failed-ingestion items before using them for review.")
        if skipped:
            actions.append("Reschedule skipped blocks into the next generated plan.")
        if completed and not actions:
            actions.append("Generate tomorrow's plan from the updated Mission Control signals.")
            actions.append("Run an interleaving assessment to feed Analytics and transfer gaps.")
        if not actions:
            actions.append("Open Mission Control and import or confirm the next source-backed item.")
        return actions

    def _sanitize_mission_summary(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not payload:
            return {}
        safe = {
            key: value
            for key, value in payload.items()
            if key in {
                "profile_id",
                "generated_at",
                "review_lab",
                "assets",
                "formulas",
                "coverage",
                "mock_retro",
                "resources",
                "language",
                "system_health",
                "recommended_actions",
            }
        }
        return self._strip_wrong_fields(safe)

    def _strip_wrong_fields(self, payload: Any) -> Any:
        if isinstance(payload, dict):
            return {
                key: self._strip_wrong_fields(value)
                for key, value in payload.items()
                if key not in WRONG_FIELD_NAMES
            }
        if isinstance(payload, list):
            return [self._strip_wrong_fields(item) for item in payload]
        return payload

    def _persist_plan(self, plan: StudyPlan) -> None:
        self._plan_path(plan.plan_id).write_text(
            json.dumps(plan.as_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _write_latest(self, profile_id: str, plan_date: str, plan_id: str) -> None:
        self._latest_path(profile_id, plan_date).write_text(plan_id, encoding="utf-8")

    def _plan_path(self, plan_id: str) -> Path:
        return self.plan_root / f"{plan_id}.json"

    def _latest_path(self, profile_id: str, plan_date: str) -> Path:
        return self.latest_root / f"{_stable_id('latest', profile_id, plan_date)}.txt"

    def _require_plan(self, plan_id: str) -> StudyPlan:
        plan = self.get_plan(plan_id)
        if plan is None:
            raise KeyError(plan_id)
        return plan

    def _require_block(self, block_id: str) -> tuple[StudyPlan, StudyPlanBlock]:
        for path in sorted(self.plan_root.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
            try:
                plan = StudyPlan.from_dict(json.loads(path.read_text(encoding="utf-8")))
            except Exception:
                continue
            for block in plan.blocks:
                if block.block_id == block_id:
                    return plan, block
        raise KeyError(block_id)

    @staticmethod
    def _fit_minutes(blocks: list[StudyPlanBlock], available_minutes: int) -> None:
        total = sum(block.target_minutes for block in blocks)
        if total <= available_minutes:
            return
        overflow = total - available_minutes
        for block in sorted(blocks, key=lambda item: item.target_minutes, reverse=True):
            reducible = max(0, block.target_minutes - 5)
            reduction = min(reducible, overflow)
            block.target_minutes -= reduction
            overflow -= reduction
            if overflow <= 0:
                break

    @staticmethod
    def _clone_block(block: StudyPlanBlock, *, target_minutes: int) -> StudyPlanBlock:
        clone = StudyPlanBlock.from_dict(block.as_dict())
        clone.target_minutes = target_minutes
        return clone

    @staticmethod
    def _count_by(blocks: list[StudyPlanBlock], attr: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for block in blocks:
            value = str(getattr(block, attr))
            counts[value] = counts.get(value, 0) + 1
        return counts

    @staticmethod
    def _ids(items: list[dict[str, Any]], key: str, limit: int) -> list[str]:
        ids: list[str] = []
        for item in items:
            value = item.get(key)
            if value and str(value) not in ids:
                ids.append(str(value))
            if len(ids) >= limit:
                break
        return ids

    @staticmethod
    def _avg(items: list[dict[str, Any]], key: str, *, default: float = 0.0) -> float:
        values: list[float] = []
        for item in items:
            try:
                values.append(float(item.get(key, default) or default))
            except (TypeError, ValueError):
                continue
        return sum(values) / len(values) if values else default

    @staticmethod
    def _goal_alignment(goal: str, keywords: str) -> float:
        if not goal.strip():
            return 0.0
        goal_words = {word.strip().lower() for word in goal.replace("/", " ").split() if word.strip()}
        key_words = {word.strip().lower() for word in keywords.split() if word.strip()}
        if not goal_words or not key_words:
            return 0.0
        return len(goal_words & key_words) / max(1, len(key_words))

    @staticmethod
    def _safe(call: Callable[[], Any], fallback: Any) -> Any:
        try:
            return call()
        except Exception:
            return fallback
