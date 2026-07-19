# PROGRESS.md — Granular checklist: what's actually built vs the full plan

**For YOU to scan any time and know exactly what's real.** Every box is checked only when its
acceptance criteria (per `docs/product/31-execution-plan-v1.0.md`, DOC-131) is met and was
actually shown working — not when someone says "basically done."

_Last updated: 2026-07-19_

**Totals: 26 of ~95 tracked items checked. Sprint 1 of 18 closed, Sprint 2 (E2) underway.
CI is genuinely green.**

**Correction (2026-07-19):** every E2 item below previously said "model exists, unwired" as
if the database table didn't exist yet. That was wrong — migration 0002 already created the
*entire* core ontology schema (Owner, Contact, Lead, Deal, Offer, Conversation, Message,
Campaign, Underwriting Run, Comp, Audit, Outbox), RLS included. The real gap was only ever
the router/service layer on top. Line items below now reflect that.

---

## E1 — Foundation (Sprint 1–2)

### Sprint 1 (closed 🟢)
- [x] `scripts/dev-up.sh` — Postgres + roles/schemas, backend+frontend deps, Alembic, boots API+frontend
- [x] CI: lint (ruff) + import-linter (4 boundary contracts) + unit skeleton
- [x] CI: Postgres 16 service container matches prod, not the dev workaround
- [x] Terraform staging scaffolded: network, RDS+Proxy, cache, ecs-service, secrets, observability modules
- [x] Terraform: prod env intentionally stubbed (by design, not a gap)
- [x] WorkOS JWKS/JWT verification path (real, not mocked) — currently unexercised, mock mode on
- [x] Identity module: Organization, Member, Invite models + state machine + dual-owner invariant
- [x] RBAC matrix as data (`app/core/rbac.py`) + `require_permission` dependency
- [x] Alembic baseline migration: schemas + tables + RLS `USING`/`WITH CHECK`
- [x] RLS adversarial suite (9 cases) — merge-blocking
- [x] docs/product mirror + module READMEs + ADR templates + runbooks

### Verified this session (2026-07-13) — proof it's not just claimed, it runs
- [x] Fresh `pip install` → `alembic upgrade head` → both migrations apply clean
- [x] `GET /api/health` returns 200 ok
- [x] `POST /api/v1/identity/orgs` creates a real org through RLS end-to-end
- [x] `yarn build` compiles the frontend clean
- [x] Fixed: `AuditEntry.metadata` reserved-name crash (blocked every fresh install)
- [x] Fixed: missing `email-validator` dependency (blocked every fresh install)
- [x] `frontend/yarn.lock` committed, `.gitignore` covers build artifacts

### CI made genuinely green (2026-07-15) — was red/unverified before this
- [x] Bootstrap-org slug-duplicate 500→409 bug — **turned out already fixed**, correcting an
  earlier wrong claim in this file; regression test exists and passes
- [x] Ruff lint clean (5 unused-import errors fixed) — this was CI's actual first failure point
- [x] Ruff format clean (31 of 88 backend files had never been formatted)
- [x] `.importlinter` allowlist fixed — was stale since the 0002 migration, contract was
  genuinely BROKEN (8 unlisted module imports), not just unverified
- [x] **Real cross-tenant RLS bypass in CI found and fixed** — `acquisition_os` was the
  Postgres bootstrap superuser (via `POSTGRES_USER`), which unconditionally bypasses RLS.
  The "merge-blocking" RLS suite was not actually verifying tenant isolation. Fixed with two
  genuine non-superuser roles; confirmed in real GitHub Actions (run 29408811712): 50 passed,
  1 skipped, 0 failed, all 9 RLS adversarial cases green
- [x] Gitleaks false positive triaged and allowlisted (verified real secret detection still works)
- [x] Full CI (`ci.yml`) green end-to-end: frontend + backend (14 steps) + security

### Sprint 2 — E1 tail (open)
- [x] Rate limiting on the public bootstrap-org endpoint — hand-rolled in-memory limiter
  (`app/core/rate_limit.py`), no new dependency (endpoint is Sprint-1-dev-only, gets replaced
  by a real WorkOS webhook next sprint — a Redis-backed library would be premature). 10
  req/hour/IP. Regression test asserts the 11th request gets 429. Confirmed in real CI.
- [ ] MFA enforcement flag per org
- [ ] Device/session listing UI
- [ ] mypy promoted from advisory (`|| true`) to hard-gate in CI
- [ ] Bootstrap-org: replace dev synthetic subject_id with real WorkOS provisioning webhook
- [ ] RBAC `dual_log=True` permissions (role change, member remove) actually enforced — currently metadata-only, no second-actor witness recorded

---

## E2 — Ontology core (Sprint 2–4)
- [x] **Owner: router + service (create/list/get), with RLS adversarial case + API tests.**
  Schema already existed (migration 0002); this wired the logic on top. Verified live
  end-to-end (real org → real owner → real list) and in real CI.
