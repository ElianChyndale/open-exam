from __future__ import annotations

import re
from typing import Any


def _timestamp(value: str) -> float:
    hours, minutes, seconds = value.replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def _subtitle_segments(content: str) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    blocks = re.split(r"\n\s*\n", content.strip())
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip() and line.strip() != "WEBVTT"]
        timing_index = next((index for index, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            continue
        start, end = [part.strip() for part in lines[timing_index].split("-->", 1)]
        text = " ".join(lines[timing_index + 1:]).strip()
        if text:
            segments.append({"text": text, "locator": f"time:{start}-{end}", "start_time": _timestamp(start), "end_time": _timestamp(end)})
    return segments


def _text_segments(content: str, locator_prefix: str = "chars") -> list[dict[str, Any]]:
    segments = []
    for match in re.finditer(r"[^.!?。！？]+[.!?。！？]?", content):
        text = match.group(0).strip()
        if text:
            segments.append({"text": text, "locator": f"{locator_prefix}:{match.start()}-{match.end()}"})
    return segments


def segment_content(content: str, import_format: str) -> list[dict[str, Any]]:
    normalized = import_format.lower()
    if normalized in {"srt", "vtt", "subtitle"}:
        return _subtitle_segments(content)
    if normalized == "pdf":
        segments = []
        for page, text in enumerate(content.split("\f"), start=1):
            for segment in _text_segments(text, f"page:{page}:chars"):
                segment["page_locator"] = f"page:{page}"
                segments.append(segment)
        return segments
    if normalized == "epub":
        return _text_segments(content, "chapter:1:chars")
    if normalized == "audio":
        return []
    return _text_segments(content)
