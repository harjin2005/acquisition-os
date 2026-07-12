# Jarvis AI Platform

**Purpose:** one AI substrate for company-internal capabilities — extracted from AcquisitionOS, not duplicated.

## Components (source: product repo → `/platform` packages, V3 extraction per roadmap)
- **Model gateway:** the product's LiteLLM config pattern; per-capability budgets (same middleware); routing by task class. Until extraction, Jarvis uses its own thin LiteLLM instance with copied config — duplication accepted for ≤2 quarters (debt, tracked).
- **Tool registry:** typed tools with per-capability, per-maturity-level mounting — L1 capabilities get read tools only; L2 adds act tools bound to approval objects. Identical enforcement pattern to the product (tools refuse what policy forbids; prompts are advisory, tools are law).
- **Prompt library:** `/capabilities/*/prompts/` versioned with changelogs, exactly the product's convention.
- **Evaluation:** the product's eval-runner pattern applied to internal capabilities where outputs are checkable: research briefs (spot-verification sampling), brief usefulness labels (FounderOS loop), extraction precision (decisions/commitments vs human confirmation). Not everything internal gets evals — only where a measurable signal exists (principle: measurable or L0/L1).
- **Observability:** Langfuse project per startup namespace; cost per capability in the monthly review.
- **Safety:** ingested external content (research pages, emails) is untrusted input — same injection posture as the product: delimited data blocks, no instruction concatenation, act-tools never mounted in sessions that read raw external content without an approval object.

## Registry rule
Every agent/capability instance is registered (name, level, tools, budgets, owner, kill switch). Unregistered automation is a policy violation — this file's table *is* the agent registry.
