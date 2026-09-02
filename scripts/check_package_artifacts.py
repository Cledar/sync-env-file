#!/usr/bin/env python3
"""Verify wheel and sdist contents before PyPI publish."""

from __future__ import annotations

import sys
import tarfile
import zipfile
from pathlib import Path

FORBIDDEN_TOKENS = (
    "platform-e2e",
    "cledar-sdk",
    "E2E_",
    "osint",
    "gitlab.com/cledar",
    "kvdevosintplatform",
)

_TEXT_SUFFIXES = (".py", ".md", ".tmpl", ".toml")

_SDIST_ALLOWED = {
    ".gitignore",
    "LICENSE",
    "README.md",
    "pyproject.toml",
    "PKG-INFO",
}


def _fail(message: str) -> None:
    print(f"check_package_artifacts: {message}", file=sys.stderr)
    sys.exit(1)


def _assert_no_forbidden_tokens(text: str, label: str) -> None:
    lowered = text.lower()
    for token in FORBIDDEN_TOKENS:
        if token.lower() in lowered:
            _fail(f"{token!r} found in {label}")


def check_wheel(out_dir: Path) -> None:
    wheels = sorted(out_dir.glob("*.whl"))
    if not wheels:
        _fail(f"no wheel found in {out_dir}")
    with zipfile.ZipFile(wheels[0]) as zf:
        names = zf.namelist()
        if any("examples/" in name for name in names):
            _fail("wheel must not include examples/")
        if any("/tests/" in name for name in names):
            _fail("wheel must not include tests/")
        for name in names:
            if not name.endswith(_TEXT_SUFFIXES):
                continue
            _assert_no_forbidden_tokens(
                zf.read(name).decode("utf-8"),
                f"wheel:{name}",
            )


def check_sdist(out_dir: Path) -> None:
    sdists = sorted(out_dir.glob("*.tar.gz"))
    if not sdists:
        _fail(f"no sdist found in {out_dir}")
    with tarfile.open(sdists[0], "r:gz") as tf:
        names = tf.getnames()
    root = names[0].split("/")[0] + "/"
    rel = [n[len(root) :] for n in names if n.startswith(root) and n != root]
    for path in rel:
        if path in _SDIST_ALLOWED:
            continue
        if not path.startswith("sync_env_file/"):
            _fail(
                f"sdist must only ship package sources and core metadata, not {path!r}"
            )


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        _fail("usage: check_package_artifacts.py <build-out-dir>")
    out_dir = Path(args[0])
    if not out_dir.is_dir():
        _fail(f"build output directory not found: {out_dir}")
    check_wheel(out_dir)
    check_sdist(out_dir)
    print(f"check_package_artifacts: OK ({out_dir})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
