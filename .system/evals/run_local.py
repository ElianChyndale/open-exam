from __future__ import annotations

import json
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.cli import run_cli


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="cfa-tier1-evals-"))
    cases = []
    with (Path(__file__).with_name("cases.jsonl")).open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                cases.append(json.loads(line))

    for case in cases:
        command = [case["command"], "--payload", json.dumps(case["payload"], ensure_ascii=False)]
        code = run_cli(command, repo_root=root)
        if code != 0:
            return code

    run_cli(["mine-patterns"], repo_root=root)
    run_cli(["pre-mock-brief"], repo_root=root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
