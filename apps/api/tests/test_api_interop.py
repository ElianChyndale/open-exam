from __future__ import annotations

import csv
import json
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    _enable_interop(repo.root)
    _seed_interop_fixture(repo.root, wrong_phrase="UNIQUE_WRONG_INTEROP_PHRASE")
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_anki_export_is_confirmed_only_safe_and_registered(client: TestClient, tmp_path: Path) -> None:
    response = client.post("/api/interop/export/anki", json={"profile_id": "p1", "format": "csv", "confirmed_only": True})

    assert response.status_code == 200
    payload = response.json()
    artifact = payload["artifact"]
    assert artifact["artifact_type"] == "anki_csv"
    assert artifact["safe_mode"] is True
    assert artifact["size_bytes"] > 0
    assert not Path(artifact["file_path"]).is_absolute()

    csv_path = tmp_path / artifact["file_path"]
    content = csv_path.read_text(encoding="utf-8")
    assert "asset-confirmed-1" in content
    assert "asset-draft-1" not in content
    assert "UNIQUE_WRONG_INTEROP_PHRASE" not in content
    for forbidden in ["wrong_choice_or_output", "wrong_formula", "wrong_reasoning", "answer_text", "selected_choice"]:
        assert forbidden not in content
    assert "openexam_id,note_type,front,back,tags,source_refs,goal_id,topic_ids,quality_status,validation_status,created_at" in content

    preview = client.post("/api/interop/import/anki/preview", json={"profile_id": "p1", "file_path": artifact["file_path"]})
    assert preview.status_code == 200
    preview_payload = preview.json()
    assert preview_payload["detected_items"] >= 1
    assert preview_payload["duplicates"] >= 1
    assert preview_payload["will_auto_confirm"] is False

    registry = client.get("/api/interop/artifacts")
    assert registry.status_code == 200
    assert any(item["artifact_id"] == artifact["artifact_id"] for item in registry.json()["artifacts"])


def test_anki_import_preview_and_commit_create_draft_candidates_with_duplicate_detection(client: TestClient, tmp_path: Path) -> None:
    import_path = tmp_path / ".system" / "memory" / "interop" / "imports" / "anki_external.csv"
    import_path.parent.mkdir(parents=True, exist_ok=True)
    with import_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "openexam_id",
                "note_type",
                "front",
                "back",
                "tags",
                "source_refs",
                "goal_id",
                "topic_ids",
                "quality_status",
                "validation_status",
                "created_at",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "openexam_id": "external-card-1",
                "note_type": "Concept recall",
                "front": "Recall the after-tax debt cost rule.",
                "back": "Use after-tax cost of debt in WACC.",
                "tags": "imported wacc",
                "source_refs": "external-deck.csv#row=2",
                "goal_id": "goal-1",
                "topic_ids": "topic-wacc",
                "quality_status": "external",
                "validation_status": "confirmed",
                "created_at": "2026-06-03T00:00:00+00:00",
            }
        )
        writer.writerow(
            {
                "openexam_id": "external-card-1",
                "note_type": "Concept recall",
                "front": "Recall the after-tax debt cost rule.",
                "back": "Use after-tax cost of debt in WACC.",
                "tags": "duplicate",
                "source_refs": "external-deck.csv#row=3",
                "goal_id": "goal-1",
                "topic_ids": "topic-wacc",
                "quality_status": "external",
                "validation_status": "confirmed",
                "created_at": "2026-06-03T00:00:00+00:00",
            }
        )

    preview = client.post(
        "/api/interop/import/anki/preview",
        json={"profile_id": "p1", "file_path": ".system/memory/interop/imports/anki_external.csv"},
    )

    assert preview.status_code == 200
    payload = preview.json()
    assert payload["detected_items"] == 2
    assert payload["duplicates"] == 1
    assert payload["will_auto_confirm"] is False
    assert payload["proposed_records"][0]["validation_status"] in {"draft", "needs_review"}
    assert payload["proposed_records"][0]["source_refs"]

    commit = client.post("/api/interop/import/anki/commit", json={"preview_id": payload["preview_id"]})
    assert commit.status_code == 200
    committed = commit.json()
    assert committed["committed_count"] == 1
    created_asset = tmp_path / ".system" / "memory" / "review" / "asset-candidates" / f"{committed['records'][0]['asset_id']}.json"
    assert created_asset.exists()
    asset_payload = json.loads(created_asset.read_text(encoding="utf-8"))
    assert asset_payload["validation_status"] in {"draft", "needs_review"}
    assert asset_payload["source_refs"][0].startswith("anki_import:")


