# Module: {name}

**Owner:** {engineer} · **Status:** {Sprint N deliverable | GA | deprecated}
**DOC-121 section:** {A-X / B-Y}
**DOC-130 §3 row:** {row title}

## Purpose

*One paragraph: why this module exists. Anchor to a specific customer job.*

## Public interface

*Service functions callers may use. Everything else is private to the module.*

- `svc.foo(...)` — one-liner
- `svc.bar(...)` — one-liner

## Domain events emitted

*Outbox contract. Consumers listen; producers emit here.*

- `something.happened` — payload shape

## Jobs / workflows owned

- {Temporal workflow name} — cadence & failure mode

## Invariants

*State machines, referential integrity, invariants that MUST hold.*

- ...

## Failure modes

| Failure | Detection | Handling |
|---|---|---|
| e.g. vendor 500 | | |

## Tests

- Unit: `app/modules/{name}/tests/`
- RLS: rows added to `backend/tests/rls/test_cross_tenant_isolation.py`
- API: `backend/tests/api/test_{name}_api.py`
- Compliance (if applicable): `backend/tests/compliance/`

## Not in scope (v1)

- ...

## Runbook links

- `docs/runbooks/{module}-incident.md`
