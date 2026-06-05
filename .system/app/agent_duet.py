from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from app.codex_loop import plan_codex_loop
from app.storage import Repository


DUET_STREAM = "agent_duet"
DUET_ROOT = Path(".system/memory/collaboration/internal-agents")
DUET_ARCHIVE = DUET_ROOT / "briefs"
DUET_CURRENT = DUET_ROOT / "CURRENT_DUET.md"


def _now() -> datetime:
    return datetime.now(UTC)


def _timestamp_slug(value: datetime) -> str:
    return value.strftime("%Y%m%d-%H%M%S")


@dataclass(slots=True)
class AgentDuetBrief:
    brief_id: str
    generated_at: str
    archive_path: str
    current_path: str
    loop_id: str
    selected_candidate_id: str
    task_path: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def export_agent_duet_brief(repo: Repository, *, mode: str = "unattended") -> AgentDuetBrief:
    plan = plan_codex_loop(repo, mode=mode)
    now = _now()
    brief_root = repo.root / DUET_ARCHIVE
    brief_root.mkdir(parents=True, exist_ok=True)

    brief_id = f"duet-{_timestamp_slug(now)}"
    archive_rel = DUET_ARCHIVE / f"{brief_id}.md"
    archive_path = repo.root / archive_rel
    current_path = repo.root / DUET_CURRENT
    current_path.parent.mkdir(parents=True, exist_ok=True)

    selected = plan.selected
    task_text = ""
    if plan.task_path:
        task_file = repo.root / plan.task_path
        if task_file.exists():
            task_text = task_file.read_text(encoding="utf-8")

    if selected is None:
        planner_lines = [
            "- No eligible candidate is available.",
            "- Do not invent work without evidence.",
            "- Ask the critic to identify the smallest safe next candidate source.",
        ]
        critic_lines = [
            "- Confirm that the loop should stop instead of fabricating tasks.",
            "- Recommend adding new candidate sources from current local evidence.",
            "- Keep core question-bank truth locked.",
        ]
        synthesis_lines = [
            "- Outcome: stop current execution work.",
            "- Next move: improve candidate discovery or import new evidence.",
        ]
    else:
        planner_lines = [
            f"- Candidate: {selected.candidate_id}",
            f"- Goal: {selected.title}",
            *[f"- Output: {item}" for item in selected.expected_outputs],
        ]
        critic_lines = [
            *[f"- Acceptance: {item}" for item in selected.acceptance_criteria],
            *[f"- Safety: {item}" for item in selected.safety_limits],
        ]
        synthesis_lines = [
            f"- Proceed with bounded task `{selected.candidate_id}`.",
            "- Implement only what the current acceptance criteria require.",
            "- Verify before marking completion or choosing another task.",
        ]

    lines = [
        "---",
        f"brief_id: {brief_id}",
        f"generated_at: {now.isoformat()}",
        f"loop_id: {plan.loop_id}",
        f"mode: {plan.mode}",
        "---",
        "",
        "# Internal Agent Duet",
        "",
        "Two local roles collaborate here when external ChatGPT control is unavailable.",
        "",
        "## Planner",
        *planner_lines,
        "",
        "## Critic",
        *critic_lines,
        "",
        "## Synthesis",
        *synthesis_lines,
        "",
        "## Active Task",
        task_text.strip() or "(no active task file)",
    ]
    body = "\n".join(lines).strip() + "\n"
    archive_path.write_text(body, encoding="utf-8")
    current_path.write_text(body, encoding="utf-8")

    payload = AgentDuetBrief(
        brief_id=brief_id,
        generated_at=now.isoformat(),
        archive_path=str(archive_rel).replace("\\", "/"),
        current_path=str(DUET_CURRENT).replace("\\", "/"),
        loop_id=plan.loop_id,
        selected_candidate_id=selected.candidate_id if selected else "",
        task_path=plan.task_path,
    )
    repo.append_jsonl_event(
        DUET_STREAM,
        {
            "event_type": "agent.duet.exported",
            **payload.as_dict(),
        },
    )
    return payload
