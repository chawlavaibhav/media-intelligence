# EVAL-012 — EMP-001 zero-spend readiness

**Verdict:** `READY_FOR_SPEND_APPROVAL`

**Branch:** `work/eval-012-emp-001-zero-spend` · **not merged**
**External provider/model/evaluator calls made by EVAL-012: 0**
**External spend: USD 0 / INR 0**

Evidence for every claim below is in
[`VERIFICATION-PRE-SPEND.md`](VERIFICATION-PRE-SPEND.md), copied from fresh runs in this branch.

---

## What the verdict means, and what it does not

It means the repository is now mechanically ready to spend money: the harness, the material and
the gates exist and were executed. **The next Controller decision is about authorising calls, not
about whether the code is ready.**

It does **not** mean anything has been measured. The empirical floor is unchanged:

- 0 qualified models or workflows;
- 0 qualified subjective/perceptual evaluator families;
- 0 empirical Capability Registry rows;
- 0 accepted evidence that Canon improves model outcomes.

Every result produced by this branch is synthetic, marked `may_populate_registry: false`, and the
real harness boundary refuses it — verified against `eval/v1/harness/harness.py` itself rather
than asserted in prose.

---

## Zero-spend artifacts built

| Artifact | What it is |
|---|---|
| `config.yaml` | frozen EMP-001 configuration; `status: PREPARED_NOT_AUTHORISED` |
| `authorization.example.yaml` | schema only — `authorised: false`, ceiling 0, no secrets |
| `budget_guard.py` | fail-closed authorisation gate + cumulative Decimal spend guard |
| `providers.py` | OpenAI/Gemini judge request builders, parsers, fail-closed dispatch |
| `preflight.py` + `preflight-result.json` | Q1/Q7/Registry/baseline/authorisation preflight, executed |
| `protected-baselines.sha256` | pre-EMP-001 fingerprints of 13 protected artifacts |
| `text_qualification/latin-pack-v1.jsonl` + `.sha256` | the frozen 96-item Latin pack |
| `text_qualification/build_latin_pack.py` | deterministic builder; refuses to write into the battery |
| `text_qualification/render_latin_pack.py` | local rasteriser + decoded-pixel perceptibility gate |
| `text_qualification/perceptibility-mechanical.json` | 48/48 mismatches visible in pixels |
| `text_qualification/perceptibility-review.csv` | human sheet, emitted **unfilled** |
| `text_qualification/qualification-contract-v1.yaml` | thresholds, all `PROVISIONAL_FIRST_RUN_GATE` |
| `text_qualification/qualify_text.py` | progressive Devanagari-first runner |
| `atex/atex-items-v1.jsonl` + `ATEXT-CONTRACT.md` | the four frozen items and their stop rule |
| `atex/run_atex.py` | the gated 16-generation runner |
| `tests/` (10 files) | 162 controls, each paired with a way it can fail |
| `VERIFICATION-PRE-SPEND.md` | fresh command output from the pre-spend gate |

## What was proved, by execution

- **Q1 geometry** — fixture count **102**, every declared image present.
- **Q7 persistence** — inherited V1 harness self-test **107/107**, exit 0; Resources cross-branch
  validation **PASS**, exit 0.
- **Registry** — **0** empirical rows, byte-identical before and after every dry run.
- **One call = one trial** — including refused calls, which keep their trial, reason and cost.
- **Retries authorised = 0** — when all 16 A-TEXT calls refuse, a seventeenth is dispatched
  exactly zero times.
- **No network for `--dry-run`** — proved by poisoning `socket` and running the whole preflight,
  with the V1 self-test invoked in-process so the poison actually covers it.
- **Disabled/missing authorisation blocks the live adapter path** — a real judge refuses without a
  transport, and refuses again without a budget guard.
- **Synthetic evidence cannot reach the Registry** — exercised against the real harness with a
  `qualified` instrument, so only the synthetic guard could have refused it.
- **Latin pack** — 96 items, 48 match / 48 mismatch, one mismatch per base string, 8 per failure
  class, every base string in both strata, every corruption re-derived from the strings alone.
- **The frozen Devanagari battery is intact** — all 13 protected baselines hash unchanged, and the
  96-item validated view was materialised **outside** the battery, its rebuilt `items.jsonl`
  matching the frozen `battery_identity` SHA.
- **16-generation ceiling** — 4 items × 2 unseeded repeats × 2 routes, counted on a fake generator.

---

## Remaining prerequisites before the first call

### 1. Explicit user approval of the spend ceiling — **BLOCKING**

> EMP-001: maximum **USD 10.00** / approximately **₹954** consumed API spend, excluding taxes,
> **no retries**, and **no account pre-funding above that ceiling**.

Nothing may infer this from "continue", from existing credits, or from an account balance. The
guard refuses a ceiling above USD 10.00, a different tranche id, a non-boolean `authorised`, and
any non-zero `retries_authorised`.

### 2. Runtime secrets and accounts — **BLOCKING**

`OPENAI_API_KEY` and `GOOGLE_API_KEY` in the execution environment, plus a funded surface for the
fal routes. If any provider demands a minimum deposit above the approved ceiling, **stop and
return** rather than funding it.

### 3. Exact provider/model snapshot pinning at execution — **BLOCKING**

`config.yaml` carries aliases (`gpt-5.4-mini`, `gemini-3.5-flash-lite`) and requires a snapshot or
exact version at execution; a judge refuses to exist without a `resolved_version`. **This branch
makes no claim about current provider availability or pricing** — the planning evidence in the
EMP-001 planning artifacts stands until a real run pins the version.

`providers.HttpTransport` is the live dispatch path and has **never been run against a provider**.
Treat it as untested until the first authorised call proves it.

### 4. Human perceptibility review of the Latin pack — **zero-spend, outstanding**

`text_qualification/perceptibility-review.csv` is emitted **unfilled** — 96 rows, every verdict
column blank. It was not performed and was deliberately not fabricated.

The **mechanical** half is done: all 48 mismatches differ after NFC *and* in their decoded RGBA8
raster. That proves a difference is **on the page**. It does not prove a person reading a
commercial surface would notice it, and the two are not the same claim.

A reviewer must answer, per item: `visible_difference` and `usable_surface`. If any item is
rejected, correct the base list in `build_latin_pack.py` and rebuild the **whole** manifest before
re-freezing the fingerprint — never patch a reviewed row in place.

This gates the **Latin** leg of qualification only. The Devanagari leg already carries a completed
human validation. Whether to run Q2a before this review closes is a Controller decision; the code
does not assume either way.

### 5. Materialising the Devanagari validated view at execution — **zero-spend, mechanical**

It is a gitignored build product. Rebuild it with `--out-dir` **outside** the battery; the runner
fails closed if the rebuilt `items.jsonl` does not match the frozen `battery_identity` SHA. The
rebuild takes about 30 seconds and costs nothing. Commands are in the README.

---

## Confirmation

- External provider/model/evaluator calls made by EVAL-012: **0**
- External spend: **USD 0 / INR 0**
- No terms accepted, no account funded, no API credit consumed
- Capability Registry empirical rows: **0**, unchanged
- Scientific roster, frozen contracts, Devanagari battery and V1 baselines: **unchanged**
- Branch pushed, **not merged**

## Is the repository ready for explicit EMP-001 spend approval?

**Yes.** The blocking items are all external to the code — approval, secrets, version pinning —
plus one outstanding zero-spend human review that gates only the Latin leg. No implementation
defect stands between this branch and a first authorised call.
