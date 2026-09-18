# CLI reference

## Authentication

Check whether authentication is available without printing the key:

```bash
jev auth status
```

Connect to Jev and verify that the resolved API key is accepted:

```bash
jev auth test
```

In a terminal, enter the API key at the hidden prompt:

```bash
jev auth set
```

For non-interactive automation, stdin remains supported:

```bash
printf '%s' "$TYPESAFE_API_KEY" | jev auth set
```

Resolution order:

1. The selected provider's environment variable: `TYPESAFE_API_KEY`, `AI_GATEWAY_API_KEY`, `OPENROUTER_API_KEY`, or `JEV_API_KEY`
2. `$XDG_CONFIG_HOME/jev-cli/credentials.json`
3. `~/.config/jev-cli/credentials.json`

The official TypeSafe API is selected by default. Vercel AI Gateway and OpenRouter can be selected per command:

```bash
jev auth set --provider vercel
jev auth test --provider vercel
jev noul --provider vercel -q 'Is this urgent?' -s 'Restore service today.' --value

jev auth set --provider openrouter
jev auth test --provider openrouter
jev noul --provider openrouter -q 'Is this urgent?' -s 'Restore service today.' --value
```

`JEV_PROVIDER` changes the default for evaluation commands. Authentication commands require an explicit `--provider` so credentials are not accidentally stored or tested against the wrong service.

For a proxy implementing the native Jev contract:

```bash
JEV_PROVIDER=custom \
JEV_ENDPOINT='https://proxy.example.com/v1/systemone' \
JEV_API_KEY='your-proxy-api-key' \
jev noul -q 'Is this urgent?' -s 'Restore service today.' --value
```

Set `JEV_MODEL` or pass `--model` when the proxy requires a different model name. Use only a trusted HTTPS endpoint because the custom bearer key is sent to it.

## Typed questions

Use `-q` for `--question` and `-s` for `--state` when a shorter command is useful. `--value` has no short form.

Return a yes/no probability from `0` to `1`:

```bash
jev noul --question 'Does this message require an urgent response?' --state 'Please respond today.'
```

Choose one stable key from explicit criteria:

```bash
jev choice --question 'Which team should receive this?' --state 'Checkout returns HTTP 500.' \
  -o engineering='Software defect or technical failure' \
  -o sales='Purchase or pricing question'
```

Score against ordered levels:

```bash
jev score --question 'How dissatisfied is this customer?' --state 'This is the third failure.' \
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
jev noul --question 'Does this require action?' --state 'Please investigate.'
```

File content:

```bash
jev noul --question 'Does this require action?' --state @message.txt
```

Standard input:

```bash
printf '%s' 'Please investigate.' | jev noul --question 'Does this require action?' --state -
```

Structured JSON state:

```bash
printf '%s' '{"message":"Please investigate","priority":"high"}' | \
  jev noul --question 'Does this require action?' --state - --json-state
```

## Output controls

Pretty JSON:

```bash
jev noul --question 'Does this require action?' --state 'Please investigate.' --pretty
```

Primary scalar only:

```bash
jev noul --question 'Does this require action?' --state 'Please investigate.' --value
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

Install the bundled `jev-cli` Agent Skill:

```bash
jev install-skills
jev install-skills --global
jev install-skills --claude
jev install-skills --global --claude
```