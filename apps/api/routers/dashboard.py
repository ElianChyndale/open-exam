"""GET /api/dashboard/effectiveness — Learning effectiveness dashboard."""

from __future__ import annotations

import json
from collections import Counter
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query

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

    question_events = repo.load_incorrect_question_events()
    attempts = repo.load_attempt_records()

    # Filter to period
    recent_events = [
        e for e in question_events
        if e.created_at[:10] >= period_start[:10]
    ]
    recent_attempts = [
        attempt for attempt in attempts
        if str(attempt.get("created_at", ""))[:10] >= period_start[:10]
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
    completion_rate = min(1.0, completed_reviews / max(total_due, 1))

    # High-confidence error count
    calibration_records: list[CalibrationRecord] = []
    high_conf_errors = 0
    for attempt in recent_attempts:
        confidence = int(attempt.get("confidence", 0) or 0)
        is_correct = bool(attempt.get("is_correct", False))
        state = ConfidenceCalibration.classify(confidence, is_correct=is_correct)
        record = CalibrationRecord(
            attempt_id=str(attempt.get("attempt_id", "")),
            topic=str(attempt.get("topic", "")),
            los=str(attempt.get("los", "")),
            confidence=confidence,
            is_correct=is_correct,
            state=state,
            created_at=str(attempt.get("created_at", "")),
        )
        calibration_records.append(record)
        if ConfidenceCalibration.is_dangerous(confidence, is_correct=is_correct):
            high_conf_errors += 1

    # Calibration summary
    cal_summary = ConfidenceCalibration.summarize(calibration_records)

    # Same-error recurrence rate
    pattern_items = collect_pattern_items(repo)
    total_patterns = len(pattern_items)
    recurrence_rate = total_patterns / max(len(recent_events), 1) if recent_events else 0.0

    # LOS risk heatmap (normalized through profile aliases)
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
    topic_counts = Counter(str(attempt.get("topic", "")) for attempt in recent_attempts)
    primary_topic = topic_counts.most_common(1)[0][0] if topic_counts else ""
    non_primary = [attempt for attempt in recent_attempts if attempt.get("topic", "") != primary_topic]
    interleaving_acc = (
        sum(1 for attempt in non_primary if attempt.get("is_correct")) / len(non_primary)
        if non_primary else 0.0
    )

    # Predicted pass probability (multi-factor model)
    from study_science.prediction import PassPredictor, PredictionInput
    from app.exam_profile import get_profile

    profile = get_profile(repo.root)
    pred_input = PredictionInput(
        total_events=len(attempts),
        topics_attempted=len(topic_counts),
        total_topics=len(profile.subjects),
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
    question_events = repo.load_incorrect_question_events()
    attempts = repo.load_attempt_records()

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
        "total_attempts": len(attempts),
        "accuracy": round(
            sum(1 for attempt in attempts if attempt.get("is_correct")) / len(attempts),
            3,
        ) if attempts else 0.0,
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
        "recovery": {
            "needed": not active_today,
            "recommended_action": "完成一个 10 分钟 Daily Review 恢复节奏" if not active_today else "保持当前节奏",
        },
    }


@router.get("/calendar")
async def get_calendar_data(
    month: str = "",
    repo=Depends(get_repo),
):
    """Get calendar data: error counts per day, review completion, exam date."""
    from collections import Counter
    from app.workflows import load_progress_events

    question_events = repo.load_incorrect_question_events()

    daily_errors: dict[str, int] = Counter()
    for e in question_events:
        day = e.created_at[:10]
        if month and not day.startswith(month):
            continue
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


@router.put("/calendar/settings")
async def update_calendar_settings(payload: dict, repo=Depends(get_repo)):
    """Persist learner calendar settings used by spacing and countdown views."""
    exam_date = str(payload.get("exam_date", "")).strip()
    if exam_date:
        try:
            date.fromisoformat(exam_date[:10])
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="exam_date must use YYYY-MM-DD") from exc
    path = repo.root / ".system" / "exam_date.txt"
    path.write_text(exam_date[:10], encoding="utf-8")
    return {"exam_date": exam_date[:10]}


