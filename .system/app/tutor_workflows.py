from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

from app.models import MistakeEvent, stable_id
from app.skill_reflection import skill_reflection_from_validator_failure
from app.skill_upgrade import proposal_from_repeated_reflections
from app.tutor_models import TutorAnalysisResult
from app.tutor_validator import validate_tutor_analysis
from study_science.review_lab_models import CorrectKnowledgeAsset, DailyReviewUnit


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _analysis_path(repo_root: Path, analysis_id: str) -> Path:
    return repo_root / ".system" / "memory" / "tutor" / "analyses" / f"{analysis_id}.json"


def _asset_seed_path(repo_root: Path, asset_id: str) -> Path:
    return repo_root / ".system" / "memory" / "tutor" / "correct-asset-seeds" / f"{asset_id}.json"


def _review_unit_seed_path(repo_root: Path, unit_id: str) -> Path:
    return repo_root / ".system" / "memory" / "tutor" / "daily-review-unit-seeds" / f"{unit_id}.json"


def _normalize_sentence(text: str) -> str:
    collapsed = re.sub(r"\s+", " ", str(text or "")).strip()
    return collapsed


def _sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+", _normalize_sentence(text))
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def _derive_tested_concept(event: MistakeEvent) -> str:
    for candidate in (event.los, event.topic):
        if candidate and candidate.strip():
            return candidate.strip()
    return "Correct concept from mistake evidence"


def _derive_principle(event: MistakeEvent) -> str:
    sentences = _sentences(event.correct_resolution)
    if sentences:
        return sentences[0]
    return f"Use the correct principle for {event.topic} / {event.los} based on source-backed resolution."


def _derive_decision_rule(event: MistakeEvent) -> str:
    prompt = _normalize_sentence(event.prompt_or_question).lower()
    if "income statement" in prompt and "common-size" in prompt:
        return "For a common-size income statement, express each line item as a percentage of revenue."
    if "balance sheet" in prompt and "common-size" in prompt:
        return "For a common-size balance sheet, express each line item as a percentage of total assets."
    if event.error_type == "formula_misuse":
        return "Name the governing rule and denominator first, then compute with that rule."
    if event.error_type == "concept_confusion":
        return "State the concept definition first, then apply the matching rule to the case."
    return "Use the correct rule from the evidence before solving."


def _derive_solution_path(event: MistakeEvent, decision_rule: str) -> list[str]:
    path = [decision_rule]
    sentences = _sentences(event.correct_resolution)
    path.extend(sentence for sentence in sentences[:3] if sentence not in path)
    if len(path) < 2:
        path.append("Walk from rule selection to the final answer without reusing the learner's wrong path.")
    return path


def _derive_boundary(event: MistakeEvent, decision_rule: str) -> str:
    prompt = _normalize_sentence(event.prompt_or_question).lower()
    if "common-size" in prompt:
        return "Do not switch statement types: match the denominator to the statement being normalized."
    if event.error_type == "formula_misuse":
        return "A correct calculation still fails if the governing denominator or rule is wrong."
    return "Apply this rule only when the question matches the tested concept and evidence."


def _derive_hint(event: MistakeEvent, decision_rule: str) -> str:
    if "common-size" in _normalize_sentence(event.prompt_or_question).lower():
        return "Before calculating, say aloud which statement you are normalizing and what its denominator must be."
    return f"Before solving, restate the correct rule for {event.topic} in one sentence."


def _derive_micro_drill(event: MistakeEvent) -> str:
    return f"Do one same-LOS micro drill for {event.topic} and explain the correct rule before revealing the answer."


def tutor_analysis_from_mistake_event(repo, event: MistakeEvent, *, skill_id: str = "cfa-question-captor") -> TutorAnalysisResult:
    decision_rule = _derive_decision_rule(event)
    analysis = TutorAnalysisResult(
        analysis_id=stable_id("analysis", event.event_id or "", skill_id),
        event_id=event.event_id or "",
        source_layer=event.source_layer,
        topic=event.topic,
        los=event.los,
        skill_id=skill_id,
        tested_concept=_derive_tested_concept(event),
        correct_principle=_derive_principle(event),
        correct_decision_rule=decision_rule,
        correct_solution_path=_derive_solution_path(event, decision_rule),
        boundary=_derive_boundary(event, decision_rule),
        tutor_hint=_derive_hint(event, decision_rule),
        next_micro_drill=_derive_micro_drill(event),
        source_refs=list(dict.fromkeys([event.event_id or "", *event.evidence_refs, *event.evidence_assets, event.moc_target])),
    )
    analysis.source_refs = [item for item in analysis.source_refs if item]
    validation = validate_tutor_analysis(analysis, source_event=event)
    reflection = skill_reflection_from_validator_failure(repo, analysis=analysis, validation=validation)
    if reflection is not None:
        analysis.reflection_event_id = reflection.reflection_id
    analysis.validation_status = "validated" if validation.is_valid else "needs_review"
    save_tutor_analysis(repo.root, analysis)
    asset_seed = tutor_analysis_to_correct_asset_seed(repo, analysis)
    review_unit_seed = tutor_analysis_to_review_unit_seed(repo, analysis, asset_seed=asset_seed)
    analysis.correct_asset_seed_id = asset_seed.asset_id
    analysis.daily_review_unit_seed_id = review_unit_seed.unit_id
    save_tutor_analysis(repo.root, analysis)
    save_correct_asset_seed(repo.root, asset_seed)
    save_review_unit_seed(repo.root, review_unit_seed)
    if reflection is not None:
        proposal_from_repeated_reflections(repo)
    return analysis


