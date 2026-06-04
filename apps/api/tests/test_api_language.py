from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.storage import Repository
from deps import get_repo
from main import app


def _write_feature_flags(root: Path, **flags: bool) -> None:
    config_dir = root / ".system" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    lines = [f"{name}: {'true' if value else 'false'}" for name, value in flags.items()]
    (config_dir / "features.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    repo = Repository(tmp_path)
    app.dependency_overrides[get_repo] = lambda: repo
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_language_api_manual_capture_review_grammar_and_graph(client: TestClient) -> None:
    profiles = client.get("/api/language/profiles")
    assert profiles.status_code == 200
    assert len(profiles.json()["profiles"]) == 4

    source = client.post("/api/language/sources", json={
        "source_type": "manual",
        "title": "Finance sentence",
        "language": "en",
        "content": "New shares can have a dilutive effect on EPS.",
    })
    assert source.status_code == 201
    segment_id = source.json()["segments"][0]["segment_id"]
    item = client.post("/api/language/items", json={
        "item_type": "phrase", "canonical_form": "dilutive effect", "language": "en", "segment_id": segment_id,
    })
    assert item.status_code == 201
    item_id = item.json()["item"]["item_id"]

    cards = client.post("/api/language/cards/generate", json={"item_id": item_id, "card_types": ["recognition", "production"]})
    assert cards.status_code == 201
    card_id = cards.json()["cards"][0]["card_id"]
    reviewed = client.post(f"/api/language/cards/{card_id}/review", json={"rating": "good"})
    assert reviewed.status_code == 200
    assert reviewed.json()["fsrs_state"]["repetitions"] == 1

    grammar = client.post("/api/language/grammar/analyze", json={"segment_id": segment_id})
    assert grammar.status_code == 200
    graph = client.post("/api/language/intuition/rebuild")
    assert graph.status_code == 200
    assert client.get("/api/language/stats").status_code == 200


def test_language_api_uses_cards_v2_when_flag_enabled(client: TestClient) -> None:
    _write_feature_flags(
        client.app.dependency_overrides[get_repo]().root,
        language_cards_v2=True,
        dictionary_os=True,
        spanish_morphology_engine=True,
    )

    source = client.post("/api/language/sources", json={
        "source_type": "manual",
        "title": "Spanish sentence",
        "language": "es",
        "content": "Yo como pan con mi familia todos los dias.",
    })
    assert source.status_code == 201
    segment_id = source.json()["segments"][0]["segment_id"]

    item = client.post("/api/language/items", json={
        "item_type": "word",
        "canonical_form": "comer",
        "language": "es",
        "segment_id": segment_id,
        "native_gloss": "to eat",
    })
    assert item.status_code == 201
    item_id = item.json()["item"]["item_id"]

    cards = client.post("/api/language/cards/generate", json={"item_id": item_id})
    assert cards.status_code == 201
    payload = cards.json()["cards"]
    assert payload
    assert all(card["front_payload"]["prompt"].strip().lower() != card["back_payload"]["answer"].strip().lower() for card in payload)


def test_language_api_keeps_legacy_card_path_when_flag_disabled(client: TestClient) -> None:
    _write_feature_flags(client.app.dependency_overrides[get_repo]().root, language_cards_v2=False)

    source = client.post("/api/language/sources", json={
        "source_type": "manual",
        "title": "Finance sentence",
        "language": "en",
        "content": "A moat can protect pricing power.",
    })
    assert source.status_code == 201
    segment_id = source.json()["segments"][0]["segment_id"]

    item = client.post("/api/language/items", json={
        "item_type": "phrase",
        "canonical_form": "pricing power",
        "language": "en",
        "segment_id": segment_id,
    })
    assert item.status_code == 201
    item_id = item.json()["item"]["item_id"]

    cards = client.post("/api/language/cards/generate", json={"item_id": item_id, "card_types": ["recognition"]})
    assert cards.status_code == 201
    card = cards.json()["cards"][0]
    assert card["front_payload"]["prompt"] == "pricing power"
    assert card["back_payload"]["answer"] == "pricing power"


def test_spanish_english_dictionary_import_and_review_gate(client: TestClient) -> None:
    _enable_dictionary_kernel(client)
    entry = {
        "headword": "aprovechar",
        "language": "es",
        "target_language": "en",
        "part_of_speech": "verb",
        "definition": "to take advantage of; to make use of",
        "translation": "take advantage of, make use of",
        "example_sentence": "Debemos aprovechar esta oportunidad.",
        "example_translation": "We should take advantage of this opportunity.",
        "collocations": ["aprovechar una oportunidad", "aprovechar el tiempo"],
        "usage_notes": ["Often used with opportunities, time, or resources."],
    }
    imported = client.post(
        "/api/language-os/dictionaries/import-json",
        json={
            "profile_id": "p1",
            "title": "Spanish-English Core",
            "dictionary_type": "spanish_english",
            "entries": [entry],
        },
    )
    assert imported.status_code == 201
    payload = imported.json()
    dictionary_id = payload["dictionary"]["dictionary_id"]
    asset = payload["lexical_assets"][0]
    assert payload["dictionary"]["validation_status"] == "draft"
    assert payload["dictionary"]["quality_score"] > 0
    assert asset["translation"] == "take advantage of, make use of"
    assert asset["example_translation"] == "We should take advantage of this opportunity."
    assert "aprovechar una oportunidad" in asset["collocations"]
    assert asset["source_refs"]
    assert asset["validation_status"] in {"draft", "needs_review"}

    before = client.post("/api/language-os/review/generate-session", json={"profile_id": "p1", "max_units": 5})
    assert before.status_code == 200
    assert not any(unit["lexical_id"] == asset["lexical_id"] for unit in before.json()["units"])

    confirmed_dictionary = client.post(f"/api/language-os/dictionaries/{dictionary_id}/confirm")
    assert confirmed_dictionary.status_code == 200
    assert confirmed_dictionary.json()["dictionary"]["quality_status"] in {"medium", "high", "trusted"}
    confirmed_asset = client.post(f"/api/language-os/lexical-assets/{asset['lexical_id']}/confirm")
    assert confirmed_asset.status_code == 200

    after = client.post("/api/language-os/review/generate-session", json={"profile_id": "p1", "max_units": 5})
    assert after.status_code == 200
    session = after.json()
    unit = next(unit for unit in session["units"] if unit["lexical_id"] == asset["lexical_id"])
    assert unit["display_mode"] in {"translation_recall", "collocation_check", "cloze_context"}
    assert "take advantage of" not in unit["front_prompt"]
    assert "take advantage of" in unit["correct_answer"]
    assert unit["source_refs"]

    completed = client.post(
        f"/api/language-os/review/units/{unit['unit_id']}/complete",
        json={"session_id": session["session_id"], "outcome": "partial", "time_spent_seconds": 22},
    )
    assert completed.status_code == 200
    memory_update = completed.json()["memory_update"]
    assert memory_update["next_review_at"]
    assert memory_update["mastery_state"] == "learning"
    assert {"definition_gap", "translation_gap"}.intersection(memory_update["weakness_tags"])


def test_english_json_csv_and_text_dictionary_imports(client: TestClient) -> None:
    _enable_dictionary_kernel(client)
    english = client.post(
        "/api/language-os/dictionaries/import-json",
        json={
            "title": "English Core",
            "dictionary_type": "english_english",
            "entries": [
                {
                    "headword": "mitigate",
                    "language": "en",
                    "part_of_speech": "verb",
                    "definition": "to make something less severe",
                    "example_sentence": "The policy helped mitigate risk.",
                    "collocations": ["mitigate risk", "mitigate damage"],
                    "synonyms": ["alleviate", "reduce"],
                }
            ],
        },
    )
    assert english.status_code == 201
    asset = english.json()["lexical_assets"][0]
    assert asset["headword"] == "mitigate"
    assert asset["language"] == "en"
    assert "mitigate risk" in asset["collocations"]
    assert "alleviate" in asset["synonyms"]
    assert asset["source_refs"]

    csv_import = client.post(
        "/api/language-os/dictionaries/import-csv",
        json={
            "title": "CSV Mini Dictionary",
            "dictionary_type": "spanish_english",
            "csv_text": "headword,language,target_language,part_of_speech,definition,translation,example_sentence,collocations\n"
            "claro,es,en,adjective,clear or obvious,clear,El mensaje es claro.,claro ejemplo; tener claro\n",
        },
    )
    assert csv_import.status_code == 201
    csv_asset = csv_import.json()["lexical_assets"][0]
    assert csv_asset["headword"] == "claro"
    assert csv_asset["translation"] == "clear"
    assert csv_asset["source_refs"]

    text_import = client.post(
        "/api/language-os/dictionaries/import-text",
        json={
            "title": "Text Snippet Dictionary",
            "dictionary_type": "english_english",
            "text": "resilient (adjective) - able to recover quickly\nexample: Resilient learners recover from mistakes.\ncollocations: resilient learner, resilient system",
        },
    )
    assert text_import.status_code == 201
    text_asset = text_import.json()["lexical_assets"][0]
    assert text_asset["headword"] == "resilient"
    assert text_asset["validation_status"] in {"draft", "needs_review"}
    assert text_asset["source_refs"]


def test_dictionary_file_imports_json_csv_and_deduplicates(client: TestClient) -> None:
    _enable_dictionary_kernel(client)
    entries = [
        {
            "headword": "aprovechar",
            "language": "es",
            "target_language": "en",
            "part_of_speech": "verb",
            "definition": "to take advantage of",
            "translation": "take advantage of",
            "example_sentence": "Hay que aprovechar la oportunidad.",
        }
    ]
    json_bytes = json.dumps(entries).encode("utf-8")
    imported = client.post(
        "/api/language-os/dictionaries/import-file",
        data={"title": "Uploaded Spanish JSON", "dictionary_type": "spanish_english"},
        files={"file": ("spanish.json", json_bytes, "application/json")},
    )
    assert imported.status_code == 201
    payload = imported.json()
    assert payload["file"]["extraction_status"] == "extracted"
    assert payload["file"]["storage_path"]
    assert not Path(payload["file"]["storage_path"]).is_absolute()
    assert payload["dictionary"]["dictionary_id"]
    asset = payload["lexical_assets"][0]
    assert asset["headword"] == "aprovechar"
    assert any(ref.startswith("file:") for ref in asset["source_refs"])

    duplicate = client.post(
        "/api/language-os/dictionaries/import-file",
        data={"title": "Uploaded Spanish JSON", "dictionary_type": "spanish_english"},
        files={"file": ("spanish.json", json_bytes, "application/json")},
    )
    assert duplicate.status_code == 201
    duplicate_payload = duplicate.json()
    assert duplicate_payload["duplicate"] is True
    assert duplicate_payload["file"]["extraction_status"] == "duplicate"
    assert duplicate_payload["dictionary"]["dictionary_id"] == payload["dictionary"]["dictionary_id"]

    csv_bytes = (
        "headword,language,target_language,part_of_speech,definition,translation,example_sentence\n"
        "claro,es,en,adjective,clear or obvious,clear,El mensaje es claro.\n"
    ).encode("utf-8")
    csv_import = client.post(
        "/api/language-os/dictionaries/import-file",
        data={"title": "Uploaded Spanish CSV", "dictionary_type": "spanish_english"},
        files={"file": ("spanish.csv", csv_bytes, "text/csv")},
    )
    assert csv_import.status_code == 201
    csv_payload = csv_import.json()
    csv_asset = csv_payload["lexical_assets"][0]
    assert csv_payload["file"]["source_type"] == "csv_dictionary"
    assert csv_asset["headword"] == "claro"
    assert any(ref.startswith("file:") for ref in csv_asset["source_refs"])


def test_rejected_lexical_assets_are_excluded_from_review(client: TestClient) -> None:
    _enable_dictionary_kernel(client)
    imported = client.post(
        "/api/language-os/dictionaries/import-json",
        json={
            "title": "Rejectable Dictionary",
            "dictionary_type": "english_english",
            "entries": [{"headword": "spurious", "language": "en", "definition": "not being what it purports to be"}],
        },
    )
    dictionary = imported.json()["dictionary"]
    asset = imported.json()["lexical_assets"][0]
    assert client.post(f"/api/language-os/dictionaries/{dictionary['dictionary_id']}/confirm").status_code == 200
    assert client.post(f"/api/language-os/lexical-assets/{asset['lexical_id']}/confirm").status_code == 200

    review = client.post("/api/language-os/review/generate-session", json={"max_units": 5})
    assert review.status_code == 200
    assert any(unit["lexical_id"] == asset["lexical_id"] for unit in review.json()["units"])

    rejected = client.post(f"/api/language-os/lexical-assets/{asset['lexical_id']}/reject")
    assert rejected.status_code == 200
    assert rejected.json()["asset"]["validation_status"] == "rejected"
    after = client.post("/api/language-os/review/generate-session", json={"max_units": 5})
    assert after.status_code == 200
    assert not any(unit["lexical_id"] == asset["lexical_id"] for unit in after.json()["units"])


def test_lexical_asset_confirmation_requires_source_refs(client: TestClient, tmp_path: Path) -> None:
    _enable_dictionary_kernel(client)
    from language_science.dictionary_models import LexicalAsset
    from language_science.models import stable_id

    asset_root = tmp_path / ".system" / "memory" / "language" / "dictionary-kernel" / "lexical-assets"
    asset_root.mkdir(parents=True, exist_ok=True)
    asset = LexicalAsset(
        lexical_id=stable_id("lex", "no-source"),
        profile_id="default",
        dictionary_id=None,
        headword="unsourced",
        language="en",
        target_language=None,
        part_of_speech="adjective",
        sense_number=1,
        definition="Missing source refs.",
        translation=None,
        example_sentence=None,
        example_translation=None,
        source_refs=[],
        validation_status="draft",
        created_at="2026-06-03T00:00:00+00:00",
    )
    (asset_root / f"{asset.lexical_id}.json").write_text(
        json.dumps(asset.as_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    response = client.post(f"/api/language-os/lexical-assets/{asset.lexical_id}/confirm")
    assert response.status_code == 422


def _enable_dictionary_kernel(client: TestClient) -> None:
    _write_feature_flags(
        client.app.dependency_overrides[get_repo]().root,
        language_os_enabled=True,
        dictionary_kernel_enabled=True,
        lexical_review_enabled=True,
        dictionary_quality_gate_enabled=True,
        spanish_english_dictionary_enabled=True,
        english_english_dictionary_enabled=True,
        file_ingestion_enabled=True,
        dictionary_file_import_enabled=True,
        file_duplicate_detection_enabled=True,
        pdf_text_extraction_enabled=True,
        ocr_extraction_enabled=False,
        dictionary_os=True,
    )
