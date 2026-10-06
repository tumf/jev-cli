---
change_type: implementation
priority: medium
dependencies: []
references:
  - src/jev_cli/__init__.py
  - src/jev_cli/mcp_server.py
  - tests/test_jev.py
  - tests/test_mcp_server.py
  - openspec/specs/mcp-server/spec.md
verifications:
  - id: cloudflare-contract-tests
    requirement: Both models, typed answers, errors, credential isolation, and MCP parity pass deterministic tests
    phase: pre-integration
    owner: conflux-acceptance
    trigger: pull-request-validation
    automation: Makefile
    evidence: make test
    rerun: make test
    prerequisites: []
    execution_class: repository-local
    completion_role: change-blocking
rollback: Revert the Cloudflare provider commit; existing providers and credentials are unchanged.
---

# Add Cloudflare Clef decision models

**Change Type**: implementation

## Acceptance
- Both Clef variants select matching URL and payload model; defaults and existing providers do not change.
- Auth failures, in-band failures and malformed envelopes fail closed; tests validate noul, choice, score and --value.
- make test, make build and strict OpenSpec validate pass. Live inference requires separately available authorized credentials.

## Why
Users need Clef and Clef-flash through the existing Jev CLI and MCP decision contract, without a new framework or dependency.

## What Changes
- Add cloudflare provider, default clef-flash and explicit clef selection.
- Separate Cloudflare credentials and account/model REST endpoint construction.
- Normalize Workers AI result envelopes while preserving probability/score semantics.
- Expose the same provider in MCP and document CLI/MCP setup.

## Impact
- Affected spec: decision-providers (ADDED), mcp-server (ADDED requirement only).
- Affected code: shared client, MCP Provider/evaluate, existing unittest suite, READMEs and embedded skills.
- No release, public push, PR, deployment, or modification of existing worktrees. No RL training, media convenience flags, new dependencies, or changes to default official provider.
