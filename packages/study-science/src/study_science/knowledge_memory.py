"""Knowledge Memory Engine — graduated memory states with forgetting-curve feedback.

Completes the system's ecological loop:
  review → knowledge-state update → next-review scheduling → decay tracking → dashboard readiness

Based on Ebbingaus forgetting curve and spaced repetition research. Knowledge points
progress through 6 states and decay if not reinforced.

State machine:
  New (0) → Reviewed (1) ↔ Familiar (2) ↔ Practiced (3) ↔ Proficient (4) ↔ Mastered (5)
     ↑           |            |             |               |               |
     └───────────┴────────────┴─────────────┴───────────────┴───────────────┘
                          Decay on timeout or "forgot" outcome
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import IntEnum
from typing import Any


class KnowledgeState(IntEnum):
    """Graduated knowledge mastery states.

    Each level corresponds to a deeper encoding in long-term memory,
    with correspondingly longer intervals before decay.
    """
    NEW = 0
    REVIEWED = 1       # Reviewed once, fragile — needs consolidation
    FAMILIAR = 2       # Can recall with effort, 1-2 good reviews
    PRACTICED = 3      # Reliable recall, 3-4 good reviews
    PROFICIENT = 4     # Quick recall, 5-7 good reviews
    MASTERED = 5       # Automatic recall, 8+ good reviews, exam-ready

    @classmethod
    def from_str(cls, s: str) -> "KnowledgeState":
        mapping = {
            "New": cls.NEW, "Reviewed once": cls.REVIEWED,
            "Familiar": cls.FAMILIAR, "Practiced": cls.PRACTICED,
            "Proficient": cls.PROFICIENT, "Mastered": cls.MASTERED,
        }
        return mapping.get(s, cls.NEW)

    def to_status_str(self) -> str:
        mapping = {
            self.NEW: "New",
            self.REVIEWED: "Reviewed once",
            self.FAMILIAR: "Familiar",
            self.PRACTICED: "Practiced",
            self.PROFICIENT: "Proficient",
            self.MASTERED: "Mastered",
        }
        return mapping[self]


@dataclass
class KnowledgeMemoryConfig:
    """Per-state intervals and decay parameters.

    `review_interval_days`: if a knowledge point is in this state, how many days
    until the system should schedule it for review.
    `decay_interval_days`: if this many days pass without a review, the state decays
    by one level (never below REVIEWED).
    `advance_required`: how many consecutive successful exposures to advance.
    """
    #                           NEW  REV.  FAM.  PRAC.  PROF.  MASTERED
    review_interval_days:  tuple = (1,   2,    5,    12,    25,     60)
    decay_interval_days:   tuple = (1,   3,    7,    14,    30,     90)
    advance_required:      tuple = (0,   2,    2,    3,     4,      0)   # 0 = terminal, no further advance


DEFAULT_CONFIG = KnowledgeMemoryConfig()


@dataclass
class KnowledgeMemoryDecision:
    """Output of a knowledge point update — what the system should do next."""
    knowledge_id: str
    state: KnowledgeState
    status_label: str
    consecutive_successes: int
    review_interval_days: int
    next_review_date: str                  # ISO date
    last_reviewed_at: str                  # ISO datetime
    days_until_overdue: int                # positive = still fresh, negative = overdue
    decay_risk: str                        # "none" | "low" | "medium" | "high" | "overdue"
    reasoning: str


@dataclass
class KnowledgeFeedbackInput:
    """What the system knows about a review exposure."""
    knowledge_id: str
    subject: str
    heading: str
    trigger: str
    source_refs: list[str]
    # From the review completion context
    outcome: str = "reviewed"              # "reviewed" | "struggled" | "forgot"
    confidence_after: int = 2              # 0-4
    time_spent_seconds: int = 60


class KnowledgeMemoryEngine:
    """Drives the knowledge point lifecycle with Ebbingaus-informed state transitions."""

    def __init__(self, config: KnowledgeMemoryConfig | None = None):
        self.config = config or DEFAULT_CONFIG

    # ── Phase 1: State computation after review ──────────────────────────

    def compute_next_state(
        self,
        current_state: KnowledgeState,
        consecutive_successes: int,
        outcome: str,
        confidence_after: int,
    ) -> tuple[KnowledgeState, int, str]:
        """Determine the next state after a review exposure.

        Returns (new_state, new_consecutive_successes, reasoning).
        """
        is_success = outcome == "reviewed" and confidence_after >= 2

        if outcome == "forgot":
            # Forgot = decay one state (never below REVIEWED)
            new_state = KnowledgeState(max(int(current_state) - 1, int(KnowledgeState.REVIEWED)))
            new_consecutive = 0
            reasoning = f"Forgot outcome → decay from {current_state.to_status_str()} to {new_state.to_status_str()}"
            return new_state, new_consecutive, reasoning

        if outcome == "struggled":
            # Struggled = no advance, reset consecutive counter if below threshold
            new_consecutive = 0 if consecutive_successes < 2 else max(0, consecutive_successes - 1)
            reasoning = f"Struggled → no advance, consecutive={new_consecutive}"
            return current_state, new_consecutive, reasoning

        # "reviewed" outcome
        if current_state == KnowledgeState.MASTERED:
            # Terminal state — stays mastered
            new_consecutive = consecutive_successes + 1
            reasoning = "Mastered state maintained"
            return current_state, min(new_consecutive, 99), reasoning

        if current_state == KnowledgeState.NEW:
            # First review: always advance from New to Reviewed
            reasoning = "First review → advance to Reviewed once"
            return KnowledgeState.REVIEWED, 1, reasoning

        # For all intermediate states: check if we've met the advance threshold
        threshold = self.config.advance_required[int(current_state)]
        new_consecutive = consecutive_successes + 1 if is_success else max(0, consecutive_successes - 1)

        if is_success and new_consecutive >= threshold:
            next_state_value = min(int(current_state) + 1, int(KnowledgeState.MASTERED))
            new_state = KnowledgeState(next_state_value)
            reasoning = (
                f"{new_consecutive} consecutive successes ≥ threshold {threshold} "
                f"→ advance from {current_state.to_status_str()} to {new_state.to_status_str()}"
            )
            return new_state, new_consecutive, reasoning

        reasoning = (
            f"{new_consecutive} consecutive successes < threshold {threshold} "
            f"→ stay at {current_state.to_status_str()}"
        )
        return current_state, new_consecutive, reasoning

    # ── Phase 2: Interval and decay calculation ─────────────────────────

    def compute_review_interval(
        self,
        state: KnowledgeState,
        exam_date: str = "",
    ) -> tuple[int, str]:
        """How many days until this knowledge point should be re-reviewed."""
        base_days = self.config.review_interval_days[int(state)]
        reasoning = f"State={state.to_status_str()}, base_interval={base_days}d"
        return base_days, reasoning

    def compute_decay_status(
        self,
        state: KnowledgeState,
        last_reviewed_at_str: str,
        today: date | None = None,
    ) -> tuple[int, str]:
        """How many days until the state decays (or how many days overdue).

        Returns (remaining_days, risk_label). Negative remaining = overdue.
        """
        if not last_reviewed_at_str or state == KnowledgeState.NEW:
            return 0, "none"

        today = today or date.today()
        try:
            last = date.fromisoformat(last_reviewed_at_str[:10])
        except (ValueError, TypeError):
            return 0, "unknown"

        max_interval = self.config.decay_interval_days[int(state)]
        elapsed = (today - last).days
        remaining = max_interval - elapsed

        if remaining <= 0:
            return remaining, "overdue"
        elif remaining <= max_interval * 0.25:
            return remaining, "high"
        elif remaining <= max_interval * 0.5:
            return remaining, "medium"
        elif remaining <= max_interval * 0.75:
            return remaining, "low"
        else:
            return remaining, "none"

    def should_decay(
        self,
        state: KnowledgeState,
        last_reviewed_at_str: str,
        today: date | None = None,
    ) -> bool:
        """Check if a knowledge point should decay one state due to elapsed time."""
        if state <= KnowledgeState.NEW or state > KnowledgeState.MASTERED:
            return False
        if not last_reviewed_at_str:
            return False

        today = today or date.today()
        try:
            last = date.fromisoformat(last_reviewed_at_str[:10])
        except (ValueError, TypeError):
            return False

        max_interval = self.config.decay_interval_days[int(state)]
        return (today - last).days > max_interval

    # ── Phase 3: Full update (called after review completion) ────────────

    def update_knowledge_point(
        self,
        current: dict[str, Any] | None,
        feedback: KnowledgeFeedbackInput,
        exam_date: str = "",
        today: date | None = None,
    ) -> tuple[dict[str, Any], KnowledgeMemoryDecision]:
        """Full update: state → interval → decay → decision.

        `current` is the existing overlay entry (or None if first time).
        Returns (updated_overlay_entry, decision).
        """
        today = today or date.today()
        occurred_at = datetime.now().astimezone().isoformat()

        # Parse current state
        if current:
            current_state = KnowledgeState.from_str(current.get("status", ""))
            consecutive_successes = int(current.get("consecutive_successes", "0") or "0")
        else:
            current_state = KnowledgeState.NEW
            consecutive_successes = 0

        # Phase 1: Compute next state from outcome
        new_state, new_consecutive, state_reasoning = self.compute_next_state(
            current_state, consecutive_successes,
            feedback.outcome, feedback.confidence_after,
        )

        # Phase 2: Compute interval
        interval_days, interval_reasoning = self.compute_review_interval(new_state, exam_date)
        next_review = (today + timedelta(days=interval_days)).isoformat()

        # Phase 3: Decay status
        remaining_days, decay_risk = self.compute_decay_status(
            new_state, occurred_at, today,
        )

        # Phase 1b: Apply decay if overdue (from existing state before this review)
        if self.should_decay(current_state, current.get("last_reviewed_at", "") if current else "", today):
            # The existing entry was overdue — state would have decayed before this review
            # We apply this as an adjustment: if the old state was higher than REVIEWED,
            # it would have decayed. Since the user _did_ review it today, we still advance
            # but note it in reasoning.
            state_reasoning += " (previous state was overdue — decay would have applied)"

        # Build overlay entry
        entry = {
            **(current or {}),
            "knowledge_id": feedback.knowledge_id,
            "subject": feedback.subject,
            "heading": feedback.heading,
            "trigger": feedback.trigger,
            "source_refs": feedback.source_refs,
            "status": new_state.to_status_str(),
            "state_value": int(new_state),
            "consecutive_successes": new_consecutive,
            "reviewed_at": occurred_at,
            "review_interval_days": interval_days,
            "next_review_at": next_review,
            "last_reviewed_at": occurred_at,
            "decay_risk": decay_risk,
        }

        decision = KnowledgeMemoryDecision(
            knowledge_id=feedback.knowledge_id,
            state=new_state,
            status_label=new_state.to_status_str(),
            consecutive_successes=new_consecutive,
            review_interval_days=interval_days,
            next_review_date=next_review,
            last_reviewed_at=occurred_at,
            days_until_overdue=remaining_days,
            decay_risk=decay_risk,
            reasoning=f"{state_reasoning}; {interval_reasoning}",
        )

        return entry, decision

    # ── Phase 4: Bulk update for a full review (used by daily review) ────

    def update_review_batch(
        self,
        existing_overlay: dict[str, Any],
        knowledge_points: list[dict[str, Any]],
        exam_date: str = "",
    ) -> tuple[dict[str, Any], list[KnowledgeMemoryDecision]]:
        """Process all knowledge points from a completed daily review.

        Returns (updated_overlay dict, list of decisions).
        """
        overlay = dict(existing_overlay)
        overlay.setdefault("schema_version", 1)
        kp_map = overlay.setdefault("knowledge_points", {})

        decisions: list[KnowledgeMemoryDecision] = []

        for point in knowledge_points:
            kid = point.get("knowledge_id", "")
            if not kid:
                continue

            feedback = KnowledgeFeedbackInput(
                knowledge_id=kid,
                subject=point.get("subject", ""),
                heading=point.get("heading", ""),
                trigger=point.get("trigger", ""),
                source_refs=point.get("source_refs", []),
                outcome="reviewed",
                confidence_after=2,  # default moderate for bulk completion
            )

            current = kp_map.get(kid)
            entry, decision = self.update_knowledge_point(current, feedback, exam_date)
            kp_map[kid] = entry
            decisions.append(decision)

        return overlay, decisions

    # ── Phase 5: Decay sweep (run periodically to detect overdue items) ──

    def decay_sweep(
        self,
        overlay: dict[str, Any],
        today: date | None = None,
    ) -> tuple[dict[str, Any], list[str]]:
        """Scan all knowledge points and decay any that are overdue.

        Returns (updated_overlay, list of decayed knowledge_ids).
        """
        today = today or date.today()
        overlay = dict(overlay)
        kp_map = overlay.get("knowledge_points", {})
        decayed: list[str] = []
        had_changes = False

        for kid, entry in kp_map.items():
            current_state = KnowledgeState.from_str(entry.get("status", ""))
            if current_state <= KnowledgeState.REVIEWED:
                continue  # REVIEWED is the minimum — don't decay further

            if not self.should_decay(current_state, entry.get("last_reviewed_at", ""), today):
                continue

            # Decay one state
            new_state_value = max(int(current_state) - 1, int(KnowledgeState.REVIEWED))
            new_state = KnowledgeState(new_state_value)
            entry["status"] = new_state.to_status_str()
            entry["state_value"] = int(new_state)
            entry["decay_risk"] = "overdue"
            decayed.append(kid)
            had_changes = True

        if had_changes:
            overlay["knowledge_points"] = kp_map

        return overlay, decayed

    # ── Phase 6: Card outcome feedback ─────────────────────────────────

    def apply_card_outcome(
        self,
        overlay_entry: dict[str, Any] | None,
        card_outcome: str,           # "recalled" | "struggled" | "forgot"
        confidence_after: int,
        card_topic: str,
        card_los: str,
        knowledge_id: str,
    ) -> tuple[dict[str, Any], KnowledgeMemoryDecision]:
        """Feed card-level review outcome back to knowledge point state.

        Maps card outcomes to the knowledge-memory vocabulary:
          "recalled"  → outcome="reviewed" (successful recall)
          "struggled" → outcome="struggled"
          "forgot"    → outcome="forgot"
        """
        outcome_map = {
            "recalled": "reviewed",
            "struggled": "struggled",
            "forgot": "forgot",
        }

        feedback = KnowledgeFeedbackInput(
            knowledge_id=knowledge_id,
            subject=card_topic,
            heading=card_los,
            trigger="",
            source_refs=[],
            outcome=outcome_map.get(card_outcome, "reviewed"),
            confidence_after=confidence_after,
        )

        return self.update_knowledge_point(overlay_entry, feedback)


# ── Convenience helpers for external use ─────────────────────────────────

def load_knowledge_overlay(repo_root_path) -> dict[str, Any]:
    """Load the knowledge-status.json overlay from a repository."""
    from pathlib import Path
    path = Path(repo_root_path) / ".system" / "memory" / "review" / "knowledge-status.json"
    if path.exists():
        import json
        return json.loads(path.read_text(encoding="utf-8"))
    return {"schema_version": 1, "knowledge_points": {}}


def save_knowledge_overlay(repo_root_path, overlay: dict[str, Any]) -> None:
    """Save the knowledge-status.json overlay to a repository."""
    from pathlib import Path
    import json
    path = Path(repo_root_path) / ".system" / "memory" / "review" / "knowledge-status.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8")
