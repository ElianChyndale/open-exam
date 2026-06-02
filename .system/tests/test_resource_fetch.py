from __future__ import annotations

import asyncio

import httpx
import pytest


def _guard():
    from resource_ingestion.policy import ResourcePolicyGuard

    return ResourcePolicyGuard(resolver=lambda _host: ["93.184.216.34"])


def test_fetcher_obeys_robots_txt() -> None:
    from resource_ingestion.fetch import PublicWebFetcher, RobotsDenied

    async def run() -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/robots.txt":
                return httpx.Response(200, text="User-agent: *\nDisallow: /private")
            return httpx.Response(200, text="<html><body>blocked</body></html>", headers={"content-type": "text/html"})

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            fetcher = PublicWebFetcher(client=client, guard=_guard())
            with pytest.raises(RobotsDenied, match="robots"):
                await fetcher.fetch("https://example.com/private")

    asyncio.run(run())


def test_fetcher_rechecks_redirect_targets_for_ssrf() -> None:
    from resource_ingestion.fetch import PublicWebFetcher
    from resource_ingestion.policy import ResourcePolicyGuard, UnsafeResourceURL

    async def run() -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/robots.txt":
                return httpx.Response(404)
            return httpx.Response(302, headers={"location": "http://127.0.0.1/admin"})

        guard = ResourcePolicyGuard(resolver=lambda host: ["127.0.0.1"] if host == "127.0.0.1" else ["93.184.216.34"])
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            fetcher = PublicWebFetcher(client=client, guard=guard)
            with pytest.raises(UnsafeResourceURL, match="public internet"):
                await fetcher.fetch("https://example.com/start")

    asyncio.run(run())


def test_fetcher_rejects_large_html_and_extracts_clean_text() -> None:
    from resource_ingestion.fetch import ResourceFetchError, PublicWebFetcher

    async def run() -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/robots.txt":
                return httpx.Response(404)
            if request.url.path == "/large":
                return httpx.Response(200, text="large", headers={"content-type": "text/html", "content-length": "500"})
            return httpx.Response(200, text="<html><body><h1>Duration</h1><script>ignore()</script><p>Cash flow sensitivity.</p></body></html>", headers={"content-type": "text/html"})

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            fetcher = PublicWebFetcher(client=client, guard=_guard(), max_body_bytes=100)
            with pytest.raises(ResourceFetchError, match="maximum"):
                await fetcher.fetch("https://example.com/large")
            fetched = await fetcher.fetch("https://example.com/article")
            assert fetched["text"] == "Duration Cash flow sensitivity."
            assert fetched["mime_type"] == "text/html"

    asyncio.run(run())


def test_fetcher_honors_retry_after_for_rate_limits() -> None:
    from resource_ingestion.fetch import PublicWebFetcher

    async def run() -> None:
        calls = 0
        sleeps: list[float] = []

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal calls
            if request.url.path == "/robots.txt":
                return httpx.Response(404)
            calls += 1
            if calls == 1:
                return httpx.Response(429, headers={"retry-after": "3"})
            return httpx.Response(200, text="Recovered", headers={"content-type": "text/plain"})

        async def sleeper(delay: float) -> None:
            sleeps.append(delay)

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            fetcher = PublicWebFetcher(client=client, guard=_guard(), sleeper=sleeper)
            fetched = await fetcher.fetch("https://example.com/article")
            assert fetched["text"] == "Recovered"
            assert sleeps == [3.0]

    asyncio.run(run())
