from __future__ import annotations

from pathlib import Path

import pytest

from app.storage import Repository


def test_policy_guard_allows_public_http_and_blocks_private_targets() -> None:
    from resource_ingestion.policy import ResourcePolicyGuard, UnsafeResourceURL

    public_guard = ResourcePolicyGuard(resolver=lambda _host: ["93.184.216.34"])
    assert public_guard.validate_url("https://example.com/research?q=duration") == "https://example.com/research?q=duration"

    private_guard = ResourcePolicyGuard(resolver=lambda _host: ["127.0.0.1"])
    with pytest.raises(UnsafeResourceURL, match="public internet"):
        private_guard.validate_url("https://example.com/internal")
    with pytest.raises(UnsafeResourceURL, match="scheme"):
        public_guard.validate_url("file:///etc/passwd")


def test_authorized_fulltext_is_hash_deduplicated_and_searchable(tmp_path: Path) -> None:
    from app.resource_workflows import import_resource_document, search_resources

    repo = Repository(tmp_path)
    first = import_resource_document(
        repo,
        lane="language",
        provider="generic_web",
        url="https://example.com/duration",
        title="Duration reading",
        text="Effective duration measures sensitivity when expected cash flows can change.",
        language="en",
        topic="Fixed Income",
        license_mode="fulltext_allowed",
    )
    second = import_resource_document(
        repo,
        lane="language",
        provider="generic_web",
        url="https://example.com/duration",
        title="Duration reading",
        text="Effective duration measures sensitivity when expected cash flows can change.",
        language="en",
        topic="Fixed Income",
        license_mode="fulltext_allowed",
    )

    assert first["duplicate"] is False
    assert second["duplicate"] is True
    assert first["document"]["document_id"] == second["document"]["document_id"]
    assert (tmp_path / first["document"]["content_ref"]).exists()
    assert list((tmp_path / ".system" / "private" / "resources" / "manifests").glob("*.json"))
    assert [event["event_type"] for event in repo.load_jsonl_events("resource")].count("resource.document.ingested") == 1
    results = search_resources(repo, query="duration", lane="language")
    assert results["count"] == 1
    assert results["results"][0]["document_id"] == first["document"]["document_id"]


def test_unknown_license_keeps_only_metadata_and_excerpt(tmp_path: Path) -> None:
    from app.resource_workflows import import_resource_document, search_resources

    repo = Repository(tmp_path)
    imported = import_resource_document(
        repo,
        lane="cfa",
        provider="generic_web",
        url="https://example.com/paywalled",
        title="Unknown rights",
        text="This body must not be retained as full text. " * 30,
        license_mode="metadata_only",
    )

    document = imported["document"]
    assert document["content_ref"] == ""
    assert 0 < len(document["excerpt"]) <= 280
    assert search_resources(repo, query="retained")["count"] == 0


def test_provider_registry_and_subscription_state_are_replayable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from app.resource_workflows import create_subscription, list_providers, list_subscriptions, update_subscription

    monkeypatch.delenv("FRED_API_KEY", raising=False)
    repo = Repository(tmp_path)
    subscription = create_subscription(
        repo,
        lane="cfa",
        provider="rss_atom",
        target="https://example.com/feed.xml",
        schedule="0 */6 * * *",
        budget=20,
    )

    provider_map = {provider["provider_id"]: provider for provider in list_providers()}
    assert {"generic_web", "rss_atom", "sitemap", "youtube_metadata", "openalex", "arxiv", "sec_edgar", "fred", "world_bank", "openai_web_search"} <= set(provider_map)
    assert provider_map["fred"]["configured"] is False
    assert list_subscriptions(repo) == [subscription]
    paused = update_subscription(repo, subscription_id=subscription["subscription_id"], enabled=False, budget=10)
    assert paused["enabled"] is False
    assert paused["budget"] == 10
    assert list_subscriptions(repo) == [paused]
    assert (tmp_path / ".system" / "memory" / "resources" / "state.json").exists()


def test_lane_promotions_keep_cfa_non_official_and_answer_bearing_assets_in_review(tmp_path: Path) -> None:
    from app.resource_workflows import import_resource_document, list_inbox, list_promotions

    repo = Repository(tmp_path)
    language = import_resource_document(
        repo,
        lane="language",
        provider="generic_web",
        url="https://example.com/licensed-language",
        title="Licensed language",
        text="Authorized language corpus text.",
        license_mode="fulltext_allowed",
    )
    official = import_resource_document(
        repo,
        lane="cfa",
        provider="sec_edgar",
        url="https://www.sec.gov/example.json",
        title="SEC structured filing",
        text='{"facts": []}',
        license_mode="official_structured",
    )
    answer_bearing = import_resource_document(
        repo,
        lane="cfa",
        provider="generic_web",
        url="https://example.com/practice-solution",
        title="Practice solution",
        text="The answer is B.",
        license_mode="fulltext_allowed",
        answer_bearing=True,
    )

    promotions = {item["target"]: item for item in list_promotions(repo)}
    assert promotions["language_private_corpus"]["approved"] is True
    assert promotions["cfa_registry_fact"]["approved"] is True
    inbox_document_ids = {item["document_id"] for item in list_inbox(repo)}
    assert answer_bearing["document"]["document_id"] in inbox_document_ids
    assert language["document"]["document_id"] not in inbox_document_ids
    assert official["document"]["document_id"] not in inbox_document_ids


def test_privacy_purge_includes_resource_private_assets(tmp_path: Path) -> None:
    from app.resource_workflows import import_resource_document
    from app.roadmap_waves import confirm_privacy_purge, request_privacy_purge

    repo = Repository(tmp_path)
    imported = import_resource_document(
        repo,
        lane="language",
        provider="generic_web",
        url="https://example.com/open",
        title="Open text",
        text="A licensed local corpus asset.",
        license_mode="fulltext_allowed",
    )
    private_path = imported["document"]["content_ref"]

    request = request_privacy_purge(repo)
    assert private_path in request["deletion_manifest"]
    confirm_privacy_purge(repo, request["confirmation_token"])
    assert not (tmp_path / private_path).exists()


def test_resource_index_can_rebuild_from_hash_manifests(tmp_path: Path) -> None:
    from app.resource_storage import ResourceRepository
    from app.resource_workflows import import_resource_document, rebuild_resource_index, search_resources

    repo = Repository(tmp_path)
    import_resource_document(
        repo,
        lane="language",
        provider="generic_web",
        url="https://example.com/rebuild",
        title="Rebuild reading",
        text="Convexity improves the duration approximation.",
        license_mode="fulltext_allowed",
    )
    resources = ResourceRepository(repo)
    resources.index.db_path.unlink()

    result = rebuild_resource_index(repo)

    assert result == {"documents": 1, "segments": 1}
    assert search_resources(repo, query="convexity")["count"] == 1


def test_privacy_export_contains_private_resource_payloads(tmp_path: Path) -> None:
    from app.resource_workflows import import_resource_document
    from app.roadmap_waves import export_privacy_bundle

    repo = Repository(tmp_path)
    import_resource_document(
        repo,
        lane="language",
        provider="generic_web",
        url="https://example.com/export",
        title="Export reading",
        text="Private licensed corpus text.",
        license_mode="fulltext_allowed",
    )

    exported = export_privacy_bundle(repo)

    assert exported["private_resources"]
    assert any(item["path"].endswith(".txt") and item["content_base64"] for item in exported["private_resources"])
