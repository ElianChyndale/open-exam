"""GET /api/export/* — Structured data export endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from deps import get_repo

router = APIRouter()


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
