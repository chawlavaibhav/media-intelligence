# EVAL-037 — Execution Contract

**Status: FROZEN.** No experimental model call has been made. Every number below was
produced by validators and the deterministic fake provider.

You are an EVAL-037 **execution worker**. You run exactly one lane. Read this file and
your own lane YAML. Nothing else, except the files your lane YAML names.

---

## 0. The one-paragraph version

Eight lanes. Each lane is one model under one condition, run in its own isolated
session: 6 briefs × 3 repetitions = **18 trials**, 8 × 18 = **144 trials** total. Every
trial is a fresh stateless provider request. You produce production-ready creative
packages and evidence. You do **not** judge them, and you do **not** generate media.

---

## 1. Substrate identity — bytes, not a commit

**The experiment-defining bytes are the authority.** No commit SHA is, and none can
be: the substrate was authored *after* the CANON-014 merge, so no commit contains both
the substrate and a fingerprint of itself. Requiring one would be an impossible
self-referential gate.

For the same reason **this document does not print either digest**: it is itself inside
the scope both digests cover, so a literal value here would invalidate itself the
moment it was written. The values live in `FREEZE-FINGERPRINT.yaml`, which is excluded
from its own scope, and the common digest is additionally embedded in every lane YAML,
which the whole-substrate digest covers but the common digest does not. Verify with
`tools/freeze_fingerprint.py --check`.

| Identity | Value | Role |
|---|---|---|
| `freeze_fingerprint` | recorded in `FREEZE-FINGERPRINT.yaml` | **Dispatch gate.** Covers the whole substrate, lanes included. Lives only in `FREEZE-FINGERPRINT.yaml` (excluded from its own scope) and in the controller approval. Verify with `tools/freeze_fingerprint.py --check`. |
| `common_substrate_digest` | recorded in `FREEZE-FINGERPRINT.yaml` and in every lane YAML | Covers the substrate **excluding `lanes/`**, which is what makes it safe to embed in every lane. This is the digest a lane verifies on its own. |
| `canon_base_commit` | `c6f8d910f7a3cdaaeafa2280313abfb9b898cddd` | **Canon provenance only.** The CANON-014 merge the two corpus fingerprints were computed against. It does **not** contain EVAL-037 and is **not** the execution-lane starting commit. |

Execution lanes run from **any checkout that contains the approved frozen substrate**
and has `canon_base_commit` as an ancestor. Preflight verifies both digests and stops
on any mismatch.

| Corpus | Files | Digest |
|---|---|---|
| Full knowledge | 193 | `cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60` |
| Q&A | 23 | `1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd` |
| rentok.com snapshot | — | `4c64d4b3d7487a5ca21a00cb51a43744e149ef61c1ce0e7a1dcbe45e700245f6` |
| getaight.ai snapshot | — | `17b88662e13b17e7694507b6511fdfa0c4399ab3fed5f591ffc337a08b975514` |

---

## 2. Isolation contract

Every execution worker **must**:

1. run from a checkout containing the approved frozen substrate, verifying the
   freeze fingerprint and the common substrate digest before dispatch;
2. read only `EXECUTION-CONTRACT.md`, its own lane YAML, and files that lane YAML names;
3. never list or read sibling lane configs;
4. never inspect another EVAL-037 execution branch, PR, log, output or report;
5. execute exactly **18** trials;
6. use a fresh stateless provider request for every trial;
7. never pass output or state from one trial into another;
8. **freeze and commit its runner before its first experimental call**;
9. make no runner, prompt or config change after its first call;
10. retain every output regardless of apparent quality;
11. do no creative judging;
12. generate no media.

Each lane YAML deliberately repeats every shared fact. That duplication **is** the
isolation property.

---

## 3. Design (fixed)

6 briefs · 3 repetitions · one model × one condition per isolated session · 18 trials
per session · 144 total · fresh provider context per trial · no creative-quality
judging at the reasoning stage · all valid packages remain eligible for later media
generation · media generation and final acceptance scoring are **outside** EVAL-037 ·
no experiment-level spend cap.

### Trial order — deterministic pseudo-random

For each lane, all 18 trial IDs are sorted by `SHA-256("EVAL-037|" + trial_id)`, and
that order is frozen into the lane YAML.

This decorrelates execution position from brief and from repetition, so a position
effect (provider warm-up, drift, rate-limit shaping) cannot line up with a brief or a
repetition. **The validator recomputes the whole ordering** — it does not merely check
that `order_index` runs 1..18, which would pass for any ordering at all.

