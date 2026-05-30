"""Interleaving Builder — mixed practice across topics.

Based on interleaved practice research (MIT Open Learning, Dunlosky 2013).
Mixes different topics/LOS in practice sessions to improve discrimination.

Default ratio from PLAN.md:
- 60% current weaknesses
- 20% old mistakes
- 10% easy-to-confuse adjacent topics
- 10% maintenance (previously mastered)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class InterleavingMix:
    """A mixed set of practice items."""
    items: list[dict] = field(default_factory=list)
    composition: dict[str, int] = field(default_factory=dict)  # bucket → count


@dataclass(slots=True)
class InterleavingConfig:
    """Configuration for interleaving ratios."""
    weak_ratio: float = 0.60       # current weaknesses
    old_mistake_ratio: float = 0.20  # old mistakes
    adjacent_ratio: float = 0.10   # easy-to-confuse adjacent
    maintenance_ratio: float = 0.10  # maintenance
    max_items: int = 20


class InterleavingBuilder:
    """Build interleaved practice sets.

    Instead of blocked practice (all items from one topic),
    this builder creates mixed sets that force the learner to
    identify which concept applies before solving.
    """

    # Adjacent topics that are commonly confused
    ADJACENCY_MAP: dict[str, list[str]] = {
        "NPV": ["IRR", "PI", "Payback Period"],
        "IRR": ["NPV", "ROIC", "WACC"],
        "Spot Rate": ["Forward Rate", "Par Rate", "YTM"],
        "Forward Rate": ["Spot Rate", "Futures Price", "Swap Rate"],
        "Fiscal Policy": ["Monetary Policy", "Supply-Side Policy"],
        "Monetary Policy": ["Fiscal Policy", "Exchange Rate Policy"],
        "Call Option": ["Put Option", "Forward", "Futures"],
        "Put Option": ["Call Option", "Forward", "Futures"],
        "LIFO": ["FIFO", "Weighted Average Cost", "Specific Identification"],
        "FIFO": ["LIFO", "Weighted Average Cost", "Specific Identification"],
        "Operating Lease": ["Finance Lease", "Service Contract"],
        "Finance Lease": ["Operating Lease", "Purchase"],
    }

    @classmethod
    def find_adjacent_topics(cls, topic: str, los: str, formula_ids: list[str]) -> list[str]:
        """Find commonly confused adjacent topics."""
        adjacent: list[str] = []

        # Check direct topic matches
        for key, neighbors in cls.ADJACENCY_MAP.items():
            if key.lower() in topic.lower() or key.lower() in los.lower():
                adjacent.extend(neighbors)

        # Check formula cross-references
        for fid in formula_ids:
            for key, neighbors in cls.ADJACENCY_MAP.items():
                if key.lower() in fid.lower():
                    adjacent.extend(neighbors)

        return list(dict.fromkeys(adjacent))  # deduplicate, preserve order

    @classmethod
    def build(
        cls,
        weak_items: list[dict],
        old_mistake_items: list[dict],
        maintenance_items: list[dict],
        config: InterleavingConfig | None = None,
    ) -> InterleavingMix:
        """Build an interleaved practice set.

        Items are shuffled within each bucket, then interleaved
        across buckets according to the ratio config.
        """
        import random

        cfg = config or InterleavingConfig()
        num = cfg.max_items

        # Allocate counts
        n_weak = max(1, int(num * cfg.weak_ratio))
        n_old = max(0, int(num * cfg.old_mistake_ratio))
        n_adjacent = max(0, int(num * cfg.adjacent_ratio))
        n_maintenance = num - n_weak - n_old - n_adjacent

        # Select items from each bucket
        def pick(items: list[dict], n: int) -> list[dict]:
            if not items:
                return []
            shuffled = list(items)
            random.shuffle(shuffled)
            # Prefer higher priority items
            shuffled.sort(key=lambda x: -(x.get("priority", 0) or 0))
            return shuffled[:n]

        selected_weak = pick(weak_items, n_weak)
        selected_old = pick(old_mistake_items, n_old)
        selected_maintenance = pick(maintenance_items, n_maintenance)

        # For adjacent items, derive from weak items' adjacency
        adjacent_items: list[dict] = []
        for item in selected_weak:
            adj_topics = cls.find_adjacent_topics(
                item.get("topic", ""),
                item.get("los", ""),
                item.get("formula_ids", []),
            )
            for adj in adj_topics:
                # Find matching maintenance items tagged with this adjacent topic
                for maint in maintenance_items:
                    if adj.lower() in maint.get("topic", "").lower():
                        adjacent_items.append(maint)
                        break
        adjacent_items = pick(adjacent_items, n_adjacent)

        # Interleave: round-robin across buckets
        buckets = [
            ("weak", selected_weak),
            ("old_mistake", selected_old),
            ("adjacent", adjacent_items),
            ("maintenance", selected_maintenance),
        ]

        interleaved: list[dict] = []
        bucket_iterators = {name: iter(items) for name, items in buckets if items}
        active = list(bucket_iterators.keys())
        random.shuffle(active)

        while active:
            next_active: list[str] = []
            for name in active:
                try:
                    item = next(bucket_iterators[name])
                    item["interleave_bucket"] = name
                    interleaved.append(item)
                    next_active.append(name)
                except StopIteration:
                    continue
            if not next_active:
                break
            random.shuffle(next_active)
            active = next_active

        composition = {
            "weak": len(selected_weak),
            "old_mistakes": len(selected_old),
            "adjacent": len(adjacent_items),
            "maintenance": len(selected_maintenance),
        }

        return InterleavingMix(items=interleaved, composition=composition)
