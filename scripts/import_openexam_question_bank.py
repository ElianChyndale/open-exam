"""Import normalized private question records into OpenExam quarantine."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT / ".system", ROOT / "apps" / "api"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.storage import LocalRepository
from services.practice_service import import_questions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="JSON array of normalized private question records")
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    questions = json.loads(args.input.read_text(encoding="utf-8"))
    result = import_questions(LocalRepository(args.root), args.source_name, questions)
    print(json.dumps({key: result[key] for key in ("import_batch_id", "verified_count", "quarantined_count")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
