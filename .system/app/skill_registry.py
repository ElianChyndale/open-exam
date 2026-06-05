from __future__ import annotations

import json
from pathlib import Path

from app.skill_models import SkillRegistryEntry


REGISTRY_FILE = Path(".system/memory/skills/registry.json")
SYSTEM_SKILLS: tuple[tuple[str, str, str], ...] = (
    ("cfa-question-captor", "CFA Question Captor", "Normalize question mistakes into evidence-backed capture artifacts."),
    ("cfa-screenshot-mistake-captor", "CFA Screenshot Mistake Captor", "Extract screenshot mistake evidence into storage-ready payloads."),
    ("tutor-analysis-pipeline", "Tutor Analysis Pipeline", "Transform mistake evidence into correct-only tutor analysis and review seeds."),
    ("cfa-validation-guard", "CFA Validation Guard", "Check correctness, evidence, and leakage invariants before promotion."),
)


def _registry_path(repo_root: Path) -> Path:
    return repo_root / REGISTRY_FILE


def _default_entries(repo_root: Path) -> list[SkillRegistryEntry]:
    entries: list[SkillRegistryEntry] = []
    skills_root = repo_root / "skills"
    seen: set[str] = set()
    for skill_id, name, boundary in SYSTEM_SKILLS:
        seen.add(skill_id)
        owned_paths = []
        if (skills_root / skill_id).exists():
            owned_paths.append(f"skills/{skill_id}")
        entries.append(
            SkillRegistryEntry(
                skill_id=skill_id,
                name=name,
                owned_paths=owned_paths,
                role_boundary=boundary,
            )
        )
    if skills_root.exists():
        for path in sorted(p for p in skills_root.iterdir() if p.is_dir()):
            if path.name in seen:
                continue
            entries.append(
                SkillRegistryEntry(
                    skill_id=path.name,
                    name=path.name.replace("-", " ").title(),
                    owned_paths=[f"skills/{path.name}"],
                    role_boundary="Local skill directory discovered from workspace.",
                )
            )
    return entries


def load_skill_registry(repo_root: Path) -> list[SkillRegistryEntry]:
    path = _registry_path(repo_root)
    if not path.exists():
        entries = _default_entries(repo_root)
        save_skill_registry(repo_root, entries)
        return entries
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [SkillRegistryEntry.from_dict(item) for item in payload.get("skills", [])]


def save_skill_registry(repo_root: Path, entries: list[SkillRegistryEntry]) -> Path:
    path = _registry_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"skills": [entry.as_dict() for entry in entries]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path
