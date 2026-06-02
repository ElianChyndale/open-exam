from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory



def write_moc(tmp_path: Path, relative_path: str, lines: list[str]) -> None:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_note(tmp_path: Path, relative_path: str, lines: list[str]) -> None:
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


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

    mock_projection = tmp_path / "CFA_tier1" / "mock" / "FI" / "00-FI-Mistakes.md"
    assert mock_projection.exists()
    projection_text = mock_projection.read_text(encoding="utf-8")
    assert "Fixed Income" in projection_text
    assert "attachments/mock4-q18.png" in projection_text


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

    write_moc(
        tmp_path,
        "CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md",
        [
            "## Quantitative Methods 核心知识树",
            "```text",
            "├── 1.5 Annualization and continuous compounding【考试核心】",
            "│   ├── 定义/直觉",
            "│   │   └── 连续复利和普通复利口径要分开",
            "```",
            "",
            "## 核心公式速查",
            "| 指标 | 公式 | 知识树节点 | 考试说明 |",
            "|------|------|------------|----------|",
            "| Convert CC Return | `e^(r_cc)-1` | `1.5` | 连续复利回到 holding period return |",
        ],
    )

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

    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    assert review.exists()
    text = review.read_text(encoding="utf-8")
    assert "CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md" in text
    assert "recurrence: 3" in text
    assert "suggested_gap_type:" in text
    assert "gap_target: knowledge_tree_concept" in text


