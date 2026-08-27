# GOV-006 — Post-Parallel Integration Reconciliation

**Task:** `governance/tasks/GOV-006.md`
**Authorisation:** `coordination/decisions/CONTROLLER-GOV-006-START-AUTHORISATION-2026-08-28.md`
**Audited `main`:** `91984f50b294f11aefc7065f5ad11f9e0d3e2b9a` — *"controller: start GOV-006 after parallel lanes settle"*, 28 Aug 2026
**Branch:** `work/gov-006-post-parallel-reconciliation`, branched from that exact commit
**Date:** 28 Aug 2026
**Spend:** USD 0. No model, evaluator, provider or paid API call was made. No resource was acquired.

---

## Verdict

# PASS WITH NON-BLOCKING NOTES

**What this verdict is.** It says only that no repository-coherence defect was found that would
mislead a future session about live project state, corrupt evidence, mutate a historical baseline or
exceed an approved boundary — **after** the current-state corrections recorded in §7 were made.

**What it is not.** It is not a certification that the Canon, Eval or Resources work is
scientifically or technically correct, that any method is sound, that any result would replicate, or
that any threshold is well chosen. Those judgements belong to the owning stream and the Controller.
See `governance/GOVERNOR-CONTRACT.md` §0.

**Seven non-blocking findings are recorded and routed in §6.** None of them changes what is
currently authorised, and none required a domain fix.

---

## 1. Was the branch based on the authorised point?

Yes, exactly.

The Controller authorised GOV-006 against `main` at `91984f50b294f11aefc7065f5ad11f9e0d3e2b9a`.
At worker start `origin/main` was at that same commit and
`origin/work/gov-006-post-parallel-reconciliation` pointed at it too. **`main` has not advanced since
authorisation**, so there were no newer Controller decisions to reconcile or to stop for. The whole
audit is against that single tree.

---

## 2. What this review had to settle, in plain terms

Five domain lanes and one governance lane ran in parallel after GOV-005 and all of them have now
landed. The repository's *evidence* moved a long way; the repository's *description of itself* did
not move with it.

Concretely, before this review the three documents a fresh session reads first — `PROJECT-MEMORY.md`,
`coordination/CONTROL-STATE.md` and `coordination/WORKSTREAM-STATUS.md` — still said that no image
had been generated, that no evaluator held benchmark-qualified status, that three lanes were still
open, and that roughly USD 1.30 had been spent. Every one of those statements had become false.

That gap is exactly what the Governor role exists to close, and closing it is the substance of
GOV-006.

---

## 3. Mechanical verification

**Mechanical checks came before prose.** Every number below was derived by the Governor from
committed bytes on the audited tree, not read out of a summary. Where a check could not be performed
from committed material, that is stated rather than glossed.

### 3.1 Capability Registry — 0 rows

| Check | Result |
|---|---|
| Data rows in `eval/registry/registry-v1.jsonl` | **0** (file holds 6 comment lines, no data) |
| `eval/registry/validate_registry.py` | **PASS** — schema valid, registry empty |
| `registry_rows_written` in the EVAL-024 sealed manifest | 0 |
| `registry_rows_written` in the EVAL-030 scoring evidence | 0 |
| `may_populate_registry` in both | `false` |

The Registry is still empty, and it is empty for the reason the Controller gave: `benchmark_qualified`
is deliberately weaker than the Registry's `qualified` / `deterministic` admission bar. **No Registry
row was added, and admission semantics were not touched.**

### 3.2 EVAL-024 — the 16 sealed A-TEXT images

Every artifact was re-hashed from the bytes committed on `main`.

