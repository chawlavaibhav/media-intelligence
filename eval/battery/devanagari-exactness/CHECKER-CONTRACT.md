# Checker input/output contract

**Status: PROPOSED, revised after Controller review. No checker has been run.**

---

## What a checker is asked

For each item the checker must answer one question:

> Does the Devanagari text visible in this image match the target string **exactly**?

Nothing else is asked. Not what the text says, not whether it is a real word, not whether it is
well spelled. **Exactness against a stated target** — because that is the production question: we
asked a generator for a specific string and must know whether we got it.

"Exactly" here means **canonically exact**, not codepoint-identical. Two encodings of the same
nukta letter draw the same pixels, so treating them as different would penalise a checker for
correctly reporting what it saw. See *Comparison predicate* below.

---

## Two checker shapes — and they receive DIFFERENT inputs

This is the part an earlier draft got wrong. It said every checker receives "one image and one
target string", while also describing shape 1 as an *indirect* test in which the model commits to
what it sees and our code does the comparison. Both cannot be true. Showing the model the target
is exactly the autocorrection pressure the indirect shape exists to remove.

### Shape 1 — `transcribe` (blind)

| | |
|---|---|
| **Checker-visible input** | the image + a frozen transcription-only prompt |
| **Target** | **evaluator-side only — the model never sees it** |
| **Model returns** | a transcription of what it believes is drawn |
| **Verdict** | derived by us: `match` iff `NFC(transcription) == NFC(target)` |

The model has no opportunity to answer "yes" without committing to what it actually saw. It also
yields a *diagnosis* — which characters it got wrong — not merely a verdict.

### Shape 2 — `verdict` (target visible)

| | |
|---|---|
| **Checker-visible input** | the image + the target string + a frozen exact-match prompt |
| **Model returns** | `match` / `mismatch` / `refused` / `error` |

Closer to how a checker would be wired in production, and structurally more exposed to
autocorrection: the plausible answer is sitting in the prompt.

### Why both

The comparison between them is a measurement in its own right. If shape 2 shows a materially
higher false-pass rate than shape 1 on the same items, that is a finding about **prompt design** —
showing a model the answer you hope for invites it to agree — not a verdict on the model.

**The same items are run through both shapes. Results are reported separately and never pooled.**

---

## The build produces three files, and only two of them go to a checker

`build_items.py` writes, next to the items manifest:

| File | Goes to a checker? | Contents |
|---|---|---|
| `checker-input-transcribe.jsonl` | **yes**, shape 1 | item id, image, image **file** hash, the frozen prompt. **No target.** |
| `checker-input-verdict.jsonl` | **yes**, shape 2 | the above **plus** the target, and a prompt carrying it |
| `scoring-key.jsonl` | **never** | target, rendered string, expected verdict, direction, plausibility, class, base word, hard-opportunity flag |

`items.jsonl` is the full build manifest and is likewise **never** handed to a checker.

### Payload shapes

```json
// checker-input-transcribe.jsonl  — shape 1
{"item_id":"dx-0007","image_file":"images/img-0005.png","image_file_sha256":"…",
 "checker_shape":"transcribe","prompt":"Transcribe the text visible in this image…"}

// checker-input-verdict.jsonl  — shape 2
{"item_id":"dx-0007","image_file":"images/img-0005.png","image_file_sha256":"…",
 "checker_shape":"verdict","target_string":"तोड़ना","prompt":"…TARGET: तोड़ना…"}
```

---

## The blind check is mechanical, and it runs before any call

`checker_input.verify_blind(payloads, shape)` returns a list of violations. **An empty list is the
only acceptable result before a run.** `write_checker_inputs()` calls it and refuses to write a
file that fails, so a leaking file cannot be produced and then used by mistake.

What it enforces:

1. **An allow-list of fields, not a deny-list.** A deny-list silently ships any field added later;
   an allow-list fails closed.
2. **No ground-truth metadata in either shape** — `rendered_string`, `expected_verdict`,
   `failure_class`, `failure_group`, `direction`, `plausibility`, `edit_detail`, `base_word`,
   `rendered_shape`, `target_shape`, the pixel fingerprints, `hard_opportunity`, `render_spec`.
3. **For `transcribe`: no target, and no Devanagari character anywhere in the payload.** The
   second rule is the one that catches a leak arriving through a field nobody anticipated —
   including a target appended to the prompt. Every target in this battery is Devanagari, so its
   presence in a blind payload is decisive regardless of what the field is called.
4. **For `verdict`: the target IS present, and the prompt actually carries it.** A verdict item
   whose prompt lost its target would be a blind item mislabelled, and would be scored as though
   the model had been shown something it never saw.

Regression tests fail if a target is injected into a transcribe payload, either as a field or
smuggled into the prompt text. This is the same discipline EVAL-003 applied to its reader pack,
for the same reason: an evaluator that can infer the answer is not being evaluated.

---

## Frozen prompts

