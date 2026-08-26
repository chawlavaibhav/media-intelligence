# GOV-004 — Final pre-execution coherence review

**Task:** `governance/tasks/GOV-004.md`
**Reviewer:** Repository Governor · **Date:** 26 Aug 2026
**Branch:** `work/gov-004-final-pre-execution-review` · **Not merged**
**Spend:** ₹0. No model, evaluator or provider call. No acquisition. No Registry write. No domain file edited.

## Verdict

> # PASS WITH NON-BLOCKING NOTES

**What this verdict means.** The repository is coherent enough for **Controller integration and
explicitly priced empirical-tranche planning**. Every cross-stream invariant the task named was
checked, and where it could be derived from a committed artifact it was derived rather than read.

**What it does not mean** — and must never be cited as meaning: the science is not proven, no model
is shown to be good, **no evaluator is qualified**, the Canon is not shown to improve outcomes, the
Planner does not exist, and **paid execution is not authorised by this review**. Those judgements
belong to the owning streams and the Controller (`governance/GOVERNOR-CONTRACT.md` §0, §3).

**Seven non-blocking notes.** Three are corrected inside Governor-owned current-state files by this
task. One must be handled at merge time. Three are wording-precision items routed to their owning
streams; none of them blocks paid execution.

### Merge-safety, per package

| Package | Branch @ commit | Coherence-safe to merge? | Basis |
|---|---|---|---|
| **CANON-010** | `work/canon-010-request-freeze` @ `3cf2979` | **Yes** | Purely additive — 11 files, **0 existing files touched** |
| **Corrected Eval / EVAL-011** | `work/eval-011-pre-execution-integration` @ `e300999` | **Yes, after one trivial merge resolution** — see N-1 | Additive plus the six EVAL-009 files it was authorised to correct; conflicts with `main` only on `coordination/CONTROL-STATE.md` |
| **RES-004** | `work/res-004-production-readiness` @ `2dc4796` | **Yes** | One existing file changed — `resources/HANDOFF.md`, which Resources owns |
| **EVAL-010** | `work/eval-010-route-verification` @ `8a8fc09` | **Yes** | Purely additive — 11 files, **0 existing files touched** |

All four commit SHAs match the assignment exactly. None is merged. `main` is at
`74d6b0da0239013269f73804164a92f80c7f1d55`, which is the SHA named at assignment.

---

## 1. Independently checked invariants

Everything in this section was **derived in this session from the committed artifacts**, not read
from prose. Where a validator was rerun, the working tree was confirmed clean afterwards, so nothing
was regenerated into the repository (the regeneration rule, `GOVERNOR-CONTRACT.md` §2).

### 1.1 The task's named invariants

