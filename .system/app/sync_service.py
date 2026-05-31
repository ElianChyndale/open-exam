"""Local sync service — export/import all study data as a portable JSON file.

This is the MVP for "ExamOS Cloud": instead of requiring a cloud backend,
users can export their entire study state to a single JSON file for backup
or transfer to another device.

Future version will add optional Supabase sync for cross-device real-time sync.
"""
from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

from app.storage import Repository


def export_all(repo: Repository) -> dict[str, Any]:
    """Export all study data as a portable dictionary.

    Includes: events, progress, streaks, calibration warnings, patterns.
    """
    events = repo.load_events()

    # Progress events
    progress_path = repo.memory_root / "progress" / "progress-events.jsonl"
    progress_events = []
    if progress_path.exists():
        for line in progress_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                progress_events.append(json.loads(line))

    # Calibration warnings
    cal_path = repo.memory_root / "strategy" / "calibration-warnings.jsonl"
    cal_warnings = []
    if cal_path.exists():
        for line in cal_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                cal_warnings.append(json.loads(line))

    # Exam settings
    exam_date = ""
    exam_date_path = repo.root / ".system" / "exam_date.txt"
    if exam_date_path.exists():
        exam_date = exam_date_path.read_text(encoding="utf-8").strip()

    active_profile = ""
    profile_path = repo.root / ".system" / "active_profile.txt"
    if profile_path.exists():
        active_profile = profile_path.read_text(encoding="utf-8").strip()

    return {
        "exported_at": datetime.now(UTC).isoformat(),
        "version": "1.0",
        "exam_date": exam_date,
        "active_profile": active_profile,
        "events": [e.as_dict() for e in events],
        "progress_events": progress_events,
        "calibration_warnings": cal_warnings,
    }


def import_all(repo: Repository, data: dict[str, Any]) -> dict[str, int]:
    """Import study data from an export dict.

    Returns counts of imported items.
    """
    from app.models import MistakeEvent
    from app.storage import MistakeCard

    counts: dict[str, int] = {"events": 0, "progress": 0}

    # Import events
    for event_dict in data.get("events", []):
        event = MistakeEvent.from_payload(event_dict)
        repo.append_event(event)
        counts["events"] += 1

    # Import progress
    progress_path = repo.memory_root / "progress" / "progress-events.jsonl"
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    for prog in data.get("progress_events", []):
        with open(progress_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(prog, ensure_ascii=False) + "\n")
        counts["progress"] += 1

    # Restore exam date
    if data.get("exam_date"):
        (repo.root / ".system" / "exam_date.txt").write_text(data["exam_date"], encoding="utf-8")

    # Restore profile
    if data.get("active_profile"):
        (repo.root / ".system" / "active_profile.txt").write_text(data["active_profile"], encoding="utf-8")

    return counts


def push_to_file(repo: Repository, output_path: str) -> Path:
    """Export all data to a JSON file."""
    path = Path(output_path)
    data = export_all(repo)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 已导出 {len(data['events'])} 条事件、{len(data['progress_events'])} 条进度")
    return path


def pull_from_file(repo: Repository, input_path: str) -> dict[str, int]:
    """Import all data from a JSON file."""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Sync file not found: {input_path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    counts = import_all(repo, data)
    print(f"✅ 已导入 {counts['events']} 条事件、{counts['progress']} 条进度")
    return counts
