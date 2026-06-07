from __future__ import annotations

import sys
import types

from app.agents_runtime import build_agent_specs, build_openai_agents


def test_build_agent_specs_preserves_six_roles_and_tutor_contract() -> None:
    specs = build_agent_specs()

    assert set(specs) == {
        "orchestrator",
        "mistake_recorder",
        "review_coach",
        "pattern_miner",
        "strategy_coach",
        "validator",
    }
    assert "Knowledge Framework" in specs["review_coach"].instructions
    assert "Step-by-Step Solution Logic" in specs["review_coach"].instructions
    assert "BA II Plus Use" in specs["review_coach"].instructions
    assert "uploaded-file contents" in specs["review_coach"].instructions
    assert "concept teaching" in specs["orchestrator"].instructions


def test_build_openai_agents_reuses_existing_roles_for_tutoring(monkeypatch) -> None:
    class FakeAgent:
        def __init__(self, **kwargs) -> None:
            self.__dict__.update(kwargs)

    monkeypatch.setitem(sys.modules, "agents", types.SimpleNamespace(Agent=FakeAgent))

    built = build_openai_agents()

    assert set(built) == {
        "orchestrator",
        "mistake_recorder",
        "review_coach",
        "pattern_miner",
        "strategy_coach",
        "validator",
    }
    assert [agent.name for agent in built["orchestrator"].handoffs] == [
        "mistake_recorder",
        "review_coach",
        "pattern_miner",
        "strategy_coach",
        "validator",
    ]
    assert "beginner-safe CFA tutor" in built["review_coach"].instructions
