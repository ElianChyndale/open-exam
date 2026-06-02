"""Tests for the Mock Question Ingestion Pipeline."""

from pathlib import Path

from app.mock_ingestion import (
    MockQuestion,
    ingest_all_mock_questions,
    parse_mock_line,
    select_proactive_questions,
)


def test_parse_valid_line():
    line = "- CFA L1 1-1 Q85 | p.19 | The international organization most likely to provide funds to create basic economic infrastructure in developing countries is the:"
    q = parse_mock_line(line, "Ethics")
    assert q is not None
    assert q.question_id == "mock-Ethics-1-1-Q85"
    assert q.mock_set == "1-1"
    assert q.question_number == "85"
    assert "international organization" in q.question_text


def test_parse_invalid_line():
    line = "# This is not a question"
    q = parse_mock_line(line, "Quant")
    assert q is None


def test_parse_with_extra_whitespace():
    line = "  - CFA L1 2-1 Q42  |  p.10  |  An indicator variable used in a simple linear regression is best described as:  "
    q = parse_mock_line(line, "Quant")
    assert q is not None
    assert q.question_id == "mock-Quant-2-1-Q42"
    assert q.question_number == "42"
    assert "indicator variable" in q.question_text


def test_difficulty_heuristic_most_likely():
    line = "- CFA L1 1-1 Q10 | p.2 | Which of the following is most likely a violation of the Standards?"
    q = parse_mock_line(line, "Ethics")
    assert q is not None
    assert q.difficulty_guess == "medium"


def test_difficulty_heuristic_least_likely():
    line = "- CFA L1 1-1 Q15 | p.3 | Which of the following is least likely to be considered a violation?"
    q = parse_mock_line(line, "Ethics")
    assert q is not None
    assert q.difficulty_guess == "hard"


def test_difficulty_heuristic_calculate():
    line = "- CFA L1 1-1 Q76 | p.17 | Calculate the portfolio standard deviation given the following data:"
    q = parse_mock_line(line, "Quant")
    assert q is not None
    assert q.difficulty_guess == "medium"


def test_subject_name_resolution():
    line = "- CFA L1 1-1 Q01 | p.1 | A zero coupon bond is priced at 90."
    q = parse_mock_line(line, "FI")
    assert q is not None
    assert q.subject_name == "Fixed_Income"


def test_exam_weight_assignment():
    line = "- CFA L1 1-1 Q01 | p.1 | A standard of conduct concerning independence."
    q = parse_mock_line(line, "Ethics")
    assert q is not None
    assert q.exam_weight == 0.18


def test_ingest_from_root(tmp_path: Path):
    # Create a mock file
    mock_dir = tmp_path / "CFA_tier1" / "mock" / "Quant"
    mock_dir.mkdir(parents=True)
    mock_file = mock_dir / "00-Quant-Mock-Questions.md"
    mock_file.write_text(
        "# Quant Mock Questions\n\n"
        "- CFA L1 1-1 Q34 | p.8 | An analyst regresses net profit margin on R&D expenditure.\n"
        "- CFA L1 1-1 Q40 | p.9 | In a simple linear regression model, the residual is computed as:\n"
    )
    result = ingest_all_mock_questions(tmp_path)
    assert result["total_questions"] >= 2
    assert "Quant" in result["by_subject"]
    assert result["by_subject"]["Quant"]["count"] == 2


def test_ingest_all_subjects(tmp_path: Path):
    """Verify that all 10 subjects produce entries in the index."""
    subjects = ["AltInv", "CorpIss", "Derivatives", "Economics", "Equity",
                "Ethics", "FI", "FRA", "Portfolio", "Quant"]
    for subj in subjects:
        mock_dir = tmp_path / "CFA_tier1" / "mock" / subj
        mock_dir.mkdir(parents=True)
        (mock_dir / f"00-{subj}-Mock-Questions.md").write_text(
            f"- CFA L1 1-1 Q01 | p.1 | A sample question for {subj}.\n"
        )
    result = ingest_all_mock_questions(tmp_path)
    assert result["total_questions"] == 10
    for subj in subjects:
        assert subj in result["by_subject"]


def test_index_file_written(tmp_path: Path):
    mock_dir = tmp_path / "CFA_tier1" / "mock" / "Equity"
    mock_dir.mkdir(parents=True)
    (mock_dir / "00-Equity-Mock-Questions.md").write_text(
        "- CFA L1 1-1 Q01 | p.1 | An equity valuation question.\n"
    )
    ingest_all_mock_questions(tmp_path)
    index_path = tmp_path / ".system" / "memory" / "mock_question_index.json"
    assert index_path.exists()
    import json
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert index["total_questions"] == 1
    assert "subject_weights" in index


def test_select_proactive_questions(tmp_path: Path):
    mock_dir = tmp_path / "CFA_tier1" / "mock" / "FI"
    mock_dir.mkdir(parents=True)
    (mock_dir / "00-FI-Mock-Questions.md").write_text(
        "- CFA L1 1-2 Q03 | p.1 | A zero coupon bond is priced at 90 and has three years to maturity.\n"
        "- CFA L1 1-2 Q15 | p.3 | The current yield for a coupon-paying bond trading at a premium is:\n"
    )
    ingest_all_mock_questions(tmp_path)
    selected = select_proactive_questions(tmp_path, subject_coverage={"FI": 0.0}, max_questions=1)
    assert len(selected) >= 1


def test_select_proactive_questions_no_index(tmp_path: Path):
    selected = select_proactive_questions(tmp_path)
    assert selected == []


def test_select_proactive_questions_weights(tmp_path: Path):
    """Questions from higher-weight subjects should rank higher at equal coverage."""
    for subj in ["Ethics", "Quant"]:
        mock_dir = tmp_path / "CFA_tier1" / "mock" / subj
        mock_dir.mkdir(parents=True)
        (mock_dir / f"00-{subj}-Mock-Questions.md").write_text(
            f"- CFA L1 1-1 Q01 | p.1 | A question for {subj}.\n"
        )
    ingest_all_mock_questions(tmp_path)
    selected = select_proactive_questions(tmp_path, max_questions=10)
    subject_codes = [q["subject_code"] for q in selected]
    # Ethics (weight 0.18) should appear before Quant (weight 0.08)
    assert subject_codes.index("Ethics") < subject_codes.index("Quant")


def test_mock_question_as_dict():
    q = MockQuestion(
        question_id="mock-Test-1-1-Q01",
        subject_code="Test",
        subject_name="Test_Subject",
        mock_set="1-1",
        question_number="01",
        source_page="1",
        question_text="A test question?",
        difficulty_guess="easy",
        exam_weight=0.08,
    )
    d = q.as_dict()
    assert d["question_id"] == "mock-Test-1-1-Q01"
    assert d["difficulty_guess"] == "easy"
    assert d["exam_weight"] == 0.08
