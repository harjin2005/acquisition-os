# Jarvis Implementation Roadmap

**Standing constraint:** Jarvis serves AcquisitionOS's velocity. Investment caps: V1 ≤ 1 founder-week; thereafter ≤10% founder time and ~0 engineer time until product milestone M3 (DOC-131). Every phase has a measurable exit.

## V1 — Substrate (weeks 1–2, alongside product Sprint 1)
Founder-os repo from scaffold · MASTER_CONTEXT.md live · Decision Engine (register + SOPs) · Claude Code environment (rules/skills/hooks incl. end-of-session write-back) · memory pipeline for git/meetings/calendar/tasks (Postgres+pgvector, one ingestion service) · daily brief v1 (static markdown, scheduled) · Research capability L1 with adapter watchlists · SOP seed set.
**Exit metric:** founder starts every session from MASTER_CONTEXT; zero "where is that decision?" moments for two consecutive weeks; brief read daily.

## V2 — Cadence & assembly (months 2–6, background)
Finance close-pack assembly · Legal obligation register + intake SOP live · Growth calendar + claim-verified drafting · design-partner CRM in memory · weekly-review + board-pack skills · graph queries (the five acceptance queries) · Langfuse/COGS feeds into brief · first L2 promotion candidates reviewed (research scheduling, security digests).
**Exit metric:** board pack in <1 hour; close pack by day 5; ≥2 capabilities promoted with KPI evidence.

## V3 — Extraction & platform (months 6–12, post-M3)
Extract `/platform/engineering-kit` + `ai-kit` from the product repo (dedup the gateway) · capability dashboards replace static brief *if* the brief proved insufficient (decision record required) · portfolio-ready namespacing hardened · Startup Factory SOP dry-run (instantiate a toy domain end-to-end as the test).
**Exit metric:** factory dry-run produces Phase-0-complete docs for a toy domain in ≤2 weeks with >80% scaffold reuse.

## Long-term
Startup #2 instantiation post-GA (StartupFactory gate) · portfolio Executive view · self-improvement loop formalized (capability KPIs reviewed like agent evals) · Jarvis remains domain-independent by the adapter rule — audited quarterly.

## Migration strategy
Nothing to migrate *from* except scattered docs: week 1 includes a one-time sweep of all existing artifacts (DOC-000..131, notes, contracts) into the repo + memory with provenance. Future migrations (e.g., tracker change) are adapter-level by design.
