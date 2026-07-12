# Decision Engine

**Purpose:** decisions are the founder's unit of work. This system makes them explicit, fast, remembered, and enforceable — for humans and AI alike.

## 1. Decision records (ADR system, generalized)
- One register (extends DOC-001 pattern company-wide): ID, question, options considered, evidence w/ confidence labels, decision, rationale, consequences, owner, status (Proposed/Accepted/Superseded), review-by date.
- Classes: **Type 1** (hard to reverse — architecture, pricing, legal posture, hires) require a written record *before* action. **Type 2** (reversible) are logged after, lightweight. Classifying is itself a rule: when unsure, it's Type 1.
- Storage: `/docs/decisions/` in git; indexed into memory; every record links the artifacts it governs.

## 2. Approval objects (the L2 mechanism)
Any capability acting at L2 acts inside a signed approval object: scope, allowed tools, budget (money/tokens/sends), duration, escalation triggers, approver, timestamp. Identical in shape to AcquisitionOS's Campaign object — one pattern, learned once, audited the same way. Approval queue surfaces in the daily brief; approvals are files (git-audited).

## 3. Decision boundaries (global, all capabilities)
Never: external communication without human send · spending outside an approval object · touching product tenant data · modifying ADR status · deleting memory (supersede, never erase — except legal/privacy-driven deletion via SOP).

## 4. Metrics
Decision latency by class · % Type 1 decisions with records before action (target 100%) · reversal rate with reasons (learning signal) · approval-object violations (target 0, alarmed).

## 5. Failure modes
Bureaucracy creep → Type 2 stays one-paragraph, and the register is reviewed for "decisions nobody needed recorded"; rubber-stamp approvals → weekly review samples one approval object for genuine scrutiny; stale review-by dates → aging alarm in brief.
