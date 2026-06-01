from __future__ import annotations

from pathlib import Path

import pytest


def test_language_profiles_source_dedupe_segments_and_replay(tmp_path: Path) -> None:
    from app.language_storage import LanguageRepository
    from app.language_workflows import import_source, list_profiles, select_profile

    repo = LanguageRepository(tmp_path)
    assert {profile["profile_id"] for profile in list_profiles(repo)} == {
        "en-general", "en-finance", "es-general", "es-business",
    }
    select_profile(repo, "es-general")
    imported = import_source(
        repo,
        source_type="manual",
        title="Spanish note",
        language="es",
        content="Actualmente estudio finanzas. Asisto a clase.",
    )
    duplicate = import_source(
        repo,
        source_type="manual",
        title="Spanish note copy",
        language="es",
        content="Actualmente estudio finanzas. Asisto a clase.",
    )

    assert duplicate["duplicate"] is True
    assert duplicate["source"]["source_id"] == imported["source"]["source_id"]
    state = repo.replay()
    assert state["active_profile_id"] == "es-general"
    assert len(state["sources"]) == 1
    assert len(state["segments"]) == 2
    assert all(segment["locator"].startswith("chars:") for segment in state["segments"].values())
    assert (tmp_path / ".system" / "memory" / "language" / "state.json").exists()


def test_item_merge_cards_fsrs_review_and_exports(tmp_path: Path) -> None:
    from app.language_storage import LanguageRepository
    from app.language_workflows import collect_item, export_language, generate_cards, import_source, review_card

    repo = LanguageRepository(tmp_path)
    imported = import_source(repo, source_type="manual", title="Finance", language="en", content="New shares may have a dilutive effect on EPS.")
    segment_id = imported["segments"][0]["segment_id"]
    first = collect_item(repo, item_type="phrase", canonical_form="dilutive effect", language="en", segment_id=segment_id)
    second = collect_item(repo, item_type="phrase", canonical_form="Dilutive Effect", language="en", segment_id=segment_id)
    assert second["merged"] is True
    assert second["item"]["item_id"] == first["item"]["item_id"]

    cards = generate_cards(repo, first["item"]["item_id"], card_types=["recognition", "production", "cloze"])
    assert {card["card_type"] for card in cards} == {"recognition", "production", "cloze"}
    reviewed = review_card(repo, cards[0]["card_id"], "good")
    assert reviewed["fsrs_state"]["repetitions"] == 1
    assert reviewed["fsrs_state"]["state"] == "review"
    assert "dilutive effect" in export_language(repo, "markdown")["content"]
    assert "canonical_form" in export_language(repo, "csv")["content"]
    assert export_language(repo, "anki")["format"] == "anki"


def test_importers_manifest_and_transcription_consent_gate(tmp_path: Path) -> None:
    from app.language_storage import LanguageRepository
    from app.language_workflows import import_source, request_transcription
    from app.roadmap_waves import record_consent

    repo = LanguageRepository(tmp_path)
    subtitle = import_source(
        repo,
        source_type="subtitle",
        title="Lecture",
        language="en",
        content="1\n00:00:01,000 --> 00:00:03,500\nDuration measures sensitivity.\n",
        import_format="srt",
    )
    assert subtitle["segments"][0]["start_time"] == 1.0
    assert subtitle["segments"][0]["end_time"] == 3.5

    audio = import_source(
        repo,
        source_type="audio",
        title="Pronunciation clip",
        language="es",
        content="base64-placeholder",
        import_format="audio",
        attachment_name="clip.mp3",
    )
    assert audio["source"]["attachment_manifest"]["stored_locally"] is True
    with pytest.raises(PermissionError, match="consent"):
        request_transcription(repo, audio["source"]["source_id"], provider="deepseek", feature_enabled=True)
    record_consent(repo.repo, provider="deepseek", purpose="language_cloud_transcription", granted=True)
    requested = request_transcription(repo, audio["source"]["source_id"], provider="deepseek", feature_enabled=True)
    assert requested["provider"] == "deepseek"


def test_grammar_cache_edit_graph_sessions_and_stats(tmp_path: Path) -> None:
    from app.language_storage import LanguageRepository
    from app.language_workflows import (
        analyze_grammar,
        collect_item,
        edit_grammar,
        export_language,
        import_source,
        language_stats,
        rebuild_intuition_graph,
        record_session,
        search_intuition,
    )

    repo = LanguageRepository(tmp_path)
    english = import_source(repo, source_type="manual", title="Ethics", language="en", content="If disclosure is required, the analyst must comply.")
    spanish = import_source(repo, source_type="manual", title="Spanish", language="es", content="Actualmente estoy embarazada.")
    en_analysis = analyze_grammar(repo, english["segments"][0]["segment_id"])
    cached = analyze_grammar(repo, english["segments"][0]["segment_id"])
    es_analysis = analyze_grammar(repo, spanish["segments"][0]["segment_id"])
    assert cached["analysis_id"] == en_analysis["analysis_id"]
    assert cached["cache_hit"] is True
    assert es_analysis["spanish_features"]
    edited = edit_grammar(repo, english["segments"][0]["segment_id"], {"notes": "Conditional ethics wording"})
    assert edited["notes"] == "Conditional ethics wording"

    collect_item(repo, item_type="phrase", canonical_form="dilutive effect", language="en", segment_id=english["segments"][0]["segment_id"])
    collect_item(repo, item_type="phrase", canonical_form="diluted EPS effect", language="en", segment_id=english["segments"][0]["segment_id"])
    collect_item(repo, item_type="word", canonical_form="actualmente", language="es", segment_id=spanish["segments"][0]["segment_id"])
    edges = rebuild_intuition_graph(repo)
    assert any(edge["edge_type"] == "co_occurrence" for edge in edges)
    assert search_intuition(repo, "dilutive")
    record_session(repo, session_type="dictation", language="es", score=0.5, output_gap=True)
    assert language_stats(repo)["output_gap_count"] == 1
    assert "LanguageOS" in export_language(repo, "obsidian")["content"]
