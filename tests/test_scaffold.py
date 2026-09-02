from __future__ import annotations

from pathlib import Path

import pytest

from sync_env_file.scaffold import run_init


def test_init_writes_chezmoi_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert run_init() == 0
    assert (tmp_path / ".chezmoi" / "chezmoi.toml").is_file()
    assert (tmp_path / ".chezmoi" / "private_dot_env.tmpl").is_file()
    assert (tmp_path / ".gitignore").is_file()


def test_init_refuses_overwrite_without_force(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert run_init() == 0
    assert run_init() == 2


def test_init_force_overwrites(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert run_init() == 0
    config = tmp_path / ".chezmoi" / "chezmoi.toml"
    config.write_text("stale", encoding="utf-8")
    assert run_init(force=True) == 0
    assert "your-vault-name" in config.read_text(encoding="utf-8")
