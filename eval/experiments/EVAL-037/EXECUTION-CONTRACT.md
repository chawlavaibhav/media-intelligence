# EVAL-037 — Execution Contract

**Status: FROZEN.** This substrate is complete and no experimental model call has been
made. Every number below was produced by validators and the fake provider.

You are an EVAL-037 **execution worker**. You run exactly one lane. Read this file and
your own lane YAML. Nothing else, except the files your lane YAML names.

---

## 0. The one-paragraph version

Eight lanes. Each lane is one model under one condition, run in its own isolated
session: 6 briefs × 3 repetitions = **18 trials**, 8 × 18 = **144 trials** total. Every
trial is a fresh stateless provider request. You produce production-ready creative
packages and evidence. You do **not** judge them, and you do **not** generate media.

---

## 1. Frozen base

| | |
|---|---|
| Base commit | `c6f8d910f7a3cdaaeafa2280313abfb9b898cddd` |
| Base subject | `CANON-014: integrate full Canon corpus` |
| Freeze branch | `work/eval-037-freeze` |
| Full-knowledge fingerprint | `cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60` (193 files) |
| Q&A fingerprint | `1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd` (23 files) |
| rentok.com snapshot | `4c64d4b3d7487a5ca21a00cb51a43744e149ef61c1ce0e7a1dcbe45e700245f6` |
| getaight.ai snapshot | `17b88662e13b17e7694507b6511fdfa0c4399ab3fed5f591ffc337a08b975514` |

Start from **exactly** that commit. If your HEAD's merge-base with it is not it, stop.

---

## 2. Isolation contract

Every execution worker **must**:

1. start from the exact frozen base commit recorded above;
2. read only
   - `EXECUTION-CONTRACT.md`
   - its own lane YAML
   - files explicitly referenced by that lane YAML;
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

Each lane YAML is deliberately repetitive: it carries the model config, condition,
tool list, brief paths, prompt path, addendum path, snapshot paths, all 18 trial IDs in
order, the retry policy, the evidence paths and schemas, and the frozen base commit.
That duplication **is** the isolation property. You never need a sibling file.

---

## 3. Design (fixed — not open to lane-level interpretation)

- 6 briefs
- 3 independent repetitions
- one model × one condition per isolated execution session
- 18 trials per session
- 144 trials total
- fresh provider context for every trial
- no creative-quality judging at the reasoning stage
- all valid packages remain eligible for later media generation
- media generation and final acceptance scoring are explicitly **outside** EVAL-037
- no experiment-level spend cap
- technical failure: initial attempt + **maximum 2** technical retries
- exactly **one** format-only repair if required
- **no retry because an answer looks creatively weak**

Trial order is repetition-major — all six briefs at R1, then R2, then R3 — so the three
repetitions of a brief are maximally separated. Every trial is stateless regardless;
the ordering makes accidental carry-over visible rather than hidden.

Trial IDs: `E037-<lane_id>-<brief>-R<rep>`, e.g. `E037-sonnet-full-canon-B04-R2`.

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

Notes that are part of the freeze, not suggestions:

- On `claude-sonnet-5`, `budget_tokens` and `temperature`/`top_p`/`top_k` are **removed
  and return 400**. "Sampling: provider defaults" is therefore both the instruction and
  the only legal call.
- `claude-haiku-4-5-20251001` is a pre-4.6 model: it takes `budget_tokens` and
  **rejects** the `effort` control. `budget_tokens` must be below `max_tokens`.
- For `gemma-4-31b-it`, **do not invent unsupported reasoning controls.** There is no
  thinking budget, no `effort`, no `reasoning_effort`. If a control is not documented
  for this model, it is not set.
- `max_tokens` is a required transport parameter, not a sampling control. It is set
  uniformly in `tools/providers.py` and is generous enough that no trial is truncated
  by our own ceiling.

**Open gate — `gemma-full-canon`.** Gemma served through the Gemini API has
historically not supported function calling or a separate system instruction. Before
trial 1 that lane must confirm the live model accepts tool declarations. If it does
not: **STOP and escalate.** Do not run a tool-less lane and call it FULL_CANON — that
is a different condition wearing this one's name. `tools/preflight.py` returns exit
code 3 on that lane to force the check.

---

## 5. Conditions

### NO_CANON

- The tested model receives **no** Canon instruction.
- **No** Canon tool is exposed.
- The execution worker must **not** read `conditions/full-canon.yaml` or any Canon
  content. Reading Canon here contaminates the control condition.
- System prompt = `common/system-prompt.txt` **verbatim**, nothing appended.

### FULL_CANON

The merged status-aware full corpus. Read-only tools: `canon_catalog`, `canon_search`,
`canon_read`.

The **tested model** decides: whether to use Canon, what to search, what to read,
whether to consume Q&A, how much to retrieve, and when to stop.

There is **no** aggregate top-K, **no** Canon token budget, **no** retrieval-count
budget, and **no** mandatory Canon use. `canon_search` returns every match unless the
model itself asks for a limit.

Status invariants, enforced in code and tested:

