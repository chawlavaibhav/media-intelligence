# AUDIT-2026-09-10 — media-intelligence
## Auditor report and Controller rollout plan

**Audit posture:** read-only. No provider spend, no model call, no cloud action, no modification of sealed `eval/experiments/**`, no PR, no commit.

**Repository state audited:** `main` at merge commit `dcfa6af1064b55761b89be29ef5ae22710fdd4cf` (PR #93).

**Important namespace clarification:** EVAL-041 / EVAL-042 / EVAL-043 are the successive Capability Lab integration PRs (#91 / #92 / #93). The sealed empirical evidence is stored under `eval/experiments/EVAL-040/**`. They are not four independent experiments.

---

# 1. Executive verdict

## Current state

The project has crossed the line from “research architecture” into a **real empirical capability system**:

- sealed provider evidence exists;
- the execution harness exists;
- provider adapters exist for image, video and audio routes;
- spend/reservation ledgers exist;
- deterministic instruments exist;
- Registry v1 contains 575 deterministic rows;
- a tiered routing evidence map contains 61 cells and RR-1..RR-16;
- price pins and a generated Stage-A package exist;
- Canon has 37 accepted sources, 1,300 SourceKnowledge objects, 2 compiled packs and CANON-GATE-001.

But it has **not** crossed the line into a production-ready autonomous media-intelligence system.

The public-release blockers are not “we need more research.” They are:

1. clean the experimental-accounting defects in the human routing tier;
2. prove reproducibility of the current HEAD locally;
3. establish condition envelopes for the handful of routes the first runtime will actually use;
4. build the missing runtime / Production IR / Planner path;
5. measure accepted outcomes and CpAO on real demand;
6. operate a private alpha with human release approval;
7. only then remove the human gate.

**Overall public-release verdict: NOT READY.**

**Private human-supervised alpha verdict: achievable after audit closeout + runtime vertical slice.**

---

# 2. Findings — ordered by severity

## F-01 — CRITICAL — one-call/one-trial semantics were violated

**Fact / contract**

`eval/harness-v2/run_live.py:128-139` says post-submit provider outcomes are trials and are never redone.

`eval/empirical-planning/STAGE-A-FREEZE-2026-09/ELIMINATION-RULES.md:27-29` says a refusal or error counts under E1 and is also a reject for E2; nothing changes mid-run.

**Observed**

Wan 2 I2V provider/request-shape failures and Kling two-speaker provider failures were later dispatched again under the same logical trial ids while the new PLANs still state `redo_of: null` and `retries_authorised: 0`.

Examples:

- `eval/experiments/EVAL-040/runs/vid-wan2-i2v/PLAN.yaml:35,47,50+`
- `eval/experiments/EVAL-040/runs/vid-2spk-kling/PLAN.yaml:30,42,45+`

RR-16 itself discloses the rerun:

- `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml:227-236`

**Impact**

The generated media remains useful product evidence, but the affected acceptance denominators are not clean Stage-A evidence.

**One-line fix**

Quarantine affected human-tier cells; recompute under the frozen rule; any replacement execution must have new trial identities and new Controller authority.

---

## F-02 — CRITICAL — E1/E2 were not applied exactly as frozen

**Frozen rule**

`ELIMINATION-RULES.md:5-9,17-29`

A refusal/hard error counts in E1 and is also a reject in E2.

**Contradictory result treatment**

RR-15 states four fal balance refusals were not counted:

- `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml:217-226`

Wan 2 reruns after request-shape failures are disclosed:

- `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml:227-236`

The map also contains `infra_refusals_not_counted` fields, e.g.:

- `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml:351-369`

**Impact**

Some route-elimination / survivor numbers are product-learning numbers, not strict pre-registered experimental numbers.

**One-line fix**

Recalculate every affected question directly from sealed attempts using the literal E1/E2 rule. Do not alter sealed evidence.

---

## F-03 — HIGH — smoke calls reused production trial identities

Examples:

- `eval/experiments/EVAL-040/runs/img-r1-smoke/PLAN.yaml:41`
- `eval/experiments/EVAL-040/runs/topo3-smoke/PLAN.yaml:50`
- `eval/experiments/EVAL-040/runs/vid-ref-smoke/PLAN.yaml:50`
- `eval/experiments/EVAL-040/runs/vid-2spk-kling-smoke/PLAN.yaml:45`
- `eval/experiments/EVAL-040/runs/vid-t2v-smoke/PLAN.yaml:45`
- `eval/experiments/EVAL-040/runs/vid-wan2-smoke/PLAN.yaml:45`
- `eval/experiments/EVAL-040/runs/aud-lip-smoke/PLAN.yaml:50`
- `eval/experiments/EVAL-040/runs/aud-music-lyria-smoke{,2,3}/PLAN.yaml:45`

Several smoke attempts returned `status: ok`, so they were real draws, not merely pre-dispatch connectivity tests.

**Impact**

Where a successful smoke and later production row share the same logical identity, the route effectively received an uncounted extra draw.

**One-line fix**

Future smoke/liveness trials require a separate namespace and may never be used as empirical candidate draws unless pre-registered as such.

---

## F-04 — HIGH — vision-judge qualification crossed its call-count authority

Sealed qualification report records:

- 206 total calls
- USD 3.156153
- 154 compared verdicts
- kappa ~0.33
- judge NOT qualified

Evidence:

- `eval/experiments/EVAL-040/QUALIFICATION-REPORT-2026-09-09.yaml:2066-2099`

The Controller authorization ceiling was 200 calls.

**Impact**

Dollar ceiling remained below USD 5, but a hard call-count limit was exceeded.

**One-line fix**

Record as a governance breach; preserve the unqualified verdict; never retroactively increase the old ceiling.

---

## F-05 — HIGH — at least one video tranche exceeds its conservative ledger ceiling

Video Piece 1 corrected ceiling:

- `coordination/decisions/CONTROLLER-SPEND-AUTHORISATION-IMAGE-HALF-TWO-AND-VIDEO-PIECE-1-2026-09-09.md:86-93`
- corrected cap USD 9.96.

Recomputed ledger consumption for plates + main video + smoke is approximately USD 10.364.

**Impact**

The Controller narrative “no cap crossed” cannot stand without a ledger-vs-vendor reconciliation.

**One-line fix**

Publish both conservative ledger consumption and actual billed charge; record the historical cap breach if ledger semantics govern the cap.

---

## F-06 — HIGH — Wan contender authority also requires reconciliation

RR-16 records the six I2V request-shape failures and rerun:

- `ROUTING-EVIDENCE-MAP-v0.yaml:227-236`

Recomputed ledger consumption across the Wan contender + I2V continuation + smoke runs is approximately USD 11.84 equivalent, above the final approximately USD 11.53 ceiling if every `type: spend` ledger entry consumes the cap.

**One-line fix**

Reconcile provider-billed versus ledger-consumed amounts and issue a Controller disposition. Do not rewrite the historical authorization.

---

## F-07 — MEDIUM — composite spend evidence became durable after some covered calls

Composite authorization/addendum Git commit:
`51ba23d...` at 2026-09-08 14:24:57Z.

Composite calls were ledgered at approximately 14:23:19–14:24:52Z.

The record says the Controller had verbally/intentionally approved “do it”, but durable evidence postdates the covered calls.

**One-line fix**

All future spend authorization must be materialised before dispatch; Controller intent in chat is not enough for the audit trail.

---

## F-08 — MEDIUM — CONTROL-STATE has material state drift

Examples:

- header remains “Updated: 9 Sep 2026 — Image Round 1...”:
  `coordination/CONTROL-STATE.md:8-11`
- early active table says remaining EVAL-040 work not authorised and Registry not yet written:
  `coordination/CONTROL-STATE.md:42-45`
- empirical floor still contains pre-final counts / zeros:
  `coordination/CONTROL-STATE.md:113-129`
- later audit index correctly carries final 575 / 61 / RR-16 state:
  `coordination/CONTROL-STATE.md:266-275`

**One-line fix**

Refresh state-of-record only after the audit disposition is made, using final evidence rather than additive historical prose.

---

## F-09 — MEDIUM — final spend narrative is not reconciled to the ledgers

`CONTROL-STATE.md:266-268` states:

- “Ledger total USD 110.7”
- “no cap crossed”

A direct sum of paid/credit `type: spend` ledger entries parsed during this audit is materially higher (about USD 119.1 before the separate judge qualification run). Some provider errors may have been recorded conservatively but not actually billed.

**Impact**

The project currently conflates:
1. ledger reservation/consumption accounting;
2. actual vendor billing;
3. cash outflow;
4. credits consumed.

**One-line fix**

Produce one reconciled spend table with those four columns per run.

---

## F-10 — MEDIUM — PR / review narrative contains stale intermediate numbers

`CONTROL-STATE.md:275` says PR #93 is open, while current `main` is its merge:
`dcfa6af1064b55761b89be29ef5ae22710fdd4cf`.

PR #92 title says Registry 480 rows while its body says 475.
PR #93 body describes Registry 546 rows / 58 cells before the later Wan round, while the final integrated state is 575 / 61.

These are understandable intermediate snapshots but cannot be treated as the final audit narrative.

**One-line fix**

One final post-merge reconciliation document becomes the only current summary.

---

## F-11 — LOW/METHOD NOTE — Controller was stricter than the literal contract on one image-reference result

`ROUTING-EVIDENCE-MAP-v0.yaml:113-121` explicitly records that two IMG-REF-02 rejections (“clothes changed”) read the contract more strictly than written.

**One-line fix**

Keep the observed judgment as product feedback but exclude it from literal contract-compliance statistics unless the next contract is amended before generation.

---

# 3. What passes

## Registry discipline — PASS WITH NOTES

Independent parse of `eval/registry/registry-v1.jsonl`:

- 575 rows.
- Every row: `evidence_tier: deterministic`.
- Every row: `instrument_qualification_status: deterministic`.
- Every row carries the same criteria SHA.
- Recomputed SHA of frozen `eval/harness-v2/instruments/PASS-CRITERIA-v0.yaml` matches the Registry SHA.
- No human / Controller / judge verdict found inside Registry evidence.
- Map keeps human and screened tiers out of Registry.

Required local commands still need one final execution from the Mac checkout:
- `validate_registry.py`
- two `registry_rows.py` dry builds and diff.

---

## Evidence-tier separation — PASS

The map structurally separates:

- deterministic;
- human_blind_acceptance;
- screened_not_qualified;
- historical_prior.

All inspected `screened_not_qualified`, human, and historical blocks are `registry: false`.

The failure is in trial accounting inside some human-tier cells, not tier mixing.

---

## Price pins — PASS on ten sampled routes

The committed roster equals its stored SHA:
`311f663159a01bc587f1b0c65c65e721d6f46937a5b7d8188ccdb3090a9ccd4c`.

Ten sampled routes match their pinned vendor bytes:

1. GPT Image 2 fallback — USD 0.053 / 1024² medium
2. Seedream 5 Pro — USD 0.0675 / image
3. FLUX.2 Pro — USD 0.03 first MP (+ USD 0.015 extra MP)
4. Qwen Image 3 — USD 0.04 / 1K image
5. Recraft V4 — USD 0.04 / image
6. MiniMax H3 Max — regular USD 0.08/s 768p
7. Kling V3 Pro — USD 0.112/s silent, USD 0.168/s audio
8. Wan 3.0 Prime — USD 0.14/s 720p
9. Wan 2.2 A14B — USD 0.08/s 720p
10. Seedance 2.5 — USD 0.473/s 720p

---

## Package-basis invariant — PASS

The generated freeze package was last changed at commit:

`d8399d84b8b4`

`eval/harness-v2/tests/_support.py:33-35` currently points `ITEM_BASIS_COMMIT` at that same package commit. The later `_support.py` update commit is `6a1b0b62a126`.

A temporary byte-for-byte rebuild still needs to be run locally to complete the mechanical proof.

---

## Network-import boundary — PASS

Direct HTTP/socket import inspection of harness Python modules found provider-network imports confined to:

`eval/harness-v2/transports.py`

Other subprocess usage is local tool/process execution rather than direct provider network access.

---

## Blind sequence — PASS WITH NOTES

For inspected judging sets, mapping or reveal commitment predates the verdict.

Examples:

- composite: mapping `0de0a1c8e8` → verdict `df9dde83ba`
- topo3: `e06d8a3ae9` → `2db1abcca8`
- Wan: `8ca0b7a41f` → `cb6a860610`
- Wan I2V: `9d6297abd8` → `2e9b746c9e`

EVAL-040 reveal-key JSON files are absent from the repository tree.

Major media directories inspected in Git history show only their original sealing commit and no later media modification.

Full binary SHA re-hash against every record still needs the local checkout.

---

# 4. Capability Lab — what EVAL-040 to 043 actually means

## EVAL-040

The sealed experiment/run namespace. All actual run evidence is stored here.

## EVAL-041 — PR #91, merged as `b0f15f1d...`

Carries the first large Day-2 integration:
Registry, image half-two, video pieces, audio work, early routing map.

PR title:
“Registry v1 (459 deterministic rows)... 49 cells, RR-1..13”.

## EVAL-042 — PR #92, merged as `9aa5142e...`

Carries two-speaker/lipsync tail and RR-14.

PR title says Registry 480; body says 475. Treat this as an intermediate integration snapshot, not final truth.

## EVAL-043 — PR #93, merged as `dcfa6af...`

Carries:
- T2V core / RR-15;
- vision-judge qualification;
- Gemini Developer API re-point;
- generated package;
- Wan 2 contender / RR-16;
- final Registry 575.

The PR body itself describes the earlier 546 / 58-cell state before the final contender round landed. Final truth must come from HEAD evidence, not PR prose.

---

# 5. Canon verdict

## Current Canon facts

From `canon/CANON-SHAPE-v1.md:29-36`:

- 37 accepted sources.
- 1,300 SourceKnowledge objects.
- 132 concept systems.
- 291 bindings.
- 2 of 10 compiled packs.
- CANON-GATE-001 exists.

From `canon/CANON-SHAPE-v1.md:113-126`, the intended order after the gate is:

1. Injection v1.
2. Template library / empirical memory.
3. Remaining packs only as the gate demands them.
4. Controller cleanup items.
5. Acceptance-rate measurement.

`coordination/CONTROL-STATE.md:277-282` is consistent with this.

## What EVAL-040 proves about Canon

Nothing causal.

EVAL-040 shows several production doctrines are useful in practice (especially deterministic exact text and correct text-bearing plates), but it does not isolate Canon vs non-Canon.

Therefore:
- “Canon works” is **not** an EVAL-040 result.
- “Canon contains useful production rules” is supported.
- Incremental value must be measured in the intended many-draw blind acceptance experiment.

## Recommendation

Do not compile the remaining eight packs as a prerequisite to launch.

Build:
- Injection v1;
- template/empirical memory;
- only the next pack/check required by a real runtime failure.

---

# 6. What is still missing before public rollout

The missing work is now primarily **product evidence and runtime**, not broad research.

## Missing scientific/product proof

1. Clean human-tier route statistics for method-tainted cells.
2. Stage-B condition envelopes for launch-critical routes.
3. Real-asset validation where stand-ins were used.
4. More than two draws for decisions that materially control customer routing.
5. A valid scalable judge, OR an explicit decision to retain human judgment in alpha.
6. Stage-C accepted-outcome evidence.
7. Fully loaded CpAO.
8. HED-1 decision before CpAO.

## Missing runtime

The required chain is still not demonstrated as one product:

customer request
→ Normalized Request
→ Canon / intelligence
→ Production IR / blueprint
→ route selection
→ generation
→ deterministic checks
→ acceptance / human or qualified judge
→ bounded repair
→ accepted outcome
→ empirical memory

See:
`coordination/CONTROL-STATE.md:298-302`.

## Missing operations

Before autonomous public delivery:

- request-level cost ceiling;
- route failover;
- provider outage behaviour;
- privacy/retention for customer media;
- provenance / audit trace per output;
- moderation and abuse policy;
- production secrets isolation;
- monitoring / alerting;
- kill switch;
- provider terms / commercial-use review;
- customer-visible failure/refund behaviour.

These were not proven in the Capability Lab.

---

# 7. Controller programme — T0 to T8

## T0 — Audit closeout / evidence quarantine
**Spend:** USD 0  
**Start:** current `main` (`dcfa6af`)  
**End condition:** no human routing number violates the frozen trial semantics.

Work:
- enumerate every logical trial id appearing in >1 dispatched run;
- mark smoke vs core vs repeat;
- recompute E1/E2 exactly from sealed attempts;
- quarantine affected RR cells/rules;
- reconcile conservative ledger consumption vs actual provider billing;
- record the judge 206/200 breach;
- record retrospective composite-authority timing;
- refresh CONTROL-STATE only after disposition.

**Parallel:** spend reconciliation and trial-accounting recompute can run in parallel.

**Controller decision:** whether affected cells are (a) merely relabelled product learning or (b) replaced by fresh clean trials.

---

## T1 — Reproducibility gate
**Spend:** USD 0  
**Start:** T0 does not need to be complete; can begin immediately in parallel.  
**End condition:** clean repeatable build from HEAD.

Required local checks:

- 326-unit-test suite;
- `validate_registry.py`;
- `registry_rows.py` dry on two selected runs, diff against committed rows;
- `evidence_map.py` regeneration/diff;
- package build to temp and byte diff;
- every sealed media SHA against record JSON;
- auth-file roster SHA vs current roster;
- secret-pattern scan of sealed JSON/YAML;
- confirm local reveal keys remain outside Git;
- status/dry-run commands only.

Any failure blocks T2+ spend.

---

## T2 — Minimal evidence repair
**Spend:** target USD 0–15; exact cap requires fresh Controller record.  
**Start:** T0 identifies affected launch-critical cells.  
**End condition:** every route used by runtime v0 has clean Stage-A identity/denominator evidence.

Do not rerun the battery.

Only rerun:
- method-tainted cells that will actually route launch traffic;
- real-asset checks where stand-in evidence is carrying a launch decision;
- selected 2-draw cells where one different draw would change the production choice.

**Kill rule:** a route with weak evidence can remain a manual fallback rather than trigger more benchmarking.

---

## T3 — Runtime vertical slice / Production IR v0
**Spend:** USD 0 to build; small provider cap only for final integration proof.  
**Start:** T1 passes; T2 may still be closing non-critical routes.  
**End condition:** one real brief passes through the complete system without hand-authoring intermediate objects.

Build the smallest version of:

NR
→ pack trigger
→ Injection v1
→ one production blueprint / Production IR
→ evidence-aware router
→ execution
→ deterministic gate
→ bounded repair
→ accepted result
→ immutable empirical-memory event.

No generic Planner architecture work beyond what this vertical slice forces.

---

## T4 — Stage B on launch-critical routes only
**Spend:** expected tens of USD, not a full matrix; exact sizing must be produced from the surviving T3 routes.  
**Start:** T3 identifies which routes actually matter.  
**End condition:** machine-readable condition envelopes exist.

For each live route establish:

- supported aspect/duration;
- text/no-text;
- Hindi/English;
- native audio/silent;
- product/reference sensitivity;
- camera-motion constraints;
- physical-detail failure modes;
- refusal / timeout behaviour;
- cost distribution;
- fallback.

Result should be “route X works under conditions A/B/C,” not “route X score = 82”.

---

## T5 — Evaluation decision
**Spend:** USD 0 decision; judge-v2 experiment likely low-single-digit USD if authorised.  
**Start:** parallel with T3/T4.  
**End condition:** release evaluation policy is frozen.

Controller chooses one:

### Option A — human-first alpha
Use blinded human acceptance as release authority; deterministic tools automate only hard checks.

### Option B — Judge v2
Build and qualify a stronger/prompt-corrected judge. It cannot enter Registry/routing authority until qualification passes.

**Recommendation:** Option A for first alpha. Judge qualification should not block learning from real customer jobs.

---

## T6 — Stage C / real-demand accepted-outcome test
**Spend:** likely largest remaining evidence tranche; size after T4, not now.  
**Start:** T3 runtime + T4 route envelopes + T5 evaluation policy.  
**End condition:** system proves it can produce accepted outcomes, not merely individual model capabilities.

Use real-demand / untouched cases.

Compare:

A. full system  
vs  
B. strongest simple baseline.

Measure:

- accepted-outcome rate;
- CpAO;
- number of generations;
- repair rate;
- human minutes;
- provider failure rate;
- latency;
- incremental value over baseline.

Resolve HED-1 before fully-loaded CpAO.

**Ship criterion:** full system must improve acceptance or operational economics enough to justify its added complexity. If a simpler LLM + fixed recipe wins, ship the simpler system.

---

## T7 — Private alpha
**Spend:** customer-job dependent, request-capped.  
**Start:** T6 passes minimally.  
**End condition:** multiple real jobs complete with no uncontrolled spend or unrecoverable failure.

Rules:

- every final output receives human release approval;
- no autonomous external delivery;
- every failure creates a new Capability Lab case;
- router may fall back to “human choose route”;
- all cost / repair / acceptance events logged.

The product can be sold/used privately at this point.

---

## T8 — Public beta gate
**Spend:** operational, not benchmark-defined.  
**Start:** private alpha proves stable.  
**End condition:** Controller signs public-release decision.

Required conditions:

1. audit closed;
2. HEAD reproducible;
3. route evidence clean;
4. Stage-B envelopes exist for public routes;
5. Stage-C accepted-outcome evidence exists;
6. CpAO measured;
7. fallback/repair bounded;
8. spend ceilings and kill switch live;
9. customer privacy/retention policy live;
10. provider commercial/terms review complete;
11. observability/incident handling live;
12. human override remains available.

Only after this gate should automatic customer delivery be enabled.

---

# 8. Parallel execution view

Immediately:

**Lane A — Audit**
T0 trial/spend reconciliation.

**Lane B — Reproducibility**
T1 local mechanical audit.

**Lane C — Runtime design**
T3 can begin in USD-0 mode using only already-accepted routes and dry execution.

After T0/T1:

**Lane D — Minimal evidence repairs**
T2.

**Lane E — Injection v1 / template memory**
small Canon-runtime work inside T3; do not launch an eight-pack Canon programme.

Then:

T4 Stage B
+
T5 evaluation policy

→ T6 Stage C

→ T7 private alpha

→ T8 public beta.

---

# 9. What should explicitly NOT happen next

Do not:

- rerun all of Stage A;
- compile all 10 Canon packs before product use;
- search indefinitely for a perfect automated judge;
- expand all two-draw cells merely for statistical neatness;
- build a generic Planner before the first vertical slice;
- run premium routes simply because they exist;
- conflate Registry deterministic evidence with human acceptance;
- treat the current 61-cell map as a production SLA;
- publicly advertise routing reliability from these sample sizes.

---

# 10. Controller decisions required now

## D1 — Evidence disposition
Choose whether method-tainted human cells are:
- descriptive only; or
- rerun cleanly where launch-critical.

**Decision cost:** USD 0.
**Execution cost:** likely small single-digit / low-double-digit USD if limited to launch routes.

## D2 — First launch use case
Freeze the first externally exposed job family.

Without this, “more testing” has no stopping rule.

**Decision cost:** USD 0.

## D3 — Human release policy
Approve mandatory human acceptance for private alpha.

**Decision cost:** USD 0.

## D4 — Judge v2
Defer or authorise.

**Expected experimental spend:** comparable order to prior judge run (~USD 3), but must be re-sized and independently capped.

## D5 — Canon
Authorize Injection v1 + empirical-memory template work only; defer blanket pack expansion.

**Build spend:** USD 0.

## D6 — Stage-B budget
Authorize only after T3 names the routes.

**Cost:** TBD from exact rows; should be a narrow tens-of-USD tranche, not the full original matrix.

## D7 — Stage-C budget
Authorize once the runtime and baseline are frozen.

**Cost:** TBD; this is the one experiment worth spending on because it measures the actual product objective.

## D8 — Public release bar
Adopt T8 as the release condition.

**Decision cost:** USD 0.

---

# 11. Bottom line

The project should now change mode.

The last two weeks were primarily:
**research → architecture → harness → empirical route discovery.**

The next phase should be:
**audit closure → vertical-slice product → targeted condition testing → accepted-outcome experiment → real customer alpha.**

The Capability Lab is now useful enough that continuing to widen it before the product consumes it will have declining value.

The central unanswered question is no longer:

> Which model is best?

It is:

> Can the complete intelligence + routing + generation + evaluation + repair system produce a customer-accepted result more reliably and cheaply than the strongest simpler workflow?

That is the Stage-C/public-product question. Everything before public rollout should now be organised around answering it.
