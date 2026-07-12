# Test credentials — AcquisitionOS Sprint 1

**Sprint 1 uses no persistent user credentials.** All authentication is dev-mode via a signed-JSON bearer token minted client-side.

## How dev auth works

- Backend runs with `WORKOS_MOCK_MODE=true` (dev-only, per `docs/adr/ADR-EMERGENT-001-runtime-adaptation.md`).
- Frontend mints a `dev.<base64json>` token in `/app/frontend/src/lib/api.js::mintDevToken()` after bootstrap.
- Backend accepts it via `/app/backend/app/core/auth.py::_decode_mock`.
- The mock path is physically disabled when `APP_ENV != development|test` (guard at line ~90 of `auth.py`).

## Reproducing an authenticated session by hand

```bash
BASE=https://422a889f-2377-4f59-b428-5e5a3adc748e.preview.emergentagent.com

# 1. Bootstrap an org — no auth required for this endpoint (dev path).
resp=$(curl -sS -X POST $BASE/api/v1/identity/orgs \
  -H 'Content-Type: application/json' \
  -d '{"name":"Test Co","slug":"test-co-'$(date +%s)'"}')
echo $resp

# 2. Mint a dev bearer for the founder.
python3 - <<'PY'
import json, base64
payload = {
  "sub":     "REPLACE_WITH_founder.subject_id",
  "org_id":  "REPLACE_WITH_org.id",
  "role":    "OWNER",
  "email":   "founder+test-co@dev.local",
  "iss":     "https://auth.acquisition-os.local",
  "aud":     "acquisition-os"
}
b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
print(f"dev.{b64}")
PY

# 3. Call authenticated endpoints.
curl -sS -H "Authorization: Bearer dev.<b64>" $BASE/api/v1/identity/orgs/me/members
```

## Real credentials (staging / prod)

- WorkOS `api_key`, `client_id`, `jwks_url` go into AWS Secrets Manager under `acquisition-os/{env}/workos/*` — see `infra/terraform/envs/staging/main.tf` `module.secrets`.
- These are **not** committed to the repo and are not needed to run the Sprint 1 preview.

## Ancillary services (Sprint 1 dev)

| Service | Host | User | Password | Note |
|---|---|---|---|---|
| Postgres (app) | localhost:5432 | `acquisition_os` | `acquisition_os_dev` | RLS-enforced (no BYPASSRLS) |
| Postgres (service role) | localhost:5432 | `acquisition_os_svc` | `acquisition_os_svc_dev` | `BYPASSRLS` — only used by `service_role_session()` |
| MongoDB | localhost:27017 | — | — | Retained for Emergent runtime; not read by app code |
