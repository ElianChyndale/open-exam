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


def test_fit_score_exact_match_is_higher_than_marginal() -> None:
    """Exact energy match should score 0.9; one level below should score 0.5."""
    assert EnergyAwarePlanner.fit_score("new_knowledge", energy_level=3) == 0.9
    assert EnergyAwarePlanner.fit_score("new_knowledge", energy_level=2) == 0.5
    assert EnergyAwarePlanner.fit_score("new_knowledge", energy_level=1) == 0.1


def test_allocate_buckets_by_fit_score_not_raw_requirement() -> None:
    """Tasks with poor fit (score < 0.4) must land in low_energy_slot,
    not moderate, even when energy_level >= 1."""
    profile = EnergyProfile(energy_level=1)
    tasks = [
        {"task_type": "new_knowledge", "description": "requires 3", "priority": 50},
        {"task_type": "mistake_review", "description": "requires 2", "priority": 50},
        {"task_type": "light_review", "description": "requires 0", "priority": 50},
    ]

    plan = EnergyAwarePlanner.allocate(tasks, profile)

    # new_knowledge (req=3) at energy=1 → fit=0.1 → must be in low
    assert any(f.task_description == "requires 3" for f in plan.low_energy_slot)
    assert not any(f.task_description == "requires 3" for f in plan.moderate_energy_slot)

    # mistake_review (req=2) at energy=1 → fit=0.5 → moderate
    assert any(f.task_description == "requires 2" for f in plan.moderate_energy_slot)

    # light_review (req=0) at energy=1 → fit=1.0 → low (because req < 1)
    assert any(f.task_description == "requires 0" for f in plan.low_energy_slot)


def test_allocate_high_energy_slot_only_when_appropriate() -> None:
    """High-energy tasks should only appear in high_energy_slot when
    energy_level is high enough for a comfortable or exact fit."""
    tasks = [
        {"task_type": "mock_exam", "description": "mock", "priority": 50},
        {"task_type": "difficult_practice", "description": "hard", "priority": 50},
    ]

    # energy=4: mock (req=4) fit=0.9 → high; difficult (req=3) fit=1.0 → high
    plan_peak = EnergyAwarePlanner.allocate(tasks, EnergyProfile(energy_level=4))
    assert len(plan_peak.high_energy_slot) == 2

    # energy=3: mock (req=4) fit=0.5 → moderate; difficult (req=3) fit=0.9 → high
    plan_high = EnergyAwarePlanner.allocate(tasks, EnergyProfile(energy_level=3))
    assert any(f.task_description == "hard" for f in plan_high.high_energy_slot)
    assert any(f.task_description == "mock" for f in plan_high.moderate_energy_slot)

    # energy=2: mock (req=4) fit=0.1 → low; difficult (req=3) fit=0.5 → moderate
    plan_mod = EnergyAwarePlanner.allocate(tasks, EnergyProfile(energy_level=2))
    assert len(plan_mod.high_energy_slot) == 0
    assert any(f.task_description == "hard" for f in plan_mod.moderate_energy_slot)
    assert any(f.task_description == "mock" for f in plan_mod.low_energy_slot)


def test_allocate_warnings_include_sleep_and_stress() -> None:
    profile = EnergyProfile(
        energy_level=2,
        sleep_hours=4.5,
        stress_level=8,
        physical_fatigue=9,
    )
    plan = EnergyAwarePlanner.allocate([], profile)

    warnings_text = " ".join(plan.warnings)
    assert "睡眠" in warnings_text
    assert "压力" in warnings_text
    assert "疲劳" in warnings_text
