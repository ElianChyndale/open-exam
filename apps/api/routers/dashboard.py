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

    # Predicted pass probability (multi-factor model)
    from study_science.prediction import PassPredictor, PredictionInput

    pred_input = PredictionInput(
        total_events=len(question_events),
        topics_attempted=len(topic_counts),
        total_topics=10,
        high_conf_errors=high_conf_errors,
        pattern_recurrence_rate=recurrence_rate,
        review_completion_rate=completion_rate,
        calibration_error_rate=cal_summary.calibration_error_rate,
        calibration_trend=cal_summary.trend,
        mock_score=None,
        days_until_exam=365,
    )

    # Check for exam date
    exam_setting_path = repo.root / ".system" / "exam_date.txt"
    if exam_setting_path.exists():
        try:
            exam_date = date.fromisoformat(exam_setting_path.read_text(encoding="utf-8").strip()[:10])
            remaining = (exam_date - today).days
            pred_input.days_until_exam = max(1, remaining)
        except (ValueError, OSError):
            pass

    prediction = PassPredictor.predict(pred_input)

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
        predicted_pass_probability=prediction.pass_probability,
        confidence_band_low=prediction.confidence_band_low,
        confidence_band_high=prediction.confidence_band_high,
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


@router.post("/what-if")
async def what_if_simulation(adjustments: dict, repo=Depends(get_repo)):
    """Run a 'what if' simulation on pass probability."""
    from study_science.prediction import PassPredictor, PredictionInput
    from collections import Counter

    events = repo.load_events()
    question_events = [e for e in events if e.source_layer == "question"]

    from app.workflows import (
        collect_pattern_items,
        collect_due_card_items,
        load_progress_events,
    )
    from study_science.calibration import ConfidenceCalibration, CalibrationRecord

    topic_counts = Counter(e.topic for e in question_events)
    recent_events = question_events

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

    cal_summary = ConfidenceCalibration.summarize(calibration_records)
    pattern_items = collect_pattern_items(repo)
    recurrence_rate = len(pattern_items) / max(len(recent_events), 1)
    due_items = collect_due_card_items(repo, date.today())
    progress = load_progress_events(repo)
    completed_reviews = sum(
        1 for p in progress
        if p.get("record_type") == "daily_review_completed"
        and p.get("status") in {"completed", "done"}
    )
    completion_rate = completed_reviews / max(len(due_items), 1)

    input_ = PredictionInput(
        total_events=len(question_events),
        topics_attempted=len(topic_counts),
        total_topics=10,
        high_conf_errors=high_conf_errors,
        pattern_recurrence_rate=recurrence_rate,
        review_completion_rate=completion_rate,
        calibration_error_rate=cal_summary.calibration_error_rate,
        calibration_trend=cal_summary.trend,
    )

    result = PassPredictor.what_if(input_, adjustments)
    return {
        "pass_probability": result.pass_probability,
        "factors": result.factors,
        "top_actions": result.top_actions,
    }