@router.post("/what-if")
async def what_if_simulation(adjustments: dict, repo=Depends(get_repo)):
    """Run a 'what if' simulation on pass probability."""
    from study_science.prediction import PassPredictor, PredictionInput
    from collections import Counter
    from app.exam_profile import get_profile

    question_events = repo.load_incorrect_question_events()
    attempts = repo.load_attempt_records()

    from app.workflows import (
        collect_pattern_items,
        collect_due_card_items,
        load_progress_events,
    )
    from study_science.calibration import ConfidenceCalibration, CalibrationRecord

    topic_counts = Counter(str(attempt.get("topic", "")) for attempt in attempts)
    recent_events = question_events

    calibration_records: list[CalibrationRecord] = []
    high_conf_errors = 0
    for attempt in attempts:
        confidence = int(attempt.get("confidence", 0) or 0)
        is_correct = bool(attempt.get("is_correct", False))
        state = ConfidenceCalibration.classify(confidence, is_correct=is_correct)
        record = CalibrationRecord(
            attempt_id=str(attempt.get("attempt_id", "")),
            topic=str(attempt.get("topic", "")),
            los=str(attempt.get("los", "")),
            confidence=confidence,
            is_correct=is_correct,
            state=state,
            created_at=str(attempt.get("created_at", "")),
        )
        calibration_records.append(record)
        if ConfidenceCalibration.is_dangerous(confidence, is_correct=is_correct):
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
        total_events=len(attempts),
        topics_attempted=len(topic_counts),
        total_topics=len(get_profile(repo.root).subjects),
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
    from datetime import date, timedelta

    today = date.today()
    this_week_start = today - timedelta(days=today.weekday())
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_start - timedelta(days=1)

    question_events = repo.load_incorrect_question_events()

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

    question_events = repo.load_incorrect_question_events()

    from app.exam_profile import get_profile
    profile = get_profile(repo.root)
    subjects = [subject["name"] for subject in profile.subjects]

    # Normalize event topics through profile aliases
    topic_events: dict[str, list] = defaultdict(list)
    for e in question_events:
        normalized = profile.normalize_subject(e.topic)
        topic_events[normalized].append(e)

    topic_los_attempted: dict[str, set] = defaultdict(set)
    los_recurrence: dict[str, Counter] = defaultdict(Counter)
    for e in question_events:
        normalized = profile.normalize_subject(e.topic)
        topic_los_attempted[normalized].add(e.los)
        key = f"{e.los}::{e.error_type}"
        los_recurrence[normalized][key] += 1

    exam_date_str = ""
    exam_setting_path = repo.root / ".system" / "exam_date.txt"
    if exam_setting_path.exists():
        exam_date_str = exam_setting_path.read_text(encoding="utf-8").strip()[:10]

    topics = []
    for subject in subjects:
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


@router.get("/knowledge-readiness")
async def get_knowledge_readiness(repo=Depends(get_repo)):
    """Knowledge point memory states with decay status and next-review schedule.

    Returns every knowledge point with its graduated state (Reviewed once →
    Familiar → Practiced → Proficient → Mastered), decay risk, and when it
    should next be reviewed.  This is the ecological feedback from the
    KnowledgeMemoryEngine — answering "what does the system know about what I know?"
    """
    from study_science.knowledge_memory import KnowledgeMemoryEngine

    overlay_path = repo.memory_root / "review" / "knowledge-status.json"
    if not overlay_path.exists():
        return {"knowledge_points": [], "decayed": [], "sweep_applied": False}

    try:
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"knowledge_points": [], "decayed": [], "sweep_applied": False}

    # Run decay sweep
    engine = KnowledgeMemoryEngine()
    today = date.today()
    overlay, decayed_ids = engine.decay_sweep(overlay, today)
    overlay_path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8")

    kp_points = overlay.get("knowledge_points", {})
    today_str = today.isoformat()

    items = []
    for kid, entry in kp_points.items():
        next_review = entry.get("next_review_at", "")[:10]
        overdue = next_review < today_str if next_review else False
        items.append({
            "knowledge_id": kid,
            "subject": entry.get("subject", ""),
            "heading": entry.get("heading", ""),
            "trigger": entry.get("trigger", ""),
            "status": entry.get("status", "New"),
            "state_value": entry.get("state_value", 0),
            "consecutive_successes": entry.get("consecutive_successes", 0),
            "next_review_at": entry.get("next_review_at", ""),
            "last_reviewed_at": entry.get("last_reviewed_at", ""),
            "review_interval_days": entry.get("review_interval_days", 0),
            "decay_risk": entry.get("decay_risk", "none"),
            "overdue": overdue,
        })

    items.sort(key=lambda x: x["state_value"])

    return {
        "knowledge_points": items,
        "decayed": decayed_ids,
        "sweep_applied": len(decayed_ids) > 0,
        "readiness_summary": {
            "total": len(items),
            "overdue": sum(1 for i in items if i["overdue"]),
            "by_state": {
                "new": sum(1 for i in items if i["state_value"] == 0),
                "reviewed_once": sum(1 for i in items if i["state_value"] == 1),
                "familiar": sum(1 for i in items if i["state_value"] == 2),
                "practiced": sum(1 for i in items if i["state_value"] == 3),
                "proficient": sum(1 for i in items if i["state_value"] == 4),
                "mastered": sum(1 for i in items if i["state_value"] == 5),
            },
            "high_decay_risk": sum(1 for i in items if i["decay_risk"] in ("high", "overdue")),
        },
    }
