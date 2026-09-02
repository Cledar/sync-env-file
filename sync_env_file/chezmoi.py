"""Chezmoi repository discovery and apply command construction."""

from __future__ import annotations

from pathlib import Path

from sync_env_file._constants import LOG_PREFIX
from sync_env_file.tools import tool_command


def repo_root(start: Path | None = None) -> Path:
    path = Path.cwd() if start is None else start.resolve()
    if path.is_file():
        path = path.parent
    for candidate in (path, *path.parents):
        if (candidate / ".chezmoi" / "chezmoi.toml").is_file():
            return candidate
    raise FileNotFoundError(f"{LOG_PREFIX} .chezmoi/chezmoi.toml not found")


def build_chezmoi_apply_command(root: Path) -> list[str]:
    chezmoi_dir = root / ".chezmoi"
    config = chezmoi_dir / "chezmoi.toml"
    return [
        *tool_command(
            "chezmoi",
            "--config",
            str(config),
            "--source",
            str(chezmoi_dir),
            "--destination",
            str(root),
            "apply",
            "--force",
            ".env",
        ),
    ]
