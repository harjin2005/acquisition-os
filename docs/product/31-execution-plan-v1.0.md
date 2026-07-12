# DOC-131 — Execution Plan: Claude Code Playbook, Sprints, Debt & Risk

**Version:** 1.0
**Status:** Build-ready; Sprint 1 executable as written
**Companion:** DOC-130 (Engineering Handbook). Claude Code guidance verified against current docs and practice as of 2026-07-07; canonical reference: https://code.claude.com/docs (best practices, memory, subagents, hooks).

---

## 1. Claude Code Development Playbook

**Philosophy:** Claude Code is a force multiplier on a 1–5 person team only if the repo is engineered as its environment — memory lean, rules scoped, guarantees enforced by hooks and CI rather than by prose. Natural-language rules are advisory; hooks and CI are law.

### 1.1 Memory & context architecture
- **CLAUDE.md (repo root, target <150 lines, pruned monthly):** stack summary (five lines), the boundary graph from DOC-130 §3, the five non-negotiables (ontology naming law; module import rules; expand-contract migrations; tests ship with code; no new deps without OSS-table entry), pointers to docs/product/ and docs/modules/ (referenced with @-paths, not inlined).
- **.claude/rules/*.md with path globs:** `backend.md` (service/router split, tenancy wrapper mandatory, index-or-justify rule), `migrations.md` (expand-contract checklist, glossary-name check), `frontend.md` (SDK-only data access, QueryBoundary states, receipts components for AI surfaces), `agents.md` (prompt-change = version bump + eval, typed variables only, no provider SDKs outside gateway).
- **.claude/skills/:** `new-module` (scaffold matching DOC-130 module anatomy), `new-migration`, `vendor-adapter` (adapter contract + fixture snapshot procedure), `new-agent-eval` (manifest + thresholds + runner wiring), `compliance-change` (anything touching campaigns/suppression: checklist + required reviewers). Rule of thumb: any workflow explained twice becomes a skill.
- **.claude/agents/:** `code-reviewer` (reviews diff against the task's acceptance criteria and DOC-130 rules; instructed to flag correctness/requirement gaps only — no style bikeshedding); `schema-auditor` (migrations vs ontology + RLS presence); `spec-checker` (implementation vs DOC-121 module section). Subagents also used for scoped research so exploration doesn't flood the main context.
- **Hooks (deterministic guarantees):** PreToolUse deny-list (no edits under `db/migrations/` applied without the migration skill checklist; block writes to `.env*`, `infra/envs/prod` without explicit confirmation); PostToolUse format+lint on edited files; Stop hook runs the affected module's fast tests and blocks completion on failure. CLAUDE.md reminds; hooks enforce.

### 1.2 Working method
- **Plan mode first** for any task >1 file or touching campaigns/underwriting/privacy; the plan is reviewed by a human before execution. Vertical slices (schema → service → API → UI → tests) over horizontal layers.
- **Prompt strategy:** every task prompt references (a) the DOC-121 module section, (b) the module README, (c) acceptance criteria from the sprint plan. Paste the failing test or bug, state the goal, don't micromanage the how. After two failed correction loops: /clear and rewrite the prompt rather than accumulating polluted context.
- **Verification doctrine:** Claude must show evidence — test output, command results — not assertions. If it can't be verified, it doesn't ship. The code-reviewer subagent reviews every non-trivial diff before the human does.
- **Branch/PR:** trunk-based; one task = one branch = one PR; PR description generated but human-edited; **a human reviews every PR** — Claude Code authorship doesn't waive review (compliance modules require the designated owner as reviewer).
- **Definition of Done:** acceptance criteria met · tests written and passing · module README updated if interfaces changed · migration follows expand-contract · eval gate green if agent paths touched · no new dep without OSS-table entry · deployed to staging and smoke-checked.
- **Documentation rules:** architectural change → ADR file in the same PR; docs/product/ is read-only mirror (changes go through the DOC process, not code PRs).
- **Refactoring policy:** boy-scout within task scope; structural refactors are scheduled debt items (§3), never drive-by; deletion is celebrated.

## 2. Sprint Plan

**Assumptions:** 3 engineers + founder (part-time technical), 2-week sprints, ~18 sprints (~9 months) to V1 GA per DOC-120 roadmap. **ADR-006 (runway/headcount) is still open — this plan scales linearly with team size and re-dates on its answer.** Complexity: S/M/L. Risk: 🔥 = on critical path.

**Critical path:** vendor contract (external, DD gate 4) → E3 ingestion → E6 underwriting engine → golden datasets → accuracy gates → GA. Second external path: 10DLC/provider approvals (start Sprint 7, weeks of carrier lead time). Everything else parallelizes.

| Epic | Scope (DOC-121 refs) | Sprints | Cx | Risk |
|---|---|---|---|---|
| E1 Foundation | Repo per DOC-130 §2, CI/CD, Terraform staging+prod, WorkOS auth, identity module (A1), Claude Code environment (§1) | S1–S2 | M | 🔥 |
| E2 Ontology core | Schemas licensed/core/derived, RLS + adversarial suite, ontology module + state machines (A5 partial), audit, outbox | S2–S4 | L | 🔥 |
| E3 Ingestion | Adapter framework, first vendor, coverage registry, expiry enforcement (A2) — **blocked on vendor term sheet** | S3–S6 | L | 🔥 |
| E4 Imports | Dialect parsers, quarantine, consent-unknown init, rollback (A3) | S4–S5 | M | |
| E5 Resolution | Splink pipeline, clusters, merge/split UX, labeled fixture set (A4) | S5–S7 | L | 🔥 (quality risk) |
| E6 Underwriting | Comps engine, adjustments, runs, workspace UI (A6, B6), receipts component kit, metro golden sets | S6–S10 | L | 🔥 |
| E7 Pipeline & workspaces | Today, pipeline board, lead/property/owner workspaces (B1–B5), search (A10), notifications (A11) | S5–S9 | M | |
| E8 Conversations | Inbox, SMS/email providers, opt-out processing, summaries (A7, B9); 10DLC onboarding started S7 | S7–S10 | M | 🔥 (carrier lead time) |
| E9 Campaigns | Authorization object, wizard, pre-flight, send service + suppression matrix tests, per-message audit (A9, B7) | S9–S12 | L | 🔥 (compliance) |
| E10 Agents | Platform (gateway, tools, evals, budgets) then Prioritization → Underwriting agent → Follow-up L1; injection eval cases | S8–S13 | L | 🔥 |
| E11 Deals & outcomes | Deal workspace, offer chains, closing checklist, outcome capture + extraction, error attribution (A8, B8); privacy/DSR saga (A13) | S10–S13 | M | |
| E12 Commercial | Billing/wallet (A14), reporting v1 (A12), admin console (A15), export controls | S12–S14 | M | |
| E13 Hardening & launch | Load tests, chaos on send path, SOC2 evidence automation, restore drill, design-partner onboarding tooling, accuracy gate review, GA metro 1 | S14–S18 | L | 🔥 |

**Milestones:** M1 (end S2) staging deployed, auth + tenancy + CI green. M2 (end S6) internal alpha: import → lead → manual underwrite loop on real metro data. M3 (end S10) design-partner beta: full loop with L1 agents, campaigns in preview (sends mocked). M4 (end S13) sends live for compliant orgs; outcome loop closing. M5 (end S18) GA metro 1, accuracy-gated (DD change 2).

**Sprint 1 (fully specified, Claude-Code-executable):**
1. Scaffold monorepo per DOC-130 §2 incl. CLAUDE.md, rules, skills, hooks. *AC: fresh clone → `scripts/dev-up.sh` → API health check + frontend render locally.*
2. CI pipeline (lint, typecheck, unit skeleton, import-linter with initial contracts). *AC: red PR on boundary violation demo.*
3. Terraform staging env (network, RDS, ECS api service, secrets). *AC: hello-world API deployed to staging via pipeline.*
4. WorkOS auth + identity module skeleton (org create, invite, roles data model + matrix file). *AC: two orgs, cross-org API access denied by tests.*
5. Alembic baseline with logical schemas + first ontology tables (organization, member, property stub) with RLS + adversarial test harness. *AC: RLS suite green and merge-blocking.*
6. docs/product mirror + module README template + ADR template seeded.
*Risk note: Sprint 1 contains zero product features by design; skipping foundation is how 3-person teams drown in month 4.*

**Parallel work guide:** Eng A (backend/data): E2→E3→E6. Eng B (product surface): E1 frontend→E7→E8 UI→E9 wizard. Eng C (platform/AI): E1 infra→E2 outbox/audit→E10→E13. Founder: vendor + 10DLC external paths, design-partner pipeline, acceptance reviews.

## 3. Technical Debt Register (intentional, pre-declared)

| ID | Compromise | Why acceptable now | Repayment trigger | Plan |
|---|---|---|---|---|
| D1 | Shared staging instead of ephemeral backend previews | Cost/complexity at team size | >5 engineers or preview collisions weekly | Ephemeral envs via Terraform workspace per PR |
| D2 | Frontend-only PR previews (Vercel) against shared API | Same | Same as D1 | Bundle with D1 |
| D3 | No table partitioning | Volumes far below threshold | message/events/audit >50M rows | Monthly partitions; models already compatible |
| D4 | Temporal Cloud + Meilisearch Cloud + Grafana Cloud spend | Ops headcount = 0 | Infra bill >8% of revenue or scale economics flip | Self-host evaluation, one at a time |
| D5 | Single active region | RTO 8h acceptable v1 | Enterprise-tier requirement or SLA sales blocker | Warm standby region |
| D6 | No native mobile; phone = responsive read views | D4D deliberately not v1 (DOC-121 A18) | Design-partner field-usage demand | React Native evaluation V2 |
| D7 | Rehab = structured inputs + ranges, no model | ADR-004 c.4 | Permit-data enrichment live (V2) | Estimator v1 per DOC-120 roadmap |
| D8 | Conversation summaries batch, not realtime | Cost + simplicity | Inbox latency complaints | Streaming summarization |
| D9 | Python SDK deferred; TS only | No Python integrators yet | First customer request | Generate from OpenAPI (cheap) |
| D10 | RLS via GUC + wrapper (pooling-sensitive) | Standard pattern, tested | Pooling architecture change | Re-run adversarial suite on any pooler change (hook-enforced checklist) |
| D11 | Reporting = 4 fixed dashboards, no custom builder | Scope discipline | Mid-market tier (V3) | Warehouse + semantic layer decision then |
| D12 | LangGraph-class framework deliberately skipped | 3 agents, typed tools | Agent #4 or multi-step planning need | Re-evaluate; prompts/tools kept framework-agnostic |

## 4. Engineering Risk Register

| # | Risk | Sev | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|---|
| ER1 | Vendor contract slips → E3/E6 critical path stalls | **Critical** | M | GA date slides 1:1 | Founder starts negotiation Sprint 1; adapter framework built vendor-agnostic against fixture data meanwhile; second vendor in parallel talks | Founder/CTO |
| ER2 | Cross-tenant leak via RLS/pooling misconfig | **Critical** | L-M | Company-ending trust event | Merge-blocking adversarial suite; SET LOCAL wrapper; pooler-change checklist (D10); pen test pre-GA | Staff Security |
| ER3 | Suppression/consent bug in send path | **Critical** | M | TCPA exposure (DOC-110 R3) | Exhaustive compliance matrix tests; suppression enforced below agents; SEV-1 drill; canary sends; per-message audit reconciliation job | Backend lead |
| ER4 | Golden datasets too small/dirty to gate accuracy honestly | **Critical** | M | Can't prove the core claim; DD change 2 unmeetable | Dataset build is an E3/E6 deliverable with size targets per metro; design-partner historicals contractually secured; label provenance recorded | AI Eng |
| ER5 | Entity resolution over-merges owners | High | M | Wrong outreach + trust damage | Conservative thresholds; human-arbitrated merges only; reversibility; precision-weighted eval | AI Eng |
| ER6 | 10DLC/carrier approval delays block E8/E9 | High | M-H | Beta sends slip | Start S7 (weeks early); provider with strong 10DLC tooling; email channel decoupled | Founder |
| ER7 | AI cost per run exceeds budget at design-partner volumes | High | M | Margin math (DOC-110 R9) | Gateway budgets + caching; routing to cheaper models for extraction; weekly COGS review | Platform Eng |
| ER8 | Bus factor: comps/calibration model knowledge in one head | High | M | Velocity + correctness risk | Model documented as docs/modules/underwriting-model.md; eval suite is the executable spec; pairing rotation | VP Eng |
| ER9 | Temporal learning curve slows E9 workflows | Medium | M | 1–2 sprint drag | Workflow patterns skill + one spike sprint task in S8; workflows isolated for replaceability | Backend lead |
| ER10 | Meilisearch/index drift causes trust-eroding search bugs | Medium | M | Support load | Checksum reconcile + rebuild runbook (DOC-130 §3) | Backend |
| ER11 | libpostal build pain across dev machines/CI | Medium | M-H | Dev friction | Prebuilt container layer; usaddress fallback flag | Platform Eng |
| ER12 | Claude-Code-generated code drift from module boundaries | Medium | M | Architecture erosion | import-linter (deterministic), reviewer subagent + human review, rules files | CTO |
| ER13 | Scope creep from design partners during beta | Medium | H | GA slip | Change control: requests → PM triage vs DOC-121 priorities; "not-build" list is law | Founder/PM |
| ER14 | Grafana/Sentry alert fatigue hides real SEVs | Low | M | Slow incident response | Page-vs-digest policy (DOC-130 §7); alert review monthly | VP Eng |
| ER15 | OpenAPI/SDK drift breaks frontend silently | Low | L | Dev friction | Drift check in CI; contracts validation in dev builds | Frontend lead |

*Changelog: v1.0 — initial execution plan; Sprint 1 executable; re-dates on ADR-006.*
