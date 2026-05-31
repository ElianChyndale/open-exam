"""Migrate existing knowledge-status.json to graduated state schema."""
import json
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / ".system"))
sys.path.insert(0, str(repo_root / "packages/study-science/src"))

from study_science.knowledge_memory import KnowledgeMemoryEngine, KnowledgeFeedbackInput

overlay_path = repo_root / ".system" / "memory" / "review" / "knowledge-status.json"
if not overlay_path.exists():
    print("No overlay found")
    sys.exit(0)

overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
kp_map = overlay.get("knowledge_points", {})
engine = KnowledgeMemoryEngine()
exam_date_path = repo_root / ".system" / "exam_date.txt"
exam_date = exam_date_path.read_text(encoding="utf-8").strip()[:10] if exam_date_path.exists() else ""

updated = 0
for kid, entry in list(kp_map.items()):
    if "state_value" in entry and "review_interval_days" in entry:
        continue

    feedback = KnowledgeFeedbackInput(
        knowledge_id=kid,
        subject=entry.get("subject", ""),
        heading=entry.get("heading", ""),
        trigger=entry.get("trigger", ""),
        source_refs=entry.get("source_refs", []),
        outcome="reviewed",
        confidence_after=2,
    )
    new_entry, decision = engine.update_knowledge_point(entry, feedback, exam_date=exam_date)
    new_entry["review_id"] = entry.get("review_id", "")
    if "reviewed_at" not in new_entry or not new_entry.get("reviewed_at"):
        new_entry["reviewed_at"] = entry.get("reviewed_at", "")
    kp_map[kid] = new_entry
    updated += 1

if updated:
    overlay["knowledge_points"] = kp_map
    overlay_path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Migrated {updated} knowledge points to graduated state schema")
else:
    print("All knowledge points already migrated")

# Verify
for kid, entry in kp_map.items():
    print(f"  {kid}: state={entry['status']} (val={entry.get('state_value', '?')}), "
          f"interval={entry.get('review_interval_days', '?')}d, "
          f"next_review={entry.get('next_review_at', '?')}, "
          f"decay_risk={entry.get('decay_risk', '?')}")