def tutor_analysis_to_correct_asset_seed(repo, analysis: TutorAnalysisResult) -> CorrectKnowledgeAsset:
    asset_type = "mistake_corrected"
    decision_text = analysis.correct_decision_rule.lower()
    if "formula" in decision_text:
        asset_type = "formula"
    elif "boundary" in analysis.boundary.lower():
        asset_type = "exam_boundary"
    elif "rule" in decision_text:
        asset_type = "decision_rule"
    asset = CorrectKnowledgeAsset(
        asset_id=stable_id("asset", analysis.analysis_id, analysis.tested_concept),
        asset_type=asset_type,
        profile_id="default",
        subject=analysis.topic,
        module=analysis.topic,
        los=analysis.los,
        title=analysis.tested_concept,
        trigger=analysis.tested_concept,
        correct_rule=analysis.correct_decision_rule,
        applies_when=[analysis.correct_principle],
        common_correct_boundary_rules=[analysis.boundary],
        example=analysis.tutor_hint,
        correct_steps=list(analysis.correct_solution_path),
        source_refs=list(analysis.source_refs),
        source_quality=0.8 if analysis.source_refs else 0.5,
        exam_weight=0.6,
        mistake_link_count=1,
        decay_risk=0.6,
        mastery_state="New",
        created_from="mistake",
        validation_status="derived",
    )
    return asset


def tutor_analysis_to_review_unit_seed(
    repo,
    analysis: TutorAnalysisResult,
    *,
    asset_seed: CorrectKnowledgeAsset | None = None,
) -> DailyReviewUnit:
    asset = asset_seed or tutor_analysis_to_correct_asset_seed(repo, analysis)
    return DailyReviewUnit(
        unit_id=stable_id("unit", analysis.analysis_id, asset.asset_id),
        unit_type=asset.asset_type,
        review_id=f"tutor-analysis-{analysis.analysis_id}",
        asset_id=asset.asset_id,
        asset_type=asset.asset_type,
        prompt=f"When this concept appears, which correct rule applies? {analysis.tested_concept}",
        front_prompt=f"State the correct rule for: {analysis.tested_concept}",
        correct_answer=analysis.correct_decision_rule,
        correct_reasoning=analysis.correct_principle,
        correct_steps=list(analysis.correct_solution_path),
        boundary_rules=[analysis.boundary],
        applies_when=[analysis.correct_principle],
        source_refs=list(analysis.source_refs),
        due_reason=analysis.next_micro_drill,
        priority=85,
        interaction_mode="recall_reveal",
        recall_instruction="Recall the correct rule before revealing the answer.",
        answer=analysis.correct_decision_rule,
        subject=analysis.topic,
        heading=analysis.tested_concept,
        los=analysis.los,
    )


def save_tutor_analysis(repo_root: Path, analysis: TutorAnalysisResult) -> Path:
    path = _analysis_path(repo_root, analysis.analysis_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(analysis.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def load_tutor_analysis(repo_root: Path, analysis_id: str) -> TutorAnalysisResult | None:
    path = _analysis_path(repo_root, analysis_id)
    if not path.exists():
        return None
    return TutorAnalysisResult.from_dict(json.loads(path.read_text(encoding="utf-8")))


def save_correct_asset_seed(repo_root: Path, asset: CorrectKnowledgeAsset) -> Path:
    path = _asset_seed_path(repo_root, asset.asset_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asset.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def save_review_unit_seed(repo_root: Path, unit: DailyReviewUnit) -> Path:
    path = _review_unit_seed_path(repo_root, unit.unit_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(unit.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def confirm_tutor_analysis(repo, analysis_id: str) -> TutorAnalysisResult:
    analysis = load_tutor_analysis(repo.root, analysis_id)
    if analysis is None:
        raise KeyError(analysis_id)
    asset_seed_path = _asset_seed_path(repo.root, analysis.correct_asset_seed_id)
    unit_seed_path = _review_unit_seed_path(repo.root, analysis.daily_review_unit_seed_id)
    if asset_seed_path.exists():
        asset_payload = json.loads(asset_seed_path.read_text(encoding="utf-8"))
        asset_payload["validation_status"] = "confirmed"
        promoted_asset_path = repo.root / ".system" / "memory" / "review" / "asset-candidates" / asset_seed_path.name
        promoted_asset_path.parent.mkdir(parents=True, exist_ok=True)
        promoted_asset_path.write_text(json.dumps(asset_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if unit_seed_path.exists():
        promoted_unit_path = repo.root / ".system" / "memory" / "review" / "unit-seeds" / unit_seed_path.name
        promoted_unit_path.parent.mkdir(parents=True, exist_ok=True)
        promoted_unit_path.write_text(unit_seed_path.read_text(encoding="utf-8"), encoding="utf-8")
    analysis.validation_status = "confirmed"
    analysis.confirmed_at = _now()
    save_tutor_analysis(repo.root, analysis)
    return analysis
