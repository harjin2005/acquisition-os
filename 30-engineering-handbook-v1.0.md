# DOC-130 — Engineering Handbook & Build Blueprint

**Version:** 1.0
**Status:** Build-ready pending ADR-010 formal acceptance (all content assumes it; if amended, §1–7 revise)
**Inputs treated as immutable:** ADR-001..005, DOC-002 (ontology), DOC-110 gates, DOC-120 (blueprint), DOC-121 (PRD/UX v0.9)
**Team assumption:** 1–5 engineers + founder using Claude Code extensively. Boring-technology bias throughout. Companion: DOC-131 (Claude Code Playbook, Sprint Plan, Debt & Risk Registers).

---

## 1. Repository Strategy

**Decision: single monorepo** (`acquisition-os`). Rationale: 1–5 engineers, atomic cross-stack changes (schema → API → SDK → UI in one PR), one CI, one CLAUDE.md context universe. Multi-repo rejected (coordination tax, no org boundary to mirror). Alternatives recorded in docs/adr/ADR-010.

- **Versioning:** the app is continuously deployed — no app semver. Versioned artifacts: DB migrations (linear, numbered), OpenAPI spec (`/v1`, additive-only within v1; breaking = `/v2`), agent releases (per-agent semver, §6), generated TS SDK (semver tracking OpenAPI).
- **Shared code:** backend shares within `backend/app`; frontend consumes only the generated SDK + `packages/contracts` (zod schemas generated from OpenAPI) — **no hand-shared types**, the spec is the contract.
- **Branching:** trunk-based; short-lived branches (<2 days); PR-only to `main`; `main` is always deployable.

## 2. Folder Structure

```
acquisition-os/
├── CLAUDE.md                      # lean project memory (see DOC-131 §1)
├── .claude/
│   ├── rules/                     # path-scoped rules (backend.md, frontend.md, migrations.md, agents.md)
│   ├── skills/                    # repeatable playbooks (new-module, new-migration, new-agent-eval, vendor-adapter)
│   ├── agents/                    # reviewer + research subagents (code-reviewer.md, schema-auditor.md)
│   └── settings.json              # permissions allowlist, hooks (lint/test gates)
├── docs/
│   ├── adr/                       # mirrors DOC-001 entries as ADR-###.md
│   ├── modules/                   # per-module README (purpose, interfaces, invariants)
│   ├── runbooks/                  # oncall: send-path incident, vendor-feed gap, restore drill
│   └── product/                   # DOC-000..121 copies (source of truth for Claude context)
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI factory, middleware stack
│   │   ├── api/v1/                # routers only — thin, no business logic
│   │   ├── core/                  # config, auth deps, RBAC decorators, tenancy (org_id GUC), errors
│   │   ├── modules/               # §3 modules; each: router.py service.py models.py schemas.py events.py jobs.py tests/
│   │   │   ├── identity/  ontology/  ingestion/  imports/  resolution/
│   │   │   ├── underwriting/  conversations/  campaigns/  outcomes/
│   │   │   └── search/  notifications/  reporting/  billing/  privacy/  admin/
│   │   ├── agents/
│   │   │   ├── platform/          # gateway (LiteLLM), tool registry, memory, run logger, budgets
│   │   │   ├── prioritization/  underwriting_agent/  followup/
│   │   │   │   └── prompts/       # versioned prompt files + CHANGELOG.md per agent
│   │   │   └── evals/             # golden set refs, runners, thresholds.yaml
│   │   ├── events/                # outbox model, dispatcher, consumers/
│   │   ├── workflows/             # Temporal: campaigns, ingestion, closing checklists, dsr
│   │   └── db/
│   │       ├── migrations/        # alembic, one head, expand-contract policy
│   │       └── schemas/           # licensed/ core/ derived/ SQLAlchemy models per logical schema
│   ├── tests/                     # integration/, rls/, api/ (module unit tests live in-module)
│   └── pyproject.toml             # uv-managed; ruff, mypy, pytest config
├── frontend/
│   ├── app/                       # Next.js App Router (§4 route map)
│   ├── components/{ui,receipts,domain}/
│   ├── lib/{api,hooks,stores}/
│   └── e2e/                       # Playwright
├── packages/
│   ├── sdk-ts/                    # generated from OpenAPI (CI job)
│   └── contracts/                 # generated zod schemas
├── infra/
│   ├── terraform/{modules,envs/{staging,prod}}/
│   └── docker/                    # Dockerfiles (api, worker, temporal-worker)
├── scripts/                       # dev-up.sh, seed.py, restore-drill.sh, eval-run.sh
└── .github/workflows/             # ci.yml, deploy.yml, eval-gate.yml, sdk-publish.yml
```

