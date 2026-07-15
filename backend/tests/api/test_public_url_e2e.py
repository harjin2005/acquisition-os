"""End-to-end API tests hitting the LIVE public REACT_APP_BACKEND_URL.

Verifies Sprint 1 acceptance criteria against the deployed backend (Emergent
ingress -> backend on :8001). Uses dev-mode WorkOS mock tokens (dev.<b64json>).

Covers:
- /api/health, /api/meta/sprint
- Identity: bootstrap, get me, list members, invites (accept & permission),
  slug idempotency (409), missing auth (401).
- Cross-tenant RLS isolation via /api/v1/ontology/properties.
"""

from __future__ import annotations

import base64
import json
import os
import uuid
from pathlib import Path

import pytest
from dotenv import load_dotenv

requests = pytest.importorskip(
    "requests", reason="Emergent-preview-only e2e test dependency"
)

# Load frontend env so we hit the SAME URL a browser user hits (Emergent preview only).
load_dotenv(Path("/app/frontend/.env"))
BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")

pytestmark = pytest.mark.skipif(
    not BASE_URL,
    reason="REACT_APP_BACKEND_URL not set — Emergent-preview-only e2e test",
)


def _mint_dev_token(
    *, org_id: str, subject_id: str, role: str = "OWNER", email: str = "u@example.com"
) -> str:
    payload = {
        "sub": str(subject_id),
        "org_id": str(org_id),
        "role": role,
        "email": email,
        "iss": "https://auth.acquisition-os.local",
        "aud": "acquisition-os",
    }
    b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    return f"dev.{b64}"


def _unique_slug(prefix: str = "test") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


@pytest.fixture(scope="module")
def s() -> requests.Session:
    sess = requests.Session()
    sess.headers.update({"Content-Type": "application/json"})
    return sess


# ---- Meta ----------------------------------------------------------------


def test_health_ok(s):
    r = s.get(f"{BASE_URL}/api/health", timeout=15)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body and isinstance(body["version"], str)
    assert "env" in body and isinstance(body["env"], str)


def test_sprint_meta_all_six_ac_met(s):
    r = s.get(f"{BASE_URL}/api/meta/sprint", timeout=15)
    assert r.status_code == 200
    body = r.json()
    assert body["sprint"] == 1
    acs = body["acceptance_criteria"]
    assert len(acs) == 6
    ac_ids = [a["id"] for a in acs]
    assert ac_ids == ["ac1", "ac2", "ac3", "ac4", "ac5", "ac6"]
    for a in acs:
        assert a["met"] is True, f"AC {a['id']} not met: {a}"


# ---- Auth guards ---------------------------------------------------------


def test_get_orgs_me_requires_auth(s):
    r = s.get(f"{BASE_URL}/api/v1/identity/orgs/me", timeout=15)
    assert r.status_code == 401


def test_list_members_requires_auth(s):
    r = s.get(f"{BASE_URL}/api/v1/identity/orgs/me/members", timeout=15)
    assert r.status_code == 401


# ---- Bootstrap + members --------------------------------------------------


