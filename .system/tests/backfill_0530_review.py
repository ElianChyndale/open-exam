"""Backfill the 5.30 daily review completion status into the new tracking system.

The 5.30 daily review was completed under the old system (before snapshot/review-event
tracking existed). This script reconstructs the snapshot and runs complete_daily_review
to properly persist the review status for all affected knowledge points and mistake cards.
"""
import json
import sys
from pathlib import Path

# Ensure we can import app modules
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / ".system"))
sys.path.insert(0, str(repo_root / "packages/study-science/src"))

from app.storage import Repository
from app.workflows import (
    complete_daily_review,
    parse_frontmatter,
)
from datetime import date


def build_0530_snapshot(repo: Repository) -> dict | None:
    """Build a snapshot JSON for the 2026-05-30 daily review from existing card data."""
    review_id = "daily-review-backfill-0530"
    snapshot_root = repo.memory_root / "review" / "daily"
    snapshot_path = snapshot_root / f"{review_id}.json"
    if snapshot_path.exists():
        print(f"  Snapshot already exists at {snapshot_path}, loading...")
        return json.loads(snapshot_path.read_text(encoding="utf-8"))

    review_date = date(2026, 5, 30)

    # Knowledge points from the 5.30 review (reconstructed from old content)
    knowledge_points = [
        {"knowledge_id": "knowledge-0530-econ-m01", "subject": "Economics", "heading": "M01 Firm, Cost, Shutdown, Market Structure", "trigger": "Market structures; Profit maximization; Breakeven", "source_refs": ["CFA_tier1/Economics/00-Economics-MOC.md"]},
        {"knowledge_id": "knowledge-0530-econ-m02", "subject": "Economics", "heading": "M02 Business Cycles and Indicators", "trigger": "Cycle phases; Indicators; Business behavior", "source_refs": ["CFA_tier1/Economics/00-Economics-MOC.md"]},
        {"knowledge_id": "knowledge-0530-econ-m04", "subject": "Economics", "heading": "M04 Monetary Policy", "trigger": "Transmission; Tools; Central bank roles; Limitations", "source_refs": ["CFA_tier1/Economics/00-Economics-MOC.md"]},
        {"knowledge_id": "knowledge-0530-qm-estimation", "subject": "Quantitative Methods", "heading": "Estimation, CLT, confidence interval, and hypothesis-testing spine", "trigger": "Standard error; t confidence interval; CLT", "source_refs": ["CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md"]},
        {"knowledge_id": "knowledge-0530-econ-m03", "subject": "Economics", "heading": "M03 Fiscal Policy", "trigger": "Policy actor", "source_refs": ["CFA_tier1/Economics/00-Economics-MOC.md"]},
        {"knowledge_id": "knowledge-0530-econ-m07", "subject": "Economics", "heading": "M07 FX Market, Quotes, Regimes", "trigger": "Capital restrictions", "source_refs": ["CFA_tier1/Economics/00-Economics-MOC.md"]},
        {"knowledge_id": "knowledge-0530-qm-regression", "subject": "Quantitative Methods", "heading": "Independence, regression, and ML-risk spine", "trigger": "Spearman rank correlation", "source_refs": ["CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md"]},
        {"knowledge_id": "knowledge-0530-econ-m08", "subject": "Economics", "heading": "M08 Cross Rates, Forward Premiums, Arbitrage", "trigger": "Covered interest parity; Cross rate; Inverted quote", "source_refs": ["CFA_tier1/Economics/00-Economics-MOC.md"]},
        {"knowledge_id": "knowledge-0530-qm-simulation", "subject": "Quantitative Methods", "heading": "Simulation and resampling spine", "trigger": "Bootstrap; Lognormal price", "source_refs": ["CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md"]},
        {"knowledge_id": "knowledge-0530-qm-return", "subject": "Quantitative Methods", "heading": "Return and compounding spine", "trigger": "Arithmetic mean; Continuously compounded return; Holding-period total return", "source_refs": ["CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md"]},
        {"knowledge_id": "knowledge-0530-pm-m03", "subject": "Portfolio Management", "heading": "M03 Portfolio Management Process", "trigger": "Process; Pooled vehicles", "source_refs": ["CFA_tier1/Portfolio_Management/00-Portfolio-Management-MOC.md"]},
        {"knowledge_id": "knowledge-0530-qm-probability", "subject": "Quantitative Methods", "heading": "Probability, statistics, and portfolio spine", "trigger": "Total probability; Expected value", "source_refs": ["CFA_tier1/Quantitative_Methods/00-Quantitative-Methods-MOC.md"]},
    ]

    # Find mistake cards that were due on or before 2026-05-30
    mistake_cards = []
    seen_card_ids = set()

    for path in sorted((repo.memory_root / "question-errors").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        due_at_str = fm.get("review_due_at", "")
        if not due_at_str:
            continue
        try:
            due_parts = due_at_str.strip().split("T")[0].split("-")
            if len(due_parts) != 3:
                continue
            due_date = date(int(due_parts[0]), int(due_parts[1]), int(due_parts[2]))
        except (ValueError, IndexError):
            continue
        if due_date > review_date:
            continue

        card_id = path.stem
        if card_id in seen_card_ids:
            continue
        seen_card_ids.add(card_id)
        mistake_cards.append({
            "card_id": card_id,
            "topic": fm.get("topic", ""),
            "los": fm.get("los", ""),
            "source_refs": [fm.get("evidence_refs", "")] if fm.get("evidence_refs") else [],
        })

    if not mistake_cards and not knowledge_points:
        print("  No cards or knowledge points found for 5.30 review")
        return None

    snapshot = {
        "schema_version": 1,
        "review_id": review_id,
        "generated_for": review_date.isoformat(),
        "generated_at": "2026-05-30T12:00:00+00:00",
        "generation": {
            "days_back": 7,
            "max_items": 20,
            "focus_topic": "unspecified",
            "knowledge_depth": "standard",
        },
        "knowledge_points": knowledge_points,
        "mistake_cards": mistake_cards,
    }

    snapshot_root.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Snapshot written to {snapshot_path}")
    print(f"  Knowledge points: {len(knowledge_points)}, Mistake cards: {len(mistake_cards)}")
    return snapshot


def main():
    repo = Repository(repo_root)

    print("Step 1: Building 5.30 review snapshot...")
    snapshot = build_0530_snapshot(repo)
    if snapshot is None:
        print("  Nothing to backfill.")
        return

    review_id = snapshot["review_id"]

    print(f"\nStep 2: Running complete_daily_review for {review_id}...")
    result = complete_daily_review(repo, review_id)

    print("\nResults:")
    print(f"  Review ID: {result['review_id']}")
    print(f"  Completed: {result['completed']}")
    print(f"  Newly reviewed items: {result['newly_reviewed_items']}")

    # Verify
    print("\nVerification:")
    overlay_path = repo.memory_root / "review" / "knowledge-status.json"
    if overlay_path.exists():
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        statuses = {v.get("status") for v in overlay.get("knowledge_points", {}).values()}
        print(f"  Knowledge-status.json: {len(overlay.get('knowledge_points', {}))} entries, statuses: {statuses}")

    review_events = repo.load_jsonl_events("review")
    event_types = [e["event_type"] for e in review_events if review_id in str(e.get("payload", {}).get("review_id", ""))]
    print(f"  Review events for this backfill: {event_types}")

    # Verify card statuses
    updated = 0
    for card in snapshot.get("mistake_cards", []):
        path = repo.memory_root / "question-errors" / f"{card['card_id']}.md"
        if path.exists():
            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            if fm.get("review_status") == "Reviewed once":
                updated += 1
    print(f"  Cards with 'review_status: Reviewed once': {updated}/{len(snapshot.get('mistake_cards', []))}")


if __name__ == "__main__":
    main()
