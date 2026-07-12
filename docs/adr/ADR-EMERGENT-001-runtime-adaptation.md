# ADR-EMERGENT-001 — Runtime adaptation for the Emergent preview environment

**Status:** Accepted (Sprint 1, dev-only)
**Date:** 2026-01-15
**Deciders:** Founder / CTO / Principal Engineers
**Supersedes:** none
**Amends:** ADR-010 (architecture) — non-canonical dev-only concessions

## Context

The AcquisitionOS repository is being incubated inside Emergent's Kubernetes preview environment, which provides:

- FastAPI backend on port 8001 (supervisor-managed, hot-reload)
- React frontend on port 3000
- MongoDB (protected env var `MONGO_URL`) as the default datastore

DOC-130 §5 / §7 mandate Postgres 16 + RLS + Alembic + WorkOS + AWS ECS + Terraform. None of those are natively provisioned inside the Emergent runtime.

## Decision

**The canonical stack (Postgres, WorkOS, AWS, Terraform) remains the source of truth.** We introduce two bounded, isolated dev-only adaptations to keep the Emergent preview functional without diverging the codebase:

1. **Postgres 15 in dev.** We install Postgres 15 directly in the preview container (Postgres 16 is not available for the preview's Debian 12 base without kernel-tier changes we cannot make). Migrations, models, and RLS policies are written for Postgres 16 semantics but are validated to run on 15. Production migrations run against Postgres 16 on RDS.
2. **`WORKOS_MOCK_MODE=true` in dev.** Auth is a signed-JSON `dev.<b64>` bearer token processed by a mock decoder that is **physically disabled** when `APP_ENV != development|test`. WorkOS SDK is wired for real JWKS verification; the switch is a boolean.
3. **MongoDB is retained** because Emergent's supervisor expects it to be running and its protected env vars are validated on deploy. `MONGO_URL` and `DB_NAME` remain in the environment but are **not read by any AcquisitionOS module** (grep the codebase — the only occurrence is in `app.core.config` for validation).

## Consequences

- The canonical DOC-130 stack does not change.
- Deploying to staging or prod requires: (a) real WorkOS credentials, (b) `WORKOS_MOCK_MODE=false`, (c) Postgres 16 via RDS. The infra Terraform is scaffolded in `infra/terraform/` for this purpose.
- The mock path is import-guarded (see `app/core/auth.py::get_principal`).
- Ontology, RLS policies, and tenancy semantics are identical in dev and prod.

## Alternatives rejected

- **Substitute MongoDB for Postgres:** violates ADR-010 §5, would erase RLS as the tenancy contract (ER2 mitigation), and would require rewriting DOC-002 modeling. Rejected.
- **Skip local dev entirely and rely on staging:** slows the design-partner feedback loop the roadmap depends on. Rejected.
- **Wait for Postgres 16 to be available in the preview base image:** blocks Sprint 1 indefinitely. Rejected.

## Re-entry criteria

- Postgres 16 becomes available in the Emergent base image → migrate dev to 16, delete this ADR clause.
- WorkOS credentials provided to the preview environment → set `WORKOS_MOCK_MODE=false` and remove the mock decoder entirely (still fenced by env, but the code path becomes dead — delete in a follow-up ADR).

## Verification

- `pytest backend/tests/rls` must be green (44 tests as of Sprint 1) — the tenancy contract is unchanged.
- `lint-imports` must be green — no module imports MongoDB drivers.
- `alembic upgrade head` succeeds on both Postgres 15 (dev) and 16 (staging).
