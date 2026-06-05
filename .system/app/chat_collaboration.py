from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.storage import Repository


COLLAB_STREAM = "collaboration"
COLLAB_ROOT = Path(".system/memory/collaboration/chatgpt")
COLLAB_BRIEFS = COLLAB_ROOT / "briefs"
COLLAB_CURRENT = COLLAB_ROOT / "CURRENT_BRIEF.md"


def _now() -> datetime:
    return datetime.now(UTC)


def _timestamp_slug(value: datetime) -> str:
    return value.strftime("%Y%m%d-%H%M%S")


def _safe_read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _latest_json(path: Path, pattern: str) -> dict[str, Any] | None:
    files = sorted(path.glob(pattern))
    if not files:
        return None
    try:
        return json.loads(files[-1].read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


@dataclass(slots=True)
class CollaborationBrief:
    brief_id: str
    chat_name: str
    generated_at: str
    archive_path: str
    current_path: str
    latest_plan_id: str
    selected_candidate_id: str
    selected_task_path: str
    latest_completion_candidate_id: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _load_latest_loop_plan(repo: Repository) -> dict[str, Any] | None:
    return _latest_json(repo.root / ".system" / "memory" / "codex-loop", "ITER-*.json")


def _load_latest_completion(repo: Repository) -> dict[str, Any] | None:
    return _latest_json(repo.root / ".system" / "memory" / "codex-loop" / "completions", "*.json")


def _build_prompt_block(
    *,
    chat_name: str,
    plan: dict[str, Any] | None,
    completion: dict[str, Any] | None,
    task_text: str,
) -> str:
    selected = plan.get("selected") if isinstance(plan, dict) else None
    plan_id = str(plan.get("loop_id", "")) if isinstance(plan, dict) else ""
    candidate_id = str((selected or {}).get("candidate_id", ""))
    title = str((selected or {}).get("title", ""))
    completion_id = str((completion or {}).get("candidate_id", ""))
    completion_summary = str((completion or {}).get("summary", ""))
    ask = (
        "Please critique this next bounded task, tighten acceptance criteria, and list the smallest safe implementation steps."
        if selected
        else "No autonomous candidate is currently available. Please propose the next smallest bounded task that respects AGENTS.md and keeps core question-bank behavior stable."
    )
    return "\n".join(
        [
            f"You are collaborating with local Codex in the ChatGPT chat named \"{chat_name}\".",
            "Use the repository rules below as hard constraints.",
            "",
            "Constraints:",
            "- Source of truth priority: .system/events -> .system/memory -> workflow code -> skills -> CFA_tier1 projections.",
            "- Do not suggest changing locked question-bank prompts, answers, or explanations.",
            "- Prefer Capture / Memory / Decision layer work before Projection-only work.",
            "- Every recommendation must be traceable, bounded, and testable.",
            "",
            "Current loop state:",
            f"- latest_plan_id: {plan_id or 'none'}",
            f"- selected_candidate_id: {candidate_id or 'none'}",
            f"- selected_title: {title or 'none'}",
            f"- latest_completed_candidate_id: {completion_id or 'none'}",
            f"- latest_completion_summary: {completion_summary or 'none'}",
            "",
            "Current task artifact:",
            task_text.strip() or "(no active task file)",
            "",
            "Your job:",
            ask,
            "Return:",
            "1. A brief decision on whether the task should proceed unchanged, be narrowed, or be replaced.",
            "2. A flat checklist of implementation steps.",
            "3. A flat checklist of verification steps.",
            "4. Any evidence gaps that block safe execution.",
        ]
    ).strip()


def export_chatgpt_collaboration_brief(
    repo: Repository,
    *,
    chat_name: str = "Codex ChatGPT 协同工作流",
) -> CollaborationBrief:
    now = _now()
    brief_root = repo.root / COLLAB_BRIEFS
    brief_root.mkdir(parents=True, exist_ok=True)

    plan = _load_latest_loop_plan(repo)
    completion = _load_latest_completion(repo)
    selected = plan.get("selected") if isinstance(plan, dict) else None
    task_rel = str(plan.get("task_path", "")) if isinstance(plan, dict) else ""
    task_text = _safe_read_text(repo.root / task_rel) if task_rel else ""

    brief_id = f"chatgpt-brief-{_timestamp_slug(now)}"
    archive_rel = COLLAB_BRIEFS / f"{brief_id}.md"
    archive_path = repo.root / archive_rel
    current_path = repo.root / COLLAB_CURRENT
    current_path.parent.mkdir(parents=True, exist_ok=True)

    prompt_block = _build_prompt_block(
        chat_name=chat_name,
        plan=plan,
        completion=completion,
        task_text=task_text,
    )
    readme_excerpt = _safe_read_text(repo.root / "README.md")
    plan_excerpt = _safe_read_text(repo.root / "PLAN.md")
    workflow_doc = _safe_read_text(repo.root / "docs" / "chatgpt_codex_collaboration_workflow.md")

    lines = [
        "---",
        f"brief_id: {brief_id}",
        f"generated_at: {now.isoformat()}",
        f"chat_name: {chat_name}",
        "---",
        "",
        "# ChatGPT Collaboration Brief",
        "",
        "## How To Use",
        "Paste the prompt block below into the ChatGPT chat, then bring the reply back here as planning input.",
        "",
        "## Current Loop Snapshot",
        f"- latest_plan_id: {plan.get('loop_id', 'none') if isinstance(plan, dict) else 'none'}",
        f"- selected_candidate_id: {(selected or {}).get('candidate_id', 'none')}",
        f"- selected_title: {(selected or {}).get('title', 'none')}",
        f"- selected_task_path: {task_rel or 'none'}",
        f"- latest_completed_candidate_id: {(completion or {}).get('candidate_id', 'none')}",
        f"- latest_completion_summary: {(completion or {}).get('summary', 'none')}",
        "",
        "## Prompt For ChatGPT",
        "```text",
        prompt_block,
        "```",
        "",
        "## Project Context Excerpts",
        "### Collaboration Workflow",
        workflow_doc.strip() or "(workflow doc not found)",
        "",
        "### PLAN.md",
        (plan_excerpt.strip()[:4000] + ("..." if len(plan_excerpt.strip()) > 4000 else "")) or "(PLAN.md not found)",
        "",
        "### README.md",
        (readme_excerpt.strip()[:2500] + ("..." if len(readme_excerpt.strip()) > 2500 else "")) or "(README.md not found)",
        "",
        "## Active Task",
        task_text.strip() or "No active `docs/codex_tasks/TASK-*.md` file is linked to the latest plan.",
    ]
    body = "\n".join(lines).strip() + "\n"
    archive_path.write_text(body, encoding="utf-8")
    current_path.write_text(body, encoding="utf-8")

    payload = CollaborationBrief(
        brief_id=brief_id,
        chat_name=chat_name,
        generated_at=now.isoformat(),
        archive_path=str(archive_rel).replace("\\", "/"),
        current_path=str(COLLAB_CURRENT).replace("\\", "/"),
        latest_plan_id=str(plan.get("loop_id", "")) if isinstance(plan, dict) else "",
        selected_candidate_id=str((selected or {}).get("candidate_id", "")),
        selected_task_path=task_rel,
        latest_completion_candidate_id=str((completion or {}).get("candidate_id", "")),
    )
    repo.append_jsonl_event(
        COLLAB_STREAM,
        {
            "event_type": "collaboration.brief.exported",
            **payload.as_dict(),
        },
    )
    return payload
