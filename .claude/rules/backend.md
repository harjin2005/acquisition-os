# Backend rules (path glob: `backend/**/*.py`)

**These rules are enforced by CI (import-linter + custom checks) where possible; treat them as law even where a check is missing.**

## Router/service/model split (DOC-130 §3)

- Routers in `backend/app/api/v1/**` and `backend/app/modules/<mod>/router.py` are **thin**. No business logic, no ORM queries beyond a Depends resolver.
- Business logic lives in `backend/app/modules/<mod>/service.py`.
- Models are private to their module. **Never import another module's models.** Cross-module data flow goes through service interfaces or domain events. Import-linter enforces this.

## Tenancy wrapper is mandatory

- Every DB session on the app engine **must** run inside `with tenancy(org_id, actor_id): with app_session() as db: ...`.
- The bare `service_role_session()` (RLS bypass) is importable only from `app.modules.ingestion` and `app.modules.admin`. If you need it elsewhere, open an ADR.
- `SET LOCAL app.org_id` — never `SET SESSION`. See DOC-131 §3 D10 (pooler compatibility).

## Index-or-justify

- Every new query path must either land on an existing index or be reviewed with a `noqa: seq-scan` comment plus a note in the PR. Missing coverage is a review block.

## Errors & responses

- Use `DomainError` and subclasses (`NotFoundError`, `InsufficientEvidence`). Never return bare HTTP 500 for a business condition.
- Illegal state transitions return 409 with a machine-readable code.
- `InsufficientEvidence` is **always** an error — never a numeric fallback (DOC-130 §3 underwriting rule).

## Datetime discipline

- Always `datetime.now(timezone.utc)`. `datetime.utcnow()` is banned (mypy will catch it in strict mode; add a lint if it slips in).

## No provider SDKs outside the gateway

- No module may import `openai`, `anthropic`, `google.generativeai`, or a Twilio/SES client directly. The LiteLLM gateway (`app.agents.platform.gateway`) is the single egress for models; `campaigns.send_service` is the only egress for messaging. Import-linter enforces this.
