"""Exam profile management — makes ExamOS exam-agnostic.

Each exam (CFA L1, FRM P1, etc.) has a YAML profile defining:
- Subjects and their weights
- Mock bucket mappings
- Subject aliases (for flexible input)
- MOC file paths
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ExamProfile:
    """An exam profile loaded from a YAML file."""
    name: str
    short_name: str
    total_los: int
    passing_score: int
    subjects: list[dict] = field(default_factory=list)
    mock_buckets: dict[str, str] = field(default_factory=dict)
    subject_aliases: dict[str, str] = field(default_factory=dict)
    moc_paths: dict[str, str] = field(default_factory=dict)
    formula_dense_subjects: set[str] = field(default_factory=lambda: set())
    concept_first_subjects: set[str] = field(default_factory=lambda: {"Ethical and Professional Standards", "Ethical_and_Professional_Standards"})

    def normalize_subject(self, value: str) -> str:
        """Normalize a subject name using aliases."""
        normalized = value.replace("_", " ").strip().lower()
        if normalized in self.subject_aliases:
            return self.subject_aliases[normalized]
        for alias, subject in self.subject_aliases.items():
            if alias in normalized:
                return subject
        return value.strip()

    def mock_bucket_for(self, subject: str) -> str | None:
        """Get the mock bucket key for a subject."""
        return self.mock_buckets.get(subject) or self.mock_buckets.get(self.normalize_subject(subject))

    def moc_path_for(self, subject: str) -> str | None:
        """Get the relative MOC path for a subject."""
        normalized = self.normalize_subject(subject)
        return self.moc_paths.get(normalized)

    def subject_weight(self, subject: str) -> int:
        """Get the exam weight for a subject."""
        normalized = self.normalize_subject(subject)
        for s in self.subjects:
            if s["name"] == normalized or s["short"] == normalized:
                return s.get("weight", 10)
        return 10


def load_profile(profile_name: str = "cfa-l1", profiles_dir: Path | None = None) -> ExamProfile:
    """Load an exam profile by name.

    Args:
        profile_name: Short name of the profile (e.g. 'cfa-l1', 'frm-p1')
        profiles_dir: Directory containing profile YAML files

    Returns:
        Loaded ExamProfile instance

    Raises:
        FileNotFoundError: If profile file doesn't exist
        ValueError: If YAML parsing fails
    """
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required. Install with: pip install pyyaml")

    if profiles_dir is None:
        # Default: look next to this file in .system/app/
        profiles_dir = Path(__file__).resolve().parent.parent / "exam_profiles"

    profile_path = profiles_dir / f"{profile_name}.yaml"
    if not profile_path.exists():
        # Try alternate path: .system/exam_profiles/ relative to repo root
        alt_path = Path(__file__).resolve().parent.parent.parent / "exam_profiles" / f"{profile_name}.yaml"
        if alt_path.exists():
            profile_path = alt_path
        else:
            raise FileNotFoundError(f"Exam profile not found: {profile_name} (tried {profile_path} and {alt_path})")

    with open(profile_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return ExamProfile(
        name=data.get("name", profile_name),
        short_name=data.get("short_name", profile_name),
        total_los=data.get("total_los", 10),
        passing_score=data.get("passing_score", 70),
        subjects=data.get("subjects", []),
        mock_buckets=data.get("mock_buckets", {}),
        subject_aliases=data.get("subject_aliases", {}),
        moc_paths=data.get("moc_paths", {}),
    )


# Global profile cache
_current_profile: ExamProfile | None = None


def get_profile() -> ExamProfile:
    """Get the currently active exam profile."""
    global _current_profile
    if _current_profile is None:
        profile_name = os.environ.get("EXAMOS_PROFILE", "cfa-l1")
        _current_profile = load_profile(profile_name)
    return _current_profile


def set_profile(profile: ExamProfile) -> None:
    """Set the active exam profile."""
    global _current_profile
    _current_profile = profile


def list_available_profiles(profiles_dir: Path | None = None) -> list[dict]:
    """List all available exam profiles."""
    try:
        import yaml
    except ImportError:
        return []

    if profiles_dir is None:
        profiles_dir = Path(__file__).resolve().parent.parent / "exam_profiles"
        alt_dir = Path(__file__).resolve().parent.parent.parent / "exam_profiles"
        if not profiles_dir.exists() and alt_dir.exists():
            profiles_dir = alt_dir

    if not profiles_dir.exists():
        return []

    profiles = []
    for path in sorted(profiles_dir.glob("*.yaml")):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        profiles.append({
            "name": data.get("name", path.stem),
            "short_name": data.get("short_name", path.stem),
            "total_los": data.get("total_los", 0),
            "passing_score": data.get("passing_score", 0),
            "subject_count": len(data.get("subjects", [])),
        })
    return profiles
