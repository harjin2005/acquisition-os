---
name: vendor-adapter
description: Add a new licensed-data vendor adapter with fixture-driven contract tests.
---

# Skill: Vendor Adapter (E3)

**When to use:** onboarding a data provider (property attributes, comps, permits, etc.).

## Steps

1. Create `backend/app/modules/ingestion/vendors/<slug>/` with:
   - `adapter.py` — implements `VendorAdapter` protocol.
   - `mapping.py` — vendor fields → ontology fields (DOC-002 exact names).
   - `fixtures/` — snapshotted sample responses for each supported endpoint.
   - `tests/test_contract.py` — replays fixtures through the mapping.

2. Register in `backend/app/modules/ingestion/registry.py`.

3. Add coverage entry: metros, refresh frequency, licensed expiry (`licensed.property.expires_at`).

4. Egress security-group entry in Terraform (`infra/terraform/modules/network`).

5. Vendor keys registered in AWS Secrets Manager with scoped IAM policy; local `.env` uses **placeholders only**.

6. Add ER (Engineering Risk) mitigation entry to DOC-131 §4 if the vendor introduces a new critical-path dependency.

## Contract test rules

- Every field the adapter emits must be exercised by at least one fixture.
- On schema drift, the adapter enters **quarantine mode**: writes to `derived.quarantine_row` and pages the on-call — never silently drops.
