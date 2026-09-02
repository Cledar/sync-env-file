# Minimal consumer example

End-to-end walkthrough for `sync-env-file` assuming the package is on public PyPI.

## Prerequisites

- Python 3.12.7, [uv](https://docs.astral.sh/uv/), [chezmoi](https://www.chezmoi.io/), Azure CLI
- `sync-env-file` on PyPI: `pip install sync-env-file`
- RBAC read access to secrets in your Key Vault

## Quick start

```bash
cd examples/minimal-consumer
uv sync
# Edit .chezmoi/chezmoi.toml (vault name) and private_dot_env.tmpl (secret names)
az login
uv run sync-env-file
uv run python verify_env.py
```

## Template patterns

| Block | Purpose |
| --- | --- |
| Optional `UV_INDEX` passthrough | Copy a shell variable into `.env` when set |
| `APP_API_*` literals | Non-secret defaults |
| `APP_DATABASE_PASSWORD` | Simple Key Vault secret |
| `APP_EVENTHUB_*` | Connection string + `$ConnectionString` username pattern |

## Troubleshooting

- `sync-env-file: no active az account` — run `az login`
- `chezmoi not found in PATH` — install chezmoi
- Key Vault secret not found — check secret id names in the template match your vault

## Relation to `sync-env-file init`

`init` writes a smaller scaffold. This directory is a reference implementation with verification.
