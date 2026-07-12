# AcquisitionOS docs

This is the **source of truth for Claude Code context**. Everything in `product/` mirrors the top-level DOC-000..131 files and is committed to the repo alongside the code so it stays version-locked with the implementation.

## Contents

- `product/` — mirrors of the company / product / engineering docs (read-only).
- `adr/` — Architecture Decision Records; new ADRs go here.
- `modules/` — per-module READMEs (spec ↔ implementation contract).
- `runbooks/` — on-call procedures (send-path incident, feed-gap, restore drill).

## How Claude Code sees this

`CLAUDE.md` at the repo root references these paths with `@`-prefixed pointers so context stays lean and the docs stay authoritative.

## How humans update these

- **DOC-000..131 changes** flow through the DOC process at the top of the repo, then are mirrored here via CI (Sprint 2+).
- **ADRs** are added directly here. Every architectural change ships in the same PR as an ADR.
- **Module READMEs** update in the same PR as any change to the module's interface.
