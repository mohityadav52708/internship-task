from __future__ import annotations

import os
import platform
import shlex
import subprocess
from pathlib import Path
from typing import Optional


def run_shell_command(command: str, cwd: Optional[str] = None, timeout_seconds: int = 60) -> str:
    safe_cwd = cwd or str(Path.cwd())
    completed = subprocess.run(
        shlex.split(command),
        cwd=safe_cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout_seconds,
    )
    return completed.stdout


def open_application(app: str) -> str:
    system = platform.system().lower()
    try:
        if system == "darwin":
            subprocess.Popen(["open", "-a", app])
        elif system == "windows":
            os.startfile(app)  # type: ignore[attr-defined]
        else:
            subprocess.Popen([app])
        return f"Opened application: {app}"
    except Exception as exc:  # noqa: BLE001
        return f"Failed to open application '{app}': {exc}"


def list_directory(path: str | None = None) -> str:
    p = Path(path) if path else Path.cwd()
    if not p.exists():
        return f"Path does not exist: {p}"
    entries = sorted([f.name for f in p.iterdir()])
    return "\n".join(entries)