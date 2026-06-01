from __future__ import annotations

from pathlib import Path

import pytest

from app.storage import Repository


def test_provenance_consent_privacy_export_and_two_step_purge(tmp_path: Path) -> None:
    from app.roadmap_waves import (
        confirm_privacy_purge,
        export_privacy_bundle,
        get_provenance,
        record_consent,
        record_provenance,
        request_privacy_purge,
    )

    repo = Repository(tmp_path)
    repo.append_attempt_record({"attempt_id": "attempt-1", "topic": "Ethics"})
    record_provenance(repo, entity_id="attempt-1", activity_type="attempt.recorded", evidence_refs=["manual-1"])
    record_consent(repo, provider="deepseek", purpose="grounded_explanations", granted=False)

    trace = get_provenance(repo, "attempt-1")
    assert trace["entity_id"] == "attempt-1"
    assert trace["evidence_refs"] == ["manual-1"]
    exported = export_privacy_bundle(repo)
    assert exported["streams"]["attempt"][0]["attempt_id"] == "attempt-1"
    assert exported["streams"]["consent"][0]["payload"]["granted"] is False

    purge = request_privacy_purge(repo)
    assert "events/attempt/attempt-events.jsonl" in "\n".join(purge["deletion_manifest"])
    with pytest.raises(ValueError, match="confirmation token"):
        confirm_privacy_purge(repo, "incorrect-token")
    result = confirm_privacy_purge(repo, purge["confirmation_token"])
    assert result["deleted_count"] >= 1
    assert repo.load_attempt_records() == []


def test_xapi_export_and_provider_opt_in_are_explicit(tmp_path: Path) -> None:
    from app.roadmap_waves import build_xapi_statements, provider_is_allowed, record_consent

    repo = Repository(tmp_path)
    repo.append_attempt_record({"attempt_id": "attempt-1", "topic": "Ethics", "is_correct": True})
    assert provider_is_allowed(repo, "deepseek", "grounded_explanations") is False
    record_consent(repo, provider="deepseek", purpose="grounded_explanations", granted=True)
    assert provider_is_allowed(repo, "deepseek", "grounded_explanations") is True

    statement = build_xapi_statements(repo)[0]
    assert statement["actor"]["account"]["name"] == "local-default"
    assert statement["verb"]["id"].endswith("/answered")
    assert statement["object"]["id"].endswith("/attempt-1")


def test_sparse_data_models_and_pedagogy_are_deterministic() -> None:
    from learner_twin import LearnerTwin
    from study_science.pedagogy import PedagogyPolicy
    from study_science.psychometrics import BayesianKnowledgeTrace, HalfLifeEstimator, RaschModel
    from study_science.structured_tasks import StructuredTask

    twin = LearnerTwin.from_attempts([
        {"topic": "Ethics", "is_correct": True, "confidence": 4},
        {"topic": "Ethics", "is_correct": False, "confidence": 4},
    ])
    assert twin.skills["Ethics"].mastery == 0.5
    assert twin.skills["Ethics"].confidence_bias == 0.5
    assert HalfLifeEstimator.recall_probability(half_life_days=7, elapsed_days=7) == 0.5
    assert round(RaschModel.probability(ability=0, difficulty=0), 3) == 0.5
    assert BayesianKnowledgeTrace.update(0.4, correct=True) > 0.4
    assert PedagogyPolicy.select(error_type="concept_confusion", confidence=4, energy_level=2).strategy == "contrast_pair"
    assert StructuredTask(task_id="task-1", task_type="active_recall", prompt="Define duration.").as_dict()["completion_state"] == "pending"


def test_grounded_claim_mcp_research_and_trust_adapters(tmp_path: Path) -> None:
    from app.roadmap_waves import (
        EvidenceClaim,
        ReadOnlyMCPAdapter,
        compare_scheduler_variants,
        export_caliper_events,
        export_open_badge,
        ground_claim,
    )

    repo = Repository(tmp_path)
    claim = ground_claim(EvidenceClaim(claim_id="claim-1", text="Duration measures rate sensitivity.", evidence_refs=["card-1"]))
    assert claim["grounded"] is True
    with pytest.raises(ValueError, match="evidence"):
        ground_claim(EvidenceClaim(claim_id="claim-2", text="Unsupported.", evidence_refs=[]))

    adapter = ReadOnlyMCPAdapter(repo)
    assert adapter.list_tools() == ["find_evidence", "get_due_reviews", "trace_provenance"]
    comparison = compare_scheduler_variants([{"is_correct": True}, {"is_correct": False}])
    assert comparison[0]["variant"] == "static-spacing"
    assert export_caliper_events(repo)["sensor"] == "OpenExam"
    assert export_open_badge("Ethics Foundations")["type"] == ["VerifiableCredential", "OpenBadgeCredential"]