- Every returned object carries `source_status`.
- `source_status` is `ACCEPTED` or `HOLD`, taken from the corpus, never inferred.
- **HOLD is never represented, relabelled or defaulted as accepted.**
- An object whose status cannot be established is dropped, not guessed.
- Q&A items carry their source's status plus `not_benchmark_ground_truth: true` and
  `independent_corroboration: false`. Q&A is accessible knowledge, **not** independent
  corroboration and **not** benchmark truth.

The FULL_CANON addendum text lives **only** in `conditions/full-canon.yaml`. It is
appended to the common system prompt after one blank line. Nothing else is added.

---

## 6. Websites

Website access is limited to two frozen snapshots, taken once during this setup task:

| Brief | Site | Snapshot |
|---|---|---|
| B01 | `https://rentok.com` | `common/websites/rentok.com/` |
| B02 | `https://getaight.ai` | `common/websites/getaight.ai/` |

B03–B06 permit **no** website.

- **No live browsing during experimental calls.** Ever.
- **No other websites.** Ever.
- Each snapshot holds `index.html` (raw bytes), `page.txt` (deterministic text
  extraction), `headers.txt`, `fetch.json` and `SNAPSHOT.yaml` with digests.
- The **tested model** decides whether to inspect the permitted snapshot.

---

## 7. Retry policy

**Technical failure** — initial attempt + maximum **2** technical retries (3 attempts
max). A retry is licensed *only* by a named technical failure class:

`timeout`, `connection_error`, `rate_limit`, `server_error_5xx`, `empty_response`,
`truncated_response`, `provider_refusal_non_content`, `sdk_error`.

A technical retry resends an **identical** request. On exhaustion, record the trial as
`failed_technical`, retain every attempt, and do not substitute a model, relax a
setting or hand-write a package.

**Format repair** — at most **one** per trial, **format only**. Permitted when the
response is present and substantive but lacks the required `FINAL_PRODUCTION_PACKAGE`
section structure. The repair may ask only for the same answer in the required shape.
It may not change, steer, enrich or improve the creative content.

**Forbidden retry reasons** — the answer looks creatively weak; the idea seems
unoriginal or safe; the package is shorter than expected; a different sample would
probably be better; the model did not use Canon.

> Creative weakness is **never** a reason for another attempt. Retrying on quality
> silently selects best-of-N and destroys the comparison this experiment exists to make.

The runner has no quality notion and cannot judge. `is_well_formed()` is a mechanical
section-presence check and nothing more.

---

## 8. Spend

No experiment-level spend cap. Cost is recorded, not enforced.

---

## 9. How to run a lane

```bash
# 1. Confirm the exact model. Stop rather than substitute.
python3 eval/experiments/EVAL-037/tools/preflight.py --lane <your lane yaml>

# 2. Confirm the substrate, without calling anything.
python3 eval/experiments/EVAL-037/tools/runner.py --lane <your lane yaml> --preflight-only

# 3. FREEZE AND COMMIT YOUR RUNNER. The runner refuses to start on a dirty tree.
git commit -am "eval-037 <lane>: freeze runner before first call"

# 4. Execute all 18 trials.
python3 eval/experiments/EVAL-037/tools/runner.py --lane <your lane yaml>

# 5. Validate your own evidence before opening a PR.
python3 eval/experiments/EVAL-037/validators/validate_lane_run.py \
    --lane <your lane yaml> --run eval/experiments/EVAL-037/runs/<lane_id>
```

Step 3 is enforced: `preflight()` refuses to proceed while the runner tree is dirty.
After your first call, change nothing — not the runner, not the prompt, not the config.

---

## 10. Evidence

Per lane, under `eval/experiments/EVAL-037/runs/<lane_id>/`:

| File | Schema |
|---|---|
| `attempt-ledger.json` | `schemas/attempt-ledger.schema.json` |
| `result.json` | `schemas/result.schema.json` |
| `raw/<trial>-a<n>.json` | raw provider response per attempt |
| `packages/<trial>.txt` | the production package |

Retain **every** output, including failed and malformed attempts. Nothing is deleted,
trimmed or tidied. `result.json` carries no creative-quality judgement and no media.

---

## 11. What the substrate already proves

Everything below was run at freeze time, against the deterministic fake provider. **No
experimental model call was made.**

| Check | Result |
|---|---|
| `validators/validate_freeze.py` | 27 gates, all PASS |
| `validators/test_substrate.py` | 63 tests, 63 pass, 0 fail |
| `validators/validate_lane_run.py` on all 8 fake lane runs | 8/8 PASS |
| Trials executed on the fake provider | 144 (8 lanes × 18) |
| Real provider calls | **0** |

The tests are mostly negative: they break one rule each and assert rejection — a
dropped trial, reordered trials, a third technical retry, a second format repair, a
moving alias, an unlicensed retry, a media file in the run directory, a NO_CANON run
claiming Canon fingerprints, a HOLD item presented without its status.

---

## 12. Out of scope

Media generation and final acceptance scoring are explicitly outside EVAL-037. All
structurally valid packages remain eligible for later media generation; eligibility is
never withdrawn on creative grounds. Do not select or recommend an image/video model
or provider anywhere in this experiment.
