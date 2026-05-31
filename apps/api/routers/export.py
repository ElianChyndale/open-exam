"""GET /api/export/* — Structured data export endpoints."""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, Response
from deps import get_repo

router = APIRouter()


@router.get("")
async def export_portable_backup(repo=Depends(get_repo)):
    """Export the explicit local-transfer envelope."""
    from app.sync_service import export_all

    return export_all(repo)


@router.get("/events.json")
async def export_events(repo=Depends(get_repo)):
    """Export all events as structured JSON."""
    events = repo.load_events()
    return {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").UTC).isoformat(),
        "count": len(events),
        "events": [e.as_dict() for e in events],
    }


@router.get("/cards.json")
async def export_cards(repo=Depends(get_repo)):
    """Export all mistake cards as structured JSON."""
    cards = []
    for domain in ("question-errors", "cognitive-bias", "agent-failures"):
        domain_path = repo.memory_root / domain
        if not domain_path.exists():
            continue
        for path in sorted(domain_path.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            frontmatter = {}
            lines = text.splitlines()
            if lines and lines[0].strip() == "---":
                for line in lines[1:]:
                    if line.strip() == "---":
                        break
                    if ":" in line:
                        key, value = line.split(":", 1)
                        frontmatter[key.strip()] = value.strip()
            cards.append({
                "card_id": path.stem,
                "domain": domain,
                **frontmatter,
            })

    return {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").UTC).isoformat(),
        "count": len(cards),
        "cards": cards,
    }


@router.get("/patterns.json")
async def export_patterns(repo=Depends(get_repo)):
    """Export all patterns as structured JSON."""
    patterns = []
    patterns_path = repo.memory_root / "patterns"
    if patterns_path.exists():
        for path in sorted(patterns_path.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            frontmatter = {}
            lines = text.splitlines()
            if lines and lines[0].strip() == "---":
                for line in lines[1:]:
                    if line.strip() == "---":
                        break
                    if ":" in line:
                        key, value = line.split(":", 1)
                        frontmatter[key.strip()] = value.strip()
            patterns.append({
                "pattern_id": path.stem,
                **frontmatter,
            })

    return {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").UTC).isoformat(),
        "count": len(patterns),
        "patterns": patterns,
    }


@router.get("/weekly-report.md")
async def export_weekly_report(repo=Depends(get_repo)):
    """Export a compact evidence-linked weekly learner report."""
    from app.workflows import load_progress_events

    today = date.today()
    start = today - timedelta(days=6)
    attempts = [
        attempt for attempt in repo.load_attempt_records()
        if str(attempt.get("created_at", ""))[:10] >= start.isoformat()
    ]
    wrong = [attempt for attempt in attempts if not attempt.get("is_correct")]
    completed = [
        event for event in load_progress_events(repo)
        if event.get("record_type") == "daily_review_completed"
        and event.get("status") in {"completed", "done"}
        and str(event.get("date") or event.get("created_at", ""))[:10] >= start.isoformat()
    ]
    accuracy = sum(1 for attempt in attempts if attempt.get("is_correct")) / len(attempts) if attempts else 0.0
    lines = [
        "# OpenExam Weekly Learner Report",
        "",
        f"- Period: {start.isoformat()} to {today.isoformat()}",
        f"- Attempts: {len(attempts)}",
        f"- Accuracy: {accuracy:.1%}",
        f"- Wrong attempts: {len(wrong)}",
        f"- Daily Reviews completed: {len(completed)}",
        "",
        "## Evidence",
        *[
            f"- {attempt.get('topic', '')} / {attempt.get('los', '')} / {attempt.get('attempt_id', '')}"
            for attempt in wrong[:10]
        ],
    ]
    return Response("\n".join(lines) + "\n", media_type="text/markdown")


@router.get("/review-cards.pdf")
async def export_review_cards_pdf(topic: str = "", limit: int = 20, repo=Depends(get_repo)):
    """Generate a due-card-only printable PDF."""
    from app.card_printer import generate_print_cards

    export_dir = repo.memory_root / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    path = export_dir / f"review-cards-{date.today().isoformat()}.pdf"
    try:
        generated = generate_print_cards(repo, topic=topic, limit=limit, output_path=str(path))
    except ImportError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return FileResponse(generated, media_type="application/pdf", filename=generated.name)
