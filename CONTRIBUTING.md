# Contributing

Contributions are welcome through GitHub issues and pull requests.

## Development setup

Install Python 3.13 or later, [uv](https://docs.astral.sh/uv/), and GNU Make. Clone the repository, then create the development environment:

```bash
uv sync
```

## Development commands

Run the complete local quality gate before committing. This executes the unit tests and builds both the wheel and source distribution.

```bash
make check
```

Run an individual task when needed:

```bash
make test
make build
make install
```

`make install` installs the local package with `uv tool` and verifies the resulting `jev` command.

## Versioning

The project follows [Semantic Versioning](https://semver.org/). The version source of truth is `project.version` in `pyproject.toml`.

## Pull requests

- Keep changes focused.
- Add or update tests for behavior changes.
- Update the README when the command interface changes.
- Do not commit API keys, credential files, `.env` files, or personal paths.
- Ensure `make check` passes before submitting.

By contributing, you agree that your contributions are licensed under the MIT License.
