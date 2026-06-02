from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from html.parser import HTMLParser
import os
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser

import httpx

from resource_ingestion.policy import DEFAULT_MAX_HTML_BYTES, DEFAULT_MAX_REDIRECTS, ResourcePolicyGuard


class ResourceFetchError(RuntimeError):
    """Raised when a public resource cannot be safely fetched."""


class RobotsDenied(ResourceFetchError):
    """Raised when robots.txt disallows a requested resource."""


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag in {"script", "style", "noscript"}:
            self.ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self.ignored_depth:
            self.ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth and data.strip():
            self.parts.append(data.strip())

    def text(self) -> str:
        return " ".join(" ".join(self.parts).split())


@dataclass(slots=True)
class _RobotsEntry:
    parser: RobotFileParser
    expires_at: datetime


class RobotsPolicyCache:
    def __init__(self, *, ttl: timedelta = timedelta(hours=24)) -> None:
        self.ttl = ttl
        self._entries: dict[str, _RobotsEntry] = {}

    async def allowed(self, client: httpx.AsyncClient, guard: ResourcePolicyGuard, url: str, user_agent: str) -> bool:
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        now = datetime.now(UTC)
        entry = self._entries.get(origin)
        if entry is None or entry.expires_at <= now:
            robots_url = guard.validate_url(f"{origin}/robots.txt")
            parser = RobotFileParser()
            parser.set_url(robots_url)
            try:
                response = await client.get(robots_url, follow_redirects=False)
            except httpx.HTTPError:
                response = None
            if response is not None and response.status_code < 400:
                parser.parse(response.text.splitlines())
            else:
                parser.parse([])
            entry = _RobotsEntry(parser=parser, expires_at=now + self.ttl)
            self._entries[origin] = entry
        return entry.parser.can_fetch(user_agent, url)


class PublicWebFetcher:
    def __init__(
        self,
        *,
        client: httpx.AsyncClient | None = None,
        guard: ResourcePolicyGuard | None = None,
        robots: RobotsPolicyCache | None = None,
        user_agent: str = "",
        max_body_bytes: int = DEFAULT_MAX_HTML_BYTES,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        max_retries: int = 2,
        sleeper: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        self.client = client
        self.guard = guard or ResourcePolicyGuard()
        self.robots = robots or RobotsPolicyCache()
        self.user_agent = user_agent or os.environ.get(
            "OPENEXAM_RESOURCE_USER_AGENT",
            "OpenExam-ResourceOS/0.1 contact=openexam-local@example.invalid",
        )
        self.max_body_bytes = max_body_bytes
        self.max_redirects = max_redirects
        self.max_retries = max_retries
        self.sleeper = sleeper

    async def fetch(self, url: str) -> dict[str, str]:
        if self.client is not None:
            return await self._fetch(self.client, url)
        timeout = httpx.Timeout(20.0, connect=5.0)
        limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)
        async with httpx.AsyncClient(timeout=timeout, limits=limits, headers={"User-Agent": self.user_agent}) as client:
            return await self._fetch(client, url)

    async def _fetch(self, client: httpx.AsyncClient, url: str) -> dict[str, str]:
        current = self.guard.validate_url(url)
        for redirect_count in range(self.max_redirects + 1):
            if not await self.robots.allowed(client, self.guard, current, self.user_agent):
                raise RobotsDenied(f"Resource denied by robots.txt: {current}")
            response = await self._request(client, current)
            if response.is_redirect:
                if redirect_count >= self.max_redirects:
                    raise ResourceFetchError("Resource exceeded the maximum redirect count.")
                location = response.headers.get("location")
                if not location:
                    raise ResourceFetchError("Resource redirect did not include a location.")
                current = self.guard.validate_url(urljoin(current, location))
                continue
            if response.status_code >= 400:
                raise ResourceFetchError(f"Resource fetch failed with HTTP {response.status_code}.")
            content_length = response.headers.get("content-length")
            if content_length and int(content_length) > self.max_body_bytes:
                raise ResourceFetchError("Resource body exceeded the maximum allowed size.")
            body = await response.aread()
            if len(body) > self.max_body_bytes:
                raise ResourceFetchError("Resource body exceeded the maximum allowed size.")
            mime_type = response.headers.get("content-type", "text/plain").split(";", 1)[0].strip().lower()
            if not (
                mime_type.startswith("text/")
                or mime_type in {"application/json", "application/xml", "application/rss+xml", "application/atom+xml"}
            ):
                raise ResourceFetchError(f"Unsupported resource MIME type: {mime_type}")
            text = body.decode(response.encoding or "utf-8", errors="replace")
            if mime_type == "text/html":
                parser = _TextExtractor()
                parser.feed(text)
                text = parser.text()
            return {
                "url": current,
                "text": text.strip(),
                "mime_type": mime_type,
                "etag": response.headers.get("etag", ""),
                "last_modified": response.headers.get("last-modified", ""),
                "retrieved_at": datetime.now(UTC).isoformat(),
            }
        raise ResourceFetchError("Resource redirect processing failed.")

    async def _request(self, client: httpx.AsyncClient, url: str) -> httpx.Response:
        for attempt in range(self.max_retries + 1):
            try:
                response = await client.get(url, headers={"User-Agent": self.user_agent}, follow_redirects=False)
            except httpx.HTTPError as exc:
                if attempt >= self.max_retries:
                    raise ResourceFetchError(f"Resource request failed: {exc}") from exc
                await self.sleeper(float(2**attempt))
                continue
            if response.status_code not in {429, 500, 502, 503, 504} or attempt >= self.max_retries:
                return response
            retry_after = response.headers.get("retry-after", "")
            delay = float(retry_after) if retry_after.isdigit() else float(2**attempt)
            await self.sleeper(delay)
        raise ResourceFetchError("Resource retries were exhausted.")
