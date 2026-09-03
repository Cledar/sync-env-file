from __future__ import annotations

import pytest

FAKE_TOOL_DIR = "/usr/bin"


@pytest.fixture(autouse=True)
def mock_external_clis(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep unit tests independent of az/chezmoi on the runner PATH."""

    def fake_which(name: str) -> str:
        return f"{FAKE_TOOL_DIR}/{name}"

    monkeypatch.setattr("sync_env_file.tools.shutil.which", fake_which)
