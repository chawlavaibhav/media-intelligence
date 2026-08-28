# Controller Brief — CANON-013

**TASK:** CANON-013
**STATUS:** completed

**HUMAN SUMMARY:** All 16 runnable marketplace cases were triaged for the later architecture experiment, and an honest 8-development / 8-holdout split **is achievable** — it is proposed here, not frozen. The most important learning: "runnable" and "usable in an experiment" are very different things. Four of the 16 cases that look runnable on paper are operationally heavy for reasons that have nothing to do with fixtures: two (the ten 3-minute videos and the 48 lecture videos) need a long-form planning object the project has not built, one (the 75–100-scripts-a-week contract) has a stated acceptance condition — sustained throughput — that the project's measurement system cannot express at all, and one (the Thomas & Anna series) entangles more hard capabilities than any other case in the bank. No fixture is a hard blocker: everything missing is authoring work, with one exception worth knowing about — the edit case needs a **base video** to edit, and how that video gets made (assembled from held material, rendered, or generated, which would need spend authorisation) is genuinely unresolved. The split is balanced by burden, length, people-vs-product, speech, identity type and commercial objective — not easy-8/hard-8 — but ten mechanisms exist in exactly one case each, so perfect balance is impossible; every one of those placements is listed with its consequence. The decision needed from you is to freeze, amend, or reject the proposed split.

**WHAT I DID:** Read the full CANON-011 brief bank (all 18 cases) plus the CANON-011 integration decision and the revised-programme decision, and verified mechanically that exactly 16 cases carry `runnable_now: true`. For each of the 16 I extracted, from committed bank evidence only, the fourteen triage dimensions the task names (deliverable count, duration, modality, speech, people, identity, fixtures and their status, reducibility, production dependencies, acceptance, confounds, burden class and its reason). I then built the split by pairing cases that exercise the same mechanism and placing one in each set, and by placing singleton mechanisms according to a stated rule: build-against mechanisms to development, generalisation tests to holdout. Zero generations, zero spend, no model quality inferred from the roster.

**OBSERVED:**
- 16 of 18 bank cases are `runnable_now: true` (verified by scan); MKT-015 and MKT-016 are excluded by the bank itself.
- No fixture on any of the 16 carries `blocks_runnable: true`.
- Burden distribution: 5 low (MKT-005, 009, 010, 012, 014), 7 medium (MKT-001, 002, 008, 011, 013, 017, 018), 4 high (MKT-003, 004, 006, 007).
- The bank records two coverage holes that land directly on triaged cases: content-fidelity-to-a-document (CO-01, MKT-004's central acceptance) and throughput-as-acceptance (CO-02, MKT-007's stated success criterion). Neither is measurable by any capability in Capability Contract v2.
- MKT-002 is the only case with a real customer unit price ($30–45 per approved video) — the only place CpAO can be computed against a real price.
- Nothing in `canon/research/marketplace-demand-v1/` changed between the task's base SHA (`719c90f`) and current main (`2995b44`); only Controller authorisation commits intervened.

**INFERRED:**
- The 8/8 split is achievable **without changing any buyer intent** — every reduction used (batch slices, representative deliverables) is a fixture the bank itself already declares. Neither stop condition triggered.
- Burden is driven far more by duration/assembly structure and judgement cost than by fixture availability. The cheap-looking cases ($150 for ten videos, $20 per lecture) are the heaviest; the well-paid single ads are the lightest.
- The edit case's base-video fixture (FX-013-basevideo) is the only fixture whose construction *method* is unresolved and could raise an authorisation question later (if generation were the only practical way to author it). Flagged as "unknown", not as a blocker.

