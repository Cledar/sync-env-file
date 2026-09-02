"""Verify required keys exist in ``.env`` without printing secret values."""

from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_KEYS = (
    "APP_API_BASE_URL",
    "APP_DATABASE_PASSWORD",
    "APP_EVENTHUB_CONNECTION_STRING",
)


def parse_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, raw = stripped.split("=", 1)
        key = key.strip()
        value = raw.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        values[key] = value
    return values


def main() -> int:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.is_file():
        print("verify_env: missing .env", file=sys.stderr)
        return 1

    values = parse_dotenv(env_path)
    ok = 0
    for key in REQUIRED_KEYS:
        if values.get(key):
            hidden = " (value hidden)" if key != "APP_API_BASE_URL" else ""
            print(f"verify_env: OK {key}{hidden}")
            ok += 1
        else:
            print(f"verify_env: MISSING {key}", file=sys.stderr)

    print(f"verify_env: {ok}/{len(REQUIRED_KEYS)} required keys present")
    return 0 if ok == len(REQUIRED_KEYS) else 1


if __name__ == "__main__":
    sys.exit(main())
