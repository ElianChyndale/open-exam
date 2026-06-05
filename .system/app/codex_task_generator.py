from __future__ import annotations

from pathlib import Path

from app.skill_models import SkillUpgradeProposal


def generate_codex_task(repo_root: Path, proposal: SkillUpgradeProposal) -> Path:
    task_root = repo_root / "docs" / "codex_tasks"
    task_root.mkdir(parents=True, exist_ok=True)
    existing = sorted(task_root.glob("TASK-*.md"))
    task_number = len(existing) + 1
    path = task_root / f"TASK-{task_number:03d}.md"
    lines = [
        f"# TASK-{task_number:03d}",
        "",
        "## Goal",
        proposal.problem_statement,
        "",
        "## Outputs",
        *[f"- {item}" for item in proposal.requested_changes],
        "",
        "## Acceptance",
        *[f"- {item}" for item in proposal.acceptance_criteria],
        "",
        "## Limits",
        *[f"- {item}" for item in proposal.limits],
        "",
        "## Proposal Trace",
        f"- proposal_id: {proposal.proposal_id}",
        f"- skill_id: {proposal.skill_id}",
        f"- reflection_ids: {', '.join(proposal.reflection_ids)}",
    ]
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return path
