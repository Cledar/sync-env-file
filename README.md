# sync-env-file

Generate a local `.env` from chezmoi templates and Azure Key Vault secrets.

## Why it exists

Local development often needs a `.env` file with a mix of committed defaults and secrets from a vault. Teams usually solve this with one-off shell scripts that are hard to reuse across projects.

`sync-env-file` provides a small, generic CLI that:

- Keeps templates under version control via [chezmoi](https://www.chezmoi.io/)
- Pulls secrets from [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/) at render time
- Writes a single repo-root `.env` with one command

No bespoke scripts, no copy-pasted vault logic.

## Installation

### Recommended: `uvx` (no project dependency)

Requires [uv](https://docs.astral.sh/uv/). `uvx` runs the CLI from an isolated Python 3.9+ environment, so the project does not need this package as a dependency:

```bash
uvx sync-env-file init
uvx sync-env-file
```

### Other install options

From PyPI:

```bash
pip install sync-env-file
```

As a project dependency with uv:

```bash
uv add sync-env-file
```

Requires Python 3.9+, [chezmoi](https://www.chezmoi.io/), and the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/) (external tools — not installed by the package or `uvx`).

## Quick start

With `uvx` (no project dependency):

```bash
uvx sync-env-file init
# Edit .chezmoi/chezmoi.toml and .chezmoi/private_dot_env.tmpl
az login
uvx sync-env-file
```

If installed via `pip` or `uv add`, omit the `uvx` prefix:

```bash
sync-env-file init
# Edit .chezmoi/chezmoi.toml and .chezmoi/private_dot_env.tmpl
az login
sync-env-file
```

## API overview

| Command | Description |
| --- | --- |
| `sync-env-file` | Same as `sync-env-file sync` |
| `sync-env-file sync` | Render `.env` from `.chezmoi/` templates (requires `az login`) |
| `sync-env-file init` | Scaffold `.chezmoi/chezmoi.toml`, `private_dot_env.tmpl`, and `.gitignore` entries |
| `sync-env-file init --force` | Overwrite existing scaffold files |

Exit codes: `0` on success, non-zero on tool errors (missing chezmoi/az, no active Azure account, chezmoi apply failure).

## Configuration

After `init`, edit two files under `.chezmoi/`:

### `chezmoi.toml`

Sets the default Key Vault name:

```toml
[azureKeyVault]
defaultVault = "your-vault-name"
```

`sync-env-file` passes `--config`, `--source`, and `--destination` to chezmoi so paths stay repo-relative.

### `private_dot_env.tmpl`

Defines the rendered `.env` content. Use chezmoi's `azureKeyVault` template function for secrets:

```text
APP_BASE_URL=https://api.example.com
APP_API_KEY={{ azureKeyVault "example-api-key" | quote }}
```

See [examples/minimal-consumer/.chezmoi/private_dot_env.tmpl](https://github.com/Cledar/sync-env-file/blob/main/examples/minimal-consumer/.chezmoi/private_dot_env.tmpl) for additional patterns (connection strings, optional passthrough variables).

## Extended example

See [examples/minimal-consumer/](https://github.com/Cledar/sync-env-file/tree/main/examples/minimal-consumer) for a full PyPI-first consumer project (not shipped in the wheel).

## Limitations

- Requires **chezmoi** and **Azure CLI** installed and on `PATH`
- Secrets are fetched from **Azure Key Vault only** (no AWS/GCP vaults)
- Renders a single target file: repo-root **`.env`**
- Requires an active Azure account with RBAC read access to the configured vault
- Does not manage chezmoi installation, vault provisioning, or secret rotation

## Roadmap

- [ ] Optional support for additional secret backends (if demand exists)
- [ ] Richer scaffold templates for common connection-string patterns

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

CI and the advisory semantic-version check run on GitHub-hosted `ubuntu-latest`
runners with read-only repository permissions. Public pull requests do not need
access to the organization's self-hosted runners. The manual PyPI release
workflow is managed separately; see the release instructions below.

## Releasing

Releases are published to PyPI from the GitHub Actions workflow in this repository; the steps are in [CONTRIBUTING](https://github.com/Cledar/sync-env-file/blob/main/CONTRIBUTING.md#releasing-to-pypi).

## How to contribute

See [CONTRIBUTING](https://github.com/Cledar/sync-env-file/blob/main/CONTRIBUTING.md) for issue reporting, development setup, and pull request guidelines.

## Maintainers

- [@arog-lahcim](https://github.com/arog-lahcim) — primary maintainer

## License

Apache License 2.0 — see [LICENSE](https://github.com/Cledar/sync-env-file/blob/main/LICENSE).
