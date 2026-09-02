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


def tool_command(name: str, *args: str) -> list[str]:
    executable = resolve_tool(name)
    if os.name == "nt" and Path(executable).suffix.lower() in WINDOWS_SCRIPT_SUFFIXES:
        return ["cmd.exe", "/c", executable, *args]
    return [executable, *args]
