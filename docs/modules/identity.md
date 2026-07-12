# Module: identity

**Owner:** Backend lead · **Status:** Sprint 1 skeleton (E1)
**DOC-121 section:** A1 Identity
**DOC-130 §3 row:** identity

## Purpose

Owns the AuthN/AuthZ substrate for AcquisitionOS: organizations (the tenant), members (subjects bound to a role), invites (pending members). Every other module derives its tenancy context from this module's data. WorkOS is the authoritative auth provider (ADR-010 §8); this module owns the app-side mirror.

## Public interface

- `IdentityService.create_organization(...)` — bootstrap tenant + founder-owner.
- `IdentityService.invite_member(...)` — mint a single-use invite (Manager+).
- `IdentityService.accept_invite(...)` — activate a Member from an invite token.
- `IdentityService.change_role(...)` — mutate a member's role, honouring the dual-owner rule (Admin+, dual-log).
- `IdentityService.remove_member(...)` — soft-remove a member; last owner protected.

## Domain events emitted (contract, Sprint 2 outbox)

- `member.invited`
- `member.role_changed`
- `member.removed`

## Jobs / workflows owned

- (Sprint 2) seat reconciliation with WorkOS (E1 tail-end).

## Invariants

- Every `member.status` follows the state machine `{pending → active | suspended | removed}`; illegal transitions raise `DomainError` with a machine-readable code.
- The last active owner cannot be demoted or removed.
- Invite tokens are single-use; expiration is enforced in service, not client.

## Failure modes

| Failure | Detection | Handling |
|---|---|---|
| Duplicate slug on org create | UNIQUE constraint | 409 `slug_conflict` |
| Invite email already active member | Service check | 409 `already_member` |
| Invite expired | Service check | 409 `invite_expired` + status flip to `expired` |
| Last owner demotion/removal | Service check | 409 `last_owner` |
| WorkOS outage (JWKS) | httpx timeout | Cached JWKS + read-only grace (E1 §9) |

## Tests

- Unit: `app/modules/identity/tests/` (Sprint 2 will host state-machine property tests).
- RLS: `backend/tests/rls/test_cross_tenant_isolation.py` — cross-org org/member/invite read + write blocked.
- API: `backend/tests/api/test_identity_api.py` — bootstrap, list members, cross-org denial, 401 on missing auth.
- RBAC: `backend/tests/rls/test_rbac_matrix.py` — table-driven role monotonicity.

## Not in scope (v1)

- SSO enforcement toggle (E1 tail, Sprint 2).
- MFA enforcement per-org (E1 tail, Sprint 2).
- Device / session listing UI (Sprint 2).
- Seat billing (E12).

## Runbook links

- `docs/runbooks/auth-outage.md` (Sprint 4 deliverable)
