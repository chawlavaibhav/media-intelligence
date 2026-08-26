# Resources V1 correction pass — Controller Brief

**Task:** `resources/tasks/RESOURCES-V1-CORRECTION-PASS.md` (R-C1 … R-C5)
**Date:** 26 Aug 2026 · **Branch:** `work/resources-v1-overnight` · **Not merged to `main`**
**Session:** cloud-browser, no laptop access, **no raw corpus**
**Status:** all five corrections complete · **0 acquisition · ₹0 / $0 spend**

**Re-verify everything in one command:** `bash resources/v1/validators/run_all.sh`
→ executed from a clean state after deleting `resources/v1/build/`: **exit 0, ALL CHECKS PASSED.**

---

## 1. What changed, in one table

| ID | Controller finding | Status | Proof |
|---|---|---|---|
| **R-C1** | "15/36 need nothing from Resources, ever" was misleading | **done** | wording precise in both places; 1/10/5/3/17 arithmetic unchanged |
| **R-C2** | Resources must own one canonical persistent storage contract | **done** | schema v2: attempt/artifact/measurement/acceptance; 13 negative controls |
| **R-C3** | Deterministic generated artifacts bloat Git | **done** | `resources/v1` tracked size **34.5 MB → 322 KB**; determinism proved by fingerprint |
| **R-C4** | Unknown source lineage must fail closed | **done** | new exit 3 (INDETERMINATE); 4 negative controls |
| **R-C5** | Fold Eval refinements into the four packs | **done** | 14 composition requirements added; **pack count unchanged at 9** |

**Nothing in R1–R5/R8 was redesigned.** The 36-row classification, the 48 requirement rows, the four
packs, the three lineage levels and the corpus rebaseline are all as accepted.

---

## 2. R-C1 — the 15/36 headline

**Replaced everywhere** (`RESOURCE-REQUIREMENTS.md` §1, overnight Controller Brief §3) with:

> **15 of 36 capabilities require no capability-specific external stimulus pack; some still inherit
> evaluator-calibration dependencies.**

**Arithmetic preserved exactly, and re-verified by the validator:** 1 available + 10
`constructed_by_eval` + 5 `no_external_resource` + 3 partial + 17 missing = 36. **No row was
reclassified to fit the wording** — that would have been fixing the evidence to match the sentence.

Both documents now spell out the two dependency kinds the old phrasing hid:

- **Evaluator-calibration dependencies.** `REQ-CAP-04` `action_adherence` is the clearest case: its
  stimulus is `constructed_by_eval`, but it has no deterministic checker, so it depends on the
  structured-VLM and temporal evaluator families — both blocked on missing packs. **No pack of its
  own, and still not measurable today.**
- **Archive dependencies.** All five `no_external_resource` rows are storage class C. `cost_and_cpao`
  is unmeasurable if the archive is incomplete, however many generations are paid for.

The correction in the overnight brief carries an explicit note that it was corrected under R-C1, so
the record shows what was said and what replaced it.

## 3. R-C2 — one canonical persistent storage contract

`EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` is now **v2** (same path — stability preferred over a
rename, as instructed). Four persistent entities:

```
attempt ──▶ artifact (0 or 1) ──▶ measurement (many)
   │                          └──▶ artifact (derived: frames, transcodes)
   └──▶ acceptance (0 or 1, per trial)
```

**The v1 defect this corrects.** v1 had one row that was written when a call was made and carried a
null output hash if it failed. That conflates the **call** (which always happened, always cost money,
always is evidence) with the **bytes** (which may not exist). Now a refusal is a first-class attempt
row with no artifact, and a sampled frame is a derived *artifact* rather than a second *attempt*.

**Failed attempts survive individually.** Aggregate reliability counters are explicitly rejected, and
the validator fails an archive whose summary disagrees with its rows (negative control
`04-aggregate-counter-replaces-preserved-rows`). A count of "5 refusals" cannot say which items were
refused, what they cost, or whether the pattern is systematic.

