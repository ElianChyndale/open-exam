from __future__ import annotations

from defusedxml import ElementTree


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_feed_urls(text: str) -> list[str]:
    root = ElementTree.fromstring(text)
    urls: list[str] = []
    for node in root.iter():
        name = _local_name(node.tag)
        if name == "link":
            value = (node.get("href") or node.text or "").strip()
            if value.startswith(("http://", "https://")):
                urls.append(value)
    return list(dict.fromkeys(urls))


def parse_sitemap_urls(text: str) -> list[str]:
    root = ElementTree.fromstring(text)
    urls = [
        (node.text or "").strip()
        for node in root.iter()
        if _local_name(node.tag) == "loc" and (node.text or "").strip().startswith(("http://", "https://"))
    ]
    return list(dict.fromkeys(urls))
