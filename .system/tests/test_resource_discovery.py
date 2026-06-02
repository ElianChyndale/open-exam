from __future__ import annotations


def test_rss_atom_and_sitemap_discovery_extract_public_candidates() -> None:
    from resource_ingestion.discovery import parse_feed_urls, parse_sitemap_urls

    rss = """<?xml version="1.0"?><rss><channel><item><link>https://example.com/a</link></item></channel></rss>"""
    atom = """<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry><link href="https://example.com/b"/></entry></feed>"""
    sitemap = """<?xml version="1.0"?><urlset><url><loc>https://example.com/c</loc></url></urlset>"""

    assert parse_feed_urls(rss) == ["https://example.com/a"]
    assert parse_feed_urls(atom) == ["https://example.com/b"]
    assert parse_sitemap_urls(sitemap) == ["https://example.com/c"]