def test_moc_gap_review_marks_formula_table_variant_when_tree_has_core_formula(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Derivatives/00-Derivatives-MOC.md",
        [
            "## Derivatives 核心知识树",
            "```text",
            "├── M05: Pricing and Valuation of Forwards and Futures【考试核心】",
            "│   ├── 核心公式",
            "│   │   └── F0(T) = S0(1+r)^T",
            "```",
            "",
            "## 核心公式速查",
            "| 指标 | 公式 | 知识树节点 | 考试说明 |",
            "|------|------|------------|----------|",
            "| Forward Price | `F0(T) = S0(1+r)^T` | `M05` | 无收入资产远期价格 |",
        ],
    )

    base_payload = {
        "source_layer": "question",
        "topic": "Derivatives",
        "los": "DER.Forward",
        "prompt_or_question": "Known-yield forward question.",
        "correct_resolution": "Use the yield-adjusted carry variant.",
        "error_type": "formula_misuse",
        "confidence": 2,
        "time_spent": 100,
        "evidence_refs": ["forward-variant"],
        "moc_target": "CFA_tier1/Derivatives/00-Derivatives-MOC.md",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    text = review.read_text(encoding="utf-8")
    assert "gap_target: formula_table_variant" in text


def test_moc_gap_review_marks_both_when_tree_and_formula_table_are_missing(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md",
        [
            "## Fixed Income 核心知识树",
            "```text",
            "├── M03: Yield Measures, Spot Rates, and Forward Rates【考试核心】",
            "│   └── 注意：先分清 spot、par、forward 的题目口径",
            "```",
            "",
            "## 高频考试陷阱速查",
            "| 错误理解 | 正确理解 |",
            "|----------|----------|",
            "| 远期利率可以直接套现值公式 | 先匹配利率定义再进公式 |",
        ],
    )

    base_payload = {
        "source_layer": "question",
        "topic": "Fixed Income",
        "los": "FI.ForwardRates",
        "prompt_or_question": "Forward rate extraction question.",
        "correct_resolution": "Use the no-arbitrage spot/forward linkage.",
        "error_type": "formula_misuse",
        "confidence": 2,
        "time_spent": 95,
        "evidence_refs": ["fi-forward-1"],
        "moc_target": "CFA_tier1/Fixed_Income/00-Fixed-Income-MOC.md",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    text = review.read_text(encoding="utf-8")
    assert "gap_target: both" in text


def test_moc_gap_review_marks_knowledge_tree_concept_for_concept_confusion(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md",
        [
            "## Corporate Issuers 核心知识树",
            "```text",
            "├── 2.3 Mutually exclusive projects【考试核心】",
            "│   └── 注意：NPV 和 IRR 排序冲突时优先 NPV",
            "```",
        ],
    )

    base_payload = {
        "source_layer": "question",
        "topic": "Corporate Issuers",
        "los": "CI.3",
        "prompt_or_question": "Capital budgeting conflict question.",
        "correct_resolution": "Choose the higher NPV project when projects are mutually exclusive.",
        "error_type": "concept_confusion",
        "confidence": 2,
        "time_spent": 150,
        "evidence_refs": ["corp-concept-1"],
        "moc_target": "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    text = review.read_text(encoding="utf-8")
    assert "gap_target: knowledge_tree_concept" in text


def test_moc_gap_review_marks_exam_trap_for_non_formula_non_concept_errors(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Economics/00-Economics-MOC.md",
        [
            "## Economics 核心知识树",
            "```text",
            "├── M04: Currency exchange rates【考试核心】",
            "│   └── 注意：先读清 base / price currency",
            "```",
        ],
    )

    base_payload = {
        "source_layer": "question",
        "topic": "Economics",
        "los": "ECO.FX",
        "prompt_or_question": "FX quote-direction question.",
        "correct_resolution": "Read the quote convention before deciding appreciation.",
        "error_type": "careless_reading",
        "confidence": 2,
        "time_spent": 80,
        "evidence_refs": ["econ-trap-1"],
        "moc_target": "CFA_tier1/Economics/00-Economics-MOC.md",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    text = review.read_text(encoding="utf-8")
    assert "gap_target: exam_trap" in text


def test_moc_gap_review_keeps_ethics_out_of_formula_targeting(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md",
        [
            "## Ethical and Professional Standards 核心知识树",
            "```text",
            "├── M03: Standard I - Professionalism【考试核心】",
            "│   └── 注意：law answers 'may I'; ethics asks 'should I'",
            "```",
            "",
            "## 核心公式速查",
            "| 指标 | 公式 | 知识树节点 | 考试说明 |",
            "|------|------|------------|----------|",
        ],
    )

    base_payload = {
        "source_layer": "question",
        "topic": "Ethical and Professional Standards",
        "los": "I.B",
        "prompt_or_question": "Independence and objectivity question.",
        "correct_resolution": "Issuer-paid travel can impair independence.",
        "error_type": "formula_misuse",
        "confidence": 2,
        "time_spent": 70,
        "evidence_refs": ["ethics-1"],
        "moc_target": "CFA_tier1/Ethical_and_Professional_Standards/00-Ethical-and-Professional-Standards-MOC.md",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    review = tmp_path / ".system" / "memory" / "strategy" / "moc-gap-review.md"
    text = review.read_text(encoding="utf-8")
    assert "gap_target: knowledge_tree_concept" in text
    assert "knowledge_tree_core_formula" not in text


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


def test_daily_review_pack_uses_due_cards_and_recent_cache(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md",
        [
            "## 2. Formula & Framework Map 公式与框架地图",
            "### Capital Investments",
            "| Tool | Formula / Framework | Exam use |",
            "|---|---|---|",
            "| NPV | `NPV = sum CFt/(1+r)^t - initial outlay` | accept if positive; best wealth-maximizing rule. |",
            "| IRR | discount rate making `NPV = 0` | can mislead for mutually exclusive projects. |",
            "## 3. Module Atlas 模块地图",
        ],
    )
    write_moc(
        tmp_path,
        "CFA_tier1/Economics/00-Economics-MOC.md",
        [
            "## 2. Formula & Framework Map 公式与框架地图",
            "### FX Calculations",
            "| Trigger | Formula / framework | Exam action |",
            "|---|---|---|",
            "| Quote convention | `A/B` means 1 unit of A costs B | `A/B` up = A appreciates versus B. |",
            "## 3. Module Atlas 模块地图",
        ],
    )

    payload = {
        "source_layer": "question",
        "topic": "Economics",
        "los": "ECO.FX",
        "prompt_or_question": "FX quote-direction question. A. USD appreciates B. EUR appreciates C. no change",
        "wrong_choice_or_output": "Read USD/EUR backwards",
        "correct_resolution": "Read the base and price currency before judging appreciation.",
        "error_type": "careless_reading",
        "confidence": 1,
        "time_spent": 90,
        "evidence_refs": ["study-cache-1"],
        "created_at": "2026-05-27T10:00:00+00:00",
    }

    run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)
    exit_code = run_cli(
        [
            "daily-review-pack",
            "--date",
            "2100-01-01",
            "--days-back",
            "30000",
            "--focus-topic",
            "Corporate Issuers",
        ],
        repo_root=tmp_path,
    )

    assert exit_code == 0
    strategy = tmp_path / ".system" / "memory" / "strategy" / "daily-review.md"
    assert strategy.exists()
    text = strategy.read_text(encoding="utf-8")
    assert "# Daily Review" in text
    assert "到期复习" in text
    assert "近期低信心 2026-05-27" in text
    assert "Corporate Issuers" in text
    assert "## 一、知识点和公式" in text
    assert "## 二、错题" in text
    assert "NPV = sum CFt" in text
    assert "**Trigger:** Tool" not in text
    assert "**先问自己：**" in text
    assert "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md" in text
    assert "Read the base and price currency" in text
    assert "- retrieval_prompt:" not in text
    assert "#### 题目" in text
    assert "> [!answer]- Reveal correct solution" in text
    assert "> A. USD appreciates" in text
    assert "> B. EUR appreciates" in text

    dashboard = tmp_path / "CFA_tier1" / "dashboard" / "Daily Review.md"
    assert dashboard.exists()
    dashboard_text = dashboard.read_text(encoding="utf-8")
    assert "## 一、知识点和公式" in dashboard_text
    assert "## 二、错题" in dashboard_text
    assert "Bedtime: only mental replay" not in dashboard_text
    legacy_dashboard = tmp_path / "CFA_tier1" / "dashboard" / "今日复习资料.md"
    assert legacy_dashboard.read_text(encoding="utf-8") == "# 今日复习资料\n\n已迁移至 [[Daily Review]]。\n"


def test_record_progress_writes_progress_ledger(tmp_path: Path) -> None:
    from app.cli import run_cli

    payload = {
        "date": "2026-05-29",
        "record_type": "daily_review_completed",
        "status": "completed",
        "focus_topic": "Corporate Issuers",
        "note": "今日复习资料完成",
    }

    exit_code = run_cli(["record-progress", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    assert exit_code == 0
    progress_log = tmp_path / ".system" / "memory" / "progress" / "progress-events.jsonl"
    assert progress_log.exists()
    text = progress_log.read_text(encoding="utf-8")
    assert "daily_review_completed" in text
    assert "Corporate Issuers" in text


def test_daily_review_command_writes_snapshot_and_collapsed_reveals(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md",
        [
            "## 2. Formula & Framework Map 公式与框架地图",
            "### Capital Investments",
            "| Tool | Formula / Framework | Exam use |",
            "|---|---|---|",
            "| NPV | `NPV = sum CFt/(1+r)^t - initial outlay` | accept if positive. |",
            "## 3. Module Atlas 模块地图",
        ],
    )
    payload = {
        "source_layer": "question",
        "topic": "Corporate Issuers",
        "los": "M05 NPV",
        "prompt_or_question": "Which capital-allocation rule should lead the decision?",
        "wrong_choice_or_output": "IRR always leads.",
        "correct_resolution": "Use NPV for mutually exclusive projects.",
        "error_type": "concept_confusion",
        "confidence": 1,
        "time_spent": 60,
        "evidence_refs": ["snapshot-test"],
        "created_at": "2026-05-29T10:00:00+00:00",
    }

    run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)
    exit_code = run_cli(
        ["daily-review", "--date", "2026-05-30", "--focus-topic", "Corporate Issuers"],
        repo_root=tmp_path,
    )

    assert exit_code == 0
    text = (tmp_path / ".system" / "memory" / "strategy" / "daily-review.md").read_text(encoding="utf-8")
    assert "# Daily Review" in text
    assert "> [!answer]- Reveal knowledge point" in text
    assert "> [!answer]- Reveal correct solution" in text
    assert "> > Use NPV for mutually exclusive projects." not in text

    latest_path = tmp_path / ".system" / "memory" / "review" / "daily" / "latest.json"
    latest = json.loads(latest_path.read_text(encoding="utf-8"))
    assert latest["schema_version"] == 1
    assert latest["review_id"].startswith("daily-review-")
    assert latest["generation"]["focus_topic"] == "Corporate Issuers"
    assert latest["knowledge_points"]
    assert latest["mistake_cards"]

    review_events = [
        json.loads(line)
        for line in (tmp_path / ".system" / "events" / "review" / "review-events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert [event["event_type"] for event in review_events] == ["daily_review.generated"]
    assert review_events[0]["payload"]["review_id"] == latest["review_id"]


def test_complete_daily_review_marks_items_reviewed_once_idempotently(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md",
        [
            "## 2. Formula & Framework Map 公式与框架地图",
            "### Capital Investments",
            "| Tool | Formula / Framework | Exam use |",
            "|---|---|---|",
            "| NPV | `NPV = sum CFt/(1+r)^t - initial outlay` | accept if positive. |",
            "## 3. Module Atlas 模块地图",
        ],
    )
    payload = {
        "source_layer": "question",
        "topic": "Corporate Issuers",
        "los": "M05 NPV",
        "prompt_or_question": "Which rule should lead mutually exclusive project selection?",
        "wrong_choice_or_output": "IRR",
        "correct_resolution": "NPV",
        "error_type": "concept_confusion",
        "confidence": 1,
        "time_spent": 60,
        "evidence_refs": ["completion-test"],
        "created_at": "2026-05-29T10:00:00+00:00",
    }

    run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)
    run_cli(
        ["daily-review", "--date", "2026-05-30", "--focus-topic", "Corporate Issuers"],
        repo_root=tmp_path,
    )
    latest = json.loads(
        (tmp_path / ".system" / "memory" / "review" / "daily" / "latest.json").read_text(encoding="utf-8")
    )
    review_id = latest["review_id"]

    assert run_cli(["complete-daily-review", "--review-id", review_id], repo_root=tmp_path) == 0
    assert run_cli(["complete-daily-review", "--review-id", review_id], repo_root=tmp_path) == 0

    card_path = next((tmp_path / ".system" / "memory" / "question-errors").glob("*.md"))
    assert "review_status: Reviewed once" in card_path.read_text(encoding="utf-8")

    overlay = json.loads(
        (tmp_path / ".system" / "memory" / "review" / "knowledge-status.json").read_text(encoding="utf-8")
    )
    assert overlay["knowledge_points"]
    assert {item["status"] for item in overlay["knowledge_points"].values()} == {"Reviewed once"}

    review_events = [
        json.loads(line)
        for line in (tmp_path / ".system" / "events" / "review" / "review-events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    event_types = [event["event_type"] for event in review_events]
    assert event_types.count("daily_review.completed") == 1
    assert event_types.count("daily_review.item.reviewed") == (
        len(latest["knowledge_points"]) + len(latest["mistake_cards"])
    )


def test_daily_review_activates_self_explanation_and_worked_example_fading(tmp_path: Path) -> None:
    from app.cli import run_cli

    base_payload = {
        "source_layer": "question",
        "topic": "Fixed Income",
        "los": "FI.Duration",
        "prompt_or_question": "Estimate the price impact after a yield change.",
        "correct_resolution": "Write the duration term first, then add the convexity adjustment.",
        "error_type": "formula_misuse",
        "confidence": 1,
        "time_spent": 60,
        "evidence_refs": ["fading-test"],
        "created_at": "2026-05-29T10:00:00+00:00",
    }
    for wrong in ("Used duration only.", "Forgot convexity.", "Used the wrong sign."):
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    run_cli(["daily-review", "--date", "2026-05-30"], repo_root=tmp_path)
    text = (tmp_path / ".system" / "memory" / "strategy" / "daily-review.md").read_text(encoding="utf-8")

    assert "#### 主动回忆" in text
    assert "#### 自我解释" in text
    assert "#### Worked example fading" in text
    assert "full solution" in text


def test_daily_review_pack_renders_choices_in_separate_section(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md",
        [
            "## 2. Formula & Framework Map 公式与框架地图",
            "### Capital Investments",
            "| Tool | Formula / Framework | Exam use |",
            "|---|---|---|",
            "| NPV | `NPV = sum CFt/(1+r)^t - initial outlay` | accept if positive. |",
            "## 3. Module Atlas 模块地图",
        ],
    )
    payload = {
        "source_layer": "question",
        "topic": "Corporate Issuers",
        "los": "M05 NPV",
        "prompt_or_question": "The NPV is closest to: A. 578. B. 605. C. 636.",
        "wrong_choice_or_output": "A. 578.",
        "correct_resolution": "C. 636. CF0 is not discounted.",
        "error_type": "formula_misuse",
        "confidence": 1,
        "time_spent": 60,
        "evidence_refs": ["npv-choice"],
        "created_at": "2026-05-29T10:00:00+00:00",
    }

    run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)
    exit_code = run_cli(
        ["daily-review-pack", "--date", "2026-05-30", "--focus-topic", "Corporate Issuers"],
        repo_root=tmp_path,
    )

    assert exit_code == 0
    text = (tmp_path / ".system" / "memory" / "strategy" / "daily-review.md").read_text(encoding="utf-8")
    assert "#### 题目" in text
    assert "#### 选项" in text
    assert "> The NPV is closest to:" in text
    assert "> A. 578." in text
    assert "> B. 605." in text
    assert "> C. 636." in text


def test_daily_review_pack_expanded_uses_module_note_and_progress(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md",
        [
            "## 2. Formula & Framework Map 公式与框架地图",
            "### Capital Investments",
            "| Tool | Formula / Framework | Exam use |",
            "|---|---|---|",
            "| NPV | `NPV = sum CFt/(1+r)^t - initial outlay` | accept if positive. |",
            "| IRR | discount rate making `NPV = 0` | compare with required return. |",
            "| ROIC | operating profit after tax / invested capital | performance metric, not a full replacement for NPV. |",
            "## 3. Module Atlas 模块地图",
        ],
    )
    write_note(
        tmp_path,
        "CFA_tier1/Corporate_Issuers/M05-Capital-Investments-and-Capital-Allocation.md",
        [
            "# M05",
            "### Project Type Classifier 项目类型识别",
            "| Project type | Core meaning | Exam trigger | Not this when... |",
            "|---|---|---|---|",
            "| Compliance project | Required by third parties to meet safety or regulatory standards | improved safety standards | not expansion |",
            "### Real Option Classifier 实物期权识别",
            "| Real option type | Core meaning | Exam trigger | Common trap |",
            "|---|---|---|---|",
            "| Sizing option | Change project scale after investment | abandon project, expand capacity | Abandonment is sizing. |",
        ],
    )
    write_note(
        tmp_path,
        "CFA_tier1/Economics/M04-Monetary-Policy.md",
        [
            "# M04",
            "## 4. Formula & Decision Bench 公式与决策台",
            "| Trigger | Formula / Framework | Exam use |",
            "|---|---|---|",
            "| QE | central bank asset purchases | non-focus expanded note should not lead the pack |",
        ],
    )
    progress_payload = {
        "date": "2026-05-29",
        "record_type": "daily_review_completed",
        "status": "completed",
        "focus_topic": "Corporate Issuers",
    }
    run_cli(["record-progress", "--payload", json.dumps(progress_payload, ensure_ascii=False)], repo_root=tmp_path)
    economics_payload = {
        "source_layer": "question",
        "topic": "Economics",
        "los": "M04 Monetary Policy",
        "prompt_or_question": "QE question. A. reserves rise B. reserves fall C. no effect",
        "wrong_choice_or_output": "B",
        "correct_resolution": "QE expands reserves.",
        "error_type": "concept_confusion",
        "confidence": 1,
        "time_spent": 60,
        "evidence_refs": ["econ-qe"],
        "created_at": "2026-05-29T10:00:00+00:00",
    }
    run_cli(["record-mistake", "--payload", json.dumps(economics_payload, ensure_ascii=False)], repo_root=tmp_path)

    exit_code = run_cli(
        [
            "daily-review-pack",
            "--date",
            "2026-05-30",
            "--focus-topic",
            "Corporate Issuers",
            "--knowledge-depth",
            "expanded",
        ],
        repo_root=tmp_path,
    )

    assert exit_code == 0
    text = (tmp_path / ".system" / "memory" / "strategy" / "daily-review.md").read_text(encoding="utf-8")
    assert "### 1. Corporate Issuers" in text
    assert "Project Type Classifier" in text
    assert "Compliance project" in text
    assert "Real Option Classifier" in text
    assert "Sizing option" in text
    assert "non-focus expanded note should not lead the pack" not in text
    assert "已完成复习: 2026-05-29" in text


def test_daily_review_pack_promotes_repeated_patterns(tmp_path: Path) -> None:
    from app.cli import run_cli

    write_moc(
        tmp_path,
        "CFA_tier1/Corporate_Issuers/00-Corporate-Issuers-MOC.md",
        [
            "## 2. Formula & Framework Map 公式与框架地图",
            "### Capital Investments",
            "| Tool | Formula / Framework | Exam use |",
            "|---|---|---|",
            "| NPV | `NPV = sum CFt/(1+r)^t - initial outlay` | best wealth-maximizing rule. |",
            "| IRR | discount rate making `NPV = 0` | can mislead with mutually exclusive projects. |",
            "## 3. Module Atlas 模块地图",
        ],
    )

    base_payload = {
        "source_layer": "question",
        "topic": "Corporate Issuers",
        "los": "CI.5",
        "prompt_or_question": "Capital allocation ranking question.",
        "correct_resolution": "NPV is the preferred criterion for mutually exclusive projects.",
        "error_type": "concept_confusion",
        "confidence": 4,
        "time_spent": 120,
        "evidence_refs": ["corp-cache"],
        "created_at": "2026-05-25T10:00:00+00:00",
    }

    for wrong in ["A", "B", "C"]:
        payload = dict(base_payload, wrong_choice_or_output=wrong)
        run_cli(["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    exit_code = run_cli(
        ["daily-review-pack", "--date", "2026-05-28", "--focus-topic", "Corporate Issuers"],
        repo_root=tmp_path,
    )

    assert exit_code == 0
    strategy = tmp_path / ".system" / "memory" / "strategy" / "daily-review.md"
    text = strategy.read_text(encoding="utf-8")
    assert "重复错误 3 次" in text
    assert "Corporate Issuers | CI.5 | concept_confusion" in text
    assert "连续 3 次以上出错" in text


def test_write_todo_archives_existing_file_and_writes_task_level_list(tmp_path: Path) -> None:
    from app.cli import run_cli

    existing = tmp_path / "today_todo.md"
    existing.write_text("# 旧 Todo\n\n- [ ] 检查椅子是否稳固、螺丝是否拧紧\n", encoding="utf-8")

    payload = {
        "date": "2026-05-28",
        "title": "今日 Todo",
        "focus": "完成 Corporate Issuers 学习并保留足够做题时间",
        "tasks": [
            "完成 Corporate Issuers 主学习",
            "完成今日复习资料",
            "做 Corporate Issuers 练习题",
            "处理今天新增错题",
            "整理学习区和设备",
        ],
        "time_blocks": [
            "上午：Corporate Issuers 主学习",
            "下午：练习题和错题",
            "晚上：轻复盘",
        ],
    }

    exit_code = run_cli(["write-todo", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    assert exit_code == 0
    archives = list((tmp_path / "schedule" / "todo_archive").glob("2026-05-28-todo*.md"))
    assert len(archives) == 1
    assert "检查椅子是否稳固" in archives[0].read_text(encoding="utf-8")

    dashboard_todo = tmp_path / "CFA_tier1" / "dashboard" / "today_todo.md"
    text = dashboard_todo.read_text(encoding="utf-8")
    assert "focus: 完成 Corporate Issuers 学习并保留足够做题时间" in text
    assert "- [ ] 完成 Corporate Issuers 主学习" in text
    assert "- [ ] 完成 Daily Review（deadline: 20:00）" in text
    assert "- [ ] 处理今天新增错题" in text
    assert "## Review" in text
    assert "检查椅子是否稳固" not in text


def test_write_todo_supports_deadlines_and_adds_daily_review_by_default(tmp_path: Path) -> None:
    from app.cli import run_cli

    payload = {
        "date": "2026-05-29",
        "title": "今日 Todo",
        "focus": "完成上线任务",
        "tasks": [
            {"task": "完成 Corporate Issuers 主学习", "deadline": "5:30pm"},
            {"task": "完成 Laptop 上线", "deadline": "18:30"},
            {"task": "完成微信小程序上线", "deadline": "8:30pm"},
            {"task": "在微信小程序发布并分享一条内容", "deadline": "21:00"},
        ],
    }

    exit_code = run_cli(["write-todo", "--payload", json.dumps(payload, ensure_ascii=False)], repo_root=tmp_path)

    assert exit_code == 0
    text = (tmp_path / "CFA_tier1" / "dashboard" / "today_todo.md").read_text(encoding="utf-8")
    assert "- [ ] 完成 Daily Review（deadline: 20:00）" in text
    assert "- [ ] 完成 Corporate Issuers 主学习（deadline: 17:30）" in text
    assert "- [ ] 完成 Laptop 上线（deadline: 18:30）" in text
    assert "- [ ] 完成微信小程序上线（deadline: 20:30）" in text
    assert "- [ ] 在微信小程序发布并分享一条内容（deadline: 21:00）" in text


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


def test_high_confidence_error_generates_calibration_warning(tmp_path: Path) -> None:
    """confidence=4 + wrong → should create calibration-warning artifact."""
    from app.cli import run_cli

    payload = {
        "source_layer": "question",
        "topic": "Fixed Income",
        "los": "FI.Convexity",
        "prompt_or_question": "Convexity adjustment test",
        "wrong_choice_or_output": "A",
        "correct_resolution": "C includes convexity",
        "error_type": "concept_confusion",
        "confidence": 4,  # VERY_CONFIDENT — max danger
        "time_spent": 120,
        "evidence_refs": ["test-calibration"],
    }

    exit_code = run_cli(
        ["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)],
        repo_root=tmp_path,
    )
    assert exit_code == 0

    warning_path = tmp_path / ".system" / "memory" / "strategy" / "calibration-warnings.jsonl"
    assert warning_path.exists()
    text = warning_path.read_text(encoding="utf-8")
    assert "FI.Convexity" in text
    assert "priority_bump" in text


def test_mistake_card_uses_spacing_scheduler(tmp_path: Path) -> None:
    """Card review_due_at should reflect SpacingScheduler output, not 1/3/7."""
    from app.cli import run_cli
    import json

    payload = {
        "source_layer": "question",
        "topic": "Quantitative Methods",
        "los": "QM.Rates",
        "prompt_or_question": "Test question",
        "wrong_choice_or_output": "A",
        "correct_resolution": "B is correct",
        "error_type": "concept_confusion",
        "confidence": 0,  # GUESS level → interval should be 1
        "time_spent": 60,
        "evidence_refs": ["test-spacing"],
    }

    exit_code = run_cli(
        ["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)],
        repo_root=tmp_path,
    )
    assert exit_code == 0

    cards = list((tmp_path / ".system" / "memory" / "question-errors").glob("*.md"))
    assert len(cards) == 1
    text = cards[0].read_text(encoding="utf-8")
    assert "spacing_interval_days:" in text
    assert "spacing_priority:" in text


def test_mark_reviewed_updates_card_and_saves_progress(tmp_path: Path) -> None:
    """Marking a card as reviewed should reschedule and record progress."""
    from app.cli import run_cli
    import json

    payload = {
        "source_layer": "question",
        "topic": "Equity",
        "los": "EQ.DDM",
        "prompt_or_question": "DDM test question",
        "wrong_choice_or_output": "A",
        "correct_resolution": "C is correct",
        "error_type": "concept_confusion",
        "confidence": 2,
        "time_spent": 90,
        "evidence_refs": ["test-review"],
    }
    run_cli(
        ["record-mistake", "--payload", json.dumps(payload, ensure_ascii=False)],
        repo_root=tmp_path,
    )

    cards = list((tmp_path / ".system" / "memory" / "question-errors").glob("*.md"))
    assert len(cards) == 1
    card_text = cards[0].read_text(encoding="utf-8")
    card_id_line = [line for line in card_text.splitlines() if line.startswith("card_id:")][0]
    card_id = card_id_line.split(": ", 1)[1].strip()

    exit_code = run_cli(
        ["mark-reviewed", "--card-id", card_id, "--outcome", "struggled", "--confidence-after", "2"],
        repo_root=tmp_path,
    )
    assert exit_code == 0

    updated = cards[0].read_text(encoding="utf-8")
    assert "previous_reviews: 1" in updated

    progress_path = tmp_path / ".system" / "events" / "progress" / "progress-events.jsonl"
    assert progress_path.exists()
    progress_text = progress_path.read_text(encoding="utf-8")
    assert "card_review" in progress_text
    assert card_id in progress_text
    assert "struggled" in progress_text
