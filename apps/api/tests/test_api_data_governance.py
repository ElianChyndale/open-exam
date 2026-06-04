from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app
from study_science.data_governance import FORBIDDEN_SAFE_PAYLOAD_KEYS, is_forbidden_key, sanitize_payload
from study_science.focus_session import FocusStep
from study_science.interop import InteropService
from study_science.knowledge_graph import strip_graph_payload
from study_science.tutor import sanitize_public


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    _enable_data_governance(repo.root)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_inventory_empty_state_reports_governed_categories(client: TestClient) -> None:
    response = client.get("/api/data-governance/inventory")

    assert response.status_code == 200
    payload = response.json()
    categories = {item["category"]: item for item in payload["items"]}
    for category in [
        "review_lab",
        "assets",
        "source_documents",
        "formulas",
        "language_dictionaries",
        "lexical_memory",
        "assessments",
        "learning_analytics",
        "study_plans",
        "knowledge_graph",
        "mission_control",
        "todos",
        "feature_flags",
    ]:
        assert category in categories
        assert "record_count" in categories[category]
        assert "size_bytes" in categories[category]
        assert categories[category]["path"] is None or not Path(categories[category]["path"]).is_absolute()
    assert payload["summary"]["category_count"] >= 19


def test_safe_export_redacts_raw_diagnostics_and_restores_dry_run(client: TestClient, tmp_path: Path) -> None:
    wrong_phrase = "UNIQUE_WRONG_BACKUP_PHRASE"
    _seed_governance_fixture(tmp_path, wrong_phrase=wrong_phrase)

    export = client.post("/api/data-governance/export", json={"profile_id": "p1", "mode": "safe"})

    assert export.status_code == 200
    payload = export.json()
    assert payload["snapshot"]["mode"] == "safe"
    assert payload["redaction_report"]["fields_removed_count"] >= 5
    export_path = tmp_path / payload["snapshot"]["file_path"]
    assert export_path.exists()
    assert not Path(payload["snapshot"]["file_path"]).is_absolute()

    payload_bytes = export_path.read_bytes()
    for forbidden in [
        b"wrong_choice_or_output",
        b"wrong_formula",
        b"wrong_reasoning",
        b"answer_text",
        b"selected_choice",
        b"internal_secret",
        wrong_phrase.encode(),
    ]:
        assert forbidden not in payload_bytes

    with zipfile.ZipFile(export_path) as archive:
        names = set(archive.namelist())
        assert {"manifest.json", "inventory.json", "checksums.json", "README_RESTORE.md"}.issubset(names)
        manifest = json.loads(archive.read("manifest.json"))
        checksums = json.loads(archive.read("checksums.json"))
        assert manifest["export_mode"] == "safe"
        assert manifest["redaction_policy"]["include_raw_diagnostics"] is False
        assert "data/assets.json" in checksums

    dry_run = client.post("/api/data-governance/restore/dry-run", json={"profile_id": "p1", "file_path": payload["snapshot"]["file_path"]})
    assert dry_run.status_code == 200
    dry_payload = dry_run.json()
    assert dry_payload["valid"] is True
    assert dry_payload["planned_changes"]
    assert dry_payload["checksum_valid"] is True


def test_full_export_requires_explicit_raw_diagnostics_flag(client: TestClient, tmp_path: Path) -> None:
    _seed_governance_fixture(tmp_path, wrong_phrase="UNIQUE_FULL_EXPORT_PHRASE")

    blocked = client.post("/api/data-governance/export", json={"mode": "full"})
    assert blocked.status_code == 400
    assert "include_raw_diagnostics" in blocked.text

    allowed = client.post("/api/data-governance/export", json={"mode": "full", "include_raw_diagnostics": True})
    assert allowed.status_code == 200
    payload = allowed.json()
    assert payload["snapshot"]["mode"] == "full"
    assert payload["warning"]["includes_raw_diagnostics"] is True
    export_path = tmp_path / payload["snapshot"]["file_path"]
    assert b"UNIQUE_FULL_EXPORT_PHRASE" in export_path.read_bytes()