| # | Invariant | Result | How it was established |
|---|---|---|---|
| 1 | Original 30 Canon briefs unchanged | **HOLDS** | `briefs.jsonl` and `briefs-source.yaml` byte-identical to `main` on all four branches; 30 lines; SHA-256 `2e313d04…` |
| 2 | Request-operation vocabulary is exactly `generate / edit / animate / restore / extend / compose / variants` | **HOLDS** | Parsed from the grammar YAML: 7 values, exact set **and exact order** |
| 3 | Requested operation stays distinct from workflow mode | **HOLDS** | `COND-OPERATION` is `customer_side`, `COND-WORKFLOW` is `planner_side`; both carry a two-way hard rule; 8 production-route values are explicitly forbidden and the CANON-010 validator rejects them |
| 4 | Capability Contract v2 = 44 = 43 active + 1 dormant repairability | **HOLDS** | Counted from the YAML: 44 entries, status split 43 active / 1 dormant; the dormant one is `repairability` |
| 5 | V1 36-capability contract and V1 100-item bank immutable | **HOLDS** | Byte-identical on every branch and after a full merge; V1 validator still reports 36/36 |
| 6 | Condition architecture = exactly 13 families | **HOLDS** | 13 entries parsed; `condition_families_count: 13` |
| 7 | Two-level full product = 8,192 cells | **HOLDS** | `two_level_naive_cells: 8192`, derivation `2 ** 13 = 8192`; independently `2**13 = 8192` |
| 8 | Scientific roster = 12 core + 2 reserve | **HOLDS** | 14 slots, `tier` field splits 12 core / 2 reserve; reserves are `IMG-05`, `IMG-06` |
| 9 | `blocked_by_prerequisite_failure` stays unsatisfied for outcome acceptance | **HOLDS** | `outcome_acceptance: unsatisfied`, `countable_in_pass_rate: false`; three negative fixtures fire when it is promoted to pass or to `not_applicable` |
| 10 | Seeded and unseeded reproducibility not silently pooled | **HOLDS** | `hard_rule_repeats` forbids pooling `held` and `unset` repeat groups; fixture `nc-seed-pooling` fires |
| 11 | IMG-04 and AUD-03 unresolved rather than substituted | **HOLDS** | Both `identity_unresolved` with `do_not_substitute: true`; `sibling_substitutions_performed: 0`; fixture `nc-silent-sibling-substitution` fires |
| 12 | Layers 1–3 do not claim customer-outcome CpAO | **HOLDS** | Stages A and B carry `metrics_forbidden: [customer-outcome CpAO]`; Stage C carries `cpao_authority: THIS STAGE ONLY`; fixture `nc-layer13-claims-cpao` fires |
| 13 | Stage Q = 0 model generations | **HOLDS** | `model_generations.count: 0` across all 8 Stage-Q units; fixture `nc-stage-q-spends-generations` fires |
| 14 | Stage A = 90 generations | **HOLDS** | **Summed the per-slot table independently: 90.** 4 image slots × 8 + 5 video × 8 + 3 audio × 6 = 32 + 40 + 18 = 90 |
| 15 | Stage B ≤ 404 additional | **HOLDS** | `generation_count_maximum: 404`, derived as `494 − 90` |
| 16 | A + B ceiling = 494 | **HOLDS** | 90 + 404 = 494, matching `design_ceiling_layers_1_3`; fixture `nc-stage-counts-do-not-reconcile` fires |
| 17 | Stage C = 32 outcome attempts, separate from the 494 ceiling | **HOLDS** | `outcome_attempt_count: 32` (8 briefs × 2 recipes × 2 repeats), explicitly *"32 OUTCOME ATTEMPTS, not 32 generations"*; its generation count is `null` with a stated reason; the rollup keeps it out of the 494 line |
| 18 | 494 / 5,515 / 188 not represented as an approved paid tranche | **HOLDS** | Labelled *"FULL Layers-1-3 DESIGN CEILING. It is not a budget and not a tranche"*; `authorises_spend: false` in all three forecast artifacts |
| 19 | Topology chain exactly `job → outcome → sequence_or_asset_set → production_unit → production_step → attempt → artifact` | **HOLDS** | All seven present in that exact order. Three supporting entities also exist (`transform_recipe`, `measurement`, `acceptance`); the brief states "10 entities" openly, so nothing is misrepresented |
| 20 | One provider/API/transform call = one trial | **HOLDS** | Gates G1, G2 and G6; fixtures `nc-G1-two-attempts-one-trial`, `nc-G2a/b`, `nc-G6-phantom-trial` all fire |
| 21 | Exactly four controlled-pack families | **HOLDS** | Validator reports 4, `fifth family created: False` |
| 22 | Provisional pack totals and 173 hours not first-run budgets | **HOLDS** | 173 h stated *"under provisional counts and R = 1, in hours not currency"*; the Eval material map states it is **not** a prerequisite to the first paid model call; fixture `nc-173-hours-mandatory` fires |
| 23 | API/tool CpAO diagnostic, fully-loaded primary | **HOLDS** | Contract table marks them `diagnostic` and `PRIMARY BUSINESS METRIC`; both computed on three positive fixtures |
| 24 | Rights/consent restrictions explicit | **HOLDS** | CC-BY-NC prohibition, consent-before-capture, no public face scraping and no request-corpus UGC identity images all stated in the pack requirements and the rights plan |
| 25 | EVAL-010 remains partial supply evidence | **HOLDS** | *"COMPLETE as a program. The supply table it produced is PARTIAL, and is labelled partial."* |
| 26 | `2/26 execution-ready` not rewritten as "only two usable models" | **HOLDS** | "Execution-ready" is defined as identity + route + billing unit + price all verified; 19 further rows are `verified_fallback_only` — *"we know exactly what and where they are, we just cannot cost them"* |
| 27 | Missing prices stay unknown | **HOLDS** | `stages_price_complete: 0` of 4; unresolved fields remain null; fixtures `nc-cash-outlay-guessed` and `nc-partial-stage-totalled` fire |
| 28 | Nano Banana 2 wording ≈ `$0.067 per generated 1K-resolution image` | **HOLDS in the machine-readable evidence** — see note N-6 on the prose shorthand | `vendor_published_per_image: "1K": {tokens: 1120, usd: 0.067}`, `resolution_dependent: true`; EVAL-011's forecast carries the Controller reading with the per-thousand reading explicitly rejected |
| 29 | Veo 3.1 Lite `$0.05` stays route-specific | **HOLDS** | Bound to `veo_3_1_lite / video_plus_audio / 720p` under `resolution_and_tier_dependent: true`; generalisation explicitly forbidden |
| 30 | Frontier Clouds unresolved | **HOLDS** | `unresolved_service_identity`; cash outlay after credits recorded `UNRESOLVED`, `do_not_infer: true` |
| 31 | No model claimed qualified | **HOLDS** | No qualification claim anywhere; roster slots carry supply status only |
| 32 | No subjective/perceptual evaluator family claimed qualified | **HOLDS** | `instruments_qualified: 0` and `instruments_qualified_today: 0`; fixture "marking an instrument qualified must FAIL" fires |
| 33 | Capability Registry empirically empty | **HOLDS** | `registry-v1.jsonl` byte-identical everywhere; validator: **0 data rows** |

