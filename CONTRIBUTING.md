# Contributing to sync-env-file

Thank you for your interest in contributing.

## Reporting issues

Open a [GitHub issue](https://github.com/Cledar/sync-env-file/issues) with:

- A clear description of the problem or feature request
- Steps to reproduce (for bugs)
- Your environment (OS, Python version, chezmoi and Azure CLI versions)

Do not include secrets, `.env` contents, or Key Vault values in issue reports.

## Development setup

Requires Python 3.9+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone git@github.com:Cledar/sync-env-file.git
cd sync-env-file
uv sync
```

Run the full check suite before opening a pull request:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy sync_env_file
```

Optional: install pre-commit hooks.

```bash
uv run pre-commit install
```

## Pull requests

1. Fork the repository and create a feature branch from `main`.
2. Keep changes focused — one logical change per PR.
3. Add or update tests for behaviour changes.
4. Ensure all checks pass locally.
5. Open a PR with a clear description of what changed and why.

Maintainers will review for correctness, safety, and alignment with project scope.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
type: short description
type(TICKET-123): short description
```

Allowed types: `feat`, `fix`, `perf`, `build`, `ci`, `refactor`, `style`, `test`, `docs`.

Examples:

```
feat: add support for multiple vault aliases
fix(CPL-1329): handle missing chezmoi config gracefully
docs: clarify Azure RBAC requirements
```

## Code style

- **Ruff** for linting and formatting (line length 88)
- **mypy** in strict mode
- Docstrings on public modules and functions
- No runtime dependencies beyond the Python standard library

Match the style of surrounding code. Avoid unrelated refactors in the same PR.

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
`release.yaml`, with no GitHub environment. The repository is public. If the
organization plan changes, add a protected `pypi` environment and update the
PyPI publisher tuple in the same reviewed change before the next release.

Build artifacts expire after 14 days. If an upload partially fails, stop and
inspect PyPI before retrying. Published files cannot be overwritten; yank a bad
release and publish a reviewed higher version instead of reusing its version.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE), the same license that covers this project.
