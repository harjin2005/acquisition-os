# Agent rules (path glob: `backend/app/agents/**`)

## Prompt = versioned file

- Prompts live in `backend/app/agents/<name>/prompts/*.md` with frontmatter (`version`, `model`, `changelog`).
- A prompt change **is** an agent-version bump. The PR must include:
  - Updated `CHANGELOG.md` line for the agent.
  - Updated `thresholds.yaml` if a metric target changes.
  - Passing evaluation via `eval-gate.yml` (blocks merge).

## Typed variables only

- System prompts are static templates. Free-form user text (inbound messages, notes) is injected inside a clearly delimited data block, **never** concatenated into instructions.
- The injection eval suite tests adversarial inbound messages attempting to trigger sends or exfiltration.

## No provider SDKs

- Every model call goes through `app.agents.platform.gateway.LiteLLM`. Import-linter blocks `openai`, `anthropic`, `google.generativeai` imports outside the gateway package.

## Tool mounting = trust level

- L1 (Assisted) agents receive read-only tools. Send-capable tools are physically absent from the L1 registry. DOC-120 §8 threat model applies.
- Every tool call re-validates RBAC + tenancy server-side. Trust the token, verify the action.

## Run logging

- Every run logs: `run_id`, `org`, `agent_version`, `prompt_version`, `model`, `token/cost`, `latency`, `tool-call tree`, `output_hash`. Langfuse trace + OTel span.
- 100% sampling in v1. Revisit at scale.
