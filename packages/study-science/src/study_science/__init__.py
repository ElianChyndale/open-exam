"""Study Science — cognitive science engines for the ExamOS platform.

Seven engines:
- RetrievalEngine: active recall before passive review
- SpacingScheduler: optimal review spacing based on confidence, correctness, exam date
- InterleavingBuilder: mixed practice across topics
- WorkedExampleFader: worked example → completion → independent solving
- SelfExplanationPrompt: concise post-error reflection prompts
- ConfidenceCalibration: detect and prioritize high-confidence errors
- EnergyAwarePlanner: align task difficulty with energy levels
"""

from study_science.retrieval import RetrievalEngine
from study_science.spacing import SpacingScheduler
from study_science.interleaving import InterleavingBuilder
from study_science.worked_example import WorkedExampleFader
from study_science.self_explanation import SelfExplanationPrompt
from study_science.calibration import ConfidenceCalibration
from study_science.energy_planner import EnergyAwarePlanner

__all__ = [
    "RetrievalEngine",
    "SpacingScheduler",
    "InterleavingBuilder",
    "WorkedExampleFader",
    "SelfExplanationPrompt",
    "ConfidenceCalibration",
    "EnergyAwarePlanner",
]
