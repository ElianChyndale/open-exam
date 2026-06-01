from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PedagogyDecision:
    strategy: str
    reason: str


class PedagogyPolicy:
    @staticmethod
    def select(*, error_type: str, confidence: int, energy_level: int) -> PedagogyDecision:
        if energy_level <= 1:
            return PedagogyDecision("light_retrieval", "Low energy: use a short active-recall task.")
        if error_type == "concept_confusion" and confidence >= 3:
            return PedagogyDecision("contrast_pair", "High-confidence confusion benefits from explicit discrimination.")
        if error_type == "formula_misuse":
            return PedagogyDecision("worked_example_fading", "Formula errors need scaffolded practice before independent recall.")
        return PedagogyDecision("active_recall", "Default to retrieval practice with immediate feedback.")
