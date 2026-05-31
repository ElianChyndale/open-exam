from __future__ import annotations

from study_science.energy_planner import EnergyAwarePlanner, EnergyProfile


def test_allocate_sorts_multiple_tasks_without_mutating_lookup_state() -> None:
    profile = EnergyProfile(energy_level=2)
    tasks = [
        {"task_type": "concept_discrimination", "description": "lower priority", "priority": 20},
        {"task_type": "active_recall", "description": "higher priority", "priority": 90},
        {"task_type": "new_knowledge", "description": "poor fit", "priority": 100},
    ]

    plan = EnergyAwarePlanner.allocate(tasks, profile)

    descriptions = [
        fit.task_description
        for fit in plan.moderate_energy_slot + plan.low_energy_slot
    ]
    assert descriptions == ["higher priority", "lower priority", "poor fit"]
