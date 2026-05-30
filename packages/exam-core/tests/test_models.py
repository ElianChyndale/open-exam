from __future__ import annotations


def test_core_models_instantiate_with_default_factories() -> None:
    from exam_core import (
        EnergyCheckIn,
        ErrorDiagnosis,
        ExamAdapter,
        ExamConfig,
        LearnerProgressReport,
        MockSession,
        QuestionAttempt,
        ReviewTask,
        StudyPlan,
        SyllabusNode,
    )
    from exam_core.models import CohortRiskReport, InstitutionCohort, PatternInsight

    instances = [
        ExamConfig(exam_name="CFA Level I", exam_date="2026-08-01", current_phase="review"),
        ExamAdapter(exam_id="cfa-l1", exam_name="CFA Level I", version="2026"),
        SyllabusNode(node_id="n1", path="CFA.Quant", title="Quant", los_code="QM.1"),
        QuestionAttempt(topic="Quantitative Methods", los="QM.1"),
        ErrorDiagnosis(attempt_id="qa-1"),
        ReviewTask(topic="Quantitative Methods", los="QM.1"),
        EnergyCheckIn(),
        StudyPlan(date="2026-05-30"),
        MockSession(exam_name="CFA Level I", session_label="Mock 1"),
        LearnerProgressReport(learner_id="learner-1"),
        InstitutionCohort(institution_id="inst-1", cohort_name="Cohort A"),
        CohortRiskReport(cohort_id="cohort-1", cohort_name="Cohort A"),
        PatternInsight(pattern_key="Quant::QM.1::concept_confusion"),
    ]

    for instance in instances:
        assert instance is not None
        timestamp = getattr(instance, "created_at", None) or getattr(instance, "generated_at", None)
        if timestamp is not None:
            assert timestamp
