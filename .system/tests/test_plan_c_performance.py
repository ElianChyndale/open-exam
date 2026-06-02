"""Performance benchmarks for Plan C modules."""

from __future__ import annotations

from time import monotonic

from language_science.scheduler import FSRS6Scheduler
from language_science.fsrs_cache import FSRSStateCache


def test_fsrs_schedule_throughput():
    """FSRS-6 should handle 1000 reviews in under 2.0s (real py-fsrs library)."""
    state = None
    start = monotonic()
    for i in range(1000):
        state = FSRS6Scheduler.schedule(state, "good")
        state = state.as_dict() if hasattr(state, 'as_dict') else state
    elapsed = monotonic() - start
    assert elapsed < 2.0, f"FSRS-6 1000 reviews took {elapsed:.2f}s, expected <2.0s"


def test_cache_throughput():
    """Cache should handle 10000 lookups in under 0.1s."""
    cache = FSRSStateCache(maxsize=1024)
    for i in range(1000):
        cache.get_or_compute(f"card-{i}", lambda: {"s": 1.0})
    hits = 0
    start = monotonic()
    for i in range(10000):
        key = f"card-{i % 1000}"
        if key in cache._cache:
            hits += 1
        cache.get_or_compute(key, lambda: {"s": 1.0})
    elapsed = monotonic() - start
    assert elapsed < 0.1, f"Cache 10000 lookups took {elapsed:.2f}s, expected <0.1s"


def test_confusion_map_lookup_throughput():
    """Confusion map should handle 10000 lookups in under 0.1s."""
    from language_science.confusion_map import lookup_confusions
    start = monotonic()
    for _ in range(10000):
        lookup_confusions("duration", domain="cfa")
        lookup_confusions("its", domain="language")
    elapsed = monotonic() - start
    assert elapsed < 0.1, f"Confusion map 20000 lookups took {elapsed:.2f}s"


def test_difficulty_estimator_throughput():
    """Difficulty estimator should handle 1000 estimates in under 0.2s."""
    from language_science.difficulty import AdaptiveDifficultyEstimator
    est = AdaptiveDifficultyEstimator(domain="cfa")
    start = monotonic()
    for _ in range(1000):
        est.estimate("duration", context="bond duration")
    elapsed = monotonic() - start
    assert elapsed < 0.2, f"Difficulty 1000 estimates took {elapsed:.2f}s"
