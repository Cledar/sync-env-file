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

Run in any project directory without adding `sync-env-file` to `pyproject.toml` or running `uv sync`:

```bash
uvx sync-env-file init
uvx sync-env-file
```

`uvx` installs the CLI in an isolated environment for that invocation. Your project stays free of this package as a dependency.

Requires [uv](https://docs.astral.sh/uv/). `uvx` manages an isolated Python environment (3.9+); your project does not need this package as a dependency.

### Other install options

From PyPI (global or user install):

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

See [examples/minimal-consumer/.chezmoi/private_dot_env.tmpl](examples/minimal-consumer/.chezmoi/private_dot_env.tmpl) for additional patterns (connection strings, optional passthrough variables).

## Extended example

See [examples/minimal-consumer/](examples/minimal-consumer/) for a full PyPI-first consumer project (not shipped in the wheel).

## Limitations

- Requires **chezmoi** and **Azure CLI** installed and on `PATH`
- Secrets are fetched from **Azure Key Vault only** (no AWS/GCP vaults)
- Renders a single target file: repo-root **`.env`**
- Requires an active Azure account with RBAC read access to the configured vault
- Does not manage chezmoi installation, vault provisioning, or secret rotation

## Roadmap

- [ ] Initial public release on PyPI
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

## Releasing to PyPI

PyPI publication uses GitHub OIDC Trusted Publishing. The repository must not
contain a PyPI token, password, credential-bearing URL, or writable deploy key.
The semantic-version workflow is advisory only: it prints the proposed version
and never commits, tags, or publishes.

The release workflow is deliberately split into two manual invocations so the
exact wheel and sdist can be reviewed before the job receives OIDC permission:

1. Merge the version change to `main`, then create an immutable `vX.Y.Z` tag on
   that reviewed commit. The tag must match `project.version` in
   `pyproject.toml`.
2. Run **Release (PyPI)** from `main` with the tag and leave
   `artifact_run_id` empty. This runs tests, builds one wheel and one sdist,
   checks their contents, smoke-tests the wheel, and uploads them with
   `release-manifest.json`. It cannot request a PyPI OIDC token.
3. Review that workflow run and manifest. Approval for publication must name
   the PyPI owner, package, version, tag and commit, both artifact hashes, the
   workflow, and the build run ID.
4. Run the same workflow again from `main`, with the same tag and the approved
   build run ID in `artifact_run_id`. The publish job downloads that exact
   artifact, rechecks its manifest and hashes, verifies that the tag still
   points to a commit on `main`, and publishes with OIDC. It never rebuilds the
   distributions.

The Trusted Publisher tuple is repository `Cledar/sync-env-file`, workflow
`release.yaml`, with no GitHub environment while this private repository is on
a plan that does not provide environments. If repository visibility or the
organization plan changes, add a protected `pypi` environment and update the
PyPI publisher tuple in the same reviewed change before the next release.

Build artifacts expire after 14 days. If an upload partially fails, stop and
inspect PyPI before retrying. Published files cannot be overwritten; yank a bad
release and publish a reviewed higher version instead of reusing its version.

## How to contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for issue reporting, development setup, and pull request guidelines.

## Maintainers

- [@arog-lahcim](https://github.com/arog-lahcim) — primary maintainer

## License

Apache License 2.0 — see [LICENSE](LICENSE).
