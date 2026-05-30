"""Agent Runtime — orchestrated multi-agent system.

Wraps OpenAI Agents SDK for structured handoff-based agent workflows.
Each agent has a clear role, instructions, and handoff description.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(slots=True)
class AgentSpec:
    """Specification for an agent role."""
    name: str
    instructions: str
    handoff_description: str
    model: str = "deepseek-v4-flash[1m]"


@dataclass(slots=True)
class AgentTask:
    """A task dispatched to the agent system."""
    task_id: str
    task_type: str              # "record_mistake", "diagnose", "review", "mine_patterns", "strategy", "validate"
    payload: dict = field(default_factory=dict)
    context: dict = field(default_factory=dict)  # additional context like recent events
    result: Any = None
    error: str = ""


class AgentRuntime:
    """Manages agent lifecycle and task dispatch.

    Can operate in two modes:
    - Local: uses deterministic rule-based execution (no API calls)
    - Remote: uses OpenAI Agents SDK for LLM-powered execution
    """

    def __init__(self, mode: str = "local") -> None:
        self.mode = mode
        self.specs = self._build_specs()
        self._agents: dict[str, Any] = {}

    @staticmethod
    def _build_specs() -> dict[str, AgentSpec]:
        return {
            "orchestrator": AgentSpec(
                name="orchestrator",
                instructions=(
                    "Route CFA Tier 1 mistake tasks to the right specialist "
                    "and keep the final answer coherent. "
                    "Never provide strategy without event evidence."
                ),
                handoff_description="Main coordinator for record, review, pattern mining, and strategy generation.",
            ),
            "mistake_recorder": AgentSpec(
                name="mistake_recorder",
                instructions=(
                    "Turn raw question, bias, or agent failure notes into "
                    "structured mistake events and cards. "
                    "Preserve all provenance: question source, evidence assets, "
                    "MOC target, confidence, time spent."
                ),
                handoff_description="Use for event normalization and storage-ready outputs.",
            ),
            "review_coach": AgentSpec(
                name="review_coach",
                instructions=(
                    "Explain the root cause of a mistake and produce fix rules "
                    "and next drills. For formula errors, reference the specific "
                    "formula and its conditions. For concept errors, clarify the "
                    "boundary between the confused concepts."
                ),
                handoff_description="Use for single-session retros and mistake explanation.",
            ),
            "pattern_miner": AgentSpec(
                name="pattern_miner",
                instructions=(
                    "Cluster repeated errors by topic, LOS, and error type, "
                    "then summarize the strongest signals. "
                    "Flag patterns with recurrence >= 3 as high severity. "
                    "Recommend targeted interventions for each cluster."
                ),
                handoff_description="Use for weekly or mock-level pattern analysis.",
            ),
            "strategy_coach": AgentSpec(
                name="strategy_coach",
                instructions=(
                    "Convert patterns into pre-mock and post-mock strategy advice. "
                    "Prioritize high-confidence errors, recurring patterns, "
                    "and time allocation improvements. "
                    "Every recommendation must reference specific evidence."
                ),
                handoff_description="Use for revision order, warmups, and pacing advice.",
            ),
            "validator": AgentSpec(
                name="validator",
                instructions=(
                    "Check whether a review or strategy summary misses evidence, "
                    "root causes, or known validation rules. "
                    "Flag unsupported claims. Verify that all regulatory/standards "
                    "conclusions trace back to authoritative source material."
                ),
                handoff_description="Use before returning final advice to the user.",
            ),
        }

    def init_remote(self) -> bool:
        """Try to initialize OpenAI Agents SDK agents."""
        try:
            from agents import Agent

            specs = self.specs
            mistake_recorder = Agent(
                name=specs["mistake_recorder"].name,
                handoff_description=specs["mistake_recorder"].handoff_description,
                instructions=specs["mistake_recorder"].instructions,
                model=specs["mistake_recorder"].model,
            )
            review_coach = Agent(
                name=specs["review_coach"].name,
                handoff_description=specs["review_coach"].handoff_description,
                instructions=specs["review_coach"].instructions,
                model=specs["review_coach"].model,
            )
            pattern_miner = Agent(
                name=specs["pattern_miner"].name,
                handoff_description=specs["pattern_miner"].handoff_description,
                instructions=specs["pattern_miner"].instructions,
                model=specs["pattern_miner"].model,
            )
            strategy_coach = Agent(
                name=specs["strategy_coach"].name,
                handoff_description=specs["strategy_coach"].handoff_description,
                instructions=specs["strategy_coach"].instructions,
                model=specs["strategy_coach"].model,
            )
            validator = Agent(
                name=specs["validator"].name,
                handoff_description=specs["validator"].handoff_description,
                instructions=specs["validator"].instructions,
                model=specs["validator"].model,
            )
            orchestrator = Agent(
                name=specs["orchestrator"].name,
                instructions=specs["orchestrator"].instructions,
                handoffs=[mistake_recorder, review_coach, pattern_miner, strategy_coach, validator],
                model=specs["orchestrator"].model,
            )
            self._agents = {
                "orchestrator": orchestrator,
                "mistake_recorder": mistake_recorder,
                "review_coach": review_coach,
                "pattern_miner": pattern_miner,
                "strategy_coach": strategy_coach,
                "validator": validator,
            }
            self.mode = "remote"
            return True
        except ImportError:
            return False

    def get_spec(self, name: str) -> AgentSpec | None:
        return self.specs.get(name)

    def list_agents(self) -> list[str]:
        return list(self.specs.keys())

    def dispatch(self, task: AgentTask) -> AgentTask:
        """Dispatch a task to the appropriate agent (local/rule-based fallback)."""
        # In local mode, tasks are handled by the deterministic workflows
        # in .system/app/workflows.py — this runtime provides the agent
        # metadata and routing logic.
        routing = {
            "record_mistake": "mistake_recorder",
            "diagnose": "review_coach",
            "review": "review_coach",
            "mine_patterns": "pattern_miner",
            "strategy": "strategy_coach",
            "validate": "validator",
        }
        agent_name = routing.get(task.task_type, "orchestrator")
        spec = self.specs.get(agent_name)
        if spec:
            task.context["agent_name"] = spec.name
            task.context["agent_instructions"] = spec.instructions
        return task
