from __future__ import annotations

from collections.abc import Callable, Iterable
import ipaddress
import socket
from urllib.parse import urlsplit, urlunsplit


LICENSE_MODES = {
    "metadata_only",
    "fulltext_allowed",
    "official_structured",
    "user_supplied_only",
    "quarantined",
}
FULLTEXT_LICENSE_MODES = {"fulltext_allowed", "official_structured", "user_supplied_only"}
DEFAULT_MAX_HTML_BYTES = 5 * 1024 * 1024
DEFAULT_MAX_REDIRECTS = 5
DEFAULT_DOMAIN_CONCURRENCY = 2
DEFAULT_SUBSCRIPTION_BUDGET = 50


class UnsafeResourceURL(ValueError):
    """Raised when a URL is not safe for deterministic public-web fetching."""


def _resolve_host(host: str) -> list[str]:
    return sorted({str(item[4][0]) for item in socket.getaddrinfo(host, None)})


def _is_public_address(value: str) -> bool:
    address = ipaddress.ip_address(value)
    return address.is_global


class ResourcePolicyGuard:
    def __init__(self, *, resolver: Callable[[str], Iterable[str]] | None = None) -> None:
        self.resolver = resolver or _resolve_host

    def validate_url(self, url: str) -> str:
        parts = urlsplit(url.strip())
        if parts.scheme.lower() not in {"http", "https"}:
            raise UnsafeResourceURL("Resource URL scheme must be http or https.")
        if not parts.hostname:
            raise UnsafeResourceURL("Resource URL must include a hostname.")
        hostname = parts.hostname.lower().rstrip(".")
        if hostname == "localhost" or hostname.endswith(".localhost"):
            raise UnsafeResourceURL("Resource URL must resolve to the public internet.")
        try:
            addresses = list(self.resolver(hostname))
        except OSError as exc:
            raise UnsafeResourceURL(f"Resource hostname could not be resolved: {hostname}") from exc
        if not addresses or any(not _is_public_address(address) for address in addresses):
            raise UnsafeResourceURL("Resource URL must resolve only to the public internet.")
        return urlunsplit((parts.scheme.lower(), parts.netloc, parts.path or "/", parts.query, parts.fragment))


def can_retain_fulltext(license_mode: str) -> bool:
    if license_mode not in LICENSE_MODES:
        raise ValueError(f"Unsupported resource license mode: {license_mode}")
    return license_mode in FULLTEXT_LICENSE_MODES