| Check | Result |
|---|---|
| Sealed PNG files present | **16** — 8 under `IMG-01`, 8 under `IMG-02` |
| SHA-256 matches manifest, byte length matches, real PNG magic bytes | **16 / 16** |
| Distinct SHA-256 values | **16** — no duplicate bytes |
| Distinct `coordinate_id` values | **16** — none missing, none repeated |
| `planned_coordinates` set == realised set | **true** |
| `missing_coordinates` | `[]` |
| Media type / dimensions on every record | `image/png`, 1024×1024 |
| `retries`, `evaluator_calls` | 0, 0 |
| `scored` / `sealed_for_later_evaluation` | `false` / `true` |
| Routes | IMG-01 = fal `openai/gpt-image-2` (8), IMG-02 = fal `fal-ai/ideogram/v3` (8) |
| Seed policy | `unseeded` on all 16 |

**Manifest fingerprint independently recomputed.** Re-deriving the SHA-256 over the fingerprinted
fields (`run_id`, `tranche_id`, `frozen_items`, `routes`, `planned_coordinates`, `call_records`,
`artifacts`, `missing_coordinates`, `scored`, `sealed_for_later_evaluation`) reproduces
`1e124343ca46ced8597bdf308d64bd8f139f6bfe9b999d0b81904bf6de948a4c` — byte-identical to the value the
Controller's integration decision records.

**Cost arithmetic reconciles from the call records, not from prose:**

- IMG-01: 8 × USD 0.053 = **USD 0.424**
- IMG-02: 8 × USD 0.060 = **USD 0.480**
- Sum = **USD 0.904** = `total_generation_cost_usd` = `atex_stage_spend_usd`
- USD 1.7357905 (cumulative through EVAL-029) + USD 0.904 = **USD 2.6397905** = the manifest's
  `cumulative_tranche_spend_usd`, matching the Controller decision exactly.

All 16 call records report `api_status: ok`, no ambiguous dispatch, and no retry.

### 3.3 EVAL-030 — scoring consumed those exact bytes and did not regenerate

This is the check that matters most, because "score the sealed images" is worthless if the images
moved underneath the scorer.

| Check | Result |
|---|---|
| Scored coordinate set == sealed coordinate set | **true**, 16 |
| Every scored `artifact_sha256` == the sealed manifest hash | **true** |
| Every scored hash re-derived from the bytes on `main` | **16 / 16** |
| Sealed manifest fingerprint carried into the scoring evidence | matches `1e124343…` |
| `generator_invoked` / `regenerated_anything` | `false` / `false` |
| **Commits touching `sealed-generation-v1/` in all of `main`'s history** | **exactly one** — `55d10a7`, the EVAL-024 generation commit |

That last row is the strongest available proof: the sealed bytes have been written once and never
altered. EVAL-030 added only scoring code and evidence files.

**The headline arithmetic, recomputed from the 16 row-level records:**

| Slice | Recomputed | Declared | Controller decision |
|---|---|---|---|
| GPT Image 2 (IMG-01) | **6 / 8** = 0.750 | 6 / 8 | 6/8 ✔ |
| Ideogram v3 (IMG-02) | **1 / 8** = 0.125 | 1 / 8 | 1/8 ✔ |
| Overall | **7 / 16** = 0.4375 | 7 / 16 | 7/16 ✔ |
| Devanagari | **5 / 8** = 0.625 | 5 / 8 | 5/8 ✔ |
| Latin / Hinglish | **2 / 4** = 0.500 | 2 / 4 | 2/4 ✔ |
| Commercial claim with ₹ | **0 / 4** = 0.0 | 0 / 4 | 0/4 ✔ |

**Spend:** the 16 rows' `evaluator_billed_usd` sum to **USD 0.0240**, and USD 0.904 + USD 0.0240 =
**USD 0.9280** — both matching the Controller decision.

**Uncertainty is carried, not dropped.** Every one of the 16 rows carries the evaluator's own
measured error rates (`evaluator_false_pass_rate`, `evaluator_false_fail_rate`), its contract id and
contract hash, and both status flags (`benchmark_qualified: true`, `strict_exactness_qualified:
false`). `human_review: false` and `target_sent_to_provider: false` on the evaluator block — the
scoring was blind and no human was involved.

