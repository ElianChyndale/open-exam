"""Retrieval Engine — active recall before passive review.

Based on the testing effect (Dunlosky et al. 2013, Nature Reviews Psych 2022).
Every learning action should begin with retrieval attempt, not reading.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(slots=True)
class RetrievalPrompt:
    """A retrieval prompt to be answered before seeing the answer."""
    prompt_id: str
    prompt_text: str           # what the user should try to recall
    answer_text: str           # the correct answer (hidden initially)
    topic: str = ""
    los: str = ""
    retrieval_type: str = ""   # "definition", "formula", "concept_boundary", "procedure"


@dataclass(slots=True)
class RetrievalSession:
    """An active retrieval session."""
    prompts: list[RetrievalPrompt] = field(default_factory=list)
    recall_scores: list[int] = field(default_factory=list)  # 0-4 per prompt
    started_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class RetrievalEngine:
    """Generate retrieval prompts and score recall quality.

    Principle: every review starts with "what do you remember?"
    before showing any answer or explanation. The act of retrieval
    itself strengthens memory (testing effect).
    """

    RETRIEVAL_TYPES = {
        "concept_confusion": "concept_boundary",
        "formula_misuse": "formula",
        "knowledge_gap": "definition",
        "careless_reading": "procedure",
        "time_pressure": "procedure",
        "confidence_calibration_failure": "concept_boundary",
        "fatigue_energy_mismatch": "definition",
        "agent_failure": "procedure",
    }

    @staticmethod
    def build_prompts(
        topic: str,
        los: str,
        error_type: str,
        correct_resolution: str,
        question_prompt: str = "",
        count: int = 3,
    ) -> list[RetrievalPrompt]:
        """Build a set of retrieval prompts for a topic/LOS/error combination."""
        retrieval_type = RetrievalEngine.RETRIEVAL_TYPES.get(error_type, "definition")
        prompts: list[RetrievalPrompt] = []

        # Always include: "what is the core concept/rule?"
        prompts.append(
            RetrievalPrompt(
                prompt_id=f"ret-{topic}-{los}-core",
                prompt_text=f"闭卷讲出 {topic} / {los} 的核心定义和判断边界。",
                answer_text=correct_resolution,
                topic=topic,
                los=los,
                retrieval_type=retrieval_type,
            )
        )

        # If formula-related: "write the formula from memory"
        if retrieval_type == "formula":
            prompts.append(
                RetrievalPrompt(
                    prompt_id=f"ret-{topic}-{los}-formula",
                    prompt_text=f"默写 {los} 的核心公式（含所有变量定义）。",
                    answer_text=correct_resolution,
                    topic=topic,
                    los=los,
                    retrieval_type="formula",
                )
            )

        # If concept boundary: "what's the easy-miss distinction?"
        if retrieval_type == "concept_boundary":
            prompts.append(
                RetrievalPrompt(
                    prompt_id=f"ret-{topic}-{los}-boundary",
                    prompt_text=f"{los} 最容易跟哪个概念混淆？用一句话划清边界。",
                    answer_text=correct_resolution,
                    topic=topic,
                    los=los,
                    retrieval_type="concept_boundary",
                )
            )

        # If question prompt is available: "re-solve without seeing options"
        if question_prompt:
            prompts.append(
                RetrievalPrompt(
                    prompt_id=f"ret-{topic}-{los}-resolve",
                    prompt_text=f"闭卷重做这题，先不看选项：\n{question_prompt[:200]}",
                    answer_text=correct_resolution,
                    topic=topic,
                    los=los,
                    retrieval_type="procedure",
                )
            )

        return prompts[:count]

    @staticmethod
    def score_recall(prompt: RetrievalPrompt, user_response: str) -> int:
        """Score a retrieval attempt (0-4).

        0 = no recall
        1 = fragmentary
        2 = partial but missing key elements
        3 = mostly correct
        4 = perfect recall
        """
        if not user_response.strip():
            return 0
        # Simple heuristic: measure overlap and length adequacy
        answer_tokens = set(prompt.answer_text.lower().split())
        response_tokens = set(user_response.lower().split())
        if not answer_tokens:
            return 2
        overlap = len(answer_tokens & response_tokens) / len(answer_tokens)
        if overlap >= 0.9:
            return 4
        if overlap >= 0.6:
            return 3
        if overlap >= 0.3:
            return 2
        return 1 if overlap > 0 else 0