**Observation units are the canonical vocabulary, verbatim:**
`frame | shot | shot_pair | sequence | whole_asset | asset_set_over_time`.
The v1 Resources-invented terms — `image`, `sampled_clip`, `whole_clip`, `asset_set` — are now
**explicitly rejected by name** (negative control `01`). Derived media is described in
`artifact.derivation`, not by redefining an observation unit. `capability_id` is stored exactly as
Eval defines it and is never renamed, normalised or mapped.

**Repeat and retry are separate concepts**, and the validator enforces it:

| | `repeat_index` | `retry_of_attempt_id` |
|---|---|---|
| What it is | deliberate experimental repeat, planned before any result is seen | repair attempt caused by a prior failure or rejection |
| Measures | reliability (`pass_at_k`) | reaching an acceptable outcome |
| In a retry chain | **never** | **always** |

Count repeats as retries and **every CpAO figure is inflated by the experimental design itself**;
count retries as repeats and `pass_at_k` runs over attempts that were not independent draws. Both are
silent and neither is recoverable after the fact. Negative control `05` fails an acceptance whose
retry chain contains a repeat.

**Published:** `resources/v1/EVAL-STORAGE-HANDOFF.md` — the exact field contract Eval must emit,
including the three open items Eval should confirm (`lane` vocabulary, `absence_reason` coverage, the
byte budget that waits on E2). **No Eval code was implemented.**

**Scale proof, from a clean state:** 1,000 attempts · 1,126 artifacts (966 direct + 160 derived
frames) · 5,796 measurements · 250 acceptances · **0 duplicate media copies** · **fan-out 6.00**
measurements per artifact · 34 refusals/errors each preserved with its verbatim reason. Everything
synthetic; fictional vendor and model names; **no provider called, no money spent.**

## 4. R-C3 — generated Git bloat removed

**`resources/v1` tracked size: 34.5 MB → 322 KB.** Net −46,789 lines.

Removed from Git: nine view `.jsonl` files (~31 MB) and the three 1,000-artifact archive files
(~3.7 MB). Both are now generated into `resources/v1/build/`, which is git-ignored.

**Kept in Git**, exactly as the task specifies: the generators and validators, the schemas, the
expected counts and deterministic fingerprints, small representative fixtures, every deliberate
negative control, and the human-readable reports.

**Determinism is proved, not assumed.** `views/view-fingerprints.json` holds each view's item count,
content-group count and SHA-256 plus a combined fingerprint; `build_views.py` rebuilds and compares.
`views/SAMPLE-RECORDS.jsonl` keeps one record per view showing the shape. **Negative-controlled:**
tampering with a single committed fingerprint makes the check exit 1.

**This is not the reproducibility hole the project has been bitten by twice.** EVAL-005's `build/`
items and the legacy spike's generated media were irreproducible because they depended on assets
*outside* git — a proprietary font, raw media. These build products depend only on
`corpus-pilot-v0.jsonl` and `lineage_keys.py`, both committed. The distinguishing test is whether an
artifact needs anything git does not hold.

**The class-C rule is explicitly not weakened.** The `.gitignore` entry says so in place:
*"Irreplaceable class-C model outputs are NOT covered by this rule and must never be git-ignored."*
The same sentence appears in `VIEWS.md`. What is ignored is deterministic proof output, never paid
model output.

## 5. R-C4 — unknown lineage cannot be certified independent

An unregistered source yields `lin_unknown::<source_id>`. **Finding two such keys different
establishes nothing** — two unregistered sources may be the same lab, the same collection effort, or
one derived from the other. Treating "different unknown keys" as "independent" is precisely how an
unregistered source gets silently certified as a clean holdout.

The validator now refuses to certify, as its own outcome:

| Exit | Meaning |
|:--:|---|
| **0** | Checked. No collision **and every lineage established.** |
| **1** | Checked. **Leak found** — a DATA INTEGRITY stop. |
| **2** | **Could not check** — bad input, missing view, unknown item id. |
| **3** | **INDETERMINATE** — independence not established. **Not clean, not a leak.** |

The existing "problem found" vs "could not check" distinction is preserved; exit 3 is added rather
than folded into either.

**Four negative controls, all passing**, over a 36-row synthetic fixture manifest so no real corpus
item is involved:

