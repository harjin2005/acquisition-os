# Restore drill runbook

**Owner:** SRE / Founder-CTO. Executed **quarterly**.

## Purpose

Verify that AcquisitionOS can be restored from RDS PITR + S3 versioned artifacts within RTO (8h) and RPO (1h) targets (DOC-120 §8).

## Steps

1. Provision an isolated VPC + RDS instance via `infra/terraform/envs/drill/`.
2. Restore the most recent daily snapshot into the drill instance.
3. Run `alembic upgrade head` — should be a no-op.
4. Point a smoke-test task at the drill endpoint and confirm `/api/health` + a canned tenant query succeed under RLS.
5. Diff the row counts of key tables (`core.member`, `licensed.property`, `events.domain_event`) against a same-hour snapshot from prod — expected drift ≤ RPO.
6. Tear down the drill VPC.

## Sign-off

Signed checklist saved to `docs/drills/YYYY-QN-restore.md`. Any deviation from RTO/RPO becomes an ADR entry (or a pre-existing debt update).
