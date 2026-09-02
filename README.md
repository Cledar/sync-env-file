# sync-env-file

Generate a local `.env` from chezmoi templates and Azure Key Vault secrets.

## Installation

From PyPI:

```bash
pip install sync-env-file
```

Using uv:

```bash
uv add sync-env-file
```

Requires Python 3.12.7+, [chezmoi](https://www.chezmoi.io/), and the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/).

## Quick start

```bash
sync-env-file init
# Edit .chezmoi/chezmoi.toml and .chezmoi/private_dot_env.tmpl
az login
sync-env-file
```

## Extended example

See [examples/minimal-consumer/](examples/minimal-consumer/) for a full PyPI-first consumer project (not shipped in the wheel).

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