| Control | Setup | Expected | Result |
|---|---|:--:|:--:|
| `LINEAGE-NC-01` | two registered, genuinely independent lineages | 0 | **PASS** |
| `LINEAGE-NC-02` | one shared registered lineage (the CVIT pair) | 1 | **PASS** |
| `LINEAGE-NC-03` | unregistered source in a protected role | 3 | **PASS** |
| `LINEAGE-NC-04` | **two *different* unknown lineages** | 3 | **PASS** |

`NC-04` is the case that motivates the correction. `NC-01` matters equally: without a case that
legitimately passes, the other three would be satisfied by a tool that refuses everything.

Registering a source is a deliberate human judgement — add it to `SOURCE_LINEAGE` in
`validators/lineage_keys.py` before using it in a protected role.

## 6. R-C5 — Eval refinements folded in, no scope explosion

**Pack count unchanged at 9. Targets unchanged. No fifth acquisition family.** 14 composition
requirements were added to the four missing packs, constraining *how the same assets are composed*:

- **Product (≥48 = 12 × ≥4):** same-category **non-match decoys** (≥2 similar products per category —
  a checker that tells a shoe from a kettle has shown nothing); **declared brand-colour reference
  values** plus capture lighting; **difficulty coverage** for curved surfaces, oblique angles and
  logo-on-surface.
- **Person (≥32 = 8 × ≥4):** identities must support known-match and known-non-match, including **at
  least one plausibly confusable pair**. **No public-face scraping**, reaffirmed as absolute.
- **AV (36 = 24 + 12):** **explicit turn boundaries with speaker attribution** on all 12 two-speaker
  clips; **≥12 clean clips reused as the temporal-perturbation base** instead of a fifth pack.
  Resources records the consequence: those reused clips **share content lineage with their AV
  originals** and cannot be an independent holdout for a speech measurement that also uses the
  original. `PACK-TEMPORAL-PERTURB-BASE` is now marked `superseded_by_when_available: PACK-AV-CLEAN`.
- **Commercial (80 = 60 + 20):** the **20-asset reserve is frozen before** any tuning touches the 60
  active. Eval or its reviewers may later establish a **≥15 known-clean subset** for false-criticism
  calibration — **Resources supplies candidates, rights and provenance and must not author that
  label**, because "clean" is a creative-quality judgement.

Every pack carries an explicit `resources_boundary` naming what Resources records versus what it must
never decide (tolerances, thresholds, similarity cut-offs, creative labels).

**Nothing was acquired.** `MISSING-PACK-SUPPLY-ROUTES.md` carries the same refinements and states that
targets are unchanged.

---

## 7. Tests run in this pass

All executed in this cloud session, from a clean state (`resources/v1/build/` deleted first):

| Suite | Result |
|---|---|
| `run_all.sh` (7 steps) | **exit 0 — ALL CHECKS PASSED** |
| Requirements matrix vs YAML source of truth | 36/36 capabilities, 6/6 families, 48 rows |
| Corpus rebaseline from the committed manifest | **46 pass, 0 fail, 1 warn** |
| Views rebuild vs committed fingerprints | **9/9 byte-identical**, combined sha256 `27aba5a4…` |
| Fingerprint tamper (negative control) | **correctly exit 1** |
| Allocation leakage — clean cross-lineage split | exit 0 |
| `DUMMY-02` content-leak negative control | **correctly exit 1** (551/551 contaminated) |
| `DUMMY-03` same split at byte level | **correctly exit 0** — the contrast case |
| R-C4 lineage negative controls | **4/4 as declared** |
| Empirical archive at 1,000 attempts | exit 0, fan-out 6.00, 0 duplicate copies |
| Archive negative controls | **13/13 as declared, each failing for its declared reason** |

*(Superseded count: the integration pass RI-C1–RI-C4 added nine more, taking the archive suite to
22/22. This table records what the correction pass itself ran and is left as-is — historical results
are not rewritten to match later numbers. See
`RESOURCES-EVAL-STORAGE-INTEGRATION-CONTROLLER-BRIEF.md`.)*

**Total: 17 deliberate negative controls, all behaving as declared.** The archive runner asserts not
just that a case fails but that the failure names the right rule — a case failing for the wrong
reason is not a passing negative control.

