from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime, UTC
import json
from pathlib import Path
from typing import Any

from app.models import stable_id
from app.storage import Repository
from app.workflows.core import archive_today_todo, normalize_deadline, normalize_todo_tasks
from learning_records import EventEnvelopeV2


DAILY_REVIEW_TEXT = "完成 Daily Review"
DAILY_REVIEW_DEADLINE = "20:00"
DAILY_REVIEW_ALIASES = {DAILY_REVIEW_TEXT.lower(), "完成今日复习资料", "daily review"}


class RevisionConflict(RuntimeError):
    def __init__(self, expected: int, actual: int) -> None:
        super().__init__(f"Todo revision conflict: expected {expected}, actual {actual}.")
        self.expected = expected
        self.actual = actual


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _task_id(plan_date: str, text: str) -> str:
    return stable_id("todo", plan_date, text.strip().lower())


def _new_task(
    *,
    plan_date: str,
    text: str,
    deadline: str = "",
    progress: int = 0,
    status: str = "pending",
    source: str = "manual",
    task_id: str = "",
) -> dict[str, Any]:
    timestamp = _now()
    normalized_progress = max(0, min(100, int(progress)))
    normalized_status = "completed" if status == "completed" or normalized_progress == 100 else "pending"
    return {
        "task_id": task_id or _task_id(plan_date, text),
        "text": text.strip(),
        "deadline": normalize_deadline(deadline),
        "progress": 100 if normalized_status == "completed" else normalized_progress,
        "status": normalized_status,
        "source": source,
        "created_at": timestamp,
        "updated_at": timestamp,
    }


def _ensure_daily_review(tasks: list[dict[str, Any]], plan_date: str) -> list[dict[str, Any]]:
    daily: dict[str, Any] | None = None
    regular: list[dict[str, Any]] = []
    for task in tasks:
        if str(task.get("text", "")).strip().lower() in DAILY_REVIEW_ALIASES:
            daily = deepcopy(task)
        else:
            regular.append(deepcopy(task))
    if daily is None:
        daily = _new_task(plan_date=plan_date, text=DAILY_REVIEW_TEXT, deadline=DAILY_REVIEW_DEADLINE, source="system")
        daily["created_at"] = ""
        daily["updated_at"] = ""
    daily["task_id"] = _task_id(plan_date, DAILY_REVIEW_TEXT)
    daily["text"] = DAILY_REVIEW_TEXT
    daily["deadline"] = DAILY_REVIEW_DEADLINE
    daily["source"] = "system"
    for index, task in enumerate(regular):
        if str(task.get("deadline", "")) > DAILY_REVIEW_DEADLINE:
            return [*regular[:index], daily, *regular[index:]]
    return [*regular, daily]


def _empty_state(plan_date: str) -> dict[str, Any]:
    return {
        "date": plan_date,
        "title": "今日 Todo",
        "focus": "完成今天最重要的任务",
        "time_blocks": [],
        "tasks": _ensure_daily_review([], plan_date),
        "revision": 0,
        "updated_at": "",
    }


def _reduce(events: list[dict[str, Any]], plan_date: str) -> dict[str, Any]:
    state = _empty_state(plan_date)
    for envelope in events:
        payload = envelope.get("payload", {})
        if payload.get("date") != plan_date:
            continue
        event_type = envelope.get("event_type")
        if event_type == "todo.list.replaced":
            state = {
                "date": plan_date,
                "title": payload.get("title") or "今日 Todo",
                "focus": payload.get("focus") or "完成今天最重要的任务",
                "time_blocks": list(payload.get("time_blocks") or []),
                "tasks": deepcopy(payload.get("tasks") or []),
                "revision": int(payload["revision"]),
                "updated_at": envelope.get("occurred_at", ""),
            }
        elif event_type == "todo.task.added":
            state["tasks"].append(deepcopy(payload["task"]))
        elif event_type == "todo.task.updated":
            for index, task in enumerate(state["tasks"]):
                if task["task_id"] == payload["task"]["task_id"]:
                    state["tasks"][index] = deepcopy(payload["task"])
                    break
        elif event_type == "todo.task.deleted":
            state["tasks"] = [task for task in state["tasks"] if task["task_id"] != payload["task_id"]]
        else:
            continue
        state["revision"] = int(payload["revision"])
        state["updated_at"] = envelope.get("occurred_at", "")
        state["tasks"] = _ensure_daily_review(state["tasks"], plan_date)
    return state


