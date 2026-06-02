from __future__ import annotations

from dataclasses import asdict, dataclass
import os
from typing import Any
from urllib.parse import urlencode


@dataclass(frozen=True, slots=True)
class ProviderSpec:
    provider_id: str
    label: str
    modes: tuple[str, ...]
    required_env: str = ""
    default_license_mode: str = "metadata_only"
    request_limit_per_second: int = 2

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["modes"] = list(self.modes)
        payload["configured"] = not self.required_env or bool(os.environ.get(self.required_env))
        payload["health"] = "ready" if payload["configured"] else "missing_key"
        return payload


PROVIDERS = (
    ProviderSpec("generic_web", "Generic Web", ("crawl",), default_license_mode="metadata_only"),
    ProviderSpec("rss_atom", "RSS / Atom", ("subscribe", "discover"), default_license_mode="metadata_only"),
    ProviderSpec("sitemap", "Sitemap", ("subscribe", "discover"), default_license_mode="metadata_only"),
    ProviderSpec("youtube_metadata", "YouTube Metadata", ("discover",), required_env="YOUTUBE_API_KEY", default_license_mode="metadata_only"),
    ProviderSpec("openalex", "OpenAlex", ("discover",), required_env="OPENALEX_API_KEY"),
    ProviderSpec("arxiv", "arXiv", ("discover",), default_license_mode="metadata_only"),
    ProviderSpec("sec_edgar", "SEC EDGAR", ("discover", "crawl"), default_license_mode="official_structured", request_limit_per_second=5),
    ProviderSpec("fred", "FRED", ("discover", "crawl"), required_env="FRED_API_KEY", default_license_mode="official_structured"),
    ProviderSpec("world_bank", "World Bank", ("discover", "crawl"), default_license_mode="official_structured"),
    ProviderSpec("openai_web_search", "OpenAI Web Search", ("ai_discover",), required_env="OPENAI_API_KEY"),
)


def list_provider_specs() -> list[dict[str, Any]]:
    return [provider.as_dict() for provider in PROVIDERS]


def get_provider_spec(provider_id: str) -> dict[str, Any]:
    for provider in PROVIDERS:
        if provider.provider_id == provider_id:
            return provider.as_dict()
    raise KeyError(provider_id)


def build_provider_discovery_url(provider_id: str, query: str) -> str:
    spec = get_provider_spec(provider_id)
    if not spec["configured"]:
        raise PermissionError(f"Provider {provider_id} requires {spec['required_env']}.")
    if provider_id == "youtube_metadata":
        return "https://www.googleapis.com/youtube/v3/search?" + urlencode(
            {"part": "snippet", "type": "video", "maxResults": 20, "q": query, "key": os.environ["YOUTUBE_API_KEY"]}
        )
    if provider_id == "openalex":
        return "https://api.openalex.org/works?" + urlencode({"search": query, "api_key": os.environ["OPENALEX_API_KEY"]})
    if provider_id == "arxiv":
        return "https://export.arxiv.org/api/query?" + urlencode({"search_query": f"all:{query}", "max_results": 20})
    if provider_id == "fred":
        return "https://api.stlouisfed.org/fred/series/search?" + urlencode(
            {"search_text": query, "api_key": os.environ["FRED_API_KEY"], "file_type": "json"}
        )
    if provider_id == "world_bank":
        return "https://api.worldbank.org/v2/indicator?" + urlencode({"format": "json", "source": 2, "per_page": 50})
    if provider_id == "sec_edgar":
        return "https://www.sec.gov/edgar/search/#/q=" + query.replace(" ", "%20")
    raise ValueError(f"Provider {provider_id} does not support query discovery.")
