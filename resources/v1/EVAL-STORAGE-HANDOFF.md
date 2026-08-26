# Eval → Resources storage handoff: the exact field contract Eval must emit

**Owner:** Resources · **Task:** R-C2 of `RESOURCES-V1-CORRECTION-PASS.md` · **Date:** 26 Aug 2026
**Schema:** `EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml` (v2) · **Validator:** `validators/check_empirical_archive.py`

---

## The split, in one line

**Resources owns persistence. Eval owns meaning.**

Resources decides how evidence is stored and what may never be lost. Eval decides what a capability
means, what an instrument's result means, what a threshold is, and whether an outcome is acceptable.
Where this contract names a `capability_id`, an instrument or an observation unit, **Resources is
storing Eval's vocabulary verbatim** — it does not define, rename, normalise or map any of it.

**This document does not implement anything in Eval.** It states the fields Eval must emit so the
archive is valid.

## Four entities, one shape

```
attempt ──▶ artifact (0 or 1) ──▶ measurement (many)
   │                          └──▶ artifact (derived: frames, transcodes)
   └──▶ acceptance (0 or 1, per trial)
```

Emit four JSONL files per archive: `attempts.jsonl`, `artifacts.jsonl`, `measurements.jsonl`,
`acceptances.jsonl`.

### Why attempt and artifact are separate

The **call** and the **bytes** are different facts. A call always happened, always cost money and
latency, and is always evidence. Bytes may not exist. Keeping them in one row (the v1 design) forced
a refused call to be stored as an artifact-shaped hole with a null hash. Now a refusal is a
first-class attempt row with no artifact, and a sampled frame is a derived *artifact* rather than a
second *attempt*.

## What Eval must emit

### 1. `attempts.jsonl` — one row per provider/API/transform call

Required: `attempt_id`, `trial_id`, `eval_item_id`, `provider`, `model_id`, `model_version`,
`endpoint`, `workflow`, `lane`, `prompt_hash`, `config_hash`, `config_location`,
`reference_asset_hashes`, `requested_at`, `completed_at`, `status`, `cost_ref`, `storage_class`,
`repeat_index`.

`status` ∈ `ok | error | refusal | timeout | cancelled`.

**Write the row when the call is made, not when it succeeds.**

Three rules that exist because breaking them loses evidence permanently:

- **Every failed or refused attempt is emitted individually, with `error_detail` carrying the
  provider's verbatim text.** An aggregate reliability counter is **not** acceptable and the validator
  rejects a summary that disagrees with the rows. A count of "5 refusals" cannot tell you which items
  were refused, what they cost, or whether the pattern is systematic.
- **`cost_ref` points at a recorded ledger line.** Never an invented number; a modelled estimate is
  labelled as one.
- **`config_location` must be resolvable.** A hash proves the config was the one used; it cannot be
  read back.

### 2. Repeat vs retry — the distinction that protects two different metrics

These are **not interchangeable** and the validator enforces it.

| | `repeat_index` / `repeat_of_attempt_id` | `retry_of_attempt_id` / `retry_reason` |
|---|---|---|
| What it is | A **deliberate experimental repeat**, planned before any result is seen | A **production/repair attempt caused by a prior failure or rejection** |
| Why it exists | To measure reliability (`pass_at_k`) | To reach an acceptable outcome |
| Retry chain | **Never** | **Always** |

`repeat_index` is required on every attempt. `retry_of_attempt_id` is set **only** when the call
exists because a prior one failed, and then `retry_reason` is required too.

**Why this matters concretely.** Cost per Accepted Outcome divides the cost of a retry chain by
accepted outcomes. If deliberate repeats were counted as retries, **every CpAO figure would be
inflated by the experimental design itself**. If retries were counted as repeats, `pass_at_k` would
be computed over attempts that were not independent draws. Both errors are silent, and neither is
recoverable after the fact.

### 3. `artifacts.jsonl` — one row per set of bytes

Required: `artifact_id`, `attempt_id`, `trial_id`, `output_hash`, `output_bytes`, `output_location`,
`media_kind`, `storage_class`.

- `status: ok` ⟺ exactly one direct artifact. Any other status ⟺ none.
- `output_hash` is **never null** — an artifact *is* its bytes. If bytes were not retained, emit no
  artifact row and let the attempt record why.
