# Vendor feed-gap runbook (E3)

**Owner:** Data / Ingestion lead

## Detect

- Nightly anomaly job: `coverage.staleness_hours` exceeds SLA per metro.
- Adapter contract test regression on latest fixture snapshot.

## Contain

1. Flip the affected metro's freshness stamp to `stale` — the Receipts kit will surface this to every user of the affected data.
2. If the gap involves a critical field (e.g. sale_price for underwriting), promote to SEV-2 and page the founder.
3. Do **not** auto-swap to a secondary vendor without an ADR — cross-vendor mismatches are worse than staleness.

## Diagnose

- Vendor status page, adapter logs, quarantine table.
- Reproduce with the fixture recorder against the failing endpoint.

## Remediate

- If it's a vendor outage: wait, communicate ETA to design partners, keep receipts honest.
- If it's a schema drift: update the adapter mapping in a PR with fixture snapshot; contract test must pass.
- If it's an expired credential: rotate via Secrets Manager, redeploy.

## Never

- Silently keep serving stale comps to underwriting. Receipts must reflect freshness.
