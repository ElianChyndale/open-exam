"""Worked Example Fader — graduated guidance from examples to independence.

Based on cognitive load theory and worked example effect (SAGE 2020,
Sweller et al.). When a learner repeatedly fails a problem type, provide
a sequence of fading worked examples rather than letting them keep failing.

Sequence: full example → completion (hidden steps) → independent solving
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class FadeStage(str, Enum):
    """Stages of worked example fading."""
    FULL_EXAMPLE = "full_example"         # complete worked solution shown
    COMPLETION = "completion"             # some steps hidden, learner fills in
    INDEPENDENT = "independent"           # learner solves from scratch


@dataclass(slots=True)
class WorkedExample:
    """A worked example with configurable fading."""
    example_id: str
    topic: str
    los: str
    problem_statement: str
    solution_steps: list[str]              # complete solution steps
    hidden_step_indices: list[int] = field(default_factory=list)  # which steps to hide
    hints: list[str] = field(default_factory=list)  # hints for hidden steps
    final_answer: str = ""


@dataclass(slots=True)
class FadingSequence:
    """A sequence of fading worked examples for one problem type."""
    examples: list[WorkedExample] = field(default_factory=list)
    current_stage: FadeStage = FadeStage.FULL_EXAMPLE
    attempts_at_stage: int = 0
    successes_at_stage: int = 0


class WorkedExampleFader:
    """Manage the fading of worked examples.

    Rules:
    - First encounter → full example
    - 2nd encounter → completion (hide 1-2 key steps)
    - 3rd+ encounter → independent with hint available
    - If learner fails at any stage → revert to previous stage
    """

    REQUIRED_SUCCESSES_TO_ADVANCE = 2      # must succeed twice to advance
    MAX_FAILURES_BEFORE_REVERT = 1         # revert after one failure

    @classmethod
    def build_sequence(
        cls,
        topic: str,
        los: str,
        problem_template: str,
        solution_steps: list[str],
        num_examples: int = 3,
    ) -> FadingSequence:
        """Build a fading sequence for a problem type."""
        sequence = FadingSequence()

        for i in range(num_examples):
            hidden: list[int] = []
            hints: list[str] = []
            stage = FadeStage.FULL_EXAMPLE

            if i == 0:
                # First: full example, nothing hidden
                stage = FadeStage.FULL_EXAMPLE
            elif i == 1:
                # Second: hide ~30% of steps (key steps)
                stage = FadeStage.COMPLETION
                if len(solution_steps) >= 3:
                    hidden = [len(solution_steps) // 2]  # hide middle step
                    hints = ["先写出这一步的公式定义，再代入数值。"]
                elif solution_steps:
                    hidden = [len(solution_steps) - 1]  # hide last
                    hints = ["用上一步的结果继续推算。"]
            else:
                # Third+: independent
                stage = FadeStage.INDEPENDENT
                hidden = list(range(len(solution_steps)))
                hints = ["如果需要帮助，回顾上一个例题的解法结构。"]

            example = WorkedExample(
                example_id=f"we-{topic}-{los}-{i+1}",
                topic=topic,
                los=los,
                problem_statement=problem_template,
                solution_steps=list(solution_steps),
                hidden_step_indices=hidden,
                hints=hints,
                final_answer=solution_steps[-1] if solution_steps else "",
            )
            sequence.examples.append(example)

        sequence.current_stage = FadeStage.FULL_EXAMPLE
        return sequence

    @classmethod
    def assess_and_advance(
        cls,
        sequence: FadingSequence,
        was_correct: bool,
    ) -> FadeStage:
        """Record an attempt result and return the next stage."""
        sequence.attempts_at_stage += 1

        if was_correct:
            sequence.successes_at_stage += 1
            if sequence.successes_at_stage >= cls.REQUIRED_SUCCESSES_TO_ADVANCE:
                # Advance to next stage
                stages = list(FadeStage)
                current_idx = stages.index(sequence.current_stage)
                next_idx = min(current_idx + 1, len(stages) - 1)
                sequence.current_stage = stages[next_idx]
                sequence.attempts_at_stage = 0
                sequence.successes_at_stage = 0
        else:
            # Failure: revert to previous stage if possible
            if sequence.attempts_at_stage >= cls.MAX_FAILURES_BEFORE_REVERT:
                stages = list(FadeStage)
                current_idx = stages.index(sequence.current_stage)
                prev_idx = max(current_idx - 1, 0)
                sequence.current_stage = stages[prev_idx]
                sequence.attempts_at_stage = 0
                sequence.successes_at_stage = 0

        return sequence.current_stage

    @classmethod
    def should_use_worked_examples(
        cls,
        consecutive_failures: int,
        error_type: str,
    ) -> bool:
        """Determine if worked example fading should be activated."""
        if consecutive_failures >= 3:
            return True
        if error_type in {"formula_misuse", "knowledge_gap"} and consecutive_failures >= 2:
            return True
        return False
