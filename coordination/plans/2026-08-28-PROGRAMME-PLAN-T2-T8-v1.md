# Controller Programme Plan — T1 close through T8 — v1 — 2026-08-28

**Status:** CONTROLLER PLANNING REFERENCE. This document plans; it does not authorise. Every paid
tranche below still requires its own durable Controller decision plus explicit user spend approval,
and every frozen contract stays frozen. Where this plan disagrees with a newer durable Controller
decision, the decision wins.

**Grounding:** repo truth on `main` (PROJECT-MEMORY, CONTROL-STATE, the PILOT-001 decision chain,
CANON-013 triage) + the advisory external review at
`coordination/plans/2026-08-28-EXTERNAL-PM-REVIEW-VIDEO-MARKET-2026-08.md` (market prices in it are
reported, not verified; execution-time verification still governs).

## 1. Where we are (evidence, not narrative)

- **T0 done.** Demand pool exists: 18 real buyer cases, 16 runnable, triaged (CANON-011/013).
  8/8 development/holdout split PROPOSED, not frozen.
- **T1 in flight.** PILOT-001 Candidate 1: mechanically perfect (12/12 hard checks), human-rejected
  on creative quality (H1/H4/H6). The single repair (Attempt 2) is dispatched under the superseded
  single-scene prompt. After Candidate 2 there is no repair; its H1–H6 review closes T1 either way.
- **Empirical floor:** 1 benchmark-qualified OCR evaluator; 16 sealed A-TEXT images (7/16 exact);
  temporal machinery unqualified; Registry deliberately 0 rows; ~USD 3.5 total spend + USD 0.80–1.60
  PILOT-001.
- **The one confirmed production lesson (paid for twice):** deterministic composition works
  first-try; text-to-video prompting without a visual anchor is the failure mode. Style adjectives
  and timed choreography are not a visual idea.

## 2. The thesis this plan optimises