@pytest.fixture(scope="module")
def org_a(s):
    slug = _unique_slug("aos-a")
    r = s.post(
        f"{BASE_URL}/api/v1/identity/orgs",
        json={"name": "AOS A", "slug": slug},
        timeout=20,
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert "org" in body and "founder" in body
    assert body["org"]["slug"] == slug
    uuid.UUID(body["org"]["id"])
    uuid.UUID(body["founder"]["subject_id"])
    assert body["founder"]["role"] == "owner"
    return body, slug


@pytest.fixture(scope="module")
def org_b(s):
    slug = _unique_slug("aos-b")
    r = s.post(
        f"{BASE_URL}/api/v1/identity/orgs",
        json={"name": "AOS B", "slug": slug},
        timeout=20,
    )
    assert r.status_code == 201, r.text
    return r.json(), slug


def test_bootstrap_slug_idempotency_returns_409(s, org_a):
    body, slug = org_a
    r = s.post(
        f"{BASE_URL}/api/v1/identity/orgs",
        json={"name": "Duplicate", "slug": slug},
        timeout=15,
    )
    assert r.status_code == 409, f"expected 409, got {r.status_code}: {r.text}"
    txt = r.text.lower()
    assert "slug" in txt or "conflict" in txt


def test_get_orgs_me_with_token(s, org_a):
    body, _slug = org_a
    org_id = body["org"]["id"]
    sub = body["founder"]["subject_id"]
    token = _mint_dev_token(org_id=org_id, subject_id=sub, role="OWNER")
    r = s.get(
        f"{BASE_URL}/api/v1/identity/orgs/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    assert r.status_code == 200
    org = r.json()
    assert org["id"] == org_id
    assert org["name"] == body["org"]["name"]


def test_members_list_shows_founder_as_owner(s, org_a):
    body, _slug = org_a
    org_id = body["org"]["id"]
    sub = body["founder"]["subject_id"]
    token = _mint_dev_token(org_id=org_id, subject_id=sub, role="OWNER")
    r = s.get(
        f"{BASE_URL}/api/v1/identity/orgs/me/members",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    assert r.status_code == 200
    members = r.json()
    assert len(members) >= 1
    owners = [m for m in members if m["role"] == "owner"]
    assert len(owners) >= 1
    assert owners[0]["subject_id"] == sub
    assert owners[0]["status"] == "active"


# ---- Invites (RBAC + accept flow) -----------------------------------------


def test_invite_viewer_gets_403(s, org_a):
    body, _slug = org_a
    org_id = body["org"]["id"]
    sub = body["founder"]["subject_id"]
    # A viewer token should be denied invite creation (needs manager+)
    token = _mint_dev_token(org_id=org_id, subject_id=sub, role="VIEWER")
    r = s.post(
        f"{BASE_URL}/api/v1/identity/orgs/me/invites",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "denied@example.com", "role": "member"},
        timeout=15,
    )
    assert r.status_code == 403, r.text
    detail = r.json()
    # error message should include permission_denied
    txt = json.dumps(detail).lower()
    assert "permission_denied" in txt or "permission" in txt


def test_invite_manager_can_create_and_accept(s, org_a):
    body, _slug = org_a
    org_id = body["org"]["id"]
    sub = body["founder"]["subject_id"]
    token = _mint_dev_token(org_id=org_id, subject_id=sub, role="OWNER")
    email = f"teammate-{uuid.uuid4().hex[:8]}@example.com"
    r = s.post(
        f"{BASE_URL}/api/v1/identity/orgs/me/invites",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": email, "role": "member"},
        timeout=15,
    )
    assert r.status_code == 201, r.text
    inv = r.json()
    assert inv["email"] == email
    assert inv["role"] == "member"
    assert inv["status"] == "pending"
    assert "token" in inv and inv["token"]

    # Accept the invite with a fresh subject_id
    new_subject = str(uuid.uuid4())
    r2 = s.post(
        f"{BASE_URL}/api/v1/identity/invites/accept",
        json={"token": inv["token"], "subject_id": new_subject},
        timeout=15,
    )
    assert r2.status_code == 200, r2.text
    member = r2.json()
    assert member["email"] == email
    assert member["role"] == "member"
    assert member["status"] == "active"
    assert member["subject_id"] == new_subject


def test_invite_accept_bad_token_returns_404(s):
    r = s.post(
        f"{BASE_URL}/api/v1/identity/invites/accept",
        json={"token": "totally-not-a-real-token", "subject_id": str(uuid.uuid4())},
        timeout=15,
    )
    assert r.status_code == 404, r.text


# ---- Cross-tenant RLS isolation via ontology stub -------------------------


def test_cross_tenant_property_isolation(s, org_a, org_b):
    a_body, _ = org_a
    b_body, _ = org_b

    a_org_id = a_body["org"]["id"]
    a_sub = a_body["founder"]["subject_id"]
    b_org_id = b_body["org"]["id"]
    b_sub = b_body["founder"]["subject_id"]

    # Founders are OWNER; property.write needs MEMBER+
    a_tok = _mint_dev_token(org_id=a_org_id, subject_id=a_sub, role="OWNER")
    b_tok = _mint_dev_token(org_id=b_org_id, subject_id=b_sub, role="OWNER")

    # Seed a property under org A
    a_prop = {
        "address_line1": "1 Alpha Way",
        "city": "AlphaCity",
        "state": "TX",
        "postal_code": "75001",
    }
    rA = s.post(
        f"{BASE_URL}/api/v1/ontology/properties",
        headers={"Authorization": f"Bearer {a_tok}"},
        json=a_prop,
        timeout=15,
    )
    assert rA.status_code == 201, rA.text
    created_a = rA.json()
    assert created_a["org_id"] == a_org_id

    # Seed a property under org B
    b_prop = {
        "address_line1": "2 Bravo Blvd",
        "city": "BravoCity",
        "state": "TX",
        "postal_code": "75002",
    }
    rB = s.post(
        f"{BASE_URL}/api/v1/ontology/properties",
        headers={"Authorization": f"Bearer {b_tok}"},
        json=b_prop,
        timeout=15,
    )
    assert rB.status_code == 201, rB.text
    created_b = rB.json()
    assert created_b["org_id"] == b_org_id

    # Org A list must NOT see org B's property.
    listA = s.get(
        f"{BASE_URL}/api/v1/ontology/properties",
        headers={"Authorization": f"Bearer {a_tok}"},
        timeout=15,
    )
    assert listA.status_code == 200
    a_rows = listA.json()
    a_org_ids = {p["org_id"] for p in a_rows}
    assert a_org_ids == {a_org_id}, f"cross-tenant leak: {a_org_ids}"
    a_addrs = [p["address_line1"] for p in a_rows]
    assert "1 Alpha Way" in a_addrs
    assert "2 Bravo Blvd" not in a_addrs

    # Org B list must NOT see org A's property.
    listB = s.get(
        f"{BASE_URL}/api/v1/ontology/properties",
        headers={"Authorization": f"Bearer {b_tok}"},
        timeout=15,
    )
    assert listB.status_code == 200
    b_rows = listB.json()
    b_org_ids = {p["org_id"] for p in b_rows}
    assert b_org_ids == {b_org_id}, f"cross-tenant leak: {b_org_ids}"


def test_property_write_denied_for_viewer(s, org_a):
    body, _ = org_a
    org_id = body["org"]["id"]
    sub = body["founder"]["subject_id"]
    token = _mint_dev_token(org_id=org_id, subject_id=sub, role="VIEWER")
    r = s.post(
        f"{BASE_URL}/api/v1/ontology/properties",
        headers={"Authorization": f"Bearer {token}"},
        json={"address_line1": "x", "city": "y", "state": "TX", "postal_code": "75001"},
        timeout=15,
    )
    assert r.status_code == 403, r.text
