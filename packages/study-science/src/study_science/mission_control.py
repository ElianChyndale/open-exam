from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from study_science.review_lab import ReviewLabEngine


EXPECTED_FEATURE_GROUPS: dict[str, list[str]] = {
    "daily_review_lab": ["daily_review_lab", "daily_review_lab_enabled"],
    "review_asset_ingestion": ["review_asset_ingestion_enabled"],
    "formula_lab": ["formula_lab", "formula_lab_enabled"],
    "syllabus_coverage": ["syllabus_coverage_enabled"],
    "mock_retro": ["mock_retro_enabled"],
    "resource_quality_gate": ["resource_quality_gate_enabled"],
    "language_os": ["language_os_enabled", "dictionary_kernel_enabled", "lexical_review_enabled"],
    "mission_control": ["mission_control_enabled", "integration_health_checks_enabled", "green_test_gate_enabled"],
    "study_planner": [
        "study_planner_enabled",
        "adaptive_session_orchestrator_enabled",
        "energy_aware_planning_enabled",
        "study_plan_retro_enabled",
    ],
    "focus_session": [
        "focus_session_enabled",
        "unified_study_flow_enabled",
        "focus_embedded_review_enabled",
        "focus_embedded_formula_enabled",
        "focus_embedded_language_enabled",
        "focus_embedded_assessment_enabled",
        "focus_tutor_hint_enabled",
    ],
    "learning_analytics": [
        "learning_analytics_enabled",
        "mastery_calibration_enabled",
        "plan_effectiveness_enabled",
        "resource_usefulness_enabled",
        "coverage_momentum_enabled",
        "correct_only_analytics_enabled",
    ],
    "adaptive_assessment": [
        "adaptive_assessment_enabled",
        "interleaving_drill_enabled",
        "assessment_feedback_correct_only_enabled",
        "assessment_transfer_gap_integration_enabled",
        "assessment_analytics_integration_enabled",
    ],
    "knowledge_graph": [
        "knowledge_graph_enabled",
        "global_search_enabled",
        "traceability_map_enabled",
        "impact_analysis_enabled",
        "correct_only_graph_enabled",
    ],
    "ux_accessibility": [
        "accessibility_hardening_enabled",
        "keyboard_shortcuts_enabled",
        "responsive_layout_hardening_enabled",
        "unified_ui_states_enabled",
        "ux_route_consistency_checks_enabled",
    ],
    "data_governance": [
        "data_governance_enabled",
        "safe_export_enabled",
        "full_export_enabled",
        "backup_restore_enabled",
        "category_reset_enabled",
        "privacy_redaction_enabled",
        "snapshot_rollback_enabled",
    ],
    "tutor_copilot": [
        "tutor_copilot_enabled",
        "grounded_tutor_retrieval_enabled",
        "tutor_source_citations_enabled",
        "tutor_correct_only_enabled",
        "tutor_conversation_memory_enabled",
    ],
    "goal_onboarding": [
        "goal_profiles_enabled",
        "course_packs_enabled",
        "first_run_onboarding_enabled",
        "day1_plan_enabled",
        "onboarding_readiness_enabled",
    ],
    "file_ingestion": [
        "file_ingestion_enabled",
        "pdf_text_extraction_enabled",
        "dictionary_file_import_enabled",
        "resource_file_import_enabled",
        "file_duplicate_detection_enabled",
    ],
}

EXPECTED_PAGES = [
    "/review/lab",
    "/review/assets",
    "/review/formulas",
    "/review/coverage",
    "/review/mock-retro",
    "/review/resources",
    "/review/mission-control",
    "/review/study-planner",
    "/review/focus",
    "/review/analytics",
    "/review/assessments",
    "/review/search",
    "/review/knowledge-map",
    "/review/data",
    "/review/tutor",
    "/review/goals",
    "/onboarding",
    "/language/dictionaries",
    "/language/review",
]

