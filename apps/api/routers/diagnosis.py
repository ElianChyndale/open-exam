"""POST /api/diagnose — Error diagnosis engine.

Generates root cause, fix rule, next drill, linked LOS, MOC node,
pattern detection, and spacing schedule for each mistake.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from deps import get_repo
from schemas import DiagnosisRequest, DiagnosisResponse

router = APIRouter()


@router.post("", response_model=DiagnosisResponse)
async def diagnose_error(req: DiagnosisRequest, repo=Depends(get_repo)):
    """Diagnose an error and return structured remediation.

    Uses the 8-category error taxonomy from PLAN.md:
    knowledge_gap, concept_confusion, formula_misuse,
    careless_reading, time_pressure, confidence_calibration_failure,
    fatigue_energy_mismatch, agent_failure.
    """
    from app.workflows import (
        default_fix_rule,
        mine_patterns,
        next_drill_for,
        update_knowledge_from_diagnosis,
    )
    from study_science.spacing import SpacingInput, SpacingScheduler
    from study_science.calibration import ConfidenceCalibration

    # Find the source event
    events = repo.load_events()
    events_by_id = {event.event_id: event for event in events}
    event = events_by_id.get(req.attempt_id)
    if event is None:
        attempt = next(
            (
                candidate
                for candidate in repo.load_attempt_records()
                if candidate.get("attempt_id") == req.attempt_id
            ),
            None,
        )
        if attempt:
            event = events_by_id.get(attempt.get("mistake_event_id"))
            if event is None:
                event = next(
                    (
                        candidate
                        for candidate in events
                        if candidate.topic == attempt.get("topic")
                        and candidate.los == attempt.get("los")
                        and candidate.prompt_or_question == attempt.get("prompt_or_question")
                        and candidate.wrong_choice_or_output == attempt.get("wrong_choice_or_output")
                    ),
                    None,
                )

    if not event:
        # Create a diagnosis from provided info
        fix_rule = default_fix_rule(req.error_type)
        next_drill = "24 小时内重做 2 道同类题。"
        return DiagnosisResponse(
            diagnosis_id=f"dx-{req.attempt_id[:12]}",
            attempt_id=req.attempt_id,
            error_category=req.error_type or "concept_confusion",
            error_summary="待详细诊断",
            fix_rule=fix_rule,
            next_drill=next_drill,
            linked_los=[],
            linked_moc_node="",
            review_due_at="",
            pattern_candidate=False,
            pattern_key="",
            spacing_interval_days=1,
        )

    # Spacing calculation
    spacing_input = SpacingInput(
        topic=event.topic,
        los=event.los,
        error_type=event.error_type,
        confidence=event.confidence,
        is_correct=False,
        time_spent_seconds=event.time_spent,
    )
    spacing = SpacingScheduler.schedule(spacing_input)

    # Calibration check
    is_calibration_danger = ConfidenceCalibration.is_dangerous(
        event.confidence, is_correct=False
    )

    # Pattern detection
    mine_patterns(repo)
    pattern_candidate = False
    pattern_key = f"{event.topic}::{event.los}::{event.error_type}"
    pattern_dir = repo.memory_root / "patterns"
    for pattern_path in pattern_dir.glob("*.md"):
        text = pattern_path.read_text(encoding="utf-8")
        if pattern_key in text:
            pattern_candidate = True
            break

    fix_rule = default_fix_rule(event.error_type)
    next_drill = next_drill_for(event)

    # If calibration danger, prepend warning to fix rule
    if is_calibration_danger:
        fix_rule = f"⚠️ 高信心错误（校准失败）—— {fix_rule}"

    # ── Feed diagnosis into KnowledgeMemoryEngine ──────────────────────────────
    # This creates/updates a knowledge point so the next Daily Review pack
    # will include a review item for this (topic, LOS, error_type).
    update_knowledge_from_diagnosis(
        repo,
        error_type=event.error_type,
        topic=event.topic,
        los=event.los,
        confidence=event.confidence,
        attempt_id=req.attempt_id,
    )

    return DiagnosisResponse(
        diagnosis_id=f"dx-{event.event_id or req.attempt_id}",
        attempt_id=req.attempt_id,
        error_category=event.error_type,
        error_summary=f"{event.topic} / {event.los}: {event.error_type}",
        fix_rule=fix_rule,
        next_drill=next_drill,
        linked_los=[event.los],
        linked_moc_node=event.moc_target or "",
        review_due_at=spacing.next_review_date,
        pattern_candidate=pattern_candidate,
        pattern_key=pattern_key,
        spacing_interval_days=spacing.interval_days,
    )


@router.get("/patterns")
async def list_patterns(repo=Depends(get_repo)):
    """List all detected error patterns."""
    from app.workflows import mine_patterns

    mine_patterns(repo)
    patterns_dir = repo.memory_root / "patterns"
    patterns = []
    for path in sorted(patterns_dir.glob("*.md")):
        from app.workflows import parse_frontmatter

        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        patterns.append({
            "pattern_id": fm.get("pattern_id", path.stem),
            "pattern_key": fm.get("pattern_key", ""),
            "recurrence": int(fm.get("recurrence", "0")),
            "severity": fm.get("severity", "medium"),
        })

    return {"count": len(patterns), "patterns": patterns}
