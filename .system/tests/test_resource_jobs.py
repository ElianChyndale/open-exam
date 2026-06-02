from __future__ import annotations

import asyncio
from pathlib import Path

from app.storage import Repository


class FakeFetcher:
    def __init__(self, pages: dict[str, str]) -> None:
        self.pages = pages
        self.urls: list[str] = []

    async def fetch(self, url: str) -> dict[str, str]:
        self.urls.append(url)
        return {
            "url": url,
            "text": self.pages[url],
            "mime_type": "text/plain",
            "etag": "",
            "last_modified": "",
            "retrieved_at": "2026-06-02T00:00:00+00:00",
        }


def test_crawl_records_completed_job_and_document(tmp_path: Path) -> None:
    from app.resource_workflows import crawl_resource_url, list_jobs

    repo = Repository(tmp_path)
    fetcher = FakeFetcher({"https://example.com/open": "Licensed duration reading."})
    result = asyncio.run(
        crawl_resource_url(
            repo,
            lane="language",
            provider="generic_web",
            url="https://example.com/open",
            license_mode="fulltext_allowed",
            fetcher=fetcher,
        )
    )

    assert result["job"]["status"] == "completed"
    assert result["document"]["document"]["content_ref"]
    assert list_jobs(repo)[0]["budget_usage"] == 1


def test_run_due_discovers_rss_candidates_and_skips_missing_key_provider(tmp_path: Path, monkeypatch) -> None:
    from app.resource_workflows import create_subscription, run_due_subscriptions

    monkeypatch.delenv("FRED_API_KEY", raising=False)
    repo = Repository(tmp_path)
    create_subscription(repo, lane="language", provider="rss_atom", target="https://example.com/feed.xml", budget=2)
    create_subscription(repo, lane="cfa", provider="fred", target="https://api.stlouisfed.org/fred/series", budget=2)
    fetcher = FakeFetcher(
        {
            "https://example.com/feed.xml": """<rss><channel><item><link>https://example.com/a</link></item><item><link>https://example.com/b</link></item></channel></rss>""",
            "https://example.com/a": "First metadata page.",
            "https://example.com/b": "Second metadata page.",
        }
    )

    result = asyncio.run(run_due_subscriptions(repo, fetcher=fetcher))

    assert result["completed"] == 1
    assert result["skipped_missing_key"] == 1
    assert result["documents_seen"] == 2
    assert fetcher.urls == ["https://example.com/feed.xml", "https://example.com/a", "https://example.com/b"]
