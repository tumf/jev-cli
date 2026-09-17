# jev-cli

A small, dependency-free command-line client for [TypeSafe Jev](https://docs.typesafe.ai/introduction). It turns text or JSON state into typed `noul`, `choice`, and `score` answers.

> This is an independent community project. It is not affiliated with or endorsed by TypeSafe AI.

## Requirements

- Python 3.13 or later
- A TypeSafe API key

## Install

Clone the repository and install it with [uv](https://docs.astral.sh/uv/) through the Makefile:

```bash
git clone https://github.com/tumf/jev-cli.git
cd jev-cli
make install
```

Check the installation:

```bash
jev-cli --version
```

## Authentication

`TYPESAFE_API_KEY` takes precedence when it is set:

```bash
export TYPESAFE_API_KEY='your-api-key'
```

Otherwise, save the key in the CLI's private credential file. The directory is created with mode `0700` and the file with mode `0600`.

```bash
pbpaste | jev-cli auth set
jev-cli auth status
```

The fallback path follows XDG conventions:

- `$XDG_CONFIG_HOME/jev-cli/credentials.json` when `XDG_CONFIG_HOME` is set
- `~/.config/jev-cli/credentials.json` otherwise

The key is never printed by `auth status`.

## Usage

### Yes/no probability

Use `noul` for a focused yes/no judgment. `--value` prints only the probability.

```bash
jev-cli noul \
  'Does this message express urgency?' \
  'Please restore service today.' \
  --value
```

### Choose one option

Use `choice` with one or more `KEY=DESCRIPTION` options.

```bash
jev-cli choice \
  'Which team should handle this?' \
  'The payment integration keeps failing.' \
  -o 'billing=Payment, charge, or refund issues' \
  -o 'technical=Bugs or integration failures' \
  -o 'other=None of these' \
  --pretty
```

### Score ordered levels

Use `score` with ordered levels. Levels are numbered from zero.

```bash
jev-cli score \
  'How frustrated is the customer?' \
  'This has failed for three days. Please help.' \
  -l 'Calm' \
  -l 'Concerned but civil' \
  -l 'Very angry' \
  --value
```

### Read stdin or a file

Pass `-` or omit the state to read stdin. Prefix a path with `@` to read a file.

```bash
pbpaste | jev-cli noul 'Does this request a refund?' --value
jev-cli noul 'Does this document mention security risks?' @document.txt --value
```

### Structured state

Use `--json-state` when the state is JSON.

```bash
printf '%s' '{"message":"Please respond today"}' | \
  jev-cli noul 'Does `message` express urgency?' --json-state --value
```

### Batch questions

Use `run` with a complete System One request to evaluate multiple questions in one API call.

```bash
jev-cli run request.json --pretty
cat request.json | jev-cli run - --pretty
```

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Success |
| `1` | Unexpected API response or other error |
| `2` | Invalid arguments or input |
| `3` | Authentication error |
| `4` | Connection, rate-limit, or transient server error |

Errors are emitted as JSON on stderr.

## Development

Run the test suite:

```bash
make test
```

Build the package:

```bash
make build
```

Run both checks:

```bash
make check
```

## License

[MIT](LICENSE)
