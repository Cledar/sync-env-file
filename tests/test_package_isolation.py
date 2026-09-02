from __future__ import annotations

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


def _assert_no_forbidden_tokens(text: str, label: str) -> None:
    lowered = text.lower()
    for token in FORBIDDEN_TOKENS:
        assert token.lower() not in lowered, f"{token!r} found in {label}"


def test_package_sources_exclude_forbidden_tokens() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    paths = [repo_root / "sync_env_file", repo_root / "README.md"]
    for path in paths:
        if path.is_dir():
            files = list(path.rglob("*"))
        else:
            files = [path]
        for file in files:
            if file.suffix not in _TEXT_SUFFIXES:
                continue
            _assert_no_forbidden_tokens(
                file.read_text(encoding="utf-8"),
                str(file.relative_to(repo_root)),
            )