The committed evidence package hashes verify, and the 20 EVAL-030 tests pass from this fresh
checkout.

### 3.4 EVAL-029 — durable evidence and deterministic recomputation

This lane existed to close GOV-005 finding **F-1**: completed live evidence that lived only in a
git-ignored local directory and could not be checked by anyone reading GitHub.

**The sealed package is present and intact.** All three files under
`eval/empirical-tranche-1/evidence/EMP-001/text-ocr/` match their recorded SHA-256 and byte length:
the strict Cloud Vision Devanagari source evidence, the completed benchmark qualification result, and
the bounded cost/ledger excerpt.

**The Governor recomputed both scripts' metrics independently**, from the committed observations,
without using the project's own scorer:

| Script | Recomputed by Governor | Accepted / declared |
|---|---|---|
| Devanagari false-pass | 18 / 144 = **0.1250** (6 unique items) | 0.1250 ✔ |
| Devanagari match false-fail | 3 / 144 = **0.0208** | 0.0208 ✔ |
| Devanagari repeat consistency | 96 / 96 = **1.0** | 1.0 ✔ |
| Latin false-pass | 15 / 144 = **0.1042** (5 unique items) | 0.1042 ✔ |
| Latin match false-fail | 0 / 144 = **0.0000** | 0.0000 ✔ |
| Latin repeat consistency | 96 / 96 = **1.0** | 1.0 ✔ |
| Infrastructure failures, both scripts | **0** | 0 ✔ |

**Both gates were then applied by hand, and they behave exactly as the Controller described.** Under
`benchmark_text_ocr_v1` (false-pass ≤ 0.15, false-fail ≤ 0.10, consistency ≥ 0.95, failure ≤ 0.05)
both scripts pass. Under the strict standard — zero mismatch false passes — both fail, because 18 and
15 are not zero. **Both statements are true at once because they answer different questions**, and the
evidence keeps them visibly separate on every record.

**Benchmark and strict remain genuinely distinct artifacts, not relabelled versions of each other.**
The two contract files have different SHA-256 hashes, both matching the sealed manifest
(strict `25602691…`, benchmark `de25e437…`), and the strict contract's last commit predates the
benchmark contract's first commit. **The historical strict result was not rewritten to look like a
pass.**

**The cost excerpt reconciles once double-entry is respected.** A naive sum over its 1,152 rows
doubles the figure, because each trial has both a `reservation` row and a `spend` row. Summing only
`spend` rows gives **USD 0.4320** for Devanagari and **USD 0.4320** for Latin, matching the declared
figures, and every one of the 288 Latin call records resolves to a ledger trial. This is correct
double-entry accounting, not a discrepancy.

**Portability from a fresh clone.** No Python file requires the original machine-local
`emp-001-live` worktree — the only two occurrences of that string in code are inside a test that
*asserts its absence*. The absolute paths that remain in the evidence JSON are declared provenance
metadata. The ten evidence-and-portability tests all pass from this checkout: the package is
committed and complete, manifest hashes match the committed bytes, the manifest fingerprint
recomputes, **both scripts recompute from committed evidence alone**, the cost excerpt traces both
screens, and no committed evidence file contains a credential.

**GOV-005 finding F-1 is therefore resolved for the text-OCR lane.** A fresh clone can now verify and
re-derive the accepted qualification without any local state. That was the single most important
open governance defect in the project, and it is closed.

*One qualification, stated plainly:* five tests in the same file still fail from a fresh clone. They
exercise the **live dispatch path**, which needs rendered Latin images that are deliberately
git-ignored reproducible build products. They do not touch the historical evidence and do not affect
any conclusion above. This is the pre-existing, already-documented rebuild limitation, recorded as
finding **G6-07**.

### 3.5 EVAL-026 — temporal qualification machinery