EXPECTED_API_ROUTES = [
    "/api/review-lab/mission-control",
    "/api/review-lab/route-registry",
    "/api/study-planner/generate",
    "/api/study-planner/today",
    "/api/study-planner/history",
    "/api/focus/start",
    "/api/focus/current",
    "/api/focus/{focus_id}",
    "/api/focus/{focus_id}/steps/{step_id}/start",
    "/api/focus/{focus_id}/steps/{step_id}/complete",
    "/api/focus/{focus_id}/steps/{step_id}/skip",
    "/api/focus/{focus_id}/complete",
    "/api/focus/{focus_id}/abandon",
    "/api/learning-analytics/summary",
    "/api/learning-analytics/events",
    "/api/learning-analytics/recompute",
    "/api/learning-analytics/calibration",
    "/api/learning-analytics/mastery-trends",
    "/api/learning-analytics/plan-effectiveness",
    "/api/learning-analytics/resource-usefulness",
    "/api/learning-analytics/coverage-momentum",
    "/api/learning-analytics/formula-outcomes",
    "/api/learning-analytics/language-outcomes",
    "/api/assessments/generate",
    "/api/assessments",
    "/api/assessments/recommendations",
    "/api/knowledge-graph/recompute",
    "/api/knowledge-graph/summary",
    "/api/knowledge-graph/nodes",
    "/api/knowledge-graph/nodes/{node_id}",
    "/api/knowledge-graph/nodes/{node_id}/trace",
    "/api/knowledge-graph/edges",
    "/api/knowledge-graph/search",
    "/api/knowledge-graph/impact/{node_id}",
    "/api/knowledge-graph/related/{node_id}",
    "/api/data-governance/inventory",
    "/api/data-governance/snapshots",
    "/api/data-governance/export",
    "/api/data-governance/restore/dry-run",
    "/api/data-governance/restore",
    "/api/data-governance/rollback/{snapshot_id}",
    "/api/data-governance/reset",
    "/api/data-governance/privacy-report",
    "/api/tutor/ask",
    "/api/tutor/search-context",
    "/api/tutor/suggestions",
    "/api/tutor/conversations",
    "/api/tutor/conversations/{conversation_id}",
    "/api/tutor/conversations/{conversation_id}/message",
    "/api/tutor/conversations/{conversation_id}/archive",
    "/api/goals/packs",
    "/api/goals",
    "/api/goals/{goal_id}",
    "/api/goals/{goal_id}/activate",
    "/api/goals/{goal_id}/archive",
    "/api/onboarding/state",
    "/api/onboarding/step",
    "/api/onboarding/skip-step",
    "/api/onboarding/generate-day1-plan",
    "/api/onboarding/readiness",
    "/api/onboarding/reset",
    "/api/review-lab/assets",
    "/api/review-lab/files",
    "/api/review-lab/sources/import-file",
    "/api/review-lab/resources/import-file",
    "/api/review-lab/formulas",
    "/api/review-lab/syllabus/coverage",
    "/api/review-lab/mock-retro/transfer-gaps",
    "/api/review-lab/resources",
    "/api/language-os/dictionaries",
    "/api/language-os/dictionaries/import-file",
    "/api/language-os/review/generate-session",
]


