"""Dependency injection for FastAPI — provides Repository and services."""

from __future__ import annotations

import sys
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import Depends, Header, HTTPException
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

_LANGUAGE_SCIENCE = Path(__file__).resolve().parents[2] / "packages" / "language-science" / "src"
if str(_LANGUAGE_SCIENCE) not in sys.path:
    sys.path.insert(0, str(_LANGUAGE_SCIENCE))

_RESOURCE_INGESTION = Path(__file__).resolve().parents[2] / "packages" / "resource-ingestion" / "src"
if str(_RESOURCE_INGESTION) not in sys.path:
    sys.path.insert(0, str(_RESOURCE_INGESTION))


from app.storage import Repository


# Root of the monorepo
def get_repo_root() -> Path:
    """Get the monorepo root directory."""
    override = os.environ.get("OPENEXAM_REPO_ROOT")
    return Path(override).resolve() if override else Path(__file__).resolve().parents[2]


@lru_cache()
def get_repo() -> Repository:
    """Get or create the Repository instance."""
    return Repository(get_repo_root())


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        return ""
    prefix = "Bearer "
    return authorization[len(prefix):].strip() if authorization.startswith(prefix) else ""


def get_current_user(
    repo: Repository = Depends(get_repo),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> dict[str, Any]:
    from app.local_auth import get_authenticated_user

    token = _extract_bearer_token(authorization)
    user = get_authenticated_user(repo, token)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return {**user, "session_token": token}


def require_admin_user(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return current_user


def get_agent_runtime():
    """Get the agent runtime instance."""
    from agent_runtime.runtime import AgentRuntime
    runtime = AgentRuntime(mode="local")
    runtime.init_remote()  # try to upgrade to remote if SDK available
    return runtime
