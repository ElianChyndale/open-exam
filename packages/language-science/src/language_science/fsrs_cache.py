"""LRU cache for computed FSRS states — eliminates O(n*m) replay scans."""

from __future__ import annotations

from typing import Any, Callable


class FSRSStateCache:
    """Per-session LRU cache keyed by card_id.

    Usage:
        cache = FSRSStateCache(maxsize=256)
        cache.get_or_compute(card_id, lambda: expensive_compute())
        cache.invalidate(card_id)  # on state change
    """

    def __init__(self, maxsize: int = 256) -> None:
        self._maxsize = maxsize
        self._cache: dict[str, dict[str, Any]] = {}
        self._hits = 0
        self._misses = 0

    def get_or_compute(self, key: str, compute: Callable[[], dict[str, Any]]) -> dict[str, Any]:
        if key in self._cache:
            self._hits += 1
            return self._cache[key]
        self._misses += 1
        value = compute()
        if len(self._cache) >= self._maxsize:
            self._cache.pop(next(iter(self._cache)))
        self._cache[key] = value
        return value

    def invalidate(self, key: str) -> None:
        self._cache.pop(key, None)

    def invalidate_many(self, keys: list[str]) -> None:
        for key in keys:
            self._cache.pop(key, None)

    def reset(self) -> None:
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    @property
    def hit_ratio(self) -> float:
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0
