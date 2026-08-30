# EVAL-037 — lane `gemma-required-canon` (SUPPLEMENTAL) execution notes

Factual worker record. No creative judging, no media generation, no merge.

**This does not replace or re-run `gemma-full-canon`.** That lane is frozen on its own
branch at `6861c8e` and records that Gemma, *offered* Canon, chose to use it **0/18**
times. This lane asks a different question: **can Gemma produce better production
packages when Canon retrieval is explicitly required?**

## Dispatch

| Gate | Result |
|---|---|
| `freeze_fingerprint` | intact — `f4f3a381248fd8724294ff13bf00953d2a22927687ff50bae87b88a0aae46f5a` |
| `common_substrate_digest` | intact — `8ac0781bf5b98ae68aee2636ad17fb0a9bd18056e2cd316692ecc768a57df684` |
| canon `full_knowledge` | `cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60` (unchanged) |
| canon `qa` | `1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd` (unchanged) |
| trial order | recomputed from `sha256("EVAL-037|"+trial_id)` — identical method, new id namespace |
| model preflight | `gemma-4-31b-it` resolves as an exact id (models.list; no generation call) |
| runner frozen | commit `7590b8d`, before trial 1 of the executed run |
| lane-run validator | **37/37 gates green** |

Started from `main` (`28aefc7`), whose EVAL-037 substrate is byte-identical to
`work/eval-037-freeze` (`396de89`) and which has `canon_base_commit c6f8d91` as an
ancestor. Same interpreter and same `google-genai 2.20.0` as the original lane.

## Outcome — 18/18 `failed_technical`

| | |
|---|---|
| trials executed | 18/18, in the frozen order |
| status | **18 `failed_technical`** |
| attempts | 54 = 18 initial + 36 transient retries (max 2 per trial, per policy) |
| failure class | `rate_limit_429` on all 54 — the one transient class actually seen |
| format repairs | 0 |
| format failures | 0 |
| packages produced | 0 |
| eligible for media generation | 0 |

**No trial satisfied the REQUIRED_CANON gate**, and no trial was marked
`failed_required_canon_use` — correctly so. The gate applies only to a trial the model
actually completed. All 18 died as provider failures before producing an answer, so each
keeps its own `failed_technical` status. The model never got its chance to comply.

## What actually happened, and why it is a result rather than a fault

The treatment worked on the first turn. Gemma **did** compose its own query and call
`canon_search` — something it never did once across 18 trials when Canon was optional.

It then called `canon_search` **without passing a `limit`**. The FULL_CANON condition
deliberately imposes no aggregate top-K, no token budget and no retrieval-count budget:
`canon_search` returns *every* scoring item unless the model itself asks for fewer. For a
representative query it composed —
`"luxury watch photography lighting product photography hero image"` — that is:

| | |
|---|---|
| items returned | **1,506** (ACCEPTED 439 / HOLD 1,067 / Q&A 409) |
| payload | **4,522,040 bytes**, roughly 1.13M tokens |
| provider input-token quota, `gemma-4-31b` | **16,000** |

The follow-up turn carrying that tool result cannot be served at any pacing — it is
~70× the quota, not a burst the retry window can absorb. The API answers
`429 RESOURCE_EXHAUSTED`. The frozen retry policy classifies 429 as **transient**, so the
runner resent the identical request twice, exhausted the budget, and recorded
`failed_technical` with every attempt retained. That is the specified behaviour executing
correctly, not a deviation.

Had the model chosen `limit=10`, the same query returns 23,373 bytes — comfortably
inside quota. Nothing in the harness prevented a bounded search; the model did not
bound it.

So the finding is not "forced Canon produced better packages" or "worse packages". It is:

> Compelled to retrieve, `gemma-4-31b-it` requests the entire matching corpus and cannot
> complete a single turn. Under this model + this condition, mandatory Canon retrieval is
> not merely unhelpful — it is unexecutable.

This is exactly the failure mode the EXECUTION-CONTRACT anticipates in spirit: resource
exhaustion caused by the model's **own** Canon consumption is a model+condition result.
Mechanically it arrived as a 429 rather than a `context_overflow`, so the frozen policy
retried it as transient. That classification was not changed post-freeze.

## Recorded anomaly — retrieval and usage evidence is NOT retained on the failure path

`canon_search`, `canon_read`, ACCEPTED/HOLD/Q&A totals and every token field read **0 /
null** in the sealed evidence, and `raw/`, `transcripts/` and `packages/` are empty. Only
`requests/` is populated.

This under-reports what happened. The model demonstrably called `canon_search` on every
trial; the evidence does not show it.

Cause: all three adapters re-raise a mid-tool-loop provider exception as

```python
except Exception as e:
    raise ProviderError(str(e)[:600], classify_exception(e)) from e   # no detail
```

(`tools/providers.py` lines 269 / 322 / 371). `turns` and `tool_log` are both in scope
and both discarded. The runner already knows how to consume them — it reads
`(e.detail or {}).get("turns", [])` — and the tool-loop-guard raise in the *same*
functions already passes exactly that detail. Only the provider-exception path drops it.

This is **pre-existing**, affects all three adapters equally, and was invisible in the
original lane because no trial there failed. It is not a consequence of any change made
for this run.

Per obligation 9 the runner was **not** modified after the first call and the lane was
**not** rerun. The zeros and nulls are honest: they report missing evidence rather than a
reconstruction passed off as recorded fact.

`lane_calculated_cost_usd` is `null`, basis "price not established for gemma-4-31b-it at
freeze time" — the frozen price snapshot carries no entry for this model, as specified.

## Instrumentation fixes carried by this run

Two were authorised in advance; two more were found at the first provider call and the
third was authorised explicitly before use. All four are detailed byte-by-byte in
`../../SUPPLEMENTAL-FREEZE.md`.

1. **Gemini usage capture** — read `usage_metadata`, not only `usage`.
2. **Canon evidence digest** — mixed bool/str YAML keys can no longer crash a hash.
3. **Gemini tool-result transport** *(found at first call, authorised)* — `datetime.date`
   values from Canon YAML could not be serialised onto the wire, killing every Canon
   retrieval. Aligns the Gemini adapter with the OpenAI and Anthropic ones.
4. **Compliance gate must not mask a provider failure** — a transport fault is no longer
   relabelled as non-compliance.

An earlier freeze (`6962345`) carrying only fixes 1 and 2 dispatched four trials that all
died at the first retrieval on defect 3. Those four were **discarded, not retained as
results**: they are transport failures under a superseded freeze, not observations of the
treatment. The 18 trials above were executed in full from the clean re-freeze `7590b8d`.

## Confirmations

- The frozen `gemma-full-canon` evidence is **untouched**. It exists only on its own
  branch (`6861c8e`); this branch never contained it, modified it, or re-ran it. It
  re-validates **32/32 gates green** under the patched validator.
- **No experimental variable changed** other than the mandatory-Canon treatment and the
  four named instrumentation fixes. Held byte-identical: model, API, settings, the six
  briefs, three repetitions, website rules and snapshots, the common system prompt, the
  corpus and Q&A fingerprints, Canon status semantics, the Canon tools, the trial-ordering
  method, retry rules, format-repair rules, no judging, no media, no provider/model
  selection, fresh stateless context per trial.
- The only prompt change is the appended treatment block —
  see `SYSTEM-PROMPT-DIFF.txt`, a 16-line pure addition.
