from __future__ import annotations

import json
import random
from copy import deepcopy
from datetime import datetime
from pathlib import Path


def _wrong_payload(**overrides) -> dict:
    payload = {
        "topic": "Fixed Income",
        "los": "FI.Duration",
        "prompt_or_question": "Estimate a bond price change.",
        "wrong_choice_or_output": "Ignored convexity.",
        "correct_resolution": "Use duration and convexity.",
        "error_type": "formula_misuse",
        "confidence": 1,
        "time_spent": 60,
        "evidence_refs": ["audit-test"],
        "created_at": "2026-05-20T10:00:00+00:00",
    }
    payload.update(overrides)
    return payload


def test_attempt_envelope_fields_cannot_be_overridden_by_payload(tmp_path: Path) -> None:
    from app.storage import Repository
    from app.workflows import record_question_attempt

    repo = Repository(tmp_path)
    result = record_question_attempt(
        repo,
        _wrong_payload(
            is_correct=True,
            event_id="forged-event",
            event_type="forged.type",
            learner_id="forged-learner",
            occurred_at="1900-01-01T00:00:00+00:00",
            source_refs=["forged-source"],
            schema_version=999,
        ),
    )

    attempt = repo.load_attempt_records()[0]
    assert attempt["event_id"] == result["attempt_id"]
    assert attempt["event_type"] == "attempt.recorded"
    assert attempt["learner_id"] == "local"
    assert attempt["occurred_at"] == "2026-05-20T10:00:00+00:00"
    assert attempt["source_refs"] == ["audit-test"]
    assert attempt["schema_version"] == 1
    assert attempt["mistake_event_id"] == ""
    assert result["event"] is None


def test_add_review_item_does_not_mutate_callers_candidate() -> None:
    from app.workflows import add_review_item

    candidate = {"priority": 10, "reasons": ("first",), "card_ids": ["card-1"]}
    items: dict[str, dict] = {}

    add_review_item(items, "key", candidate)
    items["key"]["reasons"].append("second")
    items["key"]["card_ids"].append("card-2")

    assert candidate == {"priority": 10, "reasons": ("first",), "card_ids": ["card-1"]}


def test_frontmatter_update_inserts_before_closing_delimiter_without_terminal_newline() -> None:
    from app.storage import _set_frontmatter_value

    text = "---\ncard_id: card-1\n---"

    updated = _set_frontmatter_value(text, "review_status", "Reviewed once")

    assert updated == "---\ncard_id: card-1\nreview_status: Reviewed once\n---"


def test_due_card_priority_preserves_explicit_zero(tmp_path: Path) -> None:
    from app.storage import Repository
    from app.workflows import collect_due_card_items

    repo = Repository(tmp_path)
    card_path = repo.memory_root / "question-errors" / "card-zero.md"
    card_path.write_text(
        "\n".join(
            [
                "---",
                "card_id: card-zero",
                "topic: Equity",
                "los: EQ.1",
                "root_cause: concept_confusion",
                "review_due_at: 2026-06-01",
                "spacing_priority: 0",
                "---",
            ]
        ),
        encoding="utf-8",
    )

    items = collect_due_card_items(repo, datetime.fromisoformat("2026-06-01").date())

    assert next(iter(items.values()))["priority"] == 8


def test_source_ref_normalization_supports_tuples() -> None:
    from app.workflows import _as_source_refs

    assert _as_source_refs(("one", "", "two")) == ["one", "two"]


def test_sync_preview_counts_progress_stream_and_incoming_duplicates(tmp_path: Path) -> None:
    from app.storage import Repository
    from app.sync_service import preview_import

    repo = Repository(tmp_path)
    repo.append_jsonl_event("review", {"event_id": "review-1"})
    progress_path = repo.memory_root / "progress" / "progress-events.jsonl"
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    progress_path.write_text('{"record_type": "done"}\n', encoding="utf-8")

    preview = preview_import(
        repo,
        {
            "schema_version": 1,
            "events": [],
            "progress_events": [{"record_type": "done"}, {"record_type": "new"}, {"record_type": "new"}],
            "streams": {
                "review": [{"event_id": "review-1"}, {"event_id": "review-2"}, {"event_id": "review-2"}],
            },
        },
    )

    assert preview["would_import"] == {"events": 0, "progress": 1, "stream_events": 1}
    assert preview["duplicates"] == 4


def test_knowledge_memory_update_preserves_overlay_metadata() -> None:
    from study_science.knowledge_memory import KnowledgeFeedbackInput, KnowledgeMemoryEngine

    current = {
        "status": "Reviewed once",
        "consecutive_successes": 1,
        "linked_card_ids": ["card-1"],
        "custom_note": "keep me",
    }
    feedback = KnowledgeFeedbackInput(
        knowledge_id="knowledge-1",
        subject="Equity",
        heading="DDM",
        trigger="Dividend growth",
        source_refs=["moc"],
    )

    entry, _ = KnowledgeMemoryEngine().update_knowledge_point(current, feedback)

    assert entry["linked_card_ids"] == ["card-1"]
    assert entry["custom_note"] == "keep me"


def test_calibration_warning_timestamp_is_timezone_aware(tmp_path: Path) -> None:
    from app.storage import Repository
    from app.workflows import record_question_attempt

    repo = Repository(tmp_path)
    record_question_attempt(repo, _wrong_payload(confidence=4))
    warning_path = repo.memory_root / "strategy" / "calibration-warnings.jsonl"
    warning = json.loads(warning_path.read_text(encoding="utf-8").splitlines()[0])

    assert datetime.fromisoformat(warning["created_at"]).tzinfo is not None


def test_print_card_date_validation_has_actionable_message(tmp_path: Path) -> None:
    import pytest

    from app.card_printer import collect_due_print_cards
    from app.storage import Repository

    with pytest.raises(ValueError, match="review_date must use YYYY-MM-DD"):
        collect_due_print_cards(Repository(tmp_path), review_date="not-a-date")


def test_interleaving_builder_is_repeatable_for_the_same_inputs() -> None:
    from study_science.interleaving import InterleavingBuilder, InterleavingConfig

    weak = [{"topic": f"weak-{index}", "priority": 90} for index in range(8)]
    old = [{"topic": f"old-{index}", "priority": 60} for index in range(4)]
    maintenance = [{"topic": f"maintenance-{index}", "priority": 20} for index in range(4)]
    config = InterleavingConfig(max_items=10)

    random.seed(1)
    first = InterleavingBuilder.build(deepcopy(weak), deepcopy(old), deepcopy(maintenance), config)
    random.seed(2)
    second = InterleavingBuilder.build(deepcopy(weak), deepcopy(old), deepcopy(maintenance), config)

    assert first.items == second.items