class MissionControlService:
    """Cross-system, correct-only operational summary for learning workflows."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.engine = ReviewLabEngine(self.repo_root)

    def summary(self, *, profile_id: str = "default") -> dict[str, Any]:
        profile_id = profile_id or "default"
        review_lab = self._review_lab_summary()
        assets = self._assets_summary(profile_id=profile_id)
        formulas = self._formula_summary(profile_id=profile_id)
        coverage = self._coverage_summary(profile_id=profile_id)
        mock_retro = self._mock_retro_summary(profile_id=profile_id)
        resources = self._resource_summary(profile_id=profile_id)
        language = self._language_summary(profile_id=profile_id)
        data_governance = self._data_governance_summary(profile_id=profile_id)
        tutor = self._tutor_summary(profile_id=profile_id)
        goals = self._goals_summary(profile_id=profile_id)
        system_health = {
            "green_test_gate": "runtime_summary_available",
            "test_status_hook": "not_runtime_evaluated",
            "route_registry_available": True,
            "dirty_state_note": "Working tree status is reported by validation, not this runtime endpoint.",
        }
        recommended_actions = self._recommended_actions(
            review_lab=review_lab,
            assets=assets,
            formulas=formulas,
            coverage=coverage,
            mock_retro=mock_retro,
            resources=resources,
            language=language,
            data_governance=data_governance,
            tutor=tutor,
            goals=goals,
        )
        return {
            "profile_id": profile_id,
            "generated_at": datetime.now(UTC).isoformat(),
            "active_goal": goals.get("active_goal"),
            "onboarding": goals.get("onboarding"),
            "review_lab": review_lab,
            "assets": assets,
            "formulas": formulas,
            "coverage": coverage,
            "mock_retro": mock_retro,
            "resources": resources,
            "language": language,
            "data_governance": data_governance,
            "tutor": tutor,
            "goals": goals,
            "system_health": system_health,
            "recommended_actions": recommended_actions,
        }

    def route_registry(self, *, flags: Any, mounted_paths: set[str]) -> dict[str, Any]:
        feature_groups = {
            group: {
                "flags": {flag: bool(flags.enabled(flag)) for flag in names},
                "exists": all(flag in flags.values for flag in names),
                "enabled": any(flags.enabled(flag) for flag in names),
            }
            for group, names in EXPECTED_FEATURE_GROUPS.items()
        }
        return {
            "generated_at": datetime.now(UTC).isoformat(),
            "feature_groups": feature_groups,
            "expected_pages": [{"path": page, "implemented": True} for page in EXPECTED_PAGES],
            "expected_api_routes": [
                {"path": route, "mounted": route in mounted_paths}
                for route in EXPECTED_API_ROUTES
            ],
        }

    def _review_lab_summary(self) -> dict[str, Any]:
        payload = self._safe(lambda: self.engine.get_today_units(max_units=50), {"units": []})
        units = list(payload.get("units") or [])
        active = self._safe(lambda: self.engine._latest_active_session(), None)
        return {
            "due_count": len(units),
            "next_session_available": bool(units),
            "weak_asset_count": sum(1 for unit in units if str(unit.get("memory_state_before", "")).lower() in {"new", "learning", "weak"}),
            "active_session_id": getattr(active, "session_id", "") if active else "",
            "status": "ready" if units else "empty",
        }

    def _assets_summary(self, *, profile_id: str) -> dict[str, Any]:
        items = self._safe(lambda: self.engine.list_ingested_assets(profile_id=profile_id), [])
        counts = self._count_by(items, "validation_status", ["draft", "needs_review", "confirmed", "rejected"])
        return {
            **counts,
            "total": len(items),
            "needs_confirmation_count": counts["draft"] + counts["needs_review"],
            "ready_for_review_count": counts["confirmed"],
        }

    def _formula_summary(self, *, profile_id: str) -> dict[str, Any]:
        formulas = self._safe(lambda: self.engine.list_formula_assets(profile_id=profile_id), [])
        due = [item for item in formulas if item.get("validation_status") in {"confirmed", "validated", "derived"} and self._is_due(item.get("next_review_at"))]
        weak = [
            item for item in formulas
            if str(item.get("mastery_state", "")).lower() in {"", "new", "learning", "weak"}
            or not item.get("ba_ii_plus_steps")
        ]
        return {
            "total": len(formulas),
            "due_formula_count": len(due),
            "weak_formula_count": len(weak),
            "ba_ii_plus_gap_count": sum(1 for item in formulas if not item.get("ba_ii_plus_steps")),
            "confirmed_count": sum(1 for item in formulas if item.get("validation_status") == "confirmed"),
        }

    def _coverage_summary(self, *, profile_id: str) -> dict[str, Any]:
        payload = self._safe(lambda: self.engine.recompute_syllabus_coverage(profile_id=profile_id), {})
        summary = {
            "missing": 0,
            "partial": 0,
            "draft_only": 0,
            "weak": 0,
            "stale": 0,
            "covered": 0,
            **dict(payload.get("summary") or {}),
        }
        return {
            "topic_count": int(payload.get("topic_count", 0) or 0),
            "asset_count": int(payload.get("asset_count", 0) or 0),
            "link_count": int(payload.get("link_count", 0) or 0),
            **summary,
        }

    def _mock_retro_summary(self, *, profile_id: str) -> dict[str, Any]:
        gaps = self._safe(lambda: self.engine.list_transfer_gaps(profile_id=profile_id, status="open"), [])
        types = Counter(str(gap.get("gap_type", "unknown")) for gap in gaps)
        return {
            "open_transfer_gap_count": len(gaps),
            "top_gap_types": [{"gap_type": key, "count": value} for key, value in types.most_common(5)],
            "highest_severity": max([float(gap.get("severity", 0.0) or 0.0) for gap in gaps], default=0.0),
        }

    def _resource_summary(self, *, profile_id: str) -> dict[str, Any]:
        report = self._safe(lambda: self.engine.resource_quality_report(profile_id=profile_id), {})
        summary = {
            "unscored": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
            "trusted": 0,
            "rejected": 0,
            **dict(report.get("summary") or {}),
        }
        return {
            "resource_count": int(report.get("resource_count", 0) or 0),
            "candidate_asset_count": int(report.get("candidate_asset_count", 0) or 0),
            "promoted_asset_count": int(report.get("promoted_asset_count", 0) or 0),
            "candidates_needing_promotion": max(0, int(report.get("candidate_asset_count", 0) or 0) - int(report.get("promoted_asset_count", 0) or 0)),
            **summary,
        }

    def _language_summary(self, *, profile_id: str) -> dict[str, Any]:
        try:
            from language_science.lexical_kernel import LexicalKernel
        except ImportError:
            return {
                "due_lexical_count": 0,
                "draft_lexical_count": 0,
                "weak_lexical_count": 0,
                "confirmed_lexical_count": 0,
                "dictionary_count": 0,
                "status": "language_kernel_unavailable",
            }
        kernel = LexicalKernel(self.repo_root)
        assets = self._safe(lambda: kernel.list_lexical_assets(profile_id=profile_id), [])
        dictionaries = self._safe(lambda: kernel.list_dictionaries(profile_id=profile_id), [])
        return {
            "due_lexical_count": sum(1 for item in assets if item.get("validation_status") == "confirmed" and self._is_due(item.get("next_review_at"))),
            "draft_lexical_count": sum(1 for item in assets if item.get("validation_status") in {"draft", "needs_review"}),
            "weak_lexical_count": sum(1 for item in assets if str(item.get("mastery_state", "")).lower() in {"", "new", "learning"}),
            "confirmed_lexical_count": sum(1 for item in assets if item.get("validation_status") == "confirmed"),
            "dictionary_count": len(dictionaries),
            "status": "ready" if assets or dictionaries else "empty",
        }

    def _data_governance_summary(self, *, profile_id: str) -> dict[str, Any]:
        try:
            from study_science.data_governance import DataGovernanceService

            return DataGovernanceService(self.repo_root).governance_summary(profile_id=profile_id)
        except Exception as exc:
            return {
                "backup_health": "unavailable",
                "error": str(exc),
                "local_state_size_bytes": 0,
                "raw_diagnostic_categories": [],
                "backup_count": 0,
            }

    def _tutor_summary(self, *, profile_id: str) -> dict[str, Any]:
        try:
            from study_science.tutor import TutorService

            return TutorService(self.repo_root).governance_summary(profile_id=profile_id)
        except Exception as exc:
            return {
                "conversation_count": 0,
                "active_conversation_count": 0,
                "last_conversation_at": None,
                "snapshot_route": "/review/tutor",
                "error": str(exc),
            }

    def _goals_summary(self, *, profile_id: str) -> dict[str, Any]:
        try:
            from study_science.goals import GoalOnboardingService

            service = GoalOnboardingService(self.repo_root)
            active = service.get_active_goal()
            onboarding = service.onboarding_state(profile_id=active.profile_id if active else "")
            return {
                "goal_count": service.list_goals(include_archived=True)["count"],
                "active_goal": active.as_dict() if active else None,
                "onboarding": onboarding,
                "readiness_score": onboarding["readiness_score"],
                "readiness_status": onboarding["readiness_status"],
                "snapshot_route": "/review/goals",
            }
        except Exception as exc:
            return {
                "goal_count": 0,
                "active_goal": None,
                "onboarding": {
                    "readiness_status": "unavailable",
                    "readiness_score": 0,
                    "blockers": [],
                },
                "readiness_score": 0,
                "readiness_status": "unavailable",
                "snapshot_route": "/review/goals",
                "error": str(exc),
            }

    def _recommended_actions(self, **summaries: dict[str, Any]) -> list[dict[str, Any]]:
        actions: list[dict[str, Any]] = []
        review_lab = summaries["review_lab"]
        assets = summaries["assets"]
        formulas = summaries["formulas"]
        coverage = summaries["coverage"]
        mock_retro = summaries["mock_retro"]
        resources = summaries["resources"]
        language = summaries["language"]
        data_governance = summaries.get("data_governance", {})
        tutor = summaries.get("tutor", {})
        goals = summaries.get("goals", {})
        study_ready = any(
            [
                review_lab.get("due_count"),
                formulas.get("due_formula_count"),
                formulas.get("weak_formula_count"),
                language.get("due_lexical_count"),
                mock_retro.get("open_transfer_gap_count"),
            ]
        )

        if study_ready:
            actions.append(self._action(101, "start_focus_session", "Start Focus Session", "/review/focus", "Run today as one guided task at a time using confirmed local learning signals."))

        if not goals.get("active_goal"):
            actions.append(self._action(100, "start_onboarding", "Start first-run onboarding", "/onboarding", "Choose a goal profile, course pack, time budget, and safe Day-1 plan."))
        else:
            readiness_status = goals.get("readiness_status", "not_started")
            if readiness_status not in {"ready_for_review", "active"}:
                actions.append(self._action(96, "continue_onboarding", "Continue onboarding readiness", "/onboarding", f"Current goal readiness is {readiness_status}."))
            actions.append(self._action(92, "review_goals", "Review active goal profile", "/review/goals", "Adjust modules, course pack, weekly minutes, and onboarding progress."))
        actions.append(self._action(98, "ask_tutor_copilot", "Ask grounded Tutor Copilot", "/review/tutor", "Use cited local context before choosing a review action."))
        actions.append(self._action(99, "generate_study_plan", "Generate today's adaptive study plan", "/review/study-planner", "Turn Mission Control signals into an executable energy-aware session."))
        if not tutor.get("conversation_count"):
            actions.append(self._action(89, "start_tutor_conversation", "Start first Tutor conversation", "/review/tutor", "Tutor can explain formulas, sources, weak topics, and next actions using local evidence."))
        if data_governance.get("backup_health") in {"never_backed_up", "stale", "unavailable"}:
            actions.append(self._action(97, "create_safe_backup", "Create safe local backup", "/review/data", "Export a redacted backup before more local state accumulates."))
        actions.append(self._action(93, "generate_assessment", "Generate adaptive assessment drill", "/review/assessments", "Test transfer across confirmed assets, coverage gaps, formulas, lexical items, and open gaps."))
        if review_lab["due_count"]:
            actions.append(self._action(95, "review_today", "Review today's Review Lab session", "/review/lab", f"{review_lab['due_count']} recall-first units are ready."))
        if assets["needs_confirmation_count"]:
            actions.append(self._action(88, "confirm_assets", "Confirm draft review assets", "/review/assets", f"{assets['needs_confirmation_count']} source-backed assets are blocked from review."))
        coverage_gap_count = coverage["missing"] + coverage["partial"] + coverage["weak"] + coverage["stale"] + coverage["draft_only"]
        if coverage_gap_count:
            actions.append(self._action(82, "close_coverage_gaps", "Inspect syllabus coverage gaps", "/review/coverage", f"{coverage_gap_count} syllabus topics are missing, weak, stale, partial, or draft-only."))
        if formulas["weak_formula_count"] or formulas["due_formula_count"]:
            actions.append(self._action(78, "run_formula_lab", "Run Formula Lab for weak formulas", "/review/formulas", f"{formulas['weak_formula_count']} formula assets need recall or BA II Plus reinforcement."))
        if mock_retro["open_transfer_gap_count"]:
            top = mock_retro["top_gap_types"][0]["gap_type"] if mock_retro["top_gap_types"] else "transfer_gap"
            actions.append(self._action(76, "resolve_transfer_gaps", "Review open mock transfer gaps", "/review/mock-retro", f"{mock_retro['open_transfer_gap_count']} open gaps remain; top type is {top}."))
        if resources["candidates_needing_promotion"] or resources["low"]:
            actions.append(self._action(72, "resource_quality_gate", "Promote or fix resource-backed candidates", "/review/resources", f"{resources['candidates_needing_promotion']} candidates need promotion and {resources['low']} resources are low quality."))
        if language["draft_lexical_count"]:
            actions.append(self._action(68, "confirm_lexical_assets", "Confirm dictionary lexical assets", "/language/dictionaries", f"{language['draft_lexical_count']} lexical assets cannot enter review until confirmed."))
        if language["due_lexical_count"]:
            actions.append(self._action(64, "lexical_review", "Run LanguageOS lexical review", "/language/review", f"{language['due_lexical_count']} lexical items are due."))
        if not actions:
            actions.append(self._action(10, "empty_state_setup", "Import or confirm learning sources", "/review/assets", "No urgent review actions are ready yet."))
        return sorted(actions, key=lambda item: item["priority"], reverse=True)

    @staticmethod
    def _action(priority: int, action_id: str, title: str, href: str, reason: str) -> dict[str, Any]:
        return {
            "priority": priority,
            "action_id": action_id,
            "title": title,
            "href": href,
            "reason": reason,
        }

    @staticmethod
    def _count_by(items: list[dict[str, Any]], key: str, expected: list[str]) -> dict[str, int]:
        counts = {item: 0 for item in expected}
        for item in items:
            value = str(item.get(key, ""))
            if value in counts:
                counts[value] += 1
        return counts

    @staticmethod
    def _is_due(value: Any) -> bool:
        if not value:
            return True
        try:
            parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError:
            return True
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed <= datetime.now(UTC)

    @staticmethod
    def _safe(call: Callable[[], Any], fallback: Any) -> Any:
        try:
            return call()
        except Exception:
            return fallback
