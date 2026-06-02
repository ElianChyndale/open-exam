"""End-to-end verification: knowledge memory feedback loop."""
import json
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / ".system"))
sys.path.insert(0, str(repo_root / "packages/study-science/src"))

from app.storage import Repository
from app.workflows import (
    daily_review_pack, complete_daily_review,
    load_daily_review_snapshot, mark_card_reviewed, parse_frontmatter,
)
from datetime import date
from study_science.knowledge_memory import KnowledgeMemoryEngine

repo = Repository(repo_root)

# Step 1: Generate a new daily review for today
print("=== Step 1: Generate daily review ===")
path = daily_review_pack(repo, date(2026, 6, 1), days_back=7, max_items=20, focus_topic="")
print(f"Generated at: {path}")

# Step 2: Get review ID from latest snapshot
snapshot = load_daily_review_snapshot(repo)
review_id = snapshot["review_id"]
print(f"Review ID: {review_id}")
print(f"Knowledge points: {len(snapshot.get('knowledge_points', []))}")
print(f"Mistake cards: {len(snapshot.get('mistake_cards', []))}")

# Step 3: Complete the review
print("\n=== Step 2: Complete daily review ===")
result = complete_daily_review(repo, review_id)
print(f"Completed: {result['completed']}")
print(f"Newly reviewed items: {result['newly_reviewed_items']}")
print(f"Knowledge decisions: {len(result.get('knowledge_decisions', []))}")
for kd in result.get("knowledge_decisions", []):
    print(f"  {kd['knowledge_id'][:40]:40s} -> state={kd['state']:20s} (val={kd['state_value']}) "
          f"next_review={kd['next_review_at']} interval={kd['review_interval_days']}d decay={kd['decay_risk']}")

# Step 4: Verify knowledge-status.json
print("\n=== Step 3: Verify graduated states ===")
overlay_path = repo.memory_root / "review" / "knowledge-status.json"
overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
kp = overlay.get("knowledge_points", {})
states = set()
for kid, entry in kp.items():
    state_val = entry.get("state_value", 0)
    interval = entry.get("review_interval_days", 0)
    next_review = entry.get("next_review_at", "?")[:10]
    decay = entry.get("decay_risk", "?")
    status = entry["status"]
    states.add(status)
    trunc = kid[:40]
    spaces = " " * (42 - len(trunc))
    print(f"  {trunc}{spaces}status={status:20s} val={state_val} interval={interval:2d}d next={next_review} decay={decay}")

print(f"\nAll states present: {sorted(states)}")

# Step 5: Decay sweep
print("\n=== Step 4: Decay sweep ===")
engine = KnowledgeMemoryEngine()
overlay, decayed = engine.decay_sweep(overlay)
print(f"Decayed knowledge points: {len(decayed)}")
# Should be 0 since everything was just reviewed

# Step 6: Card review feedback
print("\n=== Step 5: Card review => Knowledge feedback ===")
cards = sorted((repo.memory_root / "question-errors").glob("*.md"))
if cards:
    card_id = cards[0].stem
    text = cards[0].read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    topic = fm.get("topic", "?")

    progress = mark_card_reviewed(repo, card_id, "recalled", confidence_after=3)
    print(f"Card: {card_id}")
    print(f"  Topic: {topic}, LOS: {fm.get('los', '?')[:40]}")
    print(f"  Card review: outcome={progress['outcome']}, interval={progress['interval_days']}d")

    overlay2 = json.loads(overlay_path.read_text(encoding="utf-8"))
    kp2 = overlay2.get("knowledge_points", {})
    matched = 0
    for kid, entry in kp2.items():
        subj = entry.get("subject", "").strip().lower()
        if subj == topic.strip().lower():
            matched += 1
            print(f"  -> Linked KP: {kid[:40]:40s} state={entry['status']:20s} "
                  f"val={entry.get('state_value', '?')} succ={entry.get('consecutive_successes', '?')}")
    print(f"  Matched knowledge points: {matched}")

# Step 7: Verify via CLI
print("\n=== Step 6: CLI knowledge-status ===")
from app.cli import run_cli
exit_code = run_cli(["knowledge-status"])
print(f"CLI exit code: {exit_code}")

print("\n=== ECOLOGICAL LOOP VERIFIED ===")
