"""Product navigation and premium cockpit summaries."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal


Tier = Literal["primary", "secondary", "advanced", "hidden"]
Audience = Literal["learner", "power_user", "system"]
Frequency = Literal["daily", "weekly", "occasional", "rare"]
ProductRole = Literal["learn", "plan", "reflect", "library", "tools", "settings", "system"]


@dataclass(frozen=True, slots=True)
class NavigationSurface:
    surface_id: str
    label: str
    route: str
    tier: Tier
    audience_label: Audience
    frequency: Frequency
    product_role: ProductRole
    visible_on_main: bool
    more_group: str | None
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


SURFACES: list[NavigationSurface] = [
    NavigationSurface("today", "Today", "/review", "primary", "learner", "daily", "learn", True, None, "Main learning cockpit."),
    NavigationSurface("focus_session", "Focus Session", "/review/focus", "primary", "learner", "daily", "learn", True, None, "One-button guided learning flow."),
    NavigationSurface("study_plan", "Study Plan", "/review/study-planner", "primary", "learner", "daily", "plan", True, None, "Today's plan and next block."),
    NavigationSurface("tutor", "Tutor", "/review/tutor", "primary", "learner", "daily", "learn", True, None, "Ask for grounded help."),
    NavigationSurface("review_session", "Review Session", "/review/lab", "secondary", "learner", "daily", "learn", False, "Library & Sources", "Recall-first practice surface."),
    NavigationSurface("assessments", "Assessments", "/review/assessments", "secondary", "learner", "weekly", "reflect", False, "Intelligence", "Periodic drills and checks."),
    NavigationSurface("analytics", "Progress", "/review/analytics", "secondary", "learner", "weekly", "reflect", False, "Intelligence", "Learning progress summary."),
    NavigationSurface("coverage", "Coverage", "/review/coverage", "secondary", "learner", "weekly", "library", False, "Library & Sources", "Syllabus coverage and gaps."),
    NavigationSurface("formulas", "Formula Lab", "/review/formulas", "secondary", "learner", "weekly", "learn", False, "Library & Sources", "Formula recall and calculator practice."),
    NavigationSurface("language_review", "Language Review", "/language/review", "secondary", "learner", "weekly", "learn", False, "Library & Sources", "Lexical review queue."),
    NavigationSurface("assets", "Assets", "/review/assets", "secondary", "power_user", "occasional", "library", False, "Library & Sources", "Source-backed review assets."),
    NavigationSurface("resources", "Resources", "/review/resources", "secondary", "power_user", "occasional", "library", False, "Library & Sources", "Resource quality and promotion."),
    NavigationSurface("knowledge_map", "Knowledge Map", "/review/knowledge-map", "advanced", "power_user", "occasional", "tools", False, "Intelligence", "Raw traceability map."),
    NavigationSurface("search", "Search", "/review/search", "advanced", "power_user", "occasional", "tools", False, "Intelligence", "Advanced source search."),
    NavigationSurface("data", "Data Governance", "/review/data", "advanced", "power_user", "rare", "settings", False, "System & Portability", "Backups, restore, and privacy controls."),
    NavigationSurface("interop", "Interop", "/review/interop", "advanced", "power_user", "rare", "tools", False, "System & Portability", "Local export/import utilities."),
    NavigationSurface("dictionaries", "Dictionaries", "/language/dictionaries", "advanced", "power_user", "occasional", "library", False, "Library & Sources", "Dictionary management."),
    NavigationSurface("mission", "Mission Control", "/review/mission-control", "secondary", "power_user", "weekly", "reflect", False, "Advanced / Diagnostics", "Action summary with optional diagnostics."),
    NavigationSurface("route_registry", "Route Registry", "/review/mission-control#route-registry", "advanced", "system", "rare", "system", False, "Advanced / Diagnostics", "Developer/system route checks."),
]

GROUPS = [
    ("library_sources", "Library & Sources"),
    ("intelligence", "Intelligence"),
    ("system_portability", "System & Portability"),
    ("advanced_diagnostics", "Advanced / Diagnostics"),
]


class NavigationService:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root)

    def summary(self) -> dict[str, Any]:
        surfaces = [surface.as_dict() for surface in SURFACES]
        return {
            "generated_at": _now(),
            "surfaces": surfaces,
            "main_visible_count": sum(1 for surface in SURFACES if surface.visible_on_main),
            "primary_count": sum(1 for surface in SURFACES if surface.tier == "primary"),
        }

    def tools(self) -> dict[str, Any]:
        groups = []
        for group_id, label in GROUPS:
            items = [
                surface.as_dict()
                for surface in SURFACES
                if surface.more_group == label and surface.route != "/review/mission-control#route-registry"
            ]
            groups.append({"group_id": group_id, "label": label, "items": items})
        return {"generated_at": _now(), "groups": groups}

    def cockpit(self, profile_id: str = "default") -> dict[str, Any]:
        profile_id = profile_id or "default"
        goal = self._active_goal(profile_id)
        plan = self._latest_plan(profile_id)
        blocks = [block for block in (plan or {}).get("blocks", []) if str(block.get("status") or "pending") != "completed"]
        next_block = blocks[0] if blocks else None

        if next_block:
            primary = {
                "label": "Start Today",
                "href": "/review/focus",
                "reason": str(next_block.get("due_reason") or "Run the next useful learning block inside Focus Session."),
            }
        else:
            primary = {
                "label": "Start Today",
                "href": "/review/focus",
                "reason": "Open a safe focus session; OpenExam will use today's plan or a minimal fallback.",
            }

        readiness = _readiness(goal)
        return {
            "profile_id": profile_id,
            "generated_at": _now(),
            "active_goal": _safe_goal(goal),
            "primary_action": primary,
            "supporting_actions": [
                {"label": "Study plan", "href": "/review/study-planner", "role": "plan"},
                {"label": "Ask tutor", "href": "/review/tutor", "role": "learn"},
                {"label": "Review progress", "href": "/review/analytics", "role": "reflect"},
            ],
            "today_plan_preview": [_safe_block(block) for block in blocks[:3]],
            "learning_health": {
                "readiness": readiness,
                "plan_status": str((plan or {}).get("status") or "not_planned"),
                "next_blocks": len(blocks),
                "quality_gate": "correct_only",
            },
        }

    def _active_goal(self, profile_id: str) -> dict[str, Any] | None:
        goals = self._records(self.repo_root / ".system" / "memory" / "goals" / "profiles")
        matching = [
            goal
            for goal in goals
            if str(goal.get("profile_id") or profile_id) == profile_id and str(goal.get("status") or "") == "active"
        ]
        return matching[0] if matching else None

    def _latest_plan(self, profile_id: str) -> dict[str, Any] | None:
        plans = [
            plan
            for plan in self._records(self.repo_root / ".system" / "memory" / "study-planner" / "plans")
            if str(plan.get("profile_id") or profile_id) == profile_id
        ]
        plans.sort(key=lambda item: str(item.get("generated_at") or item.get("plan_date") or ""), reverse=True)
        return plans[0] if plans else None

    def _records(self, root: Path) -> list[dict[str, Any]]:
        if not root.exists():
            return []
        records = []
        for path in sorted(root.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(payload, dict):
                records.append(payload)
        return records


def _safe_goal(goal: dict[str, Any] | None) -> dict[str, Any] | None:
    if not goal:
        return None
    return {
        "goal_id": goal.get("goal_id"),
        "profile_id": goal.get("profile_id"),
        "title": goal.get("title"),
        "goal_type": goal.get("goal_type"),
        "target_exam": goal.get("target_exam"),
        "target_language": goal.get("target_language"),
        "weekly_minutes": goal.get("weekly_minutes"),
        "readiness_status": _readiness(goal),
    }


def _safe_block(block: dict[str, Any]) -> dict[str, Any]:
    return {
        "block_id": block.get("block_id"),
        "title": block.get("title"),
        "target_minutes": block.get("target_minutes"),
        "launch_route": block.get("launch_route"),
        "due_reason": block.get("due_reason"),
        "status": block.get("status") or "pending",
    }


def _readiness(goal: dict[str, Any] | None) -> str:
    if not goal:
        return "not_started"
    onboarding = goal.get("onboarding_status") if isinstance(goal.get("onboarding_status"), dict) else {}
    return str(onboarding.get("readiness_status") or "active")


def _now() -> str:
    return datetime.now(tz=UTC).isoformat()
