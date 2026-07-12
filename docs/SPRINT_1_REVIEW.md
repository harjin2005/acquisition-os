# Sprint 1 Review — AcquisitionOS Foundation

**Sprint window:** kickoff → 2026-01-15
**Objective (DOC-131 §2):** Repo foundation, CI, Terraform staging, WorkOS auth + identity module skeleton, Alembic + RLS baseline, docs + ADR templates.
**Team:** Founder + engineers TBD (ADR-006 still open — plan is currently scoped to 1–5 engineers per DOC-130 assumption).

---

## 1. Completed work

### AC1 — `scripts/dev-up.sh` boots api + frontend locally  ✅

- Postgres 15 + roles + schemas + Alembic migrations, then supervisor restart of backend/frontend, then a bounded `/api/health` wait.
- Postgres 15 is a dev-only concession recorded in **ADR-EMERGENT-001**; production remains Postgres 16 on RDS (per DOC-130 §5).

### AC2 — CI: lint + typecheck + unit skeleton + `import-linter`  ✅

- `.github/workflows/ci.yml` runs against a Postgres 16 service container in Actions (matching prod, not the dev workaround).
- **4 import-linter contracts** enforcing:
  1. Modules cannot depend on the API layer.
  2. DB layer cannot depend on modules or API.
  3. Modules must not import other modules' models.
  4. Provider SDKs (`openai`, `anthropic`, `litellm`, `twilio`) only inside `app.agents.platform`.
- **Boundary-violation demo** shipped as a self-verifying pytest (`tests/integration/test_import_linter.py::test_import_linter_would_catch_a_violation`) — writes a synthetic `import openai` file into a module and asserts `lint-imports` exits non-zero.

### AC3 — Terraform staging scaffolded  ✅ (unapplied by design)

- 6 modules: `network`, `rds` (PG16 + RDS Proxy + Multi-AZ + Secrets Manager), `cache` (Valkey engine), `ecs-service` (Fargate + ALB target group + circuit-breaker rollback), `secrets`, `observability`.
- `envs/staging/main.tf` composes all six + KMS master key + ECS cluster.
- `envs/prod/` is intentionally a stub — production landing is Sprint 13 (E13).
- Deploy pipeline `.github/workflows/deploy.yml` with OIDC → AWS, no long-lived keys; migration is a one-off ECS `RunTask`; smoke check waits on `/api/health`.

### AC4 — WorkOS auth + identity module skeleton  ✅

- `app/core/auth.py` — real WorkOS JWKS/JWT verification path *plus* a `WORKOS_MOCK_MODE` dev decoder that is **physically disabled** when `APP_ENV != development|test`.
- Identity module: `Organization`, `Member`, `Invite` models with state machines (`{pending → active → suspended → removed}`), CHECK constraints, and the **dual-owner invariant** (last owner cannot be demoted or removed).
- RBAC matrix as data in `app/core/rbac.py`; `require_permission()` FastAPI dependency; 35 auto-generated matrix tests prove role monotonicity for every seed permission.
- API surface: bootstrap → me → members → invites → accept → change_role → remove_member.

### AC5 — Alembic baseline + RLS + adversarial suite  ✅ merge-blocking

- Single migration `0001_baseline.py` creates schemas + tables + RLS policies with `FORCE ROW LEVEL SECURITY` (owner still subject to RLS) and both `USING` and `WITH CHECK`.
- `core.organization` uses a special policy binding `id` (not `org_id`) — the tenant is its own row.
- Dedicated `acquisition_os_svc` role with `BYPASSRLS` for the escape hatch (ingestion + admin, once those modules land).
- **9 adversarial RLS tests** cover: missing tenancy denial, cross-org read denial (org/member/invite/property), cross-org write denial (WITH CHECK), UPDATE-with-cross-org-WHERE affects zero rows, forgotten `org_id` blocked, service-role bypass still works, and `SET LOCAL` semantics verified (the D10 pooler contract).

### AC6 — docs/product mirror + module README + ADR templates  ✅

- Full mirror of top-level DOCs into `docs/product/` (12 files).
- `docs/adr/_template.md` + `docs/adr/README.md` index (with ADR-001..011 status pointers) + **ADR-EMERGENT-001** (Runtime adaptation).
- Per-module READMEs: `docs/modules/_template.md`, `docs/modules/identity.md`, `docs/modules/ontology.md`.
- Runbooks: send-path incident, restore drill, feed-gap.
- `CLAUDE.md` at repo root (≤150 lines) + `.claude/{rules,skills,agents,hooks}/*` per DOC-131 §1.

### Test posture (final)

