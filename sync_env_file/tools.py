"""Resolve external CLI tools on PATH."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from sync_env_file._constants import LOG_PREFIX, WINDOWS_SCRIPT_SUFFIXES


def resolve_tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise RuntimeError(f"{LOG_PREFIX} {name} not found in PATH")
    return path


def _running_on_windows() -> bool:
    return os.name == "nt"


def tool_command(name: str, *args: str) -> list[str]:
    executable = resolve_tool(name)
    suffix = Path(executable).suffix.lower()
    if _running_on_windows() and suffix in WINDOWS_SCRIPT_SUFFIXES:
        return ["cmd.exe", "/c", executable, *args]
    return [executable, *args]