## 3. Backend Blueprint

**Global rules (enforced, not aspirational):** routers are thin; business logic lives in services; modules communicate via (a) explicit service interfaces or (b) domain events — never by importing another module's models; **import-linter contracts in CI enforce the boundary graph**; every write path emits its domain event via the transactional outbox; every table carries org_id and every session sets the tenancy GUC (§5); DOC-002 names are law in code.

Boundary graph (dependencies point downward): `api → modules → {ontology} → db`; `agents/* → tool registry only`; `campaigns.send_service` is the **only** code that touches messaging providers; `campaigns.suppression` is the only writer of suppression state.

| Module | Purpose / responsibilities | Public interface | Events emitted | Jobs/workflows | Top failure modes → handling | Test focus |
|---|---|---|---|---|---|---|
| identity | Auth (managed provider), orgs, members, RBAC bindings, seats | `require_permission()`, org resolver | member.invited/role_changed | seat reconciliation | provider outage → cached JWKS, read-only grace | RBAC matrix table-driven tests |
| ontology | CRUD + state machines for property/owner/contact/lead/deal/offer per DOC-002 | typed services per entity; `transition_lead()` | lead.*, deal.stage_changed, offer.* | staleness SLA scanner | illegal transition → 409 with machine-readable reason | state-machine property tests |
| ingestion | Vendor adapters, coverage registry, refresh, licensed-layer writes + expiry | `get_property()`, `get_comps_candidates()`, coverage API | property.updated, coverage.changed | Temporal: nightly refresh, expiry sweeps, anomaly checks | feed gap → staleness cascades to receipts; schema drift → adapter contract tests + quarantine | adapter contract tests vs fixture snapshots |
| imports | CSV dialect parsers (PropStream/BatchLeads/DataSift/DealMachine/Podio), quarantine, consent-unknown init, 24h rollback | `start_import()`, `rollback_import()` | import.completed | async import pipeline | malformed rows → per-row quarantine report; re-import → content-hash idempotent | golden import files per dialect |
| resolution | Splink pipelines, clusters, human merge/split with audit, aliases | `resolve_owner()`, `suggest_merges()` | owner.merged/split | batch resolution on ingest/import | over-merge (worst case) → conservative thresholds, human-arbitrated merges, reversible splits | precision/recall on labeled fixture set (own golden dataset) |
| underwriting | Comps selection + adjustment engine, assumption sheets, immutable runs, calibration store | `create_run()`, `get_run_diff()` | underwriting.completed | calibration refresh from outcomes | <3 comps → typed InsufficientEvidence (never a value); override beyond bounds → review flag | golden comp sets per metro; calibration backtests |
| conversations | Unified threads, provider inbound webhooks, summaries, opt-out keyword processing, escalation flags | `log_message()`, `get_thread()` | message.received/sent, conversation.escalated | summary queue | unknown inbound → unmatched pool + suggestions; webhook replay → idempotent by provider msg id | opt-out corpus tests (STOP variants + free-form) |
| campaigns | Authorization objects, pre-flight, **send service** (consent/DNC/litigator/quiet-hours/caps enforced server-side), 10DLC state, per-message audit | `approve_campaign()`, `preflight()`, `send()` (trust-gated) | campaign.approved/completed, message.sent, consent.revoked | Temporal: campaign execution, cadence timers | provider failure mid-batch → per-message status, resumable, idempotency keys prevent double-send; **any suppression bypass = P0 incident** | most-tested module: exhaustive suppression matrix, load + chaos tests |
| outcomes | Deal economics, settlement extraction review, error attribution, calibration inputs, consented research marts | `close_deal()`, `record_actuals()` | outcome.captured | extraction queue; mart refresh | low-confidence extraction → human review diff, never silent accept | extraction golden PDFs; attribution math units |
| search | Meilisearch sync (outbox consumer), smart lists, suppression-aware flags | `search()`, `save_list()` | — | index rebuild | drift → nightly checksum reconcile + rebuild runbook | consumer idempotency |
| notifications | Preference matrix, digests, storm compression, mandatory compliance classes | `notify()` | — | digest scheduler | dupes → suppression by event key | preference matrix table tests |
| reporting | Four v1 dashboards, small-n confidence rendering, exports | `dashboard()` | — | nightly aggregates | small-n → intervals not points | metric definition snapshot tests |
| billing | Stripe sync, plans/seats, usage wallet, dunning, plan-pause | `check_entitlement()`, `debit_wallet()` | wallet.low/exhausted | webhook consumer, metering | wallet empty mid-campaign → pause + notify, never silent partial | Stripe fixture webhooks; entitlement matrix |
| privacy | DSR intake/verify, deletion across licensed cache/core/derived incl. embeddings + edges, legal hold, SLA | `open_dsr()` | dsr.completed | Temporal deletion saga | partial failure → saga retries + completeness verifier | seed→delete→scan-all-schemas completeness test |
| admin | Tenant lookup, coverage mgmt, feed health, impersonation (banner + audit) | — | — | — | impersonation w/o audit = impossible by construction | authz tests |

