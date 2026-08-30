# EVAL-037 — supplemental freeze: `gemma-controlled-canon`

A **new** treatment. It does not replace, alter, rerun or merge either prior Gemma run.
Both remain standing evidence:

| lane | condition | recorded |
|---|---|---|
| `gemma-full-canon` | Canon **optional** | Gemma used Canon **0/18** times |
| `gemma-required-canon` (PR #78) | Canon **mandatory, unbounded** | Gemma searched with no limit, drew 1,506 items (~1.13M tokens) against a 16k quota, **18/18 `failed_technical`** on 429 |

Neither is touched by this branch. Neither run directory exists here.

## The question

Does `gemma-4-31b-it` benefit from Canon when research is **mandatory**, explicitly
**objective-driven**, and **mechanically bounded**, while the model still chooses WHAT
to search for, WHAT to read, and HOW to apply it?

This is the production-relevant shape: optional Canon measured whether the model would
opt in (it did not); unbounded mandatory Canon measured what happens with no guard rails
(it drowned). Neither resembles how a production system would expose a knowledge base.

## The treatment

Canon research is required and aimed at a concrete production decision. The harness owns
the **result count**; the model owns the **query**.

| bound | value | enforced |
|---|---|---|
| `canon_search` per trial | 3 | harness |
| results per search | 6 | harness — `limit` forced before the search runs |
| `canon_read` per research question | 2 | harness |
| `canon_read` per trial | 4 | harness |
| **max items exposable per trial** | **18** | harness |

`limit` is never trusted to the model: omitted → 6; greater than 6 → clamped to 6; less
than 6 → honoured as the model's own tighter choice. A call beyond an allowance is
**refused**, not truncated — the refusal is Canon-free and carries no `source_status`, so
it can never be mistaken for retrieved knowledge. `canon_catalog` is unchanged and
uncounted: a table of contents, not evidence.

Implemented in `tools/controlled_canon.py` as a **wrapper** around Canon dispatch.
`canon_tools.py` is untouched, so Canon contents, the BM25 ranking, the tie-break order
and the ACCEPTED/HOLD/Q&A semantics are exactly what the frozen corpus and tool produce.
Verified: a governed search returns the identical item order as the frozen tool at
`limit=6`.

The harness never curates a query, names a source or object, reranks or filters Canon,
supplies a preselected packet, or reads on the model's behalf.

**Stop rule.** Research stops when the model decides it has enough, or when the allowance
is exhausted. It may not request more research merely because an answer feels weak.

## Compliance

Minimum — a successful trial needs ≥1 effective `canon_search` **and** ≥1 effective
`canon_read`. A package produced without that is retained and marked
`failed_required_canon_use`; never quality-rerun, never resampled. A trial that failed
for a **provider** reason keeps its own status: the model never got its chance to comply,
and relabelling a provider fault as non-compliance would misreport the experiment.

Maxima — **prevented, not punished.** They cannot be exceeded because the governor
refuses the excess call. The validator asserts them anyway from the governor's own
ledger, so the claim rests on evidence rather than trust.

## Instrumentation fixes

Carried forward as the minimum needed for this run. Where `main` already has an accepted
implementation it is used unchanged.

| # | fix | status |
|---|---|---|
| 1 | Gemini usage: read `usage_metadata` as well as `usage` | **added** — absent on `main` |
| 2 | Canon digest tolerant of mixed YAML key types | **taken from `main` unchanged** (`json.dumps(out, default=str)`) |
| 3 | Provider/tool history completed before a later failure is retained | **added** — absent on `main`; adapters now pass `{"turns", "tool_calls"}` as `ProviderError` detail, and the runner transcribes them exactly as on the success path |
| 4 | Gemini tool-result transport (`datetime.date`) | **added — beyond the enumerated three; see below** |

PR #78's competing digest implementation was **not** imported. `main`'s stands.

### Fix 4 — a necessary addition beyond the three named

`google-genai` serialises the outgoing request with a bare `json.dumps()` and no
`default=`, so any `datetime.date` raises `TypeError` before the call leaves the process.
Canon YAML reads a bare date as `datetime.date`. Bounding the payload does **not** avoid
it — measured on this corpus:

- **10 of 12** representative bounded (`limit=6`) searches carry at least one date
- **3 of 24** reads of returned objects carry one

So without this fix the great majority of trials die at their first retrieval and the
treatment cannot be observed at all. `main` has no implementation here, so this is not a
choice between competing versions. It aligns the Gemini adapter with the OpenAI and
Anthropic adapters, which already pre-serialise with exactly `json.dumps(out,
default=str)`. A date becomes its ISO-8601 string; nothing else changes.

This is the same fix authorised during the `gemma-required-canon` run. It is recorded
here explicitly because it is **not** among the three fixes named in the brief for this
run.

## Everything else held identical

model `gemma-4-31b-it` · Gemini API · model settings (provider defaults throughout) · the
six briefs byte-for-byte · three repetitions per brief · the system production-package
contract · website rules and the frozen snapshots · the FULL_CANON corpus and the Q&A
corpus · ACCEPTED/HOLD/Q&A semantics · trial independence and fresh stateless context ·
the trial-ordering method · retry rules · format-repair rules · no creative judging · no
media generation · no model or provider selection.

The only prompt change is the appended treatment block — see `SYSTEM-PROMPT-DIFF.txt`, a
21-line pure addition. The common system prompt's own sha256 is unchanged.

## Substrate identity

Started from `main` at `b66efd1`. The digest necessarily differs from `main`'s, because
this run adds `conditions/full-canon-controlled.yaml` and `tools/controlled_canon.py` and
carries the fixes above. `git diff origin/main` on this branch shows exactly that set.

Unchanged and still carrying their frozen individual digests: all six briefs, the common
system prompt, both website snapshots, the price snapshot, `conditions/full-canon.yaml`,
the Canon corpus (`full_knowledge` `cbd321aa…`, `qa` `1313c0ba…`), `canon_tools.py`,
`website_tools.py`, `preflight.py`, `freeze_fingerprint.py`, `build_lanes.py`,
`snapshot_websites.py`, `experiment.yaml`, `EXECUTION-CONTRACT.md`, and all eight
original lane YAMLs.

Because the eight original lane YAMLs are left untouched they will not preflight on this
branch. That is correct: this branch is not their substrate. (`main` itself already
carries this inconsistency for seven of them after PR #77 updated only the sonnet lane —
`validate_freeze` F1c fails on `main` as it stands.)

## Schema changes are additive

Widened id patterns, the `failed_required_canon_use` status, and new optional fields.
Proven additive by re-validating the **original** `gemma-full-canon` `result.json` and
`attempt-ledger.json`: both still VALID, and that lane's sealed evidence re-validates
32/32 under this branch's validator.

## Verified before the first provider call

- 14 governor invariants unit-tested, including: omitted `limit` forced to 6; `limit=500`
  clamped to 6; `limit=2` honoured; 4th search refused; 3rd read per question refused;
  total reads capped at 4; ≤18 items exposed; `canon_catalog` uncounted; refusals carry no
  `source_status`; every result still carries ACCEPTED/HOLD; **BM25 order identical to the
  frozen tool**.
- Four fake-provider dry runs (no network): a compliant researcher, a *greedy* researcher
  reproducing the PR #78 behaviour (5 searches × `limit=500` × 8 reads → contained to
  3 / 18 items / 4 reads), a search-only non-complier, and a no-tools non-complier.
  All four validate **39/39**.
- Substrate suite **152/153**; the single failure is `T125`, which asserts no provider SDK
  is installed and fails only because the run venv necessarily has `google-genai`.

These bytes were committed before any experimental call.
