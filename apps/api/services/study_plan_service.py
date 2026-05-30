"""Study plan service — integrates review pack with energy-aware planning."""

from __future__ import annotations

import sys
from pathlib import Path

for pkg in ["exam-core", "study-science"]:
    pkg_path = Path(__file__).resolve().parents[3] / "packages" / pkg / "src"
    if str(pkg_path) not in sys.path:
        sys.path.insert(0, str(pkg_path))


def build_daily_plan(
    topic: str,
    energy_level: int,
    available_minutes: int,
    review_items: list[dict],
    danger_los: list[str],
) -> dict:
    """Build a complete daily study plan with energy-aware task allocation."""
    from study_science.energy_planner import EnergyAwarePlanner, EnergyProfile
    from study_science.interleaving import InterleavingBuilder, InterleavingConfig

    profile = EnergyProfile(
        energy_level=energy_level,
        available_minutes=available_minutes,
    )

    # Convert review items to tasks
    tasks = []
    for item in review_items[:30]:
        tasks.append({
            "task_type": _map_error_to_task(item.get("error_type", "")),
            "description": f"{item.get('topic', '')} / {item.get('los', '')}: {item.get('fix_rule', '修正')}",
            "priority": item.get("priority", 50),
        })

    # Add focus topic task
    if topic:
        tasks.insert(0, {
            "task_type": "new_knowledge",
            "description": f"学习 {topic} 主内容",
            "priority": 90,
        })

    plan = EnergyAwarePlanner.allocate(tasks, profile)
    task_order = EnergyAwarePlanner.optimal_task_order(profile)

    # Build interleaving mix suggestion
    weak_items = [t for t in tasks if t["priority"] >= 70]
    old_items = [t for t in tasks if 40 <= t["priority"] < 70]
    maint_items = [t for t in tasks if t["priority"] < 40]

    interleaving = InterleavingBuilder.build(
        weak_items=weak_items,
        old_mistake_items=old_items,
        maintenance_items=maint_items,
        config=InterleavingConfig(max_items=min(20, available_minutes // 5)),
    )

    return {
        "energy_profile": {
            "level": energy_level,
            "available_minutes": available_minutes,
        },
        "task_order": task_order,
        "high_energy": [
            {"type": t.task_type, "desc": t.task_description, "fit": t.fit_score}
            for t in plan.high_energy_slot[:5]
        ],
        "moderate_energy": [
            {"type": t.task_type, "desc": t.task_description, "fit": t.fit_score}
            for t in plan.moderate_energy_slot[:5]
        ],
        "low_energy": [
            {"type": t.task_type, "desc": t.task_description, "fit": t.fit_score}
            for t in plan.low_energy_slot[:5]
        ],
        "warnings": plan.warnings,
        "danger_los": danger_los[:3],
        "interleaving_composition": interleaving.composition,
    }


def _map_error_to_task(error_type: str) -> str:
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
