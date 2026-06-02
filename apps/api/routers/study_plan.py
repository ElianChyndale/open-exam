"""GET /api/study-plan/today — Daily study plan generation.

Integrates: energy check, review pack, todo list, and cognitive science engines.
"""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query

from deps import get_repo
from schemas import StudyPlanResponse

router = APIRouter()


@router.get("/today", response_model=StudyPlanResponse)
def get_today_study_plan(
    date_str: str = Query(default="", alias="date"),
    energy_level: int | None = Query(default=None, ge=0, le=4),
    available_minutes: int = Query(default=120, ge=10),
    focus_topic: str = Query(default=""),
    repo=Depends(get_repo),
):
    """Generate today's complete study plan.

    Integrates:
    - Energy-aware task allocation
    - Review pack items as tasks
    - Pattern-based weak LOS identification
    - Calibration warnings
    """
    from app.workflows import (
        collect_due_card_items,
        collect_pattern_items,
        collect_recent_low_confidence_items,
        merge_review_sources,
        mine_patterns,
    )
    target_date = date.fromisoformat(date_str) if date_str else date.today()
    if energy_level is None:
        saved_energy = repo.load_energy_events()
        energy_level = int(saved_energy[-1].get("energy_level", 2)) if saved_energy else 2

    # Gather review items
    mine_patterns(repo)
    due = collect_due_card_items(repo, target_date)
    recent = collect_recent_low_confidence_items(repo, target_date, 7)
    patterns = collect_pattern_items(repo)
    review_items = merge_review_sources(due, patterns, recent)

    # Identify danger LOS
    danger_topics: dict[str, int] = {}
    for item in review_items:
        key = f"{item.get('topic', '')} / {item.get('los', '')}"
        if item.get("priority", 0) >= 80:
            danger_topics[key] = danger_topics.get(key, 0) + 1
    danger_list = sorted(danger_topics, key=danger_topics.get, reverse=True)[:3]

    # Focus reason
    focus_reason = ""
    if focus_topic:
        focus_reason = f"今日主线: {focus_topic}"
    elif danger_list:
        focus_reason = f"最弱领域: {danger_list[0]}"
    else:
        focus_reason = "按到期错题和间隔复习安排"

    from services.study_plan_service import build_daily_plan
    plan = build_daily_plan(
        topic=focus_topic,
        energy_level=energy_level,
        available_minutes=available_minutes,
        review_items=review_items,
        danger_los=danger_list,
    )

    return StudyPlanResponse(
        plan_id=f"sp-{target_date.isoformat()}",
        date=target_date.isoformat(),
        energy_level=energy_level,
        available_minutes=available_minutes,
        focus_topic=focus_topic or (danger_list[0] if danger_list else ""),
        focus_reason=focus_reason,
        high_energy_tasks=[
            {"task_type": task["type"], "description": task["desc"], "fit": task["fit"]}
            for task in plan["high_energy"]
        ],
        moderate_energy_tasks=[
            {"task_type": task["type"], "description": task["desc"], "fit": task["fit"]}
            for task in plan["moderate_energy"]
        ],
        low_energy_tasks=[
            {"task_type": task["type"], "description": task["desc"], "fit": task["fit"]}
            for task in plan["low_energy"]
        ],
        danger_los_list=danger_list,
        warnings=plan["warnings"],
        interleaving_composition=plan["interleaving_composition"],
    )


@router.get("/weekly-focus")
def get_weekly_focus(repo=Depends(get_repo)):
    """Get weekly study focus recommendation."""
    from app.workflows import weekly_focus_recommendation
    result = weekly_focus_recommendation(repo)
    return {"recommendation": result}
