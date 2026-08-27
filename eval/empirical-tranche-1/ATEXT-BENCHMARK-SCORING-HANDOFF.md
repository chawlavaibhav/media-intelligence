# A-TEXT Benchmark Scoring Handoff — prepared by EVAL-029, not executed

**Status:** PREPARED AND BLOCKED ON EVAL-024. No A-TEXT artifact was scored, because none exists.

## Why nothing was scored

EVAL-029 was authorised to score sealed A-TEXT artifacts *if* they were already available on a
pushed branch. They are not. This was established by inspecting GitHub, not by recalling chat:

- branch `origin/work/eval-024-parallel-atext-generation-only` exists, one commit ahead of `main`
  (`e4e4d39`);
- its diff against `main` contains **code only** — `atex/generate_atex.py` and its tests;
- it carries **no sealed manifest, no generated images and no run outputs**;
- `main`'s newest commit is *"controller: record EVAL-024 cleanup gate before live generation"*;
- `CONTROL-STATE.md` records that EVAL-024 returned with **zero live spend because `FAL_KEY` was
  unavailable**, and that a cleanup/sync pass is required before generation.

So EVAL-024 built the machine and never ran it. Per the task, the correct action is to prepare
this handoff and stop — not to wait, and not to generate anything.

## The evaluator that is ready

Cloud Vision `TEXT_DETECTION`, no language hints, is **benchmark-qualified for both scripts** under
`benchmark_text_ocr_v1`. It is **not** strict-exactness qualified and never will be under the
strict contract, which it failed.

| | Devanagari | Latin |
|---|---|---|
| Source | recomputed from stored EVAL-022 observations | live EVAL-029 screen |
| False-pass rate | 0.1250 | 0.1042 |
| Match false-fail rate | 0.0208 | 0.0000 |
| Repeat consistency | 1.0 | 1.0 |
| Failure rate | 0.0 | 0.0 |
| Complete | 288/288 | 288/288 |
| `benchmark_qualified` | true | true |
| `strict_exactness_qualified` | **false** | **false** |

**What the false-pass rate means in practice.** Roughly one adversarially corrupted string in eight
(Devanagari) or ten (Latin) is read back as if it were correct. So if a generator paints wrong text,
this evaluator will usually notice but not always. It is good enough to say *generator A produces
better text than generator B*; it is **not** good enough to say *this particular image is correct*.

**What the false-fail rate means in practice.** Latin is 0.0 and Devanagari 0.0208 — the evaluator
almost never rejects text that is actually right. This matters more than it sounds: a benchmark that
wrongly penalises good generators would rank them wrongly. This one does not.

## What the scoring run must do when EVAL-024 returns

1. **Verify before scoring.** Recompute the SHA-256 of every artifact and match it against the
   sealed EVAL-024 manifest. Any mismatch refuses that artifact — a file that is not the one that
   was sealed is not evidence about the generator that produced it.
2. **Never regenerate.** The scorer must not import, construct or reach a generator. If an artifact
   is missing, the correct output is "missing", not a replacement image.
3. **Never substitute** an artifact, alter a prompt, or change a target string.
4. Evaluator: Cloud Vision `TEXT_DETECTION`, **no** `languageHints`, target never sent, retries `0`.
5. Comparison: the frozen NFC + outer-whitespace rule. Unchanged, and not to be loosened.
6. Budget: the existing persistent EMP-001 ledger and `qualification` stage.
7. **No human review.** It is not part of this evaluator contract.

## What every reported generator number must carry

A bare score would let a reader treat a benchmark signal as a guarantee. Each result must ship with:

```
evaluator_contract_id            benchmark_text_ocr_v1
evaluator_contract_sha256        de25e43779071bf1d6e080711e9b22f75fbfc82ae7b824f18779c33d48359775
false_pass_rate_devanagari       0.1250
false_pass_rate_latin            0.1042
false_fail_rate_devanagari       0.0208
false_fail_rate_latin            0.0000
repeat_consistency               1.0 (both scripts)
script_coverage                  [devanagari, latin]
benchmark_qualified              true
strict_exactness_qualified       false
measurement_has_known_error      true
```

## What this is not

A-TEXT scored this way is a **benchmark measurement with declared error**, not a certification that
any generated image contains exactly correct text. Nothing here licenses a Registry row; Registry
population remains separately authorised and the Registry is still empty.