The product's viability is decided by **first-pass accept rate per dollar**, not model quality.
Market evidence agrees: the funded competitor that died here (Icon's AI ad-maker) died on creative
acceptance, not on rigor; prosumer T2V accept rates run ~20–35%. The lever that buys accept rate
cheaply is the **keyframe gate**: inspect composition/premium-ness/negative-space on a ~$0.04
still, pay video price only for an accepted look. Veo 3.1's first-frame conditioning is already on
our integrated route — this is a recipe change, not a substrate change.

Unit-economics targets (planning numbers, to be re-based on verified prices):
- ₹99 video → CpAO ≤ ~$0.45–0.50 → cheap plate ($0.32–0.50/8s) × ≤1.3 mean attempts + keyframe +
  mechanical checks. Veo Fast ($0.80/attempt) can only be a premium tier.
- ₹9 image → CpAO ≈ $0.03–0.05 with deterministic overlay — comfortable already.

## 3. Stage plan

### T1 — close PILOT-001 (now)
1. User reviews Candidate 2 (H1–H6). PASS → record acceptance; FAIL → record final rejection;
   either way T1 closes honestly.
2. Write PILOT-001's **fully-loaded CpAO line** (both attempts, all costs) as committed evidence —
   the first real datum for the primary metric.
3. Decide **HED-1 scope for the pilot only** (which human review time counted). Full HED-1 stays
   open until Stage-C scoring, but the pilot line must state what it includes.

### T2 — workflow-then-model screen (next paid tranche; needs user approval)
**One spend envelope: USD 25, 0 retries, one Controller decision + user approval.** Sequenced so
each phase gates the next; abort criteria explicit.

- **Phase 1 — keyframe screen (~$1.5):** 3 briefs × 4 keyframes × 3 image models (candidates:
  Imagen 4 Fast / Nano Banana 2 class / GPT Image 2 low — final roster fixed at authorisation
  after price verification). Human picks winners against frozen visual direction.
- **Phase 2 — plate screen (~$18):** winning keyframe per brief → image-to-video on ~4 routes
  spanning the price spread (Veo 3.1 Fast; Kling turbo-class; Wan 720p; Hailuo 768p) + **one pure
  T2V control per brief**. One attempt per cell.
- **Phase 3 — composite and judge ($0 API):** every plate through the existing deterministic
  P2–P4 pipeline; blind human scoring on the frozen H1–H6-style rubric; metric = first-pass
  accept per dollar, per route, per workflow.
- **Briefs:** Aight (continuity) + **MKT-005** (real buyer, the only exact-text marketplace case)
  + **MKT-012** (purest premium-product-plate test). Cheap add if headroom: **MKT-014**
  (animate a supplied still) as a demand-generalisation probe.
- **Outputs:** (a) image-first vs T2V answer; (b) cheap-plate viability at "premium"; (c) model
  shortlist for T3; (d) re-based ₹99 economics. Product-learning evidence only — no Registry rows.

**Zero-spend T2 prep (can be tasked immediately, no user approval needed):**
- execution-time price sheet for the shortlisted routes only (incl. verifying whether the reported
  "Veo Lite" tier exists) — scoped, not the forbidden broad price refresh;
- parameterize the deterministic composition layer into brand-token templates (fonts/palette/
  safe-areas/endcard as data) — this layer is the proven product IP and the seed of Production IR
  "extracted from successful real recipes";
- mine the public prompting-practice literature into Canon as normal admitted sources (one-scene/
  one-camera doctrine, keyframe planning) — book-knowledge rules apply, never capability evidence;
- demand-to-capability desk map for the 16 runnable cases → which evaluator families a real accept
  gate would call (drives T5 scope).

### T3 — architecture outcome experiment (after T2)
- **Freeze first, then generate:** CANON-013's 8/8 split (freeze, amend or reject), representative-
  deliverable policy, reviewer protocol, decision thresholds, holdout do-not-read rule.
- **Arms: start with 3, not 6** — A (raw prompt), B (strong LLM reasoning), E (Creative IR +
  production intelligence). Canon arms (D/F) run **only if E beats B** — if structured production
  intelligence cannot beat a naked frontier LLM, the Canon question is moot and cheaper to test
  later. This is a proposed amendment to the intended 6-arm design; it is within the revised
  programme's latitude (exact arm implementation was explicitly deferred to protocol-freeze time)
  and will be fixed in the T3 protocol-freeze decision.
- Run on the frozen development set using the T2-winning workflow/routes. Blind external review
  where feasible (see micro-panel below).

### T4 — keep/kill (merged into the T3 readout)
A decision meeting on T3 evidence, not a stage: which architecture components demonstrably raise
accept-per-dollar. Kill what doesn't. No standalone machinery.

### T5 — targeted eval lab (demand-driven only)
Qualify only the evaluators the runtime accept gate will actually call, chosen from the
demand-to-capability map — not the full 44-capability contract. Registry admission bar unchanged;
rows only from qualified/deterministic instruments. **External-reviewer micro-panel** (3
target-audience reviewers scoring T2/T3 batches on the frozen rubric, $0–20) tests whether founder
acceptance tracks customer acceptance (ASSUMPTIONS §13) and whether a future VLM-judge has stable
ground truth to qualify against.

### T6 — runtime v0
Productise the T4-winning recipe: request → keyframe gate → plate → deterministic brand-token
composition → mechanical checks (+ benchmark OCR where text) → batch/spot-check human gate.
Production IR is extracted from the recipes that actually won, not designed in the abstract.
Full HED-1 must be decided here (per-unit founder review does not scale at ₹99). Provider hedge:
one fal.ai standby smoke call (~$1) and route-neutral recipe records (Sora's API death is the
cautionary datum).

### T7 — untouched holdout
The frozen 8-case holdout, run end-to-end on runtime v0 vs the strongest simple baseline (arm B).
Known dependency accepted at split-freeze time: two holdout cases need a planning object and one
needs subject-matter human review.

### T8 — ship decision
Ship / simplify / research more / stop, on holdout accept-per-dollar. **Added gate: at least one
non-founder acceptance** of a marketplace-shaped outcome — we do not ship a product tuned to one
person's taste.

## 4. Standing constraints (unchanged by this plan)

No Planner before Registry evidence · no Registry rows without qualified instruments · admission
bar never weakened · sealed evidence never regenerated · exact-text imperfection never a global
stall · every text result names its standard · one call = one trial, 0 retries default ·
execution-time price verification before every paid tranche · spend beyond approved envelopes
needs explicit user approval · cancelled work stays cancelled.

## 5. Risk register (top 5, with light mitigations)

1. **Accept-rate wall (H1/H6).** Mitigation: keyframe gate everywhere; log every accepted plate's
   prompt/keyframe as a reusable pattern.
2. **Unit economics under water on premium plates.** Mitigation: T2 measures accept-per-dollar on
   cheap plates; ₹99 is a hypothesis T2 reprices, not a commitment.
3. **Demand mismatch** (pool skews identity/avatar/supplied-asset; plate+overlay serves a slice).
   Mitigation: MKT-014 probe inside T2; T3 development set spans the demand shapes.
4. **Provider churn** (Sora dead; `-preview` ids). Mitigation: route-neutral recipes, fal standby,
   execution-time verification.
5. **Single-human accept gate.** Mitigation: external micro-panel from T2 onward; HED-1 decided
   before runtime v0.

## 6. Immediate Controller queue

1. Candidate 2 human review → T1 closure decision (record outcome + pilot CpAO line).
2. Task the four zero-spend T2 prep items.
3. T2 authorisation decision (USD 25 envelope) → user approval → execute screen.
4. CANON-013 split freeze decision (before any T3 media).
