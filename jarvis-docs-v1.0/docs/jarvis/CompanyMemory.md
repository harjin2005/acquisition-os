# Company Memory

**Purpose:** institutional knowledge that outlives every tool, session, and employee. Memory is the platform; everything else is logic over it.

## 1. Sources & ingestion (V1 set — each with adapter, cadence, owner)
| Source | What | Cadence |
|---|---|---|
| Git repos (product + founder-os) | Docs, ADRs, PRDs, code structure, PR titles/descriptions, CHANGELOG | On push |
| Meetings | Transcripts/notes → summary + decisions + commitments extracted (human-confirmed before commitments enter memory) | Per meeting |
| Email/calendar | Founder-selected threads + all calendar events (metadata) — *selected*, not firehose: signal over surveillance | Daily |
| Task tracker | Epics/tasks/status | Daily |
| Product metrics | DOC-120 §12 aggregates via product API (aggregates only — Architecture.md boundary 1) | Daily |
| Finance | Stripe + bank/accounting exports | Daily/monthly |
| Research outputs | Briefs from ResearchSystem.md with confidence labels + verified-as-of dates | Per run |
| Claude sessions | Session summaries for material work (skill-generated at session end), not raw transcripts | Per session |
| Customer knowledge | Interview notes, design-partner artifacts, support themes (PII-minimized) | Per event |

## 2. Pipeline
ingest → normalize (one document model: id, source, type, created, author, org/startup namespace, provenance, sensitivity tag) → extract (entities, decisions, commitments, metrics) → link (KnowledgeGraph.md) → index (pgvector embeddings + keyword) → serve (retrieval tools via MCP to any Claude session).

## 3. Retention & versioning
Git-backed artifacts: versioned forever by git. Ingested records: append-only with supersede links; **nothing deleted except via privacy/legal SOP** (then tombstoned with reason). Version history is therefore structural, not a feature.

## 4. Retrieval contract (what every capability can ask)
`search(query, filters)` · `get_entity(id)` with neighbors · `decisions_about(topic)` · `commitments_open(person)` · `timeline(entity)` · `metrics(series, range)`. Each answer carries provenance + freshness; retrieval without provenance is a bug (same receipts doctrine as the product).

## 5. KPIs & failure modes
KPIs: source coverage (all table rows green) · retrieval usage/day · "couldn't find it" rate (founder-reported, target <1/wk) · time-to-onboard a new hire to full context (target: 1 day reading + memory access).
Failure modes: ingestion rot (a source silently stops) → per-source freshness monitors in the daily brief; junk drawer (everything ingested, nothing findable) → sensitivity + type taxonomy enforced at ingest, quarterly curation SOP; secrets in memory → ingest-time secret scanning (gitleaks patterns) with quarantine.
