# Module: ontology (Sprint 1 stub)

**Owner:** Backend / Data lead · **Status:** Sprint 1 stub (E2 landing)
**DOC-121 section:** A5 (partial)
**DOC-130 §3 row:** ontology

## Purpose

Sprint 1 lands a **licensed.property stub only**, sized to prove RLS end-to-end for a licensed-schema tenant table. The full ontology surface (property, owner, contact, lead, deal, offer) with state machines lands in E2 (Sprints 2–4).

## Public interface (Sprint 1)

- `POST /api/v1/ontology/properties` — create a stub property (Member+).
- `GET  /api/v1/ontology/properties` — list org's properties (Viewer+).

## Invariants

- Every property row has a valid `org_id`. RLS policy binds `org_id = current_setting('app.org_id')::uuid` with `WITH CHECK` on writes.
- `expires_at` is nullable in Sprint 1; Sprint 3 (E3) enforces vendor expiry semantics.

## Not in scope (Sprint 1)

- Property comps, adjustments, calibration.
- Owner / contact / lead / deal / offer entities.
- State machines (`transition_lead()` etc. — E2).

## Tests

- API: `backend/tests/api/test_identity_api.py::test_cross_org_api_is_denied` covers cross-tenant property read.
- RLS: `backend/tests/rls/test_cross_tenant_isolation.py` includes property adversarial cases.