- [ ] Outbox: dispatcher process publishing `events.outbox` rows (schema exists, unwired)
- [ ] Audit: services actually writing to `audit.log` on privileged actions (schema exists, unwired)
- [ ] Contact + ContactChannel + ConsentRecord: router + service (schema exists, unwired)
- [ ] Lead: router + full state machine service (schema exists, unwired)
- [ ] Deal + Offer: router + service (schema exists, unwired)
- [ ] BuyBox: router + service (schema exists, unwired)
- [ ] MotivationSignal: router + service (schema exists, unwired)
- [ ] MetroCoverage: router + service (schema exists, unwired)

---

## E3 — Ingestion (Sprint 3–6) — **blocked on vendor term sheet**
- [ ] Vendor adapter framework (buildable now, against fixture data — not actually blocked)
- [ ] First vendor integration — **blocked: no signed contract**
- [ ] Coverage registry (which metros/vendors are live)
- [ ] Data expiry enforcement (`licensed.property.expires_at` already modeled, not enforced)

## E4 — Imports (Sprint 4–5)
- [ ] CSV dialect parser: PropStream
- [ ] CSV dialect parser: BatchLeads
- [ ] CSV dialect parser: DataSift
- [ ] CSV dialect parser: DealMachine
- [ ] CSV dialect parser: Podio
- [ ] Quarantine flow for malformed rows
- [ ] Consent-unknown default on all imported contacts (DD-5)
- [ ] Import rollback

## E5 — Resolution (Sprint 5–7)
- [ ] Splink entity-resolution pipeline
- [ ] Owner cluster merge/split UX
- [ ] Labeled fixture set for precision eval

## E6 — Underwriting (Sprint 6–10)
- [ ] Comps engine
- [ ] Adjustment logic
- [ ] Underwriting run + workspace UI
- [ ] Receipts component kit (show-your-work UI pattern)
- [ ] Metro golden datasets (accuracy-gate requirement)

## E7 — Pipeline & workspaces (Sprint 5–9)
- [ ] "Today" view
- [ ] Pipeline board
- [ ] Lead workspace
- [ ] Property workspace
- [ ] Owner workspace
- [ ] Search (Meilisearch)
- [ ] Notifications

## E8 — Conversations (Sprint 7–10)
- [ ] Inbox UI
- [ ] SMS provider integration
- [ ] Email provider integration
- [ ] Opt-out processing
- [ ] Conversation summaries
- [ ] 10DLC carrier onboarding — **start early, has weeks of lead time once triggered**

## E9 — Campaigns (Sprint 9–12) — compliance-critical, founder review required
- [ ] Campaign authorization object
- [ ] Campaign wizard
- [ ] Pre-flight compliance check
- [ ] Send service (the only messaging egress, per import-linter contract)
- [ ] Suppression matrix + tests
- [ ] Per-message audit trail

## E10 — AI Agents (Sprint 8–13) — **0 lines of code exist**
- [ ] Agent platform: model gateway (LiteLLM)
- [ ] Agent platform: typed tool registry
- [ ] Agent platform: eval harness
- [ ] Agent platform: budget/cost tracking
- [ ] Prioritization agent (L1)
- [ ] Underwriting agent (L1)
- [ ] Follow-up agent (L1)
- [ ] Prompt-injection eval cases

## E11 — Deals & outcomes (Sprint 10–13)
- [ ] Deal workspace UI
- [ ] Offer chain versioning UI
- [ ] Closing checklist
- [ ] Outcome capture + extraction
- [ ] Error attribution (projected vs actual)
- [ ] Privacy / DSR (data subject request) saga

## E12 — Commercial (Sprint 12–14)
- [ ] Billing / usage wallet
- [ ] Reporting v1 (4 fixed dashboards)
- [ ] Admin console
- [ ] Export controls

## E13 — Hardening & GA launch (Sprint 14–18)
- [ ] Load tests
- [ ] Chaos testing on send path
- [ ] SOC2 evidence automation
- [ ] Restore drill
- [ ] Design-partner onboarding tooling
- [ ] Accuracy gate review
- [ ] GA — metro 1

---

## External / business track (not code — tracked here because it blocks E3 onward)
- [ ] ADR-006 — team size / runway decision
- [ ] Vendor data contract signed (derivative/persistence rights)
- [ ] ≥15 design-partner interviews conducted
- [ ] ≥5 design-partner LOIs signed (data-sharing) — required before PRD freeze
- [ ] ADR-008 — metro selection (3–5 disclosure-state metros)

**If nothing below E2 is moving, check this section first — it's very likely the real reason,
not an engineering slowdown.**

---

## How this file stays honest
- Only the Architect session checks/unchecks boxes, and only when the doc-defined acceptance
  criteria is actually met and demonstrated — not on "should be close."
- Session-by-session detail lives in `.claude/CURRENT_STATE.md`. The single active task is
  always in `.claude/NEXT_TASK.md`.