def rollover_todo(repo: Repository) -> dict[str, Any]:
    """Auto-rollover if today > latest todo date. Carries unfinished tasks forward."""
    today = date.today().isoformat()
    events = repo.load_jsonl_events("todo")
    if not events:
        return _empty_state(today)

    latest_date = str(events[-1].get("payload", {}).get("date", ""))
    if latest_date >= today:
        # Already current — return today's state as-is
        return get_todo(repo, plan_date=today) if latest_date == today else _reduce(events, latest_date)

    # Stale — archive old projection and carry pending tasks forward
    old_state = _reduce(events, latest_date)
    _archive_projection(repo, old_state["date"])

    pending = [
        t for t in old_state["tasks"]
        if t["status"] != "completed"
        and str(t.get("text", "")).strip().lower() not in DAILY_REVIEW_ALIASES
    ]
    new_tasks = [
        _new_task(
            plan_date=today,
            text=t["text"],
            deadline=t.get("deadline", ""),
            progress=t["progress"],
            source="rollover",
        )
        for t in pending
    ]
    return _append(
        repo,
        "todo.list.replaced",
        {
            "date": today,
            "title": "今日 Todo",
            "focus": "完成今天最重要的任务",
            "time_blocks": [],
            "tasks": new_tasks,
            "revision": 1,
            "evidence_refs": [],
        },
    )


def get_todo(repo: Repository, plan_date: str = "") -> dict[str, Any]:
    events = repo.load_jsonl_events("todo")
    if not plan_date:
        if events:
            latest_date = str(events[-1].get("payload", {}).get("date", ""))
            if latest_date < date.today().isoformat():
                return rollover_todo(repo)
        plan_date = date.today().isoformat()
    return _reduce(events, plan_date)


def _assert_revision(state: dict[str, Any], expected_revision: int) -> None:
    if expected_revision != state["revision"]:
        raise RevisionConflict(expected_revision, state["revision"])


def _state_for_task(repo: Repository, task_id: str) -> dict[str, Any]:
    events = repo.load_jsonl_events("todo")
    seen_dates: list[str] = []
    for envelope in events:
        event_date = str(envelope.get("payload", {}).get("date", ""))
        if event_date and event_date not in seen_dates:
            seen_dates.append(event_date)
    for plan_date in reversed(seen_dates):
        state = get_todo(repo, plan_date=plan_date)
        if any(task["task_id"] == task_id for task in state["tasks"]):
            return state
    return get_todo(repo)


