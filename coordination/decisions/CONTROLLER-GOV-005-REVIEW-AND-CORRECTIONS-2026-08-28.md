# Controller Review of GOV-005 — Sync Required; Evidence Persistence and Authority Ambiguities Resolved — 2026-08-28

## Status

**GOV-005 FINDINGS ACCEPTED AS REPOSITORY-COHERENCE FINDINGS. RETURNED GOVERNOR BRANCH MUST SYNC TO CURRENT MAIN BEFORE MERGE.**

Returned Governor branch:
- `work/gov-005-post-emp-001-coherence-review`
- audited main: `0e24d6a1a4acce5e83b90fa7fe198db94a92dec5`
- current main at Controller review: `28c8477a5f7c5fd7df1642bdc10a24cd1df439ce`

The Governor correctly stayed within governance scope and did not adjudicate scientific method.

However, six Controller commits landed after its audited base. Its current-state prose is stale on arrival:
- EVAL-028 is now superseded and must NOT run;
- exact text is a non-blocking measured capability;
- EVAL-029 is the active text-evaluator lane;
- EVAL-024 returned zero live spend and now has a cleanup/sync gate before live generation.

Therefore the review is accepted in substance but not merge-ready until refreshed against current main.

## Disposition of GOV-005 findings

### F-1 — live EMP-001 evidence absent from main

**ACCEPTED AS HIGH AND MUST BE FIXED.**

Standing architecture:
- the live mutable spend ledger remains gitignored/local during execution;
- completed experimental evidence must be sealed immutably into GitHub after a bounded run/screen completes.

A sealed evidence package must be sufficient for a fresh session to:
- recompute reported metrics from observations;
- inspect false-pass/false-fail item identities;
- verify candidate/config identity and qualification contract;
- trace costs to a ledger snapshot/cost refs;
- verify the snapshot's relation to the live run without exposing credentials.

Do NOT commit:
- API keys/tokens;
- auth headers;
- secrets;
- mutable local state merely because it exists;
- provider artifacts whose redistribution rights prohibit it.

For EMP-001 qualification, full text/evaluator observation records and immutable cost/evidence snapshots are expected to be small enough for Git.

Open a bounded Eval evidence-persistence correction after current active Eval work is safely isolated.

### F-2 — stale `eval/HANDOFF.md`

**ACCEPTED.**

It must be refreshed by Eval because it currently says no API/model call has happened and no spend was approved.

This can be combined with the evidence-persistence correction.

### F-3 — WORKSTREAM-STATUS stale

**ACCEPTED; Governor correction is appropriate.**

Refresh again against current main before merge because EVAL-028/EVAL-029 changed after the audit base.

### F-4 — duplicate EVAL-024 and CANON-011 authorities

**RESOLVED BY THIS DECISION.**

#### EVAL-024 authoritative chain

Current governing authority is:

1. `coordination/decisions/CONTROLLER-EVAL-024-READINESS-CLEANUP-AND-LIVE-2026-08-28.md`
2. `coordination/decisions/CONTROLLER-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md`
3. `eval/tasks/EVAL-024-PARALLEL-ATEXT-GENERATION-ONLY.md`

Historical/superseded duplicates:
- `coordination/decisions/CONTROLLER-EMP-001-PARALLEL-ATEXT-GENERATION-ONLY-2026-08-27.md`
- `eval/tasks/EVAL-024-ATEXT-GENERATION-ONLY.md`

The historical files remain preserved but are not governing instructions.

#### CANON-011 authoritative chain

Current governing authority is:

1. `coordination/decisions/CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PREP-2026-08-27.md`
2. `canon/tasks/CANON-011-MARKETPLACE-DERIVED-BRIEF-BANK.md`
3. source provenance under `canon/research/marketplace-demand-v1/README.md`

