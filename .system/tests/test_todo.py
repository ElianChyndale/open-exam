from __future__ import annotations

from pathlib import Path

import pytest

from app.storage import Repository


def test_todo_replay_projection_and_required_daily_review(tmp_path: Path) -> None:
    from app.workflows.todo import create_todo_task, get_todo, replace_todo

    repo = Repository(tmp_path)
    state = replace_todo(
        repo,
        {
            "date": "2026-06-02",
            "focus": "Finish the Todo vertical slice",
            "tasks": [{"task": "Implement reducer", "deadline": "17:30"}],
        },
    )
    state = create_todo_task(
        repo,
        text="Run verification",
        deadline="19:00",
        expected_revision=state["revision"],
    )

    replayed = get_todo(repo)
    assert replayed == state
    assert replayed["revision"] == 2
    assert [task["text"] for task in replayed["tasks"]] == [
        "Implement reducer",
        "Run verification",
        "完成 Daily Review",
    ]
    assert replayed["tasks"][-1]["deadline"] == "20:00"
    assert (tmp_path / ".system" / "memory" / "todo" / "current.json").exists()
    projection = (tmp_path / "CFA_tier1" / "dashboard" / "today_todo.md").read_text(encoding="utf-8")
    assert "- [ ] Run verification（deadline: 19:00）" in projection
    assert "- [ ] 完成 Daily Review（deadline: 20:00）" in projection


def test_todo_revision_conflict_does_not_append_event(tmp_path: Path) -> None:
    from app.workflows.todo import RevisionConflict, create_todo_task, get_todo

    repo = Repository(tmp_path)
    original = get_todo(repo, plan_date="2026-06-02")

    with pytest.raises(RevisionConflict):
        create_todo_task(repo, text="Stale write", expected_revision=99, plan_date="2026-06-02")

    assert get_todo(repo, plan_date="2026-06-02") == original
    assert repo.load_jsonl_events("todo") == []


def test_todo_rollover_archives_previous_projection(tmp_path: Path) -> None:
    from app.workflows.todo import replace_todo

    repo = Repository(tmp_path)
    replace_todo(repo, {"date": "2026-06-01", "tasks": ["Yesterday task"]})
    replace_todo(repo, {"date": "2026-06-02", "tasks": ["Today task"]})

    archives = list((tmp_path / "schedule" / "todo_archive").glob("2026-06-01-todo*.md"))
    assert len(archives) == 1
    assert "Yesterday task" in archives[0].read_text(encoding="utf-8")


def test_study_plan_import_requires_confirmation_and_deduplicates(tmp_path: Path) -> None:
    from app.workflows.todo import import_study_plan_tasks

    repo = Repository(tmp_path)
    with pytest.raises(ValueError, match="confirmation"):
        import_study_plan_tasks(
            repo,
            {"plan_id": "sp-1", "high_energy_tasks": [{"description": "Recall drill"}]},
            confirmed=False,
        )

    state = import_study_plan_tasks(
        repo,
        {
            "plan_id": "sp-1",
            "high_energy_tasks": [{"description": "Recall drill"}],
            "low_energy_tasks": [{"description": "Recall drill"}, {"description": "Read notes"}],
        },
        confirmed=True,
    )
    assert [task["text"] for task in state["tasks"]] == ["Recall drill", "Read notes", "完成 Daily Review"]
