"""Printable review card generator — produces 3×5 card layout PDF from due cards.

Uses ReportLab for PDF generation. Install with: pip install reportlab
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from app.storage import Repository


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

    from app.workflows import parse_frontmatter, extract_markdown_section, clean_display_text

    # Collect cards from question-errors
    cards: list[dict] = []
    for path in sorted((repo.memory_root / "question-errors").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        card_topic = fm.get("topic", "")

        if topic and topic.lower() not in card_topic.lower():
            continue

        prompt = extract_markdown_section(text, "Prompt") or "No prompt captured"
        wrong = extract_markdown_section(text, "Wrong Output") or ""
        correct = fm.get("correct_resolution", "")
        fix_rule = fm.get("fix_rule", "")
        next_drill = fm.get("next_drill", "")
        los = fm.get("los", "")

        cards.append({
            "card_id": path.stem,
            "topic": card_topic,
            "los": los,
            "prompt": clean_display_text(prompt[:200]),
            "wrong": clean_display_text(wrong[:100]),
            "correct": clean_display_text(correct[:200]),
            "fix_rule": clean_display_text(fix_rule[:150]),
            "next_drill": clean_display_text(next_drill[:150]),
        })

        if len(cards) >= limit:
            break

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

    for index, card in enumerate(cards):
        page_index = index // 15  # 15 cards per page (3×5)
        pos_in_page = index % 15
        col = pos_in_page % 3
        row = pos_in_page // 3

        x = margin_x + col * card_w
        y = page_h - margin_y - (row + 1) * card_h

        if pos_in_page == 0 and index > 0:
            c.showPage()

        # Card border
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.5)
        c.rect(x, y, card_w, card_h)

        # Front content
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(colors.HexColor("#333333"))
        c.drawString(x + 4, y + card_h - 10, f"{card['topic']} | {card['los']}")

        c.setFont("Helvetica", 6)
        c.setFillColor(colors.HexColor("#666666"))
        # Wrap prompt text
        prompt_lines = _wrap_text(c, card["prompt"], card_w - 8, 6)
        for li, line in enumerate(prompt_lines[:6]):
            c.drawString(x + 4, y + card_h - 22 - li * 8, line)

        # Card ID at bottom
        c.setFont("Helvetica", 5)
        c.setFillColor(colors.HexColor("#999999"))
        short_id = card["card_id"][-8:] if len(card["card_id"]) > 8 else card["card_id"]
        c.drawString(x + 4, y + 2, f"#{short_id}")

        # Draw BACK of card (on the right side of same card space)
        # Since we can't do double-sided easily in ReportLab without knowing printer,
        # we put a small "back" indicator and the fix rule
        if card["fix_rule"]:
            c.setFont("Helvetica", 5)
            c.setFillColor(colors.HexColor("#22c55e"))
            c.drawString(x + 4, y + card_h - 72, f"✓ {card['fix_rule'][:60]}")

        if card["next_drill"]:
            c.setFont("Helvetica", 5)
            c.setFillColor(colors.HexColor("#6366f1"))
            c.drawString(x + 4, y + card_h - 82, f"→ {card['next_drill'][:60]}")

    c.save()
    return out_path


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
