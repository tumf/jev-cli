# CLI reference

## Authentication

Check whether authentication is available without printing the key:

```bash
jev auth status
```

Store an API key supplied through stdin:

```bash
printf '%s' "$TYPESAFE_API_KEY" | jev auth set
```

Resolution order:

1. `TYPESAFE_API_KEY`
2. `$XDG_CONFIG_HOME/jev-cli/credentials.json`
3. `~/.config/jev-cli/credentials.json`

## Typed questions

Return a yes/no probability from `0` to `1`:

```bash
jev noul 'Does this message require an urgent response?' 'Please respond today.'
```

Choose one stable key from explicit criteria:

```bash
jev choice 'Which team should receive this?' 'Checkout returns HTTP 500.' \
  -o engineering='Software defect or technical failure' \
  -o sales='Purchase or pricing question'
```

Score against ordered levels:

```bash
jev score 'How dissatisfied is this customer?' 'This is the third failure.' \
  -l 'Not dissatisfied' \
  -l 'Slightly dissatisfied' \
  -l 'Clearly dissatisfied' \
  -l 'Extremely dissatisfied'
```

Send a complete request from a file:

```bash
jev run request.json
```

## Input forms

Literal text:

```bash
jev noul 'Does this require action?' 'Please investigate.'
```

File content:

```bash
jev noul 'Does this require action?' @message.txt
```

Standard input:

```bash
printf '%s' 'Please investigate.' | jev noul 'Does this require action?' -
```

Structured JSON state:

```bash
printf '%s' '{"message":"Please investigate","priority":"high"}' | \
  jev noul 'Does this require action?' - --json-state
```

## Output controls

Pretty JSON:

```bash
jev noul 'Does this require action?' 'Please investigate.' --pretty
```

Primary scalar only:

```bash
jev noul 'Does this require action?' 'Please investigate.' --value
```

`--value` applies to `noul`, `choice`, and `score`, not `run`.

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Success |
| `1` | Invalid response or non-retryable API error |
| `2` | Local input or credential error |
| `3` | Authentication or authorization failure |
| `4` | Retryable network, rate-limit, or server failure |

Read stderr as JSON on failure. Do not interpret a nonzero exit as a model answer.

## Installation

From the repository root:

```bash
make install
jev --version
```

The project requires Python 3.13 or later and `uv`.