## 4. Frontend Blueprint

- **App:** one Next.js (App Router) application, desktop-first (DOC-121 design language); responsive to tablet; phone = read/notify views only in v1 (debt D6).
- **Route map (mirrors DOC-121 Part B):** `/today` `/pipeline` `/inbox` `/properties/[id]` `/owners/[id]` `/leads/[id]` `/deals/[id]` `/underwriting/[runId]` `/campaigns` `/campaigns/new` (5-step wizard) `/campaigns/[id]` `/reports/[dashboard]` `/settings/*` `/admin/*` (internal flag).
- **State:** TanStack Query for all server state (keys namespaced by org); one small Zustand slice for UI state (panels, wizard progress). No Redux. Server components for read-heavy pages; client components at interaction leaves.
- **Data layer:** generated TS SDK only — no hand-written fetches; zod contract validation in dev; optimistic updates only for low-risk mutations (notes, tasks) — never for state transitions or sends.
- **Forms:** react-hook-form + zod (from `packages/contracts`); campaign wizard = plain reducer state machine (XState rejected — simplification rule).
- **Tables:** TanStack Table, virtualized (pipeline hits 10k+ rows); saved views serialize to smart lists.
- **Maps:** MapLibre GL + vector tiles (MapTiler vs Protomaps cost decision Sprint 3). Google Maps rejected (cost/licensing).
- **Charts:** Recharts (funnel, gauges, sensitivity tornado, value-band bars). No chart abstraction layer.
- **Design system:** Tailwind + Radix primitives. `components/ui` = base kit; `components/receipts` = **Receipts drawer, confidence band, freshness stamp, evidence list — built once (Sprint 4), reused by all three agents** per DOC-121 mandate; `components/domain` = lead card, comp card, consent chip, stack badges. Storybook for receipts + domain kits only.
- **Accessibility:** WCAG 2.1 AA; keyboard-first pipeline/inbox (VA power users); axe checks in Playwright.
- **States:** every route ships designed empty/loading/error via shared `<QueryBoundary>`; compliance blocks use the why + fix-path pattern.

## 5. Database Implementation Guide

