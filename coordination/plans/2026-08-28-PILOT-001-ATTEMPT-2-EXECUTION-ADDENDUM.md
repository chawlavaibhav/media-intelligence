# PILOT-001 — Attempt 2 Execution Addendum (Final Repair)

**Date:** 2026-08-28
**Status:** EXECUTION PACKET for the single authorised repair. No new authority is created here.
**Governing decision:** `coordination/decisions/CONTROLLER-PILOT-001-CANDIDATE-1-REJECTION-AND-REPAIR-2026-08-28.md`
**Spend authority (unchanged):** `coordination/decisions/CONTROLLER-PILOT-001-SPEND-AUTHORISATION-2026-08-28.md` — USD 2.00 hard cap, 0 retries.
**Base runbook:** `coordination/plans/2026-08-28-PILOT-001-KEY-BEARING-EXECUTION-RUNBOOK.md`

## Why this addendum exists

The base runbook was written before Candidate 1 was human-rejected. Two of its parts are now
superseded by the newer rejection-and-repair decision, which governs:

1. **The runbook's "Provider prompt — frozen" section is superseded.** Attempt 2 must use the
   frozen repair prompt in the rejection-and-repair decision (the concrete "one source product →
   two media outcomes" commercial scene), verbatim, with no creative rewriting after seeing the
   result.
2. **The runbook's "Repair" section is now resolved.** The Controller disposition exists:
   Candidate 1 is REJECTED (H1/H4/H6 FAIL), the defect is provider-origin, and the single repair
   is one final provider generation. Attempt 2 is that repair. Attempt 3 is forbidden.

Everything else in the base runbook (credential handling, preflight P0.2–P0.6, deterministic
brand/claims/endcard pipeline, hard checks, RES-007 recording, stop conditions, completion
response format) applies to Attempt 2 unchanged.

## Ordered steps for the key-bearing worker

1. **Update the execution branch onto current main.** `work/pilot-001-aight-execution` currently
   sits on pre-rejection main. Merge current `main` into it (do not rebase the pushed branch) so
   the rejection-and-repair decision is present in the working tree. Preserve all Attempt 1
   evidence bytes and records unchanged.
2. **Record the Candidate 1 rejection durably** in the RES-007 journey before or together with
   Attempt 2 evidence: rejected; H1 FAIL, H4 FAIL, H6 FAIL; H5 and deterministic brand rendering
   PASS; reviewer feedback preserved concisely. Do not modify the pre-acceptance archive bytes of
   Candidate 1 — supersede, never mutate.
3. **Preflight** exactly as the base runbook P0.2–P0.6: `GEMINI_API_KEY` present (else
   `STOP — GEMINI_API_KEY_MISSING`); provider contract/model/price reverified against official
   documentation; local `authorization.pilot.local.yaml` materialised, never committed; pinned
   Aight brand source verified.
4. **Open the SAME persistent run** `pilot-001-aight-2026-08-28`. Verify it reconstructs
   USD 0.80 committed / USD 0 pending before any new reservation. Never create a second run to
   reset spend.
5. **Reserve USD 0.80** under a new stable cost_ref, then dispatch **one** provider call:
   direct Gemini Developer API, `veo-3.1-fast-generate-preview`, 8 s, 9:16, 720p, using the
   frozen repair prompt from the governing decision. One request = one attempt = one trial;
   0 retries; no third call under any condition.
6. **Compose deterministically** with the exact accepted Candidate 1 deterministic layer
   (wordmark source, `Image ₹9`, `Video ₹99`, endcard, `Outcome API`, `getaight.ai`, stripped
   audio, 12 s assembly). Placement may be mechanically adjusted only to preserve legibility
   against the new plate; typography is not redesigned.
7. **New immutable identities** for everything in Attempt 2: attempt id, trial id, cost_ref,
   request config/hash, provider artifact, final Candidate 2 artifact, lineage. Candidate 1
   files are never overwritten.
8. **Run the hard checks**, persist durable evidence on `work/pilot-001-aight-execution`, push,
   and return Candidate 2 for the final human H1–H6 review using the runbook's completion
   response format. **Do not record acceptance.** After Candidate 2 there is no repair left:
   human PASS closes T1 with an accepted outcome and available CpAO; human FAIL closes T1 as a
   bounded, fully-evidenced product/integration failure.

## Environment note

Attempt 1 ran on the key-holder's local machine, where the git-ignored spend run and
`GEMINI_API_KEY` live. Attempt 2 must run in that same environment (or one that can genuinely
reconstruct the same persistent run). A session without the key stops at P0.2; it must not
substitute a route or simulate a dispatch.
