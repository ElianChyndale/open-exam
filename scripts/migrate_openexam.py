"""Create or upgrade rebuildable OpenExam local indexes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSTEM = ROOT / ".system"
if str(SYSTEM) not in sys.path:
    sys.path.insert(0, str(SYSTEM))

from app.storage import CATALOG_SCHEMA_VERSION, LocalRepository


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    LocalRepository(args.root).ensure_layout()
    print(f"OpenExam local catalog schema v{CATALOG_SCHEMA_VERSION} ready")


if __name__ == "__main__":
    main()
