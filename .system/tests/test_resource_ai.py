from __future__ import annotations

from pathlib import Path

import pytest

from app.storage import Repository


def test_ai_discovery_requires_consent_and_queues_cited_urls_for_deterministic_fetch(tmp_path: Path) -> None:
    from app.resource_workflows import discover_resources_ai, list_inbox
    from app.roadmap_waves import record_consent

    repo = Repository(tmp_path)

    def searcher(_query: str):
        return {
            "model": "fixture-model",
            "cost": 0.02,
            "candidates": [
                {
                    "url": "https://example.com/cited",
                    "title": "Cited source",
                    "confidence": 0.93,
                    "citations": ["https://example.com/cited"],
                },
                {
                    "url": "https://example.com/uncited",
                    "title": "Uncited source",
                    "confidence": 0.99,
                    "citations": [],
                },
            ],
        }

    with pytest.raises(PermissionError, match="consent"):
        discover_resources_ai(repo, lane="cfa", query="duration cases", searcher=searcher)

    record_consent(repo, provider="openai", purpose="resource_ai_discovery", granted=True)
    result = discover_resources_ai(repo, lane="cfa", query="duration cases", searcher=searcher)

    assert result["candidate_count"] == 2
    assert result["fetch_ready_count"] == 1
    inbox = list_inbox(repo)
    assert {item["reason"] for item in inbox} == {
        "ai_discovery_requires_deterministic_fetch",
        "ai_discovery_missing_citations",
    }
    assert all(item["status"] == "pending" for item in inbox)


def test_ai_discovery_enforces_cost_budget(tmp_path: Path) -> None:
    from app.resource_workflows import discover_resources_ai
    from app.roadmap_waves import record_consent

    repo = Repository(tmp_path)
    record_consent(repo, provider="openai", purpose="resource_ai_discovery", granted=True)

    with pytest.raises(ValueError, match="budget"):
        discover_resources_ai(
            repo,
            lane="language",
            query="finance language",
            max_cost=0.01,
            searcher=lambda _query: {"model": "fixture", "cost": 0.02, "candidates": []},
        )
