# EVAL-037 — supplemental freeze: `gemma-required-canon`

This branch carries a **supplemental** treatment lane. It does not replace, re-run,
amend or reinterpret the frozen `gemma-full-canon` lane, whose evidence stays exactly
as sealed on `work/eval-037-gemma-full-canon`: Gemma was offered Canon and chose to use
it **0/18** times.

The question here is different: **can Gemma produce better production packages when
Canon retrieval is explicitly required?**

## The one experimental treatment change

Canon use is mandatory. Before finalizing each production package the tested model must
call `canon_search` at least once with a query **of its own choosing**, inspect the
results, call `canon_read` on at least one retrieved object **it** chooses, and then
decide for itself what knowledge to apply.

We force **retrieval**, not the answer. The harness curates no query, names no source or
object, supplies no preselected Canon packet, and imposes no retrieval-token quota and
no fixed top-K.

## Held identical to the frozen `gemma-full-canon` lane

model `gemma-4-31b-it` · Gemini API · model settings (provider defaults throughout) ·
the six briefs byte-for-byte · three repetitions per brief · website rules and the
frozen website snapshots · the common production-package system prompt · the FULL_CANON
corpus and Q&A fingerprints · Canon status semantics · the Canon tools · the
trial-ordering method · the retry rules · the format-repair rules · no creative judging ·
no media generation · no provider/model selection · a fresh stateless context for every
trial.

The Python environment is the same interpreter and the same `google-genai 2.20.0` the
original lane ran on.

## Why the substrate digest necessarily differs

The original freeze covers the tools and schemas, so any instrumentation fix moves it.
Both the original and the supplemental values are recorded here, and every changed byte
is enumerated below. `git diff origin/main` on this branch shows exactly this set and
nothing else.

| | original EVAL-037 freeze | supplemental |
|---|---|---|
| `freeze_fingerprint` | `5fc021d96d23299e977600735cc8cf0f950f61d6ed7cd8b39099f9a10aa189ee` | see `FREEZE-FINGERPRINT.yaml` |
| `common_substrate_digest` | `d8b2c045c61e22668bf6bb8b6b387250efce8c80b1e909029e21d3d6a6c0ebc2` | see `FREEZE-FINGERPRINT.yaml` |

Unchanged and still carrying their frozen individual digests: all six briefs, the common
system prompt, both website snapshots, the price snapshot, `conditions/full-canon.yaml`,
the Canon corpus (`full_knowledge` `cbd321aa…`, `qa` `1313c0ba…`), `canon_tools.py`,
`website_tools.py`, `preflight.py`, `freeze_fingerprint.py`, `build_lanes.py`,
`snapshot_websites.py`, `experiment.yaml`, `EXECUTION-CONTRACT.md`, and all eight
original lane YAMLs.

Because the eight original lane YAMLs embed the *original* common digest and are left
untouched, they will not preflight on this branch. That is correct: this branch is not
their substrate. They preflight on `main` and on their own branches, unchanged.

## Every changed byte, and why

### 1. `tools/providers.py` — instrumentation fix: Gemini usage capture
`turn_record()` read `_get(raw, "usage")`. The `google-genai` response object names the
field **`usage_metadata`**, so every Gemini token count was recorded as `null` while the
provider had in fact reported it — the anomaly the frozen lane recorded and correctly
declined to fix mid-run. Both names are now consulted, `usage` first, so the Anthropic
and OpenAI branches resolve exactly as before. Verified against a retained raw response
from the frozen run: `input 3577 / output 1619 / reasoning 792`, previously all `null`.

### 2. `tools/providers.py` — instrumentation fix: Canon evidence digest
The Canon corpus contains 12 YAML mappings with **mixed boolean and string keys** (YAML
1.1 reads a bare `on:`/`yes:`/`no:` key as a boolean). `json.dumps(..., sort_keys=True)`
then compares a `bool` against a `str` and raises `TypeError`, aborting a Canon
retrieval that had already succeeded — purely while computing an evidence hash.
Reproduced on `scs_lsmx_001` via both `canon_read` and `canon_search`.

`_digest_keys()` / `_digest_blob()` coerce mapping keys to strings **on the way to the
hash only**. The object returned to the caller, and therefore to the model, is the
untouched original — verified: the returned item still carries its original `bool` key.
All-string-key results digest exactly as before, and the corpus contains no
`str(key)` collisions.

