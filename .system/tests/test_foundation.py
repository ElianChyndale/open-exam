from __future__ import annotations

from pathlib import Path


def test_event_envelope_v2_round_trips_payload_and_stable_id() -> None:
    from learning_records import EventEnvelopeV2

    first = EventEnvelopeV2.create(
        event_type="todo.task.added",
        source_layer="todo",
        payload={"task_id": "todo-1", "text": "Complete Daily Review"},
        evidence_refs=["study-plan-1"],
        consent_scope=["local_storage"],
        idempotency_key="todo-add-1",
    )
    second = EventEnvelopeV2.from_dict(first.as_dict())

    assert second == first
    assert first.event_id.startswith("evt2-")
    assert first.schema_version == 2
    assert first.provenance == {}


def test_feature_flags_merge_defaults_with_repository_overrides(tmp_path: Path) -> None:
    from app.feature_flags import FeatureFlags

    config = tmp_path / ".system" / "config" / "features.yaml"
    config.parent.mkdir(parents=True)
    config.write_text("language_os_enabled: true\nreduced_motion_safe: false\n", encoding="utf-8")

    flags = FeatureFlags.load(tmp_path)

    assert flags.enabled("language_os_enabled") is True
    assert flags.enabled("reduced_motion_safe") is False
    assert flags.enabled("todo_enabled") is True
    assert flags.enabled("missing_flag") is False
