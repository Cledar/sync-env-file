"""Dotenv value quoting rules (reference for chezmoi ``| quote`` output)."""

from __future__ import annotations

import re

_UNQUOTED_SAFE_RE = re.compile(r"^[A-Za-z0-9_./:@+-]+$")


def format_dotenv_value(value: str) -> str:
    if value == "":
        return ""
    if _UNQUOTED_SAFE_RE.fullmatch(value):
        return value
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )
    return f'"{escaped}"'
