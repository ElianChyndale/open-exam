from __future__ import annotations

from pathlib import Path


def _wrong_payload(**overrides) -> dict:
    payload = {
        "source_layer": "question",
        "topic": "Fixed Income",
        "los": "FI.Duration",
        "prompt_or_question": "Estimate a bond price change.",
        "wrong_choice_or_output": "Ignored convexity.",
        "correct_resolution": "Use duration and convexity.",
        "error_type": "formula_misuse",
        "confidence": 1,
        "time_spent": 60,
        "evidence_refs": ["release3-test"],
        "created_at": "2026-05-20T10:00:00+00:00",
    }
    payload.update(overrides)
    return payload


def test_sync_import_validates_schema_and_skips_duplicates(tmp_path: Path) -> None:
    from app.storage import Repository
    from app.sync_service import export_all, import_all
    from app.workflows import record_question_attempt

    source = Repository(tmp_path / "source")
    record_question_attempt(source, _wrong_payload())
    backup = export_all(source)

    target = Repository(tmp_path / "target")
    first = import_all(target, backup)
    second = import_all(target, backup)

    assert backup["schema_version"] == 1
    assert first["events"] == 1
    assert second["events"] == 0
    assert second["duplicates"] >= 1
    assert len(target.load_events()) == 1


def test_repository_rebuilds_sqlite_catalog_from_canonical_jsonl(tmp_path: Path) -> None:
    import sqlite3

    from app.storage import Repository
    from app.workflows import record_question_attempt

    repo = Repository(tmp_path)
    record_question_attempt(repo, _wrong_payload())
    repo.catalog_path.unlink()

    counts = repo.rebuild_catalog()

    assert counts == {"mistake_events": 1, "artifacts": 0}
    with sqlite3.connect(repo.catalog_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM mistake_events").fetchone()[0] == 1


def test_active_exam_profile_is_loaded_from_repository_setting(tmp_path: Path) -> None:
    from app.exam_profile import get_profile

    setting = tmp_path / ".system" / "active_profile.txt"
    setting.parent.mkdir(parents=True)
    setting.write_text("frm-p1", encoding="utf-8")

    profile = get_profile(repo_root=tmp_path, refresh=True)

    assert profile.short_name == "frm-p1"
    assert [subject["name"] for subject in profile.subjects] == [
        "Foundations of Risk Management",
        "Quantitative Analysis",
        "Financial Markets and Products",
        "Valuation and Risk Models",
    ]


def test_print_card_collection_only_returns_due_cards(tmp_path: Path) -> None:
    from app.card_printer import collect_due_print_cards
    from app.storage import Repository
    from app.workflows import record_question_attempt

    repo = Repository(tmp_path)
    record_question_attempt(repo, _wrong_payload())
    record_question_attempt(repo, _wrong_payload(los="FI.YTM", prompt_or_question="Compute YTM.", evidence_refs=["future-card"]))
    cards = sorted((repo.memory_root / "question-errors").glob("*.md"))
    future_text = cards[1].read_text(encoding="utf-8").replace("review_due_at: 2026-", "review_due_at: 2100-", 1)
    cards[1].write_text(future_text, encoding="utf-8")

    due = collect_due_print_cards(repo, review_date="2099-12-31")

    assert len(due) == 1
    assert due[0]["card_id"] == cards[0].stem
