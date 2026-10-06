## 1. Implement shared provider
- [x] verification-id: cloudflare-contract-tests — 1.1 Add cloudflare credential/default model and validated model-aware endpoints; preserve other provider contracts.
- [x] verification-id: cloudflare-contract-tests — 1.2 Unwrap Cloudflare envelopes and normalize typed answers without inventing values; fail on malformed/in-band failure.
- [x] verification-id: cloudflare-contract-tests — 1.3 Pass effective model through CLI and MCP endpoints and expose cloudflare in MCP schema.

## 2. Tests and documentation
- [x] verification-id: cloudflare-contract-tests — 2.1 Add deterministic unittest coverage for both models, account/model rejection, credentials, envelope errors, typed values, run passthrough and MCP parity; update existing PROVIDERS traversal tests (generic custom-model and None endpoint assumptions) for Cloudflare; demonstrate tests fail before implementation.
- [x] verification-id: cloudflare-contract-tests — 2.2 Update English/Japanese READMEs and skill sources; regenerate embedded skills.
- [x] verification-id: cloudflare-contract-tests — 2.3 Run make check, full unittest suite, CLI help and strict OpenSpec validation, recording actual results. No public push/release.
- [x] verification-id: cloudflare-contract-tests — 2.4 Keep spec deltas archive-ready (additive decision-providers spec, additive mcp-server requirement, no rewrite of unrelated canonical requirements), stage only change-owned files and leave other operators' worktrees untouched; archive and commits are owned by the Conflux archive/apply stages. Report live inference as unverified because approved Cloudflare credentials are unavailable (verification: contract tests via make test; live inference not-testable here).

## Notes
- Test-first evidence: before the implementation, `uv run --python 3.13 -m unittest discover -s tests` ran 78 tests with `FAILED (failures=12, errors=42)` (new Cloudflare tests and the PROVIDERS-derived MCP schema enum test). After the implementation, the same command reported `Ran 78 tests ... OK`.
- `make check` (embed-skills, full unittest suite, `uv build`) passed: 78 tests OK; built `dist/jev_cli-0.6.2.tar.gz` and wheel. Version was not bumped, and there was no push or release.
- CLI help lists `--provider {official,vercel,openrouter,custom,cloudflare}` for evaluation and auth commands, with default still `official`; `jev noul --provider cloudflare` without `CLOUDFLARE_ACCOUNT_ID` exits 2 with a structured error and no network access.
- `cflx openspec validate add-cloudflare-clef --strict` passed.
- Live inference is UNVERIFIED: `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` are absent in this environment, so no request was sent to Cloudflare. Envelope fixtures are derived from the documented Clef schema-output.json (fetched 2026-10-06), and they are contract tests rather than observed inference.
- Decision: a missing cloudflare entry next to other stored providers keeps the existing `stored cloudflare API key is empty` message (unchanged `api_key` behavior).
- Acceptance repair (acceptance-cloudflare-falsy-run-model): `src/jev_cli/mcp_server.py` changed only to pass `payload["model"]` (always set by setdefault/question_request) so the sentinel default in `provider_endpoint` applies only when a model is truly omitted. After the fix, `make check` ran 80 tests OK and `cflx openspec validate add-cloudflare-clef --strict` passed.
- Archive and commits are not performed by apply; Conflux owns the final Apply commit and the archive stage.

## Final Validation
- `cflx openspec validate add-cloudflare-clef --strict`
- `cflx openspec validate add-cloudflare-clef --archive-gate`
- `make test`
- Corrected delivery baseline: `feat/cloudflare-clef` derives from `origin/main`; video assets and the video-only Japanese README are excluded. Latest `make check`: 81 tests OK and v0.6.3 wheel/sdist built; canonical strict validation passed.
