"""Tests for CRITICAL/HIGH EXAMOS audit fixes.

Covers:
  - C3/C4: Wildcard imports eliminated, write_todo not shadowed
  - H5:   Screenshot filename sanitization (path traversal)
  - C1:   PedagogyPolicy replaced by stateful AdaptivePedagogy
  - C2:   DistractorAnalyzer.classify_distractor with real logic
"""

from __future__ import annotations

from pathlib import Path


# ── C3/C4: No wildcard imports; write_todo resolves to todo version ──────────

def test_no_wildcard_imports() -> None:
    """__init__.py must NOT use `from ... import *`."""
    init_path = (
        Path(__file__).resolve().parents[1]
        / "app" / "workflows" / "__init__.py"
    )
    source = init_path.read_text(encoding="utf-8")
    # Block any line that says "from ... import *" (with optional trailing comment)
    lines = source.splitlines()
    offending = [i + 1 for i, ln in enumerate(lines) if "import *" in ln and not ln.strip().startswith("#")]
    assert not offending, f"Wildcard imports still present at lines {offending}"


def test_write_todo_is_todo_version(tmp_path: Path) -> None:
    """write_todo must be importable and be the todo.py (V2 reducer) version."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from app.storage import Repository
    from app.workflows import write_todo
    repo = Repository(tmp_path)
    payload = {
        "date": "2026-06-02",
        "tasks": [{"text": "Test task", "deadline": "12:00"}],
    }
    result = write_todo(repo, payload)
    assert result is not None
    assert result.exists()
    assert "Test task" in result.read_text(encoding="utf-8")


def test_core_archive_todo_is_exported(tmp_path: Path) -> None:
    """core_archive_todo is the aliased archive_today_todo from core.py."""
    from app.workflows import core_archive_todo
    from app.storage import Repository
    repo = Repository(tmp_path)
    todo_path = repo.obsidian_root / "today_todo.md"
    todo_path.parent.mkdir(parents=True, exist_ok=True)
    todo_path.write_text("# Old content", encoding="utf-8")
    result = core_archive_todo(repo, "2026-06-02")
    # Should have created an archive copy
    assert result is not None
    assert result.exists()
    assert "Old content" in result.read_text(encoding="utf-8")


def test_as_source_refs_still_exported() -> None:
    """Private _as_source_refs remains available for tests."""
    from app.workflows import _as_source_refs
    assert _as_source_refs(("one", "", "two")) == ["one", "two"]


def test_all_core_exports_available() -> None:
    """Key symbols from core.py are still re-exported via __init__.py."""
    from app.workflows import (
        record_question_attempt,
        daily_review_pack,
        complete_daily_review,
        mine_patterns,
        moc_gap_review,
        pre_mock_brief,
        post_mock_retro,
        record_event,
        record_progress,
        refresh_learning_outputs,
        mark_card_reviewed,
        batch_import_events,
        batch_import_attempts,
        weekly_focus_recommendation,
        load_payload,
        record_fix_rule_feedback,
        load_progress_events,
        collect_due_card_items,
        collect_pattern_items,
        collect_recent_low_confidence_items,
        merge_review_sources,
        interleave_review_items,
        load_daily_review_snapshot,
        add_review_item,
        clean_display_text,
        extract_markdown_section,
        parse_date,
        parse_frontmatter,
        default_fix_rule,
        next_drill_for,
    )
    # All are callable (or at least not None)
    assert record_question_attempt is not None


# ── H5: Screenshot path traversal prevention ─────────────────────────────────

def test_screenshot_filename_sanitization(tmp_path: Path) -> None:
    """Screenshot filename must strip directory components (path traversal)."""
    # Simulate the logic from attempts.py upload_screenshot endpoint
    from datetime import datetime
    from pathlib import Path as PathLib

    malicious = "../../../etc/passwd"
    safe_name = PathLib(malicious).name  # -> "passwd"
    assert safe_name == "passwd", f"Expected 'passwd', got {safe_name!r}"

    safe_name2 = PathLib("..\\..\\windows\\system32\\config").name
    assert ".." not in safe_name2
    assert "\\" not in safe_name2

    # Verify the full filename pattern used in the fix
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}-{safe_name}"
    assert "../" not in filename
    assert filename.endswith("-passwd")


def test_screenshot_filename_keeps_extension() -> None:
    """Sanitized filename should preserve the original file extension."""
    from pathlib import Path as PathLib
    filename = PathLib("../../attack.png").name
    assert filename == "attack.png"


# ── C1: AdaptivePedagogy (replaces PedagogyPolicy) ──────────────────────────

def test_adaptive_pedagogy_low_energy_recall() -> None:
    """Energy <= 1 always returns 'recall' strategy."""
    from study_science.pedagogy import AdaptivePedagogy
    ped = AdaptivePedagogy()
    d = ped.select(topic="Equity", los="EQ.DDM", energy_level=0, confidence=4)
    assert d.strategy == "recall"
    d2 = ped.select(topic="Equity", energy_level=1)
    assert d2.strategy == "recall"


def test_adaptive_pedagogy_discrimination() -> None:
    """concept_confusion + high confidence -> discrimination."""
    from study_science.pedagogy import AdaptivePedagogy
    ped = AdaptivePedagogy()
    d = ped.select(topic="FI", error_type="concept_confusion", confidence=3, energy_level=3)
    assert d.strategy == "discrimination"


def test_adaptive_pedagogy_worked_example_then_application() -> None:
    """formula_misuse with low consecutive_correct -> worked_example, then application."""
    from study_science.pedagogy import AdaptivePedagogy
    ped = AdaptivePedagogy()
    # Fewer than 2 correct in a row -> worked_example
    d = ped.select(topic="QM", error_type="formula_misuse", consecutive_correct=0, energy_level=3)
    assert d.strategy == "worked_example"
    # After >= 2 correct -> application
    d2 = ped.select(topic="QM", error_type="formula_misuse", consecutive_correct=2, energy_level=3)
    assert d2.strategy == "application"


def test_adaptive_pedagogy_interleaving() -> None:
    """3+ consecutive correct -> interleaving."""
    from study_science.pedagogy import AdaptivePedagogy
    ped = AdaptivePedagogy()
    d = ped.select(topic="PM", consecutive_correct=3, energy_level=3)
    assert d.strategy == "interleaving"


def test_adaptive_pedagogy_default_recall() -> None:
    """Default/fallback strategy is 'recall'."""
    from study_science.pedagogy import AdaptivePedagogy
    ped = AdaptivePedagogy()
    d = ped.select(topic="PM", energy_level=2)
    assert d.strategy == "recall"


def test_adaptive_pedagogy_record_outcome() -> None:
    """record_outcome tracks consecutive_correct correctly."""
    from study_science.pedagogy import AdaptivePedagogy
    ped = AdaptivePedagogy()
    ped.record_outcome("FI:DCF", True)
    assert ped._history["FI:DCF"]["consecutive_correct"] == 1
    ped.record_outcome("FI:DCF", True)
    assert ped._history["FI:DCF"]["consecutive_correct"] == 2
    ped.record_outcome("FI:DCF", False)
    assert ped._history["FI:DCF"]["consecutive_correct"] == 0
    assert ped._history["FI:DCF"]["total"] == 3
    assert ped._history["FI:DCF"]["correct"] == 2


def test_pedagogy_strategies_dict_keys() -> None:
    """All expected strategy keys exist."""
    from study_science.pedagogy import PEDAGOGY_STRATEGIES
    expected = {"recall", "discrimination", "worked_example", "application", "interleaving"}
    assert set(PEDAGOGY_STRATEGIES) == expected
    for k in expected:
        assert PEDAGOGY_STRATEGIES[k].strategy == k


# ── C2: DistractorAnalyzer.classify_distractor ──────────────────────────────

def test_classify_distractor_calculation_sign_error() -> None:
    """Sign error detection: correct=5, selected=-5."""
    from study_science.distractor import classify_distractor
    result = classify_distractor(5, -5, "calculation", "QM")
    assert result["distractor_type"] == "sign_error"
    assert result["confidence"] >= 0.8


def test_classify_distractor_calculation_unit_error() -> None:
    """Unit error: selected is 2x correct."""
    from study_science.distractor import classify_distractor
    result = classify_distractor(50, 100, "calculation", "FI")
    assert result["distractor_type"] == "unit_error"
    assert result["confidence"] >= 0.7


def test_classify_distractor_calculation_unit_error_half() -> None:
    """Unit error: selected is 0.5x correct."""
    from study_science.distractor import classify_distractor
    result = classify_distractor(200, 100, "calculation", "FI")
    assert result["distractor_type"] == "unit_error"


def test_classify_distractor_concept_inverse() -> None:
    """Inverse relationship detection for concept questions."""
    from study_science.distractor import classify_distractor
    result = classify_distractor("increase reserves", "decrease reserves", "concept", "Econ")
    assert result["distractor_type"] == "inverse_relationship"
    assert result["confidence"] >= 0.8


def test_classify_distractor_concept_call_put() -> None:
    """Call/put inverse relationship."""
    from study_science.distractor import classify_distractor
    result = classify_distractor("call option", "put option", "concept", "Derivatives")
    assert result["distractor_type"] == "inverse_relationship"


def test_classify_distractor_concept_asset_liability() -> None:
    """Asset/liability inverse relationship."""
    from study_science.distractor import classify_distractor
    result = classify_distractor("asset backed", "liability backed", "concept", "FI")
    assert result["distractor_type"] == "inverse_relationship"


def test_classify_distractor_fallback() -> None:
    """Unrecognized patterns fall back to 'concept_pair'."""
    from study_science.distractor import classify_distractor
    result = classify_distractor("something", "something else", "concept", "PM")
    assert result["distractor_type"] == "concept_pair"
    assert result["topic"] == "PM"
    assert result["confidence"] == 0.5


def test_classify_distractor_non_numeric_calculation() -> None:
    """Calculation type with non-numeric values should not crash."""
    from study_science.distractor import classify_distractor
    result = classify_distractor("A", "B", "calculation", "QM")
    assert result["distractor_type"] == "concept_pair"
    assert result["confidence"] == 0.5


def test_distractor_analyzer_record_and_patterns(tmp_path: Path) -> None:
    """DistractorAnalyzer.record_attempt and get_patterns work."""
    from study_science.distractor import DistractorAnalyzer
    da = DistractorAnalyzer()
    entry = da.record_attempt("item-1", True, "sign_error", "QM")
    assert entry["item_id"] == "item-1"
    assert entry["correct"] is True
    assert len(da.get_patterns("item-1")) == 1
    assert len(da.get_patterns()) == 1


def test_distractor_analyzer_most_common(tmp_path: Path) -> None:
    """most_common_distractor returns the top distractor type."""
    from study_science.distractor import DistractorAnalyzer
    da = DistractorAnalyzer()
    da.record_attempt("i1", False, "sign_error", "QM")
    da.record_attempt("i2", False, "sign_error", "QM")
    da.record_attempt("i3", False, "unit_error", "QM")
    assert da.most_common_distractor("QM") == "sign_error"


def test_distractor_analyzer_most_common_empty() -> None:
    """most_common_distractor returns '' when no data."""
    from study_science.distractor import DistractorAnalyzer
    da = DistractorAnalyzer()
    assert da.most_common_distractor("QM") == ""