def _append(repo: Repository, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    envelope = EventEnvelopeV2.create(
        event_type=event_type,
        source_layer="todo",
        payload=payload,
        evidence_refs=list(payload.get("evidence_refs") or []),
        provenance={"projection": "CFA_tier1/dashboard/today_todo.md"},
        consent_scope=["local_storage"],
        idempotency_key=f"{event_type}:{payload['date']}:{payload['revision']}:{payload.get('task_id', '')}",
    )
    repo.append_jsonl_event("todo", envelope.as_dict())
    state = get_todo(repo, plan_date=payload["date"])
    project_todo(repo, state)
    return state


def _archive_projection(repo: Repository, archive_date: str) -> Path | None:
    projection = repo.obsidian_root / "today_todo.md"
    if not projection.exists() or not projection.read_text(encoding="utf-8").strip():
        return None
    archive_root = repo.schedule_root / "todo_archive"
    archive_root.mkdir(parents=True, exist_ok=True)
    path = archive_root / f"{archive_date}-todo.md"
    counter = 2
    while path.exists():
        path = archive_root / f"{archive_date}-todo-{counter}.md"
        counter += 1
    path.write_text(projection.read_text(encoding="utf-8"), encoding="utf-8")
    return path


def render_todo_projection(state: dict[str, Any]) -> str:
    lines = [
        "---",
        f"date: {state['date']}",
        f"focus: {state['focus']}",
        f"revision: {state['revision']}",
        "status: active",
        "---",
        "",
        f"# {state['title']}",
        "",
        f"> Focus: {state['focus']}",
        "",
        "## Tasks",
    ]
    for task in state["tasks"]:
        mark = "x" if task["status"] == "completed" else " "
        suffix = f"（deadline: {task['deadline']}）" if task.get("deadline") else ""
        progress = f" [{task['progress']}%]" if task.get("progress") not in {0, 100} else ""
        lines.append(f"- [{mark}] {task['text']}{suffix}{progress}")
    if state["time_blocks"]:
        lines.extend(["", "## Time Blocks", *[f"- {block}" for block in state["time_blocks"]]])
    lines.extend(["", "## Review", "- 完成了什么：", "- 卡住或调整：", "- 明天保留："])
    return "\n".join(lines).strip() + "\n"


def project_todo(repo: Repository, state: dict[str, Any]) -> Path:
    snapshot_root = repo.memory_root / "todo"
    snapshot_root.mkdir(parents=True, exist_ok=True)
    body = json.dumps(state, ensure_ascii=False, indent=2) + "\n"
    (snapshot_root / "current.json").write_text(body, encoding="utf-8")
    snapshots = snapshot_root / "snapshots"
    snapshots.mkdir(parents=True, exist_ok=True)
    (snapshots / f"{state['date']}.json").write_text(body, encoding="utf-8")
    path = repo.obsidian_root / "today_todo.md"
    repo.write_markdown(path, render_todo_projection(state), "todo_projection", f"todo-{state['date']}")
    return path


def replace_todo(repo: Repository, payload: dict[str, Any]) -> dict[str, Any]:
    plan_date = str(payload.get("date") or date.today().isoformat())
    previous_events = repo.load_jsonl_events("todo")
    previous = get_todo(repo) if previous_events else None
    if previous and previous["date"] != plan_date:
        _archive_projection(repo, previous["date"])
    normalized = normalize_todo_tasks(payload.get("tasks", []))
    tasks = [
        _new_task(plan_date=plan_date, text=item["task"], deadline=item.get("deadline", ""), source=str(payload.get("source") or "manual"))
        for item in normalized
    ]
    tasks = _ensure_daily_review(tasks, plan_date)
    revision = (previous["revision"] if previous and previous["date"] == plan_date else 0) + 1
    return _append(
        repo,
        "todo.list.replaced",
        {
            "date": plan_date,
            "title": payload.get("title") or "今日 Todo",
            "focus": payload.get("focus") or payload.get("theme") or "完成今天最重要的任务",
            "time_blocks": list(payload.get("time_blocks") or []),
            "tasks": tasks,
            "revision": revision,
            "evidence_refs": list(payload.get("evidence_refs") or []),
        },
    )


def create_todo_task(
    repo: Repository,
    *,
    text: str,
    deadline: str = "",
    progress: int = 0,
    expected_revision: int,
    plan_date: str = "",
    source: str = "manual",
) -> dict[str, Any]:
    state = get_todo(repo, plan_date)
    _assert_revision(state, expected_revision)
    if any(task["text"].strip().lower() == text.strip().lower() for task in state["tasks"]):
        return state
    task = _new_task(plan_date=state["date"], text=text, deadline=deadline, progress=progress, source=source)
    return _append(repo, "todo.task.added", {"date": state["date"], "revision": state["revision"] + 1, "task": task})


def update_todo_task(repo: Repository, task_id: str, patch: dict[str, Any], expected_revision: int) -> dict[str, Any]:
    state = _state_for_task(repo, task_id)
    _assert_revision(state, expected_revision)
    task = next((deepcopy(item) for item in state["tasks"] if item["task_id"] == task_id), None)
    if task is None:
        raise KeyError(task_id)
    if "text" in patch and str(patch["text"]).strip():
        task["text"] = str(patch["text"]).strip()
    if "deadline" in patch:
        task["deadline"] = normalize_deadline(patch["deadline"])
    if "progress" in patch:
        task["progress"] = max(0, min(100, int(patch["progress"])))
    if "status" in patch:
        task["status"] = "completed" if patch["status"] == "completed" else "pending"
    if task["progress"] == 100:
        task["status"] = "completed"
    if task["status"] == "completed":
        task["progress"] = 100
    task["updated_at"] = _now()
    return _append(repo, "todo.task.updated", {"date": state["date"], "revision": state["revision"] + 1, "task": task})


def toggle_todo_task(repo: Repository, task_id: str, expected_revision: int) -> dict[str, Any]:
    state = _state_for_task(repo, task_id)
    task = next((item for item in state["tasks"] if item["task_id"] == task_id), None)
    if task is None:
        raise KeyError(task_id)
    status = "pending" if task["status"] == "completed" else "completed"
    return update_todo_task(repo, task_id, {"status": status, "progress": 0 if status == "pending" else 100}, expected_revision)


def delete_todo_task(repo: Repository, task_id: str, expected_revision: int) -> dict[str, Any]:
    state = _state_for_task(repo, task_id)
    _assert_revision(state, expected_revision)
    if not any(task["task_id"] == task_id for task in state["tasks"]):
        raise KeyError(task_id)
    return _append(repo, "todo.task.deleted", {"date": state["date"], "revision": state["revision"] + 1, "task_id": task_id})


def import_study_plan_tasks(repo: Repository, plan: dict[str, Any], *, confirmed: bool) -> dict[str, Any]:
    if not confirmed:
        raise ValueError("Study-plan import requires explicit confirmation.")
    state = get_todo(repo)
    for tier in ("high_energy_tasks", "moderate_energy_tasks", "low_energy_tasks"):
        for item in plan.get(tier, []):
            text = str(item.get("description") or item.get("desc") or "").strip()
            if text:
                state = create_todo_task(
                    repo,
                    text=text,
                    expected_revision=state["revision"],
                    plan_date=state["date"],
                    source=f"study-plan:{plan.get('plan_id', '')}",
                )
    return state


def list_todo_archives(repo: Repository) -> list[str]:
    archive_root = repo.schedule_root / "todo_archive"
    return [str(path.relative_to(repo.root)) for path in sorted(archive_root.glob("*-todo*.md"), reverse=True)]


def write_todo(repo: Repository, payload: dict[str, Any]) -> Path:
    if not repo.load_jsonl_events("todo"):
        archive_today_todo(repo, str(payload.get("date") or date.today().isoformat()))
    replace_todo(repo, payload)
    return repo.obsidian_root / "today_todo.md"
