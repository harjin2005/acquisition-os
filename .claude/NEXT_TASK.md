# NEXT_TASK.md — The ONE task the current session should do

**Only one task lives here at a time. The founder (or the Architect session) sets it.**

## Current task
**Session:** BACKEND (session 2)
**Goal:** Fix one known, already-diagnosed bug. Do not add features, do not touch other modules.

Foundation (identity + ontology + RLS + CI) is already built and was verified running locally
by the Architect session on 2026-07-13 — do not rebuild or redesign anything. This task is a
single, scoped bug fix.

## The bug

`POST /api/v1/identity/orgs` (bootstrap) returns **HTTP 500** instead of the documented
**409 `slug_conflict`** when the same slug is submitted twice.

Root cause (already diagnosed in `test_reports/iteration_1.json`, which you should read first):
`IdentityService.create_organization` in `backend/app/modules/identity/service.py` checks for
a duplicate slug using `service_role_session()` — but the router (`identity/router.py::bootstrap_org`)
wraps the whole call in `tenancy(new_org_id)` for a brand-new org id. Re-verify this is still the
live bug (it may have shifted slightly) before patching — read both files, don't assume the old
diagnosis is 100% still accurate line-for-line.

## Steps
1. Read `backend/app/modules/identity/service.py::create_organization` and
   `backend/app/modules/identity/router.py::bootstrap_org`. Confirm the exact failure path.
2. Fix so a duplicate slug returns `409` with `{"error": "domain_error", "code": "slug_conflict"}`
   (matches the `DomainError` pattern already used elsewhere in this file — see
   `app/core/errors.py` for how `DomainError` maps to HTTP responses).
3. Add a regression test in `backend/tests/api/test_identity_api.py`: bootstrap the same slug
   twice, assert the second call is 409 with code `slug_conflict`, not 500.
4. Run `pytest backend/tests/api backend/tests/rls -q` — show the founder the output. All must
   pass, including the new test.
5. Do NOT touch: rate limiting, dual-log enforcement, any other module, any migration. Those are
   separate, later tasks — one task at a time.

**Definition of done:** the new regression test passes, the full existing suite
(`tests/api`, `tests/rls`, `tests/integration`) still passes, and you show the founder real
pytest output (not a summary claim).

**If anything is unclear:** follow `.claude/STOP_RULES.md` — stop and ask one question.

---
### Also flagged, NOT this task, needs its own future task:
- `frontend/yarn.lock` should be committed (currently missing from the repo, only exists after
  running `yarn install` locally; CI's `ci.yml` already assumes it exists for caching).
- `.claude/skills/new-migration.md` and `.claude/skills/new-migration/SKILL.md` — two skills
  with the same name, different content. Founder should pick one and delete the other.