### 2b. `tools/providers.py` — instrumentation fix: Gemini tool-result transport

**Found at the first provider call, not before it, and authorised separately.** The
first freeze was executed as specified with only the two named fixes. Four trials were
then dispatched and all four died at the model's first Canon retrieval:

```
google/genai/_api_client.py:1470   data = json.dumps(http_request.data)   # no default=
TypeError: Object of type date is not JSON serializable
  ... 'first_seen' -> 'item' -> 'results' -> 'functionResponse' -> 'contents'
```

`google-genai` serialises the outgoing request with a bare `json.dumps()` and no
`default=`, so any `datetime.date` raises before the call leaves the process. The Canon
corpus carries **1410** such values — YAML reads a bare date as `datetime.date`. The
OpenAI and Anthropic adapters already pre-serialise their tool results with exactly
`json.dumps(out, default=str)`; the Gemini adapter alone passed the raw Python object
into `contents`. The fix aligns it with the other two and does nothing else: a date
becomes its ISO-8601 string, no other value is touched.

This defect **could not have surfaced in the frozen `gemma-full-canon` lane**, which
called Canon zero times. Forcing retrieval is precisely what exposes it.

The four dead trials were discarded, not retained as results — they are transport
failures under a superseded freeze, not observations of the treatment. The run below was
executed in full from a clean re-freeze.

### 2c. `tools/runner.py` — compliance gate must not mask a provider failure

Exposed by those same four trials: the gate overrode `failed_execution` with
`failed_required_canon_use`, reporting a transport fault as a behavioural result. The
gate now applies only to a trial the model actually completed
(`complete` / `format_repaired` / `failed_format`). A transient or deterministic
provider failure keeps its own status: the model never got its chance to comply.

All four fixes are instrumentation only. None alters Canon content returned to the model,
BM25 ranking, any prompt, any brief, the model configuration, or retry behaviour.

### 3. Treatment wiring (not a cleanup — the treatment itself)

- **`conditions/full-canon-required.yaml`** *(new)* — the frozen FULL_CANON addendum
  text verbatim, followed by the mandatory-Canon instruction. Asserted at build time and
  re-checked by validator gate R38.
- **`lanes/gemma-required-canon.yaml`** *(new)* — derived mechanically from
  `lanes/gemma-full-canon.yaml`; `LANE-DIFF.txt` in the run directory is the full diff.
- **`tools/runner.py`** — (a) `expected_trial_order()` accepts a lane-declared
  `trial_id_prefix` so this run occupies its own trial-id namespace; the ordering method
  is unchanged and the default path is bit-identical for every existing lane. (b) the
  REQUIRED_CANON compliance gate, evaluated **after** the trial from evidence already
  collected: it issues no further provider call, so a non-compliant trial is recorded and
  never quality-retried or resampled. (c) the treatment id and the per-trial
  `canon_search` / `canon_read` / `canon_catalog` counts are written into the evidence.
- **`schemas/*.json`** — additive only: widened id patterns, the new
  `failed_required_canon_use` status, and the new optional fields. Proven additive by
  re-validating the **original** `gemma-full-canon` `result.json` and
  `attempt-ledger.json` against the widened schemas: both still VALID.
- **`validators/validate_lane_run.py`** — gates R34–R38, which fire only when
  `treatment == "REQUIRED_CANON"`. Every other lane validates through exactly the
  original 33 gates.
- **`tools/fake_provider.py`** — one test-only scenario, `required_canon_user`, so the
  compliance gate could be exercised in both directions with no network call before the
  first real one. The fake provider is never reachable in a live run.

## Compliance gate

A trial satisfies REQUIRED_CANON only if its retained evidence contains **≥ 1
`canon_search`** *and* **≥ 1 `canon_read`**. `canon_catalog` alone is deliberately not
Canon use. On violation: the output is **retained**, the trial is marked
`failed_required_canon_use`, and it is **not** quality-retried and **not** resampled.
Non-compliance is a real result of this treatment, not a fault to be sampled away.

## One tension, recorded rather than edited away

The frozen FULL_CANON addendum contains the line *"Use any amount of it if useful, or
none."* The appended treatment block states that Canon use is required. The frozen text
was preserved verbatim rather than edited, because editing it would have changed a
variable the brief required to be held constant. The treatment block is later in the
prompt and states the requirement explicitly.

## Frozen before the first provider call

These bytes were committed before any experimental call. `runner_commit` in the sealed
evidence is that commit.
