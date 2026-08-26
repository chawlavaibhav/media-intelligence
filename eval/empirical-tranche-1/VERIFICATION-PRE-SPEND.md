# EMP-001 pre-spend verification record

**Date:** 27 Aug 2026
**Branch:** `work/eval-013-emp-001-live-path-correction`
**Supersedes:** the EVAL-012 record on `work/eval-012-emp-001-zero-spend`
**External calls made producing this record: 0. Spend: USD 0 / INR 0.**

Every block below is **copied from a fresh run in this branch**, not written from expectation.
Environment: macOS (Darwin 23.6.0), Python 3.14.6, pytest 9.1.1, PyYAML 6.0.3 in a throwaway
virtualenv outside the repository. `hb-view` is a local rendering tool; nothing here reaches a
network.

## What changed since the EVAL-012 record

The Controller blocked EVAL-012 on five defects (B1–B5). The suite then proved refusal
exhaustively and never proved dispatch, which is how a missing live orchestration and a
mislabelled measurement path both survived a green run. This record therefore leads with the
**positive** controls.

---

## Step 1 — all EMP-001 tests

```
$ python3 -m pytest -q eval/empirical-tranche-1/tests
...............................                                          [100%]
247 passed in 2.15s
EXIT=0
```

## Step 2 — inherited V1 harness verification

```
$ python3 eval/v1/harness/run_selftest.py
RESULT: 107/107 checks passed
Registry rows created: 0  (must be 0)
Paid API calls made:   0
==========================================================================
EXIT=0
```

```
$ bash eval/v1/harness/run_cross_branch_validation.sh
[PASS] fan-out 7.00 measurements per artifact — one generation, many measurements

RESULT: PASS — Eval's emission satisfies the current Resources contract (exit 0)
EXIT=0
```

## Step 3 — dry runs, network disabled

```
$ python3 eval/empirical-tranche-1/preflight.py --dry-run
verdict: PREFLIGHT_GREEN
  [PASS] adapter_path_blocked
  [PASS] authorisation_blocked
  [PASS] geometry_fixtures
  [PASS] harness_selftest
  [PASS] one_call_one_trial
  [PASS] protected_baselines
  [PASS] registry_empirical_rows
  [PASS] synthetic_cannot_reach_registry
external calls: 0   spend USD: 0
written: /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-worktrees/eval-013/eval/empirical-tranche-1/preflight-result.json
EXIT=0
```

```
$ python3 eval/empirical-tranche-1/text_qualification/qualify_text.py --dry-run
dry run: 2 synthetic candidates
  fake-openai-candidate      devanagari= 576 latin= 576 scope=['devanagari', 'latin']
  fake-google-candidate      devanagari= 576 latin=   0 scope=none
external calls: 0   spend USD: 0
written: /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-worktrees/eval-013/eval/empirical-tranche-1/text_qualification/qualification-dryrun.json
EXIT=0
```

```
$ python3 eval/empirical-tranche-1/atex/run_atex.py --dry-run
generations: 16  per route: {'IMG-01': 8, 'IMG-02': 8}  retries: 0
registry rows written: 0  boundary refused synthetic evidence: True
external calls: 0   spend USD: 0
written: /Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-worktrees/eval-013/eval/empirical-tranche-1/atex/atex-dryrun.json
EXIT=0
```

## Step 4 — POSITIVE fake-live paths

The correction the Controller asked for. Same orchestration, same request builders, same
provider-specific auth headers, same parsers, same scorer — with an injected recorder standing
exactly where the socket would be. Both walk the real authorisation gate.

```
$ python3 .../qualify_text.py --fake-live --authorisation <valid> --out <path>
fake-live: 2304 recorded dispatches, 0 network calls
  openai:FAKE-LIVE-openai-snapshot   devanagari= 576 latin= 576 scope=['devanagari', 'latin']
  google:FAKE-LIVE-google-snapshot   devanagari= 576 latin= 576 scope=['devanagari', 'latin']
external calls: 0   spend USD: 0
written: /tmp/q-fl.json
EXIT=0
```

2,304 dispatches is the frozen maximum: 2 candidates x 2 scripts x 96 items x 2 shapes x 3 passes.
Both fake candidates are perfect readers, so both survive to Latin. That is a property of the
fake, not a finding about any model.

```
$ python3 .../run_atex.py --fake-live --authorisation <valid> --out <path>
fake-live: 16 generations ({'IMG-01': 8, 'IMG-02': 8}), 16 evaluator dispatches, 0 network calls
exact matches: 16/16  (perfect reader — not evidence about any model)
synthetic: False   registry rows: 0
external calls: 0   spend USD: 0
written: /tmp/a-fl.json
EXIT=0
```