**Nothing is claimed as PASS that was not executed.** Where a check could not run, it exits 2 and is
reported as unrun.

## 8. Residual blockers — unchanged by this pass

- **The raw 5.70 GB corpus is not in this session.** No media file was opened. "34,786/34,786 decode
  cleanly" remains **prior committed evidence**, not a cloud re-run.
- **The BSTD 351-vs-364 discrepancy is still open.** The rebaseline still reports it as the single
  warning. Settling it needs the raw annotation files. **Not silently corrected in either direction.**
- **GOV-001 R3 is still untouched** — `build_reports.py` exits 0 on a degraded report. It was outside
  this pass's scope and needs its own Controller-assigned task. **It was not run**, since running it
  in a corpus-less session is what destroys the committed integrity evidence.
- **Official rights verification still cannot be completed here** — the egress proxy blocks direct
  fetches of official distribution pages. The ABO licence contradiction (CC BY-NC 4.0 vs CC BY 4.0)
  remains **blocked pending human verification**, not guessed.
- **All four packs remain blocked on a human decision** — consent, permission or capture. None was
  attempted.

## 9. Files changed

**Modified:** `resources/v1/RESOURCE-REQUIREMENTS.md` (R-C1) · `resources/v1/resource-requirements.yaml`
(R-C5) · `resources/v1/MISSING-PACK-SUPPLY-ROUTES.md` (R-C5) ·
`resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` (R-C2, v2) · `resources/v1/EMPIRICAL-ARCHIVE.md`
(R-C2/R-C3) · `resources/v1/RESOURCE-ALLOCATION-SPEC.md` (R-C3/R-C4) · `resources/v1/views/VIEWS.md`
(R-C3) · `resources/findings/RESOURCES-V1-OVERNIGHT-CONTROLLER-BRIEF.md` (R-C1) ·
`validators/lineage_keys.py`, `check_allocation_leakage.py`, `build_views.py`,
`check_empirical_archive.py`, `make_dummy_archive.py`, `run_all.sh` · `.gitignore`

**Added:** `resources/v1/EVAL-STORAGE-HANDOFF.md` · `views/view-fingerprints.json` ·
`views/SAMPLE-RECORDS.jsonl` · `fixtures/empirical-archive-negative-controls/CASES.yaml` ·
`fixtures/lineage/` (manifest + README) · 4 `LINEAGE-NC-*.yaml` allocations ·
`validators/run_archive_negative_controls.py` · `validators/run_lineage_negative_controls.sh` ·
this brief

**Deleted from Git (now build products):** 9 view `.jsonl` files · 3 dummy-archive `.jsonl` files

## 10. Compliance statement

- **0** source families acquired. **0** downloads. **0** logins, accounts, forms, terms acceptances,
  emails, purchases or consent actions. **₹0 / $0** spent.
- **0** media files opened from the raw corpus; **0** laptop paths accessed.
- **0** rows reclassified to fit corrected wording. **0** new acquisition families created.
- **0** creative labels, thresholds, tolerances or acceptance decisions authored by Resources.
- **0** protected roles assigned — every view still carries
  `unassigned_pending_eval_experiment_split`.
- **0** later tasks started (R6/R7/R9 untouched). **0** files changed outside `resources/` and
  `.gitignore`.
- **0** Eval code implemented — `EVAL-STORAGE-HANDOFF.md` states a contract only.
- **Not merged to `main`.**

## 11. Completion criteria

| # | Criterion | Met |
|:--:|---|:--:|
| 1 | 15/36 wording precise everywhere | ✅ |
| 2 | One canonical attempt/artifact/measurement/acceptance contract under Resources | ✅ |
| 3 | Observation units match the canonical vocabulary exactly | ✅ |
| 4 | Repeats and retries are separate concepts | ✅ |
| 5 | Failed/refused attempts survive individually | ✅ |
| 6 | Deterministic large artifacts removed from Git, rebuilt by validation | ✅ |
| 7 | Unknown lineage cannot be certified independent | ✅ |
| 8 | Four packs incorporate the refinements without scope explosion | ✅ |
| 9 | Full validator suite and negative controls freshly run | ✅ |
| 10 | This correction brief exists | ✅ |
