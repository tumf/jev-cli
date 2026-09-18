---
name: jev-cli
description: Use when classifying or scoring state with the `jev` CLI.
version: 0.1.0
author: tumf
license: MIT
metadata:
  hermes:
    tags: [jev, cli, classification, scoring]
    related_skills: []
---

# jev-cli

## Overview

Use the `jev` command to ask TypeSafe Jev typed questions about text or JSON state. Prefer this skill when a task needs a compact machine-readable probability, one choice from explicit criteria, an ordered score, or several typed answers in one request.

The package and repository are named `jev-cli`; the installed command is `jev`.

## Workflow

1. Confirm the command is installed with `jev --version`. If it is missing, install from the repository root with `make install`. Completion: `jev --version` exits successfully.
2. Confirm authentication with `jev auth status`. If absent, ask the user to provide or configure a TypeSafe API key; never print, infer, or commit it. Completion: the status command returns `ok: true`.
3. Choose the narrowest question type:
   - `noul` for a yes/no probability.
   - `choice` for one key from explicit options.
   - `score` for an ordered numeric level.
   - `run` for a complete request object or multiple questions.
4. Send only the state needed for the judgment. TypeSafe receives the submitted state and questions, so do not send secrets or private data without explicit authorization.
5. Use default JSON output for automation. Use `--value` only when a scalar is sufficient. Completion: parse the result and account for the exit code before acting on it.

Read [references/cli.md](references/cli.md) for copy-paste command forms, inputs, output controls, and exit codes.

## Decision rules

- Give `choice` options stable keys and descriptions that make the categories mutually understandable.
- Give `score` levels in ascending order; the returned number may be fractional.
- Use `--json-state` only when the state must retain JSON structure.
- Use `@file` or stdin for long input instead of embedding it in shell arguments.
- Set `TYPESAFE_API_KEY` only for process-level overrides. The normal credential store remains under the user's config directory.
- Treat model output as a structured judgment, not verified fact. Keep consequential actions behind the caller's own validation and authorization rules.

## Common pitfalls

1. **Calling the executable `jev-cli`.** The package is `jev-cli`, but the executable is `jev`.
2. **Using `--value` with `run`.** Batched requests require the JSON response.
3. **Treating transport failures as negative answers.** Exit code `4` means retryable API or network failure, not a model judgment.
4. **Leaking state through convenience.** Inspect file and stdin content before submission when it may contain credentials or private records.
5. **Embedding an API key in examples.** Use `jev auth set` through stdin or the environment variable without writing its value into scripts or documentation.

## Verification checklist

- [ ] `jev --version` succeeds.
- [ ] `jev auth status` succeeds without exposing the key.
- [ ] The selected question type matches the desired answer shape.
- [ ] Submitted state contains no unauthorized secret or private data.
- [ ] The caller handles JSON and nonzero exit codes.
- [ ] Consequential follow-up actions retain their own authorization checks.