### 1.2 Two cross-checks the task did not ask for, worth recording

**The 43 active capabilities partition exactly across the 7 evaluator families.** Summing
`by_evaluator_family` gives 5 + 12 + 9 + 2 + 7 + 4 + 4 = **43**, equal to `v2_active`. The Stage-Q
plan's 8 units also sum to 43 capabilities unblocked. Two independently authored files agree on a
number neither is derived from.

**The v1 → v2 capability arithmetic closes.** 36 − 4 ids removed + 12 ids added = **44**. The four
removed (`spatial_relationship`, `spoken_language_correctness`, `reproducibility_repairability`,
`anatomy_hands`) and the twelve added match the Controller's four splits, one rename and four
additions exactly, with no capability appearing or vanishing unaccounted for.

### 1.3 Validators rerun in this session

A gate that never fails proves nothing, so the negative controls matter more than the passes. Every
suite below was executed here, and **every negative fixture fired**.

| Suite | Result |
|---|---|
| CANON-010 `validate_request_freeze.py` | **PASSED**, 7/7 gates |
| CANON-010 `tests/test_request_freeze_gates.py` | **7/7 negative controls fire**; bank restored, tree clean |
| CANON-010 `combined_coverage.py` | Regenerates the committed measurement **byte-identically** |
| EVAL-009 `validate_freeze_package.py` | **PASS — 10 gates**; 36→44 (43+1), 12 core/2 reserve, 0 instruments qualified, V1 unmodified |
| EVAL-009 `test_negative_fixtures.py` | **17 gate fixtures rejected + 6 aggregation semantics hold** |
| EVAL-011 `validate_integration_package.py` | **PASS — 13 gates**; 13 families / 8,192 cells, 7 ops owner `canon`, Q=0 A=90 B≤404 C=32, price-complete stages 0 |
| EVAL-011 `test_negative_fixtures.py` | **16/16 negative fixtures caught** |
| RES-004 `run_all_res004.sh` | **exit 0** — 18/18 lineage controls, 13/13 CpAO controls, 4 packs, inherited v2.1 and RES-003 suites still green |
| Canon audit gate | 19 records, **0 errors** — live Canon still 19 |
| CANON-003 historical validator | Still 16 books / 505 / 54 / 417 / 53 / 111, 0 errors — **unchanged, as it must be** |
| V1 capability contract | **PASS — 36/36, scope unchanged** |
| Registry | **PASS — registry empty** |

### 1.4 Full merge simulation

All four packages were merged into `main` in a scratch branch. One conflict arose (N-1) and was
resolved by keeping `main`'s newer Controller-authored `CONTROL-STATE.md`. On the resulting tree:

- the only non-added file relative to `main` is `resources/HANDOFF.md`, which Resources owns;
- every protected baseline is byte-unchanged;
- `governance/tasks/GOV-004.md` survives — the deletion that appears in a raw branch-vs-`main` diff
  is an artifact of EVAL-011 being three commits behind, not something the branch does;
