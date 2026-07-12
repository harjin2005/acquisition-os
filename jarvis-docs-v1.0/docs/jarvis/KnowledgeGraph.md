# Company Knowledge Graph

**Purpose:** link memory so questions like "what did we decide about pricing, based on which evidence, and what depends on it?" are one query, not an archaeology dig.

## Ontology (company domain — deliberately small; grow only under pressure)
**Nodes:** Person · Organization (startup/customer/vendor/competitor) · Document · Decision · Commitment · Meeting · Metric · Risk · Task/Epic · Capability · Artifact(code/release).
**Edges (typed, temporal where state changes):** DECIDES(person→decision) · EVIDENCED_BY(decision→document) · GOVERNS(decision→artifact/doc) · SUPERSEDES(decision→decision) · COMMITS(person→commitment) · DISCUSSED_IN(x→meeting) · OWNS(person→risk/task/capability) · MEASURES(metric→capability/OKR) · DEPENDS_ON(task→task) · ABOUT(document→org/topic).

## Implementation
Edges-as-tables in the same Postgres as the memory index (identical pattern to the product's derived layer — one skill, two uses). Extraction: deterministic where possible (git links, calendar attendees), LLM-assisted with human confirmation for decisions/commitments. No Neo4j unless traversal depth proves it (same rejection + re-entry criteria as ADR-010).

## The queries that justify its existence (acceptance tests)
"Open commitments by person" · "decisions lacking evidence links" · "everything governed by ADR-010" · "what changed since the last board pack" · "orphan risks (no owner)". If these five queries aren't used monthly, the graph is over-built — review it.
