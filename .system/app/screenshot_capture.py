from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from app.models import stable_id
from app.storage import Repository


SCREENSHOT_DRAFT_DIR = Path(".system/memory/capture/screenshot-drafts")


@dataclass(slots=True)
class ScreenshotExtractionDraft:
    draft_id: str
    created_at: str
    status: str
    evidence_path: str
    draft_path: str
    topic: str
    los: str
    source_type: str
    uncertain_fields: list[str]
    payload: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def create_screenshot_extraction_draft(
    repo: Repository,
    *,
    evidence_path: str,
    topic: str,
    los: str,
) -> ScreenshotExtractionDraft:
    now = datetime.now(UTC)
    draft_id = stable_id("screenshot-draft", evidence_path, now.isoformat())
    uncertain_fields = [
        "prompt_or_question",
        "wrong_choice_or_output",
        "correct_resolution",
        "choices",
        "question_source",
        "moc_target",
    ]
    if not topic.strip():
        uncertain_fields.append("topic")
    if not los.strip():
        uncertain_fields.append("los")

    payload: dict[str, object] = {
        "source_layer": "question",
        "topic": topic,
        "los": los,
        "prompt_or_question": "",
        "wrong_choice_or_output": "",
        "correct_resolution": "",
        "error_type": "concept_confusion",
        "confidence": 0,
        "time_spent": 0,
        "evidence_refs": [draft_id],
        "question_source": "",
        "source_type": "screenshot",
        "evidence_assets": [evidence_path],
        "moc_target": "",
        "question_format": "",
        "choices": [],
        "is_correct": False,
    }

    draft_rel = SCREENSHOT_DRAFT_DIR / f"{draft_id}.json"
    draft_abs = repo.root / draft_rel
    draft_abs.parent.mkdir(parents=True, exist_ok=True)

    draft = ScreenshotExtractionDraft(
        draft_id=draft_id,
        created_at=now.isoformat(),
        status="needs_extraction",
        evidence_path=evidence_path,
        draft_path=str(draft_rel).replace("\\", "/"),
        topic=topic,
        los=los,
        source_type="screenshot",
        uncertain_fields=uncertain_fields,
        payload=payload,
    )
    draft_abs.write_text(json.dumps(draft.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    repo.append_jsonl_event(
        "capture",
        {
            "event_type": "screenshot.draft.created",
            "draft_id": draft_id,
            "created_at": draft.created_at,
            "evidence_path": evidence_path,
            "draft_path": draft.draft_path,
            "topic": topic,
            "los": los,
            "uncertain_fields": uncertain_fields,
            "event_id": stable_id("capture-event", draft_id),
        },
    )
    return draft
