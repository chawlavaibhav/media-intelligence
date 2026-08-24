# Checker input/output contract

**Status: PROPOSED. No checker has been run.**

---

## What a checker is asked

For each item the checker receives **one image** and **one target string**, and must answer one
question:

> Does the Devanagari text visible in this image match the target string **exactly**, character
> for character?

Nothing else is asked. Not what the text says, not whether it is a real word, not whether it is
well spelled. **Exactness against a stated target** — because that is the production question: we
asked a generator for a specific string and must know whether we got it.

---

## Two checker shapes, both supported

The contract deliberately admits both, because they fail differently and we do not yet know which
is better.

### Shape 1 — `transcribe` (indirect)
The checker transcribes what it sees; **we** compare against the target.

- Prompt instructs transcription only, never confirmation. The existing `check-vlm.mjs` prompt
  already does this: *"Do NOT correct spelling. Do NOT guess what it was meant to say."*
- The comparison is deterministic and ours, so the checker cannot fudge it.
- **This shape is preferred**, because it removes the model's opportunity to answer "yes" without
  committing to what it actually saw. It also yields a diagnosis, not just a verdict.

### Shape 2 — `verdict` (direct)
The checker is shown the target and answers match / mismatch.

- Closer to how a checker would be wired in production.
- Structurally more exposed to autocorrection: the plausible answer is visible in the prompt.
- Measured *because* it is more exposed. If shape 2 shows a materially higher false-pass rate than
  shape 1 on the same items, that is a finding about prompt design, not about the model.

**The same items are run through both shapes.** Results are reported separately and never pooled.

---

## Input record

One JSONL line per item. Produced by `build_items.py`; consumed unchanged.

```json
{
  "item_id": "dx-0007",
  "image_file": "images/img-0005.png",
  "image_sha256": "…",
  "target_string": "तोड़ना",
  "checker_shape": "transcribe | verdict"
}
```

**What the checker must never receive:** `rendered_string`, `expected_verdict`, `failure_class`,
`direction`, `plausibility`, `edit_detail`, or any other item's result. The build manifest contains
all of these; the checker input is a strict projection that omits them.

A `--verify-blind` style check is required before any run: the checker input file must contain no
field that reveals the answer. This is the same discipline EVAL-003 applied to its reader pack, for
the same reason — an evaluator that can infer the answer is not being evaluated.

## Output record

```json
{
  "item_id": "dx-0007",
  "checker_id": "…", "checker_version": "…", "checker_shape": "transcribe",
  "raw_response": "…",
  "transcription": "…",          // shape 1 only
  "verdict": "match | mismatch | refused | error",
  "latency_ms": 0, "cost_units": 0.0,
  "run_id": "…", "repeat_index": 0
}
```

- **`refused` is a distinct outcome**, never silently folded into either verdict. A checker that
  declines is not the same as one that gets it wrong, and treating a refusal as a pass would be the
  most dangerous rounding in the whole design.
- `raw_response` is retained verbatim so a verdict can be re-derived if parsing is later found
  wrong.

## Deriving the verdict in `transcribe` shape

```
verdict = "match" if NFC(transcription) == NFC(target_string) else "mismatch"
```

NFC and nothing else. **No fuzzy matching, no edit-distance threshold, no stripping of diacritics.**
The whole point is exactness; a tolerant comparison would rebuild the very autocorrection we are
trying to detect, only in our own code this time.

NFC is chosen deliberately, not for tidiness: it collapses precomposed nukta letters onto their
decomposed equivalents, which is also what the renderer draws. Comparing in NFC therefore agrees
with the pixels. Any other normalisation would disagree with them.

Character edit distance is recorded **alongside** as a diagnostic. It never affects the verdict.

---

## Run discipline

| Rule | Why |
|---|---|
| Items presented in a fixed shuffled order, recorded | order effects are removed but reproducible |
| No item's result visible while another is judged | each item is independent |
| Repeats on the leading checker (≥3 full passes) | a checker that is right on average but unstable per item is not usable as a gate |
| Checker id **and version** recorded | a changed version is a different instrument and needs re-qualification |
| Temperature/sampling fixed and recorded | otherwise repeats measure sampling noise, not the checker |
| Prompt frozen before the run | changing a prompt after seeing results and reporting it as the same run is an EXPERIMENT MUTATION stop |

---

## What is deliberately not in the contract

- **No confidence score.** We are not equipped to calibrate one, and an uncalibrated confidence
  invites exactly the over-trust this battery exists to prevent.
- **No partial credit.** The production question is binary: did we get the string we asked for.
- **No "close enough".** See above.
