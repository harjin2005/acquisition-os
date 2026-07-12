# Engineering Capability

**Purpose:** ship the product fast inside hard rails. This capability already exists at L2 — it *is* DOC-130/131 — Jarvis generalizes it for reuse.

**Responsibilities:** architecture governance (ADR discipline) · Claude Code development per playbook · repo management · PR review workflow (reviewer subagents + human) · CI/CD ownership · QA/testing strategy · release management · debt register upkeep · infra via Terraform modules.
**Inputs:** PRDs, sprint plan, incident reports. **Outputs:** shipped software, ADRs, runbooks, debt entries. **Knowledge sources:** docs/product mirror, module READMEs, past incident memory. **Memory writes:** PR summaries (auto), ADRs, incident postmortems, release notes.
**Tools:** the entire DOC-131 §1 environment (rules, skills, hooks, subagents) — Jarvis's contribution is packaging it as the **reusable engineering kit**: `.claude/` scaffold, CI workflow templates, Terraform modules, module-anatomy generator, RLS/test harness patterns → `/platform/engineering-kit` at V3 extraction.
**Approval rules:** merges = human review always; prod deploys = manual approval; compliance-module PRs = designated owner (inherited from DOC-131).
**Decision boundaries:** no dependency without OSS-table entry; no boundary-graph violation (import-linter is law); no schema name outside the glossary.
**Failure modes → mitigations:** are DOC-131 §4's ER-items; Jarvis adds one: *kit drift* between startups → kit versioned, startups pin + upgrade deliberately.
**KPIs:** DOC-120 §12 engineering rows (deploy freq, change-fail rate) + kit reuse ratio at Startup #2 (target: >80% of scaffold unchanged).
**Continuous improvement:** monthly playbook retro — every recurring Claude Code correction becomes a rule; every repeated workflow becomes a skill (the DOC-131 doctrine, on a schedule).
