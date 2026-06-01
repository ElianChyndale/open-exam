from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimulationResult:
    sessions: int
    initial_mastery: float
    final_mastery: float


class SimulationLab:
    @staticmethod
    def run(*, initial_mastery: float, sessions: int, learning_rate: float = 0.12) -> SimulationResult:
        mastery = max(0.0, min(1.0, initial_mastery))
        for _ in range(max(0, sessions)):
            mastery += (1 - mastery) * learning_rate
        return SimulationResult(sessions=max(0, sessions), initial_mastery=initial_mastery, final_mastery=round(mastery, 6))
