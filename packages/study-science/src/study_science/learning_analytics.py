"""Correct-only learning analytics projections.

This module reads local OpenExam state and projects it into aggregate learning
metrics without exposing raw wrong-answer fields.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from hashlib import sha1
import json
from pathlib import Path
from typing import Any, Literal

from study_science.data_governance import FORBIDDEN_SAFE_PAYLOAD_KEYS, sanitize_payload

WRONG_KEYS = FORBIDDEN_SAFE_PAYLOAD_KEYS
ReviewOutcome = Literal["recalled", "partial", "forgot", "skipped"]


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _stable_id(prefix: str, *parts: Any) -> str:
    text = "|".join(str(part) for part in parts)
    return f"{prefix}-{sha1(text.encode('utf-8')).hexdigest()[:16]}"


def _parse_time(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed


def _range_start(range_key: str) -> datetime | None:
    normalized = (range_key or "30d").lower()
    now = datetime.now(UTC)
    if normalized in {"all", "all_time"}:
        return None
    if normalized in {"today", "1d"}:
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    if normalized in {"7d", "7days", "week"}:
        return now - timedelta(days=7)
    return now - timedelta(days=30)


def _success_value(outcome: str | None) -> float | None:
    return {
        "recalled": 1.0,
        "correct": 1.0,
        "completed": 1.0,
        "partial": 0.5,
        "forgot": 0.0,
        "incorrect": 0.0,
        "skipped": 0.0,
    }.get(str(outcome or "").lower())


@dataclass(slots=True)
class LearningAnalyticsEvent:
    event_id: str
    profile_id: str
    event_type: str
    occurred_at: str
    subsystem: Literal[
        "review_lab",
        "formula_lab",
        "language_os",
        "study_planner",
        "coverage",
        "mock_retro",
        "resource_os",
        "file_ingestion",
        "assets",
        "assessment",
    ]
    asset_id: str | None = None
    topic_id: str | None = None
    lexical_id: str | None = None
    formula_family: str | None = None
    plan_id: str | None = None
    block_id: str | None = None
    outcome: str | None = None
    confidence_before: float | None = None
    confidence_after: float | None = None
    time_spent_seconds: int | None = None
    source_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return strip_wrong_fields(
            {
                "event_id": self.event_id,
                "profile_id": self.profile_id,
                "event_type": self.event_type,
                "occurred_at": self.occurred_at,
                "subsystem": self.subsystem,
                "asset_id": self.asset_id,
                "topic_id": self.topic_id,
                "lexical_id": self.lexical_id,
                "formula_family": self.formula_family,
                "plan_id": self.plan_id,
                "block_id": self.block_id,
                "outcome": self.outcome,
                "confidence_before": self.confidence_before,
                "confidence_after": self.confidence_after,
                "time_spent_seconds": self.time_spent_seconds,
                "source_refs": self.source_refs,
                "metadata": self.metadata,
            }
        )


@dataclass(slots=True)
class MasteryCalibrationRecord:
    record_id: str
    profile_id: str
    scope_type: Literal["asset", "topic", "formula", "lexical", "plan", "global"]
    scope_id: str
    recall_attempts: int
    recalled_count: int
    partial_count: int
    forgot_count: int
    skipped_count: int
    average_confidence_before: float | None
    average_confidence_after: float | None
    calibration_error: float | None
    overconfidence_count: int
    underconfidence_count: int
    transfer_gap_count: int
    mastery_trend: Literal["improving", "stable", "declining", "unknown"]
    last_updated_at: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "profile_id": self.profile_id,
            "scope_type": self.scope_type,
            "scope_id": self.scope_id,
            "recall_attempts": self.recall_attempts,
            "recalled_count": self.recalled_count,
            "partial_count": self.partial_count,
            "forgot_count": self.forgot_count,
            "skipped_count": self.skipped_count,
            "average_confidence_before": self.average_confidence_before,
            "average_confidence_after": self.average_confidence_after,
            "calibration_error": self.calibration_error,
            "overconfidence_count": self.overconfidence_count,
            "underconfidence_count": self.underconfidence_count,
            "transfer_gap_count": self.transfer_gap_count,
            "mastery_trend": self.mastery_trend,
            "last_updated_at": self.last_updated_at,
        }


class LearningAnalyticsService:
    """Read local state and compute correct-only learning analytics."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.analytics_root = self.repo_root / ".system" / "memory" / "learning-analytics"
        self.analytics_root.mkdir(parents=True, exist_ok=True)
        self.review_root = self.repo_root / ".system" / "memory" / "review"
        self.language_root = self.repo_root / ".system" / "memory" / "language" / "dictionary-kernel"
        self.planner_root = self.repo_root / ".system" / "memory" / "study-planner"

    def recompute(self, *, profile_id: str = "default", range_key: str = "30d") -> dict[str, Any]:
        events = self.events(profile_id=profile_id, range_key=range_key)
        summary = self.summary(profile_id=profile_id, range_key=range_key, events=events)
        self._write_projection(profile_id, events, summary)
        return {
            "profile_id": profile_id or "default",
            "generated_at": summary["generated_at"],
            "event_count": len(events),
            "summary": summary,
        }

    def events(self, *, profile_id: str = "default", range_key: str = "30d") -> list[dict[str, Any]]:
        profile_id = profile_id or "default"
        events: list[LearningAnalyticsEvent] = []
        events.extend(self._review_events(profile_id))
        events.extend(self._language_events(profile_id))
        events.extend(self._study_plan_events(profile_id))
        events.extend(self._coverage_events(profile_id))
        events.extend(self._transfer_gap_events(profile_id))
        events.extend(self._resource_events(profile_id))
        events.extend(self._asset_events(profile_id))
        events.extend(self._file_events(profile_id))
        events.extend(self._assessment_events(profile_id))
        events = self._filter_range(events, range_key)
        events.sort(key=lambda event: event.occurred_at, reverse=True)
        return [event.as_dict() for event in events]

    def summary(
        self,
        *,
        profile_id: str = "default",
        range_key: str = "30d",
        events: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        profile_id = profile_id or "default"
        events = events if events is not None else self.events(profile_id=profile_id, range_key=range_key)
        calibration = self.calibration_records(profile_id=profile_id, range_key=range_key, events=events)
        plan = self.plan_effectiveness(profile_id=profile_id, range_key=range_key, events=events)
        resources = self.resource_usefulness(profile_id=profile_id, range_key=range_key, events=events)
        coverage = self.coverage_momentum(profile_id=profile_id, range_key=range_key, events=events)
        formulas = self.formula_outcomes(profile_id=profile_id, range_key=range_key, events=events)
        language = self.language_outcomes(profile_id=profile_id, range_key=range_key, events=events)
        review = self._review_summary(events)
        mock = self._mock_summary(events)
        file_summary = self._file_summary(events)
        global_record = next((record for record in calibration if record["scope_type"] == "global"), None)
        overall_success = self._success_rate(events)
        summary = {
            "profile_id": profile_id,
            "generated_at": _now(),
            "date_range": {"range": range_key, "start": (_range_start(range_key).isoformat() if _range_start(range_key) else None), "end": _now()},
            "overall": {
                "event_count": len(events),
                "recall_success_rate": overall_success,
                "mastery_trend": (global_record or {}).get("mastery_trend", "unknown"),
                "active_subsystems": sorted({event["subsystem"] for event in events}),
            },
            "review_lab": review,
            "formula_lab": formulas,
            "language_os": language,
            "study_planner": plan,
            "coverage": coverage,
            "mock_retro": mock,
            "resource_os": resources,
            "file_ingestion": file_summary,
            "calibration": {
                "record_count": len(calibration),
                "overconfidence_count": sum(record["overconfidence_count"] for record in calibration if record["scope_type"] == "global"),
                "underconfidence_count": sum(record["underconfidence_count"] for record in calibration if record["scope_type"] == "global"),
                "average_calibration_error": (global_record or {}).get("calibration_error"),
                "records": calibration[:20],
            },
        }
        summary["recommended_strategy_adjustments"] = self.strategy_adjustments(summary)
        return strip_wrong_fields(summary)

    def calibration_records(
        self,
        *,
        profile_id: str = "default",
        range_key: str = "30d",
        events: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        events = events if events is not None else self.events(profile_id=profile_id, range_key=range_key)
        groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for event in events:
            if event.get("outcome") in {"recalled", "partial", "forgot", "skipped"}:
                groups[("global", "global")].append(event)
                if event.get("asset_id"):
                    groups[("asset", event["asset_id"])].append(event)
                if event.get("topic_id"):
                    groups[("topic", event["topic_id"])].append(event)
                if event.get("formula_family"):
                    groups[("formula", event["formula_family"])].append(event)
                if event.get("lexical_id"):
                    groups[("lexical", event["lexical_id"])].append(event)
                if event.get("plan_id"):
                    groups[("plan", event["plan_id"])].append(event)
        gap_events = [event for event in events if event.get("subsystem") == "mock_retro"]
        if gap_events and ("global", "global") not in groups:
            groups[("global", "global")] = []

        records = [self._calibration_record(profile_id or "default", scope_type, scope_id, items, gap_events) for (scope_type, scope_id), items in groups.items()]
        records.sort(key=lambda record: (record.scope_type != "global", -record.overconfidence_count, -record.recall_attempts, record.scope_id))
        return [record.as_dict() for record in records]

    def mastery_trends(self, *, profile_id: str = "default", range_key: str = "30d") -> list[dict[str, Any]]:
        records = self.calibration_records(profile_id=profile_id, range_key=range_key)
        return [record for record in records if record["scope_type"] != "global"]

    def plan_effectiveness(
        self,
        *,
        profile_id: str = "default",
        range_key: str = "30d",
        events: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        events = events if events is not None else self.events(profile_id=profile_id, range_key=range_key)
        block_events = [event for event in events if event.get("subsystem") == "study_planner" and event.get("event_type") == "study_plan_block"]
        plan_ids = {event.get("plan_id") for event in block_events if event.get("plan_id")}
        completed = [event for event in block_events if event.get("outcome") == "completed"]
        skipped = [event for event in block_events if event.get("outcome") == "skipped"]
        blocked = [event for event in block_events if event.get("outcome") == "blocked"]
        by_type: dict[str, dict[str, int]] = {}
        for event in block_events:
            block_type = event.get("metadata", {}).get("block_type", "unknown")
            by_type.setdefault(block_type, {"completed": 0, "skipped": 0, "blocked": 0, "total": 0})
            by_type[block_type]["total"] += 1
            if event.get("outcome") in by_type[block_type]:
                by_type[block_type][event["outcome"]] += 1
        planned_minutes = sum(int(event.get("metadata", {}).get("target_minutes", 0) or 0) for event in block_events)
        completed_minutes = sum(int(event.get("metadata", {}).get("target_minutes", 0) or 0) for event in completed)
        return {
            "plan_count": len(plan_ids),
            "block_count": len(block_events),
            "completed_blocks": len(completed),
            "skipped_blocks": len(skipped),
            "blocked_blocks": len(blocked),
            "block_completion_rate": round(len(completed) / max(1, len(block_events)), 4),
            "plan_completion_rate": round(len([event for event in events if event.get("event_type") == "study_plan_completed"]) / max(1, len(plan_ids)), 4) if plan_ids else 0.0,
            "planned_minutes": planned_minutes,
            "completed_minutes": completed_minutes,
            "planned_vs_completed_minutes": {"planned": planned_minutes, "completed": completed_minutes},
            "high_value_block_completion_rate": self._high_value_completion_rate(block_events),
            "block_completion_by_type": by_type,
            "recurring_blocked_reasons": Counter(str(event.get("metadata", {}).get("blocked_reason", "")) for event in blocked if event.get("metadata", {}).get("blocked_reason")).most_common(5),
        }

    def resource_usefulness(
        self,
        *,
        profile_id: str = "default",
        range_key: str = "30d",
        events: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        events = events if events is not None else self.events(profile_id=profile_id, range_key=range_key)
        resource_events = [event for event in events if event.get("subsystem") == "resource_os"]
        asset_events = [
            event for event in events
            if event.get("event_type") in {"asset_validation", "resource_asset_promoted"}
            and event.get("metadata", {}).get("resource_id")
        ]
        resources: dict[str, dict[str, Any]] = {}
        for event in resource_events:
            resource_id = event.get("metadata", {}).get("resource_id")
            if not resource_id:
                continue
            item = resources.setdefault(
                resource_id,
                {
                    "resource_id": resource_id,
                    "quality_status": event.get("metadata", {}).get("quality_status", "unscored"),
                    "quality_score": float(event.get("metadata", {}).get("quality_score", 0.0) or 0.0),
                    "imported": 0,
                    "scored": 0,
                    "confirmed": 0,
                    "rejected": 0,
                    "candidate_assets": 0,
                    "promoted_assets": 0,
                    "reviewed_promoted_assets": 0,
                    "average_recall_success": 0.0,
                    "resource_usefulness_score": 0.0,
                },
            )
            if event.get("event_type") == "resource_imported":
                item["imported"] += 1
                item["quality_status"] = event.get("metadata", {}).get("quality_status", item["quality_status"])
                item["quality_score"] = float(event.get("metadata", {}).get("quality_score", item["quality_score"]) or 0.0)
            if item["quality_status"] != "unscored":
                item["scored"] = 1
            if event.get("metadata", {}).get("validation_status") == "confirmed":
                item["confirmed"] = 1
            if event.get("metadata", {}).get("validation_status") == "rejected":
                item["rejected"] = 1
        for event in asset_events:
            resource_id = event.get("metadata", {}).get("resource_id")
            if resource_id and resource_id in resources:
                resources[resource_id]["candidate_assets"] += 1
                if event.get("metadata", {}).get("resource_promoted_at"):
                    resources[resource_id]["promoted_assets"] += 1
        review_by_asset = {event.get("asset_id"): event for event in events if event.get("asset_id") and event.get("outcome") in {"recalled", "partial", "forgot", "skipped"}}
        for item in resources.values():
            promoted_asset_ids = [
                event.get("asset_id") for event in asset_events
                if event.get("metadata", {}).get("resource_id") == item["resource_id"]
                and event.get("metadata", {}).get("resource_promoted_at")
            ]
            reviewed = [review_by_asset[asset_id] for asset_id in promoted_asset_ids if asset_id in review_by_asset]
            item["reviewed_promoted_assets"] = len(reviewed)
            successes = [_success_value(event.get("outcome")) or 0.0 for event in reviewed]
            item["average_recall_success"] = round(sum(successes) / len(successes), 4) if successes else 0.0
            item["resource_usefulness_score"] = round(
                0.35 * min(item["promoted_assets"] / 5, 1.0)
                + 0.25 * min(item["reviewed_promoted_assets"] / 5, 1.0)
                + 0.20 * item["average_recall_success"]
                + 0.10 * min(item["candidate_assets"] / 5, 1.0)
                + 0.10 * min(item["quality_score"], 1.0),
                4,
            )
        ordered = sorted(resources.values(), key=lambda item: item["resource_usefulness_score"], reverse=True)
        return {
            "resources_imported": sum(item["imported"] for item in ordered),
            "resources_scored": sum(item["scored"] for item in ordered),
            "resources_confirmed": sum(item["confirmed"] for item in ordered),
            "resources_rejected": sum(item["rejected"] for item in ordered),
            "candidate_assets": sum(item["candidate_assets"] for item in ordered),
            "promoted_assets": sum(item["promoted_assets"] for item in ordered),
            "reviewed_promoted_assets": sum(item["reviewed_promoted_assets"] for item in ordered),
            "average_resource_usefulness": round(sum(item["resource_usefulness_score"] for item in ordered) / max(1, len(ordered)), 4),
            "resources": ordered,
        }

    def coverage_momentum(
        self,
        *,
        profile_id: str = "default",
        range_key: str = "30d",
        events: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        events = events if events is not None else self.events(profile_id=profile_id, range_key=range_key)
        coverage_events = [event for event in events if event.get("subsystem") == "coverage"]
        counts = Counter(event.get("metadata", {}).get("coverage_status", "unknown") for event in coverage_events)
        high_weight_missing = [
            event for event in coverage_events
            if event.get("metadata", {}).get("coverage_status") == "missing"
            and float(event.get("metadata", {}).get("exam_weight", 0.0) or 0.0) >= 0.75
        ]
        return {
            "topic_count": len(coverage_events),
            "covered": counts.get("covered", 0),
            "partial": counts.get("partial", 0),
            "draft_only": counts.get("draft_only", 0),
            "missing": counts.get("missing", 0),
            "weak": counts.get("weak", 0),
            "stale": counts.get("stale", 0),
            "coverage_gap_count": counts.get("missing", 0) + counts.get("partial", 0) + counts.get("draft_only", 0) + counts.get("weak", 0) + counts.get("stale", 0),
            "persistent_missing_high_weight_topics": [
                {"topic_id": event.get("topic_id"), "exam_weight": event.get("metadata", {}).get("exam_weight")}
                for event in high_weight_missing[:10]
            ],
            "transitions": {
                "missing_to_draft_only": 0,
                "draft_only_to_partial": 0,
                "partial_to_covered": 0,
                "newly_covered_high_weight_topics": sum(1 for event in coverage_events if event.get("metadata", {}).get("coverage_status") == "covered" and float(event.get("metadata", {}).get("exam_weight", 0) or 0) >= 0.75),
            },
        }

    def formula_outcomes(
        self,
        *,
        profile_id: str = "default",
        range_key: str = "30d",
        events: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        events = events if events is not None else self.events(profile_id=profile_id, range_key=range_key)
        formula_events = [event for event in events if event.get("subsystem") == "formula_lab"]
        gap_events = [event for event in events if event.get("subsystem") == "mock_retro"]
        gap_counts = Counter(event.get("metadata", {}).get("gap_type", "unknown") for event in gap_events)
        return {
            "attempts": len(formula_events),
            "recall_success_rate": self._success_rate(formula_events),
            "calculator_procedure_gap_count": gap_counts.get("calculator_procedure_gap", 0),
            "variable_confusion_count": gap_counts.get("variable_confusion", 0),
            "boundary_confusion_count": gap_counts.get("boundary_confusion", 0),
            "formula_recall_gap_count": gap_counts.get("formula_recall_gap", 0),
            "ba_ii_plus_step_weakness_count": sum(1 for event in formula_events if event.get("metadata", {}).get("needed_hint") or "ba_ii" in str(event.get("metadata", {}).get("display_mode", ""))),
            "by_formula_family": self._success_by_key(formula_events, "formula_family"),
        }

    def language_outcomes(
        self,
        *,
        profile_id: str = "default",
        range_key: str = "30d",
        events: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        events = events if events is not None else self.events(profile_id=profile_id, range_key=range_key)
        language_events = [event for event in events if event.get("subsystem") == "language_os"]
        production = [event for event in language_events if event.get("metadata", {}).get("review_mode_group") == "production"]
        recognition = [event for event in language_events if event.get("metadata", {}).get("review_mode_group") == "recognition"]
        weakness_tags = Counter(tag for event in language_events for tag in event.get("metadata", {}).get("weakness_tags", []))
        return {
            "attempts": len(language_events),
            "recognition_attempts": len(recognition),
            "production_attempts": len(production),
            "recognition_success_rate": self._success_rate(recognition),
            "production_success_rate": self._success_rate(production),
            "translation_gap_count": weakness_tags.get("translation_gap", 0),
            "collocation_gap_count": weakness_tags.get("collocation_gap", 0) + weakness_tags.get("collocation_confusion", 0),
            "morphology_gap_count": weakness_tags.get("morphology_gap", 0),
            "sense_confusion_count": weakness_tags.get("sense_confusion", 0),
            "weakness_tags": dict(weakness_tags),
        }

    def strategy_adjustments(self, summary: dict[str, Any]) -> list[dict[str, Any]]:
        adjustments: list[dict[str, Any]] = []
        if summary["study_planner"]["block_completion_rate"] < 0.6 and summary["study_planner"]["block_count"]:
            adjustments.append(self._adjustment(94, "use_low_energy_plan_mode", "Use low-energy plan mode; plan adherence is low.", "/review/study-planner"))
        if summary["formula_lab"]["calculator_procedure_gap_count"] or summary["formula_lab"]["ba_ii_plus_step_weakness_count"]:
            adjustments.append(self._adjustment(90, "increase_formula_lab", "Increase Formula Lab; calculator/procedure gaps remain.", "/review/formulas"))
        if summary["mock_retro"]["open_transfer_gap_count"]:
            adjustments.append(self._adjustment(86, "increase_transfer_drills", "Increase transfer drills; mock transfer gaps are recurring.", "/review/mock-retro"))
        if summary["coverage"]["coverage_gap_count"]:
            adjustments.append(self._adjustment(82, "review_coverage_gaps", "Review coverage gaps before adding more resources.", "/review/coverage"))
        if summary["language_os"]["production_success_rate"] < summary["language_os"]["recognition_success_rate"]:
            adjustments.append(self._adjustment(78, "focus_lexical_production", "Focus on lexical production; recognition is stronger than production.", "/language/review"))
        if summary["resource_os"]["candidate_assets"] > summary["resource_os"]["promoted_assets"]:
            adjustments.append(self._adjustment(72, "promote_resources", "Promote high-quality resource candidates; coverage gaps remain missing.", "/review/resources"))
        if summary["calibration"]["overconfidence_count"]:
            adjustments.append(self._adjustment(70, "calibrate_confidence", "Reduce overconfidence by requiring recall before reveal.", "/review/lab"))
        if not adjustments:
            adjustments.append(self._adjustment(10, "keep_current_loop", "Keep current plan and review cadence; no strong negative analytics signal.", "/review/study-planner"))
        return sorted(adjustments, key=lambda item: item["priority"], reverse=True)

    def _review_events(self, profile_id: str) -> list[LearningAnalyticsEvent]:
        events: list[LearningAnalyticsEvent] = []
        for path in (self.review_root / "lab-sessions").glob("*.json"):
            payload = self._read_json(path)
            if not payload:
                continue
            review_id = str(payload.get("review_id") or "")
            dedicated_formula_session = review_id.startswith("formula-lab-") or str(payload.get("session_id") or "").startswith("formula-session")
            units = {unit.get("unit_id"): unit for unit in payload.get("units", [])}
            for outcome in payload.get("outcomes", []):
                unit = units.get(outcome.get("unit_id"), {})
                subsystem = "formula_lab" if dedicated_formula_session and self._is_formula_unit(unit) else "review_lab"
                occurred_at = payload.get("completed_at") or payload.get("started_at") or _now()
                events.append(
                    LearningAnalyticsEvent(
                        event_id=_stable_id("evt", path.stem, outcome.get("unit_id"), len(events)),
                        profile_id=profile_id,
                        event_type="formula_unit_completed" if subsystem == "formula_lab" else "review_unit_completed",
                        occurred_at=occurred_at,
                        subsystem=subsystem,  # type: ignore[arg-type]
                        asset_id=unit.get("asset_id"),
                        topic_id=unit.get("syllabus_topic_id") or unit.get("topic_id") or unit.get("los"),
                        formula_family=unit.get("formula_family") or None,
                        outcome=outcome.get("outcome"),
                        confidence_before=self._float_or_none(outcome.get("confidence_before")),
                        confidence_after=self._float_or_none(outcome.get("confidence_after")),
                        time_spent_seconds=self._int_or_none(outcome.get("time_spent_seconds")),
                        source_refs=list(unit.get("source_refs") or []),
                        metadata={
                            "unit_type": unit.get("unit_type"),
                            "display_mode": unit.get("display_mode"),
                            "answer_quality": outcome.get("answer_quality"),
                            "needed_hint": bool(outcome.get("needed_hint")),
                            "next_action": outcome.get("next_action"),
                        },
                    )
                )
        return events

    def _language_events(self, profile_id: str) -> list[LearningAnalyticsEvent]:
        events: list[LearningAnalyticsEvent] = []
        for path in (self.language_root / "review-sessions").glob("*.json"):
            payload = self._read_json(path)
            if not payload:
                continue
            units = {unit.get("unit_id"): unit for unit in payload.get("units", [])}
            for outcome in payload.get("outcomes", []):
                unit = units.get(outcome.get("unit_id"), {})
                memory_update = outcome.get("memory_update") or {}
                events.append(
                    LearningAnalyticsEvent(
                        event_id=_stable_id("evt", path.stem, outcome.get("unit_id"), len(events)),
                        profile_id=payload.get("profile_id") or profile_id,
                        event_type="lexical_unit_completed",
                        occurred_at=outcome.get("completed_at") or payload.get("completed_at") or payload.get("started_at") or _now(),
                        subsystem="language_os",
                        lexical_id=outcome.get("lexical_id") or unit.get("lexical_id"),
                        outcome=outcome.get("outcome"),
                        time_spent_seconds=self._int_or_none(outcome.get("time_spent_seconds")),
                        source_refs=list(unit.get("source_refs") or []),
                        metadata={
                            "display_mode": unit.get("display_mode"),
                            "review_mode_group": self._language_mode_group(unit.get("display_mode")),
                            "weakness_tags": list(memory_update.get("weakness_tags") or []),
                            "mastery_state": memory_update.get("mastery_state"),
                        },
                    )
                )
        return events

    def _study_plan_events(self, profile_id: str) -> list[LearningAnalyticsEvent]:
        events: list[LearningAnalyticsEvent] = []
        for path in (self.planner_root / "plans").glob("*.json"):
            payload = self._read_json(path)
            if not payload or payload.get("profile_id", profile_id) not in {profile_id, "default"}:
                continue
            for block in payload.get("blocks", []):
                status = block.get("status")
                if status not in {"completed", "skipped", "blocked"}:
                    continue
                events.append(
                    LearningAnalyticsEvent(
                        event_id=_stable_id("evt", path.stem, block.get("block_id")),
                        profile_id=payload.get("profile_id") or profile_id,
                        event_type="study_plan_block",
                        occurred_at=payload.get("generated_at") or _now(),
                        subsystem="study_planner",
                        plan_id=payload.get("plan_id"),
                        block_id=block.get("block_id"),
                        outcome=status,
                        metadata={
                            "block_type": block.get("block_type"),
                            "target_minutes": block.get("target_minutes"),
                            "priority": block.get("priority"),
                            "blocked_reason": block.get("blocked_reason"),
                        },
                    )
                )
            if payload.get("status") == "completed":
                events.append(
                    LearningAnalyticsEvent(
                        event_id=_stable_id("evt", path.stem, "completed"),
                        profile_id=payload.get("profile_id") or profile_id,
                        event_type="study_plan_completed",
                        occurred_at=payload.get("summary", {}).get("retro", {}).get("completed_at") or payload.get("generated_at") or _now(),
                        subsystem="study_planner",
                        plan_id=payload.get("plan_id"),
                        outcome="completed",
                        metadata={"energy_mode": payload.get("energy_mode"), "available_minutes": payload.get("available_minutes")},
                    )
                )
        return events

    def _coverage_events(self, profile_id: str) -> list[LearningAnalyticsEvent]:
        events: list[LearningAnalyticsEvent] = []
        for path in (self.review_root / "syllabus").glob("coverage-*.json"):
            payload = self._read_json(path)
            if not payload:
                continue
            for record in payload.get("records", []):
                topic = record.get("topic") or {}
                events.append(
                    LearningAnalyticsEvent(
                        event_id=_stable_id("evt", path.stem, record.get("record_id")),
                        profile_id=payload.get("profile_id") or profile_id,
                        event_type="coverage_record",
                        occurred_at=_now(),
                        subsystem="coverage",
                        topic_id=record.get("topic_id"),
                        outcome=record.get("coverage_status"),
                        metadata={
                            "coverage_status": record.get("coverage_status"),
                            "coverage_score": record.get("coverage_score"),
                            "exam_weight": topic.get("exam_weight", record.get("exam_weight", 0.0)),
                            "missing_asset_types": list(record.get("missing_asset_types") or []),
                        },
                    )
                )
        return events

    def _transfer_gap_events(self, profile_id: str) -> list[LearningAnalyticsEvent]:
        events: list[LearningAnalyticsEvent] = []
        for path in (self.review_root / "mock-retro" / "transfer-gaps").glob("transfer-gap-*.json"):
            gap = self._read_json(path)
            if not gap or gap.get("profile_id", profile_id) not in {profile_id, "default"}:
                continue
            events.append(
                LearningAnalyticsEvent(
                    event_id=_stable_id("evt", path.stem),
                    profile_id=gap.get("profile_id") or profile_id,
                    event_type="transfer_gap",
                    occurred_at=gap.get("last_seen_at") or _now(),
                    subsystem="mock_retro",
                    asset_id=gap.get("asset_id"),
                    topic_id=gap.get("topic_id"),
                    formula_family=gap.get("formula_family"),
                    outcome=gap.get("status"),
                    source_refs=list(gap.get("source_refs") or []),
                    metadata={
                        "gap_type": gap.get("gap_type"),
                        "severity": gap.get("severity"),
                        "evidence_count": gap.get("evidence_count"),
                        "status": gap.get("status"),
                    },
                )
            )
        return events

    def _resource_events(self, profile_id: str) -> list[LearningAnalyticsEvent]:
        events: list[LearningAnalyticsEvent] = []
        for path in (self.review_root / "resources").glob("*.json"):
            resource = self._read_json(path)
            if not resource or resource.get("profile_id", profile_id) not in {profile_id, "default"}:
                continue
            events.append(
                LearningAnalyticsEvent(
                    event_id=_stable_id("evt", path.stem, "resource"),
                    profile_id=resource.get("profile_id") or profile_id,
                    event_type="resource_imported",
                    occurred_at=resource.get("imported_at") or _now(),
                    subsystem="resource_os",
                    source_refs=list(resource.get("source_refs") or []),
                    metadata={
                        "resource_id": resource.get("resource_id"),
                        "resource_type": resource.get("resource_type"),
                        "origin": resource.get("origin"),
                        "quality_score": resource.get("quality_score"),
                        "quality_status": resource.get("quality_status"),
                        "validation_status": resource.get("validation_status"),
                    },
                )
            )
        return events

    def _asset_events(self, profile_id: str) -> list[LearningAnalyticsEvent]:
        events: list[LearningAnalyticsEvent] = []
        for path in (self.review_root / "asset-candidates").glob("*.json"):
            asset = self._read_json(path)
            if not asset or asset.get("profile_id", profile_id) not in {profile_id, "default"}:
                continue
            subsystem = "resource_os" if asset.get("resource_id") and asset.get("resource_promoted_at") else "assets"
            events.append(
                LearningAnalyticsEvent(
                    event_id=_stable_id("evt", path.stem, "asset"),
                    profile_id=asset.get("profile_id") or profile_id,
                    event_type="resource_asset_promoted" if subsystem == "resource_os" else "asset_validation",
                    occurred_at=asset.get("resource_promoted_at") or asset.get("created_at") or _now(),
                    subsystem=subsystem,  # type: ignore[arg-type]
                    asset_id=asset.get("asset_id"),
                    topic_id=asset.get("syllabus_topic_id") or asset.get("los"),
                    formula_family=asset.get("formula_family"),
                    outcome=asset.get("validation_status"),
                    source_refs=list(asset.get("source_refs") or []),
                    metadata={
                        "asset_type": asset.get("asset_type"),
                        "validation_status": asset.get("validation_status"),
                        "resource_id": asset.get("resource_id"),
                        "resource_promoted_at": asset.get("resource_promoted_at"),
                        "resource_quality_status": asset.get("resource_quality_status"),
                        "source_quality": asset.get("source_quality"),
                    },
                )
            )
        return events

    def _file_events(self, profile_id: str) -> list[LearningAnalyticsEvent]:
        events: list[LearningAnalyticsEvent] = []
        for path in (self.review_root / "files").glob("*.json"):
            file_payload = self._read_json(path)
            if not file_payload or file_payload.get("profile_id", profile_id) not in {profile_id, "default"}:
                continue
            events.append(
                LearningAnalyticsEvent(
                    event_id=_stable_id("evt", path.stem, "file"),
                    profile_id=file_payload.get("profile_id") or profile_id,
                    event_type="file_ingestion_status",
                    occurred_at=file_payload.get("imported_at") or _now(),
                    subsystem="file_ingestion",
                    outcome=file_payload.get("extraction_status"),
                    source_refs=list(file_payload.get("source_refs") or []),
                    metadata={
                        "file_id": file_payload.get("file_id"),
                        "source_type": file_payload.get("source_type"),
                        "extraction_status": file_payload.get("extraction_status"),
                        "page_count": file_payload.get("page_count"),
                        "warnings": list(file_payload.get("warnings") or []),
                    },
                )
            )
        return events

    def _assessment_events(self, profile_id: str) -> list[LearningAnalyticsEvent]:
        try:
            from study_science.assessments import assessment_outcome
        except ImportError:
            return []
        events: list[LearningAnalyticsEvent] = []
        for path in (self.repo_root / ".system" / "memory" / "assessments" / "sessions").glob("assessment-*.json"):
            payload = self._read_json(path)
            if not payload or payload.get("profile_id", profile_id) not in {profile_id, "default"}:
                continue
            questions = {question.get("question_id"): question for question in payload.get("questions", [])}
            for response in payload.get("responses", []):
                question = questions.get(response.get("question_id"), {})
                score = self._float_or_none(response.get("score"))
                events.append(
                    LearningAnalyticsEvent(
                        event_id=_stable_id("evt", path.stem, response.get("response_id")),
                        profile_id=payload.get("profile_id") or profile_id,
                        event_type="assessment_question_answered",
                        occurred_at=response.get("created_at") or payload.get("generated_at") or _now(),
                        subsystem="assessment",
                        asset_id=(question.get("linked_asset_ids") or [None])[0],
                        topic_id=(question.get("linked_topic_ids") or [None])[0],
                        lexical_id=(question.get("linked_lexical_ids") or [None])[0],
                        formula_family=(question.get("interleaving_tags") or [None, None])[1] if question.get("category") == "formula" else None,
                        outcome=assessment_outcome(score),
                        confidence_before=self._float_or_none(response.get("confidence_before")),
                        confidence_after=self._float_or_none(response.get("confidence_after")),
                        time_spent_seconds=self._int_or_none(response.get("time_spent_seconds")),
                        source_refs=[f"assessment:{payload.get('assessment_id')}:{response.get('question_id')}", *list(question.get("source_refs") or [])],
                        metadata={
                            "assessment_id": payload.get("assessment_id"),
                            "mode": payload.get("mode"),
                            "question_type": question.get("question_type"),
                            "category": question.get("category"),
                            "score": score,
                            "is_correct": response.get("is_correct"),
                        },
                    )
                )
            if payload.get("status") == "completed":
                events.append(
                    LearningAnalyticsEvent(
                        event_id=_stable_id("evt", path.stem, "completed"),
                        profile_id=payload.get("profile_id") or profile_id,
                        event_type="assessment_completed",
                        occurred_at=payload.get("summary", {}).get("completed_at") or payload.get("generated_at") or _now(),
                        subsystem="assessment",
                        outcome="completed",
                        metadata={
                            "assessment_id": payload.get("assessment_id"),
                            "mode": payload.get("mode"),
                            "score": payload.get("summary", {}).get("score"),
                            "transfer_gaps_created": payload.get("summary", {}).get("transfer_gaps_created"),
                        },
                    )
                )
        return events

    def _calibration_record(
        self,
        profile_id: str,
        scope_type: str,
        scope_id: str,
        events: list[dict[str, Any]],
        gap_events: list[dict[str, Any]],
    ) -> MasteryCalibrationRecord:
        outcomes = [event.get("outcome") for event in events]
        successes = [_success_value(outcome) for outcome in outcomes]
        numeric_successes = [value for value in successes if value is not None]
        before = [float(event["confidence_before"]) for event in events if event.get("confidence_before") is not None]
        after = [float(event["confidence_after"]) for event in events if event.get("confidence_after") is not None]
        avg_before = round(sum(before) / len(before), 4) if before else None
        avg_after = round(sum(after) / len(after), 4) if after else None
        success_rate = sum(numeric_successes) / len(numeric_successes) if numeric_successes else None
        calibration_error = round(abs((avg_before / 4) - success_rate), 4) if avg_before is not None and success_rate is not None else None
        overconfidence = sum(
            1 for event in events
            if event.get("confidence_before") is not None
            and float(event.get("confidence_before") or 0) >= 3
            and event.get("outcome") in {"forgot", "skipped", "partial"}
        )
        underconfidence = sum(
            1 for event in events
            if event.get("confidence_before") is not None
            and float(event.get("confidence_before") or 0) <= 1
            and event.get("outcome") == "recalled"
        )
        if scope_type == "global":
            overconfidence += sum(1 for event in gap_events if float(event.get("metadata", {}).get("severity", 0.0) or 0.0) >= 0.7)
        return MasteryCalibrationRecord(
            record_id=_stable_id("cal", profile_id, scope_type, scope_id),
            profile_id=profile_id,
            scope_type=scope_type,  # type: ignore[arg-type]
            scope_id=scope_id,
            recall_attempts=len(events),
            recalled_count=outcomes.count("recalled"),
            partial_count=outcomes.count("partial"),
            forgot_count=outcomes.count("forgot"),
            skipped_count=outcomes.count("skipped"),
            average_confidence_before=avg_before,
            average_confidence_after=avg_after,
            calibration_error=calibration_error,
            overconfidence_count=overconfidence,
            underconfidence_count=underconfidence,
            transfer_gap_count=len(gap_events) if scope_type == "global" else 0,
            mastery_trend=self._trend(events),
            last_updated_at=max([event.get("occurred_at") or "" for event in events + gap_events], default=_now()),
        )

    def _review_summary(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        review_events = [event for event in events if event.get("subsystem") == "review_lab"]
        return {
            "attempts": len(review_events),
            "recall_success_rate": self._success_rate(review_events),
            "average_time_spent_seconds": self._avg([event.get("time_spent_seconds") for event in review_events]),
            "recalled": sum(1 for event in review_events if event.get("outcome") == "recalled"),
            "partial": sum(1 for event in review_events if event.get("outcome") == "partial"),
            "forgot": sum(1 for event in review_events if event.get("outcome") == "forgot"),
            "skipped": sum(1 for event in review_events if event.get("outcome") == "skipped"),
        }

    def _mock_summary(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        gap_events = [event for event in events if event.get("subsystem") == "mock_retro"]
        gap_counts = Counter(event.get("metadata", {}).get("gap_type", "unknown") for event in gap_events)
        return {
            "open_transfer_gap_count": sum(1 for event in gap_events if event.get("outcome") == "open"),
            "transfer_gap_count": len(gap_events),
            "highest_severity": max([float(event.get("metadata", {}).get("severity", 0.0) or 0.0) for event in gap_events], default=0.0),
            "top_gap_types": [{"gap_type": key, "count": value} for key, value in gap_counts.most_common(5)],
        }

    def _file_summary(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        file_events = [event for event in events if event.get("subsystem") == "file_ingestion"]
        statuses = Counter(event.get("outcome", "unknown") for event in file_events)
        return {
            "file_count": len(file_events),
            "extracted": statuses.get("extracted", 0),
            "extracted_no_text": statuses.get("extracted_no_text", 0),
            "failed": statuses.get("failed", 0),
            "unsupported": statuses.get("unsupported", 0),
            "duplicate": statuses.get("duplicate", 0),
        }

    def _write_projection(self, profile_id: str, events: list[dict[str, Any]], summary: dict[str, Any]) -> None:
        (self.analytics_root / f"events-{profile_id or 'default'}.json").write_text(
            json.dumps({"events": events}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (self.analytics_root / f"summary-{profile_id or 'default'}.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _is_formula_unit(unit: dict[str, Any]) -> bool:
        return bool(
            unit.get("formula_family")
            or unit.get("unit_type") == "formula_lab"
            or unit.get("asset_type") == "formula"
            or str(unit.get("display_mode", "")).startswith(("recall_formula", "ba_ii", "derive_formula"))
        )

    @staticmethod
    def _language_mode_group(display_mode: Any) -> str:
        if str(display_mode) in {"sentence_production", "collocation_check", "morphology_check"}:
            return "production"
        return "recognition"

    @staticmethod
    def _filter_range(events: list[LearningAnalyticsEvent], range_key: str) -> list[LearningAnalyticsEvent]:
        start = _range_start(range_key)
        if start is None:
            return events
        filtered = []
        for event in events:
            occurred = _parse_time(event.occurred_at)
            if occurred is None or occurred >= start:
                filtered.append(event)
        return filtered

    @staticmethod
    def _success_rate(events: list[dict[str, Any]]) -> float:
        values = [_success_value(event.get("outcome")) for event in events]
        values = [value for value in values if value is not None]
        return round(sum(values) / len(values), 4) if values else 0.0

    @staticmethod
    def _success_by_key(events: list[dict[str, Any]], key: str) -> dict[str, Any]:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for event in events:
            groups[str(event.get(key) or "unknown")].append(event)
        return {
            group_key: {"attempts": len(group_events), "success_rate": LearningAnalyticsService._success_rate(group_events)}
            for group_key, group_events in groups.items()
        }

    @staticmethod
    def _trend(events: list[dict[str, Any]]) -> Literal["improving", "stable", "declining", "unknown"]:
        scored = [event for event in sorted(events, key=lambda item: item.get("occurred_at", "")) if _success_value(event.get("outcome")) is not None]
        if len(scored) < 3:
            return "unknown"
        midpoint = max(1, len(scored) // 2)
        old = [_success_value(event.get("outcome")) or 0.0 for event in scored[:midpoint]]
        recent = [_success_value(event.get("outcome")) or 0.0 for event in scored[midpoint:]]
        delta = (sum(recent) / len(recent)) - (sum(old) / len(old))
        if delta > 0.15:
            return "improving"
        if delta < -0.15:
            return "declining"
        return "stable"

    @staticmethod
    def _high_value_completion_rate(events: list[dict[str, Any]]) -> float:
        high_value = [event for event in events if float(event.get("metadata", {}).get("priority", 0.0) or 0.0) >= 50]
        if not high_value:
            return 0.0
        return round(sum(1 for event in high_value if event.get("outcome") == "completed") / len(high_value), 4)

    @staticmethod
    def _adjustment(priority: int, action_id: str, title: str, href: str) -> dict[str, Any]:
        return {"priority": priority, "action_id": action_id, "title": title, "href": href}

    @staticmethod
    def _avg(values: list[Any]) -> float:
        numbers = [float(value) for value in values if value is not None]
        return round(sum(numbers) / len(numbers), 4) if numbers else 0.0

    @staticmethod
    def _float_or_none(value: Any) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _int_or_none(value: Any) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}


def strip_wrong_fields(payload: Any) -> Any:
    sanitized, _ = sanitize_payload(payload)
    return sanitized
