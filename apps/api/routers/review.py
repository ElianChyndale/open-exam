"""GET /api/review-pack/today — Daily review pack generation."""

from __future__ import annotations

from datetime import date, datetime

from fastapi import APIRouter, Depends, Query

from deps import get_repo
from schemas import DailyReviewCompleteResponse, ReviewPackResponse

router = APIRouter()


@router.get("/today", response_model=ReviewPackResponse)
async def get_today_review_pack(
    date_str: str = Query(default="", alias="date"),
    days_back: int = Query(default=7, ge=1, le=90),
    max_items: int = Query(default=20, ge=1, le=100),
    focus_topic: str = Query(default=""),
    knowledge_depth: str = Query(default="standard", pattern="^(standard|expanded)$"),
    repo=Depends(get_repo),
):
    """Generate today's review pack.

    Includes:
    - Due/overdue mistake cards
    - Recent low-confidence events
    - Repeated patterns (recurrence >= 3)
    - Knowledge warm-start from MOC formula/concept tables
    """
    from app.workflows import daily_review_pack

    review_date = date.fromisoformat(date_str) if date_str else None
    result_path = daily_review_pack(
        repo,
        review_date=review_date,
        days_back=days_back,
        max_items=max_items,
        focus_topic=focus_topic,
        knowledge_depth=knowledge_depth,
    )

    if result_path and result_path.exists():
        content = result_path.read_text(encoding="utf-8")
    else:
        content = "# Daily Review\n\n暂无复习内容。"

    from app.workflows import load_daily_review_snapshot
    snapshot = load_daily_review_snapshot(repo)

    from study_science.structured_tasks import StructuredTask

    structured_items = [
        StructuredTask(
            task_id=item["knowledge_id"],
            task_type="active_recall",
            prompt=f"Recall: {item.get('heading', '')}",
            evidence_refs=item.get("source_refs", []),
        ).as_dict()
        for item in snapshot.get("knowledge_points", [])
    ]
    structured_items.extend(
        StructuredTask(
            task_id=item["card_id"],
            task_type="mistake_review",
            prompt=f"Review: {item.get('topic', '')} / {item.get('los', '')}",
            evidence_refs=item.get("source_refs", []),
        ).as_dict()
        for item in snapshot.get("mistake_cards", [])
    )

    return ReviewPackResponse(
        review_id=snapshot["review_id"],
        generated_for=(review_date or datetime.now().date()).isoformat(),
        focus_topic=focus_topic or "unspecified",
        review_item_count=content.count("#### 下次规则"),
        warm_start_item_count=content.count("- **先问自己：**"),
        source_event_count=snapshot.get("source_event_count", 0),
        markdown_content=content,
        items=structured_items,
    )


@router.post("/{review_id}/complete", response_model=DailyReviewCompleteResponse)
async def complete_review(review_id: str, repo=Depends(get_repo)):
    """Mark all items in a generated Daily Review as reviewed once."""
    from app.workflows import complete_daily_review

    return DailyReviewCompleteResponse(**complete_daily_review(repo, review_id))


@router.get("/due")
async def list_due_items(repo=Depends(get_repo)):
    """List all due/overdue review items."""
    from app.workflows import collect_due_card_items, collect_pattern_items, collect_recent_low_confidence_items, merge_review_sources
    from datetime import date

    today = date.today()
    due = collect_due_card_items(repo, today)
    recent = collect_recent_low_confidence_items(repo, today, 7)
    patterns = collect_pattern_items(repo)
    merged = merge_review_sources(due, patterns, recent)

    return {
        "date": today.isoformat(),
        "total_due": len(due),
        "total_recent_low_confidence": len(recent),
        "total_patterns": len(patterns),
        "merged_count": len(merged),
        "top_items": [
            {
                "topic": item.get("topic", ""),
                "los": item.get("los", ""),
                "error_type": item.get("error_type", ""),
                "priority": item.get("priority", 0),
                "reasons": item.get("reasons", []),
            }
            for item in merged[:10]
        ],
    }
