"""CLI entrypoint."""

from __future__ import annotations

import argparse
import sys

from sync_env_file.scaffold import run_init
from sync_env_file.sync import run_sync


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sync-env-file", description="Sync local .env via chezmoi"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("sync", help="Render .env from .chezmoi templates")
    init_parser = sub.add_parser(
        "init", help="Scaffold .chezmoi/ in the current directory"
    )
    init_parser.add_argument(
        "--force", action="store_true", help="Overwrite existing scaffold files"
    )

    args = parser.parse_args(argv)
    command = args.command or "sync"

    if command == "sync":
        return run_sync()
    if command == "init":
        return run_init(force=args.force)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
