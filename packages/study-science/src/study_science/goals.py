from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Literal

from study_science.data_governance import sanitize_payload, stable_id


GoalType = Literal["exam", "language", "course", "career", "project", "custom"]
EnergyMode = Literal["low", "normal", "high"]
GoalStatus = Literal["draft", "active", "archived"]
PackType = Literal["exam", "language", "course", "custom"]


ONBOARDING_STEPS = [
    "choose_goal",
    "choose_course_pack",
    "set_time_budget",
    "import_syllabus_or_seed_demo",
    "import_resources_or_files",
    "import_dictionary_if_language",
    "confirm_initial_assets",
    "generate_first_plan",
    "start_first_review_or_assessment",
    "backup_reminder",
]

MODULE_RECOMMENDATIONS: dict[str, list[str]] = {
    "exam": ["Review Lab", "Coverage", "Formula Lab", "Assessments", "Analytics", "Planner", "Tutor"],
    "language": ["LanguageOS", "Lexical Review", "Assessments", "Planner", "Analytics", "Tutor"],
    "course": ["Resources", "Coverage", "Review Lab", "Assessments", "Knowledge Map", "Tutor"],
    "career": ["Resources", "Knowledge Map", "Planner", "Tutor", "Assessments"],
    "project": ["Resources", "Knowledge Map", "Planner", "Tutor"],
    "custom": ["Resources", "Review Lab", "Planner", "Tutor"],
}


@dataclass(slots=True)
class CoursePack:
    pack_id: str
    title: str
    pack_type: PackType
    description: str
    default_modules: list[str]
    suggested_imports: list[dict[str, Any]]
    syllabus_seed: list[dict[str, Any]]
    formula_families: list[str]
    lexical_config: dict[str, Any]
    planner_defaults: dict[str, Any]
    assessment_defaults: dict[str, Any]
    quality_gate_policy: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class GoalProfile:
    goal_id: str
    profile_id: str
    title: str
    goal_type: GoalType
    target_exam: str | None
    target_language: str | None
    source_language: str | None
    target_date: str | None
    weekly_minutes: int
    default_energy_mode: EnergyMode
    enabled_modules: list[str]
    preferred_review_modes: list[str]
    created_at: str
    updated_at: str
    status: GoalStatus
    onboarding_status: dict[str, Any]
    pack_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> GoalProfile:
        return cls(
            goal_id=str(payload.get("goal_id") or ""),
            profile_id=str(payload.get("profile_id") or "default"),
            title=str(payload.get("title") or "Untitled goal"),
            goal_type=str(payload.get("goal_type") or "custom"),  # type: ignore[arg-type]
            target_exam=payload.get("target_exam"),
            target_language=payload.get("target_language"),
            source_language=payload.get("source_language"),
            target_date=payload.get("target_date"),
            weekly_minutes=int(payload.get("weekly_minutes") or 300),
            default_energy_mode=str(payload.get("default_energy_mode") or "normal"),  # type: ignore[arg-type]
            enabled_modules=list(payload.get("enabled_modules") or []),
            preferred_review_modes=list(payload.get("preferred_review_modes") or []),
            created_at=str(payload.get("created_at") or _now()),
            updated_at=str(payload.get("updated_at") or _now()),
            status=str(payload.get("status") or "draft"),  # type: ignore[arg-type]
            onboarding_status=dict(payload.get("onboarding_status") or {}),
            pack_id=payload.get("pack_id"),
        )


@dataclass(slots=True)
class OnboardingState:
    profile_id: str
    active_goal_id: str | None
    completed_steps: list[str] = field(default_factory=list)
    skipped_steps: list[str] = field(default_factory=list)
    current_step: str = "choose_goal"
    readiness_score: float = 0.0
    readiness_status: str = "not_started"
    blockers: list[dict[str, Any]] = field(default_factory=list)
    recommended_next_action: dict[str, Any] | None = None
    updated_at: str = field(default_factory=lambda: _now())

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> OnboardingState:
        return cls(
            profile_id=str(payload.get("profile_id") or "default"),
            active_goal_id=payload.get("active_goal_id"),
            completed_steps=list(payload.get("completed_steps") or []),
            skipped_steps=list(payload.get("skipped_steps") or []),
            current_step=str(payload.get("current_step") or "choose_goal"),
            readiness_score=float(payload.get("readiness_score") or 0.0),
            readiness_status=str(payload.get("readiness_status") or "not_started"),
            blockers=list(payload.get("blockers") or []),
            recommended_next_action=payload.get("recommended_next_action"),
            updated_at=str(payload.get("updated_at") or _now()),
        )


