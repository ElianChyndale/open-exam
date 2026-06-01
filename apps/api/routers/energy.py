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

    # Generate warnings (including sleep/stress)
    warnings: list[str] = []
    if req.energy_level <= 1:
        warnings.append("⚠️ 当前精力偏低，不建议学习新知识或做高难度练习。")
    if req.energy_level == 0:
        warnings.append("🛑 精力耗尽。建议休息或仅做被动回顾。")
    if req.physical_fatigue >= 8:
        warnings.append("😴 身体疲劳度高，建议先休息再学习。")
    if req.sleep_hours > 0 and req.sleep_hours < 6:
        warnings.append(f"😴 睡眠仅 {req.sleep_hours:.0f} 小时，睡眠不足会影响记忆巩固和学习效率。")
    if req.stress_level >= 7:
        warnings.append("🧘 压力水平偏高（{}/10），高压状态下学习效率会显著下降，建议先做放松。".format(req.stress_level))

    # Save the check-in as an event
    from datetime import datetime, UTC
    from app.models import stable_id

    stable_parts = (
        str(req.energy_level),
        str(req.mental_clarity),
        str(req.physical_fatigue),
        str(req.motivation),
        str(req.sleep_hours),
        str(req.stress_level),
        datetime.now(UTC).strftime('%Y%m%d'),
    )
    check_in_id = stable_id("en", *stable_parts)
    check_in_data = {
        "schema_version": 1,
        "event_type": "energy.checked_in",
        "learner_id": "local",
        "check_in_id": check_in_id,
        "energy_level": req.energy_level,
        "mental_clarity": req.mental_clarity,
        "physical_fatigue": req.physical_fatigue,
        "motivation": req.motivation,
        "sleep_hours": req.sleep_hours,
        "stress_level": req.stress_level,
        "notes": req.notes,
        "created_at": datetime.now(UTC).isoformat(),
        "occurred_at": datetime.now(UTC).isoformat(),
        "source_refs": [],
    }
    check_in_data["event_id"] = check_in_id
    check_in_data["payload"] = {
        key: check_in_data[key]
        for key in ("energy_level", "mental_clarity", "physical_fatigue", "motivation", "sleep_hours", "stress_level", "notes")
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
