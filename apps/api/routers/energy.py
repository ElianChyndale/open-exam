"""POST /api/energy/check-in — Energy check-in and planning."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from deps import get_repo
from schemas import EnergyCheckInRequest, EnergyCheckInResponse

router = APIRouter()


@router.post("/check-in", response_model=EnergyCheckInResponse)
async def energy_check_in(req: EnergyCheckInRequest, repo=Depends(get_repo)):
    """Record energy level and get recommended task ordering.

    Uses the Energy-Aware Planner from study-science to recommend
    which task types to do now vs defer.
    """
    from study_science.energy_planner import EnergyAwarePlanner, EnergyProfile

    profile = EnergyProfile(
        energy_level=req.energy_level,
        mental_clarity=req.mental_clarity,
        physical_fatigue=req.physical_fatigue,
        motivation=req.motivation,
        available_minutes=120,
    )

    # Get recommended task order
    task_order = EnergyAwarePlanner.optimal_task_order(profile)
    from services.daily_loop_service import refit_today_tasks

    refit_today_tasks(repo, task_order)

    # Generate warnings
    warnings: list[str] = []
    if req.energy_level <= 1:
        warnings.append("⚠️ 当前精力偏低，不建议学习新知识或做高难度练习。")
    if req.energy_level == 0:
        warnings.append("🛑 精力耗尽。建议休息或仅做被动回顾。")
    if req.physical_fatigue >= 8:
        warnings.append("😴 身体疲劳度高，建议先休息再学习。")

    # Save the check-in as an event
    from datetime import datetime, UTC

    check_in_id = f"en-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
    check_in_data = {
        "check_in_id": check_in_id,
        "energy_level": req.energy_level,
        "mental_clarity": req.mental_clarity,
        "physical_fatigue": req.physical_fatigue,
        "motivation": req.motivation,
        "notes": req.notes,
        "created_at": datetime.now(UTC).isoformat(),
    }

    repo.append_energy_event(check_in_data)

    return EnergyCheckInResponse(
        check_in_id=check_in_id,
        energy_level=req.energy_level,
        recommended_task_order=task_order,
        warnings=warnings,
    )


@router.get("/history")
async def energy_history(limit: int = 30, repo=Depends(get_repo)):
    """Get recent energy check-in history."""
    events = repo.load_energy_events()

    recent = events[-limit:]
    return {
        "count": len(recent),
        "total": len(events),
        "history": list(reversed(recent)),
    }
