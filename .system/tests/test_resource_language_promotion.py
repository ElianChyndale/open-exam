from __future__ import annotations

from pathlib import Path

from app.storage import Repository


def test_high_confidence_cited_language_extraction_creates_review_card(tmp_path: Path) -> None:
    from app.language_storage import LanguageRepository
    from app.resource_workflows import import_resource_document, promote_language_extractions

    repo = Repository(tmp_path)
    imported = import_resource_document(
        repo,
        lane="language",
        provider="generic_web",
        url="https://example.com/language",
        title="Finance English",
        text="New shares may have a dilutive effect on EPS.",
        language="en",
        license_mode="fulltext_allowed",
    )
    segment_id = imported["segments"][0]["segment_id"]

    promoted = promote_language_extractions(
        repo,
        document_id=imported["document"]["document_id"],
        items=[{"item_type": "phrase", "canonical_form": "dilutive effect", "native_gloss": "摊薄效应"}],
        citations=[segment_id],
        confidence=0.91,
        provider="fixture-ai",
        model="fixture-model",
    )

    language_state = LanguageRepository(repo).replay()
    assert promoted["promoted"] is True
    assert promoted["new_card_count"] == 1
    assert len(language_state["items"]) == 1
    assert len(language_state["cards"]) == 1


def test_low_confidence_language_extraction_is_quarantined(tmp_path: Path) -> None:
    from app.resource_workflows import import_resource_document, list_inbox, promote_language_extractions

    repo = Repository(tmp_path)
    imported = import_resource_document(
        repo,
        lane="language",
        provider="generic_web",
        url="https://example.com/low-confidence",
        title="Finance English",
        text="Duration measures sensitivity.",
        language="en",
        license_mode="fulltext_allowed",
    )
    segment_id = imported["segments"][0]["segment_id"]

    result = promote_language_extractions(
        repo,
        document_id=imported["document"]["document_id"],
        items=[{"item_type": "word", "canonical_form": "duration"}],
        citations=[segment_id],
        confidence=0.5,
        provider="fixture-ai",
        model="fixture-model",
    )

    assert result["promoted"] is False
    assert any(item["reason"] == "language_ai_extraction_requires_review" for item in list_inbox(repo))
