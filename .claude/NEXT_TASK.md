# NEXT_TASK.md — The ONE task the current session should do

**Only one task lives here at a time. The founder (or the Architect session) sets it.**

## Status update before the new task

The previous task written here (fix the bootstrap slug 500→409 bug) turned out to already be
fixed — verified with a passing regression test. **Do not redo it.** See
`.claude/CURRENT_STATE.md` for the full list of what this session actually found and fixed,
including a real cross-tenant RLS bypass in CI that's now resolved and confirmed green in
real GitHub Actions.

## Proposed current task (awaiting founder confirmation — not started)

**Session:** BACKEND (session 2)
**Goal:** Add rate limiting to the one public, unauthenticated endpoint. Foundation-only,
no other module, no migration.

### Why this one
Of the open E1-tail items (MFA flag, device-session UI, mypy hard-gate, RBAC dual-log
enforcement, rate limiting), this is the smallest, most self-contained, and the one flagged
highest-risk in review: `POST /api/v1/identity/orgs` (bootstrap) is fully public and
unauthenticated by design (dev path, per ADR-EMERGENT-001) — with no rate limit, anyone can
spam-create organizations and rows in the database.

### Steps
1. Read `backend/app/modules/identity/router.py::bootstrap_org` and check what rate-limiting
   library (if any) is already in `backend/requirements.txt` — none currently is. Adding one is
   a new dependency: per `.claude/STOP_RULES.md` rule 3, **stop and ask before adding it** (e.g.
   `slowapi`). Don't assume.
2. Apply a rate limit to `POST /api/v1/identity/orgs` only — a reasonable low ceiling
   (e.g. 10/hour per IP) since it's a bootstrap/dev path, not a high-traffic endpoint.
3. Add a test asserting the limit actually triggers a 429 after the threshold.
4. Run `pytest backend/tests/api backend/tests/rls -q` — show the founder real output.
5. Do NOT touch: MFA, dual-log enforcement, mypy hard-gate, any other module. One task at a time.

**Definition of done:** the new test passes, the full existing suite still passes, founder
sees real pytest output.

**If anything is unclear:** follow `.claude/STOP_RULES.md` — stop and ask one question.

---
### Also flagged, NOT this task, needs its own future task:
- MFA enforcement flag per org (E1 tail).
- Device/session listing UI (E1 tail).
- mypy promoted from advisory (`|| true` in `ci.yml`) to hard-gate (E1 tail, pre-declared debt
  DEB-S1-002).
- RBAC `dual_log=True` enforcement for `org.member.role` / `org.member.remove` — currently
  metadata-only, no second-actor witness recorded or checked. Likely blocked on E2's audit
  schema (`AuditEntry`/`OutboxEvent` exist as models but have no migration/router/service yet).
- `deploy.yml`'s migrate step is a placeholder (`echo "Would run: ..."`) — not real. Needs a
  decision on when staging actually gets applied before this matters.
