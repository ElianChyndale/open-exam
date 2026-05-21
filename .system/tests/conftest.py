from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SYSTEM_ROOT = ROOT / ".system"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if str(SYSTEM_ROOT) not in sys.path:
    sys.path.insert(0, str(SYSTEM_ROOT))
