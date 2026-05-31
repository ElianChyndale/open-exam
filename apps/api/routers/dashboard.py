"""GET /api/dashboard/effectiveness — Learning effectiveness dashboard."""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query

from deps import get_repo
from schemas import EffectivenessResponse

router = APIRouter()


@router.get("/effectiveness", response_model=EffectivenessResponse)
async def get_effectiveness_dashboard(
    days: int = Query(default=30, ge=7, le=365),
    repo=Depends(get_repo),
):
    """Generate the learning effectiveness dashboard.

    Metrics per PLAN.md:
    - Due review completion rate
    - High-confidence error count
    - Interleaving accuracy
    - Same-error recurrence rate
    - LOS risk heatmap
    - Predicted pass probability
    """
    from app.workflows import (
        collect_due_card_items,
        collect_pattern_items,
    )
    from study_science.calibration import ConfidenceCalibration, CalibrationRecord

    today = date.today()
    period_start = (today - timedelta(days=days)).isoformat()
    period_end = today.isoformat()

    events = repo.load_events()
    question_events = [e for e in events if e.source_layer == "question"]

    # Filter to period
    recent_events = [
        e for e in question_events
        if e.created_at[:10] >= period_start[:10]
    ]

    # Due review completion rate
    due_items = collect_due_card_items(repo, today)
    total_due = len(due_items)
    # Count completed reviews from progress events
    from app.workflows import load_progress_events

    progress = load_progress_events(repo)
    completed_reviews = sum(
        1 for p in progress
        if p.get("record_type") == "daily_review_completed"
        and p.get("status") in {"completed", "done"}
        and p.get("date", "")[:10] >= period_start[:10]
    )
    completion_rate = (completed_reviews / max(days, 1)) if days > 0 else 0.0

    # High-confidence error count
    calibration_records: list[CalibrationRecord] = []
    high_conf_errors = 0
    for e in recent_events:
        state = ConfidenceCalibration.classify(e.confidence, is_correct=False)
        record = CalibrationRecord(
            attempt_id=e.event_id or "",
            topic=e.topic,
            los=e.los,
            confidence=e.confidence,
            is_correct=False,
            state=state,
            created_at=e.created_at,
        )
        calibration_records.append(record)
        if ConfidenceCalibration.is_dangerous(e.confidence, is_correct=False):
            high_conf_errors += 1

    # Calibration summary
    cal_summary = ConfidenceCalibration.summarize(calibration_records)

    # Same-error recurrence rate
    pattern_items = collect_pattern_items(repo)
    total_patterns = len(pattern_items)
    recurrence_rate = total_patterns / max(len(recent_events), 1) if recent_events else 0.0

    # LOS risk heatmap
    los_errors: dict[str, int] = Counter()
    for e in recent_events:
        key = f"{e.topic}/{e.los}"
        los_errors[key] += 1

    max_errors = max(los_errors.values()) if los_errors else 1
    heatmap = {
        los: count / max_errors
        for los, count in los_errors.most_common(20)
    }

    # Top 3 danger LOS
    danger_top_3 = [
        f"{los} ({count} errors)"
        for los, count in los_errors.most_common(3)
    ]

    # Interleaving accuracy (approximation: accuracy on non-primary-topic items)
    topic_counts = Counter(e.topic for e in recent_events)
    primary_topic = topic_counts.most_common(1)[0][0] if topic_counts else ""
    non_primary = [e for e in recent_events if e.topic != primary_topic]
    interleaving_acc = 0.0  # We don't have is_correct in MistakeEvent ATM

    # Predicted pass probability (heuristic)
    # Formula: base_rate + calibration_penalty + completion_bonus + pattern_penalty
    base_rate = 0.65
    calibration_penalty = min(0.20, cal_summary.calibration_error_rate * 0.5)
    completion_bonus = min(0.15, completion_rate * 0.15)
    pattern_penalty = min(0.10, recurrence_rate * 0.3)

    pass_prob = base_rate - calibration_penalty + completion_bonus - pattern_penalty
    pass_prob = max(0.20, min(0.95, pass_prob))

    # Error count trend (daily buckets)
    daily_counts: dict[str, int] = Counter()
    for e in recent_events:
        daily_counts[e.created_at[:10]] += 1

    sorted_dates = sorted(daily_counts.keys())
    error_trend = [daily_counts[d] for d in sorted_dates[-30:]]

    return EffectivenessResponse(
        report_id=f"eff-{today.isoformat()}",
        period_start=period_start,
        period_end=period_end,
        due_review_completion_rate=round(completion_rate, 3),
        high_confidence_error_count=high_conf_errors,
        interleaving_accuracy=round(interleaving_acc, 3),
        same_error_recurrence_rate=round(recurrence_rate, 3),
        los_risk_heatmap=heatmap,
        danger_top_3=danger_top_3,
        predicted_pass_probability=round(pass_prob, 3),
        confidence_band_low=round(max(0.10, pass_prob - 0.10), 3),
        confidence_band_high=round(min(0.99, pass_prob + 0.10), 3),
        calibration_trend=cal_summary.trend,
        error_count_trend=error_trend if error_trend else [0],
    )


