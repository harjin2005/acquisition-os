# Send-path incident runbook (E9/E10)

**Owner:** Backend lead + Compliance reviewer
**Severity ladder:** any suppression bypass = SEV-1. Any silent send failure > 5% of a batch = SEV-2.

## Detect

- Grafana alert: `suppression_verifier_failure > 0` → page.
- Grafana alert: `send_service_error_rate > 5%` over 5m → page.
- Sentry: any exception thrown by `campaigns.send_service` → page.

## Contain (first 5 minutes)

1. `admin.emergency_stop_sends(org_id | 'ALL')` — pauses all in-flight campaigns.
2. Notify #incidents-sev1 with the run_id, org_id, and time range.
3. Snapshot the affected `message` rows and `audit.log` entries.

## Diagnose

- Inspect the suppression matrix inputs for the affected messages.
- Cross-check `consent_state`, `dnc`, `litigator_flag`, `quiet_hours`, per-day caps against actual behavior.
- If the discrepancy is in the send service: this is a code bug. If it is in the state: this is a data bug (upstream).

## Remediate

- **Code bug** → hotfix branch, expand-only migration if state schema needs a fix, deploy, resume via `admin.resume_sends()`.
- **Data bug** → replay ingestion + reconcile suppression before resume.

## Report

- Public postmortem in `docs/postmortems/YYYY-MM-DD-send-path.md` within 5 business days.
- Update this runbook if detection or containment was slow.

## Never

- Bypass suppression to "clear the queue".
- Ship a hotfix without the compliance matrix test being updated first.