def test_anki_import_duplicate_detection_normalizes_case_spacing_and_punctuation(client: TestClient, tmp_path: Path) -> None:
    import_path = tmp_path / ".system" / "memory" / "interop" / "imports" / "anki_normalized_duplicate.csv"
    import_path.parent.mkdir(parents=True, exist_ok=True)
    with import_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "openexam_id",
                "note_type",
                "front",
                "back",
                "tags",
                "source_refs",
                "goal_id",
                "topic_ids",
                "quality_status",
                "validation_status",
                "created_at",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "openexam_id": "external-normalized-duplicate",
                "note_type": "Concept recall",
                "front": "after tax   debt COST in wacc",
                "back": "use after tax cost of debt in WACC",
                "tags": "normalized",
                "source_refs": "external-deck.csv#row=2",
                "goal_id": "goal-1",
                "topic_ids": "topic-wacc",
                "quality_status": "external",
                "validation_status": "confirmed",
                "created_at": "2026-06-03T00:00:00+00:00",
            }
        )

    preview = client.post(
        "/api/interop/import/anki/preview",
        json={"profile_id": "p1", "file_path": ".system/memory/interop/imports/anki_normalized_duplicate.csv"},
    )

    assert preview.status_code == 200
    payload = preview.json()
    assert payload["detected_items"] == 1
    assert payload["duplicates"] == 1
    assert payload["proposed_records"] == []


def test_markdown_export_zip_and_import_preview_are_safe_draft_round_trip(client: TestClient, tmp_path: Path) -> None:
    export = client.post("/api/interop/export/markdown", json={"profile_id": "p1", "confirmed_only": True})

    assert export.status_code == 200
    artifact = export.json()["artifact"]
    assert artifact["artifact_type"] == "markdown_zip"
    zip_path = tmp_path / artifact["file_path"]
    assert zip_path.exists()
    payload_bytes = zip_path.read_bytes()
    assert b"UNIQUE_WRONG_INTEROP_PHRASE" not in payload_bytes
    assert b"wrong_choice_or_output" not in payload_bytes

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        assert "OpenExam-Export/README.md" in names
        assert any(name.startswith("OpenExam-Export/Assets/") and name.endswith(".md") for name in names)
        note_name = next(name for name in names if name.startswith("OpenExam-Export/Assets/") and name.endswith(".md"))
        note_text = archive.read(note_name).decode("utf-8")
        assert note_text.startswith("---\n")
        assert "openexam_id:" in note_text
        assert "source_refs:" in note_text
        assert "UNIQUE_WRONG_INTEROP_PHRASE" not in note_text

    markdown_path = tmp_path / ".system" / "memory" / "interop" / "imports" / "external_note.md"
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(
        """---
openexam_id: external-md-1
type: concept
goal_id: goal-1
validation_status: confirmed
quality_status: external
source_refs:
  - obsidian://vault/Finance.md#WACC
tags:
  - wacc
---
# WACC imported note

Correct rule: Use after-tax cost of debt in WACC.
""",
        encoding="utf-8",
    )
    preview = client.post(
        "/api/interop/import/markdown/preview",
        json={"profile_id": "p1", "file_path": ".system/memory/interop/imports/external_note.md"},
    )
    assert preview.status_code == 200
    preview_payload = preview.json()
    assert preview_payload["detected_items"] == 1
    assert preview_payload["will_auto_confirm"] is False
    assert preview_payload["proposed_records"][0]["validation_status"] in {"draft", "needs_review"}
    assert any("external_note.md" in ref for ref in preview_payload["proposed_records"][0]["source_refs"])


def test_calendar_and_learning_record_exports_are_local_safe_xapi_style(client: TestClient, tmp_path: Path) -> None:
    calendar = client.post(
        "/api/interop/export/calendar",
        json={"profile_id": "p1", "plan_id": "plan-1", "start_datetime": "2026-06-03T09:00:00+08:00", "timezone": "Asia/Shanghai"},
    )
    assert calendar.status_code == 200
    ics_path = tmp_path / calendar.json()["artifact"]["file_path"]
    ics_text = ics_path.read_text(encoding="utf-8")
    assert "BEGIN:VCALENDAR" in ics_text
    assert "SUMMARY:Review confirmed WACC rules" in ics_text
    assert "/review/lab" in ics_text
    assert "goal-1" in ics_text

    records = client.post("/api/interop/export/learning-records", json={"profile_id": "p1", "safe_mode": True})
    assert records.status_code == 200
    json_path = tmp_path / records.json()["artifact"]["file_path"]
    statements = json.loads(json_path.read_text(encoding="utf-8"))
    assert statements
    assert {"actor", "verb", "object", "context", "timestamp"}.issubset(statements[0])
    payload_text = json.dumps(statements, ensure_ascii=False)
    assert "UNIQUE_WRONG_INTEROP_PHRASE" not in payload_text
    assert "wrong_choice_or_output" not in payload_text
    assert "answer_text" not in payload_text


def test_interop_privacy_report_and_data_governance_inventory_include_artifacts(client: TestClient, tmp_path: Path) -> None:
    export = client.post("/api/interop/export/anki", json={"profile_id": "p1"})
    assert export.status_code == 200

    privacy = client.get("/api/interop/privacy-report")
    assert privacy.status_code == 200
    privacy_payload = privacy.json()
    assert privacy_payload["safe_mode_default"] is True
    assert "wrong_choice_or_output" in privacy_payload["redacted_fields"]
    assert privacy_payload["artifact_count"] >= 1

    inventory = client.get("/api/data-governance/inventory")
    assert inventory.status_code == 200
    categories = {item["category"]: item for item in inventory.json()["items"]}
    assert "interop_artifacts" in categories
    assert categories["interop_artifacts"]["record_count"] >= 1

    backup = client.post("/api/data-governance/export", json={"mode": "safe", "categories": ["interop_artifacts"]})
    assert backup.status_code == 200
    with zipfile.ZipFile(tmp_path / backup.json()["snapshot"]["file_path"]) as archive:
        assert "data/interop_artifacts.json" in archive.namelist()


