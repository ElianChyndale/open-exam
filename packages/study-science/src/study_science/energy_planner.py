"""Energy-Aware Planner — align tasks with energy levels.

Based on MIT Learning Strategies Assessment (wellbeing + cognition)
and PLAN.md energy-task mapping:
- High energy: new knowledge, difficult practice, interleaved sets, mock
- Moderate energy: mistake review, formula application, worked example fading
- Low energy: active recall cards, concept discrimination, light review

Key insight: don't push new learning when fatigued — it creates
weak memory traces and increases calibration errors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(slots=True)
class EnergyProfile:
    """User's energy profile for a session."""
    energy_level: int = 2            # 0-4 (depleted → peak)
    mental_clarity: int = 5          # 1-10
    physical_fatigue: int = 5        # 1-10 (higher = more tired)
    motivation: int = 5              # 1-10
    time_of_day: str = ""            # "morning", "afternoon", "evening"
    available_minutes: int = 120
    sleep_hours: float = 0.0         # 0 = not reported
    stress_level: int = 0            # 0 = not reported, 1-10


@dataclass(slots=True)
class TaskEnergyFit:
    """How well a task fits the current energy level."""
    task_type: str
    task_description: str
    energy_required: int             # 0-4 minimum energy needed
    fit_score: float = 1.0           # 0.0-1.0, higher = better fit
    recommendation: str = ""


