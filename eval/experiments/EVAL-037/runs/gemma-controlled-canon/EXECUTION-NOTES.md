# EVAL-037 — lane `gemma-controlled-canon` (SUPPLEMENTAL) execution notes

Factual worker record. No creative judging, no media generation, no merge.

A **new** treatment. It does not replace, alter, rerun or merge `gemma-full-canon`
(Canon optional; used 0/18) or `gemma-required-canon` / PR #78 (Canon mandatory but
unbounded; 18/18 `failed_technical`). Neither run directory exists on this branch.

## Dispatch

| Gate | Result |
|---|---|
| `freeze_fingerprint` | intact — `899eb3f5e3ba7bab8ef43006bb632a8bea59543b7b020607cbb89e10cbd311dc` |
| `common_substrate_digest` | intact — `fe0a51267444d8584fa70036f11f990fd36ec4fd09c3597f854134271af823be` |
| canon `full_knowledge` / `qa` | `cbd321aa…` / `1313c0ba…` — unchanged |
| trial order | recomputed from `sha256("EVAL-037|"+trial_id)` — identical method, new namespace |
| model preflight | `gemma-4-31b-it` resolves as an exact id (models.list; no generation call) |
| runner frozen | commit `86dabdd`, before trial 1 |
| lane-run validator | **39/39 gates green** |

Started from `main` at `b66efd1`.

## Outcome

| status | count |
|---|---|
| `complete` | **1** |
| `failed_required_canon_use` | **13** |
| `failed_technical` (rate limit) | **4** |

Format outcome, before the compliance gate: **14 `complete`**, 4 `failed_technical`.
0 format repairs. 0 format failures. 11 transient retries. All 15 failure-classified
attempts were `rate_limit_429`.

## The finding

**Gemma researches well and then refuses to read.**

The objective-driven half of the treatment worked. Across 20 searches Gemma composed
**20 distinct queries, all of them specific production questions** — never the broad
terms the instruction forbade:

- `spatial continuity 180 degree rule cinematic tension café`
- `UGC performance video skincare creator codes`
- `luxury watch photography lighting sunburst dial brushed steel`
- `commercial video pacing problem solution contrast`
- `premium beverage photography lighting composition`

That is exactly the behaviour the treatment asked for, and it is a marked change from
the optional-Canon lane, where it searched zero times.

The second half did not happen. Of the **14 trials that reached a package**, **13 called
`canon_search`, inspected the returned set, and then produced the package without ever
calling `canon_read`** — despite the instruction stating plainly *"You must use at least
one canon_search and one canon_read."* Exactly **one** trial (`B04-R3`) completed the
full search → read → produce cycle, and it is the run's single `complete` trial.

| | all 18 | the 14 that reached a package |
|---|---|---|
| `canon_search` per trial, mean / median | 1.11 / 1 | 1.29 / 1 |
| `canon_read` per trial, mean / median | **0.06 / 0** | **0.07 / 0** |
| results exposed per trial, mean / median | 6.67 / 6 | 7.71 / 6 |

So bounded, objective-driven research is **executable** for this model where unbounded
mandatory research was not — the harness contained retrieval exactly as designed, and
packages were produced. But Gemma treats the search result snippets as sufficient and
does not open an object. Under this treatment it is the *reading* step, not the search
step and not the payload size, that it fails to perform.

## Governor behaviour — the bounds held

| bound | max observed | cap |
|---|---|---|
| `canon_search` per trial | 3 | 3 |
| results per single search | **6** | 6 |
| items exposed per trial | **18** | 18 |
| `canon_read` per trial | 1 | 4 |

One search was refused after a trial had spent its allowance (`B03-R2`, which used all 3
searches and saw the full 18 items). No read was ever refused — the model never
approached the read allowance. Every one of the 20 searches returned **≤ 6 items**, and
`limit` was applied by the harness on every call rather than being left to the model.

