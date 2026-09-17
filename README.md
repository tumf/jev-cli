# jev-cli

A small, dependency-free CLI for [TypeSafe Jev](https://docs.typesafe.ai/introduction). Send text or JSON state, ask typed questions, and receive machine-readable `noul`, `choice`, or `score` answers.

The `jev` command is useful when application code needs a fast classification or judgment instead of generated prose.

> This is an independent community project. It is not affiliated with or endorsed by TypeSafe AI.

## Features

- Supports all three Jev primitives: `noul`, `choice`, and `score`
- Sends multiple questions in one request with `run`
- Accepts text, JSON, files, and stdin
- Emits compact JSON by default
- Can print only the primary value for shell scripts
- Uses structured stderr errors and meaningful exit codes
- Has no runtime dependencies outside Python's standard library

## Requirements

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/)
- GNU Make
- A TypeSafe API key

## Install

Clone the repository and install the command with `uv tool` through the Makefile. This installs `jev` into uv's executable directory and verifies the installed version.

```bash
git clone https://github.com/tumf/jev-cli.git
cd jev-cli
make install
```

Verify that the command is available:

```bash
jev --version
```

Expected output:

```text
jev 0.2.0
```

## Authentication

The recommended approach for automation is the `TYPESAFE_API_KEY` environment variable. It takes precedence over the credential file.

```bash
export TYPESAFE_API_KEY='your-api-key'
jev auth status
```

For local use, pipe the key to the private credential store instead. `auth set` does not accept the key as a command-line argument, which keeps it out of process arguments and shell history.

```bash
printf '%s' 'your-api-key' | jev auth set
jev auth status
```

`auth status` reports only whether a key is available. It never prints the key.

The fallback credential path follows XDG conventions:

- `$XDG_CONFIG_HOME/jev-cli/credentials.json` when `XDG_CONFIG_HOME` is set
- `~/.config/jev-cli/credentials.json` otherwise

The credential directory is created with mode `0700`; the file is written atomically with mode `0600`.

## Quick start

Ask whether a message expresses urgency. `--value` prints only the resulting probability from `0` to `1`.

```bash
jev noul \
  'Does this message express urgency?' \
  'Please restore service today.' \
  --value
```

Example output:

```text
0.98
```

Without `--value`, the command returns the complete API response as JSON, including model and token usage.

```bash
jev noul \
  'Does this message express urgency?' \
  'Please restore service today.' \
  --pretty
```

## Question types

### Noul: yes/no probability

Use `noul` for one focused yes/no judgment. The value is the probability that the answer is yes.

```bash
jev noul \
  'Does this message request a refund?' \
  'The integration is broken, but I do not want a refund.' \
  --value
```

### Choice: select one option

Use `choice` when the answer must be one of a known set. Each option uses `KEY=DESCRIPTION` syntax.

```bash
jev choice \
  'Which team should handle this?' \
  'The payment integration keeps failing.' \
  -o 'billing=Payment, charge, or refund issues' \
  -o 'technical=Bugs or integration failures' \
  -o 'other=None of these' \
  --pretty
```

### Score: evaluate ordered levels

Use `score` for an ordered scale. Levels are numbered from zero in the order supplied.

```bash
jev score \
  'How frustrated is the customer?' \
  'This has failed for three days. Please help.' \
  -l 'Calm' \
  -l 'Concerned but civil' \
  -l 'Very angry' \
  --value
```

## Input formats

### Standard input

Omit the state or pass `-` to read it from stdin. This is useful for pipelines and avoids putting sensitive input in shell history.

```bash
printf '%s' 'Please resolve this today.' | \
  jev noul 'Does this message express urgency?' --value
```

### File input

Prefix a path with `@` to read its contents.

```bash
jev noul \
  'Does this document mention security risks?' \
  @document.txt \
  --value
```

### JSON state

Use `--json-state` to parse the state as JSON. Instructions can refer to named fields.

```bash
printf '%s' '{"message":"Please respond today"}' | \
  jev noul \
  'Does `message` express urgency?' \
  --json-state \
  --value
```

## Batch questions

Jev evaluates questions independently against the same state. Use `run` to send a complete System One request and avoid one API call per question.

Create `request.json`:

```json
{
  "state": {
    "message": "The payment integration has failed for three days. Please fix it today."
  },
  "model": "jev-latest",
  "questions": {
    "department": {
      "type": "choice",
      "instructions": "Which team should handle `message`?",
      "criteria": {
        "billing": "Payment, charge, or refund issues",
        "technical": "Bugs or integration failures",
        "other": "None of these"
      }
    },
    "urgent": {
      "type": "noul",
      "instructions": "Does `message` express urgency?"
    }
  }
}
```

Send it in one request:

```bash
jev run request.json --pretty
```

A request can also be piped through stdin:

```bash
cat request.json | jev run - --pretty
```

## Output and automation

The default stdout is one JSON object. Logs and structured errors go to stderr, so stdout can be piped directly into another program.

Use `--value` with `noul`, `choice`, or `score` when a script needs only the primary answer:

```bash
if awk 'BEGIN { exit !(ARGV[1] >= 0.9) }' \
  "$(jev noul 'Is this urgent?' 'Restore service today.' --value)"; then
  echo urgent
fi
```

Use `--model` to select another model available to the account:

```bash
jev noul 'Is this urgent?' 'Restore service today.' \
  --model jev-latest \
  --pretty
```

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Success |
| `1` | Unexpected API response or other error |
| `2` | Invalid arguments or input |
| `3` | Missing or rejected authentication |
| `4` | Connection, rate-limit, or transient server error |

An error is emitted as JSON on stderr:

```json
{"ok": false, "error": "TypeSafe API key is not stored; pipe it to: jev auth set"}
```

## Scope and limitations

The `jev` command is a thin client for focused System One judgments. It does not generate prose, perform arithmetic, compare dates, or replace application-level validation. Keep deterministic work in code and use Jev for semantic judgments.

The CLI sends the supplied state and questions to the TypeSafe API. Do not submit data that your organization is not permitted to send to that service.

## License

[MIT](LICENSE)
