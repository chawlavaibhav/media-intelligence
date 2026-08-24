# Finding 01 — Can we tell right from wrong automatically?

**Date:** 16 Aug 2026 · **Cost:** ~₹25 · **Time:** one sitting

The whole product rests on one assumption: a machine can look at an output and say pass or fail
without a human. This tests that assumption on the hardest case — Devanagari text in a generated image.

## Material

14 samples, all real model output, all already paid for (₹0 to gather):

| Source | n | Ground truth |
|---|---|---|
| `aight_chai-composite.mp4` frames — text placed by code | 6 | GOOD — सुबह की पहली चाय |
| `wan_chai-sign.mp4` frames — text painted by the model | 6 | BROKEN — सुवह की पहली चाथ (ब→व, य→थ) |
| `nano_chai-headline.png` | 1 | GOOD |
| `seedream_chai-headline.png` | 1 | BROKEN — gibberish |

Checkers were asked to **transcribe** ("do not correct spelling, do not guess what it was meant to
say"), never to confirm — so an agreeable model can't simply say yes.

## Result

| Checker | Correct verdicts | False passes | Cost/check |
|---|---|---|---|
| **qwen3-vl-235b** | **14 / 14** | 0 | ~₹0.90 |
| claude-sonnet-4.5 | 7 / 13 | **6** | ~₹0.90 |
| tesseract (hin) | 0 / 14 — unreadable output | n/a | free |

## What it means

**1. The assumption holds — with one specific checker.** Qwen3-VL caught every broken frame and
passed every good one, including the six frames where the misspelling is a single character.

**2. The wrong checker is worse than no checker.** Claude Sonnet 4.5 reported "सुबह की पहली चाय —
exact match" for all six frames that visibly read सुवह की पहली चाथ. Built on that checker, the
pipeline would have shipped the broken sign to a customer *with a passing grade attached*.

**3. The failure mode is predictable and points one way.** Language models auto-correct toward the
plausible word — that is what they are for. As spelling verifiers this produces **false passes**
specifically, which is precisely the silent failure the product exists to eliminate. Any checker must
be measured for this before it is trusted, and re-measured when its version changes.

**4. Classical OCR is not an option.** Matches the published research on Devanagari OCR.

**5. Even the good checker under-reports.** Qwen caught सुबह→सुवह but silently corrected चाथ→चाय.
Verdict right, diagnosis incomplete. Fine for gating, not yet trustworthy for explaining *what* broke.

## Limits of this result

- 14 samples but only **4 independent sources**; the 12 frames are highly correlated.
- Ground truth is one reading plus the 24 Jul record — they agree, but **neither reader's first
  language is Hindi. A Hindi reader should confirm the labels before this is quoted.**
- One run per sample; checker consistency across repeat runs not measured.
- One Claude sample errored out (13 not 14).

## Incidental finding

The Wan misspelling **drifts across the clip** — frames 1–4 read सुवह की, frames 5–6 read सुवह के.
The error isn't even stable within one five-second video.

## Next

- Hindi reader confirms the 14 labels.
- Repeat runs on Qwen to measure checker consistency.
- Widen to fresh model output (~₹70 for 20 new generations) so n of independent cases rises.
