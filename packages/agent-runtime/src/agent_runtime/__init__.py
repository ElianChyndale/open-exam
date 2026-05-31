"""Agent Runtime — pluggable AI agent orchestration for OpenExam.

Six agent roles from PLAN.md:
- orchestrator: route tasks to specialists
- mistake_recorder: normalize mistakes into structured events
- review_coach: explain root causes, produce fix rules and drills
- pattern_miner: cluster repeated errors
- strategy_coach: convert patterns into strategy advice
- validator: check outputs for evidence gaps
"""

from agent_runtime.runtime import AgentRuntime, AgentSpec, AgentTask

__all__ = ["AgentRuntime", "AgentSpec", "AgentTask"]
