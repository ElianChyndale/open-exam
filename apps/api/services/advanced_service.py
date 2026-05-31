"""Offline mock, coach, search, graph, and report services."""

from __future__ import annotations

import json
import re
import sqlite3
from contextlib import closing
from datetime import UTC, date, datetime
from typing import Any

from app.models import stable_id
from services.daily_loop_service import curriculum_summary
from services.practice_service import load_questions


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _mock_runs(repo) -> dict[str, dict[str, Any]]:
    runs: dict[str, dict[str, Any]] = {}
    for event in repo.load_stream_events("mock-run"):
        run = event.get("payload", {}).get("run")
        if run and run.get("run_id"):
            runs[run["run_id"]] = run
    return runs


def _checkpoints(total_minutes: int, total_questions: int) -> list[dict[str, int]]:
    return [
        {
            "question_number": question_number,
            "target_elapsed_seconds": round(total_minutes * 60 * question_number / total_questions),
        }
        for question_number in range(30, total_questions + 1, 30)
    ]


def _pre_mock_brief(repo) -> dict[str, Any]:
    risk_topics = []
    for event in reversed(repo.load_events()):
        if event.source_layer == "question" and event.topic not in risk_topics:
            risk_topics.append(event.topic)
    return {
        "pacing_rule": "Check elapsed time every 30 questions and move on when a question exceeds its budget.",
        "risk_topics": risk_topics[:3],
        "warm_start": "Review the cited weak topics, then solve five short discrimination questions.",
    }


def _post_mock_retro(repo, run_id: str) -> dict[str, Any]:
    answers = _mock_answers(repo, run_id)
    incorrect = [answer for answer in answers if not answer.get("is_correct")]
    return {
        "answered_count": len(answers),
        "incorrect_count": len(incorrect),
        "stop_doing": ["Stop spending beyond the pacing checkpoint on a single question."],
        "next_strategy": "Review captured mistakes, then run one short weak-LOS set before the next mock.",
    }


def create_mock_run(repo, payload: dict[str, Any], source_kind: str = "local") -> dict[str, Any]:
    created_at = _now()
    run = {
        "run_id": stable_id("mock-run", payload.get("session_label", ""), created_at),
        "session_label": payload.get("session_label", "Mock run"),
        "source_kind": source_kind,
        "status": "active",
        "total_minutes": payload.get("total_minutes", 135),
        "total_questions": payload.get("total_questions", 90),
        "elapsed_seconds": 0,
        "answered_count": 0,
        "correct_count": 0,
        "checkpoints": _checkpoints(payload.get("total_minutes", 135), payload.get("total_questions", 90)),
        "pre_mock_brief": _pre_mock_brief(repo),
        "created_at": created_at,
    }
    repo.append_stream_event("mock-run", "mock-run.started", {"run": run})
    return run


def get_mock_run(repo, run_id: str) -> dict[str, Any] | None:
    run = _mock_runs(repo).get(run_id)
    return {**run, "answers": _mock_answers(repo, run_id)} if run else None


def list_mock_runs(repo) -> list[dict[str, Any]]:
    return [get_mock_run(repo, run_id) for run_id in reversed(list(_mock_runs(repo)))]


def _mock_answers(repo, run_id: str) -> list[dict[str, Any]]:
    answers = []
    for event in repo.load_stream_events("mock-run"):
        payload = event.get("payload", {})
        if payload.get("answer", {}).get("run_id") == run_id:
            answers.append(payload["answer"])
        if payload.get("run", {}).get("run_id") == run_id and payload.get("answers"):
            answers.extend(payload["answers"])
    return answers


def update_mock_run_state(repo, run_id: str, action: str, elapsed_seconds: int) -> dict[str, Any] | None:
    run = get_mock_run(repo, run_id)
    if run is None:
        return None
    run = {
        **run,
        "status": {"pause": "paused", "resume": "active", "complete": "completed"}[action],
        "elapsed_seconds": elapsed_seconds,
        "updated_at": _now(),
    }
    if action == "complete":
        run["post_mock_retro"] = _post_mock_retro(repo, run_id)
    repo.append_stream_event("mock-run", f"mock-run.{action}d", {"run": run})
    return run


