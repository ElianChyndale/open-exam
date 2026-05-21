from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class AgentSpec:
    name: str
    instructions: str
    handoff_description: str


def build_agent_specs() -> dict[str, AgentSpec]:
    return {
        "orchestrator": AgentSpec(
            name="orchestrator",
            instructions="Route CFA Tier 1 mistake tasks to the right specialist and keep the final answer coherent.",
            handoff_description="Main coordinator for record, review, pattern mining, and strategy generation.",
        ),
        "mistake_recorder": AgentSpec(
            name="mistake_recorder",
            instructions="Turn raw question, bias, or agent failure notes into structured mistake events and cards.",
            handoff_description="Use for event normalization and storage-ready outputs.",
        ),
        "review_coach": AgentSpec(
            name="review_coach",
            instructions="Explain the root cause of a mistake and produce fix rules and next drills.",
            handoff_description="Use for single-session retros and mistake explanation.",
        ),
        "pattern_miner": AgentSpec(
            name="pattern_miner",
            instructions="Cluster repeated errors by topic, LOS, and error type, then summarize the strongest signals.",
            handoff_description="Use for weekly or mock-level pattern analysis.",
        ),
        "strategy_coach": AgentSpec(
            name="strategy_coach",
            instructions="Convert patterns into pre-mock and post-mock strategy advice.",
            handoff_description="Use for revision order, warmups, and pacing advice.",
        ),
        "validator": AgentSpec(
            name="validator",
            instructions="Check whether a review or strategy summary misses evidence, root causes, or known validation rules.",
            handoff_description="Use before returning final advice to the user.",
        ),
    }


def build_openai_agents() -> dict[str, Any]:
    try:
        from agents import Agent
    except ImportError:
        return {}

    specs = build_agent_specs()
    review_coach = Agent(
        name=specs["review_coach"].name,
        handoff_description=specs["review_coach"].handoff_description,
        instructions=specs["review_coach"].instructions,
    )
    pattern_miner = Agent(
        name=specs["pattern_miner"].name,
        handoff_description=specs["pattern_miner"].handoff_description,
        instructions=specs["pattern_miner"].instructions,
    )
    strategy_coach = Agent(
        name=specs["strategy_coach"].name,
        handoff_description=specs["strategy_coach"].handoff_description,
        instructions=specs["strategy_coach"].instructions,
    )
    validator = Agent(
        name=specs["validator"].name,
        handoff_description=specs["validator"].handoff_description,
        instructions=specs["validator"].instructions,
    )
    mistake_recorder = Agent(
        name=specs["mistake_recorder"].name,
        handoff_description=specs["mistake_recorder"].handoff_description,
        instructions=specs["mistake_recorder"].instructions,
    )
    orchestrator = Agent(
        name=specs["orchestrator"].name,
        instructions=specs["orchestrator"].instructions,
        handoffs=[mistake_recorder, review_coach, pattern_miner, strategy_coach, validator],
    )
    return {
        "orchestrator": orchestrator,
        "mistake_recorder": mistake_recorder,
        "review_coach": review_coach,
        "pattern_miner": pattern_miner,
        "strategy_coach": strategy_coach,
        "validator": validator,
    }

