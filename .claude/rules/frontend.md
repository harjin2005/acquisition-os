# Frontend rules (path glob: `frontend/**/*.{ts,tsx,js,jsx}`)

## Data access

- **SDK-only.** No hand-written `fetch(...)` calls. Every server interaction goes through the generated TS SDK in `packages/sdk-ts` (Sprint 3+; Sprint 1 has a thin hand-written shim under `frontend/src/lib/api.js` that will be replaced).
- Server state = TanStack Query, keyed by `[org_id, resource, ...args]`.
- Local UI state = one small Zustand slice. **No Redux.**

## QueryBoundary states

- Every route must handle empty / loading / error via the shared `<QueryBoundary>` component (built in Sprint 4 with the Receipts kit).
- Compliance blocks use the "why + fix-path" pattern — the user sees the reason and the next action.

## Receipts kit (DOC-121 mandate)

- The Receipts drawer, confidence band, freshness stamp, and evidence list are built **once** in `frontend/src/components/receipts/*` (Sprint 4).
- All three agents reuse the same components. If you find yourself duplicating a receipts element, stop and add it to the kit instead.

## Accessibility

- WCAG 2.1 AA. Keyboard-first for pipeline/inbox — VA power users.
- Axe checks run in Playwright.

## Design system

- Tailwind + Radix primitives. Do not introduce a new UI library without an OSS-table entry.
- No inline styles outside genuine one-offs. If a style repeats, extract a class.
