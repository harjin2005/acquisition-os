# Integrations

**Principle:** fewest possible, least privilege, all registered (token registry in Security.md), each with an owner and a freshness monitor (CompanyMemory.md §5).

| Integration | Purpose | Access level | V |
|---|---|---|---|
| GitHub | Repos, PRs, CI events → memory; Claude Code workflows | Repo-scoped tokens | V1 |
| Calendar | Events metadata → cadence + commitments | Read | V1 |
| Email | Founder-selected threads → memory; drafts out via human | Read-selected / draft-only | V1 |
| Meeting transcription | Transcripts → extraction pipeline | Per-meeting | V1 |
| Task tracker (Linear-class) | Epics/tasks sync | Read/write tasks | V1 |
| Stripe | Revenue/wallet data → Finance | Read | V1 |
| Accounting/bank exports | Close pack inputs | Export files | V1 |
| Product metrics API | DOC-120 §12 aggregates ONLY (boundary 1) | Scoped read | V1 |
| Analytics (web) | Growth funnel | Read | V1.5 |
| Langfuse / Grafana | AI + infra observability into briefs | Read | V1.5 |
| Sec scanners (Dependabot, gitleaks) | Security digests | Native | V1 |

**Rules:** no integration writes to external systems without an approval object (and V1 mounts no such tools) · every integration has a revoke runbook · adding an integration = decision record (Type 2) + registry row. **Failure mode:** integration sprawl → quarterly registry review culls unused rows.
