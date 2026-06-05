from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from app.codex_task_generator import generate_codex_task
from app.feature_flags import FeatureFlags
from app.models import stable_id
from app.skill_models import SkillHealthScore, SkillReflectionEvent, SkillUpgradeProposal
from app.skill_reflection import load_reflections


def _proposal_path(repo_root: Path, proposal_id: str) -> Path:
    return repo_root / ".system" / "memory" / "skills" / "proposals" / f"{proposal_id}.json"


def load_upgrade_proposals(repo_root: Path) -> list[SkillUpgradeProposal]:
    root = repo_root / ".system" / "memory" / "skills" / "proposals"
    rows: list[SkillUpgradeProposal] = []
    for path in sorted(root.glob("*.json")):
        rows.append(SkillUpgradeProposal.from_dict(json.loads(path.read_text(encoding="utf-8"))))
    return rows


def save_upgrade_proposal(repo_root: Path, proposal: SkillUpgradeProposal) -> Path:
    path = _proposal_path(repo_root, proposal.proposal_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(proposal.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def proposal_from_repeated_reflections(repo, *, threshold: int = 3) -> list[SkillUpgradeProposal]:
    flags = FeatureFlags.load(repo.root)
    if not flags.enabled("skill_upgrade_proposals_enabled"):
        return []

    reflections = [item for item in load_reflections(repo.root) if item.status == "open"]
    proposals = load_upgrade_proposals(repo.root)
    existing_keys = {
        (proposal.skill_id, tuple(sorted(proposal.reflection_ids)))
        for proposal in proposals
        if proposal.status in {"proposed", "approved", "open"}
    }
    grouped: dict[tuple[str, tuple[str, ...]], list[SkillReflectionEvent]] = defaultdict(list)
    for reflection in reflections:
        key = (reflection.skill_id, tuple(sorted(set(reflection.failure_codes))))
        grouped[key].append(reflection)

    created: list[SkillUpgradeProposal] = []
    for (skill_id, failure_codes), bucket in grouped.items():
        if len(bucket) < threshold:
            continue
        reflection_ids = sorted(item.reflection_id for item in bucket)
        key = (skill_id, tuple(reflection_ids))
        if key in existing_keys:
            continue
        title = f"Upgrade proposal for {skill_id}: {'/'.join(failure_codes) or 'validator failures'}"
        problem = (
            f"The skill `{skill_id}` produced {len(bucket)} validator failures with the same pattern: "
            f"{', '.join(failure_codes) or 'unspecified failures'}."
        )
        proposal = SkillUpgradeProposal(
            proposal_id=stable_id("proposal", skill_id, ",".join(reflection_ids)),
            skill_id=skill_id,
            title=title,
            problem_statement=problem,
            evidence_summary="; ".join(item.failure_message for item in bucket[:3]),
            requested_changes=[
                "Audit the prompt or transformation rules that generated the failing tutor analysis.",
                "Add or tighten validation coverage for the repeated failure pattern.",
                "Keep any change behind tests and explicit approval; do not auto-edit skill files.",
            ],
            acceptance_criteria=[
                "Repeated failure pattern is covered by deterministic validation or safer generation logic.",
                "New or updated tests reproduce the old failure and pass after the fix.",
                "Skill files are not modified automatically by the proposal pipeline.",
            ],
            limits=[
                "Do not auto-modify skill files.",
                "Do not bypass validator, tests, or approval.",
                "Do not expose wrong-answer diagnostics in public tutor outputs.",
            ],
            reflection_ids=reflection_ids,
        )
        if flags.enabled("skill_codex_task_generator_enabled"):
            task_path = generate_codex_task(repo.root, proposal)
            proposal.codex_task_path = str(task_path.relative_to(repo.root)).replace("\\", "/")
        save_upgrade_proposal(repo.root, proposal)
        created.append(proposal)
        existing_keys.add(key)
    return created


def compute_skill_health(repo_root: Path, skill_id: str) -> SkillHealthScore:
    reflections = [item for item in load_reflections(repo_root) if item.skill_id == skill_id]
    proposals = [item for item in load_upgrade_proposals(repo_root) if item.skill_id == skill_id]
    recent_failures = len([item for item in reflections if item.status == "open"])
    score = max(0, 100 - recent_failures * 18 - len(proposals) * 8)
    status = "healthy" if score >= 85 else "watch" if score >= 65 else "degraded"
    last_reflection_at = max((item.created_at for item in reflections), default="")
    return SkillHealthScore(
        skill_id=skill_id,
        score=score,
        status=status,
        reflection_count=len(reflections),
        recent_failures=recent_failures,
        proposal_count=len(proposals),
        last_reflection_at=last_reflection_at,
    )
