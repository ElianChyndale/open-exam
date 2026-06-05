from __future__ import annotations

from pathlib import Path

from app.chat_collaboration import export_chatgpt_collaboration_brief
from app.codex_loop import complete_codex_loop_candidate, plan_codex_loop
from app.storage import Repository


def _enable_loop(root: Path) -> None:
    config = root / ".system" / "config" / "features.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text("codex_self_loop_enabled: true\n", encoding="utf-8")


def test_export_chatgpt_collaboration_brief_includes_latest_loop_and_task(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_loop(tmp_path)
    (tmp_path / "README.md").write_text("# Demo Repo\n", encoding="utf-8")
    (tmp_path / "PLAN.md").write_text("# Demo Plan\n", encoding="utf-8")
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(exist_ok=True)
    (docs_dir / "chatgpt_codex_collaboration_workflow.md").write_text(
        "# Workflow\nUse ChatGPT for bounded planning.\n",
        encoding="utf-8",
    )

    plan = plan_codex_loop(repo)
    brief = export_chatgpt_collaboration_brief(repo)

    current_text = (tmp_path / brief.current_path).read_text(encoding="utf-8")
    archive_text = (tmp_path / brief.archive_path).read_text(encoding="utf-8")
    assert plan.selected is not None
    assert plan.selected.candidate_id in current_text
    assert "Prompt For ChatGPT" in current_text
    assert "Current task artifact:" in current_text
    assert current_text == archive_text

    events = repo.load_jsonl_events("collaboration")
    assert events[-1]["event_type"] == "collaboration.brief.exported"
    assert events[-1]["selected_candidate_id"] == plan.selected.candidate_id


def test_export_chatgpt_collaboration_brief_handles_no_active_candidate(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_loop(tmp_path)
    (tmp_path / "README.md").write_text("# Demo Repo\n", encoding="utf-8")
    (tmp_path / "PLAN.md").write_text("# Demo Plan\n", encoding="utf-8")
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(exist_ok=True)
    (docs_dir / "chatgpt_codex_collaboration_workflow.md").write_text("# Workflow\n", encoding="utf-8")

    complete_codex_loop_candidate(
        repo,
        candidate_id="self-cycle-skill-governance",
        summary="done",
        artifacts=[".system/app/codex_loop.py"],
        verification="pytest -q .system/tests/test_codex_loop.py",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-1-import-contract",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-2-practice-generation",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-2-answer-wrongbook-contract",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-3-practice-ui-contract",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )
    complete_codex_loop_candidate(
        repo,
        candidate_id="phase-4-analytics-extension-boundary",
        summary="done",
        artifacts=["a"],
        verification="ok",
    )
    plan_codex_loop(repo)

    brief = export_chatgpt_collaboration_brief(repo)
    current_text = (tmp_path / brief.current_path).read_text(encoding="utf-8")
    assert "No autonomous candidate is currently available" in current_text
