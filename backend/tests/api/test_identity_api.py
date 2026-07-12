"""API happy-path integration tests via FastAPI TestClient + real Postgres.

Runs against the same DB as RLS tests — fixtures truncate between tests.
"""

from __future__ import annotations

import base64
import json
import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def _dev_token(*, org_id: uuid.UUID, actor_id: uuid.UUID, role: str = "OWNER", email: str = "u@example.com") -> str:
    payload = {
        "sub": str(actor_id),
        "org_id": str(org_id),
        "role": role,
        "email": email,
        "iss": "https://auth.acquisition-os.local",
        "aud": "acquisition-os",
    }
    b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    return f"dev.{b64}"


def test_health(client: TestClient):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_sprint_meta(client: TestClient):
    r = client.get("/api/meta/sprint")
    assert r.status_code == 200
    body = r.json()
    assert body["sprint"] == 1
    assert all(ac["met"] is True for ac in body["acceptance_criteria"])


def test_bootstrap_and_list(client: TestClient, clean_db):
    r = client.post("/api/v1/identity/orgs", json={"name": "Bootstrap Co", "slug": "boot-co"})
    assert r.status_code == 201, r.text
    body = r.json()
    org_id = uuid.UUID(body["org"]["id"])
    founder = body["founder"]

    token = _dev_token(org_id=org_id, actor_id=uuid.UUID(founder["subject_id"]), role="OWNER")
    r2 = client.get("/api/v1/identity/orgs/me/members", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert len(r2.json()) == 1


def test_bootstrap_slug_idempotency_returns_409(client: TestClient, clean_db):
    """Regression: RCA — the slug pre-check must use the RLS-bypass service
    role because slug is a global-namespace invariant. Reposting the same
    slug must return 409 slug_conflict, never 500."""
    slug = "dup-slug-co"
    r1 = client.post("/api/v1/identity/orgs", json={"name": "First", "slug": slug})
    assert r1.status_code == 201

    r2 = client.post("/api/v1/identity/orgs", json={"name": "Second", "slug": slug})
    assert r2.status_code == 409, r2.text
    body = r2.json()
    assert body["error"] == "slug_conflict"


def test_cross_org_api_is_denied(client: TestClient, two_orgs):
    """AC-4: two orgs, cross-org API access denied by RLS."""
    org_a, org_b = two_orgs
    a_actor = uuid.uuid4()
    token = _dev_token(org_id=org_a, actor_id=a_actor)
    r = client.get("/api/v1/ontology/properties", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert uuid.UUID(body[0]["org_id"]) == org_a
    assert body[0]["city"] == "Alpha City"


def test_missing_auth_is_401(client: TestClient):
    r = client.get("/api/v1/identity/orgs/me")
    assert r.status_code == 401
