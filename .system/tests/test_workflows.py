from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


def test_record_question_mistake_creates_event_and_card(tmp_path: Path) -> None:
    from app.cli import run_cli

    payload = {
        "source_layer": "question",
        "topic": "Ethical and Professional Standards",
        "los": "I.A",
        "prompt_or_question": "A client requests selective performance presentation.",
        "wrong_choice_or_output": "A",
        "correct_resolution": "B because selective presentation violates fair dealing.",
        "error_type": "concept_confusion",
        "confidence": 2,
        "time_spent": 110,
        "evidence_refs": ["schweser-vol1-p23"],
    }

    exit_code = run_cli(
        ["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)],
        repo_root=tmp_path,
    )

    assert exit_code == 0

    question_events = list((tmp_path / ".system" / "events" / "question").glob("*.jsonl"))
    assert question_events, "question event log should be created"
    event_record = json.loads(question_events[0].read_text(encoding="utf-8").splitlines()[0])
    assert event_record["topic"] == "Ethical and Professional Standards"
    assert event_record["source_layer"] == "question"

    cards = list((tmp_path / ".system" / "memory" / "question-errors").glob("*.md"))
    assert len(cards) == 1
    card_text = cards[0].read_text(encoding="utf-8")
    assert "root_cause: concept_confusion" in card_text
    assert "next_drill:" in card_text
    assert "correct_resolution:" in card_text


def test_record_question_mistake_preserves_screenshot_metadata(tmp_path: Path) -> None:
    from app.cli import run_cli

    payload = {
        "source_layer": "question",
        "topic": "Fixed Income",
        "los": "FI.8",
        "prompt_or_question": "Screenshot-derived bond convexity question.",
        "wrong_choice_or_output": "Selected the duration-only approximation.",
        "correct_resolution": "For a larger yield move, include convexity in the price estimate.",
        "error_type": "formula_misuse",
        "confidence": 2,
        "time_spent": 140,
        "evidence_refs": ["mock-4", "screen-001"],
        "question_source": "official_mock",
        "source_type": "screenshot",
        "evidence_assets": ["attachments/mock4-q18.png"],
        "moc_target": "CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md",
    }

    exit_code = run_cli(
        ["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)],
        repo_root=tmp_path,
    )

    assert exit_code == 0

    question_events = list((tmp_path / ".system" / "events" / "question").glob("*.jsonl"))
    event_record = json.loads(question_events[0].read_text(encoding="utf-8").splitlines()[0])
    assert event_record["question_source"] == "official_mock"
    assert event_record["source_type"] == "screenshot"
    assert event_record["evidence_assets"] == ["attachments/mock4-q18.png"]
    assert event_record["moc_target"] == "CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md"

    cards = list((tmp_path / ".system" / "memory" / "question-errors").glob("*.md"))
    card_text = cards[0].read_text(encoding="utf-8")
    assert "question_source: official_mock" in card_text
    assert "source_type: screenshot" in card_text
    assert "evidence_assets: attachments/mock4-q18.png" in card_text
    assert "moc_target: CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md" in card_text


def test_learning_block_is_classified_as_cognitive_bias(tmp_path: Path) -> None:
    from app.cli import run_cli

    payload = {
        "source_layer": "bias",
        "topic": "Quantitative Methods",
        "los": "QM.7",
        "prompt_or_question": "总是把 time value of money 的 N 和 I/Y 搞混。",
        "wrong_choice_or_output": "把期数和利率位置填反",
        "correct_resolution": "先写现金流时间轴，再代入计算器。",
        "error_type": "formula_misuse",
        "confidence": 3,
        "time_spent": 240,
        "evidence_refs": ["study-session-2026-05-21"],
    }

    exit_code = run_cli(
        ["review-session", "--payload", json.dumps(payload, ensure_ascii=False)],
        repo_root=tmp_path,
    )

    assert exit_code == 0

    bias_cards = list((tmp_path / ".system" / "memory" / "cognitive-bias").glob("*.md"))
    assert len(bias_cards) == 1
    text = bias_cards[0].read_text(encoding="utf-8")
    assert "bias_signal: formula_misuse" in text
    assert "fix_rule:" in text
    assert "question-errors" not in str(bias_cards[0])


def test_audit_agent_generates_failure_and_validation_rule(tmp_path: Path) -> None:
    from app.cli import run_cli

    payload = {
        "source_layer": "agent",
        "topic": "Financial Reporting and Analysis",
        "los": "FRA.12",
        "prompt_or_question": "Summarize inventory accounting pitfalls.",
        "wrong_choice_or_output": "Agent claimed LIFO is allowed under IFRS.",
        "correct_resolution": "IFRS does not permit LIFO.",
        "error_type": "hallucinated_rule",
        "confidence": 1,
        "time_spent": 30,
        "evidence_refs": ["agent-run-001"],
    }

    exit_code = run_cli(
        ["audit-agent", "--payload", json.dumps(payload, ensure_ascii=False)],
        repo_root=tmp_path,
    )

    assert exit_code == 0

    failures = list((tmp_path / ".system" / "memory" / "agent-failures").glob("*.md"))
    assert len(failures) == 1
    assert "hallucinated_rule" in failures[0].read_text(encoding="utf-8")

    rules = list((tmp_path / ".system" / "memory" / "validation").glob("*.md"))
    assert len(rules) == 1
    rule_text = rules[0].read_text(encoding="utf-8")
    assert "failure_message:" in rule_text
    assert "IFRS does not permit LIFO" in rule_text


def test_mine_patterns_creates_insight_after_three_related_errors(tmp_path: Path) -> None:
    from app.cli import run_cli

    base_payload = {
        "source_layer": "question",
        "topic": "Corporate Issuers",
        "los": "CI.3",
        "prompt_or_question": "Capital budgeting conflict question",
        "correct_resolution": "Choose project with higher NPV when mutually exclusive.",
        "error_type": "concept_confusion",
        "confidence": 2,
        "time_spent": 150,
        "evidence_refs": ["mock-1"],
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(
            ["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)],
            repo_root=tmp_path,
        )

    exit_code = run_cli(["mine-patterns"], repo_root=tmp_path)

    assert exit_code == 0
    patterns = list((tmp_path / ".system" / "memory" / "patterns").glob("*.md"))
    assert len(patterns) == 1
    text = patterns[0].read_text(encoding="utf-8")
    assert "pattern_key: Corporate Issuers::CI.3::concept_confusion" in text
    assert "recurrence: 3" in text


def test_moc_gap_review_creates_recommendation_for_repeated_targeted_errors(tmp_path: Path) -> None:
    from app.cli import run_cli

    base_payload = {
        "source_layer": "question",
        "topic": "Quantitative Methods",
        "los": "QM.Regression",
        "prompt_or_question": "Regression slope interpretation screenshot question.",
        "correct_resolution": "Slope significance is not the same as economic significance.",
        "error_type": "concept_confusion",
        "confidence": 2,
        "time_spent": 120,
        "evidence_refs": ["qbank-1"],
        "question_source": "official_practice_pack",
        "source_type": "screenshot",
        "evidence_assets": ["attachments/qm-regression.png"],
        "moc_target": "CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(
            ["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)],
            repo_root=tmp_path,
        )

    exit_code = run_cli(["moc-gap-review"], repo_root=tmp_path)

    assert exit_code == 0
    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    assert review.exists()
    text = review.read_text(encoding="utf-8")
    assert "CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md" in text
    assert "recurrence: 3" in text
    assert "suggested_gap_type:" in text


def test_moc_gap_review_skips_repeated_errors_without_moc_target(tmp_path: Path) -> None:
    from app.cli import run_cli

    base_payload = {
        "source_layer": "question",
        "topic": "Economics",
        "los": "ECO.FX",
        "prompt_or_question": "FX quote-direction screenshot question.",
        "correct_resolution": "Check the quote convention before judging appreciation.",
        "error_type": "concept_confusion",
        "confidence": 2,
        "time_spent": 105,
        "evidence_refs": ["qbank-2"],
        "question_source": "official_qbank",
        "source_type": "screenshot",
        "evidence_assets": ["attachments/fx-quote.png"],
        "moc_target": "",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(
            ["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)],
            repo_root=tmp_path,
        )

    exit_code = run_cli(["moc-gap-review"], repo_root=tmp_path)

    assert exit_code == 0
    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    if review.exists():
        text = review.read_text(encoding="utf-8")
        assert "Economics" not in text


def test_post_mock_retro_merges_question_bias_and_agent_findings(tmp_path: Path) -> None:
    from app.cli import run_cli

    question_payload = {
        "source_layer": "question",
        "topic": "Equity Investments",
        "los": "EI.8",
        "prompt_or_question": "Dividend discount model question",
        "wrong_choice_or_output": "Chose high-growth model incorrectly",
        "correct_resolution": "Use Gordon growth only when growth is stable.",
        "error_type": "concept_confusion",
        "confidence": 2,
        "time_spent": 180,
        "evidence_refs": ["mock-2"],
    }
    bias_payload = {
        "source_layer": "bias",
        "topic": "Mock Timing",
        "los": "TIME.1",
        "prompt_or_question": "后半场时间分配失衡",
        "wrong_choice_or_output": "最后 20 题只剩 12 分钟",
        "correct_resolution": "前 60 题控制在 78 分钟内。",
        "error_type": "time_misallocation",
        "confidence": 2,
        "time_spent": 0,
        "evidence_refs": ["mock-2"],
    }
    agent_payload = {
        "source_layer": "agent",
        "topic": "Mock Review",
        "los": "AGENT.1",
        "prompt_or_question": "Agent review summary",
        "wrong_choice_or_output": "Missed timing issue in summary",
        "correct_resolution": "Summary should include time allocation root cause.",
        "error_type": "missed_root_cause",
        "confidence": 1,
        "time_spent": 20,
        "evidence_refs": ["mock-2"],
    }

    run_cli(["record-mistake", "--payload", json.dumps(question_payload, ensure_ascii=False)], repo_root=tmp_path)
    run_cli(["review-session", "--payload", json.dumps(bias_payload, ensure_ascii=False)], repo_root=tmp_path)
    run_cli(["audit-agent", "--payload", json.dumps(agent_payload, ensure_ascii=False)], repo_root=tmp_path)

    exit_code = run_cli(["post-mock-retro", "--session-id", "mock-2"], repo_root=tmp_path)

    assert exit_code == 0
    summary = tmp_path / ".system" / "memory" / "strategy" / "mock-2-retro.md"
    assert summary.exists()
    text = summary.read_text(encoding="utf-8")
    assert "Equity Investments" in text
    assert "time_misallocation" in text
    assert "missed_root_cause" in text


def test_obsidian_export_updates_existing_pages_instead_of_duplication(tmp_path: Path) -> None:
    from app.cli import run_cli

    payload = {
        "source_layer": "question",
        "topic": "Fixed Income",
        "los": "FI.5",
        "prompt_or_question": "Duration and convexity question",
        "wrong_choice_or_output": "Ignored convexity adjustment",
        "correct_resolution": "Use convexity for larger yield shifts.",
        "error_type": "concept_confusion",
        "confidence": 2,
        "time_spent": 200,
        "evidence_refs": ["mock-3"],
    }

    run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)
    first = run_cli(["pre-mock-brief"], repo_root=tmp_path)
    second = run_cli(["pre-mock-brief"], repo_root=tmp_path)

    assert first == 0
    assert second == 0

    daily = tmp_path / "CFA_tier1" / "dashboard" / "今日新增错题.md"
    assert daily.exists()
    text = daily.read_text(encoding="utf-8")
    assert text.count("Fixed Income") == 1


def test_workflow_releases_catalog_before_temporary_repo_cleanup() -> None:
    from app.cli import run_cli

    payload = {
        "source_layer": "question",
        "topic": "Derivatives",
        "los": "DER.1",
        "prompt_or_question": "Forward payoff question from a temporary smoke repository.",
        "wrong_choice_or_output": "Confused payoff with profit.",
        "correct_resolution": "Payoff excludes the original derivative premium or financing cost.",
        "error_type": "concept_confusion",
        "confidence": 2,
        "time_spent": 95,
        "evidence_refs": ["temp-smoke"],
    }

    with TemporaryDirectory() as repo_dir:
        exit_code = run_cli(
            ["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)],
            repo_root=Path(repo_dir),
        )

        assert exit_code == 0
