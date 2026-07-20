# NEXT_TASK.md — The ONE task the current session should do

**Only one task lives here at a time. The founder (or the Architect session) sets it.**

## Status update

Contact + ContactChannel + ConsentRecord done — router + service, RLS-tested, verified
live via curl. 83/83 tests pass locally, import-linter clean. **One open item:** GitHub's
API was down (503) when this was pushed, so the real-CI green check hasn't been confirmed
yet — check `gh run list --workflow=ci.yml --limit 3` next session and confirm before
trusting this as fully closed out.

## No task currently assigned

Natural next candidates (same pattern: schema exists, needs router + service):
- BuyBox (small, self-contained)
- MotivationSignal (small, self-contained)
- Lead (bigger — needs the state-machine service, not just CRUD)

**Founder: say which one, or say "pick the next one."**