- The same `output_hash` must not appear at two `output_location`s. That is a duplicate copy, not two
  artifacts.

**Derived media** — a sampled frame, transcode, crop or segment — sets `derived_from_artifact_id`,
`derivation_type` and `derivation_params`, and **inherits its parent's `trial_id` and `attempt_id`**.
It never gets its own. Ten frames sampled from one clip are ten artifacts of **one** trial; letting
each claim a trial would inflate every downstream sample size by an order of magnitude.

### 4. `measurements.jsonl` — many per artifact

Required: `measurement_id`, `trial_id`, `capability_id`, `instrument_ref`, `instrument_version`,
`instrument_config_hash`, `instrument_qualification_ref`, `observation_unit`, `measured_at`, plus
`artifact_id` unless the measurement is defined over a whole trial.

**`capability_id` is emitted exactly as Eval defines it**, from the canonical 36-capability map.
Resources stores the string and never transforms it.

**`observation_unit` must be one of the canonical vocabulary, verbatim:**

```
frame | shot | shot_pair | sequence | whole_asset | asset_set_over_time
```

The validator **rejects** `image`, `sampled_clip`, `whole_clip`, `asset_set` and any other local
coinage. Those were a Resources-invented vocabulary in v1 and are now explicitly forbidden: a local
synonym silently breaks comparability between two measurements that should be comparable. If you need
to describe *derived media*, that belongs in `artifact.derivation`, not here.

**Exactly one of `result` and `absence_reason` is set** — never both, never neither. A measurement
that could not be taken is evidence too; `absence_reason` ∈ `not_applicable | instrument_unavailable
| parse_failure | human_adjudication_pending | other` keeps it from becoming a silent gap.

`defects` is a **list**: multiple defects per artifact are permitted and expected. Collapsing an
artifact to one salient label is exactly what the Eval master plan identifies as the flaw in the
legacy failure records.

`evaluator_cost_ref` is separate from the attempt's `cost_ref`, so evaluator spend never hides inside
generation spend.

An unqualified instrument still emits its measurement, carrying
`instrument_qualification_ref: required_but_no_calibrated_instrument`. Storing it is correct;
**reporting it as a capability score is not.**

### 5. `acceptances.jsonl` — one per trial that reached a decision

Required: `acceptance_id`, `trial_id`, `accepted`, `decided_by`, `decided_at`, `brief_ref`.
Optional: `rejection_reasons` (a list), `retry_chain`.

**`decided_by` is never Resources**, and the validator rejects it. Resources stores the decision; a
human or an Eval process makes it.

`retry_chain` contains **retries only**, built from `retry_of_attempt_id` links. A deliberate
reliability repeat in a retry chain is a hard failure.

## What Resources guarantees in return

- Every emitted attempt, artifact, measurement and acceptance is retained under **storage class C**,
  durably, **regardless of the result**. Deleting rejected outputs after scoring destroys the
  denominator of CpAO.
- Nothing is deduplicated, normalised or relabelled. Observer terms are preserved verbatim; ontology
  mapping happens later and never by silent rewrite.
- Lineage keys are maintained so contamination between roles is checkable rather than remembered.
- Ingestion happens **as part of execution**, not as a tidy-up afterwards. An output that is scored
  and then cleaned up has already been lost.

## Validating before you commit to it

```bash
python3 resources/v1/validators/check_empirical_archive.py <archive_dir>
```

Exit **0** valid · **1** schema violation · **2** could not check. "I found no problem" and "I could
not look" never share an exit code.

Thirteen committed negative controls in
`fixtures/empirical-archive-negative-controls/CASES.yaml` each break exactly one rule above, and
`validators/run_archive_negative_controls.py` asserts that each fails **for its declared reason**. If
one of them starts passing, that rule has silently stopped being enforced.

## Open items for Eval

1. **Confirm the `lane` vocabulary.** Resources stores it verbatim; the values should match E2's
   roster lanes exactly.
2. **Confirm `absence_reason` covers the real cases.** The list is a starting set, not a claim to be
   exhaustive.
3. **Byte budget.** Not forecast: it needs per-endpoint duration and resolution from E2. The schema
   carries `output_bytes` per artifact, so the forecast becomes a sum once E2 lands.
