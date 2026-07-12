---
name: spec-checker
description: Validates an implementation diff against the DOC-121 PRD section for the module.
---

# spec-checker

Given a module path (e.g. `backend/app/modules/underwriting`), read the matching section in `docs/product/21-prd-ux-blueprint-v0.9.md` and check:

- Does the router expose the endpoints the PRD requires? Are naming and shapes consistent with DOC-002?
- Are the state machines implemented as documented?
- Are receipts / freshness / confidence surfaces present when the PRD mandates them?
- Are compliance-visible behaviors (opt-out, DSR, quiet hours) implemented and tested?

If a documented behavior is missing, flag it as a blocker. If the PRD is ambiguous, propose a specific interpretation and ask for confirmation — do not silently pick one.
