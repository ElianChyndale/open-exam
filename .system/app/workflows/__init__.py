# OpenExam workflows package
# Explicit re-exports — no wildcard imports to avoid silent name shadowing.
# Both core.py and todo.py define write_todo; the todo (V2 reducer) version
# is the one exposed here. archive_today_todo only exists in core.py.

from app.workflows.core import (
    # Core workflow functions
    record_question_attempt,
    daily_review_pack,
    complete_daily_review,
    mine_patterns,
    moc_gap_review,
    pre_mock_brief,
    post_mock_retro,
    record_event,
    record_progress,
    refresh_learning_outputs,
    mark_card_reviewed,
    batch_import_events,
    batch_import_attempts,
    weekly_focus_recommendation,
    load_payload,
    record_fix_rule_feedback,
    load_progress_events,
    collect_due_card_items,
    collect_pattern_items,
    collect_recent_low_confidence_items,
    merge_review_sources,
    interleave_review_items,
    load_daily_review_snapshot,
    add_review_item,
    clean_display_text,
    extract_markdown_section,
    parse_date,
    parse_frontmatter,
    default_fix_rule,
    next_drill_for,
    update_knowledge_from_diagnosis,
    # Aliased to avoid shadowing if a todo version ever appears
    archive_today_todo as core_archive_todo,
    # Private symbol needed by tests
    _as_source_refs,
)

# Todo is event sourced. Its write_todo is the V2 reducer entry point.
from app.workflows.todo import (
    write_todo,
    rollover_todo,
)