| Check | Result |
|---|---|
| Deterministic perturbation types | **13**, all distinct ids |
| Temporal capabilities addressed | **9** |
| Do those 9 match the frozen set? | **Exactly.** The frozen `EVALUATOR-QUALIFICATION-MAP.yaml` lists 9 `temporal_video` capabilities and declares 9 in its own family tally; the EVAL-026 set is identical — no capability added, none omitted |
| Full injected-truth coverage | **7** |
| Negative-direction-only | **2** — `action_adherence`, `camera_framing_fidelity` |
| Numeric pass mark | `status: DOES_NOT_EXIST` — **no threshold was invented** |
| `instruments_qualified_by_this_file` / `capabilities_added` / `thresholds_set` / `human_labels` | 0 / 0 / 0 / 0 |
| External calls / spend | 0 / USD 0 |
| Package tests | **153 passed** |
| `validate_package.py` | **PASS** — no network or provider import, no invented pass mark in any module |

The "7 full, 2 negative-direction-only" split is not a prose claim: it is derived from the contract's
own `runnable_on_12_clips` field, which is `true` for seven capabilities and `partial` for exactly
those two. **No temporal evaluator is qualified**, and the harness cannot emit `qualified` — a
self-test against constructed stand-in material correctly returns `unmeasurable` with
`registry_use_permitted: false`.

### 3.6 RES-005 — the temporal perturbation base

Recounted directly from `resources/pre-execution-freeze/mat-av-min/MAT-AV-MIN-MANIFEST.jsonl`:

| Check | Recomputed | Controller decision |
|---|---|---|
| Clips | **12** | 12 ✔ |
| Distinct source works | **12** | 12 distinct works ✔ |
| Distinct content lineage keys / clip hashes | **12 / 12** | — |
| Resources cleanliness screen | **12 / 12 PASS** | 12/12 ✔ |
| Pre-existing freeze runs / black intervals / interlacing | **0 / 0 / 0** | 0 ✔ |
| Licences | CC BY 3.0 ×3, US-Gov public domain ×5, CC BY-SA 4.0 ×2, CC BY 4.0 ×1, CC0 ×1 | within the permitted routes ✔ |

**Documented opportunity counts all reproduce:**

| Population | Recomputed | Decision |
|---|---|---|
| General freeze / reversal base | **12** | 12 ✔ |
| Multi-shot | **6** (cross-checked: 6 clips have `shot_count_measured` ≥ 2) | 6 ✔ |
| On-screen text | **6** | 6 ✔ |
| Product region | **5** | 5 ✔ |
| Rendered-character identity | **4** | 4 ✔ |
| Photographed-face identity | **3** | 3 ✔ |

**The two identity populations really are kept separate**, and more carefully than the headline
suggests. The manifest's `tag_person` field takes four distinct values: `rendered` (4), `real` (3),
`no` (4) and `real_hand_no_face` (1). The clip showing a real hand with no face is deliberately
excluded from the photographed-face population rather than quietly folded into it. That is the right
call and it is visible in the data.

**Ingest scope is stated honestly and is not inflated.** `INGEST-VERIFICATION.md` records **3 of 3**
representative clips accepted by EVAL-026's ingest, names which three and why they were chosen, and
states that the full twelve-clip attempt exhausted local disk mid-write. Nothing on `main` presents
this as 12/12. A repository-wide search for such a claim returns only the Controller's own note that
the original brief overstated it and was corrected before merge, plus GOV-006's own instruction. The
`12/12` figures in `VERIFICATION-EVAL-026.md` are a self-test against constructed stand-in clips that
correctly returns `unmeasurable` — not real-clip ingest.

**Raw media is honestly represented as transient.** The clips themselves are git-ignored, and what is
committed is hashes, provenance, licence records, retrieval scripts, measurements and lineage —
enough to establish the acquisition record and to rebuild.

### 3.7 The three cross-stream reconciliation commits

All three named in the Controller's RES-005 decision are ancestors of the audited `main`:

