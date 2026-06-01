from __future__ import annotations

from math import exp


class HalfLifeEstimator:
    @staticmethod
    def recall_probability(*, half_life_days: float, elapsed_days: float) -> float:
        if half_life_days <= 0:
            raise ValueError("half_life_days must be positive.")
        return round(2 ** (-max(0.0, elapsed_days) / half_life_days), 6)


class RaschModel:
    @staticmethod
    def probability(*, ability: float, difficulty: float) -> float:
        return 1.0 / (1.0 + exp(-(ability - difficulty)))


class BayesianKnowledgeTrace:
    @staticmethod
    def update(
        prior: float,
        *,
        correct: bool,
        learn_rate: float = 0.12,
        guess_rate: float = 0.2,
        slip_rate: float = 0.1,
    ) -> float:
        prior = max(0.0, min(1.0, prior))
        likelihood_known = 1 - slip_rate if correct else slip_rate
        likelihood_unknown = guess_rate if correct else 1 - guess_rate
        denominator = likelihood_known * prior + likelihood_unknown * (1 - prior)
        posterior = (likelihood_known * prior / denominator) if denominator else prior
        return round(posterior + (1 - posterior) * learn_rate, 6)