## Confound — 4 trials lost to MY execution pacing, not to the model

The 4 `failed_technical` trials are **an artefact of how I dispatched the run**, and are
not a model result and not a property of the treatment. The quota hit was:

```
generativelanguage.googleapis.com/generate_content_paid_tier_3_input_token_count
limit: 16000     (input tokens PER MINUTE)
```

A single trial here averages **11,817 input tokens** (range 6,017–23,840). Running 18
trials back-to-back with no delay therefore exhausts a per-minute allowance on pacing
alone. Trials `B05-R1`, `B04-R1` and `B04-R2` failed on their very first call with zero
turns; `B01-R1` and `B04-R3` were hit mid-tool-loop.

This is unrelated to the `gemma-required-canon` 429s, which were caused by a single
~1.13M-token payload that no pacing could have rescued. These are ordinary
requests arriving too quickly.

**The primary finding is not contaminated by it.** The read-avoidance result rests on the
14 trials that actually reached a package, and those 14 completed normally with 2–5
turns; they chose not to read. The 4 lost trials never got the chance to demonstrate
anything either way.

A paced re-run would convert those 4 into observations. It was not attempted here: the
runner is frozen and obligation 9 forbids changing it after the first call.

## Instrumentation fixes

| # | fix | status |
|---|---|---|
| 1 | Gemini usage: read `usage_metadata` | **added** (absent on `main`) |
| 2 | Canon digest tolerant of mixed YAML keys | **`main`'s implementation, unchanged** |
| 3 | tool/turn history retained past a later failure | **added** (absent on `main`) |
| 4 | Gemini tool-result transport (`datetime.date`) | **added — beyond the three named** |

PR #78's competing digest implementation was **not** imported.

Fixes 1 and 3 are both visibly working in this evidence: usage is reported for **37 of 37
provider turns** (the previous Gemma runs reported 0 of 26), and `B01-R1` retains 3 turns
and 2 searches despite ending in a technical failure — under the old harness it would
have recorded zeros.

Fix 4 is recorded explicitly as an addition beyond the brief's list of three. Bounding
the payload does not avoid the defect: on this corpus **10 of 12** representative
`limit=6` searches and **3 of 24** reads carry a `datetime.date`, so without it most
trials would have died at first retrieval and the treatment could not have been observed.
`main` carries no implementation there, so this was not a choice between versions.

## Usage and cost

| | |
|---|---|
| input | **177,259** |
| output | **17,801** |
| thought | **19,917** |
| cached | `null` — not reported by the provider |
| provider turns | 37, all 37 reporting usage |
| cost | `null` — price not established for `gemma-4-31b-it` at freeze time |

Retrieval totals across the run: **ACCEPTED 72 · HOLD 49 · Q&A 42**. `website_read` was
called 6 times, all on B01/B02, all served from the sealed snapshots.

## Confirmations

- `gemma-full-canon` and `gemma-required-canon` (PR #78) are **untouched**. Neither run
  directory exists on this branch; neither was read, modified, rerun or merged. The
  optional-Canon evidence re-validates **32/32** under this branch's validator.
- **Every search returned ≤ 6 items**, asserted from the governor's own ledger, worst
  single search = 6, worst trial = 18.
- **No variable changed** except the controlled mandatory-retrieval treatment and the
  named instrumentation fixes. Held byte-identical: model, API, settings, the six briefs,
  three repetitions, the system production-package contract, website rules and snapshots,
  the FULL_CANON and Q&A corpora, ACCEPTED/HOLD/Q&A semantics, trial independence, the
  ordering method, retry rules, format-repair rules, no judging, no media, no
  provider/model selection. The only prompt change is a 21-line pure addition
  (`SYSTEM-PROMPT-DIFF.txt`).
- `canon_tools.py` is **unmodified**: the governor is a wrapper, and a governed search was
  verified to return the identical BM25 item order as the frozen tool at `limit=6`.
