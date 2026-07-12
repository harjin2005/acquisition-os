# AcquisitionOS — PRD (Living)

**Owner:** Founder / CTO  ·  **Sprint:** 1 (Foundation)  ·  **Version:** 0.1.0  ·  **As of:** 2026-01-15

Canonical PRD lives in `/app/docs/product/21-prd-ux-blueprint-v0.9.md` (mirror of DOC-121). This file is the *implementation-facing* companion: it tracks what has been built, what's next, and the running backlog. Never contradicts DOC-121 — extend it.

---

## Original problem statement (verbatim)

> Build a production-grade SaaS company (AcquisitionOS) faithfully following the documentation in the repo. Implement one sprint at a time. Do not redesign the product, ontology, architecture, or workflows. Sprint 1 is fully specified in DOC-131 §2. Stop after Sprint 1 for review.

## User's Sprint 1 direction (verbatim)

- 1a — PostgreSQL as canonical. Install locally in dev. Only fall back to 1c if impossible.
- 2a — Scaffold Terraform + CI/CD + GitHub Actions + AWS as code artifacts.
- 3a — WorkOS integration exactly as documented with placeholders/mocks.
- 4a — Sprint 1 exactly as documented. No invented UI or product functionality.
- 5a — AcquisitionOS Sprint 1 only. No Jarvis implementation.
- Do not deviate from ADRs without creating a new ADR.
- Keep the repository production-first, even if the preview has limitations.
- Build only Sprint 1 and stop for review.

## Company context (see MASTER_CONTEXT.md)

- **Mission:** decision-quality Acquisition Operating System for 2–10-person US real-estate investment teams (flip + buy-and-hold).
- **Stage:** pre-build, documentation phases 0–4 complete. 0 customers, $0 revenue.
- **Wedge ICP:** disclosure-state metros, small teams doing flips + buy-and-hold.
- **Critical path:** vendor data contract → ingestion → underwriting golden datasets → accuracy-gated GA (metro 1 by ~Sprint 18).

## Architecture summary (see DOC-130 + Architecture.md)

- **Backend:** FastAPI + SQLAlchemy 2.0 + Alembic; Postgres 16 (dev: 15 per ADR-EMERGENT-001) with logical schemas `licensed`, `core`, `derived`, `audit`, `events`; row-level security via `SET LOCAL app.org_id` inside every transaction; Temporal Cloud (E9+); LiteLLM gateway (E10).
- **Frontend:** React + TanStack Query. Product routes land in E7+.
- **Auth:** WorkOS (mock in dev per ADR-EMERGENT-001).
- **Infra:** AWS ECS Fargate + RDS + ElastiCache + S3, provisioned via Terraform. GitHub Actions for CI/CD with OIDC.

## Sprint 1 — Done (as of 2026-01-15)

- [x] AC1 — `scripts/dev-up.sh` boots api + frontend locally.
- [x] AC2 — CI (`.github/workflows/ci.yml`) runs lint + typecheck + unit + `import-linter` (4 contracts, all green; boundary-violation demo covered in `tests/integration/test_import_linter.py`).
- [x] AC3 — Terraform staging env scaffolded (`infra/terraform/envs/staging/` + reusable modules: network, rds, cache, ecs-service, secrets, observability). Not applied — apply is a `deploy.yml` step gated on AWS credentials.
- [x] AC4 — WorkOS auth + identity module skeleton. Two-org cross-org denial verified in `tests/rls/test_cross_tenant_isolation.py` (9 adversarial cases) + `tests/api/test_identity_api.py::test_cross_org_api_is_denied`.
- [x] AC5 — Alembic baseline (`0001_baseline.py`) creates schemas + `core.organization/member/invite` + `licensed.property` with RLS `USING`/`WITH CHECK`. 9 RLS tests + 35 RBAC-matrix tests are **merge-blocking**.
- [x] AC6 — `docs/product/` mirror + `docs/modules/` (identity, ontology) + `docs/adr/_template.md` + `docs/adr/ADR-EMERGENT-001-runtime-adaptation.md` + runbooks (send-path incident, restore drill, feed-gap).

