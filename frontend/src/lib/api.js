// Sprint 1 API shim. The generated TS SDK (packages/sdk-ts) replaces this in
// Sprint 3+ (see .github/workflows/sdk-publish.yml).

const BASE = process.env.REACT_APP_BACKEND_URL || '';

export async function apiGet(path, token) {
  const res = await fetch(`${BASE}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json();
}

export async function apiPost(path, body, token) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json();
}

// Sprint 1 dev auth (ADR-EMERGENT-001): mint a dev bearer for a subject we
// hold locally. Production uses WorkOS-hosted UI + JWKS-verified JWTs and this
// entire helper is dead code.
export function mintDevToken({ subject_id, org_id, role = 'OWNER', email }) {
  const payload = {
    sub: subject_id,
    org_id,
    role,
    email,
    iss: 'https://auth.acquisition-os.local',
    aud: 'acquisition-os',
  };
  const b64 = btoa(JSON.stringify(payload)).replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_');
  return `dev.${b64}`;
}
