"""GET /api/study-plan/today — Daily study plan generation.

Integrates: energy check, review pack, todo list, and cognitive science engines.
"""

from __future__ import annotations

from datetime import date, datetime

from fastapi import APIRouter, Depends, Query

from deps import get_repo
from schemas import StudyPlanRequest, StudyPlanResponse

router = APIRouter()


@router.get("/today", response_model=StudyPlanResponse)
async def get_today_study_plan(
    date_str: str = Query(default="", alias="date"),
    energy_level: int = Query(default=2, ge=0, le=4),
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
        build_warm_start_items,
        mine_patterns,
    )
    from study_science.energy_planner import EnergyAwarePlanner, EnergyProfile

    target_date = date.fromisoformat(date_str) if date_str else date.today()

    # Gather review items
    mine_patterns(repo)
    due = collect_due_card_items(repo, target_date)
    recent = collect_recent_low_confidence_items(repo, target_date, 7)
    patterns = collect_pattern_items(repo)
    review_items = merge_review_sources(due, patterns, recent)

    # Build energy profile
    profile = EnergyProfile(
        energy_level=energy_level,
        available_minutes=available_minutes,
    )

    # Convert review items to tasks
    tasks = []
    for item in review_items[:30]:
        tasks.append({
            "task_type": _map_to_task_type(item.get("error_type", "")),
            "description": f"{item.get('topic', '')} / {item.get('los', '')}: {item.get('fix_rule', '')}",
            "priority": item.get("priority", 50),
        })

    # Add focus topic tasks if specified
    if focus_topic:
        tasks.insert(0, {
            "task_type": "new_knowledge",
            "description": f"学习 {focus_topic} 主内容",
            "priority": 90,
        })

    # Energy-aware allocation
    plan = EnergyAwarePlanner.allocate(tasks, profile)

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

    return StudyPlanResponse(
        plan_id=f"sp-{target_date.isoformat()}",
        date=target_date.isoformat(),
        energy_level=energy_level,
        available_minutes=available_minutes,
        focus_topic=focus_topic or (danger_list[0] if danger_list else ""),
        focus_reason=focus_reason,
        high_energy_tasks=[
            {"task_type": t.task_type, "description": t.task_description, "fit": t.fit_score}
            for t in plan.high_energy_slot[:5]
        ],
        moderate_energy_tasks=[
            {"task_type": t.task_type, "description": t.task_description, "fit": t.fit_score}
            for t in plan.moderate_energy_slot[:5]
        ],
        low_energy_tasks=[
            {"task_type": t.task_type, "description": t.task_description, "fit": t.fit_score}
            for t in plan.low_energy_slot[:5]
        ],
        danger_los_list=danger_list,
        warnings=plan.warnings,
    )


def _map_to_task_type(error_type: str) -> str:
    """Map error type to task category for energy planning."""
    mapping = {
        "concept_confusion": "concept_discrimination",
        "formula_misuse": "formula_drill",
        "knowledge_gap": "new_knowledge",
        "careless_reading": "active_recall",
        "time_pressure": "active_recall",
        "confidence_calibration_failure": "mistake_review",
        "fatigue_energy_mismatch": "light_review",
        "agent_failure": "mistake_review",
    }
    return mapping.get(error_type, "mistake_review")


@router.get("/weekly-focus")
async def get_weekly_focus(repo=Depends(get_repo)):
    """Get weekly study focus recommendation."""
    from app.workflows import weekly_focus_recommendation
    result = weekly_focus_recommendation(repo)
    return {"recommendation": result}
