# Memory Tiers & Session Model

**Purpose:** define how knowledge reaches an AI session — the difference between a platform and a pile of documents.

## Tiers
- **T0 Standing context (always loaded):** MASTER_CONTEXT.md + the session's capability rules. Budget: small by design (<3k tokens). This is why MASTER_CONTEXT is ruthlessly maintained.
- **T1 Retrieved context (on demand):** Company Memory via retrieval tools — pulled, cited, never bulk-pasted. Sessions reference @-paths and query tools instead of inlining documents.
- **T2 Archive:** everything else, reachable by search, never auto-loaded.

## Session lifecycle
Start → T0 loads → task declared → capability skill loads (just-in-time) → work with T1 retrieval → **end-of-session skill writes back**: summary, decisions (to Decision Engine), commitments, artifacts committed. A session that produced material work and wrote nothing back is an unfinished session (Definition of Done, ClaudeCode.md).

## Write-back rules
Only structured write-backs (summary, decision record, commitment, artifact) — no raw transcript dumping. Human confirms extracted decisions/commitments before they bind. Superseding beats editing.

## Anti-patterns (named so they can be policed)
Context stuffing (loading T2 wholesale) · memory hoarding (write-backs nobody retrieves — quarterly curation prunes) · shadow memory (knowledge living in chat history instead of write-backs — the end-of-session hook exists to prevent exactly this).