- **every validator listed in §1.3 still passes**, and the working tree is clean.

---

## 2. Cross-package authority and boundaries (task §A)

| Check | Result |
|---|---|
| Worker recommendations distinct from Controller decisions | **HOLDS.** Every freeze artifact carries a status such as `PROPOSED_FOR_CONTROLLER_FREEZE_NOT_IN_FORCE`, `PROPOSED_READY_FOR_FREEZE` or `IMPLEMENTATION_READY_PENDING_CONTROLLER_FREEZE`. None claims to be in force. |
| Controller decision is the authority | **HOLDS.** Artifacts cite `coordination/decisions/…` as `authority`; `CONTROL-STATE.md` separates accepted freeze targets from what is not authorised. |
| No branch claims paid execution, Registry population or qualification happened | **HOLDS.** `authorises_spend: false` in all three forecasts; `instruments_qualified: 0`; Registry byte-identical with 0 rows; a text scan for approval/qualification claims returned nothing. |
| No stream exceeded its write boundary | **HOLDS.** CANON-010 and EVAL-010 touch nothing pre-existing. RES-004 touches only its own handoff. EVAL-011 modified six EVAL-009 files — **exactly the correction it was authorised to make** — plus `CONTROL-STATE.md`, and that edit is the Controller's own sync commit `f2248f2`, not the worker's. |
| No broad research task silently reopened | **HOLDS.** No new task file was created on any branch. |

**Stream ownership of the shared vocabulary is explicit and machine-checked.** The condition
contract records `vocabulary_owner: canon` and `eval_may_extend: false` for the requested-operation
field, and a validator gate fires if Eval's copy drifts from Canon's. Comparing the two files
directly, the seven machine ids are identical.

---

## 3. The wording question GOV-004 asked to be adjudicated

**Question.** `EVAL-011-CONTROLLER-BRIEF.md` says three evaluator families can be qualified from
material already in the repository, while `EVALUATOR-AND-MATERIAL-STAGE-MAP.yaml` reports
`families_qualifiable_with_material_already_in_repository: 2` and
`families_qualifiable_with_eval_built_material_no_resources_pack: 1`. Defect, or shorthand?

**Determination: harmless shorthand. Not a coherence defect. Routed to Eval as a precision note
only (N-5), and it does not block paid execution.**

**What the evidence actually shows.** Working from the committed files rather than the prose:

| Family | Capabilities | Material | Held today? |
|---|---:|---|---|
| `deterministic_cv_geometry` | 5 of 5 | `MAT-CV`, 102-item CV-geometry fixture pack | **yes, in repository** |
| `operational_logging` | 4 of 4 | `MAT-LOG`, harness run records | **needs no material at all** |
| `text_ocr` | 1 of 2 | `MAT-DEV`, the frozen 96-item Devanagari battery | **yes, in repository** |
| `text_ocr` | 2 of 2 | `MAT-LAT`, a Latin exact-text pack | **no — Eval must build it, no Resources pack needed** |

So the YAML's `2` counts families **fully** qualifiable from held material, and its `1` is `text_ocr`,
which needs one further Eval-built artifact. `2 + 1 + 4 blocked = 7`, and the file's own
`evaluator_families: 7` closes. **The YAML is arithmetically correct and is the more precise
statement.**

The brief's "three" is true of a different question — how many families are **not blocking Stage Q**
— which the same YAML answers as three in `evaluator_blockers_by_stage.stage_Q.not_blocking`. The
brief lists three *materials* and attaches the count to *families*, and one of those three families
is only half-covered by the held material.

**Why this cannot mislead a zero-context session into a wrong action.** Three independent reasons:

1. **The brief's very next sentence supplies the missing piece**: *"A Latin exact-text set can be
   built by Eval with no new Resources pack."* A reader of two consecutive sentences has the correct
   picture.
2. **The operational artifact is unambiguous.** Nobody plans Stage Q from the brief; they plan it
   from `STAGED-EXECUTION-PLAN.yaml`, which enumerates **Q2b `text_ocr_latin`** as its own unit with
   `material_status: EVAL_BUILDABLE_NO_RESOURCES_PACK_NEEDED` and `blocker: pack must be built`. The
   Latin build cannot be silently dropped from a plan that lists it as a numbered unit.
