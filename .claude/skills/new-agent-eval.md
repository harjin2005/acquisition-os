---
name: new-agent-eval
description: Wire up an agent's eval manifest, thresholds, and CI gate.
---

# Skill: New Agent + Evaluation

## Steps

1. Create `backend/app/agents/<name>/` with:
   - `prompts/` — versioned prompt files with frontmatter.
   - `tools.py` — pydantic-typed tools, registered in `agents/platform/tools.py`.
   - `agent.py` — orchestration entry.
   - `CHANGELOG.md` — one line per version bump.

2. Create eval manifest under `backend/app/agents/evals/manifests/<name>.yaml`:

   ```yaml
   agent: <name>
   version: 0.1.0
   dataset:
     s3_uri: s3://acquisition-os-evals/<name>/v1/manifest.json
     hash: sha256:PLACEHOLDER
     metro: dallas
     size: 100
     label_provenance: design_partner_historicals
   thresholds:
     precision: 0.85
     recall: 0.80
     injection_refusal: 1.00
   ```

3. Update `.github/workflows/eval-gate.yml` if the workflow needs a new path filter.

4. Set the online metrics dashboard in Langfuse (linked from `docs/modules/<agent>.md`).

## Gate rules

- Merge is blocked until the eval score meets thresholds AND no metric regresses more than the tolerance in `thresholds.yaml`.
- L1 agents (Prioritization + Underwriting) start with **no send-capable tools**. Adding one requires an ADR.
