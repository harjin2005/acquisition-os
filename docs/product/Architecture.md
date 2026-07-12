# Jarvis Architecture

**Owner: Founder/CTO · Status: V1 buildable**

## 1. The layered model

```
┌─────────────────────────────────────────────────────────┐
│ L5  FOUNDER INTERFACE                                    │
│     Claude Code / Cowork sessions · daily brief ·        │
│     dashboards · approval queue                          │
├─────────────────────────────────────────────────────────┤
│ L4  CAPABILITIES (13, Capabilities.md)                   │
│     Executive · Product · Engineering · AI Platform ·    │
│     Knowledge · Research · Growth · Sales · CS ·         │
│     Finance · Legal · Operations · Security              │
├─────────────────────────────────────────────────────────┤
│ L3  DECISION ENGINE (DecisionEngine.md)                  │
│     ADR system · approval objects · maturity ladder ·    │
│     decision latency tracking                            │
├─────────────────────────────────────────────────────────┤
│ L2  COMPANY MEMORY (CompanyMemory.md / Memory.md /       │
│     KnowledgeGraph.md)                                   │
│     ingestion → normalize → link → index → retrieve      │
├─────────────────────────────────────────────────────────┤
│ L1  AI PLATFORM (AIPlatform.md)                          │
│     model gateway · tool registry · eval harness ·       │
│     budgets — EXTRACTED from AcquisitionOS, not rebuilt  │
├─────────────────────────────────────────────────────────┤
│ L0  INTEGRATIONS (Integrations.md)                       │
│     GitHub · calendar · email · Stripe · analytics ·     │
│     meeting transcripts · task tracker                   │
└─────────────────────────────────────────────────────────┘
```

## 2. Physical form (V1 — deliberately boring)

- **`founder-os` monorepo**: `/docs` (this system + all company docs, git-versioned = version history for free), `/memory` (ingestion pipeline + index config), `/capabilities/<name>/` (SOPs, prompts, skills per capability), `/.claude` (rules, skills, agents, hooks per ClaudeCode.md), `/platform` (extracted shared packages, V2+), `/adapters/acquisition-os/` (domain adapter #1).
- **Memory store**: same boring stack the company already runs — Postgres + pgvector for the memory index, S3 for artifacts, Meilisearch optional. One small ingestion service (Python, scheduled jobs). No new databases, no new vendors. Rationale: operational surface ≈ zero; the team is 1–5 people.
- **No Jarvis web app in V1.** The founder interface is Claude Code/Cowork over the repo + memory tools (MCP), plus a static daily-brief markdown generated on schedule. A dashboard app is V2, and only if the brief proves insufficient. Trade-off accepted: less shiny, dramatically less to maintain.

## 3. Hard boundaries (non-negotiable)

1. **Jarvis never touches AcquisitionOS tenant data.** Customer PII, leads, conversations stay in the product under its RLS/compliance regime. Jarvis ingests only aggregates, metrics, and the company's own artifacts. Rationale: DOC-503/504 obligations must not leak into an internal tool with looser controls.
2. **Jarvis inherits the product's security posture** where it stores anything sensitive (secrets in AWS SM, least-privilege integration tokens, audit on approval actions). See Security.md.
3. **Every capability is replaceable** behind its spec; every memory record carries provenance; every automated action carries an approval object or an L-level justification.

## 4. Why this architecture

- *Memory-centric* because capability logic is cheap and changes weekly; institutional knowledge is expensive and must outlive every tool choice.
- *Extraction over abstraction* because platform code speculatively built for "any startup" is how founders build frameworks instead of companies. AcquisitionOS pays for the components; Jarvis harvests them once proven (ImplementationRoadmap.md V3).
- *Claude-Code-native* because the founder's real interface is already an agentic session; Jarvis makes every session start smart (MASTER_CONTEXT.md) instead of building parallel chat UX.

**Trade-offs register:** repo-as-database limits concurrent non-technical users (acceptable: team ≤5) · git versioning of docs beats a wiki's editing UX for auditability but loses WYSIWYG (accepted) · single memory index couples startups' infra in the factory model (mitigated: per-startup namespaces, StartupFactory.md §4).