| Commit | Subject | Effect |
|---|---|---|
| `c049cfe` | align temporal ingest example with pack-level material contract | Replaces the "each containing a person, a product and on-screen text" phrasing with the pack-level contract, and renames `pack_ref` from `PACK-AV-CLEAN` to `MAT-TEMPORAL-BASE` |
| `68667c5` | correct temporal qualification material precondition | Rewrites the contract precondition to pack-level and cites the Controller decision by path |
| `88b5a1b` | make family-4 pack-level coverage explicit | Adds `content_coverage_scope: pack_level` and an explanatory note to `RESOURCE-REQUESTS.yaml` |

### 3.8 CANON-011

| Check | Result |
|---|---|
| Cases | **18**, all with distinct ids |
| `runnable_now: true` | **16** |
| `runnable_now: false` | **2** — `MKT-015`, `MKT-016`, matching the Controller's dispositions |
| Source marketplace of all 18 cases | **`upwork`** — buyer jobs only |
| Fiverr material | present only as `fiverr_convention_inputs`, never as a customer-intent case |
| Prompt-ready envelopes | 18 |
| `validate_marketplace_bank.py` | **PASS** — all gates G1–G14 hold |
| Negative controls | **PASS** — 28 deliberately broken fixtures all rejected |
| Grammar gaps | 4 (GG-01…GG-04), status `OBSERVED_AND_ROUTED_NO_CHANGE_MADE` |
| `MEDIA-REQUEST-GRAMMAR-v1.yaml` history | **one commit only** (CANON-010) — untouched by CANON-011 |
| 30-brief authored bank history | **one commit only** — byte-identical, as required |

**The request grammar was not reopened.** The four gaps are recorded as observations with no change
made, exactly as the Controller directed.

### 3.9 Chat-only manual A-TEXT review

**Not present anywhere on `main`.** A repository-wide search for manual/human A-TEXT review language
returns only the prohibition itself in the GOV-006 authorisation, plus an unrelated historical
planning document. The EVAL-030 evidence records `human_review: false` and the EVAL-029 result
records `human_review_required: false`. **Nothing was imported, and this review does not record any
such result as project truth.**

---

## 4. What could not be independently verified

Stated explicitly, because converting worker-reported evidence into Governor-verified evidence is the
failure this role exists to prevent.

1. **That the live provider calls happened as recorded.** The Governor verified internal consistency,
   hashes, arithmetic and the fingerprint chain. It cannot verify from a repository that Google Cloud
   Vision or fal actually returned these bytes on 27 August. Provider identity, routes and prices rest
   on the Controller's own pre-spend verification record.
2. **The exact live billed amounts.** Costs reconcile against the committed ledger excerpt and the
   published per-unit rates; `cost_basis` on the generation records is
   `provisional_planning_rate`, so these are planning-rate figures reconciled internally, not invoice
   figures.
3. **The 12 RES-005 clips' visual content.** The tag counts were recomputed from the manifest. Whether
   a clip tagged `rendered` really shows a rendered character is a Resources judgement the Governor
   did not re-adjudicate, and the raw media is git-ignored.
4. **Whether any of this science is right.** Out of scope by contract.

---

## 5. Programme boundaries — all preserved

Checked against the audited tree; none of the settled lanes moved any of them.

| Boundary | State |
|---|---|
| Product = API-native media production intelligence layer, not a foundation model | Unchanged |
| Primary long-term metric = Cost per Accepted Outcome | Unchanged |
| Creative IR = what should exist; Production IR = how today's tools make it | Unchanged |
| **Production IR still does not exist** | Confirmed |
| **No Planner exists**, and none was built against an empty Registry | Confirmed |
| Capability Registry remains empirical only | Confirmed — 0 rows, admission semantics untouched |
| Canon / books / marketplace research do not prove model capability | Confirmed — CANON-011 sits in `canon/research/`, is not a Canon source, live Canon stays 19 |
| Exact Hindi/text is not a programme-wide blocker | Confirmed |
| Benchmark-grade OCR is not a production exactness certifier | Confirmed — carried on every scored row |
| No mandatory two-human text-review loop | Confirmed — EVAL-028 remains cancelled; `human_review: false` throughout |
| CANON-011 grammar gaps do not reopen the grammar | Confirmed |
| Cheapest reliable production recipe remains the posture | Unchanged |
| No temporal qualification run authorised or performed | Confirmed |