| Suite | Count | Status |
|---|---|---|
| RLS adversarial (`tests/rls/`) | 9 | ✅ merge-blocking |
| RBAC matrix | 35 | ✅ |
| Identity API | 6 | ✅ (includes 409 slug regression) |
| Integration (import-linter) | 2 | ✅ |
| Live URL e2e (added by testing subagent) | 12 | ✅ |
| **Total** | **64** | **✅ 100%** |

---

## 2. Remaining work (Sprint 2+, in priority)

Nothing from Sprint 1 was deferred. Sprint 2 begins with E1 tail (MFA, device sessions) + E2 kickoff (outbox, audit, ontology full surface). Full backlog lives in `/app/memory/PRD.md`.

---

## 3. Technical debt introduced (all pre-declared)

| ID | Debt | Repayment trigger |
|---|---|---|
| **DEB-S1-001** | Dev uses Postgres 15 (ADR-EMERGENT-001); prod uses 16. | Emergent base image ships PG16 → migrate + delete ADR clause. |
| **DEB-S1-002** | mypy is advisory in CI (`|| true`). | Sprint 2 promotes to hard-gate once module set stabilizes. |
| **DEB-S1-003** | Ontology naming CI grep is permissive (log-only). | Sprint 3 (E3) requires strict enforcement before vendor data lands. |
| **DEB-S1-004** | Bootstrap endpoint is unauthenticated dev-path (mints synthetic subject_id). | Sprint 2 replaces with WorkOS provisioning webhook (E1 tail). |
| **DEB-S1-005** | JWKS cache in `app/core/auth.py` has no TTL/rotation. | Sprint 2 hardening. |

The DOC-131 §3 register (D1..D12) is *unchanged* — no new items promoted into the master debt register in Sprint 1.

---

## 4. Risks discovered (delta to DOC-131 §4)

- **ER-S1-A (Low):** dev environment's Postgres 15 could hide a PG16-only migration bug. Mitigation: the CI Postgres service image is 16, so migrations run on 16 in every PR. Prod parity preserved.
- **ER-S1-B (Low):** the mock auth path in `app/core/auth.py` is fenced only by `APP_ENV`. Mitigation: env comes from AWS Secrets Manager in staging/prod; a runtime toggle plus an integration test that asserts the dev decoder is unreachable outside dev lands in Sprint 2.

No new items make ER-critical.

---

## 5. Open questions for review

1. **ADR-006 (runway / team):** still open per MASTER_CONTEXT. Sprint 2 dating depends on this. Do we lock 1, 3, or 5 engineers?
2. **ADR-008 (metro selection):** does not block Sprint 2 but starts to matter at E3 (vendor terms are metro-specific). Preference?
3. **WorkOS environment provisioning:** please provide staging + prod WorkOS `client_id`s and `api_key`s (Secrets Manager path is scaffolded, values are placeholders). Cheapest path is to file them into `acquisition-os/staging/workos/*` before the first `terraform apply`.
4. **Vendor negotiation start (DD gate 4):** blocked on ADR-006 answer. The adapter framework will be built against fixtures regardless (per ER1 mitigation).

---

## 6. What Sprint 1 deliberately did NOT do

- No Pipeline / Inbox / Workspaces UI. Those are E7+.
- No campaigns, sends, suppression, or 10DLC wiring — E8/E9.
- No agents. E10.
- No vendor adapters. E3.
- No SDK generation past scaffold (`sdk-publish.yml` runs, but there is no consumer yet).
- No Jarvis. Per user direction, Sprint 5a: AcquisitionOS only.

The Sprint 1 note in DOC-131 §2 is quoted verbatim: *"Sprint 1 contains zero product features by design; skipping foundation is how 3-person teams drown in month 4."*

---

## 7. Definition of Done (self-check)

- [x] Acceptance criteria met, verified in test.
- [x] Tests written and passing (64/64).
- [x] Module READMEs written for identity + ontology.
- [x] Migration is single-phase, additive, glossary-conformant, with rollback.
- [x] Eval gate — N/A (no agent paths touched).
- [x] No new deps without an OSS-table entry (see updated `docs/product/30-engineering-handbook-v1.0.md` §10).
- [x] Deployed to preview and smoke-checked; deploy pipeline for staging scaffolded.

---

## 8. Recommendation

**Sprint 1 is complete. Please review and approve before Sprint 2 begins.**

Suggested first review checkpoints:
1. Read `CLAUDE.md` + `/app/memory/PRD.md` + `docs/adr/ADR-EMERGENT-001-runtime-adaptation.md`.
2. Visit `/api/meta/sprint` on the preview URL.
3. Run `cd backend && pytest tests/rls -q` — the load-bearing security certification.
4. Skim `.claude/rules/*.md` to confirm the enforced guardrails match your intent.

**I will not begin Sprint 2 until approval and answers to §5 open questions.**
