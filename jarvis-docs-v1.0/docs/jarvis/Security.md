# Security Capability (Jarvis scope)

**Purpose:** Jarvis and the company's internal surface inherit the product's security posture — one standard, no soft underbelly.

**Responsibilities:** dependency audit digests (product + founder-os repos; criticals immediate) · secret hygiene (scanning on all repos incl. memory ingestion quarantine, rotation calendar) · integration token registry (least-privilege scopes, owner, review date — joined with the vendor register) · incident response SOP (severity ladder shared with product; SEV-1 definitions include memory-store exposure and approval-object violations) · SOC 2 evidence automation assistance (Engineering owns controls; Jarvis assembles evidence packs on schedule) · privacy operations for company data (interviewees' PII minimization; deletion SOP — the one sanctioned memory deletion path) · access reviews (quarterly script output → founder sign-off, filed as evidence).
**Inputs:** scanners, advisories (ResearchSystem), audit logs. **Outputs:** digests, incident records, evidence packs, review reports. **Memory writes:** all incidents + postmortems (the never-again file).
**Approval rules:** L1→L2: automated *detection* is L2 (runs standing); any *remediation* beyond dependency-bump PRs (which still require human merge) is human.
**Decision boundaries:** Jarvis never holds product tenant data (Architecture boundary 1) · no security exceptions without a decision record with expiry.
**Failure modes:** alert fatigue → same page-vs-digest policy as DOC-130 §7; evidence scramble at audit → evidence packs assembled monthly, not annually.
**KPIs:** critical CVE time-to-triage <24h · secrets incidents: 0 · access reviews on schedule: 100% · audit evidence assembly time.
