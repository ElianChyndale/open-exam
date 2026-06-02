"""FSRS-6 scheduler with optimized parameters from day one.

Real py-fsrs v6.3.1 integration via the `fsrs` pip package.
- Uses a single set of optimized parameters (no graduated vs simplified split)
- py-fsrs unavailable: fallback fixed multipliers (param_version=0)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, Protocol

from language_science.fsrs_cache import FSRSStateCache

try:
    from fsrs import Card, Rating as FsrsRating, Scheduler, State as FsrsState
    FSRS_AVAILABLE = True
except ImportError:
    FSRS_AVAILABLE = False


Rating = Literal["again", "hard", "good", "easy"]

RATING_MAP: dict[str, Any] = {
    "again": FsrsRating.Again,
    "hard": FsrsRating.Hard,
    "good": FsrsRating.Good,
    "easy": FsrsRating.Easy,
} if FSRS_AVAILABLE else {}

# Default FSRS parameters (optimized set, no graduated/simplified split)
DEFAULT_PARAMS = (
    0.5, 1.5, 3.0, 8.0, 5.0, 0.8, 3.0, 0.001, 1.8, 0.15,
    0.8, 1.5, 0.06, 0.26, 1.6, 0.6, 1.8, 0.5, 0.09, 0.15, 0.15,
)

# Fallback fixed multipliers (only used when py-fsrs unavailable)
_FALLBACK_INTERVALS = {"again": 0.01, "hard": 1.0, "good": 3.0, "easy": 7.0}
_FALLBACK_MULTIPLIERS = {"again": 0.35, "hard": 1.2, "good": 2.2, "easy": 3.2}


@dataclass(slots=True)
class ScheduleDecision:
    next_due_at: str
    stability: float
    difficulty: float
    retrievability: float
    state: str
    repetitions: int
    explanation: str
    param_version: int = 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "next_due_at": self.next_due_at,
            "stability": self.stability,
            "difficulty": self.difficulty,
            "retrievability": self.retrievability,
            "state": self.state,
            "repetitions": self.repetitions,
            "explanation": self.explanation,
            "param_version": self.param_version,
        }


class MemorySchedulerProtocol(Protocol):
    @classmethod
    def preview(cls, state: dict[str, Any] | None = None, *, now: datetime | None = None) -> dict[Rating, ScheduleDecision]: ...
    @classmethod
    def schedule(cls, state: dict[str, Any] | None, rating: Rating, *, now: datetime | None = None) -> ScheduleDecision: ...


class _FallbackScheduler:
    """Fixed-multiplier fallback when py-fsrs is not installed."""

    @classmethod
    def schedule(cls, state: dict[str, Any] | None, rating: Rating, *, now: datetime | None = None) -> ScheduleDecision:
        if rating not in _FALLBACK_MULTIPLIERS:
            raise ValueError(f"Unsupported rating: {rating}")
        current = dict(state or {})
        repetitions = int(current.get("repetitions", 0)) + 1
        old_stability = float(current.get("stability", 1.0))
        old_difficulty = float(current.get("difficulty", 5.0))
        stability = max(0.25, round(old_stability * _FALLBACK_MULTIPLIERS[rating], 4))
        difficulty = round(max(1.0, min(10.0, old_difficulty + {"again": 1.0, "hard": 0.3, "good": -0.2, "easy": -0.5}[rating])), 4)
        interval_days = _FALLBACK_INTERVALS[rating] * max(1.0, stability)
        current_time = now or datetime.now(UTC)
        due = current_time + timedelta(days=interval_days)
        return ScheduleDecision(
            next_due_at=due.isoformat(), stability=stability, difficulty=difficulty,
            retrievability=1.0 if rating != "again" else 0.45,
            state="relearning" if rating == "again" else "review",
            repetitions=repetitions, param_version=0,
            explanation=f"Fallback: rating={rating}, interval={interval_days:.2f}d.",
        )

    @classmethod
    def preview(cls, state: dict[str, Any] | None = None, *, now: datetime | None = None) -> dict[Rating, ScheduleDecision]:
        return {r: cls.schedule(state, r, now=now) for r in ("again", "hard", "good", "easy")}


# Map old-format state strings to fsrs State enum
_STATE_MAP = {
    "new": FsrsState.Learning,       # fsrs starts in Learning
    "learning": FsrsState.Learning,
    "review": FsrsState.Review,
    "relearning": FsrsState.Relearning,
}


def _legacy_state_to_fsrs_card(state: dict[str, Any] | None) -> Card:
    """Convert old-format fsrs_state to a py-fsrs Card object."""
    if state is None:
        return Card()
    stability = state.get("stability")
    difficulty = state.get("difficulty")
    state_str = str(state.get("state", "new")).lower()
    card = Card()
    card.stability = float(stability) if stability is not None else None
    card.difficulty = float(difficulty) if difficulty is not None else None
    card.state = _STATE_MAP.get(state_str, FsrsState.Learning)
    if "due" in state:
        card.due = state["due"]
    if "last_review" in state:
        card.last_review = state["last_review"]
    return card


_SCHEDULER: Scheduler | None = None


def _get_scheduler() -> Scheduler:
    """Get or create cached Scheduler instance with optimized parameters."""
    global _SCHEDULER
    if _SCHEDULER is None:
        _SCHEDULER = Scheduler(parameters=DEFAULT_PARAMS)
    return _SCHEDULER


def _card_to_schedule_decision(card: Card, rating: Rating, scheduler: Scheduler) -> ScheduleDecision:
    """Convert a py-fsrs Card after review into a ScheduleDecision."""
    state_name = card.state.name.lower() if hasattr(card.state, "name") else str(card.state)
    retrievability = scheduler.get_card_retrievability(card, card.due) if card.due else 1.0
    return ScheduleDecision(
        next_due_at=str(card.due) if card.due else datetime.now(UTC).isoformat(),
        stability=float(card.stability) if card.stability is not None else 1.0,
        difficulty=float(card.difficulty) if card.difficulty is not None else 5.0,
        retrievability=float(retrievability),
        state=state_name,
        repetitions=card.step if hasattr(card, "step") else 0,
        param_version=2,
        explanation=f"FSRS-6: rating={rating}, stability={card.stability}, difficulty={card.difficulty}",
    )


class FSRS6Scheduler:
    """FSRS-6 scheduler with optimized parameters from day one."""

    @classmethod
    def schedule(cls, state: dict[str, Any] | None, rating: Rating, *, now: datetime | None = None, _cache: FSRSStateCache | None = None) -> ScheduleDecision:
        if not FSRS_AVAILABLE:
            return _FallbackScheduler.schedule(state, rating, now=now)

        # Wire cache: use cached state if available
        if _cache is not None and state is not None:
            card_id = str(state.get("card_id", ""))
            if card_id:
                state = _cache.get_or_compute(card_id, lambda: state)  # type: ignore[arg-type]

        scheduler = _get_scheduler()
        card = _legacy_state_to_fsrs_card(state)
        rating_enum = RATING_MAP[rating]
        card, _ = scheduler.review_card(card, rating_enum)

        return _card_to_schedule_decision(card, rating, scheduler)

    @classmethod
    def preview(cls, state: dict[str, Any] | None = None, *, now: datetime | None = None) -> dict[Rating, ScheduleDecision]:
        return {r: cls.schedule(state, r, now=now) for r in ("again", "hard", "good", "easy")}

    @classmethod
    def total_reviews_from_events(cls, events: list[dict[str, Any]]) -> int:
        """Count total language.review.completed events."""
        return sum(1 for e in events if e.get("event_type") == "language.review.completed")
