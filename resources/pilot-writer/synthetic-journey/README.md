# RES-007 synthetic journey — committed test evidence

Everything here is produced deterministically by
`resources/pilot-writer/tests/test_pilot_journey.py` (re-running it reproduces these bytes
exactly). **Nothing here is real:** fictional provider `dummy-vendor`, test currency XTS,
synthetic binary fixture bytes. No provider was called, no media was generated, no money
was spent (RES-007 budget: USD 0).

| File | What it is |
|---|---|
| `pilot-journey-synthetic.yaml` | One complete v3 archive: 1 job → 1 accepted video outcome, 3 provider steps (5 attempts incl. 1 refusal + 1 timeout), 2 local ffmpeg-shaped steps, 2 human-review steps, 5 binary artifacts with ordered multi-parent lineage. Passes `validate_topology_v3.py` (all 11 gates) and `recompute_cpao_v3.py` (fully-loaded 42.00 XTS, matching the hand-computed expectation embedded in the file). |
| `artifacts/*.bin` | The actual binary artifact bytes (deliberately not valid UTF-8). The archive's SHA-256 and byte counts are computed from, and verified against, these files. `cut.bin` really is `shot-a.bin`+`shot-b.bin`; `final.bin` really is `cut.bin`+`logo.bin` — the recorded lineage is the lineage that produced the bytes. |
| `recipes.md` | The `params_location` for the two transform recipes — full parameter strings whose SHA-256 the archive records. |
| `repair-journey.yaml` | A second, smaller valid journey exercising the repair path: a local `step_kind: repair` step with `repair_of_step_id`, producing a repaired artifact from the defective one with no manufactured attempt. Passes both frozen validators. |
| `negative-controls/nc-mutable-cost-ref.yaml` | Deliberately invalid: one ledger entry `immutable: false`. The frozen CpAO engine must REFUSE (exit 3). |
| `negative-controls/nc-only-failed-attempts.yaml` | A journey where the provider refused and nothing was accepted. Topology-valid (the failure is evidence), zero artifacts (no fake output), and CpAO is refused as UNDEFINED — never reported as zero. |
| `negative-controls/nc-tampered-local-step-attempt.yaml` | The valid archive edited after writing to fake an attempt on a local step. The frozen validator must reject it under G2. |
