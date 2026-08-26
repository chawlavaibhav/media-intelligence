# EVAL–RESOURCES STORAGE INTEGRATION PASS

**Status:** AUTHORIZED final bounded integration correction on `work/eval-v1-overnight` only.  
**Purpose:** make the corrected Eval harness emit the exact Resources v2 persistence contract and close remaining Controller code-review defects before merge.  
**Spend:** ₹0. No paid API/model/evaluator call, no instrument qualification, no empirical Registry population, and no merge to `main`.

## Zoom-out

Eval owns the meaning of capabilities/instruments and the empirical measurements. Resources owns persistent evidence storage. Both streams now agree conceptually on four durable records: **attempt → artifact → measurement → acceptance**. The remaining problem is exact compatibility: the current Eval JSONL emission does not satisfy Resources v2 required fields/vocabularies.

Do not restart E1–E5 or redesign the harness. This is a final interface hardening pass.

## Controller decisions

### EI-C1 — Conform exactly to Resources v2

Fetch/read the latest `work/resources-v1-overnight` versions of:
- `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml`
- `resources/v1/EVAL-STORAGE-HANDOFF.md`
- `resources/v1/validators/check_empirical_archive.py`

Emit exactly what that corrected contract requires after its RI integration update. Do not preserve a parallel Eval vocabulary.

### EI-C2 — Trial semantics: one call = one trial

One provider/API generation/transform call is one trial. Every repeat and every retry is a distinct trial. Derived media adds artifacts, not trials.

Emit a `trial_id` on every attempt and artifact/measurement. It may equal `attempt_id`; otherwise prove one-to-one uniqueness. A production retry links to the previous attempt but never shares its trial id. A deliberate repeat likewise gets its own trial id.

### EI-C3 — Required attempt provenance

The persistent attempt row must include the Resources-required fields, including:
- `trial_id`
- `prompt_hash` of the exact prompt text sent
- canonical `status` (`ok | error | refusal | timeout | cancelled`)
- `cost_ref`
- `storage_class`
- exact provider/model/version/endpoint/workflow/lane/config/reference/timestamps
- repeat/retry metadata.

Exact lane ids for V1:
`image | general_video | native_av | lipsync | tts`.

If the internal harness keeps `refused`, map it to persistent `refusal`; do not make Resources accept two synonyms.

Add a minimal synthetic cost ledger for self-tests so `cost_ref` resolves. Do not invent real-provider prices.

### EI-C4 — Artifact fields

Emit Resources' required artifact fields:
`artifact_id`, `attempt_id`, `trial_id`, `output_hash`, `output_bytes`, `output_location`, `media_kind`, `storage_class`.

For derived media use the exact derivation contract (`derived_from_artifact_id`, `derivation_type`, `derivation_params`) and preserve the parent's attempt/trial id.

No machine-specific absolute paths.

### EI-C5 — Measurement fields and absence semantics

Emit the flat Resources-required measurement provenance fields rather than a nested competing shape:
`measurement_id`, `artifact_id` (nullable only where genuinely trial-level), `trial_id`, `capability_id`, `instrument_ref`, `instrument_version`, `instrument_config_hash`, `instrument_qualification_ref`, `observation_unit`, `measured_at`, `result`, `absence_reason`, plus optional defects/cost refs.

Canonical V1 `absence_reason` set:
`not_applicable | not_measured | instrument_unavailable | parse_failure | human_adjudication_pending | other`.

Rules:
- provider refusal/error/timeout lives on the attempt, not a measurement absence;
- `instrument_unqualified` is not an absence; store the observational result with `instrument_qualification_ref: required_but_no_calibrated_instrument` and keep it out of Registry scores;
- exactly one of `result` and `absence_reason` is non-null.

### EI-C6 — Fix operational cost accounting

`operational_metrics()` currently sums generation cost over produced artifacts/provenance, which omits failed/refused/timeout attempts. Cost was incurred by the call even when no bytes exist.

Compute total provider/transform call cost from **attempt records**, not successful artifacts. Preserve separate lines for generation/transform/evaluator/human where applicable.

Also correct any misleading `cost_in_retry_chains` naming/calculation: the cost of an accepted retry chain includes its originating attempt plus retries. If no acceptance exists yet, do not pretend a full CpAO chain cost has been computed. Either expose accurately named `cost_of_retry_attempts` or compute complete chains only where an acceptance/retry chain is present.

Add regression tests with a refused attempt carrying non-zero synthetic cost and prove it survives totals.

### EI-C7 — Tighten Registry repeat/measurement structure

Current homogeneity hardening is good but still permits two silent inflation cases.

Before writing a Registry row enforce:
1. exactly one scoreable measurement per trial for that capability/instrument cell; duplicate measurements of the same trial are refused;
2. the observed trial structure exactly matches `repeats_per_item`, not merely `observed_max <= declared`;
3. every included base item contributes the declared number of non-retry experimental trials, or the row is explicitly a different incomplete design and cannot claim that `repeats_per_item` value;
4. `trials == n_items * repeats_per_item` for a balanced qualification cell unless the schema explicitly records a justified unbalanced design. V1 qualification should stay balanced.

Derive/validate repeat counts from provenance. Do not trust the caller.

Add negative controls for:
- declared 2 repeats with only 1 observed;
- duplicate measurement for one trial;
- one item having fewer repeats than another;
- a retry masquerading inside the repeat cell.

### EI-C8 — Cross-branch validation is the real completion gate

After emission is corrected, validate the Eval dummy archive with **Resources' actual validator from `work/resources-v1-overnight`**. Use a temporary worktree/fetch if needed; do not copy a second validator into Eval.

Required end-to-end result:

> Eval dummy generation → canonical JSONL handoff → Resources `check_empirical_archive.py` → exit 0.

Also run the Eval harness self-test and all prior correction suites. If the Resources branch changes while you work, refresh it before the final cross-branch validation.

## E2 remains separate

Do not invent model ids/prices. The unresolved official-provider lookup is not part of this interface correction and does not block the storage contract from becoming merge-ready.

## Completion

Write `eval/findings/EVAL-RESOURCES-STORAGE-INTEGRATION-CONTROLLER-BRIEF.md` with exact commands/results, including the Resources branch SHA/schema version used for validation. Commit and push to the existing branch. Do not merge.