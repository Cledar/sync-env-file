# Contributing to sync-env-file

Thank you for your interest in contributing. This project follows the [Cledar Open-Source Publication Guidelines](https://app.notion.com/p/2b10f2e73c5b80d9b1a5fc7ef306a708).

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

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE), the same license that covers this project.
