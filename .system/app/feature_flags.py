from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


DEFAULT_FEATURE_FLAGS: dict[str, bool] = {
    "todo_enabled": True,
    "event_envelope_v2_enabled": True,
    "provenance_enabled": False,
    "privacy_controls_enabled": False,
    "learner_twin_enabled": False,
    "structured_tasks_enabled": False,
    "grounded_ai_enabled": False,
    "sync_v2_enabled": False,
    "mcp_read_only_enabled": False,
    "research_runtime_enabled": False,
    "trust_exports_enabled": False,
    "language_os_enabled": False,
    "language_fsrs_enabled": False,
    "language_grammar_lens": False,
    "language_intuition_graph": False,
    "language_content_import": False,
    "language_cloud_transcription": False,
    "language_embedding_search": False,
    "gsap_motion_enabled": False,
    "reduced_motion_safe": True,
}


@dataclass(frozen=True, slots=True)
class FeatureFlags:
    values: dict[str, bool]

    @classmethod
    def load(cls, root: Path) -> FeatureFlags:
        config_path = root / ".system" / "config" / "features.yaml"
        overrides: dict[str, Any] = {}
        if config_path.exists():
            parsed = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            if not isinstance(parsed, dict):
                raise ValueError("Feature flag configuration must be a mapping.")
            overrides = parsed
        values = dict(DEFAULT_FEATURE_FLAGS)
        values.update({key: bool(value) for key, value in overrides.items()})
        return cls(values=values)

    def enabled(self, name: str) -> bool:
        return self.values.get(name, False)
