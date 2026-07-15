# CURRENT_STATE.md — What is done so far

**This file is the shared memory between all sessions. Every session updates it when finished.**
**Keep it short. Newest at top.**

_Last updated: 2026-07-15 (Architect session — CI is genuinely green for the first time)_

## Project status
- Phase: Sprint 1 (Foundation) — built, verified locally AND in real CI this session.
- All design docs are complete and live in `/docs/product/`.
- Next milestone: M1 — foundation deployed. Locally proven + CI-proven this session;
  staging deploy still not applied (Terraform scaffolded only).
- **CI (`ci.yml`) is fully green for the first time since this repo was pushed to GitHub.**
  Run: https://github.com/harjin2005/acquisition-os/actions/runs/29408811712

## What's built
- Backend: FastAPI app (`backend/app/main.py`), identity module (orgs/members/invites/roles,
  real service logic, RLS-enforced), ontology module (Property, stub router). 9 real HTTP
  endpoints. Postgres RLS with `FORCE ROW LEVEL SECURITY`, `SET LOCAL app.org_id` tenancy wrapper.
  2 Alembic migrations (schemas + baseline tables, then ontology expansion).
- Frontend: React 3-screen app (Overview / Bootstrap / Console) — intentionally minimal,
  proves the identity flow works, not product UI.
- CI: `.github/workflows/ci.yml` — lint, format, mypy (advisory), import-linter, ontology
  check, alembic upgrade, **RLS adversarial suite (genuinely verified now)**, API tests,
  integration tests, frontend build, gitleaks, pip-audit. All green.
- Infra: Terraform modules for AWS (network/rds/cache/ecs/secrets/observability) — written,
  never applied. No live staging/prod environment exists.
- AI agents (prioritization/underwriting/followup): NOT built. Empty stub folders only. This
  is expected — per the execution plan, agents land in Sprint 8-13 (E10), not Sprint 1.
- ~10 other modules (leads, deals, conversations, campaigns, underwriting, admin, billing,
  imports, ingestion, notifications, outcomes, privacy) have SQLAlchemy models only — no
  migration, no router, no service, no tests. Not wired into the running app.

## Fixed this session (foundation bugs, not new features)
1. `AuditEntry.metadata` → `details` (reserved SQLAlchemy attribute name, crashed every fresh
   install via `db/registry.py`'s model imports). No migration existed yet — pure Python fix.
2. Added missing `email-validator==2.2.0` to `requirements.txt` (`pydantic.EmailStr` needs it;
   backend couldn't boot without it).
3. `tests/api/test_public_url_e2e.py` crashed collection for the whole `tests/api` directory
   outside the Emergent preview (hard `import requests` + hard env-var lookup). Now skips
   cleanly via `pytest.importorskip` + `skipif`.
4. **Corrected a wrong claim from earlier this session:** the bootstrap slug-idempotency 500
   bug (previously believed unfixed, per a stale testing-agent report) was **already fixed** —
   `service.py` already does the RLS-bypass slug check, `errors.py` already has the
   `IntegrityError→409` safety net, and a regression test already existed and passes.
5. Fixed the CI backend job's actual first failure: 5 ruff unused-import lint errors
   (auto-fixed), then a second gate it hadn't reached yet — `ruff format --check` failing on
   31 never-formatted files (applied `ruff format .`). Reformatting exposed a fragile
   `# noqa: F821` that had been suppressing an undefined `Principal` type hint in
   `identity/service.py` — fixed properly by importing `Principal` instead of re-aligning
   the comment.
6. Fixed `.importlinter`'s stale `ignore_imports` allowlist — `db/registry.py` was expanded
   (0002_ontology_expansion) to import 8 module model files, but the allowlist only covered
   2. The "merge-blocking" boundary contract was genuinely broken; now matches reality.
7. **The big one — real cross-tenant RLS bypass in CI, confirmed in actual GitHub Actions,
   not just locally:** `ci.yml`'s Postgres service container set `POSTGRES_USER: acquisition_os`,
   which makes that role the Postgres **bootstrap superuser** — superusers unconditionally
   bypass RLS regardless of `BYPASSRLS`/`FORCE ROW LEVEL SECURITY`. The "merge-blocking" RLS
   adversarial suite was not actually verifying tenant isolation. Fixed by provisioning two
   genuine non-superuser roles (`acquisition_os_app` for the RLS-restricted app engine,
   `acquisition_os_svc` with BYPASSRLS for migrations/service access) and never connecting as
   the bootstrap role again. Verified locally end-to-end before pushing, then confirmed in a
   real CI run: 50 passed, 1 skipped, 0 failed, all 9 RLS adversarial cases green.
8. Gitleaks flagged `token=body.token, subject_id=body.subject_id` in `identity/router.py` as
   a secret (generic-api-key rule). Verified false positive (keyword args passing a
   user-submitted token, not a credential; entropy ~3.7 vs ~4.5+ for real secrets). Added
   `.gitleaks.toml` with `[extend] useDefault = true` + a narrow regex allowlist for this one
   finding — verified locally that fake AWS/GitHub tokens are still caught by the full
   default ruleset.
9. Resolved `.claude/skills/new-migration` duplication (kept the new founder-facing
   `SKILL.md`, removed the old flat file). Committed `frontend/yarn.lock`. Added `.claude/PROGRESS.md`
   as a granular founder-facing checklist against the full 18-sprint plan.

## Proof it runs (this session)
- Local (throwaway Docker Postgres, exact CI role recipe): `alembic upgrade head` clean,
  50 passed / 1 skipped / 0 failed including all 9 RLS adversarial cases + 35 RBAC matrix cases.
- Real GitHub Actions run 29408811712: **all 3 workflows green** — frontend build, full
  backend suite (14 steps), security (gitleaks + pip-audit).
- `POST /api/v1/identity/orgs` → created a real org + founder end-to-end through the
  RLS-enforced identity service.

## Known problems / things to watch
- No rate limiting on the public, unauthenticated bootstrap-org endpoint.
- RBAC permissions mark `org.member.role` / `org.member.remove` as `dual_log=True` but no
  code actually enforces or records a second-actor witness — metadata without enforcement.
- ADR-006 (team size / budget) still open — does not block Sprint 1.
- Vendor data contract not signed yet — does not block Sprint 1.
- `deploy.yml`'s migrate step is a placeholder (`echo "Would run: aws ecs run-task..."`) —
  not a real migration execution. Not touched this session (deploy pipeline, no AWS account
  wired yet — out of scope until staging is actually being applied).

## Log (newest first)
- 2026-07-15 — Architect session: found and fixed a real cross-tenant RLS bypass in CI
  (bootstrap-superuser role), confirmed via real GitHub Actions runs before and after.
  CI is fully green for the first time. Corrected an earlier wrong claim about the slug bug
  (it was already fixed). Fixed ruff lint/format, stale import-linter allowlist, a gitleaks
  false positive. See "Fixed this session" above for full detail.
- 2026-07-13 — Architect session: extracted the `.claude/` setup kit from
  `claude-code-setup-v1.zip` (merged, did not blindly overwrite existing rules/agents/settings).
  Verified Sprint 1 foundation actually boots locally end-to-end. Fixed 2 real foundation bugs
  found during verification (`metadata` reserved-name crash, missing `email-validator` dep).