@router.get("/weekly-trend")
async def get_weekly_trend(repo=Depends(get_repo)):
    """Get week-over-week trend comparison."""
    from collections import Counter, defaultdict
    from datetime import date, timedelta

    today = date.today()
    this_week_start = today - timedelta(days=today.weekday())
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_start - timedelta(days=1)

    events = repo.load_events()
    question_events = [e for e in events if e.source_layer == "question"]

    this_week = [e for e in question_events if this_week_start.isoformat() <= e.created_at[:10] <= today.isoformat()]
    last_week = [e for e in question_events if last_week_start.isoformat() <= e.created_at[:10] <= last_week_end.isoformat()]

    this_errors = len(this_week)
    last_errors = len(last_week)
    error_change = ((this_errors - last_errors) / max(last_errors, 1)) * 100

    this_high_conf = sum(1 for e in this_week if e.confidence >= 3 and not e.is_correct)
    last_high_conf = sum(1 for e in last_week if e.confidence >= 3 and not e.is_correct)
    high_conf_change = ((this_high_conf - last_high_conf) / max(last_high_conf, 1)) * 100

    this_topics = len(set(e.topic for e in this_week))
    last_topics = len(set(e.topic for e in last_week))

    from app.workflows import load_progress_events
    progress = load_progress_events(repo)
    this_reviews = sum(1 for p in progress if p.get("record_type") == "daily_review_completed"
                       and p.get("status") in {"completed", "done"}
                       and this_week_start.isoformat() <= str(p.get("date") or p.get("created_at", "")[:10]) <= today.isoformat())
    last_reviews = sum(1 for p in progress if p.get("record_type") == "daily_review_completed"
                       and p.get("status") in {"completed", "done"}
                       and last_week_start.isoformat() <= str(p.get("date") or p.get("created_at", "")[:10]) <= last_week_end.isoformat())

    def trend(current: float, previous: float, lower_is_better: bool = True) -> str:
        if previous == 0 and current == 0:
            return "stable"
        if previous == 0:
            return "worsening" if current > 0 and lower_is_better else "improving"
        ratio = (current - previous) / previous
        if lower_is_better:
            return "improving" if ratio < -0.1 else "worsening" if ratio > 0.1 else "stable"
        return "improving" if ratio > 0.1 else "worsening" if ratio < -0.1 else "stable"

    return {
        "this_week": {"start": this_week_start.isoformat(), "end": today.isoformat()},
        "last_week": {"start": last_week_start.isoformat(), "end": last_week_end.isoformat()},
        "errors": {"current": this_errors, "previous": last_errors, "change_pct": round(error_change, 1), "trend": trend(this_errors, last_errors)},
        "high_confidence_errors": {"current": this_high_conf, "previous": last_high_conf, "change_pct": round(high_conf_change, 1), "trend": trend(this_high_conf, last_high_conf)},
        "topics_covered": {"current": this_topics, "previous": last_topics, "trend": trend(this_topics, last_topics, lower_is_better=False)},
        "reviews_completed": {"current": this_reviews, "previous": last_reviews, "trend": trend(this_reviews, last_reviews, lower_is_better=False)},
    }


@router.get("/mastery")
async def get_topic_mastery(repo=Depends(get_repo)):
    """Get topic-level mastery scores for radar chart."""
    from collections import Counter, defaultdict
    from app.workflows import collect_due_card_items

    events = repo.load_events()
    question_events = [e for e in events if e.source_layer == "question"]

    SUBJECTS = [
        "Quantitative Methods", "Economics", "Financial Statement Analysis",
        "Corporate Issuers", "Equity", "Fixed Income", "Derivatives",
        "Alternative Investments", "Portfolio Management", "Ethical and Professional Standards",
    ]

    topic_events: dict[str, list] = defaultdict(list)
    for e in question_events:
        topic_events[e.topic].append(e)

    topic_los_attempted: dict[str, set] = defaultdict(set)
    los_recurrence: dict[str, Counter] = defaultdict(Counter)
    for e in question_events:
        topic_los_attempted[e.topic].add(e.los)
        key = f"{e.los}::{e.error_type}"
        los_recurrence[e.topic][key] += 1

    from datetime import date
    exam_date_str = ""
    exam_setting_path = repo.root / ".system" / "exam_date.txt"
    if exam_setting_path.exists():
        exam_date_str = exam_setting_path.read_text(encoding="utf-8").strip()[:10]

    topics = []
    for subject in SUBJECTS:
        t_events = topic_events.get(subject, [])
        if not t_events:
            topics.append({"topic": subject, "mastery": 0, "errors": 0, "status": "no_data"})
            continue

        los_count = len(topic_los_attempted.get(subject, set()))
        error_density = len(t_events) / max(los_count, 1)
        density_score = max(0, 1 - error_density / 5)

        recurrences = [c for c in los_recurrence.get(subject, {}).values() if c >= 2]
        recurrence_score = max(0, 1 - len(recurrences) / max(los_count, 1))

        high_conf_wrong = sum(1 for e in t_events if e.confidence >= 3 and not e.is_correct)
        cal_score = max(0, 1 - high_conf_wrong / max(len(t_events), 1) * 2)

        mastery = int((density_score * 0.35 + recurrence_score * 0.35 + cal_score * 0.30) * 100)
        status = "critical" if mastery < 30 else "needs_work" if mastery < 60 else "ready"

        topics.append({
            "topic": subject,
            "mastery": mastery,
            "errors": len(t_events),
            "status": status,
            "error_density": round(error_density, 2),
            "recurrence_count": len(recurrences),
            "high_conf_errors": high_conf_wrong,
        })

    overall = int(sum(t["mastery"] for t in topics) / len(topics)) if topics else 0

    return {
        "topics": topics,
        "overall_mastery": overall,
        "exam_date": exam_date_str,
    }
