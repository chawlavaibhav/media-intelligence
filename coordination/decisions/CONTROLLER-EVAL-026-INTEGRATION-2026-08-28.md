# Controller EVAL-026 Integration — 2026-08-28

## Status

**ACCEPTED AND MERGED AS QUALIFICATION MACHINERY ONLY.**

Integration:
- PR #52
- merge commit `2af1dbdb14eacf7dee191fc81619e94c7860958a`

## Accepted result

- deterministic real-clip ingest and temporal perturbation machinery;
- 13 injected defect types;
- all 9 frozen `temporal_video` capabilities covered by the machinery;
- 7 with full injected-truth coverage once real clips exist;
- `action_adherence` and `camera_framing_fidelity` negative-direction-only in Stage Q;
- constructed stand-in material can never qualify an instrument;
- scoring code cannot emit `qualified`;
- no capability added or redefined;
- no Registry rows;
- external/API/model/evaluator calls 0;
- spend USD 0;
- human labels 0.

## Not yet authorised / not yet true

The temporal evaluator family is **not qualified**.

Actual qualification remains blocked on:
1. the 12 clean approved real base clips required by the frozen material contract;
2. a Controller-approved numeric pass mark frozen **before** the first real checker qualification run;
3. any separately required human adjudication for capabilities whose frozen map still requires it.

Do not invent the pass mark merely to make the machinery conclude.

## Pass-mark timing

No numeric pass mark is set by this integration.

The Controller will set it after the actual candidate checker and approved real-clip material are known, but before any candidate qualification observations are run or inspected. This preserves precommitment without forcing a meaningless threshold before the measurement setup is concrete.
