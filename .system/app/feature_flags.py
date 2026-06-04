from __future__ import annotations

from dataclasses import dataclass
import os
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
    "language_os_enabled": True,
    "language_fsrs_enabled": False,
    "language_grammar_lens": False,
    "language_intuition_graph": False,
    "language_content_import": False,
    "language_cloud_transcription": False,
    "language_embedding_search": False,
    "resource_ingestion_enabled": False,
    "resource_fulltext_index_enabled": False,
    "resource_language_auto_promotion_enabled": False,
    "resource_cfa_official_promotion_enabled": False,
    "resource_ai_discovery_enabled": False,
    "resource_scheduler_enabled": False,
    "resource_code_audit_enabled": False,
    "gsap_motion_enabled": False,
    "reduced_motion_safe": True,
    "knowledge_pdf_ingestion": False,
    "knowledge_atom_extraction": False,
    "knowledge_coverage_audit": False,
    "daily_review_lab": False,
    "daily_review_lab_enabled": False,
    "daily_review_correct_only_mode": True,
    "daily_review_asset_scoring": False,
    "daily_review_unit_scoring": False,
    "formula_lab": False,
    "review_asset_ingestion_enabled": True,
    "review_asset_manual_confirm_required": True,
    "review_asset_draft_preview_enabled": False,
    "formula_lab_enabled": True,
    "formula_asset_enrichment_enabled": True,
    "formula_review_units_enabled": True,
    "formula_ba_ii_plus_steps_enabled": True,
    "syllabus_coverage_enabled": True,
    "syllabus_demo_seed_enabled": True,
    "syllabus_asset_mapping_enabled": True,
    "coverage_guided_review_selection_enabled": True,
    "mock_retro_enabled": True,
    "transfer_gap_priority_enabled": True,
    "mock_retro_correct_only_mode": True,
    "mock_retro_review_generation_enabled": True,
    "resource_quality_gate_enabled": True,
    "resource_evidence_extraction_enabled": True,
    "resource_asset_promotion_enabled": True,
    "resource_quality_guided_review_enabled": True,
    "resource_conflict_detection_enabled": True,
    "dictionary_kernel_enabled": True,
    "lexical_review_enabled": True,
    "dictionary_quality_gate_enabled": True,
    "spanish_english_dictionary_enabled": True,
    "english_english_dictionary_enabled": True,
    "mission_control_enabled": True,
    "integration_health_checks_enabled": True,
    "green_test_gate_enabled": True,
    "file_ingestion_enabled": True,
    "pdf_text_extraction_enabled": True,
    "dictionary_file_import_enabled": True,
    "resource_file_import_enabled": True,
    "file_duplicate_detection_enabled": True,
    "ocr_extraction_enabled": False,
    "study_planner_enabled": True,
    "adaptive_session_orchestrator_enabled": True,
    "energy_aware_planning_enabled": True,
    "study_plan_retro_enabled": True,
    "focus_session_enabled": True,
    "unified_study_flow_enabled": True,
    "focus_embedded_review_enabled": True,
    "focus_embedded_formula_enabled": True,
    "focus_embedded_language_enabled": True,
    "focus_embedded_assessment_enabled": True,
    "focus_tutor_hint_enabled": True,
    "focus_polish_enabled": True,
    "focus_local_reveal_contract_enabled": True,
    "validation_resource_cleanup_enabled": True,
    "playwright_state_isolation_enabled": True,
    "learning_analytics_enabled": True,
    "mastery_calibration_enabled": True,
    "plan_effectiveness_enabled": True,
    "resource_usefulness_enabled": True,
    "coverage_momentum_enabled": True,
    "correct_only_analytics_enabled": True,
    "adaptive_assessment_enabled": True,
    "interleaving_drill_enabled": True,
    "assessment_feedback_correct_only_enabled": True,
    "assessment_transfer_gap_integration_enabled": True,
    "assessment_analytics_integration_enabled": True,
    "knowledge_graph_enabled": True,
    "global_search_enabled": True,
    "traceability_map_enabled": True,
    "impact_analysis_enabled": True,
    "correct_only_graph_enabled": True,
    "accessibility_hardening_enabled": True,
    "keyboard_shortcuts_enabled": True,
    "responsive_layout_hardening_enabled": True,
    "unified_ui_states_enabled": True,
    "ux_route_consistency_checks_enabled": True,
    "data_governance_enabled": True,
    "safe_export_enabled": True,
    "full_export_enabled": True,
    "backup_restore_enabled": True,
    "category_reset_enabled": True,
    "privacy_redaction_enabled": True,
    "snapshot_rollback_enabled": True,
    "tutor_copilot_enabled": True,
    "grounded_tutor_retrieval_enabled": True,
    "tutor_source_citations_enabled": True,
    "tutor_correct_only_enabled": True,
    "tutor_llm_provider_enabled": False,
    "tutor_conversation_memory_enabled": True,
    "goal_profiles_enabled": True,
    "course_packs_enabled": True,
    "first_run_onboarding_enabled": True,
    "day1_plan_enabled": True,
    "onboarding_readiness_enabled": True,
    "interop_enabled": True,
    "anki_interop_enabled": True,
    "markdown_interop_enabled": True,
    "calendar_export_enabled": True,
    "learning_record_export_enabled": True,
    "interop_safe_mode_enabled": True,
    "premium_cockpit_enabled": True,
    "progressive_disclosure_enabled": True,
    "advanced_tools_hub_enabled": True,
    "simplified_mission_control_enabled": True,
    "premium_visual_system_enabled": True,
    "dictionary_os": False,
    "dictionary_private_index": False,
    "language_cards_v2": False,
    "spanish_morphology_engine": False,
    "resource_quality_gate": False,
    "resource_candidate_queue": False,
    "ai_knowledge_enrichment": False,
    "unified_dashboard": False,
    "pwa_offline": False,
    "cfa_onboarding": False,
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
        for key in list(values):
            env_value = os.environ.get(f"OPENEXAM_FEATURE_{key.upper()}")
            if env_value is not None:
                values[key] = env_value.strip().lower() in {"1", "true", "yes", "on"}
        return cls(values=values)

    def enabled(self, name: str) -> bool:
        return self.values.get(name, False)
