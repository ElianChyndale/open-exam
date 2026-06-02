"""Mock exam session manager — timed 90-question CFA-style exams."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from app.cfa_storage import CfaRepository
from app.cfa_workflows import EXAM_WEIGHTS
from app.models import stable_id


PASS_THRESHOLD = 0.70
DEFAULT_QUESTION_COUNT = 90
DEFAULT_TIME_LIMIT_MINUTES = 135


def _now() -> str:
    return datetime.now(UTC).isoformat()


class MockExamManager:
    """Manages a single mock exam session with timing, scoring, and per-subject breakdown."""

    def __init__(self, cfa_repo: CfaRepository) -> None:
        self._repo = cfa_repo
        self._session: dict[str, Any] | None = None

    def start_session(self, *, question_count: int = DEFAULT_QUESTION_COUNT, time_limit_minutes: int = DEFAULT_TIME_LIMIT_MINUTES) -> dict[str, Any]:
        session_id = stable_id("mock-exam", _now())
        # Distribute questions by exam weight
        subject_distribution: dict[str, int] = {}
        remaining = question_count
        subjects = sorted(EXAM_WEIGHTS.items(), key=lambda x: -x[1])
        for i, (subject, weight) in enumerate(subjects):
            count = max(1, round(question_count * weight))
            if i == len(subjects) - 1:
                count = remaining  # last subject gets remainder
            subject_distribution[subject] = count
            remaining -= count

        self._session = {
            "session_id": session_id,
            "status": "in_progress",
            "question_count": question_count,
            "time_limit_minutes": time_limit_minutes,
            "subject_distribution": subject_distribution,
            "answers": [],
            "started_at": _now(),
            "completed_at": "",
            "score": 0.0,
            "pass": False,
            "subject_scores": {},
        }
        return self._session

    def record_answer(self, question_id: str, subject: str, correct: bool, time_spent_seconds: float = 0.0) -> dict[str, Any]:
        if self._session is None or self._session["status"] != "in_progress":
            raise ValueError("No active mock exam session")
        self._session["answers"].append({
            "question_id": question_id,
            "subject": subject,
            "correct": correct,
            "time_spent_seconds": time_spent_seconds,
        })
        return self._session

    def complete_session(self) -> dict[str, Any]:
        if self._session is None or self._session["status"] != "in_progress":
            raise ValueError("No active mock exam session")
        answers = self._session["answers"]
        if not answers:
            raise ValueError("Cannot complete a session with no answers")

        total = len(answers)
        correct = sum(1 for a in answers if a["correct"])
        score = correct / total

        # Per-subject scores
        subject_correct: dict[str, int] = {}
        subject_total: dict[str, int] = {}
        for a in answers:
            s = a["subject"]
            subject_total[s] = subject_total.get(s, 0) + 1
            if a["correct"]:
                subject_correct[s] = subject_correct.get(s, 0) + 1
        subject_scores = {
            s: round(subject_correct.get(s, 0) / max(subject_total.get(s, 1), 1), 3)
            for s in set(list(subject_correct.keys()) + list(subject_total.keys()))
        }

        # Timing analysis
        total_time = sum(a.get("time_spent_seconds", 0) for a in answers)
        avg_time_per_q = round(total_time / max(total, 1), 1)

        self._session["status"] = "completed"
        self._session["completed_at"] = _now()
        self._session["score"] = round(score, 3)
        self._session["pass"] = score >= PASS_THRESHOLD
        self._session["subject_scores"] = subject_scores
        self._session["timing"] = {
            "total_seconds": total_time,
            "avg_seconds_per_question": avg_time_per_q,
            "under_limit": total_time <= self._session["time_limit_minutes"] * 60,
        }
        self._session.pop("answers")  # compact for storage

        self._repo.append("cfa.mock.completed", self._session)
        return self._session

    @staticmethod
    def session_summary(session: dict[str, Any]) -> dict[str, Any]:
        passing_subjects = sum(1 for s in session.get("subject_scores", {}).values() if s >= PASS_THRESHOLD)
        total_subjects = len(session.get("subject_scores", {}))
        return {
            "session_id": session["session_id"],
            "score": session["score"],
            "pass": session["pass"],
            "passing_subjects": f"{passing_subjects}/{total_subjects}",
            "timing": session.get("timing", {}),
            "subject_scores": session.get("subject_scores", {}),
        }