def submit_mock_answer(repo, run_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    run = get_mock_run(repo, run_id)
    if run is None:
        return None
    mistake_event_id = _capture_mock_mistake(repo, run_id, payload)
    run = {
        **run,
        "answered_count": run.get("answered_count", 0) + 1,
        "correct_count": run.get("correct_count", 0) + int(payload["is_correct"]),
        "updated_at": _now(),
    }
    answer = {**payload, "run_id": run_id, "mistake_event_id": mistake_event_id}
    repo.append_stream_event(
        "mock-run",
        "mock-run.answered",
        {"run": run, "answer": answer},
        source_refs=[mistake_event_id] if mistake_event_id else [],
    )
    return answer


def _capture_mock_mistake(repo, run_id: str, payload: dict[str, Any]) -> str:
    if payload["is_correct"] or not payload.get("prompt") or not payload.get("correct_answer"):
        return ""
    from app.workflows import record_event

    event = record_event(
        repo,
        {
            "topic": payload.get("topic", ""),
            "los": payload.get("los", ""),
            "prompt_or_question": payload.get("prompt", ""),
            "wrong_choice_or_output": payload.get("answer", ""),
            "correct_resolution": payload.get("explanation") or payload.get("correct_answer", ""),
            "error_type": "mock_mistake",
            "confidence": payload.get("confidence", 1),
            "time_spent": payload.get("elapsed_seconds", 0),
            "evidence_refs": [run_id, payload["question_id"]],
            "question_source": "mock_run",
            "source_type": "mock_answer",
        },
        mode="record-mistake",
    )
    return event.event_id or ""


def import_mock_results(repo, payload: dict[str, Any]) -> dict[str, Any]:
    total_questions = payload.get("total_questions") or len(payload.get("answers", []))
    run = create_mock_run(
        repo,
        {
            "session_label": payload.get("session_label", "External mock"),
            "total_minutes": 135,
            "total_questions": max(total_questions, 1),
        },
        source_kind="external_import",
    )
    run = {
        **run,
        "status": "completed",
        "source_name": payload.get("source_name", ""),
        "total_questions": total_questions,
        "answered_count": len(payload.get("answers", [])),
        "correct_count": sum(answer.get("is_correct", False) for answer in payload.get("answers", [])),
        "updated_at": _now(),
    }
    for answer in payload.get("answers", []):
        _capture_mock_mistake(repo, run["run_id"], answer)
    run["post_mock_retro"] = _post_mock_retro(repo, run["run_id"])
    repo.append_stream_event("mock-run", "mock-run.imported", {"run": run, "answers": payload.get("answers", [])})
    return run


def create_coach_brief(repo, payload: dict[str, Any], kind: str = "session-retro") -> dict[str, Any]:
    source_refs = payload.get("source_refs", [])
    if not source_refs:
        raise ValueError("Coach recommendations require evidence references")
    biases = payload.get("biases", [])
    recommendations = ["Review the cited evidence before the next study block."]
    if biases:
        recommendations.append(f"Run one deliberate drill for: {biases[0]}.")
    brief = {
        "brief_id": stable_id("coach", kind, payload.get("summary", ""), ",".join(source_refs), _now()),
        "kind": kind,
        "summary": payload.get("summary", ""),
        "biases": biases,
        "recommendations": recommendations,
        "evidence_refs": source_refs,
        "validated": True,
        "created_at": _now(),
    }
    repo.append_stream_event("coach", f"coach.{kind}", {"brief": brief}, source_refs=source_refs)
    return brief


def coach_briefs(repo) -> list[dict[str, Any]]:
    return [
        event["payload"]["brief"]
        for event in reversed(repo.load_stream_events("coach"))
        if event.get("payload", {}).get("brief")
    ]


def audit_agent_failure(repo, payload: dict[str, Any]) -> dict[str, Any]:
    from app.workflows import record_event

    event = record_event(
        repo,
        {
            "topic": "Agent quality",
            "los": "AGENT.Validation",
            "prompt_or_question": payload.get("summary", ""),
            "wrong_choice_or_output": payload.get("summary", ""),
            "correct_resolution": "Require an evidence-linked correction and validation check before reuse.",
            "error_type": payload.get("risk_kind", "unsupported_claim"),
            "confidence": 4,
            "time_spent": 0,
            "evidence_refs": payload.get("source_refs", []),
            "question_source": "coach_audit",
            "source_type": "agent_output",
        },
        mode="audit-agent",
    )
    return create_coach_brief(
        repo,
        {**payload, "source_refs": [*payload.get("source_refs", []), event.event_id or ""]},
        kind="audit-agent",
    )


def _search_documents(repo) -> list[tuple[str, str, str, str, str]]:
    documents: list[tuple[str, str, str, str, str]] = []
    registry = curriculum_summary(repo)
    for subject in registry["subjects"]:
        for module in subject["modules"]:
            title = f"{subject['subject']} {module['module']} {module['official_module']}"
            body = " ".join(module.get("los", []))
            documents.append((stable_id("search", title), "curriculum", title, body, module["module"]))
    for event in repo.load_events():
        title = f"{event.topic} {event.los}"
        body = f"{event.prompt_or_question} {event.correct_resolution} {event.error_type}"
        documents.append((event.event_id or stable_id("search", title, body), "mistake-card", title, body, event.event_id or ""))
    for question in load_questions(repo):
        if question.get("verification_status") != "verified":
            continue
        title = f"{question.get('topic', '')} {question.get('los', '')}"
        body = f"{question.get('prompt', '')} {question.get('explanation', '')}"
        documents.append((question["question_id"], "verified-question", title, body, question["question_id"]))
    memory_kinds = {
        "patterns": "pattern",
        "strategy": "strategy",
        "validation": "validation",
        "question-errors": "mistake-card",
        "cognitive-bias": "bias",
        "agent-failures": "agent-failure",
    }
    for directory, kind in memory_kinds.items():
        for path in sorted((repo.memory_root / directory).glob("*.md")):
            body = path.read_text(encoding="utf-8")
            documents.append((stable_id("search", str(path)), kind, path.stem, body, str(path.relative_to(repo.root))))
    for path in sorted(repo.vault_root.glob("*/*.md")):
        body = path.read_text(encoding="utf-8")
        documents.append((stable_id("search", str(path)), "curriculum-note", path.stem, body, str(path.relative_to(repo.root))))
    return documents


def search_assets(repo, query: str, limit: int = 20) -> list[dict[str, str]]:
    terms = re.findall(r"[\w-]+", query, flags=re.UNICODE)
    if not terms:
        return []
    with closing(sqlite3.connect(repo.catalog_path)) as connection:
        connection.execute("DELETE FROM search_documents")
        connection.executemany(
            "INSERT INTO search_documents(document_id, kind, title, body, source_ref) VALUES (?, ?, ?, ?, ?)",
            _search_documents(repo),
        )
        rows = connection.execute(
            """
            SELECT document_id, kind, title, snippet(search_documents, 3, '[', ']', '...', 16), source_ref
            FROM search_documents
            WHERE search_documents MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (" OR ".join(f'"{term}"' for term in terms), limit),
        ).fetchall()
    return [
        {"document_id": row[0], "kind": row[1], "title": row[2], "snippet": row[3], "source_ref": row[4]}
        for row in rows
    ]


def knowledge_graph(repo) -> dict[str, list[dict[str, Any]]]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    subject_ids = {}
    for subject_index, subject in enumerate(curriculum_summary(repo)["subjects"]):
        subject_id = stable_id("subject", subject["subject"])
        subject_ids[subject["subject"]] = subject_id
        nodes.append(
            {
                "id": subject_id,
                "label": subject["subject"],
                "source_kind": "official",
                "node_type": "subject",
                "x": subject_index * 260,
                "y": 0,
                "locked": True,
            }
        )
        for module_index, module in enumerate(subject["modules"]):
            module_id = stable_id("module", subject["subject"], module["module"])
            nodes.append(
                {
                    "id": module_id,
                    "label": module["official_module"],
                    "source_kind": "official",
                    "node_type": "module",
                    "x": subject_index * 260,
                    "y": 140 + module_index * 100,
                    "locked": True,
                }
            )
            edges.append(
                {
                    "id": stable_id("edge", subject_id, module_id),
                    "source": subject_id,
                    "target": module_id,
                    "source_kind": "official",
                    "locked": True,
                }
            )
            for los_index, los in enumerate(module.get("los", [])):
                los_id = stable_id("los", subject["subject"], module["module"], los)
                nodes.append(
                    {
                        "id": los_id,
                        "label": los,
                        "source_kind": "official",
                        "node_type": "los",
                        "x": subject_index * 260 + 120,
                        "y": 180 + module_index * 100 + los_index * 42,
                        "locked": True,
                    }
                )
                edges.append(
                    {
                        "id": stable_id("edge", module_id, los_id),
                        "source": module_id,
                        "target": los_id,
                        "source_kind": "official",
                        "locked": True,
                    }
                )
    for event_index, event in enumerate(repo.load_events()):
        node_id = stable_id("evidence", event.event_id or "")
        nodes.append(
            {
                "id": node_id,
                "label": f"{event.topic}: {event.error_type}",
                "source_kind": "evidence",
                "node_type": "mistake",
                "x": event_index * 180,
                "y": 1180,
                "locked": True,
                "notes": event.correct_resolution,
            }
        )
        if event.topic in subject_ids:
            edges.append(
                {
                    "id": stable_id("edge", node_id, subject_ids[event.topic]),
                    "source": node_id,
                    "target": subject_ids[event.topic],
                    "source_kind": "evidence",
                    "label": "weakness",
                    "locked": True,
                }
            )
    for path in sorted((repo.memory_root / "patterns").glob("*.md")):
        pattern_id = stable_id("pattern-node", path.stem)
        nodes.append(
            {
                "id": pattern_id,
                "label": path.stem,
                "source_kind": "evidence",
                "node_type": "pattern",
                "x": 0,
                "y": 1320 + len(nodes) * 10,
                "locked": True,
                "notes": path.read_text(encoding="utf-8"),
            }
        )
    signal_count = 0
    for path in sorted((repo.memory_root / "strategy").glob("*.md")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            lowered = line.lower()
            node_type = "formula" if "formula" in lowered or "公式" in line else "trap" if "trap" in lowered or "陷阱" in line else ""
            if not node_type:
                continue
            nodes.append(
                {
                    "id": stable_id(node_type, str(path), str(line_number)),
                    "label": line.strip("-# >")[:120],
                    "source_kind": "evidence",
                    "node_type": node_type,
                    "x": 240 + signal_count * 30,
                    "y": 1420 + signal_count * 18,
                    "locked": True,
                    "notes": str(path.relative_to(repo.root)),
                }
            )
            signal_count += 1
            if signal_count >= 40:
                break
        if signal_count >= 40:
            break
    overlay = repo.latest_stream_payload("graph-overlay", "graph-overlay.updated") or {"nodes": [], "edges": []}
    return {"nodes": [*nodes, *overlay["nodes"]], "edges": [*edges, *overlay["edges"]]}


def update_graph_overlay(repo, payload: dict[str, Any]) -> dict[str, Any]:
    records = [*payload.get("nodes", []), *payload.get("edges", [])]
    if any(record.get("source_kind") != "personal" for record in records):
        raise ValueError("Only personal graph overlay records are mutable")
    clean = {
        "nodes": [{**node, "locked": False} for node in payload.get("nodes", [])],
        "edges": [{**edge, "locked": False} for edge in payload.get("edges", [])],
    }
    repo.append_stream_event("graph-overlay", "graph-overlay.updated", clean)
    return clean


def weekly_report(repo) -> dict[str, Any]:
    briefs = coach_briefs(repo)
    evidence_refs = sorted({ref for brief in briefs for ref in brief.get("evidence_refs", [])})
    attempts = repo.load_attempt_records()
    mock_runs = list(_mock_runs(repo).values())
    report_id = stable_id("weekly-report", date.today().isoformat(), ",".join(evidence_refs))
    lines = [
        "# OpenExam weekly learner report",
        "",
        f"- Report ID: {report_id}",
        f"- Attempts captured: {len(attempts)}",
        f"- Mock runs: {len(mock_runs)}",
        f"- Validated coach briefs: {len(briefs)}",
        "",
        "## Evidence references",
        *[f"- {ref}" for ref in evidence_refs],
    ]
    return {
        "report_id": report_id,
        "generated_at": _now(),
        "attempt_count": len(attempts),
        "mock_run_count": len(mock_runs),
        "coach_brief_count": len(briefs),
        "evidence_refs": evidence_refs,
        "markdown_content": "\n".join(lines) + "\n",
    }
