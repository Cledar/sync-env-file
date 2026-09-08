"""Sync flow: chezmoi apply to render ``.env``."""

from __future__ import annotations

import subprocess
import sys

from sync_env_file._constants import LOG_PREFIX
from sync_env_file.azure_cli import ensure_az_logged_in
from sync_env_file.chezmoi import build_chezmoi_apply_command, repo_root
from sync_env_file.tools import resolve_tool


def ensure_tools() -> None:
    resolve_tool("chezmoi")
    resolve_tool("az")


def run_sync() -> int:
    try:
        ensure_tools()
        ensure_az_logged_in()
        root = repo_root()
        cmd = build_chezmoi_apply_command(root)
    except (FileNotFoundError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "chezmoi apply failed").strip()
        print(f"{LOG_PREFIX} {message}", file=sys.stderr)
        return result.returncode

    print(f"{LOG_PREFIX} wrote .env")
    return 0
