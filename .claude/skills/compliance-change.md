---
name: compliance-change
description: Checklist for any change touching campaigns, suppression, consent, or TCPA-adjacent surfaces.
---

# Skill: Compliance-Sensitive Change

**If your PR touches ANY of these paths, this checklist is required:**

- `backend/app/modules/campaigns/**`
- `backend/app/modules/conversations/**` (opt-out handling)
- `backend/app/modules/privacy/**`
- Any migration touching `contact_channel`, `consent_state`, `suppression`, `campaign`, `message`.

## Required in the PR

- [ ] Backend lead **and** designated compliance reviewer approve the PR.
- [ ] Suppression matrix test (`backend/tests/compliance/`) covers every new branch of {consent state × DNC × litigator × quiet hours × caps × opt-out timing}.
- [ ] Per-message audit reconciliation still passes on staging.
- [ ] Injection eval cases updated if an agent surface is involved.
- [ ] Provider idempotency keys verified.
- [ ] Runbook entry added / updated in `docs/runbooks/send-path-incident.md` if incident semantics change.

## Never

- Merge a "quick fix" to the send path without a passing compliance matrix.
- Bypass suppression from any code path except `campaigns.suppression` (import-linter enforced).
- Add a suppression exception without a documented legal review.

## SEV-1 posture

Any bypass of suppression state at runtime = SEV-1 incident. Immediate mitigation is "pause all sends" via `admin.emergency_stop_sends()`.
