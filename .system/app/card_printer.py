"""Printable review card generator — produces 3×5 card layout PDF from due cards.

Uses ReportLab for PDF generation. Install with: pip install reportlab
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from app.storage import Repository


def collect_due_print_cards(
    repo: Repository,
    topic: str = "",
    limit: int = 20,
    review_date: str | date | None = None,
) -> list[dict]:
    """Collect due mistake cards for PDF rendering."""
    from app.workflows import clean_display_text, extract_markdown_section, parse_date, parse_frontmatter

    target_date = date.fromisoformat(review_date) if isinstance(review_date, str) else review_date or date.today()
    cards: list[dict] = []
    for path in sorted((repo.memory_root / "question-errors").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        card_topic = fm.get("topic", "")
        due_at = parse_date(fm.get("review_due_at", ""))
        if not due_at or due_at > target_date:
            continue
        if topic and topic.lower() not in card_topic.lower():
            continue

        cards.append({
            "card_id": path.stem,
            "topic": card_topic,
            "los": fm.get("los", ""),
            "prompt": clean_display_text((extract_markdown_section(text, "Prompt") or "No prompt captured")[:200]),
            "wrong": clean_display_text((extract_markdown_section(text, "Wrong Output") or "")[:100]),
            "correct": clean_display_text(fm.get("correct_resolution", "")[:200]),
            "fix_rule": clean_display_text(fm.get("fix_rule", "")[:150]),
            "next_drill": clean_display_text(fm.get("next_drill", "")[:150]),
            "review_due_at": due_at.isoformat(),
        })
        if len(cards) >= limit:
            break
    return cards


def generate_print_cards(
    repo: Repository,
    topic: str = "",
    limit: int = 20,
    output_path: str | None = None,
) -> Path:
    """Generate a PDF with 3×5 review cards from due mistake cards.

    Each card has:
    - FRONT: card_id, topic, LOS, prompt/question
    - BACK: correct answer, fix_rule, next_drill

    Args:
        repo: Repository instance
        topic: Filter by topic (empty = all topics)
        limit: Maximum number of cards to include
        output_path: Output PDF path (default: review-cards-YYYY-MM-DD.pdf)

    Returns:
        Path to the generated PDF.
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.lib.units import inch
        from reportlab.pdfgen import canvas
    except ImportError:
        raise ImportError("ReportLab required. Install: pip install reportlab")

    cards = collect_due_print_cards(repo, topic=topic, limit=limit)

    if not cards:
        raise ValueError("No cards found matching the criteria")

    # Generate PDF
    today_str = date.today().isoformat()
    out_path = Path(output_path or f"review-cards-{today_str}.pdf")

    # 3x5 card layout: 3 columns x 5 rows per page
    # Card size: ~2.5in x 1.5in (fits 3x5 on letter)
    page_w, page_h = landscape(letter)
    margin_x = 0.5 * inch
    margin_y = 0.5 * inch
    card_w = (page_w - 2 * margin_x) / 3
    card_h = (page_h - 2 * margin_y) / 5

    c = canvas.Canvas(str(out_path), pagesize=landscape(letter))
    c.setTitle(f"ExamOS Review Cards - {today_str}")

    for page_start in range(0, len(cards), 15):
        page_cards = cards[page_start : page_start + 15]
        for pos_in_page, card in enumerate(page_cards):
            col = pos_in_page % 3
            row = pos_in_page // 3
            x = margin_x + col * card_w
            y = page_h - margin_y - (row + 1) * card_h
            _draw_card_front(c, colors, card, x, y, card_w, card_h)
        c.showPage()

        # Mirror columns so each back aligns after duplex printing on the long edge.
        for pos_in_page, card in enumerate(page_cards):
            col = 2 - (pos_in_page % 3)
            row = pos_in_page // 3
            x = margin_x + col * card_w
            y = page_h - margin_y - (row + 1) * card_h
            _draw_card_back(c, colors, card, x, y, card_w, card_h)
        if page_start + 15 < len(cards):
            c.showPage()

    c.save()
    return out_path


def _draw_card_front(c, colors, card: dict, x: float, y: float, card_w: float, card_h: float) -> None:
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(0.5)
    c.rect(x, y, card_w, card_h)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(x + 4, y + card_h - 10, f"{card['topic']} | {card['los']}")
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor("#666666"))
    for index, line in enumerate(_wrap_text(c, card["prompt"], card_w - 8, 6)[:7]):
        c.drawString(x + 4, y + card_h - 22 - index * 8, line)
    _draw_card_id(c, colors, card, x, y)


def _draw_card_back(c, colors, card: dict, x: float, y: float, card_w: float, card_h: float) -> None:
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(0.5)
    c.rect(x, y, card_w, card_h)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(x + 4, y + card_h - 10, "Correct solution")
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor("#444444"))
    lines = _wrap_text(c, card["correct"] or "See source evidence.", card_w - 8, 6)
    for index, line in enumerate(lines[:4]):
        c.drawString(x + 4, y + card_h - 22 - index * 8, line)
    c.setFont("Helvetica", 5)
    c.setFillColor(colors.HexColor("#16803A"))
    c.drawString(x + 4, y + 19, f"Rule: {card['fix_rule'][:70]}")
    c.setFillColor(colors.HexColor("#4F46E5"))
    c.drawString(x + 4, y + 11, f"Next: {card['next_drill'][:70]}")
    _draw_card_id(c, colors, card, x, y)


def _draw_card_id(c, colors, card: dict, x: float, y: float) -> None:
    c.setFont("Helvetica", 5)
    c.setFillColor(colors.HexColor("#999999"))
    short_id = card["card_id"][-8:] if len(card["card_id"]) > 8 else card["card_id"]
    c.drawString(x + 4, y + 2, f"#{short_id}")


def _wrap_text(canvas_obj, text: str, max_width: float, font_size: int) -> list[str]:
    """Simple text wrapping for PDF generation."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        w = canvas_obj.stringWidth(test, "Helvetica", font_size)
        if w > max_width and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines if lines else [text[:80]]
