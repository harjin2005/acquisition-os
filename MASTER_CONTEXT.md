# MASTER_CONTEXT.md — AcquisitionOS / Founder-OS

**The first thing every AI session reads. Refreshed weekly by skill; diffs human-approved. Keep <3k tokens — pointers over prose.**
**As of: 2026-07-07 · Refresh owner: Founder**

## Mission & positioning
Decision-quality **Acquisition Operating System** for 2–10-person US real-estate investment teams (flip + buy-and-hold). Accuracy is the product; workflow is the retention; outcome data is the moat; knowledge graph is the intelligence layer; AI is an implementation detail. (Proposed ADR-009.)

## Company state
Stage: pre-build, documentation phases 0–4 complete. Customers: 0 (design-partner recruiting = top priority). Revenue: $0. Team: founder + engineers TBD (**ADR-006 open — blocks sprint dating**). Funding/runway: UNKNOWN (ADR-006).

## Current plan
Next milestone: Sprint 1 (repo foundation, per DOC-131 §2 — fully specified). Critical path: vendor data contract → ingestion → underwriting golden datasets → accuracy-gated GA (metro 1, ~S18). External clocks: vendor negotiation (start immediately), 10DLC (start ~S7), design partners (≥5 signed before PRD freeze).

## Current priorities (top 3)
1. Recruit design partners (≥15 interviews, ≥5 LOIs w/ data-sharing) — DD gate 3.
2. Vendor term sheet with derivative/persistence rights — DD gate 4 / risk ER1.
3. Sprint 1 execution per DOC-131.

## Decisions (register: /docs/decisions/ · full log DOC-001 v0.4)
Accepted: ADR-001 wedge ICP · ADR-002 hybrid data (licensed + derived moat) · ADR-003 outreach = human-approved campaigns, no AI voice · ADR-004 three agents (Prioritization, Underwriting, Follow-up) · ADR-005 3–5 disclosure-state metros.
Proposed: ADR-009 positioning · ADR-010 architecture (modular monolith, Python/FastAPI, Postgres+RLS, Temporal, AWS) · ADR-011 pricing ($299/$599/$1,199 + usage wallet).
Open: ADR-006 runway/team · ADR-007 founder assets · ADR-008 metro selection.

## Top risks (full registers: DOC-110 §6, DOC-131 §4)
R1/ER4 accuracy insufficient or ungateable · ER1 vendor contract slip · R3/ER3 TCPA/suppression failure (SEV-1 class) · R2 wedge churn · R4 data COGS/terms break margins.

## Architecture & stack (DOC-130)
Monorepo · modular monolith FastAPI + Next.js · Postgres 16 (schemas: licensed/core/derived; RLS; pgvector) · Temporal Cloud · ElastiCache(Valkey) · Meilisearch Cloud · AWS ECS Fargate + Terraform · LiteLLM gateway + Langfuse evals · WorkOS · Stripe. Non-negotiables: ontology naming law (DOC-002) · module boundary graph (import-linter) · expand-contract migrations · eval gates on agent paths · suppression enforced below agents.

## KPIs (targets, DOC-120 §12 — no actuals yet)
NSM: Underwritten Deals Closed/org/mo ≥1.0 by M5. Guardrails: median ARV error beats baseline AVM ≥15% rel.; acted-upon ≥40%; suppression violations = 0. Business: GM ≥75% (kill floor 60%), churn ≤3%/mo.

## Open questions (U-register, DOC-120 §12b)
U1 interview-validated pain ranking · U2 vendor terms/COGS · U3 rehab estimation path · U5 MLS access · U6 ADR-006/007 · U7 metros · U9 backtest-demo conversion.

## Document map
Governance: DOC-000 roadmap · DOC-001 decisions · DOC-002 ontology (normative). Diligence: DOC-110 (verdict BUILD WITH CHANGES + 5 binding gates). Company: DOC-120 blueprint · DOC-121 PRD/UX (v0.9 gated). Engineering: DOC-130 handbook · DOC-131 execution (Sprint 1 executable). Jarvis: /docs/jarvis/ (start: ExecutiveSummary.md, Architecture.md).
