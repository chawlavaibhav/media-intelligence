# EVAL-037 — supplemental treatment `sonnet-controlled-canon`

**This is a supplemental run. It replaces nothing.**

The original `sonnet-full-canon` lane (PR #71) and the repaired unbounded-retrieval run
(PR #77, now on `main`) remain the evidence of what happens when `claude-sonnet-5` is
given unrestricted autonomous Canon retrieval. This lane writes to its own run
directory, under its own trial ids, on its own branch, and touches neither.

## The question

Can `claude-sonnet-5` **benefit** from the full Canon corpus when retrieval is
**objective-driven and controlled** rather than free-form and unbounded?

The unbounded lane answered a different question and answered it clearly: given no
retrieval discipline, the model exhausts its own context. One unbounded `canon_search`
over this corpus returns **3,999 items / 10.4 MB / ~2.6M tokens** — more than the
context window, from a single call. That is a real property of the model+condition
pairing and it stands.

This lane approximates the production system we actually want instead: the reasoning
model researches **only what it needs** to produce the customer's requested media
outcome.

## The one changed variable

Everything is the frozen `sonnet-full-canon` treatment except how retrieval is
conducted.

**Unchanged:** model `claude-sonnet-5` · Anthropic Messages API · adaptive thinking ·
`effort=high` · provider-default sampling · the six briefs byte-for-byte · three
repetitions · the common system prompt · the FULL_CANON corpus and Q&A corpus (Canon
was **not** altered; both fingerprints recompute unchanged) · ACCEPTED/HOLD/Q&A status
semantics · website rules and frozen snapshots · the production-package schema · the
trial-ordering method · the technical retry policy · the format-repair policy ·
stateless independent trials · no creative judging · no media generation · no
model/provider selection.

**Changed:** the retrieval treatment, expressed in the condition addendum.

The `CONTROLLED_CANON` addendum keeps the FULL_CANON corpus and status paragraphs
**verbatim** and replaces exactly two lines — `Use any amount of it if useful, or
none.` and `Decide for yourself what is relevant.` — because unbounded discretion *is*
the variable under test. The controlled research procedure takes their place.

## The procedure asked of the model

| Step | Ask |
|---|---|
| 1 — identify | At most **three** concrete production knowledge needs, declared in the model's own working message under a `RESEARCH_NEEDS:` line. Not facts the customer supplied. Not provider/model recommendations. No broad exploration. |
| 2 — search | At most **one** `canon_search` per need, queried for that need only, **passing `limit` ≤ 8**. Ceiling: 3 searches, 24 result items. |
| 3 — read | Read only the items judged worth reading: ≤ 3 objects per need, ≤ **6** total, by `item_id` where possible. `canon_catalog` discouraged. |
| 4 — stop | Stop when the production decision can be made. Unused allowance is not a reason to keep going. |
| 5 — produce | The same frozen `FINAL_PRODUCTION_PACKAGE`, from the brief, the permitted website snapshot, and only the Canon knowledge actually retrieved **and judged useful**. `KNOWLEDGE_AND_WEBSITE_USE` lists what was actually used. |

## Treatment, not guard — and why that matters

> The retrieval limits are an **experimental treatment**, not a technical
> context-window guard.

The harness caps, truncates, clamps and blocks **nothing**. `canon_search` still
returns every scoring item when `limit` is omitted — that default is deliberately left
alone, so a model that ignores the treatment is **observed** doing so rather than
silently rescued into looking compliant.

Compliance is **measured after the fact** by `tools/controlled_retrieval.py`. A trial
that exceeds the allowance is recorded **`failed_controlled_retrieval`**, its output
retained, `eligible_for_media_generation: false`. It is never repaired by changing the
treatment, never rescued by expanding the allowance, and **never re-run**.

Gate `C10` proves the non-enforcement empirically: for every `canon_search`, the tool's
own `limit_applied` must equal the `limit` the model asked for — including `None`.

**If the model cannot produce a useful package inside this procedure, that is a
result.**

## Harness changes carried forward

Only the two already-established instrumentation fixes, plus the mechanics the
treatment itself requires. No unrelated improvements.

| # | Change | Why |
|---|---|---|
| **EVIDENCE-001** | Canon tool-result digest must not crash on mixed YAML key types | **Already on `main`** via PR #77; inherited, not re-applied. |
| **EVIDENCE-002** | Failed provider/tool paths preserve completed provider turns and Canon tool transcripts | Every raise out of an adapter loop now carries `_detail()`: completed turns, completed tool calls (with full results, so the transcript is still written), and assistant text emitted alongside a tool call. The runner persists all of it on the failure path exactly as on the success path. PR #77 flagged this exact gap and deliberately left it for a separate decision: its 16 overflow trials recorded `turns=0 canon=0` and its lane cost covered only the 2 complete trials. |
| *treatment mechanics* | `trial_id_prefix` on a lane | Distinct trial ids (`E037SCC-sonnet-…`) so this run can never collide with or be mistaken for existing evidence. The ordering **method** is untouched — ids are still sorted by `sha256("EVAL-037\|" + trial_id)`. Absent the field, behaviour is byte-identical to before. |
| *treatment mechanics* | `CONTROLLED_CANON` condition | Accepted by the runner and by `canon_tools`. The Canon tools, corpus, BM25 ranking and status semantics it receives are **byte-identical** to FULL_CANON; the module cannot tell which condition is running. |
| *treatment mechanics* | intermediate assistant text captured per turn | The model's own declared `RESEARCH_NEEDS` are required evidence. Capture only — never fed back to the model, never edited. |
| *treatment mechanics* | additive schema extension | New lane id, condition, trial-id form, the `failed_controlled_retrieval` status, and the `controlled_retrieval` evidence block. Verified additive: existing lane evidence still validates unchanged. |

## Freeze status — lane-scoped, and F1c is red **on `main` already**

These changes live inside the common-substrate scope, so the freeze necessarily moved:

| | value |
|---|---|
| `common_substrate_digest` | re-stamped on **this lane only** |
| `freeze_fingerprint` | regenerated in `FREEZE-FINGERPRINT.yaml` |

The eight original lane YAMLs are **deliberately left untouched** — re-stamping them
would modify the original EVAL-037 freeze. `validate_freeze.py` gate **F1c** is
therefore red on this branch.

**F1c and `test_substrate.py` were already red on `main` before this branch existed**,
inherited from the PR #77 merge, which re-stamped only `lanes/sonnet-full-canon.yaml`
and left the other seven carrying `d8b2c045…`. Verified against a clean checkout of
`main`. A programme-wide re-stamp is a controller decision, not this worker's.

**This freeze is LANE-SCOPED.** It is valid for `sonnet-controlled-canon`.

## Evidence recorded per trial

Declared knowledge needs · every `canon_search` query with its requested `limit` and
the results actually returned · every `canon_read` target · totals against each
allowance · violation list and compliance verdict · ACCEPTED/HOLD/Q&A counts · provider
turns · input/output/cached/reasoning tokens · cost · latency · the final package ·
failures, retries and format repair.

## Validation

```bash
python3 tools/freeze_fingerprint.py --check
python3 tools/preflight.py --lane lanes/sonnet-controlled-canon.yaml
python3 validators/validate_lane_run.py \
    --lane lanes/sonnet-controlled-canon.yaml --run runs/sonnet-controlled-canon
python3 validators/validate_controlled_retrieval.py \
    --lane lanes/sonnet-controlled-canon.yaml --run runs/sonnet-controlled-canon
```

`validate_lane_run.py` is **unmodified** and still owns every frozen gate.
`validate_controlled_retrieval.py` adds only the treatment's own questions.