Trial IDs: `E037-<lane_id>-<brief>-R<rep>`.

---

## 4. Models

Exact ids. **No moving aliases.** Preflight the exact model and **stop rather than
substitute** if it is unavailable.

| Lane key | Provider | Model id | API | Settings |
|---|---|---|---|---|
| `sol` | OpenAI | `gpt-5.6-sol` | Responses API | `reasoning.effort=high`; sampling: provider defaults |
| `sonnet` | Anthropic | `claude-sonnet-5` | Messages API | `thinking={"type":"adaptive"}`, `output_config.effort="high"`; sampling: provider defaults |
| `haiku` | Anthropic | `claude-haiku-4-5-20251001` | Messages API | `thinking={"type":"enabled","budget_tokens":8000}`; sampling: provider defaults |
| `gemma` | Google Gemini API | `gemma-4-31b-it` | Gemini API (`GEMINI_API_KEY`) | provider defaults throughout |

Part of the freeze, not suggestions:

- On `claude-sonnet-5`, `budget_tokens` and `temperature`/`top_p`/`top_k` are removed
  and return 400. "Sampling: provider defaults" is both the instruction and the only
  legal call.
- `claude-haiku-4-5-20251001` is pre-4.6: it takes `budget_tokens` and **rejects**
  `effort`. `budget_tokens` must be below `max_tokens`.
- For `gemma-4-31b-it`, **do not invent unsupported reasoning controls.** No thinking
  budget, no `effort`, no `reasoning_effort`.
- `max_tokens` is a required transport parameter, not a sampling control.

**Every lane gets the same exact-model preflight — there is no model-specific
capability gate.** If a live endpoint rejects a lane's exact tool configuration at run
time, the runner records the concrete API error and that lane **stops**. It never
substitutes another model.

---

## 5. Conditions

### NO_CANON
No Canon instruction, no Canon tool. The worker must not read
`conditions/full-canon.yaml` or any Canon content. System prompt =
`common/system-prompt.txt` verbatim, nothing appended.

### FULL_CANON
Read-only `canon_catalog`, `canon_search`, `canon_read` over the merged status-aware
corpus.

`canon_search` is **deterministic tokenized BM25** (k1=1.2, b=0.75) ranked retrieval
across source knowledge, concept systems, operational bindings, ontology terms and
concepts, visual-evidence items and Q&A. No embedding and no model call. Ties break on
`(-score, source_dir, kind, item_id)`, so the same query always returns the same order.

The **tested model** decides whether to use Canon, what to search, what to read,
whether to consume Q&A, how much to retrieve, and when to stop. There is **no**
aggregate top-K, **no** token budget, **no** retrieval-count budget, and **no**
mandatory use. `canon_search` returns every scoring item unless the model itself asks
for a `limit`.

Status invariants, enforced in code and tested:

- Every returned object carries `source_status`.
- `source_status` is `ACCEPTED` or `HOLD`, taken from the corpus, never inferred.
- **HOLD is never represented, relabelled or defaulted as accepted.**
- An object whose status cannot be established is dropped, not guessed.
- Q&A carries `not_benchmark_ground_truth: true` and `independent_corroboration: false`.

The addendum text lives **only** in `conditions/full-canon.yaml`.

---

## 6. Websites — the `website_read` tool

Website access is a property of the **brief**, not of the condition. `website_read` is
exposed **identically in NO_CANON and FULL_CANON** and serves **byte-identical**
snapshot content in both.

| Brief | Tool exposed | Site |
|---|---|---|
| B01 | yes | `https://rentok.com` |
| B02 | yes | `https://getaight.ai` |
| B03–B06 | **no** | none |

`website_read` returns the frozen `page.txt` for the one site that brief permits, plus
the snapshot sha256 actually served and the source URL. There is no fetch path in the
code: **no live browsing**, and any other domain is **refused**, not fetched. A brief
that permits no website cannot even construct the tool.

The tested model decides whether to call it. **Every call is recorded with its
arguments and the exact snapshot digest returned**, and `website_snapshot_used` is
derived from actual calls — it is never hardcoded.

---

## 7. Retry policy

A retry is licensed **only** by a **TRANSIENT** provider failure:

`timeout`, `connection_error`, `rate_limit_429`, `server_error_5xx`

