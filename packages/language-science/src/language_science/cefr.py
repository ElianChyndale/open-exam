from __future__ import annotations

CEFR_ORDER = ["pre-a1", "a1", "a2", "b1", "b2", "c1", "c2"]

CEFR_NUMERIC: dict[str, int] = {
    "pre-a1": 0,
    "a1": 1,
    "a2": 2,
    "b1": 3,
    "b2": 4,
    "c1": 5,
    "c2": 6,
}


def _parse_cefr_range(value: str) -> tuple[int, int]:
    """Parse a CEFR range like 'A1-B2' or 'B1' into numeric bounds."""
    normalized = value.lower().strip().replace(" ", "")
    if "-" in normalized:
        low_str, high_str = normalized.split("-", 1)
    else:
        low_str = high_str = normalized
    low = CEFR_NUMERIC.get(low_str, 0)
    high = CEFR_NUMERIC.get(high_str, 6)
    return low, high


def _cefr_allowed(entry_level: str, user_min: str, user_max: str) -> bool:
    """Return True if entry_level falls within [user_min, user_max]."""
    if not entry_level:
        return True
    entry_level = entry_level.lower().strip()
    entry_val = CEFR_NUMERIC.get(entry_level)
    if entry_val is None:
        return True
    min_val = CEFR_NUMERIC.get(user_min.lower().strip(), 0)
    max_val = CEFR_NUMERIC.get(user_max.lower().strip(), 6)
    return min_val <= entry_val <= max_val
