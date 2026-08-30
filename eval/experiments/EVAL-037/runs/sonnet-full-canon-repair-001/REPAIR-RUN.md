# EVAL-037 — lane `sonnet-full-canon` — **REPAIR RUN 001**

**This is a repair run, not the original execution.** The original failed execution is
preserved unchanged in PR #71 (branch `work/eval-037-sonnet-full-canon`, run directory
`runs/sonnet-full-canon/`). Nothing in this directory replaces it.

Same lane, same frozen 18 coordinates, same order. Re-run after one non-semantic
harness fix. No creative judging. No media generation. No acceptance scoring.

## What changed between the two runs — exactly one line

`tools/providers.py`, in `_run_tool`:

```diff
- blob = json.dumps(out, sort_keys=True, default=str)
+ blob = json.dumps(out, default=str)
```

`blob` feeds only `result_digest` and `result_bytes` in the tool-call evidence record.
It is **not** what the model receives: the adapter serialises the tool result separately
with `json.dumps(out, default=str)`, and those bytes are byte-identical before and
after this change.

- `result_bytes` is unchanged — sorting reorders keys, it does not resize the payload.
- `result_digest` is now exactly `sha256` of the bytes the model actually received
  (verified: `digest == sha256(model-facing bytes)`).
- The Canon corpus was **not** edited, so both corpus fingerprints are unchanged:
  `cbd321aa…` (193 files) and `1313c0ba…` (23 files).

### Explicitly unchanged

System prompt · FULL_CANON addendum · briefs · `canon_tools.py` and all Canon retrieval
semantics · model id and settings (`claude-sonnet-5`, adaptive thinking, `effort=high`,
provider-default sampling) · trial order · retry policy · tool-loop guard · website
snapshots.

## Result

| | original (PR #71) | **repair-001** |
|---|---|---|
| `complete` | 1 | **2** |
| `sdk_error` | **12** | **0** |
| `context_overflow` | 5 | **16** |
| Validator | 32/32 PASS | 32/32 PASS |
| Runner frozen at | `a2e9a70` | `a685534` |
| Reported cost | $0.412806 | $3.228778 |

Complete trials: `E037-sonnet-full-canon-B01-R3`, `E037-sonnet-full-canon-B02-R2`.

### The fix worked, and it changed the diagnosis

`sdk_error` is **gone — 0 of 18**. Every trial that previously died inside the evidence
digest now runs to a genuine provider outcome.

What it exposed is that the harness crash had been **masking** the real behaviour. In
the original run, 12 trials died early, before retrieving much. With the crash removed,
those trials keep retrieving — and overflow instead. The observed prompt sizes are
correspondingly larger:

- original run, 5 overflows: 1.11M – 3.43M tokens
- repair run, 16 overflows: 1.11M – **7.96M** tokens (median 3.31M), against a 1M limit

Full distribution (tokens): 1.11M, 2.20M, 2.20M, 2.40M, 3.05M, 3.14M, 3.16M, 3.28M,
3.34M, 3.49M, 3.82M, 4.19M, 4.34M, 4.58M, 6.45M, 7.96M.

## Context overflow — left as a legitimate outcome, by instruction

All 16 failures are `context_overflow`: real provider 400s, `prompt is too long`.

Per EXECUTION-CONTRACT §7 these are **model+condition execution failures and real
results of this experiment**, not faults. They were given zero retries, no substitution,
and were **not** repaired. They are the finding, not an obstacle to it.

Mechanism, which is the frozen design (§5: no aggregate top-K, no token budget, no
retrieval-count budget, no mandatory use): `canon_search` returns every scoring item
unless the model itself asks for a `limit`. Measured against this corpus, one unbounded
`canon_search` returns a **3.9 MB** JSON payload — on the order of 1M tokens from a
single call. Two or three such calls exceed the context window on their own.

The substantive result of this lane is therefore: **`claude-sonnet-5` under FULL_CANON,
given unbounded retrieval over this corpus, exhausts its own context in 16 of 18
trials.** That is a property of the model+condition pairing, and it survives the repair.

## Evidence limitation — still present, deliberately not fixed

`providers.py` still raises on the API-exception path with no `detail`, so the 16
overflow trials record `turns=0 canon=0 web=0` even though they can only have reached
2–8M tokens by making many Canon calls. **What they retrieved is still not retained.**

Consequences, unchanged from the original run:

- `lane_usage_totals` (1,505,004 in / 21,877 out) and `lane_calculated_cost_usd`
  **$3.228778** cover only the 2 complete trials. Real lane spend is materially higher;
  the billed turns preceding each overflow were not recorded.
- Gate **R19** inspects only trials that *report* Canon turns — here, 2 — so 32/32 still
  passes vacuously on the 16 failures.

This was left alone on purpose. The instruction was a single non-semantic digest fix;
repairing evidence retention is a larger change to the failure path and is a separate
controller decision.

## Freeze status — lane-scoped, and one gate is red

The fix is inside `tools/`, which is inside the common substrate scope, so the freeze
necessarily moved:

| | before | after |
|---|---|---|
| `common_substrate_digest` | `d8b2c045…` | `aa1d2f99259ead8279d9909319ba731aeac2ae8115b432aacd72632a9d19d25a` |
| `freeze_fingerprint` | `5fc021d9…` | `0dcd4edbc786c0e6f9dc3c06f2209cb8e73c8fc084ebb2c2b4ad1d35f5ca8d24` |

`lanes/sonnet-full-canon.yaml` was re-stamped with the new common digest — that one
line only.

**`validate_freeze.py` gate F1c now FAILS: "every lane embeds the common substrate
digest."** The other seven lane YAMLs still carry the old `d8b2c045…`. Re-stamping them
would require opening sibling lane configs, which the isolation contract forbids this
worker from doing. F1a and F1b pass; F1c is the only failure.

**This repair freeze is therefore LANE-SCOPED.** It is valid for `sonnet-full-canon`.
A controller-level programme-wide re-stamp is required before any other lane runs on
this fix — and every FULL_CANON lane needs it, since the original defect is corpus-wide.

## Provenance

- Base `origin/main` `28aefc7`; repair freeze committed at `a685534` **before** the
  first experimental call of this run; no runner, prompt or config change after it.
- Preflight at dispatch: computed common digest `aa1d2f99…` matched the lane; freeze
  fingerprint `0dcd4edb…` matched; `canon_base_commit c6f8d910` an ancestor of HEAD;
  Canon fingerprints `cbd321aa…` / `1313c0ba…` unchanged; trial order recomputed from
  `sha256("EVAL-037|"+trial_id)` and matched.
- `claude-sonnet-5` resolved at preflight and was used throughout; never substituted.
- Only `EXECUTION-CONTRACT.md`, `lanes/sonnet-full-canon.yaml` and the files that lane
  names were read. No sibling lane config, branch, PR, log, output or report was opened.
- Written to a distinct directory via the runner's `--out` flag, so the original run
  directory is untouched.
- Other EVAL-037 lanes were running concurrently on the same host under other sessions;
  their directories were not read. No `rate_limit_429` occurred in this lane.