- **Migrations:** Alembic, single linear head, **expand → backfill → contract** for live tables; every migration PR carries a rollback note; weekly CI job runs pending migrations against a snapshot-restored copy (drift + duration check). Naming per DOC-002 §9 with a CI grep against the glossary allowlist.
- **Tenancy/RLS:** every tenant table `org_id uuid not null`; policies `USING (org_id = current_setting('app.org_id')::uuid)`; app sets the GUC per transaction. **Pooling caveat (critical):** with transaction-mode pooling (RDS Proxy/pgbouncer), the GUC must be `SET LOCAL` inside each transaction — a session wrapper refuses queries without tenancy context; CI runs adversarial cross-tenant read attempts. Ingestion/admin use a distinct service role with RLS bypass, importable only inside those modules (import-linter enforced).
- **Constraints/invariants:** FKs everywhere; CHECKs on state enums; `underwriting_run` + approved `campaign` immutable via revoked UPDATE + audit trigger; `contact_channel` unique per (org, channel, value) with suppression columns indexed; graph edges (valid_from, valid_to) with exclusion constraint on overlapping identical edges.
- **Indexes:** per DOC-120 §6; review rule: every new query path names its index or justifies a seq scan (.claude/rules/backend.md).
- **Partitioning:** none at launch; pre-declared plan (debt D3): `message`, `events.domain_event`, `audit.log` partition monthly past ~50M rows; models avoid cross-partition FKs now to keep the path open.
- **Caching:** ElastiCache (Valkey engine — avoids Redis licensing) for hot property/comp candidates, TTL ≤ licensed `expires_at` (mechanical R4 compliance, tested); dashboard caches invalidated by outbox events.
- **Backups/lifecycle:** RDS PITR (RPO ≤1h) + daily cross-region snapshots; S3 versioning + replication; quarterly `restore-drill.sh` into isolated VPC with signed checklist; nightly licensed-expiry sweep; audit/consent retention ≥7yr; embeddings derived → rebuildable, outside tight RPO.
- **Performance posture:** p95 targets — entity page <300ms, pipeline query <500ms @50k leads, comps candidate fetch <2s; pg_stat_statements on day one; perf budget is a CI-visible dashboard, not a vibe.

## 6. AI Implementation Guide

- **Gateway:** LiteLLM (self-hosted proxy) as the single egress to model providers — routing config per task class, per-org and per-run **budget middleware** (hard stop + alert), response caching keyed on (input hash, model, prompt_version). No module calls a provider SDK directly (import-linter rule).
- **Prompt architecture:** prompts are files in `agents/<name>/prompts/` with frontmatter (version, model targets, changelog entry required by CI); system prompts are static templates with **typed variable injection only** — user/inbound free text is always presented inside clearly delimited data blocks, never concatenated into instructions (injection posture, with eval-suite attack cases). A prompt change = a PR = an agent version bump = eval gate.
- **Tool architecture:** pydantic-typed tools registered in `agents/platform/tools.py`; registry mounts tools per (agent, trust level, org) at runtime — Level-1 agents physically receive no send-capable tools (DOC-120 §8 threat model); every tool call re-validates RBAC + tenancy server-side and is trace-logged with arguments (PII-redacted in traces).
- **Memory:** org memory = structured tables (buy box, assumptions, override stats) read via tools; entity memory = the graph + conversation summaries; run memory = ephemeral. No vector "agent memory" store in v1 (simplification; the graph is the memory — DOC-120 §5.0).
- **Evaluation pipeline:** golden datasets versioned in S3 with manifest files in-repo (`evals/manifests/*.yaml`: dataset hash, metro, size, label provenance); `eval-run.sh` executes per-agent suites (pytest-based) producing scored reports to Langfuse; **CI gate `eval-gate.yml`: an agent-version PR merges only if thresholds in `thresholds.yaml` pass and no metric regresses >X%**; online metrics (acted-upon, override, opt-out guardrails) dashboarded per agent per org.
- **Logging/observability:** every run logged: run_id, org, agent_version, prompt_version, model, token/cost, latency, tool-call tree, output hash → Langfuse trace + OTel span; sampling 100% in v1 (volume is small; revisit at scale).
- **Versioning/rollback:** agent_version is a per-org feature flag; rollback = flag flip (seconds), no deploy; prompts+code+thresholds move together in one PR so a version is reproducible.
- **Cost control:** budgets above + weekly per-org COGS report (DOC-120 §9) combining gateway spend + data enrichment spend; underwriting run p95 cost target set Sprint 6 and enforced by budget middleware.
- **Safety:** injection attack cases in every agent's eval suite (adversarial inbound messages attempting to trigger sends/exfiltration must produce refusals + escalation flags); suppression enforcement lives below the agent (send service), tested independently; kill switch per agent per org (flag) documented in runbooks.

## 7. Infrastructure Blueprint

