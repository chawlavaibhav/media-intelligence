# E5 harness verification log

**Executed:** 26 Aug 2026 in the cloud session · **Runner:** Python 3.11.15
**Status:** `implementation_written_AND_executed_in_cloud`

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

DEMO 2 — a retry creates a NEW attempt and never replaces the output
  [PASS] new attempt id
         att-d38f3df1b600 -> att-81b678298242
  [PASS] new asset id (original NOT overwritten)
  [PASS] original asset still on disk with its original hash
  [PASS] retry linkage recorded
  [PASS] each asset has exactly one provenance record

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
         raised: REGISTRY WRITE REFUSED: synthetic/dummy measurements may never become empirical Registry rows.
  [PASS] empty measurement set is REFUSED
         raised: REGISTRY WRITE REFUSED: no measurements. An empty check is not a passing check.
  [PASS] registry still empty

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

STORAGE HANDOFF
  [PASS] artifact manifest carries every required field
         7 asset rows, 20 required fields, missing=none
  [PASS] no routing score or weight was computed
  [PASS] generation and evaluator costs are separate lines
         gen=3.0 eval=0.121

==========================================================================
RESULT: 38/38 checks passed
Registry rows created: 0  (must be 0)
Paid API calls made:   0
==========================================================================
```
