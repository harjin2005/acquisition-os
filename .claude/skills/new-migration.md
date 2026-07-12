---
name: new-migration
description: Create an Alembic migration under the expand-contract policy.
---

# Skill: New Migration

## Checklist

- [ ] `cd backend && alembic revision -m "<slug>"` (do NOT hand-edit the revision id).
- [ ] Name is in `snake_case`, prefixed with the module (`identity_add_mfa_flag`).
- [ ] The migration is a **single phase** (expand OR backfill OR contract). Never combine.
- [ ] All new column names match the ontology glossary (`docs/product/02-glossary-domain-ontology-v1.0.md`).
- [ ] For every new tenant-scoped table:
  - `org_id uuid not null` column, indexed;
  - `ENABLE ROW LEVEL SECURITY` + `FORCE ROW LEVEL SECURITY`;
  - `CREATE POLICY <table>_tenant_iso ...` binding `org_id` to `current_setting('app.org_id', true)::uuid` with `WITH CHECK`.
- [ ] `backend/tests/rls/test_cross_tenant_isolation.py` has a new adversarial case for the table.
- [ ] `downgrade()` implemented (or the PR is a `no_downgrade` ADR).
- [ ] Rollback note included in the PR description.

## Never

- `DROP COLUMN` in the same migration as its previous read path. Contract phase only.
- Manual DDL in prod. Everything is migrations.
- Modify an already-merged migration file. Add a follow-up.