3. **No count, gate or budget consumes the brief's number.** The validators read the YAML.

**What is genuinely worth tightening**, and why it is recorded rather than waved away: the same YAML
file answers two different questions with two different partitions of the same seven families — `3`
under `not_blocking`, `2 + 1` in its `headline` — without saying they are different questions. Both
are correct; the file does not label the distinction. That is the cleanest statement of the issue and
it is what N-5 routes.

---

## 4. Findings

All seven are non-blocking. Severity follows the contract's test: **what would a future zero-context
session wrongly believe, and would it act on it?**

| ID | Finding | Severity | Owner | Status |
|---|---|---|---|---|
| N-1 | EVAL-011 branch conflicts with `main` on `CONTROL-STATE.md`; resolving it the wrong way regresses current state | **Medium** | Controller | **must be handled at merge time** |
| N-2 | `DECISION-LOG.md` does not index the pre-execution integration decision | **Medium** | Governor | **corrected here** |
| N-3 | `WORKSTREAM-STATUS.md` still describes the four programmes as active | **Medium** | Governor | **corrected here** |
| N-4 | `PROJECT-MEMORY.md` still says the three macro branches are unmerged and knows nothing of the pre-execution tranche | **Medium** | Governor | **corrected here** |
| N-5 | "Three evaluator families" shorthand vs the YAML's `2 + 1` partition | **Low** | Eval | routed — precision only |
| N-6 | EVAL-010 brief's `$0.067 per 1K image` shorthand | **Low** | Eval | routed — precision only |
| N-7 | `CPAO-CONTRACT-v3.md` does not restate the one-time-R&D exclusion | **Low** | Resources | routed — precision only |

**None of N-5, N-6 or N-7 needs to be resolved before paid execution.** Each is a wording tightening
in a prose file whose machine-readable counterpart is already correct and already gated. They are
listed so the owning stream can fix them when it freezes the artifact, not as conditions.

### N-1 — the EVAL-011 merge conflict · Medium · Controller · handle at merge

**Evidence.** Merging `work/eval-011-pre-execution-integration` into `main` produces a content
conflict in `coordination/CONTROL-STATE.md`, six hunks. Nothing else conflicts. The branch is
**three commits behind** `main`:

| Side | Commit | Time | `CONTROL-STATE.md` says |
|---|---|---|---|
| branch | `f2248f2` | 16:01 | "four pre-execution programs reviewed; **one bounded Eval integration correction active**" |
| `main` | `74d6b0d` | 16:52 | "**EVAL-011 correction complete**; final Repository Governor review active" |

**Both sides are Controller-authored.** This is not a worker overstepping — commit `f2248f2` is the
Controller's own branch sync. The conflict exists only because the Controller then advanced `main`
while the branch stood still.

**Why it matters.** `main`'s version is strictly newer and describes the true current state.
Resolving toward the branch would put the repository back to saying the EVAL-011 correction is still
running and GOV-004 has not been assigned — a false current state on the file that
`PROJECT-MEMORY.md` names as authoritative for what is currently authorised.

**The correction is trivial and is the Controller's to make:** take `main`'s
`coordination/CONTROL-STATE.md` when merging EVAL-011, or bring the branch up to date with `main`
first. A simulated merge resolved that way was verified in §1.4: clean tree, all validators pass,
`governance/tasks/GOV-004.md` intact.

**One thing this is not.** A raw `git diff origin/main <branch>` shows `governance/tasks/GOV-004.md`
as deleted. That is an artifact of comparing a behind-branch against `main`, **not** a deletion the
branch performs; a real merge keeps the file. This was checked rather than assumed, because the same
appearance on a different branch would be a serious finding.

### N-2 — the decision index misses the decision this review is measured against · Medium · Governor · corrected

**Evidence.** `coordination/decisions/` holds nine Controller records. `coordination/DECISION-LOG.md`
indexed eight. The missing one was
`CONTROLLER-PRE-EXECUTION-INTEGRATION-2026-08-26.md` — **the authoritative joint disposition for the
whole package under review**, and the file GOV-004 names as required reading.

The index has otherwise been kept current since GOV-003 routed this class of defect; this is a single
newest-entry lag rather than the systemic gap found last time. Corrected in this task by adding one
row in the existing format.

