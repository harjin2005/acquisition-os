"""Ontology API tests — Owner CRUD via FastAPI TestClient + real Postgres."""

from __future__ import annotations

import base64
import json
import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.modules.identity.router import bootstrap_rate_limiter


@pytest.fixture()
def client() -> TestClient:
    # bootstrap_rate_limiter is process-global state (see app.core.rate_limit);
    # reset it per test so another test file's calls can't trip this one's.
    bootstrap_rate_limiter.reset()
    return TestClient(create_app())


def _dev_token(*, org_id: uuid.UUID, actor_id: uuid.UUID, role: str = "OWNER") -> str:
    payload = {
        "sub": str(actor_id),
        "org_id": str(org_id),
        "role": role,
        "email": "u@example.com",
        "iss": "https://auth.acquisition-os.local",
        "aud": "acquisition-os",
    }
    b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    return f"dev.{b64}"


@pytest.fixture()
def bootstrapped_org(client: TestClient, clean_db):
    r = client.post(
        "/api/v1/identity/orgs", json={"name": "Owner Test Co", "slug": "owner-test-co"}
    )
    assert r.status_code == 201, r.text
    body = r.json()
    org_id = uuid.UUID(body["org"]["id"])
    actor_id = uuid.UUID(body["founder"]["subject_id"])
    token = _dev_token(org_id=org_id, actor_id=actor_id)
    return client, token, org_id


def test_create_and_get_owner(bootstrapped_org):
    client, token, org_id = bootstrapped_org
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/api/v1/ontology/owners",
        json={"display_name": "Jane Landlord", "entity_type": "person"},
        headers=headers,
    )
    assert r.status_code == 201, r.text
    owner = r.json()
    assert owner["display_name"] == "Jane Landlord"
    assert owner["entity_type"] == "person"
    assert owner["org_id"] == str(org_id)

    r2 = client.get(f"/api/v1/ontology/owners/{owner['id']}", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["id"] == owner["id"]


def test_list_owners(bootstrapped_org):
    client, token, _org_id = bootstrapped_org
    headers = {"Authorization": f"Bearer {token}"}

    for name in ("Owner A", "Owner B"):
        r = client.post(
            "/api/v1/ontology/owners", json={"display_name": name}, headers=headers
        )
        assert r.status_code == 201

    r = client.get("/api/v1/ontology/owners", headers=headers)
    assert r.status_code == 200
    names = {o["display_name"] for o in r.json()}
    assert names == {"Owner A", "Owner B"}


def test_get_missing_owner_is_404(bootstrapped_org):
    client, token, _org_id = bootstrapped_org
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get(f"/api/v1/ontology/owners/{uuid.uuid4()}", headers=headers)
    assert r.status_code == 404


def test_owner_write_requires_auth(client: TestClient):
    r = client.post("/api/v1/ontology/owners", json={"display_name": "No Auth"})
    assert r.status_code == 401
