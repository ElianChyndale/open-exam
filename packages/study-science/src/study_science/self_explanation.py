"""Self-Explanation Prompt — concise post-error reflection.

Based on self-explanation effect (Dunlosky 2013, Chi et al.).
Prompts the learner to explain why the correct answer is correct
and why their answer was wrong — but keeps it brief.

PLAN.md rule: "每道错题只问极短复盘，不要求写长文"
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PromptStyle(str, Enum):
    """Self-explanation prompt styles by error type."""
    CONCEPT = "concept"       # "为什么A是对的而B是错的？"
    FORMULA = "formula"       # "哪一步计算出了错？正确的计算链是什么？"
    PROCEDURE = "procedure"   # "应该先判断什么再判断什么？"
    TRAP = "trap"             # "题目在哪个词上设了陷阱？"


@dataclass(slots=True)
class SelfExplanationResult:
    """User's self-explanation response."""
    prompt: str
    user_response: str = ""
    quality_score: int = 0    # 0-3 heuristic score
    was_completed: bool = False


class SelfExplanationPrompt:
    """Generate short, targeted self-explanation prompts.

    Never asks for long essays. Each prompt targets exactly one
    cognitive operation: identify the mistake, explain the correct
    reasoning, or extract a rule.
    """

    PROMPT_TEMPLATES = {
        "concept_confusion": [
            "用一句话说出：为什么 `{correct}` 是对的，而你的答案错了？",
            "这道题考的是哪个概念的哪个边界？用 20 个字回答。",
            "把 `{topic}` / `{los}` 的关键判断标准写下来（一句即可）。",
        ],
        "formula_misuse": [
            "写出正确的计算步骤（只写步骤，不写解释）。",
            "你在哪一步用错了公式？正确的公式是什么？",
            "把这道题的正确计算链写下来（≤3 行）。",
        ],
        "careless_reading": [
            "原文哪个词/数字你读漏了？用引号标出来。",
            "重新读题：题目问的是什么？（≤10 字）",
        ],
        "time_pressure": [
            "这道题你花了多久？如果时间正常，你会怎么判断？",
        ],
        "confidence_calibration_failure": [
            "你觉得对但实际错了——你的判断依据是什么？写出来看看。",
            "你确定的地方，跟正确答案的差距在哪？",
        ],
        "knowledge_gap": [
            "这道题需要你知道什么？查资料后补一句定义。",
        ],
        "fatigue_energy_mismatch": [
            "做题时的状态如何？如果精力好，这题会不会对？",
        ],
    }

    FALLBACK_PROMPT = "这道题我错在哪里？（一句话）"

    @classmethod
    def generate(
        cls,
        error_type: str,
        topic: str = "",
        los: str = "",
        correct_answer: str = "",
        user_answer: str = "",
        question_stem: str = "",
    ) -> str:
        """Generate a single concise self-explanation prompt."""
        templates = cls.PROMPT_TEMPLATES.get(error_type, [cls.FALLBACK_PROMPT])

        # Use first template for simplicity, or rotate based on attempt count
        template = templates[0]

        # Fill in variables
        prompt = template.format(
            topic=topic,
            los=los,
            correct=correct_answer[:100] if correct_answer else "正确答案",
            wrong=user_answer[:100] if user_answer else "你的答案",
            question=question_stem[:80] if question_stem else "这道题",
        )

        # Truncate to keep it short
        if len(prompt) > 120:
            prompt = prompt[:117] + "..."

        return prompt

    @classmethod
    def evaluate_quality(cls, prompt: str, response: str) -> int:
        """Heuristically score self-explanation quality (0-3).

        0 = no response or "idk"
        1 = vague / surface-level
        2 = specific but incomplete
        3 = specific, identifies root cause
        """
        if not response.strip() or response.strip().lower() in {"idk", "不知道", "不知道。"}:
            return 0
        if len(response.strip()) < 5:
            return 1
        # Check for specificity signals
        has_specific = any(
            marker in response.lower()
            for marker in ["因为", "because", "所以", "therefore", "公式", "formula", "计算", "calc"]
        )
        if has_specific and len(response) > 15:
            return 3
        if len(response) > 10:
            return 2
        return 1
