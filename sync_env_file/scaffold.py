"""Scaffold ``.chezmoi/`` for new projects."""

from __future__ import annotations

import sys
from importlib.resources import files
from pathlib import Path

from sync_env_file._constants import LOG_PREFIX

_GITIGNORE_LINES = (
    ".env",
    ".env.*",
    ".chezmoi/chezmoistate.boltdb",
)


def _template_text(name: str) -> str:
    return (files("sync_env_file") / "templates" / name).read_text(encoding="utf-8")


def run_init(*, force: bool = False, target_dir: Path | None = None) -> int:
    root = Path.cwd() if target_dir is None else target_dir.resolve()
    chezmoi_dir = root / ".chezmoi"
    chezmoi_dir.mkdir(parents=True, exist_ok=True)

    targets = {
        chezmoi_dir / "chezmoi.toml": _template_text("chezmoi.toml.tmpl"),
        chezmoi_dir / "private_dot_env.tmpl": _template_text("private_dot_env.tmpl"),
    }

    if not force:
        for path in targets:
            if path.exists():
                print(
                    f"{LOG_PREFIX} {path} already exists (use --force to overwrite)",
                    file=sys.stderr,
                )
                return 2

    for path, content in targets.items():
        path.write_text(content, encoding="utf-8")
        print(f"{LOG_PREFIX} wrote {path.relative_to(root)}")

    gitignore = root / ".gitignore"
    if gitignore.exists():
        existing = gitignore.read_text(encoding="utf-8").splitlines()
        missing = [line for line in _GITIGNORE_LINES if line not in existing]
        if missing:
            suffix = "" if existing and existing[-1] == "" else "\n"
            gitignore.write_text(
                gitignore.read_text(encoding="utf-8")
                + suffix
                + "\n".join(missing)
                + "\n",
                encoding="utf-8",
            )
            print(f"{LOG_PREFIX} updated .gitignore")
    else:
        gitignore.write_text("\n".join(_GITIGNORE_LINES) + "\n", encoding="utf-8")
        print(f"{LOG_PREFIX} wrote .gitignore")

    return 0
