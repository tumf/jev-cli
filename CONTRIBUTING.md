# Contributing

Contributions are welcome through GitHub issues and pull requests.

## Development setup

Install [uv](https://docs.astral.sh/uv/), clone the repository, then run:

```bash
uv sync
uv run --python 3.13 -m unittest discover -s tests -v
```

## Pull requests

- Keep changes focused.
- Add or update tests for behavior changes.
- Update the README when the command interface changes.
- Do not commit API keys, credential files, `.env` files, or personal paths.
- Ensure the test suite and `uv build` pass before submitting.

By contributing, you agree that your contributions are licensed under the MIT License.
