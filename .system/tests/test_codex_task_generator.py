from __future__ import annotations

from pathlib import Path

from app.codex_task_generator import generate_codex_task
from app.skill_models import SkillUpgradeProposal


def test_codex_task_generator_writes_governed_task_markdown(tmp_path: Path) -> None:
    proposal = SkillUpgradeProposal(
        proposal_id="proposal-1",
        skill_id="cfa-question-captor",
        title="Improve tutor validator coverage",
        problem_statement="Repeated tutor analyses are missing boundary fields.",
        evidence_summary="Three reflections showed the same omission.",
        requested_changes=["Add boundary generation.", "Add validator coverage."],
        acceptance_criteria=["Boundary is always present.", "Tests pass."],
        limits=["Do not auto-modify skill files."],
        reflection_ids=["reflection-1", "reflection-2", "reflection-3"],
    )
    path = generate_codex_task(tmp_path, proposal)
    body = path.read_text(encoding="utf-8")
    assert "## Goal" in body
    assert "## Outputs" in body
    assert "## Acceptance" in body
    assert "## Limits" in body
    assert "Do not auto-modify skill files." in body