- **Accounts/regions:** AWS Organizations — separate prod and staging accounts; single primary region + cross-region backup copies (DR posture per DOC-120 §8; multi-region active = debt D5, not v1).
- **Compute:** ECS Fargate services — `api`, `worker` (queue consumers), `temporal-worker`; Kubernetes rejected at this team size (ops burden, ADR-010).
- **Managed choices (boring-by-default):** RDS Postgres 16 (Multi-AZ prod) + RDS Proxy; ElastiCache (Valkey); **Temporal Cloud** (running Temporal ourselves is real ops load; cost accepted, revisit at scale — debt D4); **Meilisearch Cloud** (same logic); S3; SES + Twilio-class SMS provider; WorkOS for auth; Stripe.
- **Terraform:** modules (network, ecs-service, rds, cache, queues, observability) instantiated per env; state in S3 + lock table; no console changes in prod (drift detection weekly).
- **Docker:** multi-stage builds (uv for deps), distroless-ish runtime images, one image per service role, SBOM generated in CI.
- **CI/CD (GitHub Actions):** `ci.yml` — lint (ruff, eslint), typecheck (mypy, tsc), unit+integration (testcontainers Postgres), RLS adversarial suite, import-linter, OpenAPI drift check, migration dry-run; `eval-gate.yml` on agent paths; `deploy.yml` — build/push ECR, staging deploy on merge, prod deploy on manual approval, blue/green via ECS deployment circuit breaker + automatic rollback; GitHub OIDC → AWS (no long-lived keys).
- **Preview:** Vercel preview per PR for frontend against shared staging API (full ephemeral backends = debt D2); seeded demo org in staging refreshed nightly.
- **Monitoring/logging:** OTel SDK → Grafana Cloud (metrics/traces/logs; Datadog rejected on cost at this stage — revisit); Sentry (frontend+backend errors); alert policy: page on send-path errors, suppression-verifier failures, feed-gap anomalies, budget breaches; everything else → Slack digest.
- **Secrets:** AWS Secrets Manager + SSM; injected at task definition; rotation runbook; pre-commit + CI secret scanning (gitleaks).
- **Scaling:** Fargate target-tracking on CPU/queue depth; RDS vertical headroom plan; send-path rate limiting is compliance-driven, not capacity-driven (never "scale up" past carrier caps).
- **DR:** per DOC-120 §8 — RPO ≤1h / RTO ≤8h, quarterly restore drill, runbooks in docs/runbooks/.

## 8. Testing Handbook

| Tier | Tooling | Scope & gates |
|---|---|---|
| Unit | pytest + factory_boy; vitest | Module logic, state machines, adjustment math; fast (<3 min CI) |
| Integration | pytest + testcontainers Postgres/Valkey | Service+DB per module; outbox/consumer idempotency; Temporal workflows via test server |
| RLS/security | dedicated `tests/rls` suite | Adversarial cross-tenant reads/writes per table; service-role boundary tests; **merge-blocking** |
| API contract | schemathesis against OpenAPI | Fuzz + contract conformance; SDK generation must succeed |
| E2E | Playwright | Happy paths only: onboarding checklist, import→lead→underwrite→campaign preflight→(mock) send→close loop; axe accessibility checks |
| Compliance matrix | pytest parametrized | The suppression truth table: {consent state × DNC × litigator × quiet hours × caps × opt-out timing} × channels — exhaustive, merge-blocking, owned by campaigns module |
| AI evals | eval runner + Langfuse | Golden sets per agent per metro; regression thresholds; injection attack cases; merge-blocking on agent paths |
| Load | k6 | Send pipeline (10k-message campaign), pipeline queries @50k leads, ingestion burst; pre-GA gate |
| Perf regression | pg_stat_statements diff job | Weekly report vs budget |
| Security scanning | gitleaks, pip-audit, npm audit, bandit, Dependabot | CI + weekly |