**SURPRISES / BELIEF UPDATES:**
- The inversion between price and feasibility: the marketplace's cheapest jobs are structurally the hardest for this project, because they are volume/long-form work that requires planning, while premium single ads are the most attemptable. Do not equate "low budget" with "easy pilot case".
- The bank's two recorded coverage holes are not abstract: they are the *primary* acceptance conditions of two of the 16 cases. A lecture video that teaches the wrong material would pass every contract capability.
- The only case whose measurement is nearly free (MKT-013's deterministic preservation check) is also the only case whose key fixture might itself need a generation call. Cheap to judge, unresolved to stage.

**FAILURES / BLOCKERS:** None for this task. Two forward-looking flags (not blockers to freezing the split): MKT-003 and MKT-004 in holdout cannot be attempted end-to-end until a segmentation/assembly planning object exists, so the final product test inherits that dependency; and MKT-004's central acceptance will require subject-matter human review under frozen criteria because no instrument family covers it.

**UNKNOWN / NOT VERIFIED:**
- How FX-013-basevideo would actually be constructed (assembly from held rights-cleared material vs synthetic render vs generation). Matters because the last option needs spend authorisation.
- Real per-video durations for the five cases where the buyer stated none (MKT-006, 008, 009, 011, 018) — the envelope fixtures stand in; the true jobs could be materially larger.
- Whether the arms A–F experiment will run every case in both sets at full declared cardinality or use the representative-deliverable reductions recorded in the triage; that protocol decision is the Controller's, at freeze time.

**ASSUMPTIONS CHALLENGED:** none from `coordination/ASSUMPTIONS.md` directly; the triage adds evidence to the bank's existing observation (CO-03) that cross-asset identity is heavily load-bearing — it is the primary acceptance condition in three development-relevant cases.

**LOCAL IMPLICATIONS:** Canon now has, for the first time, a feasibility-ordered view of the marketplace pool: which cases can seed early arms-A–F work cheaply (MKT-012/014-class shapes are in holdout deliberately, so the cheapest *development* entry points are MKT-005 and MKT-009), and which will need staging investment before they can run (MKT-006's four fixture families, MKT-002's eight-product photography pack).

**CROSS-STREAM IMPLICATIONS (CROSS_STREAM — proposed, not acted):**
- **Eval:** the two coverage holes (CO-01 content fidelity, CO-02 throughput) will bite the architecture experiment exactly where the triage says; if either case is to be *scored* rather than purely human-reviewed, Eval needs a decision on how.
- **Resources:** if the split freezes as proposed, the development set's fixture load is concentrated in MKT-006 (character sheets, voice samples, dashboard recordings) and MKT-013 (base video). Fixture construction is not authorised by this task and would need its own tasking.

**ARCHITECTURAL IMPLICATIONS:** none new — the triage *confirms* the known gap (no Production IR / planning object) and makes its cost concrete: it is the single reason four cases are burden-high. No stop was required because nothing here needs a new IR field; the gap is already on record.

**DECISIONS NEEDED FROM CONTROLLER:**
1. **Freeze, amend or reject the proposed 8/8 split** (`proposed-brief-split.yaml`). Freezing enables the architecture-experiment protocol design; amending is cheap now and expensive after media exists.
2. **Rule on the two holdout flags:** keep MKT-004 in holdout accepting human-only judgement of its core acceptance, or swap it; accept that MKT-003/004 make the final test planner-dependent.
3. **Decide the holdout access rule:** the split file proposes that post-freeze task Context Contracts name the holdout ids as do-not-read. Only a Controller decision can make that binding.

**EVIDENCE WORTH HUMAN INSPECTION:**
- `proposed-brief-split.yaml` — the `unbalanceable_dimensions` section is the honest core of the proposal: ten singleton mechanisms and where each went. Check whether you agree with the placement rule before freezing.
- `marketplace-feasibility-triage.yaml` — the `looked_runnable_but_operationally_heavy` table, if you read only one thing.

**FILES CREATED / MODIFIED:**
- `canon/experiments/architecture-outcome-v1/marketplace-feasibility-triage.yaml` (new)
- `canon/experiments/architecture-outcome-v1/proposed-brief-split.yaml` (new)
- `canon/experiments/architecture-outcome-v1/CANON-013-CONTROLLER-BRIEF.md` (new — this file)

**RECOMMENDED NEXT STEP:** Controller reviews and freezes the split (gate 2 in CONTROL-STATE), then commissions the architecture-experiment protocol (arm implementations, reviewer protocol, decision thresholds) against the frozen development list — and, separately, a fixture-construction task for the development set's two heavy kits, since no development case can generate media before its fixtures exist.

**EPISTEMIC CHECK:** Every buyer fact above traces to the committed CANON-011 bank; burden ratings and the split are labelled as this worker's inference/proposal throughout; unknowns are stated as unknown (fixture construction method, true durations); route vocabulary was used to name dependencies only, and no model capability was inferred from the roster; no unapproved decision is presented as fact — the split is explicitly PROPOSED_NOT_FROZEN.

**CONFIRMATION:** No unapproved next strategic step was started. No media was generated, no model was run, no fixture was created, no bank file was modified, and the proposed split is marked not frozen.
