#!/usr/bin/env python3
"""Verify wheel and sdist contents before PyPI publish."""

from __future__ import annotations

import sys
import tarfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import NoReturn

FORBIDDEN_TOKENS = (
    "platform-e2e",
    "cledar-sdk",
    "E2E_",
    "osint",
    "gitlab.com/cledar",
    "kvdevosintplatform",
)

_TEXT_SUFFIXES = (".py", ".md", ".tmpl", ".toml", ".txt")
_TEXT_FILENAMES = {"LICENSE", "METADATA", "PKG-INFO", "entry_points.txt"}

_SDIST_ALLOWED = {
    ".gitignore",
    "LICENSE",
    "README.md",
    "pyproject.toml",
    "PKG-INFO",
}


def _fail(message: str) -> NoReturn:
    print(f"check_package_artifacts: {message}", file=sys.stderr)
    sys.exit(1)


def _assert_no_forbidden_tokens(text: str, label: str) -> None:
    lowered = text.lower()
    for token in FORBIDDEN_TOKENS:
        if token.lower() in lowered:
            _fail(f"{token!r} found in {label}")


def _is_text_path(path: str) -> bool:
    item = PurePosixPath(path)
    return item.name in _TEXT_FILENAMES or item.suffix.lower() in _TEXT_SUFFIXES


def _assert_safe_archive_path(path: str, label: str) -> None:
    item = PurePosixPath(path)
    if item.is_absolute() or ".." in item.parts:
        _fail(f"unsafe path in {label}: {path!r}")


def check_wheel(out_dir: Path) -> None:
    wheels = sorted(out_dir.glob("*.whl"))
    if len(wheels) != 1:
        _fail(f"expected exactly one wheel in {out_dir}, found {len(wheels)}")
    with zipfile.ZipFile(wheels[0]) as zf:
        names = zf.namelist()
        dist_info_roots = {
            PurePosixPath(name).parts[0]
            for name in names
            if PurePosixPath(name).parts
            and PurePosixPath(name).parts[0].endswith(".dist-info")
        }
        if len(dist_info_roots) != 1:
            _fail("wheel must contain exactly one .dist-info directory")
        allowed_roots = {"sync_env_file", *dist_info_roots}
        for name in names:
            _assert_safe_archive_path(name, "wheel")
            parts = PurePosixPath(name).parts
            if parts and parts[0] not in allowed_roots:
                _fail(f"unexpected top-level path in wheel: {name!r}")
        if any("examples/" in name for name in names):
            _fail("wheel must not include examples/")
        if any("/tests/" in name for name in names):
            _fail("wheel must not include tests/")
        for name in names:
            if not _is_text_path(name):
                continue
            _assert_no_forbidden_tokens(
                zf.read(name).decode("utf-8"),
                f"wheel:{name}",
            )


def check_sdist(out_dir: Path) -> None:
    sdists = sorted(out_dir.glob("*.tar.gz"))
    if len(sdists) != 1:
        _fail(f"expected exactly one sdist in {out_dir}, found {len(sdists)}")
    with tarfile.open(sdists[0], "r:gz") as tf:
        members = tf.getmembers()
        for member in members:
            _assert_safe_archive_path(member.name, "sdist")
        roots = {
            PurePosixPath(member.name).parts[0]
            for member in members
            if PurePosixPath(member.name).parts
        }
        if len(roots) != 1:
            _fail("sdist must contain exactly one top-level directory")
        for member in members:
            parts = PurePosixPath(member.name).parts
            if len(parts) == 1:
                continue
            path = PurePosixPath(*parts[1:]).as_posix()
            if path not in _SDIST_ALLOWED and not path.startswith("sync_env_file/"):
                _fail(
                    "sdist must only ship package sources and core metadata, "
                    f"not {path!r}"
                )
            if member.isfile() and _is_text_path(path):
                extracted = tf.extractfile(member)
                if extracted is None:
                    _fail(f"could not read sdist member {member.name!r}")
                _assert_no_forbidden_tokens(
                    extracted.read().decode("utf-8"),
                    f"sdist:{path}",
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
