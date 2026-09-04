# EVAL-037 — lane `sonnet-full-canon` — worker notes

These are **worker notes, not experimental data**. The experimental record is
`result.json`, `attempt-ledger.json`, and the `requests/`, `raw/`, `transcripts/`,
`packages/` directories. Nothing here was used to alter a trial.

No creative judging was performed. No media was generated. The runner, prompts and
config were not changed after the first experimental call.

## Outcome

| | |
|---|---|
| Trials executed | 18 / 18, in the recomputed SHA-256 order |
| `complete` | **1** (`E037-sonnet-full-canon-B01-R2`) |
| `failed_execution` | **17** |
| Eligible for media generation | 1 |
| Validator | `validate_lane_run.py` — 32/32 gates PASS |
| Runner frozen at | `a2e9a701f5749c17369683a0f4c25d1b1f503a0a` (before first call) |
| Base | `origin/main` `28aefc78ef55c7bb52d67a47d8042e5699ae5f89` |

The lane ran exactly as frozen. It did **not** produce a usable comparison sample,
for the two independent reasons below.

## Failure 1 — substrate defect: `sdk_error` (12 / 18 trials)

Recorded error, identical in all 12:

```
'<' not supported between instances of 'bool' and 'str'
```

This is **not** a provider rejection and **not** a model behaviour. It is a crash in
the frozen harness. Isolated traceback:

```
tools/providers.py:403  in _run_tool
    blob = json.dumps(out, sort_keys=True, default=str)
TypeError: '<' not supported between instances of 'bool' and 'str'
  when serializing list item 0
  when serializing dict item 'dependencies'
  when serializing dict item 'internal_structure'
  when serializing dict item 'item'
  when serializing list item 599
  when serializing dict item 'results'
```

Root cause — a data × code interaction inside the approved freeze:

- `canon/candidates/canon-014/light-science-magic-beyond-ch3/source-concept-systems.yaml:322`
  (item `scs_lsmx_005`, kind `concept_system`, status **HOLD**) contains:

  ```yaml
  dependencies:
  - {from: sk_lsmx_0053, on: sk_lsmx_0052, note: "...", origin: source_stated}
  ```

  The unquoted `on:` key is parsed by PyYAML under YAML 1.1 as the **boolean** `True`,
  so that mapping has mixed key types: `'from'` (str), `True` (bool), `'note'`,
  `'origin'`.

- `_run_tool` computes the tool-result digest with `json.dumps(..., sort_keys=True)`.
  Sorting mixed `bool` / `str` keys raises `TypeError`.

Consequences:

- Deterministic, not transient. Correctly given 0 retries under the retry policy.
- Triggered by **any** `canon_search` broad enough to return `scs_lsmx_005`. The
  model's query decides whether a trial dies; nothing the model did was wrong.
- The tool result actually **sent** to the model is serialised at
  `providers.py` with `json.dumps(out, default=str)` (no `sort_keys`) and works.
  Only the **evidence digest** crashes. The experiment is killed by its own
  evidence-recording line.
- This is corpus-wide and condition-wide: it is expected to affect **every
  FULL_CANON lane**, not just this one. NO_CANON lanes cannot hit it.

## Failure 2 — genuine result: `context_overflow` (5 / 18 trials)

Real provider 400s, e.g.:

```
prompt is too long: 2064948 tokens > 1000000 maximum
```

Observed prompt sizes: 1.11M, 1.27M, 2.06M, 2.20M, 3.43M tokens.

Per EXECUTION-CONTRACT §7 this is a **model+condition execution failure and a real
result of this experiment**, not a fault and not a transient failure. Correctly
recorded as `failed_execution` with zero retries and no substitution.

Mechanism: `canon_search` returns every scoring item unless the model asks for a
`limit`, by design (§5: no aggregate top-K, no token budget). Measured directly
against this corpus, a single unbounded query returns on the order of 374–680 full
items; two or three such calls exceed the 1M context.

## Evidence limitation the validator does not catch

`tools/providers.py` raises on the API-exception path as:

```python
raise ProviderError(str(e)[:600], classify_exception(e)) from e
```

with **no `detail`**. The runner therefore records `provider_turns: []` and
`tool_calls: []` for every failed attempt. So:

- All 17 failures are logged as `turns=0 canon=0 web=0`. For the 5 overflow trials
  this is demonstrably untrue — they can only have reached 2M+ tokens by making many
  Canon calls. **What they retrieved was not retained.**
- `lane_usage_totals` (144,948 in / 12,291 out, 4 turns) and
  `lane_calculated_cost_usd` **0.412806** cover only the single complete trial.
  Real spend for the lane is higher; the billed turns that preceded each failure were
  not recorded.
- This is in tension with §8 ("Retain **every** output, including failed and
  malformed attempts"; every provider invocation retains its exact request).
- The validator still returns 32/32 because gate R19 only inspects trials that
  *report* Canon turns — here, one. The suite passes vacuously on the failures.

Reporting this, not fixing it: obligation 9 forbids changing the runner after the
first call, and any change would alter the frozen substrate digest.

## Environment

- Run from a clean worktree of `origin/main` @ `28aefc7`, not from the existing
  `eval-037` worktree, which carried **uncommitted** edits to `runner.py`,
  `providers.py` and `fake_provider.py` that are not part of the approved freeze and
  would have changed `common_substrate_digest`.
- The machine had neither `anthropic` nor `pyyaml`. Both were installed into a
  throwaway venv **outside** the repository; no repository file was touched.
- Gate values verified before dispatch: `freeze_fingerprint`
  `5fc021d96d23299e977600735cc8cf0f950f61d6ed7cd8b39099f9a10aa189ee`;
  `common_substrate_digest`
  `d8b2c045c61e22668bf6bb8b6b387250efce8c80b1e909029e21d3d6a6c0ebc2`;
  canon `cbd321aa…` / `1313c0ba…`; `canon_base_commit c6f8d910` an ancestor of HEAD.
- `claude-sonnet-5` resolved at preflight; the exact id was used throughout and never
  substituted.
- Six other EVAL-037 lanes were running concurrently on the same host under other
  sessions. Their directories were not read. Shared rate limits are a possible
  confound for latency, though no `rate_limit_429` was recorded in this lane.

## Diagnostic disclosure

Root cause was isolated **after** the frozen run completed, using two scripts kept
outside the repository:

1. an offline call of the Canon tools (no provider call) that reproduced the
   `sort_keys=True` crash and located `scs_lsmx_005`;
2. one replay of trial `E037-sonnet-full-canon-B05-R2`'s saved request to capture the
   traceback.

Neither wrote into `runs/`. Neither is a trial, and neither is counted in the
experimental record. No trial was re-run, and no failed trial was resampled.

## For the controller

The lane is reported as executed and failed, not as a result to compare. A
FULL_CANON-vs-NO_CANON comparison cannot be drawn from 1 of 18 trials. Failure 1 is a
substrate bug that needs a controller decision (it is a one-line fix in either the
corpus or `_run_tool`, but both are inside the freeze, so fixing either invalidates
the current `freeze_fingerprint` and requires a re-freeze and re-dispatch). Failure 2
is a real finding about FULL_CANON on this corpus and should survive any re-freeze.
