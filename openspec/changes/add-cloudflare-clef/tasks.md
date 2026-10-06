## 1. Implement shared provider
- [ ] verification-id: cloudflare-contract-tests — 1.1 Add cloudflare credential/default model and validated model-aware endpoints; preserve other provider contracts.
- [ ] verification-id: cloudflare-contract-tests — 1.2 Unwrap Cloudflare envelopes and normalize typed answers without inventing values; fail on malformed/in-band failure.
- [ ] verification-id: cloudflare-contract-tests — 1.3 Pass effective model through CLI and MCP endpoints and expose cloudflare in MCP schema.

## 2. Tests and documentation
- [ ] verification-id: cloudflare-contract-tests — 2.1 Add deterministic unittest coverage for both models, account/model rejection, credentials, envelope errors, typed values, run passthrough and MCP parity; update existing PROVIDERS traversal tests (generic custom-model and None endpoint assumptions) for Cloudflare; demonstrate tests fail before implementation.
- [ ] verification-id: cloudflare-contract-tests — 2.2 Update English/Japanese READMEs and skill sources; regenerate embedded skills.
- [ ] verification-id: cloudflare-contract-tests — 2.3 Run make check, full unittest suite, CLI help and strict OpenSpec validation, recording actual results. No public push/release.
- [ ] verification-id: cloudflare-contract-tests — 2.4 Archive with canonical spec parity and clean thematic commits; keep other operators' worktrees untouched. Report live inference as unverified if approved credentials are unavailable.
