# NEXT_TASK.md — The ONE task the current session should do

**Only one task lives here at a time. The founder (or the Architect session) sets it.**

## Status update

Owner CRUD (create/list/get) is done — router + service, RLS-tested, verified live and in
real CI. See `.claude/CURRENT_STATE.md` for full detail. Also corrected `PROGRESS.md`: the
whole E2 database schema already existed (migration 0002) — what's missing on every
remaining E2 item is just the router/service layer, not the database.

## No task currently assigned

Natural next candidates, same pattern as Owner (schema exists, needs router + service):
- Contact + ContactChannel + ConsentRecord
- Lead (needs the state-machine service, not just CRUD — more involved)
- BuyBox
- MotivationSignal

**Founder: say which one (or say "pick the next one" and it'll be proposed with reasoning).**