**Live preview endpoints:**
- `GET /api/health` — health probe.
- `GET /api/meta/sprint` — machine-readable AC status.
- `POST /api/v1/identity/orgs` — bootstrap org + founder-owner (dev path; WorkOS webhook replaces this in Sprint 2).
- `GET /api/v1/identity/orgs/me` · `.../members` · `POST .../invites` · `POST /api/v1/identity/invites/accept`.
- `POST /api/v1/ontology/properties` · `GET .../properties` (stub for RLS validation).

**Test posture (Sprint 1 exit):** 52 in-process tests + 12 live-URL e2e tests = 64/64 green.

## Backlog (P0/P1/P2, grows over time)

### Sprint 2 (P0) — DOC-131 E1 tail + E2 kickoff

- Outbox model + dispatcher + audit schema (E2).
- Ontology full surface: property, owner, contact, lead, deal, offer + state machines.
- MFA enforcement flag per org.
- Device/session listing UI.
- mypy hard-gate (advisory in Sprint 1 CI).
- Vendor negotiation kickoff (external, founder-owned).

### Sprint 3–6 (P0) — E3 ingestion + E4 imports + E5 resolution + E6 underwriting start

- Vendor adapter framework + first vendor (blocked on ADR-006 + vendor term sheet).
- CSV dialect parsers (PropStream/BatchLeads/DataSift/DealMachine/Podio).
- Splink pipeline for entity resolution.
- Comps engine + underwriting run/workspace.

### Sprint 7–13 (P0) — Conversations, campaigns, agents, deals

- 10DLC onboarding (start S7 for carrier lead time).
- Send service + suppression matrix + compliance PR reviewer discipline.
- Prioritization → Underwriting → Follow-up agents (L1 → L2 gradual).

### Sprint 14–18 (P0) — Hardening + GA

- Load tests, chaos on send path, SOC 2 evidence automation, restore drill, GA metro 1.

### Deferred (D-series debt, DOC-131 §3)

- Native mobile (D6), rehab model (D7), streaming summaries (D8), Python SDK (D9), custom reporting builder (D11), LangGraph (D12).

## Personas (from DOC-121 §A.1)

- **Owner-founder:** 2–5 person REI shop, does flips + rentals.
- **Acquisitions manager:** runs pipeline day-to-day.
- **VA:** power-user of inbox/pipeline (keyboard-first).
- **Analyst:** underwrites deals.

## Prioritized user problems (from DOC-121 §A.2)

1. "Which lead should I call first?" — Prioritization agent (L1).
2. "Is this a deal, and at what price?" — Underwriting agent (L1) + comps engine.
3. "Where did I leave this thread?" — Conversations + summaries (E8).
4. "Did we do what we promised?" — Outcomes + attribution (E11).

## Success metrics (DOC-120 §12, targets — no actuals yet)

- NSM: Underwritten Deals Closed/org/mo ≥ 1.0 by M5.
- Median ARV error beats baseline AVM ≥ 15% relative.
- Acted-upon ≥ 40%.
- Suppression violations = 0.
- GM ≥ 75% (kill floor 60%), churn ≤ 3%/mo.

## Change log

- **2026-01-15 · v0.1.0 — Sprint 1 shipped.** Foundation, RLS, WorkOS skeleton, Terraform + CI scaffolds, boundary-enforcing import-linter. One HIGH bug caught by testing agent and fixed: bootstrap slug idempotency (RCA: RLS-blinded pre-check → moved to service_role_session + IntegrityError safety-net handler). ADR-EMERGENT-001 filed to document dev-only runtime adaptations (Postgres 15, WORKOS_MOCK_MODE, MongoDB coexistence).