### N-3 — the workstream status file describes a state that has passed · Medium · Governor · corrected

**Evidence.** `coordination/WORKSTREAM-STATUS.md` stated *"Four Controller-assigned ₹0 cloud programs
are active in parallel"* and listed `work/eval-009-measurement-freeze` as live work, with the Governor
row reading *"none while domain tranche runs"*. All four programmes have returned, EVAL-009 has been
superseded by EVAL-011 as the live Eval proposal, and GOV-004 is the single active assignment. The
file also did not list the pre-execution integration decision among its authoritative decisions.

**Why it matters.** A fresh Controller session reading this file would believe four domain programmes
were still running and would look for live work on a branch that is now historical.

Corrected in this task, keeping the file's own current-state-only convention.

### N-4 — project memory predates two merges and a whole tranche · Medium · Governor · corrected

**Evidence.** `PROJECT-MEMORY.md` was last refreshed at GOV-003 against `main` `2cd29037`. Since then
the Controller merged CANON-009, EVAL-007, RES-003 and the GOV-003 review into `main`, ran the entire
final pre-execution freeze tranche, and issued the integration decision. Memory still said the three
macro branches were **unmerged**, still said *"four research programmes … all four are unmerged"*, and
contained no mention of CANON-010, EVAL-009, EVAL-010, EVAL-011 or RES-004.

Two of its own routed warnings had also gone stale in the opposite direction: it warned that
`WORKSTREAM-STATUS.md` describes a total audit freeze and that `DECISION-LOG.md` had not been updated
since 25 August. Both were refreshed by the Controller on 26 August, so those warnings were
themselves now misleading.

Corrected in this task. The refresh is narrow and stays a bootstrap rather than a transcript — see §6.

### N-5 — "three evaluator families" · Low · Eval · routed, precision only

Fully adjudicated in §3. The recommended fix is one clause, at Eval's discretion when the artifact is
frozen: say *"three families do not block Stage Q — two are fully covered by material already in the
repository, and `text_ocr`'s second half needs one Eval-built pack that requires no Resources
acquisition"*, and label the two partitions in the YAML as answers to different questions.

**Not a condition on paid execution.** The plan that Stage Q would actually be run from is already
correct and complete.

### N-6 — `$0.067 per 1K image` · Low · Eval · routed, precision only

**Evidence.** `EVAL-010-CONTROLLER-BRIEF.md` writes the Nano Banana 2 price as *"$0.067 per 1K
image"*. That is the exact phrasing the Controller had to clarify in decision §5.1, because it can be
read as $0.067 per one thousand images.

**The evidence chain is already sound.** `PRICE-VERIFICATION.yaml` records it under a key literally
named `vendor_published_per_image`, as `"1K": {tokens: 1120, usd: 0.067}` with
`resolution_dependent: true` — unambiguous. EVAL-011's `PRICE-READY-STAGED-FORECAST.yaml` carries the
Controller's reading with `incorrect_reading_explicitly_rejected: USD 0.067 per one thousand images`.
So every downstream artifact is protected.

**Why it is still worth routing.** The brief is what a human reads before approving money. Adopting
the Controller's phrasing — *"approximately $0.067 per generated 1K-resolution image"* — costs one
line and removes the last place the ambiguous shorthand survives.

### N-7 — the one-time-R&D exclusion is enforced but not stated · Low · Resources · routed, precision only

**Evidence.** The Controller decision §4.2 excludes one-time R&D, benchmark design, pack acquisition
and evaluator qualification from per-customer CpAO. `CPAO-CONTRACT-v3.md` defines four cost classes
(`api_tool`, `local_compute`, `human_required`, `human_optional`) and does not restate that exclusion.

**It is nonetheless enforced, structurally.** Reading `recompute_cpao_v3.py`, the engine charges only
ledger entries reachable from the accepted outcome's own production steps, attempts and measurements.
A pack-acquisition or evaluator-qualification cost is not attached to a customer outcome's production
step, so it cannot enter either CpAO view. The same walk dedupes by ledger id, so a shared upstream
artifact is counted once, and `journey()` stops at a `scope_change_boundary` — both Controller
requirements, verified by running the fixtures.

**The gap is documentary, not behavioural.** A reader of the contract file alone does not learn the
exclusion. One sentence at freeze closes it.