`synthetic: False` on a run that cost nothing is the point: the label now tracks the EXECUTION
MODE rather than being a constant. 16 exact matches out of 16 is what a perfect reader scores and
says nothing whatever about IMG-01 or IMG-02.

### The refusal paths still refuse

```
$ python3 eval/empirical-tranche-1/preflight.py          # no --dry-run, no authorisation
REFUSED: EMP-001 paid execution is not authorised, so there is no non-dry-run preflight to perform. Reasons:
  - no authorisation file exists at that path
Re-run with --dry-run.
EXIT=2
```

```
$ python3 eval/empirical-tranche-1/atex/run_atex.py --live
REFUSED: EMP-001 paid A-TEXT generation requires an explicit authorisation and a qualified judge produced by a real qualification run.
  - no authorisation file exists at that path
EXIT=2
```

## Step 5 — protected baselines, byte for byte

```
$ shasum -a 256 -c <(grep -v '^#' eval/empirical-tranche-1/protected-baselines.sha256)
eval/v1/capability-contract.yaml: OK
eval/v1/bank/master-bank-v1.jsonl: OK
eval/v1/instruments/fixtures/cv-geometry/manifest.json: OK
eval/battery/devanagari-exactness/human-validation/human-validation-v1.json: OK
eval/battery/devanagari-exactness/CHECKER-CONTRACT.md: OK
eval/battery/devanagari-exactness/build_items.py: OK
eval/battery/devanagari-exactness/devtext.py: OK
eval/battery/devanagari-exactness/checker_input.py: OK
eval/battery/devanagari-exactness/perturb.py: OK
eval/registry/registry-v1.jsonl: OK
eval/v1/harness/harness.py: OK
eval/v1/harness/models.py: OK
eval/v1/harness/adapters.py: OK
EXIT=0
```

### Capability Registry

```
$ grep -v '^#' eval/registry/registry-v1.jsonl | grep -c '[^[:space:]]'
0
```

Zero empirical rows, before and after every run above, including both fake-live runs.

### Nothing outside the tranche package was touched

```
$ git diff --name-only origin/main...HEAD | grep -v '^eval/empirical-tranche-1/'
.gitignore
eval/tasks/EVAL-013-EMP-001-LIVE-PATH-CORRECTION.md
```

`.gitignore` carries the EVAL-012 entries; the EVAL-013 task file is the Controller's own commit.

---

## Rebuilding the derived material first

Both image sets are gitignored build products, so a fresh checkout must materialise them before
the suite can run. This is not optional and it costs nothing:

```bash
python3 eval/empirical-tranche-1/text_qualification/render_latin_pack.py
cd eval/battery/devanagari-exactness
python3 build_items.py --total 120 \
  --out-dir ../../empirical-tranche-1/text_qualification/build/devanagari
python3 apply_human_validation.py \
  --from-build ../../empirical-tranche-1/text_qualification/build/devanagari \
  --out-dir    ../../empirical-tranche-1/text_qualification/build/devanagari/validated
```

The rebuilt `items.jsonl` hashes to `9c69cac2…`, the `battery_identity` pinned in the frozen human
validation record, which is how the materialised view is proved to be the one the reviewer
actually validated. The battery itself is read and never written to.

## Defects this correction found in its own predecessor

Beyond the five the Controller identified, writing the positive controls surfaced three more:

1. **The blind check never ran on the live path.** The checker contract requires it before any
   call; it was enforced only in tests. A leak would have reached the wire. It is now a
   pre-dispatch refusal.

2. **The blindness scan was blind.** The transport serialised with `ensure_ascii=True`, so a
   Devanagari target would have travelled as `\uXXXX` and every check scanning for Devanagari
   characters would have passed while seeing nothing. The wire now carries UTF-8 and the scan
   parses first.

3. **The verdict blind rule cried wolf.** It demanded the target appear exactly once across the
   whole serialised body — not an invariant, since short targets occur incidentally in prompt
   prose, in enum values like `input_text` and inside base64. It fired on the preflight's own
   probe. Replaced with the rule the Devanagari checker contract already settled on.

## Deviations from the implementation plan, and why

Carried forward from the EVAL-012 record and still true: the hyphenated package directory is
authoritative so modules are imported via `tests/conftest.py`; `shasum -a 256` replaces
`sha256sum` on macOS; `pytest` and `PyYAML` live in a throwaway virtualenv outside the repository.

**The human perceptibility review remains NOT performed and NOT fabricated.**
`text_qualification/perceptibility-review.csv` is still emitted with all 96 verdict columns blank.
Latin paid qualification remains gated on that zero-spend human review.

Task 9 (paid execution) was not executed. No provider, model or evaluator was contacted.
