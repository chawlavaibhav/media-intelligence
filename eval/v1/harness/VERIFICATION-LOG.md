# E5 harness verification log

**Executed:** 26 Aug 2026 in the cloud session · **Runner:** Python 3.11.15
**Status:** `implementation_written_AND_executed_in_cloud`
**Covers corrections:** E-C4 (repeat vs retry), E-C5 (mixed-cell refusal), E-C6 (no synthetic bypass), E-C7 (canonical handoff)

All fixtures are dummy/synthetic. No network call, no model call, no paid API call,
no empirical Registry row. Reproduce with:

```
python3 eval/v1/harness/run_selftest.py
```

```text
==========================================================================
E5 HARNESS VERIFICATION — dummy/synthetic fixtures only, zero spend
==========================================================================

DEMO 1 — one generated asset scored by several evaluators, no regeneration
  [PASS] one generation call only
         attempts=1, assets=1
  [PASS] >=3 distinct evaluators scored the SAME asset
         12 measurements from 4 instruments (dummy-ocr, dummy-temporal, dummy-vlm, file-probe) on 1 asset
  [PASS] all measurements point at that one asset
  [PASS] still exactly one trial asset
         measurements_per_trial_asset = 12.0x
  [PASS] multiple defects recorded on one output
         co-occurrence: ['face_drift + text_mutates_mid_clip']

DEMO 2 — an experimental REPEAT creates a new attempt, never a replacement
  [PASS] new attempt id
         att-d38f3df1b600 -> att-81b678298242
  [PASS] new asset id (original NOT overwritten)
  [PASS] original asset still on disk with its original hash
  [PASS] repeat linkage recorded as a REPEAT
  [PASS] a repeat is NOT a retry
  [PASS] each asset has exactly one provenance record

DEMO 2b — E-C4: repeat and retry are structurally separate
  [PASS] a repeat is counted as a repeat, NOT a retry
         experimental_repeats=1
  [PASS] a retry is counted as a retry, NOT a repeat
         production_retries=1
  [PASS] the two counters are reported separately and never summed
  [PASS] the CpAO retry chain contains the retry and EXCLUDES the repeat
         chain=['att-d38f3df1b600', 'att-7807f9f3ef8c']
  [PASS] retry-chain cost and repeat cost are separate lines
         retry_chain=1.0 repeats=1.0
  [PASS] an attempt that is BOTH repeat and retry is REFUSED
         raised: An attempt cannot be BOTH an experimental repeat and a production retry. A repeat is decided before the run to measure r
  [PASS] a retry with no reason is REFUSED
         raised: A production retry requires retry_reason. An unexplained retry is indistinguishable from an experimental repeat.
  [PASS] a repeat with repeat_index 0 is REFUSED
         raised: An experimental repeat requires a repeat_index >= 1. repeat_index 0 is the first attempt of a repeat set, not a repeat o

DEMO 3 — frames sampled from a clip keep the parent trial id
  [PASS] 4 child assets created
  [PASS] every frame names its parent
  [PASS] every frame resolves to the parent TRIAL
  [PASS] 4 frames added 0 new trials
         assets=6 but trial_assets=2 (2 generations, 4 derived frames). Frames from one clip are ONE trial.
  [PASS] frame extraction cost nothing

DEMO 4 — the duplicate-regeneration guard fires
  [PASS] regenerating the same item+config is REFUSED
         raised: DUPLICATE GENERATION REFUSED for item compound-024 config 5e49a5af55f2: asset ast-16e10d7c249c already exists. Evaluatin
  [PASS] guard did not create a stray attempt
         attempts still 2
  [PASS] but re-measuring the SAME asset is allowed and free
         evaluating another capability needs no new generation - the point of fan-out

DEMO 5 — an unqualified instrument cannot write a Registry row
  [PASS] unqualified instrument REFUSED at the Registry boundary
         raised: REGISTRY WRITE REFUSED: instrument dummy-vlm has qualification status 'screened_not_qualified'. Only ('qualified', 'dete
  [PASS] dummy-vlm is correctly marked not-writable
         status=screened_not_qualified
  [PASS] file-probe IS writable (deterministic needs no calibration)
  [PASS] even a QUALIFIED instrument is refused on synthetic data
         raised: REGISTRY WRITE REFUSED: synthetic/dummy measurements may never become empirical Registry rows. There is no override.
  [PASS] empty measurement set is REFUSED
         raised: REGISTRY WRITE REFUSED: no measurements. An empty check is not a passing check.
  [PASS] registry still empty

DEMO 5d — E-C6: there is NO synthetic promotion bypass
  [PASS] write_registry_row exposes NO override parameter
         parameters: ['capability', 'instrument_id', 'measurements', 'conditions', 'difficulty_level', 'repeats_per_item']
  [PASS] no allow_synthetic anywhere in the harness source
  [PASS] no call shape promotes synthetic measurements
         2/2 call shapes refused
  [PASS] registry STILL empty after bypass attempts

DEMO 5e — E-C5: a Registry row must be ONE coherent cell
  [PASS] mixing TWO MODELS in one cell is REFUSED
         raised: REGISTRY WRITE REFUSED: mixed cell. Trials disagree on 'model': ['model-A', 'model-B']. Two providers, models, versions,
  [PASS] mixing TWO CAPABILITIES in one cell is REFUSED
         raised: REGISTRY WRITE REFUSED: mixed cell. Measurements disagree on 'capability': ['action_adherence', 'text_logo_stability_in_
  [PASS] mixing TWO INSTRUMENTS in one cell is REFUSED
         raised: REGISTRY WRITE REFUSED: mixed cell. Measurements disagree on 'capability': ['action_adherence', 'text_logo_stability_in_
  [PASS] a capability that is not the requested one is REFUSED
         raised: REGISTRY WRITE REFUSED: requested capability 'text_logo_stability_in_clip' but measurements are for 'action_adherence'.
  [PASS] an instrument that is not the requested one is REFUSED
         raised: REGISTRY WRITE REFUSED: requested instrument 'dummy-ocr' but measurements came from 'dummy-temporal'.
  [PASS] a declared condition contradicting the trials is REFUSED
         raised: REGISTRY WRITE REFUSED: declared condition model='model-Z' contradicts the trials, which carry 'model-A'.
  [PASS] an over-declared repeats_per_item is not trusted
         raised: REGISTRY WRITE REFUSED: repeats_per_item must be >= 1.
  [PASS] pooling a production RETRY into a pass-rate cell is REFUSED
         raised: REGISTRY WRITE REFUSED: 1 trial(s) in this cell are production RETRIES. A retry exists because something failed; pooling
  [PASS] no Registry row was created by any mixed-cell attempt

DEMO 5b — absence reasons and harness negative controls
  [PASS] 'absent' carries a machine-readable reason
         reason=not_applicable
  [PASS] 'absent' with NO reason is REFUSED
         raised: absent verdict needs a reason from ('not_applicable', 'not_measured', 'instrument_unqualified', 'generation_failed', 're
  [PASS] verdict outside the vocabulary is REFUSED
         raised: instrument returned unknown verdict probably_fine
  [PASS] found a capability owned by the instrument but outside the fan-out
         using 'anatomy_hands'
  [PASS] scoring a capability outside the item's fan-out is REFUSED
         raised: capability anatomy_hands is not in item compound-006's measurement fan-out. The bank decides what an asset may validly e
  [PASS] using an instrument outside its judgement family is REFUSED
         raised: instrument dummy-ocr is not specified for capability object_count. Qualification NEVER generalises across judgement fami

DEMO 5c — a refused generation yields 'absent/refused', not a fail
  [PASS] refusal recorded as a refusal, not a failed capability
         refusals=1, error_classes={'moderation_block': 1}

DEMO 6 — the Registry schema validates and starts EMPTY
  [PASS] registry file exists
  [PASS] registry contains ZERO empirical rows
         0 data rows
  [PASS] registry schema file exists
  [PASS] schema parses and declares zero entries
         status=PROPOSED_NOT_IN_FORCE

DEMO 7 — E-C7: canonical Resources storage handoff
  [PASS] canonical record file emitted: attempts.jsonl
  [PASS] canonical record file emitted: artifacts.jsonl
  [PASS] canonical record file emitted: measurements.jsonl
  [PASS] canonical record file emitted: acceptances.jsonl
  [PASS] no competing Eval-specific persistent manifest is emitted
         the old single manifest is gone; Resources owns the persistent model
  [PASS] every failed/refused call survives as an ATTEMPT record
         2 non-ok attempts, all with no artifact; statuses=['error', 'refused']
  [PASS] attempts without an artifact are NOT dropped from the handoff
         attempts_without_artifact=2
  [PASS] attempt records carry every contract field
         5 rows, 20 required, missing=none
  [PASS] artifact records carry every contract field
         7 rows, 8 required, missing=none
  [PASS] measurement records carry every contract field
         14 rows, 10 required, missing=none
  [PASS] observation units are the CANONICAL vocabulary only
         used: ['frame']
  [PASS] derived artifacts point to a parent and add no trial
         7 artifacts, 4 derived, 3 trials
  [PASS] acceptance is EMPTY - Eval does not decide it
  [PASS] no routing score or weight was computed
  [PASS] generation and evaluator costs are separate lines
         gen=3.0 eval=0.121

==========================================================================
RESULT: 72/72 checks passed
Registry rows created: 0  (must be 0)
Paid API calls made:   0
==========================================================================
```
