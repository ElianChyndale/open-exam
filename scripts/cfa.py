from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYSTEM_ROOT = ROOT / ".system"

if str(SYSTEM_ROOT) not in sys.path:
    sys.path.insert(0, str(SYSTEM_ROOT))

from app.main import run_cli  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(run_cli())
