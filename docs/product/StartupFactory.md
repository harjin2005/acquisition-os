# Startup Factory

**Purpose:** Startup #2 requires a domain adapter, not a rebuild. This file defines exactly what is shared, what is per-startup, and the instantiation procedure.

## 1. What is reusable (the platform inventory)
- **Documentation system:** the DOC-000 governance (roadmap, decision log, glossary-first ontology discipline, phase-gated diligence with confidence labels, blueprint templates) — the *method* that produced DOC-000..131, packaged as templates + skills.
- **Engineering kit:** `.claude/` scaffold, CI workflows, Terraform modules, module anatomy, RLS/tenancy harness, testing tiers, OSS policy table (DOC-130 patterns → `/platform/engineering-kit`).
- **AI platform:** gateway config, tool-registry pattern, eval-runner, budget middleware, prompt conventions (→ `/platform/ai-kit`).
- **Jarvis itself:** memory pipeline, graph, Decision Engine, capability specs, SOP seed set, cadences, integrations scaffolding.
- **Commercial patterns:** design-partner program structure, pricing-architecture method (tiers+usage, COGS dashboard), clean-hands growth doctrine.
- **Security/compliance:** posture, incident ladder, evidence automation, vendor/token registries.

## 2. What is per-startup (the domain adapter `/adapters/<startup>/`)
ICP + anti-ICP · domain ontology/glossary (the new DOC-002 — **never reused**, always rebuilt for the domain; ontology reuse is how you smuggle wrong assumptions) · competitor + legal + source watchlists · metric definitions + NSM · tone/brand guide · data-vendor landscape · compliance specifics · pricing inputs.

## 3. Instantiation SOP (Startup #2, target ≤2 weeks to "Phase-0 complete")
1) New namespace in memory/graph/Langfuse; new repos from scaffolds. 2) Adapter skeleton generated; founder fills ICP/domain seeds. 3) Run the documentation method: roadmap → diligence (research capability executes the DOC-110 playbook against the new domain, same confidence labels, same kill criteria requirement) → decisions ADR-001-equivalents. 4) Engineering kit instantiated only after the diligence verdict is BUILD-class (the factory enforces the discipline that saved Startup #1). 5) Shared-capability review: which Jarvis capabilities serve both startups as-is; conflicts → decision records.
**Gate:** Startup #2 does not begin before AcquisitionOS reaches M5/GA or a deliberate pivot ADR — the factory is sequenced leverage, not parallel distraction.

## 4. Multi-startup posture
Per-startup namespaces everywhere (memory, budgets, dashboards); shared platform versioned — startups pin kit versions and upgrade deliberately (no forced simultaneous migrations); Executive capability gains a portfolio view (per-startup KPIs, capital allocation decisions as Type 1 records).
**Trade-off:** shared infra couples failure domains → mitigations: namespace isolation, per-startup budget hard-stops, and the option (pre-declared) to fork the platform for any startup that outgrows sharing.