@router.get("/summary")
async def get_summary(repo=Depends(get_repo)):
    """Get a quick summary of the learner's current state."""
    from collections import Counter

    events = repo.load_events()
    question_events = [e for e in events if e.source_layer == "question"]

    total_questions = len(question_events)
    topic_counts = Counter(e.topic for e in question_events)
    error_counts = Counter(e.error_type for e in question_events)

    # Due items
    from app.workflows import collect_due_card_items
    due = collect_due_card_items(repo, date.today())

    # Patterns
    from app.workflows import collect_pattern_items
    patterns = collect_pattern_items(repo)

    return {
        "total_events": len(events),
        "total_questions_recorded": total_questions,
        "total_bias_events": sum(1 for e in events if e.source_layer == "bias"),
        "total_agent_failures": sum(1 for e in events if e.source_layer == "agent"),
        "top_topics": [
            {"topic": t, "count": c}
            for t, c in topic_counts.most_common(5)
        ],
        "top_error_types": [
            {"type": t, "count": c}
            for t, c in error_counts.most_common(5)
        ],
        "due_review_items": len(due),
        "active_patterns": len(patterns),
    }


@router.get("/calibration-warnings")
async def get_calibration_warnings(repo=Depends(get_repo)):
    """Get recent calibration warnings for the dashboard."""
    import json
    warning_path = repo.memory_root / "strategy" / "calibration-warnings.jsonl"
    if not warning_path.exists():
        return {"warnings": []}

    warnings = []
    for line in warning_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            warnings.append(json.loads(line))
    return {"warnings": warnings[-10:]}


@router.get("/streaks")
async def get_streaks(repo=Depends(get_repo)):
    """Get learning streak and weekly goal progress."""
    from app.streaks import compute_streak, compute_weekly_goal_progress, load_progress_dates
    from app.workflows import load_progress_events

    progress_path = repo.memory_root / "progress" / "progress-events.jsonl"
    active_dates = load_progress_dates(progress_path)
    streak, active_today = compute_streak(active_dates)
    progress_events = load_progress_events(repo)
    weekly = compute_weekly_goal_progress(progress_events)

    return {
        "current_streak": streak,
        "active_today": active_today,
        "longest_streak": streak,  # simplified: tracks current as longest
        "weekly_goal": weekly,
    }


@router.get("/calendar")
async def get_calendar_data(
    month: str = "",
    repo=Depends(get_repo),
):
    """Get calendar data: error counts per day, review completion, exam date."""
    from collections import Counter
    from app.workflows import load_progress_events

    events = repo.load_events()
    question_events = [e for e in events if e.source_layer == "question"]

    daily_errors: dict[str, int] = Counter()
    for e in question_events:
        day = e.created_at[:7] if month else e.created_at[:10]
        daily_errors[day] += 1

    progress = load_progress_events(repo)
    review_days = set()
    for p in progress:
        if p.get("record_type") == "daily_review_completed" and p.get("status") in {"completed", "done"}:
            d = str(p.get("date") or p.get("created_at", "")[:10])
            if d:
                review_days.add(d)

    from datetime import date
    exam_date_str = ""
    countdown_days = 0
    exam_setting_path = repo.root / ".system" / "exam_date.txt"
    if exam_setting_path.exists():
        exam_date_str = exam_setting_path.read_text(encoding="utf-8").strip()
        try:
            exam = date.fromisoformat(exam_date_str[:10])
            remaining = (exam - date.today()).days
            countdown_days = max(0, remaining)
        except ValueError:
            pass

    return {
        "daily_errors": dict(daily_errors.most_common(90)),
        "review_days": sorted(review_days),
        "exam_date": exam_date_str,
        "countdown_days": countdown_days,
    }
