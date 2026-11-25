---
change_type: implementation
verifications:
  - id: clef-contract
    requirement: Missing Cloudflare answers fail in CLI and MCP while valid fractional scores stay unchanged
    phase: pre-integration
    owner: conflux-acceptance
    trigger: pull-request-validation
    automation: Makefile
    evidence: make check
    rerun: make check
    prerequisites: []
    execution_class: repository-local
    completion_role: change-blocking
---

# Fix incomplete Cloudflare decision results

**Change Type**: implementation

Cloudflare can be reported as successful even when the response omits a requested answer. Reject that case in the shared Cloudflare path before printing CLI stdout or returning an MCP success. Keep other providers, existing exit mappings, valid fractional scores, and extra response fields unchanged. Clarify both MCP score descriptions to say levels start at zero and scores can be fractional, e.g. Clef probability-weighted scores. No live inference, push, release or deployment. Use synthetic responses only. Missing IDs fail with exit 1 and a bounded message without response content, including for auth test. Check only mapping-shaped questions; validation of present answer fields or non-object questions is out of scope.
