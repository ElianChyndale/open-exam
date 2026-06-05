from __future__ import annotations

import json
from pathlib import Path

from app.screenshot_capture import create_screenshot_extraction_draft
from app.storage import Repository


def test_create_screenshot_extraction_draft_persists_artifact_and_event(tmp_path: Path) -> None:
    repo = Repository(tmp_path)

    draft = create_screenshot_extraction_draft(
        repo,
        evidence_path="evidence/screenshots/example.png",
        topic="Fixed Income",
        los="",
    )

    draft_path = tmp_path / draft.draft_path
    assert draft.status == "needs_extraction"
    assert draft_path.exists()

    payload = json.loads(draft_path.read_text(encoding="utf-8"))
    assert payload["payload"]["evidence_assets"] == ["evidence/screenshots/example.png"]
    assert "los" in payload["uncertain_fields"]

    events = repo.load_jsonl_events("capture")
    assert events[-1]["event_type"] == "screenshot.draft.created"
    assert events[-1]["draft_id"] == draft.draft_id
