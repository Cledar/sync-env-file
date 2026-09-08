"""Azure CLI login checks."""

from __future__ import annotations

import subprocess
from collections.abc import Callable

from sync_env_file._constants import LOG_PREFIX
from sync_env_file.tools import tool_command

RunFn = Callable[..., subprocess.CompletedProcess[str]]


def ensure_az_logged_in(run: RunFn = subprocess.run) -> None:
    result = run(
        tool_command("az", "account", "show", "--output", "none"),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"{LOG_PREFIX} no active az account; run: az login")