Both prompts are constants in `checker_input.py` and their SHA-256 is recorded with any run.
Changing a prompt after seeing results and reporting it as the same run is an **EXPERIMENT
MUTATION** stop under `shared/AUTONOMY-POLICY.md`.

**Shape 1 (`PROMPT_TRANSCRIBE`)** instructs transcription only and contains no target and no
Devanagari:

> Transcribe the text visible in this image, exactly as it appears. Output only the transcription
> and nothing else. Do NOT correct spelling. Do NOT guess what it was meant to say. If a character
> looks wrong or unusual, transcribe what is actually drawn.

**Shape 2 (`PROMPT_VERDICT`)** carries the target and asks for one word:

> Does the text visible in this image match the following target string exactly, character for
> character? TARGET: `{target}` Answer with exactly one word: MATCH or MISMATCH. Do NOT correct
> spelling. Do NOT allow for a plausible intended reading. Judge only what is actually drawn
> against the target as given.

---

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
  declines is not the same as one that gets it wrong, and treating a refusal as a pass would be
  the most dangerous rounding in the whole design.
- `raw_response` is retained verbatim so a verdict can be re-derived if parsing is later found
  wrong.

---

## Comparison predicate, and the three rules that are NOT the same rule

An earlier version had a single function called `nfc()` that also stripped whitespace, while the
contract said "NFC and nothing else". Those are different operations, and whitespace handling is a
real decision that should not hide inside a function named after a normalisation form. There are
now three separately named, separately tested rules:

| Rule | What it does | Where it applies |
|---|---|---|
| `nfc(s)` | Unicode NFC. **Nothing else.** | inside the comparison predicate |
| `strip_outer_whitespace(s)` | removes leading/trailing whitespace, never internal | **ingest** (annotation files) and **response parsing** (raw model reply) |
| `canonical_equal(a, b)` | `nfc(a) == nfc(b)` | the verdict in shape 1 |

Deriving the shape-1 verdict, precisely:

```
transcription = strip_outer_whitespace(raw_response)     # transport rule, parsing step
verdict       = "match" if canonical_equal(transcription, target) else "mismatch"
```

**Why whitespace is stripped at parsing and not at comparison.** A leading newline in a chat reply
belongs to the transport, not to what the model claims it saw; scoring it as a mismatch would
inflate false fails for a reason that has nothing to do with reading Devanagari. But the stripping
is a named step in the pipeline, visible and testable, rather than a hidden effect of the
comparison. **Internal** whitespace is never touched: `सुबह की` and `सुबहकी` are different strings
and compare unequal.

**Why NFC and not raw codepoints.** NFC collapses the precomposed nukta letters (U+0958..U+095F)
onto their decomposed equivalents — which is what the renderer draws. Measured on the pinned font:
`क़` as U+0958 and as U+0915 U+093C produce **byte-identical PNGs**. Comparing in NFC therefore
agrees with the pixels. Raw-codepoint comparison would mark a checker wrong for correctly
describing an image.

**Everything looser is forbidden.** No fuzzy matching, no edit-distance threshold, no stripping of
diacritics, no "close enough". A tolerant comparison would rebuild the very autocorrection we are
trying to detect, only in our own code this time.

Character edit distance is recorded **alongside** as a diagnostic. It never affects the verdict.

---

## Run discipline

| Rule | Why |
|---|---|
| `verify_blind` returns no violations before the first call | a leaked target invalidates shape 1 entirely, and it cannot be detected afterwards from the responses |
| Items presented in a fixed shuffled order, recorded | order effects are removed but reproducible |
| No item's result visible while another is judged | prevents context leakage between items — one response must not condition the next. **This is execution isolation, not statistical independence:** it stops the checker from seeing the other items, it does not make its errors uncorrelated across them. See `METRICS-AND-QUALIFICATION.md`. |
| **Every checker given a qualification status completes the full repeat requirement** | see `METRICS-AND-QUALIFICATION.md`; a checker that was not repeated is not qualified because another one was |
| Checker id **and version** recorded | a changed version is a different instrument and needs re-qualification |
| Temperature/sampling fixed and recorded | otherwise repeats measure sampling noise, not the checker |
| Prompt frozen before the run, sha256 recorded | changing a prompt after seeing results and reporting it as the same run is an EXPERIMENT MUTATION stop |
| Font file sha256, face index, renderer and shaper versions recorded | a different font is a different experiment; see `README.md` §Reproducing |
| `image_file_sha256` recorded per response | proves the checker read the exact file we shipped. It is **artifact** identity — the visibility gate uses the decoded-pixel fingerprint instead, and the two must not be confused |

---

## What is deliberately not in the contract

- **No confidence score.** We are not equipped to calibrate one, and an uncalibrated confidence
  invites exactly the over-trust this battery exists to prevent.
- **No partial credit.** The production question is binary: did we get the string we asked for.
- **No "close enough".** See above.