---

## 6. Findings — seven, all non-blocking, all routed

Severity is judged by **what a fresh zero-context session would wrongly believe**, per
`GOVERNOR-CONTRACT.md` §6.

### G6-01 · The temporal spec understates the human-adjudication requirement · Medium · Eval

**Where:** `eval/v1/instruments/temporal-perturbation/PERTURBATION-SPEC.md:221`

**The claim:** *"Four of the nine capabilities are marked `model_based_plus_human` with required
adjudication in the frozen map."*

**The stronger evidence:** `eval/pre-execution-freeze/EVALUATOR-QUALIFICATION-MAP.yaml` marks
**five** — `camera_framing_fidelity`, `motion_action_quality`, `multi_shot_spatial_continuity`,
`sequence_state_continuity` and `technical_visual_integrity`. Four is the count of the *other* group,
the `model_based` capabilities, which suggests the two numbers were transposed.

The spec's own readiness table names the human-adjudication residual for only two of the five
(`sequence_state_continuity`, `technical_visual_integrity`); `camera_framing_fidelity` is covered in
the contract YAML but not the spec table, and `motion_action_quality` and
`multi_shot_spatial_continuity` carry no such note in either.

**Why it matters:** GOV-006 requires that frozen human-adjudication requirements stay explicit before
any temporal qualification. A session designing that run from the spec could drop required
adjudication for up to three capabilities. It misleads about a *future* requirement rather than
current live state, and nothing is currently authorised to run, so it is non-blocking.

**Disposition:** `routed` to Eval. Stream-owned file; the Governor did not edit it. The frozen map
governs where the two disagree.

### G6-02 · No committed cumulative spend figure includes EVAL-030 · Medium · Eval / Controller

**The gap:** the last cumulative EMP-001 figure recorded anywhere on `main` is **USD 2.6397905**,
through the EVAL-024 tranche. EVAL-030's **USD 0.024** evaluator spend is recorded only as a stage
figure. No committed artifact or decision states a consolidated total that includes it.

**Why it matters:** the USD 10 ceiling is a real, mechanically enforced constraint, but a Controller
reading GitHub alone cannot find one authoritative "total consumed to date". The arithmetic is
obvious, which is exactly why it should be recorded rather than inferred by each reader.

**The Governor did not invent the total.** `PROJECT-MEMORY.md` and `CONTROL-STATE.md` now state the
last *recorded* cumulative and the separately recorded EVAL-030 stage figure, and say plainly that a
consolidated post-EVAL-030 figure is not committed.

**Disposition:** `routed`.

### G6-03 · The accepted CANON-011 bank still declares itself not frozen · Medium · Canon

**Where:** `canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml`, `meta.status`

**The claim:** `PROPOSED_WORKER_OUTPUT_NOT_FROZEN`.

