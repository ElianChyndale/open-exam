from __future__ import annotations

import json
from pathlib import Path
# The test invokes the repository's fixed CLI entry point without a shell.
import subprocess  # nosec B404
import sys


ROOT = Path(__file__).resolve().parents[2]


def test_resource_cli_cold_starts_provider_registry() -> None:
    completed = subprocess.run(  # nosec B603
        [sys.executable, "scripts/resources.py", "providers"],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
        timeout=30,
    )
    payload = json.loads(completed.stdout)
    assert any(provider["provider_id"] == "generic_web" for provider in payload["providers"])


def test_scheduler_scripts_are_explicit_user_operations() -> None:
    install = (ROOT / "scripts" / "install-resource-scheduler.ps1").read_text(encoding="utf-8")
    remove = (ROOT / "scripts" / "remove-resource-scheduler.ps1").read_text(encoding="utf-8")
    assert "schtasks.exe /Create" in install
    assert "/SC HOURLY /MO 6" in install
    assert "schtasks.exe /Delete" in remove
