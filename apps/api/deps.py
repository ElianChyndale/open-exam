"""Dependency injection for FastAPI — provides Repository and services."""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

# Ensure .system/app is importable
_SYSTEM = Path(__file__).resolve().parents[2] / ".system"
if str(_SYSTEM) not in sys.path:
    sys.path.insert(0, str(_SYSTEM))

# Ensure study-science package is importable
_STUDY_SCIENCE = Path(__file__).resolve().parents[2] / "packages" / "study-science" / "src"
if str(_STUDY_SCIENCE) not in sys.path:
    sys.path.insert(0, str(_STUDY_SCIENCE))

_EXAM_CORE = Path(__file__).resolve().parents[2] / "packages" / "exam-core" / "src"
if str(_EXAM_CORE) not in sys.path:
    sys.path.insert(0, str(_EXAM_CORE))

_AGENT_RUNTIME = Path(__file__).resolve().parents[2] / "packages" / "agent-runtime" / "src"
if str(_AGENT_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_AGENT_RUNTIME))

_LEARNING_RECORDS = Path(__file__).resolve().parents[2] / "packages" / "learning-records" / "src"
if str(_LEARNING_RECORDS) not in sys.path:
    sys.path.insert(0, str(_LEARNING_RECORDS))

_LEARNER_TWIN = Path(__file__).resolve().parents[2] / "packages" / "learner-twin" / "src"
if str(_LEARNER_TWIN) not in sys.path:
    sys.path.insert(0, str(_LEARNER_TWIN))


from app.storage import Repository


# Root of the monorepo
def get_repo_root() -> Path:
    """Get the monorepo root directory."""
    return Path(__file__).resolve().parents[2]


@lru_cache()
def get_repo() -> Repository:
    """Get or create the Repository instance."""
    return Repository(get_repo_root())


def get_agent_runtime():
    """Get the agent runtime instance."""
    from agent_runtime.runtime import AgentRuntime
    runtime = AgentRuntime(mode="local")
    runtime.init_remote()  # try to upgrade to remote if SDK available
    return runtime
