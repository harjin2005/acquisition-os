# NEXT_TASK.md — The ONE task the current session should do

**Only one task lives here at a time. The founder (or the Architect session) sets it.**

## Status update before the new task

Previous task (rate limiting on the public bootstrap endpoint) is **done** — hand-rolled
in-memory limiter, no new dependency, regression test passes, confirmed green in real CI
(run 29411451384). See `.claude/CURRENT_STATE.md` for full detail.

## No task currently assigned

Nothing is queued right now. The remaining open E1-tail items (see
`.claude/PROGRESS.md` → "Sprint 2 — E1 tail") are:
- MFA enforcement flag per org
- Device/session listing UI
- mypy promoted from advisory to hard-gate in CI
- Bootstrap-org: replace dev synthetic subject_id with real WorkOS provisioning webhook
- RBAC `dual_log=True` enforcement (likely blocked on E2's audit schema landing first)

**Founder: tell the Architect session which of these (or something else) is next**, or say
"pick the next one" and it'll propose the smallest, most self-contained option the way it did
for rate limiting — with reasoning, not just a pick.
