from __future__ import annotations

from pathlib import Path

from app.agent_duet import export_agent_duet_brief
from app.codex_loop import complete_codex_loop_candidate
from app.storage import Repository


def _enable_loop(root: Path) -> None:
    config = root / ".system" / "config" / "features.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text("codex_self_loop_enabled: true\n", encoding="utf-8")


def test_agent_duet_brief_exports_planner_and_critic_sections(tmp_path: Path) -> None:
    repo = Repository(tmp_path)
    _enable_loop(tmp_path)
    complete_codex_loop_candidate(
        repo,
        candidate_id="self-cycle-skill-governance",
        summary="done",
        artifacts=[".system/app/codex_loop.py"],
        verification="ok",
    )

    attempts_path = tmp_path / "apps" / "api" / "routers"
    attempts_path.mkdir(parents=True, exist_ok=True)
    (attempts_path / "attempts.py").write_text(
        'return {"status": "screenshot_saved", "suggested_payload": {}}\n',
        encoding="utf-8",
    )

    brief = export_agent_duet_brief(repo)

    text = (tmp_path / brief.current_path).read_text(encoding="utf-8")
    assert "## Planner" in text
    assert "## Critic" in text
    assert "gap-screenshot-structured-extraction" in text

    events = repo.load_jsonl_events("agent_duet")
    assert events[-1]["event_type"] == "agent.duet.exported"