Coverage guidance: campaigns/underwriting/privacy ≥90% line+branch; overall ≥75%; coverage is a review signal, not a fetish. Golden datasets: comps holdouts per launch metro (built during E3 with vendor data + recorder-verified sales), resolution labeled pairs, opt-out language corpus, settlement-statement PDFs, prioritization historical-outcome set (seeded from design partners' migrated history — a design-partner data-sharing deliverable).

## 9. Security Implementation Guide (blueprint → tasks)

1. **AuthN:** WorkOS integration (SSO-ready but disabled), JWT verification middleware, MFA enforcement flag per org, device/session listing UI. (E1)
2. **AuthZ:** permission matrix as data (`core/rbac/matrix.py`) + `require_permission` dependency + decorator tests generated from the matrix; privileged actions (campaign approval, trust promotion, merge) additionally require role ≥ Manager and dual-log. (E1, extended per module)
3. **Tenancy:** GUC wrapper + RLS policies + CI adversarial suite (§5). (E2, merge-blocking)
4. **Audit:** append-only audit schema + middleware capturing actor/agent provenance + admin viewer + 7yr retention policy job. (E2)
5. **Encryption:** KMS CMKs for RDS/S3; TLS termination at ALB with strict policies; application-layer encryption for contact channel values with blind-index columns for suppression lookups (design doc task, E8). 
6. **Secrets:** SM/SSM wiring, OIDC deploy roles, gitleaks, rotation runbook. (E1)
7. **Threat mitigations:** tool-mounting enforcement + injection eval cases (E10); export endpoints permissioned + volume anomaly alarm (E12); vendor keys scoped + egress allow-list security groups (E3); impersonation banner+audit (E12).
8. **Compliance controls-as-code:** branch protection + PR-only deploys (change mgmt), quarterly access-review script against WorkOS/AWS, vendor register doc, incident response runbook + severity ladder (suppression bypass = SEV-1), evidence folder automation for SOC 2 Type I (month 12 target). (E13)
9. **Privacy engineering:** DSR deletion saga + completeness verifier + legal-hold flag (E11); FCRA guardrail = lint rule banning eligibility/credit vocabulary in UI strings (cheap, real). 

## 10. Open Source Adoption Plan

| Project | Purpose | License | Maint. | Integration cost | Replacement risk | Verdict |
|---|---|---|---|---|---|---|
| FastAPI / Pydantic / SQLAlchemy / Alembic | API + data core | MIT | High | Low | Low (commodity) | Adopt |
| uv, ruff, mypy | Python toolchain | MIT/Apache | High | Low | Low | Adopt |
| Temporal (via Cloud) | Durable workflows | MIT SDK | High | Medium (concepts) | Medium — pre-declared exit: workflows isolated in `workflows/` | Adopt |
| LiteLLM | Model gateway/budgets | MIT | High | Low | Low (thin seam) | Adopt |
| Langfuse | AI traces/evals | MIT core | High | Low | Medium (export path exists) | Adopt (cloud) |
| Splink | Entity resolution | MIT | High (MoJ-backed) | Medium | Low alternatives — this is a bet; fixture-tested | Adopt |
| libpostal (+postal bindings) | Address normalization | MIT | Medium (C build pain) | Medium | usaddress fallback documented | Adopt w/ fallback |
| pgvector | Embeddings | PG license | High | Low | Low | Adopt |
| Meilisearch (Cloud) | App search | MIT | High | Low | Medium (Typesense alt) | Adopt |
| Valkey (ElastiCache) | Cache/queues | BSD | High | Low | Low | Adopt |
| Next.js/React/TanStack/Radix/Tailwind/Recharts/MapLibre | Frontend stack | MIT/BSD | High | Low | Low | Adopt |
| react-hook-form + zod | Forms/validation | MIT | High | Low | Low | Adopt |
| Playwright, schemathesis, testcontainers, factory_boy, k6 | Testing | Apache/MIT (k6 AGPL — dev-tool only, not embedded) | High | Low | Low | Adopt |
| import-linter | Boundary enforcement | BSD | Medium | Low | Low | Adopt |
| gitleaks, bandit, pip-audit | Security scanning | MIT/Apache | High | Low | Low | Adopt |
| **Rejected for v1:** Neo4j (graph-as-tables first, DOC-110 §8), Kubernetes, Airflow (Temporal covers), LangGraph (three agents with typed tools don't need a graph framework yet — re-evaluate at agent #4; keep prompts/tools framework-agnostic), Kafka (outbox+SQS-class queues suffice), self-hosted Keycloak. Each rejection recorded with re-entry criteria in docs/adr/. |

License policy: MIT/BSD/Apache only in shipped code; AGPL permitted for dev tools never linked into the product; new dependencies require an entry in this table via PR (rule in .claude/rules).

*Continues in DOC-131: Claude Code Development Playbook, Sprint Plan, Technical Debt Register, Engineering Risk Register.*