Initial attempt + maximum **2** transient retries. A retry resends the **identical**
request. On exhaustion: `failed_technical`, every attempt retained, no substitution.

**Deterministic failures are never retried.** `invalid_request_4xx`, `auth_error`,
`tool_schema_rejected`, `context_overflow`, `tool_loop_guard_exhausted`,
`model_refusal`, `truncated_response`, `empty_response`, `sdk_error` → status
`failed_execution`, zero retries.

> Context overflow or tool-loop exhaustion caused by the model's **own** Canon
> consumption is a **model+condition execution failure** and a real result of this
> experiment — not a transient provider fault, and never rerun as one.

Truncation and refusal are detected from the provider's **own stop/finish reason**, not
inferred from missing section headings.

**Format repair** — at most **one** per trial, format only. The repair is a fresh
provider request that **contains**:

1. the original customer brief;
2. the original model answer, verbatim;
3. exactly the frozen format-only instruction.

It must not expose another trial or any new creative guidance. It records
`repair_source_response_digest`.

- A **transient** failure during a repair call retries **that same repair request**
  under the transient policy. It **never** falls back to a fresh creative generation.
- If the repaired answer is **still** structurally invalid: retain it, mark the trial
  **`failed_format`**, and set `eligible_for_media_generation: false`. An invalid
  repair is **never** labelled `format_repaired`.

**Forbidden retry reasons** — the answer looks creatively weak; the idea seems
unoriginal; the package is shorter than expected; a different sample would probably be
better; the model did not use Canon or the website.

> Creative weakness is **never** a reason for another attempt.

**Tool-loop guard** — 100 provider turns, an emergency stop against literal runaway
execution. It is **not** a retrieval budget.

---

## 8. Evidence

Per lane, under `eval/experiments/EVAL-037/runs/<lane_id>/`:

| Path | Contents |
|---|---|
| `attempt-ledger.json` | every attempt (schema: `schemas/attempt-ledger.schema.json`) |
| `result.json` | the 18 trials (schema: `schemas/result.schema.json`) |
| `requests/<trial>-a<n>.request.json` | the **exact serialised request**, not only a digest |
| `raw/<trial>-a<n>.response.json` | the raw provider response |
| `transcripts/<trial>-a<n>.jsonl` | the **complete tool transcript** |
| `packages/<trial>.txt` | the production package |

**Usage and cost.** Every provider invocation — **including every intermediate turn
caused by a tool call** — records: input tokens, cached input tokens, output tokens,
reasoning/thinking tokens, provider model version, provider request id, stop/finish
reason, latency, and the provider-reported usage object verbatim. These are summed to
**trial totals** and **lane totals**. A Canon run's reasoning cost is the sum of *all*
its turns, not only the final response. `*_turns_reporting` counts how many turns
contributed, so a partial sum can never pass as a complete one.

A field the provider does not expose is stored as **null**. Nothing is invented. Cost
comes from the frozen `common/price-snapshot.yaml`; where a price is not established
the cost is `null` and `cost_basis` says why.

**Tool transcript.** Every tool call retains: tool name, the **actual arguments**,
result item IDs, source IDs, `source_status`, item kind, Q&A flag, result digest, and
the **full tool result** in the transcript file with an exact `transcript_ref`. Argument
hashes and aggregate counts are kept too, but they are not what the evidence rests on.

Retain **every** output, including failed and malformed attempts.

---

## 9. How to run a lane

```bash
python3 eval/experiments/EVAL-037/tools/freeze_fingerprint.py --check
python3 eval/experiments/EVAL-037/tools/preflight.py --lane <your lane yaml>
python3 eval/experiments/EVAL-037/tools/runner.py --lane <your lane yaml> --preflight-only
git commit -am "eval-037 <lane>: freeze runner before first call"
python3 eval/experiments/EVAL-037/tools/runner.py --lane <your lane yaml>
python3 eval/experiments/EVAL-037/validators/validate_lane_run.py \
    --lane <your lane yaml> --run eval/experiments/EVAL-037/runs/<lane_id>
```

The commit step is enforced: the runner refuses to start on a dirty tree.

---

## 10. Out of scope

Media generation and final acceptance scoring are explicitly outside EVAL-037. All
structurally valid packages remain eligible for later media generation; eligibility is
never withdrawn on creative grounds. Do not select or recommend an image/video model
or provider anywhere in this experiment.
