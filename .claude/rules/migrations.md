# Migration rules (path glob: `backend/app/db/migrations/**`)

## Expand → backfill → contract

Every migration touching a live table must land in the *expand* phase first:

1. **Expand**: additive DDL — new nullable columns, new tables, new indexes with `CONCURRENTLY`, new policies. Deploy.
2. **Backfill**: data movement in a Temporal workflow, chunked, idempotent, resumable.
3. **Contract**: drop old columns/tables, tighten nullable, remove policies. Deploy only after the backfill dashboard is 100% and the expand version has been in prod ≥1 deploy cycle.

Each phase is its own migration file. **Never combine them.** PR description names which phase this is and the target date for the next phase.

## Rollback note

The PR description **must** include a rollback plan. `alembic downgrade -1` is the minimum bar; explain data implications.

## Ontology naming

Every new table/column name must be present in `docs/product/02-glossary-domain-ontology-v1.0.md`. CI greps the migration file against the glossary allowlist and fails on unknown terms.

## Indexes

Add indexes concurrently in a follow-up migration if the table is non-empty. Prefer partial + covering indexes over kitchen-sink indexes.

## RLS

Any new tenant-scoped table must:
- include `org_id uuid not null` (or, for the tenant itself, use `id` as the tenancy discriminator like `core.organization`);
- enable `ROW LEVEL SECURITY` and `FORCE ROW LEVEL SECURITY`;
- have a policy of the form `USING (org_id = current_setting('app.org_id')::uuid) WITH CHECK (org_id = current_setting('app.org_id')::uuid)`.

The RLS adversarial suite in `backend/tests/rls/` must add a case for the new table. Merge is blocked until it does.
