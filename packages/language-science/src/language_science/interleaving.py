"""Interleaving Builder V2 — domain-aware mixed practice with split adjacency maps."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


CFA_ADJACENCY: dict[str, list[str]] = {
    "NPV": ["IRR", "Payback Period", "Profitability Index"],
    "IRR": ["NPV", "Hurdle Rate", "Cost of Capital"],
    "Duration": ["Convexity", "Macaulay Duration", "Modified Duration"],
    "Macaulay Duration": ["Modified Duration", "Effective Duration", "Duration"],
    "Modified Duration": ["Macaulay Duration", "Effective Duration", "Duration"],
    "Yield to Maturity": ["Current Yield", "Yield to Call", "Holding Period Return"],
    "Sharpe Ratio": ["Treynor Ratio", "Sortino Ratio", "Information Ratio"],
    "Call Option": ["Put Option", "Forward Contract", "Futures Contract"],
    "Put Option": ["Call Option", "Forward Contract"],
    "LIFO": ["FIFO", "Weighted Average Cost", "Specific Identification"],
    "FIFO": ["LIFO", "Weighted Average Cost"],
    "Type I Error": ["Type II Error", "Significance Level", "Power of Test"],
    "Type II Error": ["Type I Error", "Power of Test"],
    "Fiscal Policy": ["Monetary Policy", "Government Spending", "Central Bank"],
    "Monetary Policy": ["Fiscal Policy", "Interest Rates", "Open Market Operations"],
    "DTA": ["DTL", "Deferred Tax", "Income Tax Expense"],
    "DTL": ["DTA", "Deferred Tax"],
    "WACC": ["Cost of Equity", "Cost of Debt", "CAPM"],
    "CAPM": ["WACC", "Cost of Equity", "Security Market Line"],
    "Operating Lease": ["Finance Lease", "Capital Lease", "Off-Balance Sheet"],
}

LANGUAGE_ADJACENCY: dict[str, list[str]] = {
    "its": ["it's", "his", "her"],
    "it's": ["its", "its"],
    "there": ["their", "they're", "here"],
    "their": ["there", "they're"],
    "they're": ["there", "their"],
    "affect": ["effect", "impact"],
    "effect": ["affect"],
    "principal": ["principle"],
    "principle": ["principal"],
    "accept": ["except"],
    "except": ["accept"],
    "than": ["then"],
    "then": ["than"],
    "less": ["fewer"],
    "fewer": ["less"],
    "who": ["whom"],
    "whom": ["who"],
}


@dataclass
class InterleavingMixV2:
    items: list[dict[str, Any]] = field(default_factory=list)
    composition: dict[str, int] = field(default_factory=dict)


@dataclass
class InterleavingConfigV2:
    weak_ratio: float = 0.40
    adjacent_ratio: float = 0.20
    maintenance_ratio: float = 0.20
    new_ratio: float = 0.20
    max_items: int = 20


class InterleavingBuilderV2:
    def __init__(self, domain: str = "language") -> None:
        self.domain = domain
        self.adjacency = CFA_ADJACENCY if domain == "cfa" else LANGUAGE_ADJACENCY

    def find_adjacent(self, canonical_form: str) -> list[str]:
        normalized = canonical_form.lower().strip()
        for key, related in self.adjacency.items():
            if key.lower() == normalized:
                return related
        return []

    def build(self, weak: list[dict[str, Any]], old: list[dict[str, Any]], maintenance: list[dict[str, Any]], new_items: list[dict[str, Any]] | None = None, config: InterleavingConfigV2 | None = None) -> InterleavingMixV2:
        cfg = config or InterleavingConfigV2()
        new_items = new_items or []
        max_items = cfg.max_items

        # Adjacent items are derived from weak items using adjacency map
        adjacent: list[dict[str, Any]] = []
        remaining_weak = list(weak)
        for item in weak:
            related = self.find_adjacent(item.get("canonical_form", ""))
            if related:
                adjacent.append(item)
                remaining_weak.remove(item)
                if len(adjacent) >= int(max_items * cfg.adjacent_ratio):
                    break

        # Allocate slots per bucket
        weak_count = min(len(remaining_weak), int(max_items * cfg.weak_ratio))
        adjacent_count = min(len(adjacent), int(max_items * cfg.adjacent_ratio))
        maintenance_count = min(len(maintenance), int(max_items * cfg.maintenance_ratio))
        new_count = min(len(new_items), int(max_items * cfg.new_ratio))

        # Fill remaining with weak
        allocated = weak_count + adjacent_count + maintenance_count + new_count
        if allocated < max_items:
            extra = min(len(remaining_weak) - weak_count, max_items - allocated)
            weak_count += extra

        interleaved = []
        buckets = [
            (remaining_weak[:weak_count], "weak"),
            (adjacent[:adjacent_count], "adjacent"),
            (maintenance[:maintenance_count], "maintenance"),
            (new_items[:new_count], "new"),
        ]
        while any(bucket for bucket, _ in buckets):
            for bucket, label in buckets:
                if bucket:
                    item = bucket.pop(0)
                    item.setdefault("_interleaving_label", label)
                    interleaved.append(item)

        composition = {"weak": weak_count, "adjacent": adjacent_count, "maintenance": maintenance_count, "new": new_count}
        return InterleavingMixV2(items=interleaved, composition=composition)
