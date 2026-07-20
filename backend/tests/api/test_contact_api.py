"""Contact + ContactChannel + ConsentRecord API tests."""

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
        "/api/v1/identity/orgs",
        json={"name": "Contact Test Co", "slug": "contact-test-co"},
    )
    assert r.status_code == 201, r.text
    body = r.json()
    org_id = uuid.UUID(body["org"]["id"])
    actor_id = uuid.UUID(body["founder"]["subject_id"])
    token = _dev_token(org_id=org_id, actor_id=actor_id)
    return client, token, org_id


def test_create_contact_and_get(bootstrapped_org):
    client, token, _org_id = bootstrapped_org
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/api/v1/ontology/contacts",
        json={"display_name": "John Seller"},
        headers=headers,
    )
    assert r.status_code == 201, r.text
    contact = r.json()
    assert contact["display_name"] == "John Seller"
    assert contact["role"] == "owner_of_record"

    r2 = client.get(f"/api/v1/ontology/contacts/{contact['id']}", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["id"] == contact["id"]


def test_add_channel_defaults_to_consent_unknown(bootstrapped_org):
    client, token, _org_id = bootstrapped_org
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/api/v1/ontology/contacts",
        json={"display_name": "Jane Seller"},
        headers=headers,
    )
    contact_id = r.json()["id"]

    r2 = client.post(
        f"/api/v1/ontology/contacts/{contact_id}/channels",
        json={"channel": "sms", "address": "+15551234567"},
        headers=headers,
    )
    assert r2.status_code == 201, r2.text
    ch = r2.json()
    assert ch["channel"] == "sms"
    assert ch["address"] == "+15551234567"
    # The compliance-critical assertion: a freshly added channel is NEVER
    # sendable by default — must start unknown, never opted-in.
    assert ch["consent_state"] == "consent_unknown"

    r3 = client.get(f"/api/v1/ontology/contacts/{contact_id}/channels", headers=headers)
    assert r3.status_code == 200
    channels = r3.json()
    assert len(channels) == 1
    assert channels[0]["consent_state"] == "consent_unknown"


def test_duplicate_channel_is_conflict(bootstrapped_org):
    client, token, _org_id = bootstrapped_org
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/api/v1/ontology/contacts", json={"display_name": "Dup Test"}, headers=headers
    )
    contact_id = r.json()["id"]

    body = {"channel": "email", "address": "seller@example.com"}
    r1 = client.post(
        f"/api/v1/ontology/contacts/{contact_id}/channels", json=body, headers=headers
    )
    assert r1.status_code == 201

    r2 = client.post(
        f"/api/v1/ontology/contacts/{contact_id}/channels", json=body, headers=headers
    )
    assert r2.status_code == 409, r2.text
    assert r2.json()["error"] == "channel_conflict"


def test_channel_on_missing_contact_is_404(bootstrapped_org):
    client, token, _org_id = bootstrapped_org
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post(
        f"/api/v1/ontology/contacts/{uuid.uuid4()}/channels",
        json={"channel": "sms", "address": "+15550000000"},
        headers=headers,
    )
    assert r.status_code == 404