@dataclass(slots=True)
class EnergyPlan:
    """A complete energy-aware task allocation."""
    profile: EnergyProfile
    high_energy_slot: list[TaskEnergyFit] = field(default_factory=list)
    moderate_energy_slot: list[TaskEnergyFit] = field(default_factory=list)
    low_energy_slot: list[TaskEnergyFit] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class EnergyAwarePlanner:
    """Plan study tasks based on current energy level.

    Task-to-energy mapping:
    - Energy 3-4 (high/peak): new knowledge, difficult practice, interleaved, mock
    - Energy 2 (moderate): mistake review, formula drills, worked example fading
    - Energy 1 (low): active recall, concept discrimination, light review
    - Energy 0 (depleted): only passive review or rest (recommend rest)
    """

    # Task types → minimum energy level required
    ENERGY_REQUIREMENTS = {
        "new_knowledge": 3,              # requires high focus
        "difficult_practice": 3,         # requires high cognitive load
        "interleaved_set": 3,            # requires discrimination ability
        "mock_exam": 4,                  # requires peak performance
        "mistake_review": 2,             # moderate focus OK
        "formula_drill": 2,              # pattern application
        "worked_example_fading": 2,      # structured guidance OK
        "active_recall": 1,              # low cognitive load
        "concept_discrimination": 1,     # quick judgments
        "light_review": 0,               # passive OK
    }

    # Task descriptions
    TASK_LABELS = {
        "new_knowledge": "新知识学习",
        "difficult_practice": "高难度练习题",
        "interleaved_set": "交错题组",
        "mock_exam": "模拟考试",
        "mistake_review": "错题复盘",
        "formula_drill": "公式应用练习",
        "worked_example_fading": "例题渐隐练习",
        "active_recall": "主动回忆卡",
        "concept_discrimination": "易混概念判断",
        "light_review": "轻量复习",
    }

    @classmethod
    def fit_score(cls, task_type: str, energy_level: int) -> float:
        """Calculate how well a task fits the current energy level.

        Returns 0.0–1.0; thresholds are chosen so that:
        - 1.0  → energy exceeds requirement (comfortable)
        - 0.9  → exact match (optimal)
        - 0.5  → one level below (doable but efficiency drops)
        - 0.1  → two or more levels below (not recommended)
        """
        required = cls.ENERGY_REQUIREMENTS.get(task_type, 2)
        diff = energy_level - required
        if diff >= 1:
            return 1.0     # comfortable surplus
        if diff == 0:
            return 0.9     # exact match — optimal
        if diff == -1:
            return 0.5     # marginal — doable with reduced efficiency
        return 0.1         # poor fit — avoid or defer

    @classmethod
    def allocate(
        cls,
        tasks: list[dict],
        profile: EnergyProfile,
    ) -> EnergyPlan:
        """Allocate tasks to energy slots.

        Each task dict should have at minimum:
        - task_type: str
        - description: str
        - priority: int (0-100)
        """
        ranked_fits: list[tuple[TaskEnergyFit, int]] = []
        for task in tasks:
            task_type = task.get("task_type", "light_review")
            score = cls.fit_score(task_type, profile.energy_level)
            ranked_fits.append(
                (
                    TaskEnergyFit(
                    task_type=task_type,
                    task_description=task.get("description", task_type),
                    energy_required=cls.ENERGY_REQUIREMENTS.get(task_type, 2),
                    fit_score=score,
                    recommendation=cls._recommendation(task_type, score, profile.energy_level),
                    ),
                    int(task.get("priority", 0)),
                )
            )

        # Sort by fit score descending, then by priority
        ranked_fits.sort(key=lambda item: (-item[0].fit_score, -item[1]))

        plan = EnergyPlan(profile=profile)

        for fit, _priority in ranked_fits:
            if fit.fit_score >= 0.8:
                # Fully suitable — place by cognitive load tier
                if fit.energy_required >= 3:
                    plan.high_energy_slot.append(fit)
                elif fit.energy_required >= 1:
                    plan.moderate_energy_slot.append(fit)
                else:
                    plan.low_energy_slot.append(fit)
            elif fit.fit_score >= 0.4:
                # Marginal — still doable, show in moderate tier with warning
                plan.moderate_energy_slot.append(fit)
            else:
                # Poor fit — push to low tier so the user sees it is not recommended
                plan.low_energy_slot.append(fit)

        # Warnings
        if profile.energy_level == 0:
            plan.warnings.append(
                "🛑 精力耗尽。建议休息或仅做被动回顾。强制学习会产生更多校准错误。"
            )
        elif profile.energy_level <= 1:
            plan.warnings.append(
                "⚠️ 当前精力偏低，不建议学习新知识或做高难度练习。优先完成复习和轻量任务。"
            )
        if profile.physical_fatigue >= 8:
            plan.warnings.append(
                "😴 身体疲劳度高，学习效率会显著下降。考虑缩短学习时间或先休息。"
            )
        if profile.sleep_hours > 0 and profile.sleep_hours < 6:
            plan.warnings.append(
                f"😴 睡眠仅 {profile.sleep_hours:.0f} 小时，睡眠不足会影响记忆巩固和学习效率。"
            )
        if profile.stress_level >= 7:
            plan.warnings.append(
                f"🧘 压力水平偏高（{profile.stress_level}/10），高压状态下学习效率显著下降，建议先做放松。"
            )

        return plan

    @classmethod
    def _recommendation(cls, task_type: str, fit_score: float, energy_level: int) -> str:
        if fit_score >= 0.9:
            return "✅ 当前精力完全匹配此任务"
        if fit_score >= 0.8:
            return "✅ 当前精力适合此任务"
        if fit_score >= 0.4:
            return "⚠️ 勉强可行，但效率会降低"
        return "❌ 建议等精力恢复后再做此任务"

    @classmethod
    def optimal_task_order(cls, profile: EnergyProfile) -> list[str]:
        """Suggest optimal task type ordering for the available energy."""
        if profile.energy_level >= 3:
            return [
                "interleaved_set",
                "difficult_practice",
                "new_knowledge",
                "mistake_review",
                "formula_drill",
                "worked_example_fading",
                "active_recall",
                "concept_discrimination",
                "light_review",
            ]
        if profile.energy_level >= 2:
            return [
                "mistake_review",
                "formula_drill",
                "worked_example_fading",
                "active_recall",
                "concept_discrimination",
                "light_review",
            ]
        return [
            "active_recall",
            "concept_discrimination",
            "light_review",
        ]
