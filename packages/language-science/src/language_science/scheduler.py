from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, Protocol


Rating = Literal["again", "hard", "good", "easy"]


@dataclass(slots=True)
class ScheduleDecision:
    next_due_at: str
    stability: float
    difficulty: float
    retrievability: float
    state: str
    repetitions: int
    explanation: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class MemorySchedulerProtocol(Protocol):
    @classmethod
    def preview(cls, state: dict[str, Any] | None = None, *, now: datetime | None = None) -> dict[Rating, ScheduleDecision]: ...

    @classmethod
    def schedule(cls, state: dict[str, Any] | None, rating: Rating, *, now: datetime | None = None) -> ScheduleDecision: ...


class FSRSCompatibleScheduler:
    """Sparse-data deterministic scheduler with an FSRS-compatible interface."""

    INTERVALS = {"again": 0.01, "hard": 1.0, "good": 3.0, "easy": 7.0}

    @classmethod
    def schedule(cls, state: dict[str, Any] | None, rating: Rating, *, now: datetime | None = None) -> ScheduleDecision:
        if rating not in cls.INTERVALS:
            raise ValueError(f"Unsupported language review rating: {rating}")
        current = dict(state or {})
        repetitions = int(current.get("repetitions", 0)) + 1
        old_stability = float(current.get("stability", 1.0))
        old_difficulty = float(current.get("difficulty", 5.0))
        multipliers = {"again": 0.35, "hard": 1.2, "good": 2.2, "easy": 3.2}
        stability = max(0.25, round(old_stability * multipliers[rating], 4))
        difficulty = round(max(1.0, min(10.0, old_difficulty + {"again": 1.0, "hard": 0.3, "good": -0.2, "easy": -0.5}[rating])), 4)
        interval_days = max(cls.INTERVALS[rating], stability * cls.INTERVALS[rating])
        current_time = now or datetime.now(UTC)
        due = current_time + timedelta(days=interval_days)
        return ScheduleDecision(
            next_due_at=due.isoformat(),
            stability=stability,
            difficulty=difficulty,
            retrievability=1.0 if rating != "again" else 0.45,
            state="relearning" if rating == "again" else "review",
            repetitions=repetitions,
            explanation=f"FSRS-compatible sparse schedule: rating={rating}, interval={interval_days:.2f}d.",
        )

    @classmethod
    def preview(cls, state: dict[str, Any] | None = None, *, now: datetime | None = None) -> dict[Rating, ScheduleDecision]:
        return {rating: cls.schedule(state, rating, now=now) for rating in ("again", "hard", "good", "easy")}
