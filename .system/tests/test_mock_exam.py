from pathlib import Path
from app.mock_exam import MockExamManager, PASS_THRESHOLD
from app.cfa_storage import CfaRepository
from app.storage import Repository


def test_mock_exam_start_session(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    manager = MockExamManager(cfa)
    session = manager.start_session()
    assert session["status"] == "in_progress"
    assert session["question_count"] == 90
    assert len(session["subject_distribution"]) == 10


def test_mock_exam_subject_distribution(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    manager = MockExamManager(cfa)
    session = manager.start_session(question_count=100)
    total = sum(session["subject_distribution"].values())
    assert total == 100, f"Subject distribution should sum to {session['question_count']}, got {total}"


def test_mock_exam_record_answer(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    manager = MockExamManager(cfa)
    manager.start_session()
    manager.record_answer("q-1", "Quantitative_Methods", True)
    assert len(manager._session["answers"]) == 1  # type: ignore


def test_mock_exam_complete_session(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    manager = MockExamManager(cfa)
    manager.start_session(question_count=10)
    for i in range(10):
        manager.record_answer(f"q-{i}", "Fixed_Income" if i < 7 else "Equity", correct=i < 7, time_spent_seconds=60.0)
    result = manager.complete_session()
    assert result["status"] == "completed"
    assert result["score"] == 0.7  # 7/10 correct
    assert result["pass"] == (0.7 >= PASS_THRESHOLD)
    assert "subject_scores" in result


def test_mock_exam_no_active_session(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    manager = MockExamManager(cfa)
    try:
        manager.complete_session()
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_mock_exam_session_summary(tmp_path: Path):
    repo = Repository(tmp_path)
    cfa = CfaRepository(repo)
    manager = MockExamManager(cfa)
    manager.start_session(question_count=10)
    for i in range(10):
        manager.record_answer(f"q-{i}", "Ethical_and_Professional_Standards", correct=True, time_spent_seconds=60.0)
    session = manager.complete_session()
    summary = MockExamManager.session_summary(session)
    assert summary["pass"] is True
    assert summary["passing_subjects"] == "1/1"
