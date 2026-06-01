from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class StructuredTask:
    task_id: str
    task_type: str
    prompt: str
    completion_state: str = "pending"
    response: str = ""
    score: float | None = None
    evidence_refs: list[str] | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