Historical/superseded duplicates:
- `coordination/decisions/CONTROLLER-MARKETPLACE-DERIVED-BRIEF-PROMPT-PREP-2026-08-27.md`
- `canon/tasks/CANON-011-MARKETPLACE-DERIVED-BRIEF-PROMPT-BANK.md`

Reason: the later pair explicitly binds the committed marketplace-source provenance and preserves the route-neutral brief -> prompt-ready-envelope separation.

### F-5 — DECISION-LOG incomplete

**ACCEPTED, BUT DO NOT HAND-MAINTAIN IT AS A CLAIM OF EXHAUSTIVE DISCOVERY.**

Controller decision:
- `coordination/DECISION-LOG.md` is a curated historical/navigation index, not the exhaustive source of post-26-Aug decisions.
- Current authorisation is discovered from `coordination/CONTROL-STATE.md`.
- Durable detailed decisions are discovered directly under `coordination/decisions/` plus stream-owned durable decision records referenced by Controller state.
- PROJECT-MEMORY must not tell a fresh session that DECISION-LOG is exhaustive.

A future mechanical index may replace this, but no manual 30+ row transcription is required now.

### F-6 — frozen v2 contracts still say NOT IN FORCE

**ACCEPTED AS MEDIUM.**

The adopted/frozen status is established by Controller decision and CONTROL-STATE, but generated artifacts carrying stale `NOT_IN_FORCE` status are misleading.

Open a bounded Eval correction to update the generating source(s), regenerate affected v2 artifacts, and prove semantic content unchanged except status/authority metadata.

Do not hand-edit generated YAML.

### F-7 — preflight absolute paths

**ACCEPTED.**

Fix generator/output to store repository-relative or machine-neutral paths for committed preflight evidence.

### F-8 — hand-maintained prior-spend default

**ACCEPTED.**

Remove/derive the stale planning default from the persistent run/evidence input rather than manually updating a number.

This must not alter the live budget guard, which already reads the ledger.

### F-9 — EVAL-024 perceptibility reserialization

Already handled by:
- `CONTROLLER-EVAL-024-READINESS-CLEANUP-AND-LIVE-2026-08-28.md`

The EVAL-024 worker must restore that file byte-for-byte from current main.

### F-10 — numbering gaps

No action. Task-number continuity is not an invariant.

## Current exact-text state the Governor must reflect

The human-confirmed EVAL-028 direction was superseded after the Governor's audited base.

Current authority:
- `coordination/decisions/CONTROLLER-EXACT-TEXT-NONBLOCKING-BENCHMARK-THRESHOLD-2026-08-28.md`
- `eval/status/EVAL-028-SUPERSEDED-2026-08-28.md`
- `eval/tasks/EVAL-029-BENCHMARK-GRADE-TEXT-OCR.md`

Current product/science split:
- strict zero-false-pass exactness results remain valid historical research;
- exact-text is NOT a global programme blocker;
- benchmark-grade OCR may be qualified at the separate bounded-error thresholds;
- no mandatory human-in-loop production architecture;
- unrelated Stage-A/evaluator work may proceed independently.

## GOV-005 merge gate

Before returning GOV-005 for merge, Governor must:

1. integrate current `origin/main`;
2. preserve the original GOV-005 review's audit base and findings as historically accurate for `0e24d6a`;
3. add a short Controller-disposition/update section rather than rewriting what the audit observed at that historical base;
4. refresh PROJECT-MEMORY, WORKSTREAM-STATUS and governance README to current main;
5. replace EVAL-028-as-active with EVAL-029/current exact-text posture;
6. reflect EVAL-024's returned zero-live-spend cleanup gate;
7. mark F-4 resolved by this decision;
8. reflect DECISION-LOG as curated/non-exhaustive, not an exhaustive index;
9. keep F-1 unresolved until Eval seals completed evidence;
10. do not edit domain-owned Eval/Canon/Resources artifacts.

Push the synced Governor branch.
Do not merge.
Return exact head and final diff to Controller.
