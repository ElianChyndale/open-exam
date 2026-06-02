from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SYSTEM_ROOT = ROOT / ".system"
LANGUAGE_SCIENCE_SRC = ROOT / "packages" / "language-science" / "src"
STUDY_SCIENCE_SRC = ROOT / "packages" / "study-science" / "src"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if str(SYSTEM_ROOT) not in sys.path:
    sys.path.insert(0, str(SYSTEM_ROOT))

if str(LANGUAGE_SCIENCE_SRC) not in sys.path:
    sys.path.insert(0, str(LANGUAGE_SCIENCE_SRC))

if str(STUDY_SCIENCE_SRC) not in sys.path:
    sys.path.insert(0, str(STUDY_SCIENCE_SRC))
