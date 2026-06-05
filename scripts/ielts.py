from __future__ import annotations

import runpy
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = ROOT / "ielts-claude-skills" / "shared" / "ielts_cli.py"


if __name__ == "__main__":
    if not CLI_PATH.exists():
        raise SystemExit(f"IELTS CLI not found: {CLI_PATH}")
    subprocess.run([sys.executable, str(CLI_PATH), "init"], check=False, capture_output=True)
    sys.argv[0] = str(CLI_PATH)
    runpy.run_path(str(CLI_PATH), run_name="__main__")
