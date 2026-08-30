# EVAL-037 — lane `sonnet-controlled-canon` — supplemental run

**Supplemental treatment. Replaces nothing.** The original `sonnet-full-canon` lane
(PR #71) and the repaired unbounded-retrieval run (PR #77, now on `main` at
`runs/sonnet-full-canon-repair-001/`) are untouched and remain the evidence of what
unrestricted autonomous Canon retrieval does to `claude-sonnet-5`.

Same model, same six briefs, same three repetitions, same corpus, same package schema.
One changed variable: retrieval is **objective-driven and controlled** instead of
free-form and unbounded.

## Headline

**18 of 18 trials complete. Zero context overflows. Zero failures of any class.**

| | unbounded (`repair-001`, on `main`) | **controlled (this run)** |
|---|---|---|
| `complete` | 2 / 18 | **18 / 18** |
| `context_overflow` | **16 / 18** | **0** |
| `failed_technical` / `failed_format` / `sdk_error` | 0 / 0 / 0 | 0 / 0 / 0 |
| `failed_controlled_retrieval` | n/a | **0** |
| Format repairs | 0 | 0 |
| Transient retries | 0 | 0 |
| Frozen lane gates | 32/32 PASS | **32/32 PASS** |
| Controlled-retrieval gates | n/a | **13/13 PASS** |

The unbounded lane's cost (**$3.228778**) covered only its 2 complete trials — the
16 overflow trials lost their spend evidence entirely. This run's **$2.861148** covers
**all 18**. Controlled retrieval produced nine times the completed trials for less
recorded spend.

## Retrieval actually performed

| Measure | Allowance | Observed |
|---|---|---|
| `canon_search` calls / trial | ≤ 3 | mean 2.94, median 3 (**53 total**) |
| Results returned per search | ≤ 8 | max **8** — every search passed `limit` |
| Search results exposed / trial | ≤ 24 | mean 23.56, median **24**, min 16, max 24 |
| `canon_read` objects / trial | ≤ 6 | mean 0.06, median **0**, max 1 (**1 total**) |
| `canon_catalog` calls | discouraged | **0** |
| Knowledge needs declared | ≤ 3 | ≤ 3 in every trial; declared in **13/18** |

**Every trial stayed inside the allowance. No violation occurred, so no trial was
recorded `failed_controlled_retrieval`.**

Items returned, by epistemic status: **ACCEPTED 198 · HOLD 227 · Q&A 112**. HOLD
outnumbering ACCEPTED is a property of what BM25 ranks highly on these briefs, not a
status-handling defect — every item carried its own `source_status`, and gate R22
confirms it.

### The behavioural finding

Sonnet **saturated its search allowance and almost entirely ignored its read
allowance**: 53 searches against 1 read, with a median of zero `canon_read` calls. It
treated the ranked search envelopes as sufficient and stopped — STEP 4 exercised, not
skipped.

That is a real result about how this model uses a bounded research budget, and it is
worth carrying into the production design: under this treatment the read allowance was
close to dead weight, while the search allowance was the binding constraint.

Packages cite retrieved items by id with their status and handle HOLD cautiously
unprompted — e.g. *"all HOLD status — treated only as creative-technique inspiration,
not as validated performance evidence"*. `KNOWLEDGE_AND_WEBSITE_USE` is faithful to
what was actually retrieved.

## Why the unbounded lane failed, measured

One unbounded `canon_search` over this corpus returns **3,999 items / 10.4 MB /
~2.6M tokens** — past the context window from a single call. The same query at
`limit=8` returns **23.5 KB**. The treatment does not make the corpus smaller; it makes
the model ask for a slice of it.

## Usage, cost, latency

| | |
|---|---|
| Input tokens | 641,539 |
| Cached input tokens | 0 |
| Output tokens | 157,807 |
| Reasoning tokens | **null** — not exposed separately by the provider; recorded as null, never invented |
| Provider turns | 38 (all 18 trials, tool turns included) |
| Cost | **$2.861148**, `cost_basis: computed`, frozen price snapshot |
| Latency / trial | mean 111.8 s, median 110.3 s |
| Website calls | 6 (B01 ×3, B02 ×3; B03–B06 zero, as required) |

## Treatment, not guard — verified, not asserted

The harness capped, clamped and blocked nothing. `canon_search` still returns every
scoring item when `limit` is omitted. Gate **C10** checks this empirically: for every
`canon_search`, the tool's own `limit_applied` equals the `limit` the model asked for.
Compliance was measured after the fact by `tools/controlled_retrieval.py`, and gate
**C2** recomputes every recorded count from the raw tool transcript, so the numbers
above cannot have been hand-written.

Had a trial exceeded the allowance it would have been recorded
`failed_controlled_retrieval`, its package retained, `eligible_for_media_generation:
false`, and **not re-run**. No trial did. No trial was re-run for any reason.

## Execution provenance — one restart, disclosed

An earlier execution attempt was **destroyed by session teardown** after 2 trials, when
the working directory it ran in was deleted. The runner seals `result.json` and
`attempt-ledger.json` only after all 18 trials, so **no evidence was ever written** for
that attempt — there was nothing to preserve, supersede or select from.

This is **not a quality-rerun**. Nothing was discarded because of how it looked. The
lane was then executed once, completely, from the **identical frozen commit
`e1336ee`**, in a durable directory. `freeze_fingerprint` and `common_substrate_digest`
were re-verified intact at dispatch, and no runner, prompt or config byte changed
between the freeze and the first call of the run that produced this evidence.

Another EVAL-037 lane was running concurrently on the same host under a different
session; its directory was not read. No `rate_limit_429` occurred in this lane.

## Provenance

- Base `origin/main` `b66efd1` (which already carries PR #77's EVIDENCE-001 digest fix).
- Substrate frozen and committed at **`e1336ee`**, before the first experimental call.
- `freeze_fingerprint` `5a81f59a35cc06d612c3c20d0a6f79bf00fc755c486a864726ec449b343a2d27`
- `common_substrate_digest` `012b9e6799cd89acc6badf7cbdde1e6bdb50e4d14bc2279728fbbeefb0764036`
- Canon fingerprints `cbd321aa…` / `1313c0ba…` — **unchanged. Canon was not altered.**
- `claude-sonnet-5` resolved at preflight and used throughout; never substituted.
- Trial order recomputed from `sha256("EVAL-037|" + trial_id)` and matched.
- Written to `runs/sonnet-controlled-canon/` under `E037SCC-sonnet-*` trial ids; no
  other lane's evidence was written to or read.

## Freeze status — lane-scoped; F1c was already red on `main`

`validate_freeze.py` gate **F1c** fails on this branch: the eight original lane YAMLs
still embed an older common digest. They are **deliberately untouched** — re-stamping
them would modify the original EVAL-037 freeze.

**F1c and `test_substrate.py` were already red on `main` before this branch existed**,
inherited from the PR #77 merge, which re-stamped only `lanes/sonnet-full-canon.yaml`.
Verified against a clean checkout of `main`. A programme-wide re-stamp is a controller
decision.

## Reproduce

```bash
python3 tools/freeze_fingerprint.py --check
python3 tools/preflight.py --lane lanes/sonnet-controlled-canon.yaml
python3 validators/validate_lane_run.py \
    --lane lanes/sonnet-controlled-canon.yaml --run runs/sonnet-controlled-canon
python3 validators/validate_controlled_retrieval.py \
    --lane lanes/sonnet-controlled-canon.yaml --run runs/sonnet-controlled-canon
```