def _enable_interop(repo_root: Path) -> None:
    config_path = repo_root / ".system" / "config" / "features.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        "\n".join(
            [
                "review_lab_enabled: true",
                "review_asset_ingestion_enabled: true",
                "review_asset_manual_confirm_required: true",
                "data_governance_enabled: true",
                "safe_export_enabled: true",
                "full_export_enabled: true",
                "backup_restore_enabled: true",
                "privacy_redaction_enabled: true",
                "goal_profiles_enabled: true",
                "course_packs_enabled: true",
                "study_planner_enabled: true",
                "interop_enabled: true",
                "anki_interop_enabled: true",
                "markdown_interop_enabled: true",
                "calendar_export_enabled: true",
                "learning_record_export_enabled: true",
                "interop_safe_mode_enabled: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _seed_interop_fixture(repo_root: Path, *, wrong_phrase: str) -> None:
    asset_root = repo_root / ".system" / "memory" / "review" / "asset-candidates"
    asset_root.mkdir(parents=True, exist_ok=True)
    (asset_root / "asset-confirmed-1.json").write_text(
        json.dumps(
            {
                "asset_id": "asset-confirmed-1",
                "asset_type": "decision_rule",
                "profile_id": "p1",
                "subject": "Corporate Issuers",
                "module": "Cost of Capital",
                "los": "CI.WACC.1",
                "title": "After-tax debt cost in WACC",
                "trigger": "When using debt cost in WACC",
                "correct_rule": "Use after-tax cost of debt in WACC.",
                "source_refs": ["local-note#WACC"],
                "syllabus_topic_id": "topic-wacc",
                "resource_quality_status": "trusted",
                "validation_status": "confirmed",
                "created_from": "manual",
                "wrong_choice_or_output": wrong_phrase,
                "wrong_reasoning": wrong_phrase,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (asset_root / "asset-draft-1.json").write_text(
        json.dumps(
            {
                "asset_id": "asset-draft-1",
                "asset_type": "definition",
                "profile_id": "p1",
                "title": "Draft beta note",
                "trigger": "Draft prompt",
                "correct_rule": "Draft answer should not export by default.",
                "source_refs": ["draft-note#1"],
                "validation_status": "draft",
                "wrong_choice_or_output": wrong_phrase,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    goals_root = repo_root / ".system" / "memory" / "goals" / "profiles"
    goals_root.mkdir(parents=True, exist_ok=True)
    (goals_root / "goal-1.json").write_text(
        json.dumps({"goal_id": "goal-1", "profile_id": "p1", "title": "CFA safe interop goal", "active": True}, ensure_ascii=False),
        encoding="utf-8",
    )

    plans_root = repo_root / ".system" / "memory" / "study-planner" / "plans"
    plans_root.mkdir(parents=True, exist_ok=True)
    (plans_root / "plan-1.json").write_text(
        json.dumps(
            {
                "plan_id": "plan-1",
                "profile_id": "p1",
                "plan_date": "2026-06-03",
                "energy_mode": "normal",
                "available_minutes": 90,
                "generated_at": "2026-06-03T00:00:00+00:00",
                "status": "active",
                "blocks": [
                    {
                        "block_id": "block-1",
                        "plan_id": "plan-1",
                        "block_type": "review_lab",
                        "title": "Review confirmed WACC rules",
                        "description": "Recall the confirmed WACC decision rule.",
                        "target_minutes": 30,
                        "priority": 9.5,
                        "launch_route": "/review/lab",
                        "due_reason": "Confirmed asset due for recall.",
                        "linked_asset_ids": ["asset-confirmed-1"],
                        "linked_topic_ids": ["topic-wacc"],
                        "source_refs": ["local-note#WACC"],
                        "goal_id": "goal-1",
                        "status": "pending",
                    }
                ],
                "summary": {"block_count": 1},
                "source_signals": {"goal_id": "goal-1"},
                "recommended_next_actions": [],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    attempt_root = repo_root / ".system" / "events" / "attempt"
    attempt_root.mkdir(parents=True, exist_ok=True)
    (attempt_root / "attempt-events.jsonl").write_text(
        json.dumps(
            {
                "event_id": "attempt-interop-1",
                "profile_id": "p1",
                "topic": "Corporate Issuers",
                "asset_id": "asset-confirmed-1",
                "correct_resolution": "Use after-tax cost of debt in WACC.",
                "wrong_choice_or_output": wrong_phrase,
                "answer_text": wrong_phrase,
                "is_correct": False,
                "created_at": "2026-06-03T00:00:00+00:00",
                "source_refs": ["local-note#WACC"],
                "goal_id": "goal-1",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
