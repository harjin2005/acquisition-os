---
name: new-module
description: Scaffold a new backend module matching DOC-130 §3 module anatomy.
---

# Skill: New Backend Module

**When to use:** you are adding a module listed in DOC-130 §3 (or extending the list via an ADR).

## Steps

1. Create the directory: `backend/app/modules/<name>/` with these files:
   - `__init__.py`
   - `models.py` — SQLAlchemy models. Use `TenantMixin` for tenant-scoped tables.
   - `schemas.py` — Pydantic request/response shapes.
   - `service.py` — business logic; router does not touch the DB directly.
   - `router.py` — thin FastAPI router, wired under `/api/v1/<name>` in `app/main.py`.
   - `events.py` — domain events emitted by the module (outbox contract).
   - `jobs.py` — background/Temporal task registrations (empty at first).
   - `tests/` — module-scope unit tests (integration lives in `backend/tests/integration`).

2. Register the module's models in `backend/app/db/registry.py`.

3. Add tables (if any) via a new Alembic migration (`alembic revision -m "<mod>: initial"`) following the `new-migration` skill.

4. Add per-module README at `docs/modules/<name>.md` using the template in `docs/modules/_template.md`.

5. Update the import-linter contracts in `.importlinter` if your module needs new boundary edges. Prefer service interfaces + domain events.

6. Wire the router in `app/main.py`.

7. Write tests before merging:
   - Unit tests: state machines, business rule invariants.
   - RLS tests: at least one adversarial cross-tenant test per new tenant table.
   - API contract: one happy-path test per public endpoint.

## Don't

- Import models across modules. Route through the module's service.
- Add a new dependency without an OSS-table entry in DOC-130 §10.
- Ship without a module README.