**The stronger evidence:** `coordination/decisions/CONTROLLER-CANON-011-INTEGRATION-2026-08-28.md`
records **ACCEPTED AND MERGED** (PR #49, merge `610d69f`).

**Why it matters:** a fresh session opening the bank could conclude it is an unaccepted draft. This is
the same class as GOV-005 finding **F-6** — a status string emitted by a generator that has not been
rerun since the merge. `CONTROL-STATE.md` governs.

**Disposition:** `routed` to Canon. Stream-owned; not edited.

### G6-04 · The Resources handoff says RES-005 is unmerged and unsettled · Medium · Resources

**Where:** `resources/HANDOFF.md:208` and the surrounding section.

**The claims:** RES-005 is *"not merged"*, and the integration-change proposal *"asks the Controller
to settle which of two frozen documents defines MAT-AV-MIN, because they disagree."*

**The stronger evidence:** RES-005 was merged (PR #54, merge `3a49464`) and the Controller settled the
material contract at pack level in
`coordination/decisions/CONTROLLER-RES-005-INTEGRATION-AND-TEMPORAL-MATERIAL-RESOLUTION-2026-08-28.md`,
with three reconciliation commits already on `main` (§3.7).

The same section also describes the unblock as *"nine capabilities, twelve clips, zero annotation"*,
which reads past the human adjudication the frozen map still requires for five of the nine — the same
substance as **G6-01**.

**Disposition:** `routed` to Resources. Stream-owned; not edited.

### G6-05 · The Eval handoff still states ₹0 spend and no checker run · High · Eval

**Where:** `eval/HANDOFF.md`, lines 33, 131, 160 and nearby.

**The claims:** *"₹0 API/model · ₹0 generation · 0 Registry entries"* and *"No checker/model/API call
has occurred and no checker has been selected."*

**The stronger evidence:** cumulative recorded spend is **USD 2.6397905** through EVAL-024 plus USD
0.024 for EVAL-030; **16 images have been generated**; ten evaluator configurations have been
measured; and Cloud Vision holds `benchmark_qualified` status on both scripts.

**Why the severity rose.** This is GOV-005 finding **F-2**, still unresolved, and it is now
substantially more wrong than when it was first raised — at GOV-005 no image existed and no evaluator
was benchmark-qualified. The project's own session-start guidance sends Eval workers to this file
second. Its "₹0 generation" line is now contradicted by 16 committed PNGs in the same stream.

It remains non-blocking only because `PROJECT-MEMORY.md` and `CONTROL-STATE.md` both explicitly warn
that this handoff is stale on spend and qualification state, and both govern where they differ.

**Disposition:** `routed` to Eval, **escalated**. Stream-owned; not edited.

### G6-06 · The Canon handoff does not mention CANON-011 · Low–Medium · Canon

**Where:** `canon/HANDOFF.md` — zero occurrences of `CANON-011`.

A Canon worker following the prescribed reading order would not learn from their own handoff that 18
marketplace-derived buyer cases exist and are now the preferred real-demand pool for Stage-C
selection. Live Canon is correctly still 19 sources, so no count is wrong — the file is incomplete
rather than false, which is why this sits below the others.

**Disposition:** `routed` to Canon. Stream-owned; not edited.

### G6-07 · Five live-dispatch tests fail from a fresh clone · Low · Eval

**Where:** `eval/empirical-tranche-1/tests/test_benchmark_text_ocr.py` — five tests exercising the
live Latin dispatch path.

Running the file from this fresh checkout gives 25 passed, 5 failed. All five fail with the same
`FileNotFoundError`: the rendered Latin pack images are git-ignored reproducible build products, and
one of them needs the pinned proprietary Arial render.

**This does not affect any historical result.** The ten tests that verify the sealed evidence, the
manifest hashes, the fingerprint and the recomputation of both scripts all pass without any local
state — which is what the Controller's merge gate actually required. This is the long-standing,
already-documented rebuild limitation, not new breakage.

**Disposition:** `routed` as a note. No action proposed; recorded so a future session does not read a
red test run as evidence corruption.

---

## 7. Current-state corrections made under GOV-006

Four files were corrected, all within the Governor's write boundary
(`PROJECT-MEMORY.md`, `governance/**`, and factual current-state corrections in `coordination/**`
where an approved governance task includes that scope — GOV-006 §D does).

| File | What was false | What it says now |
|---|---|---|
| `PROJECT-MEMORY.md` | Presented CANON-011, EVAL-024 and EVAL-029 as open lanes; "0 A-TEXT image generations"; "0 benchmark-qualified"; cumulative spend USD 1.3037905; EVAL-026, EVAL-030 and RES-005 absent; F-1 shown as unresolved | Six settled lanes described as merged with their verified results; the sealed evidence and its recomputation path named; F-1 recorded as resolved for the text-OCR lane; spend stated as last-recorded plus the separate EVAL-030 figure |
| `coordination/CONTROL-STATE.md` | "EVAL-024 still has no live artifacts"; "A-TEXT still has no generated artifacts and remains unscored"; EVAL-029 "not merge-ready"; three lanes listed as authorised/active | Records all six integrations, the 16 sealed artifacts, the 7/16 benchmark result, Registry still 0, and the temporal prerequisites that remain |
| `coordination/WORKSTREAM-STATUS.md` | Same stale lane table, spend and empirical floor; Governor row said GOV-005 awaiting merge | Per-stream state refreshed to the settled tree; GOV-005 shown closed and merged, GOV-006 as the current round |
| `governance/README.md` | Pinned to `main` at `8990a7a` with three lanes running | Pinned to `91984f5`; GOV-006 added to the task history |

**Nothing else was touched.** No domain artifact, no threshold, no Registry file, no stream handoff or
task file was edited. `coordination/DECISION-LOG.md` was deliberately left unchanged: the Controller
settled at GOV-005 (finding F-5) that it is a curated historical and navigation index and is not to be
back-filled, and its own scope notice already says so accurately.

**Historical records were preserved, not corrected.** `governance/reviews/GOV-005-…` still carries the
USD 1.3037905 figure that was correct when written. Superseding is allowed; silent mutation is not.

---

## 8. Can a fresh zero-context Controller now reconstruct the settled state from GitHub alone?

**Yes for the settled empirical state — and this is the first time in the project that has been true
of a completed paid result.**

A fresh session reading `PROJECT-MEMORY.md` → `coordination/CONTROL-STATE.md` → the decision records
can now find, and independently re-derive from committed bytes:

- the 16 sealed A-TEXT images, their hashes and their manifest fingerprint;
- that EVAL-030 scored those exact bytes without regenerating anything;
- the 6/8, 1/8 and 7/16 result, recomputable from row-level evidence;
- the Cloud Vision Devanagari and Latin benchmark metrics, recomputable from sealed observations,
  with the benchmark-versus-strict distinction preserved on every record;
- the qualification-stage cost trace;
- EVAL-026's 13 perturbation types and 9 capabilities, with no invented pass mark;
- RES-005's 12 clips, their cleanliness screen and every documented opportunity count;
- that the Registry holds 0 rows and why.

**Three honest limits on that "yes":**

1. **Stream handoffs still mislead** (G6-04, G6-05, G6-06). A worker who follows the prescribed
   reading order — charter, then handoff — reaches a stale document before a current one. The
   control-plane documents warn about this and govern, but the warning has to be read first.
2. **No single committed figure states total spend to date** (G6-02).
3. **The reconstruction is of the settled *state*, not of the live run.** The EMP-001 mutable ledger
   remains local by design, and the Devanagari battery and Latin pack still cannot be rebuilt from a
   clone without the pinned proprietary font.

The recorded state is now materially more reconstructible than at GOV-005, when no live evidence at
all was committed. **The remaining gap is in the stream-owned files the Governor may not edit**, which
is why those three findings are routed rather than fixed.

---

## 9. Return to Controller

| | |
|---|---|
| **Verdict** | **PASS WITH NON-BLOCKING NOTES** |
| **Audited `main`** | `91984f50b294f11aefc7065f5ad11f9e0d3e2b9a` |
| **Branch** | `work/gov-006-post-parallel-reconciliation` — pushed, **not merged** |
| **Blocking findings** | **None** |
| **Non-blocking findings** | 7 — G6-01 … G6-07 (§6), all routed |
| **Registry rows** | 0, unchanged |
| **Spend** | USD 0 |
| **GOV-005 F-1** | **Resolved** for the text-OCR lane |

**No decision is required of the Controller by this review.** The routed findings are for the owning
streams; only the Controller may open tasks for them.