def test_canonical_correct_only_sanitizer_is_consistent_across_services(tmp_path: Path) -> None:
    secret = "UNIQUE_CANONICAL_SANITIZER_SECRET"
    forbidden_payload = {
        key: secret
        for key in [
            "wrong_choice_or_output",
            "wrong_formula",
            "wrong_reasoning",
            "wrong_answer",
            "wrong_output",
            "answer_text",
            "selected_choice",
            "selected_answer",
            "raw_response",
            "common_wrong_path",
            "internal_secret",
        ]
    }
    forbidden_payload["diagnostics"] = {"raw": secret}
    forbidden_payload["internal_notes"] = secret
    payload = {
        "correct_answer": "Use after-tax cost of debt in WACC.",
        "safe_sentence": f"Correct-only text must not echo {secret}.",
        "nested": {"keep": "source-backed", **forbidden_payload},
    }

    assert FORBIDDEN_SAFE_PAYLOAD_KEYS.issuperset(set(forbidden_payload) - {"internal_notes"})
    assert is_forbidden_key("internal_runtime_trace")
    assert is_forbidden_key("internal_notes")
    assert is_forbidden_key("diagnostics")

    sanitized, report = sanitize_payload(payload)
    assert report["fields_removed_count"] >= len(forbidden_payload)

    interop_clean, _ = InteropService(tmp_path)._redact_payload(payload)
    focus_step = FocusStep(
        step_id="step-safe",
        focus_id="focus-safe",
        step_type="review_lab",
        title="Safe step",
        description="Correct-only",
        target_minutes=5,
        embedded_payload=payload,
    ).as_dict()
    service_payloads = [
        sanitized,
        sanitize_public(payload),
        strip_graph_payload(payload),
        interop_clean,
        focus_step,
    ]
    for service_payload in service_payloads:
        body = json.dumps(service_payload, ensure_ascii=False)
        assert secret not in body
        for key in FORBIDDEN_SAFE_PAYLOAD_KEYS:
            assert key not in body
        assert "internal_runtime_trace" not in body


def test_canonical_sanitizer_redacts_absolute_local_paths() -> None:
    payload = {
        "source_refs": [r"C:\Users\Administrator\secret\absolute-note.md"],
        "note": r"Use the repository copy, not C:\Users\Administrator\secret\absolute-note.md.",
        "correct_answer": "Repository-relative refs are safe.",
    }

    sanitized, report = sanitize_payload(payload)
    body = json.dumps(sanitized, ensure_ascii=False)

    assert "C:\\Users\\Administrator" not in body
    assert "absolute-note.md" not in body
    assert "[local-path]" in body
    assert report["local_path_redactions_count"] >= 2