class GoalOnboardingService:
    """Top-level local goal/profile and first-run onboarding coordinator."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.root = self.repo_root / ".system" / "memory" / "goals"
        self.profile_root = self.root / "profiles"
        self.onboarding_root = self.root / "onboarding"
        self.day1_root = self.root / "day1"
        for path in (self.profile_root, self.onboarding_root, self.day1_root):
            path.mkdir(parents=True, exist_ok=True)
        self.active_path = self.root / "active.json"

    def list_course_packs(self) -> dict[str, Any]:
        packs = [pack.as_dict() for pack in COURSE_PACKS]
        return {"count": len(packs), "packs": packs}

    def get_course_pack(self, pack_id: str | None) -> CoursePack | None:
        if not pack_id:
            return None
        return next((pack for pack in COURSE_PACKS if pack.pack_id == pack_id), None)

    def create_goal(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload, _ = sanitize_payload(payload or {})
        pack = self.get_course_pack(str(payload.get("pack_id") or "")) or self._default_pack_for(payload)
        goal_type = _clean_choice(payload.get("goal_type") or pack.pack_type, set(MODULE_RECOMMENDATIONS), "custom")
        profile_id = str(payload.get("profile_id") or "default")
        title = str(payload.get("title") or pack.title or "Learning goal").strip() or "Learning goal"
        now = _now()
        modules = list(payload.get("enabled_modules") or pack.default_modules or MODULE_RECOMMENDATIONS[goal_type])
        weekly_minutes = _int_between(payload.get("weekly_minutes"), 30, 6000, int(pack.planner_defaults.get("weekly_minutes", 300)))
        energy_mode = _clean_choice(payload.get("default_energy_mode") or pack.planner_defaults.get("default_energy_mode"), {"low", "normal", "high"}, "normal")
        goal = GoalProfile(
            goal_id=stable_id("goal", profile_id, title, now),
            profile_id=profile_id,
            title=title,
            goal_type=goal_type,  # type: ignore[arg-type]
            target_exam=_optional_text(payload.get("target_exam")),
            target_language=_optional_text(payload.get("target_language") or pack.lexical_config.get("target_language")),
            source_language=_optional_text(payload.get("source_language") or pack.lexical_config.get("source_language")),
            target_date=_optional_text(payload.get("target_date")),
            weekly_minutes=weekly_minutes,
            default_energy_mode=energy_mode,  # type: ignore[arg-type]
            enabled_modules=modules,
            preferred_review_modes=list(payload.get("preferred_review_modes") or _preferred_modes(goal_type)),
            created_at=now,
            updated_at=now,
            status="draft",
            onboarding_status={"pack_id": pack.pack_id, "created_from_pack": True},
            pack_id=pack.pack_id,
        )
        self._persist_goal(goal)
        state = self._load_or_new_state(profile_id)
        state.completed_steps = _dedupe(state.completed_steps + ["choose_goal", "choose_course_pack", "set_time_budget"])
        state.active_goal_id = self.active_goal_id()
        self._refresh_state(state, goal=self.get_active_goal())
        self._persist_state(state)
        return {"goal": goal.as_dict(), "course_pack": pack.as_dict(), "onboarding": state.as_dict()}

    def list_goals(self, *, profile_id: str = "", include_archived: bool = False) -> dict[str, Any]:
        goals = self._load_goals()
        if profile_id:
            goals = [goal for goal in goals if goal.profile_id == profile_id]
        if not include_archived:
            goals = [goal for goal in goals if goal.status != "archived"]
        active = self.get_active_goal()
        return {
            "count": len(goals),
            "goals": [goal.as_dict() for goal in sorted(goals, key=lambda item: item.updated_at, reverse=True)],
            "active_goal": active.as_dict() if active else None,
        }

    def get_goal(self, goal_id: str) -> dict[str, Any] | None:
        goal = self._load_goal(goal_id)
        if goal is None:
            return None
        pack = self.get_course_pack(goal.pack_id)
        return {"goal": goal.as_dict(), "course_pack": pack.as_dict() if pack else None}

    def activate_goal(self, goal_id: str) -> dict[str, Any]:
        target = self._require_goal(goal_id)
        for goal in self._load_goals():
            if goal.profile_id == target.profile_id and goal.status == "active" and goal.goal_id != target.goal_id:
                goal.status = "draft"
                goal.updated_at = _now()
                self._persist_goal(goal)
        target.status = "active"
        target.updated_at = _now()
        self._persist_goal(target)
        self.active_path.write_text(json.dumps({"goal_id": goal_id}, ensure_ascii=False, indent=2), encoding="utf-8")
        state = self._load_or_new_state(target.profile_id)
        state.active_goal_id = target.goal_id
        state.completed_steps = _dedupe(state.completed_steps + ["choose_goal", "choose_course_pack", "set_time_budget"])
        self._refresh_state(state, goal=target)
        self._persist_state(state)
        return {"goal": target.as_dict(), "onboarding": state.as_dict()}

    def archive_goal(self, goal_id: str) -> dict[str, Any]:
        goal = self._require_goal(goal_id)
        goal.status = "archived"
        goal.updated_at = _now()
        self._persist_goal(goal)
        if self.active_goal_id() == goal.goal_id and self.active_path.exists():
            self.active_path.unlink()
        state = self._load_or_new_state(goal.profile_id)
        state.active_goal_id = self.active_goal_id()
        self._refresh_state(state, goal=self.get_active_goal())
        self._persist_state(state)
        return {"goal": goal.as_dict(), "onboarding": state.as_dict()}

    def patch_goal(self, goal_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        payload, _ = sanitize_payload(payload or {})
        goal = self._require_goal(goal_id)
        for key in ("title", "target_exam", "target_language", "source_language", "target_date"):
            if key in payload:
                if key == "title":
                    goal.title = str(payload.get(key) or goal.title).strip() or goal.title
                else:
                    setattr(goal, key, _optional_text(payload.get(key)))
        if "goal_type" in payload:
            goal.goal_type = _clean_choice(payload.get("goal_type"), set(MODULE_RECOMMENDATIONS), goal.goal_type)  # type: ignore[assignment]
        if "weekly_minutes" in payload:
            goal.weekly_minutes = _int_between(payload.get("weekly_minutes"), 30, 6000, goal.weekly_minutes)
        if "default_energy_mode" in payload:
            goal.default_energy_mode = _clean_choice(payload.get("default_energy_mode"), {"low", "normal", "high"}, goal.default_energy_mode)  # type: ignore[assignment]
        if "enabled_modules" in payload and isinstance(payload["enabled_modules"], list):
            goal.enabled_modules = [str(item) for item in payload["enabled_modules"] if str(item).strip()]
        if "preferred_review_modes" in payload and isinstance(payload["preferred_review_modes"], list):
            goal.preferred_review_modes = [str(item) for item in payload["preferred_review_modes"] if str(item).strip()]
        goal.updated_at = _now()
        self._persist_goal(goal)
        state = self._load_or_new_state(goal.profile_id)
        self._refresh_state(state, goal=self.get_active_goal() if self.active_goal_id() == goal.goal_id else goal)
        self._persist_state(state)
        return {"goal": goal.as_dict(), "onboarding": state.as_dict()}

    def active_goal_id(self) -> str | None:
        if not self.active_path.exists():
            return None
        try:
            return json.loads(self.active_path.read_text(encoding="utf-8")).get("goal_id")
        except (OSError, json.JSONDecodeError):
            return None

    def get_active_goal(self) -> GoalProfile | None:
        active_id = self.active_goal_id()
        if active_id:
            goal = self._load_goal(active_id)
            if goal and goal.status == "active":
                return goal
        for goal in self._load_goals():
            if goal.status == "active":
                return goal
        return None

    def onboarding_state(self, *, profile_id: str = "") -> dict[str, Any]:
        goal = self._goal_for_profile(profile_id)
        resolved_profile = profile_id or (goal.profile_id if goal else "default")
        state = self._load_or_new_state(resolved_profile)
        self._refresh_state(state, goal=goal)
        self._persist_state(state)
        return state.as_dict()

    def complete_step(self, *, profile_id: str = "", step_id: str) -> dict[str, Any]:
        goal = self._goal_for_profile(profile_id)
        resolved_profile = profile_id or (goal.profile_id if goal else "default")
        state = self._load_or_new_state(resolved_profile)
        if step_id in ONBOARDING_STEPS:
            state.completed_steps = _dedupe(state.completed_steps + [step_id])
            state.skipped_steps = [step for step in state.skipped_steps if step != step_id]
        self._refresh_state(state, goal=goal)
        self._persist_state(state)
        return state.as_dict()

    def skip_step(self, *, profile_id: str = "", step_id: str) -> dict[str, Any]:
        goal = self._goal_for_profile(profile_id)
        resolved_profile = profile_id or (goal.profile_id if goal else "default")
        state = self._load_or_new_state(resolved_profile)
        if step_id in ONBOARDING_STEPS:
            state.skipped_steps = _dedupe(state.skipped_steps + [step_id])
        self._refresh_state(state, goal=goal)
        self._persist_state(state)
        return state.as_dict()

    def reset_onboarding(self, *, profile_id: str = "") -> dict[str, Any]:
        goal = self._goal_for_profile(profile_id)
        resolved_profile = profile_id or (goal.profile_id if goal else "default")
        state = OnboardingState(profile_id=resolved_profile, active_goal_id=self.active_goal_id())
        self._refresh_state(state, goal=None)
        self._persist_state(state)
        return state.as_dict()

    def readiness(self, *, profile_id: str = "") -> dict[str, Any]:
        goal = self._goal_for_profile(profile_id)
        state = self._load_or_new_state(profile_id or (goal.profile_id if goal else "default"))
        return self._readiness_payload(goal=goal, state=state)

    def generate_day1_plan(self, *, profile_id: str = "", goal_id: str = "") -> dict[str, Any]:
        goal = self._load_goal(goal_id) if goal_id else self._goal_for_profile(profile_id)
        resolved_profile = profile_id or (goal.profile_id if goal else "default")
        state = self._load_or_new_state(resolved_profile)
        signals = self._signals(resolved_profile)
        blocks = self._day1_blocks(goal=goal, signals=signals)
        planner_payload = self._generate_study_planner_seed(goal, resolved_profile)
        state.completed_steps = _dedupe(state.completed_steps + ["generate_first_plan"])
        self._refresh_state(state, goal=goal)
        self._persist_state(state)
        plan_id = stable_id("day1", resolved_profile, goal.goal_id if goal else "no-goal", _today())
        payload = {
            "plan_id": plan_id,
            "profile_id": resolved_profile,
            "generated_at": _now(),
            "goal": goal.as_dict() if goal else None,
            "blocks": blocks,
            "readiness": self._readiness_payload(goal=goal, state=state),
            "study_planner_seed": planner_payload,
            "safety": {
                "correct_only": True,
                "draft_content_enters_review": False,
                "external_network": False,
            },
        }
        payload, _ = sanitize_payload(payload)
        self._day1_path(plan_id).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return payload

    def governance_summary(self, *, profile_id: str = "default") -> dict[str, Any]:
        active = self.get_active_goal()
        state = self.onboarding_state(profile_id=profile_id if profile_id != "default" else "")
        goals = self.list_goals(include_archived=True)["goals"]
        return {
            "goal_count": len(goals),
            "active_goal": active.as_dict() if active else None,
            "readiness_score": state["readiness_score"],
            "readiness_status": state["readiness_status"],
            "current_step": state["current_step"],
            "blocker_count": len(state["blockers"]),
            "snapshot_route": "/review/goals",
        }

    def _readiness_payload(self, *, goal: GoalProfile | None, state: OnboardingState) -> dict[str, Any]:
        signals = self._signals(goal.profile_id if goal else state.profile_id)
        components = {
            "goal_configured": (0.20, goal is not None and goal.status == "active"),
            "syllabus_or_language_scope_exists": (0.15, signals["scope_count"] > 0 or bool(goal and goal.goal_type == "language" and goal.pack_id)),
            "confirmed_assets_or_lexical_items": (0.15, signals["confirmed_count"] > 0),
            "source_refs_present": (0.10, signals["source_ref_count"] > 0),
            "quality_gate_health": (0.10, signals["has_learning_state"] and signals["draft_count"] == 0 and signals["low_quality_count"] == 0),
            "plan_generated": (0.10, signals["plan_count"] > 0 or "generate_first_plan" in state.completed_steps),
            "first_review_available": (0.10, signals["confirmed_count"] > 0),
            "backup_available": (0.05, signals["backup_count"] > 0),
            "tutor_search_available": (0.05, goal is not None and signals["tutor_search_available"]),
        }
        component_payload: dict[str, Any] = {}
        score = 0.0
        for name, (weight, earned) in components.items():
            contribution = weight if earned else 0.0
            score += contribution
            component_payload[name] = {"weight": weight, "earned": bool(earned), "contribution": round(contribution, 2)}
        blockers = self._blockers(goal=goal, signals=signals, state=state)
        status = self._readiness_status(goal=goal, signals=signals, state=state, score=score)
        return {
            "profile_id": goal.profile_id if goal else state.profile_id,
            "active_goal_id": goal.goal_id if goal and goal.status == "active" else None,
            "completed_steps": state.completed_steps,
            "skipped_steps": state.skipped_steps,
            "current_step": self._current_step(state, goal=goal),
            "readiness_score": round(score, 2),
            "readiness_status": status,
            "components": component_payload,
            "blockers": blockers,
            "recommended_next_action": self._recommended_next_action(status, blockers, goal),
            "updated_at": state.updated_at,
            "signals": {
                key: signals[key]
                for key in [
                    "scope_count",
                    "draft_count",
                    "confirmed_count",
                    "formula_count",
                    "lexical_count",
                    "source_ref_count",
                    "plan_count",
                    "backup_count",
                ]
            },
        }

    def _refresh_state(self, state: OnboardingState, *, goal: GoalProfile | None) -> None:
        readiness = self._readiness_payload(goal=goal, state=state)
        state.active_goal_id = readiness["active_goal_id"]
        state.readiness_score = readiness["readiness_score"]
        state.readiness_status = readiness["readiness_status"]
        state.blockers = readiness["blockers"]
        state.recommended_next_action = readiness["recommended_next_action"]
        state.current_step = self._current_step(state, goal=goal)
        state.updated_at = _now()

    def _day1_blocks(self, *, goal: GoalProfile | None, signals: dict[str, Any]) -> list[dict[str, Any]]:
        blocks: list[dict[str, Any]] = []
        if goal is None:
            blocks.append(_block("setup", "Choose an active learning goal", "/onboarding", "Select a goal profile before importing or reviewing content.", 15))
            blocks.append(_block("import", "Pick a safe local course pack", "/onboarding", "Starter packs only use generic placeholder scope until you import official material.", 15))
        else:
            pack = self.get_course_pack(goal.pack_id)
            if signals["scope_count"] == 0:
                title = "Import syllabus or seed generic starter topics"
                if goal.goal_type == "language":
                    title = "Import dictionary or choose lexical starter scope"
                blocks.append(_block("import", title, "/onboarding", "No trusted scope exists yet; import local material or seed generic placeholders first.", 20))
            if goal.goal_type == "language" and signals["lexical_count"] == 0:
                blocks.append(_block("dictionary_import", "Import or create first dictionary items", "/language/dictionaries", "Language goals need dictionary-backed lexical items before review.", 20))
            if signals["draft_count"] > 0:
                blocks.append(_block("confirmation", "Confirm draft assets before review", "/review/assets", f"{signals['draft_count']} draft or needs-review items are blocked by quality gates.", 20))
            if signals["confirmed_count"] > 0:
                blocks.append(_block("review_lab", "Run first correct-only Review Lab block", "/review/lab", "Confirmed source-backed assets are available for recall.", 25))
            if signals["formula_count"] > 0 and "Formula Lab" in goal.enabled_modules:
                blocks.append(_block("formula_lab", "Run a short Formula Lab drill", "/review/formulas", "Formula assets exist and should be practiced with calculator/procedure checks.", 20))
            if signals["lexical_count"] > 0 and goal.goal_type == "language":
                blocks.append(_block("lexical_review", "Run first lexical review", "/language/review", "Confirmed lexical items are available.", 20))
            if pack and pack.suggested_imports:
                blocks.append(_block("import_resources", "Import the first local resource", "/onboarding", f"Suggested import: {pack.suggested_imports[0]['label']}", 15))
        blocks.append(_block("mission_control_review", "Open Mission Control", "/review/mission-control", "Check readiness, blockers, and subsystem health before deeper work.", 10))
        blocks.append(_block("backup_reminder", "Create a safe local backup", "/review/data", "Back up local state after setting the first goal and plan.", 10))
        return blocks

    def _signals(self, profile_id: str) -> dict[str, Any]:
        assets = self._records(self.repo_root / ".system" / "memory" / "review" / "asset-candidates", profile_id=profile_id)
        topics = self._records(self.repo_root / ".system" / "memory" / "review" / "syllabus", profile_id=profile_id)
        lexical = self._records(self.repo_root / ".system" / "memory" / "language" / "dictionary-kernel" / "lexical-assets", profile_id=profile_id)
        dictionaries = self._records(self.repo_root / ".system" / "memory" / "language" / "dictionary-kernel" / "dictionaries", profile_id=profile_id)
        resources = self._records(self.repo_root / ".system" / "memory" / "review" / "resources", profile_id=profile_id)
        plans = self._records(self.repo_root / ".system" / "memory" / "study-planner" / "plans", profile_id=profile_id)
        day1 = self._records(self.day1_root, profile_id=profile_id)
        confirmed_assets = [
            item for item in assets
            if item.get("validation_status") in {"confirmed", "validated", "derived"}
        ]
        confirmed_lexical = [item for item in lexical if item.get("validation_status") == "confirmed"]
        draft = [
            item for item in assets + lexical + resources
            if item.get("validation_status") in {"draft", "needs_review"}
        ]
        low_quality = [
            item for item in resources
            if item.get("quality_status") in {"unscored", "low"}
        ]
        formulas = [
            item for item in confirmed_assets
            if item.get("asset_type") == "formula" or item.get("plain_formula") or item.get("formula_latex")
        ]
        source_ref_count = sum(1 for item in topics + assets + lexical + dictionaries + resources if item.get("source_refs"))
        try:
            from app.feature_flags import FeatureFlags

            flags = FeatureFlags.load(self.repo_root)
            tutor_search_available = flags.enabled("tutor_copilot_enabled") and flags.enabled("global_search_enabled")
        except Exception:
            tutor_search_available = False
        return {
            "scope_count": len(topics) + len(dictionaries),
            "draft_count": len(draft),
            "confirmed_count": len(confirmed_assets) + len(confirmed_lexical),
            "formula_count": len(formulas),
            "lexical_count": len(confirmed_lexical),
            "source_ref_count": source_ref_count,
            "low_quality_count": len(low_quality),
            "plan_count": len(plans) + len(day1),
            "backup_count": len(list((self.repo_root / ".system" / "memory" / "backups" / "snapshots").glob("*.json"))),
            "has_learning_state": bool(topics or assets or lexical or dictionaries or resources),
            "tutor_search_available": tutor_search_available,
        }

    def _records(self, root: Path, *, profile_id: str) -> list[dict[str, Any]]:
        if not root.exists():
            return []
        paths = [root] if root.is_file() else sorted(path for path in root.rglob("*.json") if path.is_file())
        rows: list[dict[str, Any]] = []
        for path in paths:
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            candidates = payload if isinstance(payload, list) else payload.get("items") or payload.get("records") or [payload]
            if not isinstance(candidates, list):
                candidates = [payload]
            for item in candidates:
                if not isinstance(item, dict):
                    continue
                item_profile = str(item.get("profile_id") or profile_id or "default")
                if profile_id in {"", "default"} or item_profile in {profile_id, "default"}:
                    safe, _ = sanitize_payload(item)
                    rows.append(safe)
        return rows

    def _blockers(self, *, goal: GoalProfile | None, signals: dict[str, Any], state: OnboardingState) -> list[dict[str, Any]]:
        blockers: list[dict[str, Any]] = []
        if goal is None:
            blockers.append({"blocker_id": "goal_missing", "severity": "high", "message": "No active goal profile is configured.", "launch_route": "/onboarding"})
            return blockers
        if signals["scope_count"] == 0:
            blockers.append({"blocker_id": "scope_missing", "severity": "high", "message": "Import syllabus, dictionary, or seed generic starter scope.", "launch_route": "/onboarding"})
        if signals["draft_count"] > 0:
            blockers.append({"blocker_id": "confirmation_required", "severity": "high", "message": "Draft content cannot enter review until confirmed.", "launch_route": "/review/assets"})
        if signals["confirmed_count"] == 0:
            blockers.append({"blocker_id": "confirmed_assets_missing", "severity": "medium", "message": "No confirmed assets or lexical items are ready for review.", "launch_route": "/review/assets"})
        if signals["plan_count"] == 0 and "generate_first_plan" not in state.completed_steps:
            blockers.append({"blocker_id": "plan_missing", "severity": "medium", "message": "Generate a Day-1 plan before starting review.", "launch_route": "/onboarding"})
        if signals["backup_count"] == 0:
            blockers.append({"blocker_id": "backup_missing", "severity": "low", "message": "Create a safe local backup after setup.", "launch_route": "/review/data"})
        return blockers

    def _readiness_status(self, *, goal: GoalProfile | None, signals: dict[str, Any], state: OnboardingState, score: float) -> str:
        if goal is None:
            return "not_started"
        if signals["scope_count"] == 0:
            return "needs_import"
        if signals["draft_count"] > 0 and signals["confirmed_count"] == 0:
            return "needs_confirmation"
        if signals["plan_count"] == 0 and "generate_first_plan" not in state.completed_steps:
            return "ready_for_first_plan" if score >= 0.35 else "needs_import"
        if signals["confirmed_count"] > 0:
            return "active" if score >= 0.75 else "ready_for_review"
        return "ready_for_first_plan"

    def _recommended_next_action(self, status: str, blockers: list[dict[str, Any]], goal: GoalProfile | None) -> dict[str, Any] | None:
        if blockers:
            blocker = blockers[0]
            return {
                "action_id": blocker["blocker_id"],
                "title": blocker["message"],
                "launch_route": blocker["launch_route"],
            }
        if status in {"ready_for_review", "active"}:
            return {"action_id": "start_review", "title": "Start first review or assessment", "launch_route": "/review/mission-control"}
        if goal:
            return {"action_id": "generate_day1_plan", "title": "Generate Day-1 plan", "launch_route": "/onboarding"}
        return {"action_id": "start_onboarding", "title": "Start onboarding", "launch_route": "/onboarding"}

    def _current_step(self, state: OnboardingState, *, goal: GoalProfile | None) -> str:
        if goal is None:
            return "choose_goal"
        for step in ONBOARDING_STEPS:
            if step not in state.completed_steps and step not in state.skipped_steps:
                if goal.goal_type != "language" and step == "import_dictionary_if_language":
                    continue
                return step
        return "backup_reminder"

    def _generate_study_planner_seed(self, goal: GoalProfile | None, profile_id: str) -> dict[str, Any] | None:
        if goal is None:
            return None
        try:
            from study_science.study_planner import StudyPlannerService

            minutes = max(20, min(120, goal.weekly_minutes // 7))
            plan = StudyPlannerService(self.repo_root).generate_plan(
                profile_id=profile_id,
                energy_mode=goal.default_energy_mode,
                available_minutes=minutes,
                goal=goal.title,
            )
            return {"plan_id": plan.plan_id, "launch_route": "/review/study-planner", "available_minutes": minutes}
        except Exception as exc:
            return {"error": str(exc), "launch_route": "/review/study-planner"}

    def _goal_for_profile(self, profile_id: str) -> GoalProfile | None:
        if profile_id:
            active = self.get_active_goal()
            if active and active.profile_id == profile_id:
                return active
            goals = [goal for goal in self._load_goals() if goal.profile_id == profile_id and goal.status != "archived"]
            return sorted(goals, key=lambda item: item.updated_at, reverse=True)[0] if goals else None
        return self.get_active_goal()

    def _default_pack_for(self, payload: dict[str, Any]) -> CoursePack:
        goal_type = str(payload.get("goal_type") or "")
        if goal_type == "language":
            return self.get_course_pack("language_learning") or COURSE_PACKS[1]
        if goal_type == "exam":
            return self.get_course_pack("custom_exam_course") or COURSE_PACKS[0]
        return self.get_course_pack("custom_exam_course") or COURSE_PACKS[0]

    def _load_goals(self) -> list[GoalProfile]:
        goals = []
        for path in sorted(self.profile_root.glob("*.json")):
            try:
                goals.append(GoalProfile.from_dict(json.loads(path.read_text(encoding="utf-8"))))
            except (OSError, json.JSONDecodeError, TypeError, ValueError):
                continue
        return goals

    def _load_goal(self, goal_id: str) -> GoalProfile | None:
        path = self._goal_path(goal_id)
        if not path.exists():
            return None
        return GoalProfile.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _require_goal(self, goal_id: str) -> GoalProfile:
        goal = self._load_goal(goal_id)
        if goal is None:
            raise KeyError(goal_id)
        return goal

    def _persist_goal(self, goal: GoalProfile) -> None:
        payload, _ = sanitize_payload(goal.as_dict())
        self._goal_path(goal.goal_id).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_or_new_state(self, profile_id: str) -> OnboardingState:
        path = self._state_path(profile_id)
        if not path.exists():
            return OnboardingState(profile_id=profile_id, active_goal_id=self.active_goal_id())
        try:
            return OnboardingState.from_dict(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return OnboardingState(profile_id=profile_id, active_goal_id=self.active_goal_id())

    def _persist_state(self, state: OnboardingState) -> None:
        payload, _ = sanitize_payload(state.as_dict())
        self._state_path(state.profile_id).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _goal_path(self, goal_id: str) -> Path:
        return self.profile_root / f"{goal_id}.json"

    def _state_path(self, profile_id: str) -> Path:
        return self.onboarding_root / f"{stable_id('onboarding', profile_id or 'default')}.json"

    def _day1_path(self, plan_id: str) -> Path:
        return self.day1_root / f"{plan_id}.json"


def course_packs() -> list[CoursePack]:
    return COURSE_PACKS


def _block(block_type: str, title: str, launch_route: str, reason: str, minutes: int) -> dict[str, Any]:
    return {
        "block_id": stable_id("day1-block", block_type, title, launch_route),
        "block_type": block_type,
        "title": title,
        "description": reason,
        "target_minutes": minutes,
        "launch_route": launch_route,
        "due_reason": reason,
    }


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _today() -> str:
    return date.today().isoformat()


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _clean_choice(value: Any, allowed: set[str], default: str) -> str:
    text = str(value or "").strip()
    return text if text in allowed else default


def _int_between(value: Any, low: int, high: int, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(low, min(high, parsed))


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            out.append(item)
            seen.add(item)
    return out


def _preferred_modes(goal_type: str) -> list[str]:
    if goal_type == "language":
        return ["lexical_review", "language_help", "assessment_review"]
    if goal_type == "exam":
        return ["review_lab", "formula_help", "assessment_review"]
    return ["review_lab", "explain", "study_strategy"]


COURSE_PACKS: list[CoursePack] = [
    CoursePack(
        pack_id="custom_exam_course",
        title="Custom Exam / Course",
        pack_type="exam",
        description="Generic exam or course setup with local imports and manual confirmation gates.",
        default_modules=MODULE_RECOMMENDATIONS["exam"],
        suggested_imports=[
            {"import_type": "syllabus", "label": "Import your official syllabus or outline", "required": True},
            {"import_type": "resources", "label": "Import local notes, PDFs, or text extracts", "required": False},
        ],
        syllabus_seed=[
            {"topic_id": "custom-topic-1", "title": "Generic topic placeholder", "source_refs": []},
            {"topic_id": "custom-topic-2", "title": "Practice and review workflow", "source_refs": []},
        ],
        formula_families=[],
        lexical_config={},
        planner_defaults={"weekly_minutes": 300, "default_energy_mode": "normal"},
        assessment_defaults={"mode": "mixed", "question_count": 10},
        quality_gate_policy={"manual_confirm_required": True, "draft_enters_review": False},
    ),
    CoursePack(
        pack_id="language_learning",
        title="Language Learning",
        pack_type="language",
        description="Vocabulary and reading workflow for a target language using local dictionaries.",
        default_modules=MODULE_RECOMMENDATIONS["language"],
        suggested_imports=[
            {"import_type": "dictionary", "label": "Import a local dictionary or vocabulary list", "required": True},
            {"import_type": "reading", "label": "Add short reading examples with source notes", "required": False},
        ],
        syllabus_seed=[
            {"topic_id": "language-scope-1", "title": "Core vocabulary and usage", "source_refs": []},
            {"topic_id": "language-scope-2", "title": "Example sentences and collocations", "source_refs": []},
        ],
        formula_families=[],
        lexical_config={"source_language": "en", "target_language": "target"},
        planner_defaults={"weekly_minutes": 210, "default_energy_mode": "low"},
        assessment_defaults={"mode": "lexical", "question_count": 12},
        quality_gate_policy={"manual_confirm_required": True, "dictionary_quality_gate": True},
    ),
    CoursePack(
        pack_id="cfa_finance",
        title="CFA-style Finance Study",
        pack_type="exam",
        description="Finance exam workflow with generic placeholder topics, formulas, coverage, assessments, and tutor support.",
        default_modules=MODULE_RECOMMENDATIONS["exam"],
        suggested_imports=[
            {"import_type": "syllabus", "label": "Import your licensed curriculum outline", "required": True},
            {"import_type": "formula_sheet", "label": "Import your own formula notes", "required": False},
            {"import_type": "mock_retro", "label": "Import sanitized mock review notes", "required": False},
        ],
        syllabus_seed=[
            {"topic_id": "finance-generic-quant", "title": "Quantitative methods overview", "source_refs": []},
            {"topic_id": "finance-generic-reporting", "title": "Financial reporting overview", "source_refs": []},
            {"topic_id": "finance-generic-corporate", "title": "Corporate issuers overview", "source_refs": []},
            {"topic_id": "finance-generic-fixed-income", "title": "Fixed income overview", "source_refs": []},
        ],
        formula_families=["time_value_of_money", "cost_of_capital", "fixed_income_duration", "portfolio_risk"],
        lexical_config={},
        planner_defaults={"weekly_minutes": 600, "default_energy_mode": "normal"},
        assessment_defaults={"mode": "interleaving", "question_count": 20},
        quality_gate_policy={"manual_confirm_required": True, "draft_enters_review": False, "source_refs_required": True},
    ),
    CoursePack(
        pack_id="spanish_english_vocabulary",
        title="Spanish-English Vocabulary",
        pack_type="language",
        description="Spanish vocabulary workflow with dictionary import, lexical review, assessments, and tutor support.",
        default_modules=MODULE_RECOMMENDATIONS["language"],
        suggested_imports=[
            {"import_type": "dictionary", "label": "Import Spanish-English vocabulary JSON/CSV", "required": True},
            {"import_type": "reading", "label": "Add Spanish example sentences", "required": False},
        ],
        syllabus_seed=[
            {"topic_id": "spanish-vocab-core", "title": "Core Spanish vocabulary", "source_refs": []},
            {"topic_id": "spanish-vocab-collocations", "title": "Collocations and sentence patterns", "source_refs": []},
        ],
        formula_families=[],
        lexical_config={"source_language": "en", "target_language": "es", "dictionary_type": "spanish_english"},
        planner_defaults={"weekly_minutes": 210, "default_energy_mode": "low"},
        assessment_defaults={"mode": "lexical", "question_count": 12},
        quality_gate_policy={"manual_confirm_required": True, "dictionary_quality_gate": True},
    ),
    CoursePack(
        pack_id="academic_english_vocabulary",
        title="Academic English Vocabulary",
        pack_type="language",
        description="Academic English vocabulary workflow for exam, writing, or reading preparation.",
        default_modules=MODULE_RECOMMENDATIONS["language"],
        suggested_imports=[
            {"import_type": "dictionary", "label": "Import academic English word list", "required": True},
            {"import_type": "resources", "label": "Import local reading passages or notes", "required": False},
        ],
        syllabus_seed=[
            {"topic_id": "academic-english-words", "title": "Academic word families", "source_refs": []},
            {"topic_id": "academic-english-usage", "title": "Register, collocation, and usage", "source_refs": []},
        ],
        formula_families=[],
        lexical_config={"source_language": "en", "target_language": "en", "dictionary_type": "english_english"},
        planner_defaults={"weekly_minutes": 240, "default_energy_mode": "normal"},
        assessment_defaults={"mode": "lexical", "question_count": 15},
        quality_gate_policy={"manual_confirm_required": True, "dictionary_quality_gate": True},
    ),
]
