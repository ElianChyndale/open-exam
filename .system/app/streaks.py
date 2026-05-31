"""Learning streak tracking.

Tracks consecutive days of study activity and weekly goal completion.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


def load_progress_dates(progress_path: Path) -> list[str]:
    """Load all dates where study activity occurred from progress-events.jsonl."""
    if not progress_path.exists():
        return []
    dates: set[str] = set()
    for line in progress_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        import json
        try:
            event = json.loads(line)
            created = event.get("created_at", "") or event.get("date", "")
            if created:
                dates.add(created[:10])
        except json.JSONDecodeError:
            continue
    return sorted(dates)


def compute_streak(active_dates: list[str], until: date | None = None) -> tuple[int, bool]:
    """Compute current streak length and whether active today.

    Args:
        active_dates: Sorted list of ISO date strings with activity.
        until: Date to compute streak up to (defaults to today).

    Returns:
        (streak_length, active_today) tuple.
    """
    target = until or date.today()
    target_str = target.isoformat()

    if not active_dates or active_dates[-1] < target_str:
        return 0, False

    active_today = active_dates[-1] == target_str
    streak = 0
    check = target if active_today else target - timedelta(days=1)

    while check.isoformat() in active_dates:
        streak += 1
        check -= timedelta(days=1)

    return streak, active_today


def compute_weekly_goal_progress(progress_events: list[dict], week_start: date | None = None) -> dict:
    """Compute weekly goal progress.

    Returns count of completed review packs this week.
    """
    if week_start is None:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())

    week_end = week_start + timedelta(days=6)
    week_start_str = week_start.isoformat()
    week_end_str = week_end.isoformat()

    completed = 0
    for event in progress_events:
        if event.get("record_type") != "daily_review_completed":
            continue
        if event.get("status") not in {"completed", "done"}:
            continue
        event_date = str(event.get("date") or event.get("created_at", "")[:10])
        if week_start_str <= event_date <= week_end_str:
            completed += 1

    return {
        "week_start": week_start_str,
        "week_end": week_end_str,
        "completed_reviews": completed,
        "goal": 5,
        "progress_pct": min(100, int(completed / 5 * 100)),
    }