---

## 5. What this review did not check

Stated plainly, because a review's silence is read as approval.

- **Whether any domain method is correct.** Not the Governor's judgement. This review does not
  evaluate whether 44 is the right number of capabilities, whether 13 condition families are the
  right families, whether the 12 scientific questions are the right questions, whether the staging is
  wise, or whether the outcome topology is the right shape. It checks that the repository says the
  same thing about them everywhere and that the Controller's dispositions are reflected.
- **Any external claim.** Provider prices, model identities, release dates, licence terms and
  benchmark figures were checked only for **internal consistency, evidence labelling and preservation
  of the Controller's clarifications**. None was verified against its primary source here, and no
  network call was made. All four workers recorded that provider egress was blocked in their
  sessions.
- **Anything requiring the raw corpus or a model call.** The 5.70 GB media corpus is git-ignored and
  absent; no media file was opened; no model, evaluator or provider was called.
- **Whether the packages are complete as designs.** Coherence is not completeness. Several fields are
  deliberately unresolved — prices, Frontier Clouds, `n_latin`, Stage C generation counts, HED-1 —
  and this review confirms they are **labelled** unresolved, not that they are resolved.

---

## 6. Current-state documents updated

Under GOV-004's grant to update Governor-authorised current-state documentation, three files were
corrected. **No domain artifact was touched.**

| File | Change |
|---|---|
| `PROJECT-MEMORY.md` | Narrow refresh: the four macro branches are merged; the pre-execution tranche returned and its four packages are unmerged and under this review; the Controller-adopted freeze targets; the staged execution model; that paid execution remains blocked; stale routed warnings removed now that the Controller has refreshed those files |
| `coordination/WORKSTREAM-STATUS.md` | Current-state refresh: programmes returned rather than active; EVAL-011 is the live Eval proposal and EVAL-009 is historical; GOV-004 is the single active assignment; the integration decision added to the authoritative list |
| `coordination/DECISION-LOG.md` | One row added for `CONTROLLER-PRE-EXECUTION-INTEGRATION-2026-08-26.md` |

`coordination/CONTROL-STATE.md` was **not** edited. It is Controller-owned, it is current, and it
already separates accepted freeze targets from what is not authorised correctly. Checking it against
the underlying artifacts, every quantified claim it makes — 44 = 43 + 1, 13 families, 8,192 cells,
12 + 2 slots, Q=0 / A=90 / B≤404 / ceiling 494 / C=32, four packs, 0 Registry rows, 0 qualified
instruments — is confirmed by the derivations in §1.

**A note on how the memory refresh should be read after a merge.** It records the four packages as
unmerged **as of `main` `74d6b0d`, 26 Aug 2026**. If the Controller merges them, that becomes
historical and the Governor should refresh it. The SHA is attached so the staleness is self-evident
rather than silent.

---

## 7. Answer to the question the Controller actually asked

**Is the repository coherent enough for Controller merge/integration and explicit priced-tranche
planning?**

**Yes**, subject to N-1 being handled at merge time.

The reasoning, briefly. Priced-tranche planning needs four things to be true of the repository, and
all four were verified mechanically rather than read:

1. **The counts a price would be computed from are internally consistent and reproducible.**
   90 + 404 = 494 was re-derived from the per-slot table; 44 = 43 + 1 and 13 → 8,192 were re-derived
   from the schemas; 12 + 2 slots were re-derived from the `tier` field.
2. **Nothing is priced that is not known.** `stages_price_complete: 0 of 4`. Every unresolved price,
   the Frontier Clouds identity and cash-outlay-after-credits stay explicitly unresolved, and
   negative fixtures fire if anyone totals a partial stage or guesses the cash line.
3. **Nothing already reads as approved.** 494 / 5,515 / 188 and the 173 hours are labelled ceilings
   and provisional estimates, `authorises_spend: false` throughout, and the Controller decision's
   "explicitly not frozen" list is reflected in current state.
4. **The floor holds.** 0 instruments qualified, 0 Registry rows, V1 baselines byte-identical, the
   original 30 briefs byte-identical, one call = one trial intact.

What the Controller is being asked to price is therefore **a described, bounded, internally
consistent design with its unknowns visibly marked** — not a package that quietly assumes it has
already been approved.
