from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from sync_env_file.azure_cli import ensure_az_logged_in
from sync_env_file.chezmoi import build_chezmoi_apply_command, repo_root
from sync_env_file.dotenv import format_dotenv_value
from sync_env_file import tools


def _fake_which(name: str) -> str:
    return f"/usr/bin/{name}"


def test_format_dotenv_value_quotes_connection_string() -> None:
    raw = "Endpoint=sb://x.servicebus.windows.net/;SharedAccessKey=a+b=c;EntityPath=p#1"
    quoted = format_dotenv_value(raw)
    assert quoted.startswith('"') and quoted.endswith('"')
    assert "SharedAccessKey=a+b=c" in quoted


def test_format_dotenv_value_quotes_dollar_sign_username() -> None:
    assert format_dotenv_value("$ConnectionString") == '"$ConnectionString"'


def test_repo_root_finds_chezmoi(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    chezmoi_dir = tmp_path / ".chezmoi"
    chezmoi_dir.mkdir()
    (chezmoi_dir / "chezmoi.toml").write_text('[azureKeyVault]\ndefaultVault = "x"\n', encoding="utf-8")
    nested = tmp_path / "src" / "app"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)
    root = repo_root()
    assert root == tmp_path


def test_build_chezmoi_apply_command_uses_repo_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tools.shutil, "which", _fake_which)
    chezmoi_dir = tmp_path / ".chezmoi"
    chezmoi_dir.mkdir()
    (chezmoi_dir / "chezmoi.toml").write_text('[azureKeyVault]\ndefaultVault = "x"\n', encoding="utf-8")
    cmd = build_chezmoi_apply_command(tmp_path)
    assert cmd[0] == "/usr/bin/chezmoi"
    assert str(tmp_path / ".chezmoi") in cmd
    assert str(tmp_path) in cmd
    assert cmd[-1] == ".env"


def test_tool_command_wraps_az_cmd_on_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    az_path = r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"

    def fake_which(name: str) -> str | None:
        return az_path if name == "az" else None

    monkeypatch.setattr(tools.os, "name", "nt")
    monkeypatch.setattr(tools.shutil, "which", fake_which)
    assert tools.tool_command("az", "account", "show") == [
        "cmd.exe",
        "/c",
        az_path,
        "account",
        "show",
    ]


def test_tool_command_uses_resolved_exe_on_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    chezmoi_path = r"C:\bin\chezmoi.exe"

    def fake_which(name: str) -> str | None:
        return chezmoi_path if name == "chezmoi" else None

    monkeypatch.setattr(tools.os, "name", "nt")
    monkeypatch.setattr(tools.shutil, "which", fake_which)
    assert tools.tool_command("chezmoi", "apply") == [chezmoi_path, "apply"]


def test_ensure_az_logged_in_requires_active_account() -> None:
    def fail_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(cmd, 1, "", "")

    with pytest.raises(RuntimeError, match="az login"):
        ensure_az_logged_in(run=fail_run)