def test_restore_dry_run_rejects_path_traversal(client: TestClient) -> None:
    response = client.post(
        "/api/data-governance/restore/dry-run",
        json={"profile_id": "p1", "file_path": r"..\..\outside.zip"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["valid"] is False
    assert any("inside repository root" in error for error in payload["errors"])


def test_category_export_restore_corrupt_reset_and_rollback_controls(client: TestClient, tmp_path: Path) -> None:
    _seed_governance_fixture(tmp_path, wrong_phrase="UNIQUE_CATEGORY_EXPORT_PHRASE")

    category_export = client.post("/api/data-governance/export", json={"mode": "category", "categories": ["assets", "feature_flags"]})
    assert category_export.status_code == 200
    export_path = tmp_path / category_export.json()["snapshot"]["file_path"]
    with zipfile.ZipFile(export_path) as archive:
        data_files = {name for name in archive.namelist() if name.startswith("data/")}
    assert data_files == {"data/assets.json", "data/feature_flags.json"}

    corrupt = tmp_path / ".system" / "memory" / "backups" / "corrupt.zip"
    corrupt.parent.mkdir(parents=True, exist_ok=True)
    corrupt.write_text("not a zip", encoding="utf-8")
    corrupt_dry_run = client.post("/api/data-governance/restore/dry-run", json={"file_path": ".system/memory/backups/corrupt.zip"})
    assert corrupt_dry_run.status_code == 200
    assert corrupt_dry_run.json()["valid"] is False

    blocked_reset = client.post("/api/data-governance/reset", json={"category": "knowledge_graph", "confirmation": "RESET"})
    assert blocked_reset.status_code == 400
    assert (tmp_path / ".system" / "memory" / "knowledge-graph" / "graph.json").exists()

    reset = client.post("/api/data-governance/reset", json={"category": "knowledge_graph", "confirmation": "RESET knowledge_graph"})
    assert reset.status_code == 200
    reset_payload = reset.json()
    assert reset_payload["snapshot"]["snapshot_id"]
    assert not (tmp_path / ".system" / "memory" / "knowledge-graph" / "graph.json").exists()

    rollback = client.post(f"/api/data-governance/rollback/{reset_payload['snapshot']['snapshot_id']}", json={"categories": ["knowledge_graph"]})
    assert rollback.status_code == 200
    assert rollback.json()["restored_categories"] == ["knowledge_graph"]
    assert (tmp_path / ".system" / "memory" / "knowledge-graph" / "graph.json").exists()


def test_privacy_report_and_mission_control_surface_backup_health(client: TestClient, tmp_path: Path) -> None:
    _seed_governance_fixture(tmp_path, wrong_phrase="UNIQUE_PRIVACY_REPORT_PHRASE")

    privacy = client.get("/api/data-governance/privacy-report")
    assert privacy.status_code == 200
    privacy_payload = privacy.json()
    assert "assets" in privacy_payload["raw_diagnostic_categories"]
    assert privacy_payload["redacted_fields_count"] >= 5
    assert privacy_payload["safe_export"]["includes_raw_diagnostics"] is False

    mission = client.get("/api/review-lab/mission-control")
    assert mission.status_code == 200
    governance = mission.json()["data_governance"]
    assert governance["backup_health"] in {"never_backed_up", "stale", "ok"}
    assert governance["local_state_size_bytes"] > 0
    assert "assets" in governance["raw_diagnostic_categories"]


def _seed_governance_fixture(repo_root: Path, *, wrong_phrase: str) -> None:
    attempt_root = repo_root / ".system" / "events" / "attempt"
    attempt_root.mkdir(parents=True, exist_ok=True)
    (attempt_root / "attempt-events.jsonl").write_text(
        json.dumps(
            {
                "event_id": "attempt-backup-1",
                "profile_id": "p1",
                "wrong_choice_or_output": wrong_phrase,
                "selected_choice": wrong_phrase,
                "internal_secret": "local diagnostic",
                "correct_resolution": "Use effective duration for callable bonds.",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    asset_root = repo_root / ".system" / "memory" / "review" / "asset-candidates"
    asset_root.mkdir(parents=True, exist_ok=True)
    (asset_root / "asset-1.json").write_text(
        json.dumps(
            {
                "asset_id": "asset-1",
                "title": "Callable bond duration",
                "correct_answer": "Use effective duration when cash flows can change.",
                "wrong_choice_or_output": wrong_phrase,
                "wrong_formula": wrong_phrase,
                "wrong_reasoning": wrong_phrase,
                "source_refs": ["task015-fixture"],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    assessment_root = repo_root / ".system" / "memory" / "assessments" / "sessions"
    assessment_root.mkdir(parents=True, exist_ok=True)
    (assessment_root / "assessment-1.json").write_text(
        json.dumps(
            {
                "assessment_id": "assessment-1",
                "questions": [{"question_id": "q1", "correct_answer": "Effective duration"}],
                "responses": [{"question_id": "q1", "answer_text": wrong_phrase, "selected_choice": wrong_phrase}],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    graph_root = repo_root / ".system" / "memory" / "knowledge-graph"
    graph_root.mkdir(parents=True, exist_ok=True)
    (graph_root / "graph.json").write_text(json.dumps({"nodes": [{"node_id": "n1"}], "edges": []}), encoding="utf-8")

    feature_config = repo_root / ".system" / "config" / "features.yaml"
    feature_config.parent.mkdir(parents=True, exist_ok=True)
    feature_config.write_text("data_governance_enabled: true\nsafe_export_enabled: true\n", encoding="utf-8")


def _enable_data_governance(repo_root: Path) -> None:
    config_path = repo_root / ".system" / "config" / "features.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        "\n".join(
            [
                "daily_review_lab: true",
                "daily_review_lab_enabled: true",
                "mission_control_enabled: true",
                "integration_health_checks_enabled: true",
                "green_test_gate_enabled: true",
                "data_governance_enabled: true",
                "safe_export_enabled: true",
                "full_export_enabled: true",
                "backup_restore_enabled: true",
                "category_reset_enabled: true",
                "privacy_redaction_enabled: true",
                "snapshot_rollback_enabled: true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
