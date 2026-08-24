# V0 language composition — decision record

**Task:** EVAL-003 · **Status: DECIDED 24 Aug 2026 — retained as the record of the decision.**

> ### Controller decision
> **The primary V0 pack is Hindi-focused.** Shared photographs are admitted **once**; only
> Hindi-labelled items are selected. Built and committed: **54 Hindi from 173 eligible**, 54 distinct
> hashes, configuration `--overlap-policy admit-once --language-filter hindi --target-n 54`.
>
> This is **Option B**, narrowed to Hindi only. The **Marathi stress subset (Option C) is deferred,
> not rejected** — it would need Marathi-competent readers and a separately reported result, and is
> not part of the primary V0 human spend.
>
> The options below are retained as the reasoning that led here.

---

## The problem, in one line

**The pool the pipeline currently produces contains no Hindi at all** — 53 Marathi and 1 unlabelled
of 54 — and that is a structural consequence of the deduplication rule, not a sampling accident.

## Why it happens

| Language label | Labelled records | How many sit in the cross-dataset overlap |
|---|---:|---:|
| hindi | 173 | **173 — all of them (100%)** |
| marathi | 202 | 0 |
| IIIT-ILST (script-labelled, no language) | 176 | 173 |

**The smaller dataset's Devanagari folder is the larger dataset's Hindi folder.** So the rule
"exclude every file that appears in both datasets" removes **every Hindi-labelled photograph**,
leaving a pool that is entirely Marathi.

Deduplication and Hindi coverage are in direct conflict in this corpus. That was not visible until
the material was actually inspected.

## Why it matters — script-general vs Hindi-specific reading

These are different tests, and the difference is not academic:

**Script-general Devanagari reading** — can the checker read the *letterforms*? Marathi is written
in Devanagari, so Marathi signage tests this perfectly well.

**Hindi-specific reading** — can the checker read *Hindi*? Different vocabulary, some different
conventions, and a different prior in the model.

**The failure mode we exist to catch is a language-prior failure.** A vision-language model does not
read letter by letter; it reads toward the plausible *word*. That is precisely why one checker
reported six visibly misspelled Hindi signs as correct — its Hindi prior overwrote what was drawn.

A model's prior over Hindi is generally much stronger than over Marathi. So a Marathi-only pool can
plausibly **under-detect the exact defect we care about**: with a weak prior the model has less to
auto-correct toward, transcribes more literally, and looks better than it would on Hindi.

Two further points: **our production failure is Hindi** (`सुबह की पहली चाय` rendered as `सुवह...`),
and **the checker prompt itself says "Devanagari (Hindi) text"**. Calibrating that prompt on
material containing no Hindi is a validity gap, not a rounding error.

⚠️ **The size of that effect is not measured.** That a Hindi prior is stronger than a Marathi one is
a reasonable expectation, not something this project has evidence for. It is a reason to ensure
coverage, not a finding.

## Options

### Option A — exclude all overlaps  ❌ **not adopted**
- **Pool:** 202 eligible → 54 selected. 53 Marathi, 1 unlabelled. **0 Hindi.**
- Faithful to EVAL-003 as originally written.
- Calibrates **script-general Devanagari reading only.** Any claim about Hindi would be unsupported.
- *This is the superseded pre-finalization configuration. Do not rebuild the pack this way.*

### Option B — admit each shared photograph once  ✅ **ADOPTED (narrowed to Hindi only)**
Admit a photograph that appears in both datasets **exactly once**, attributed to the first source in
fixed order.

- **Pool:** 375 eligible → 54 selected. **19 Hindi, 35 Marathi** (measured, not estimated).
- **Independence is preserved:** one photograph is still one item, verified — 54 items, 54 distinct
  file hashes. The dedup rule exists to stop one photograph being counted twice, and admitting it
  once does not do that.
- **What is genuinely lost:** these are the photographs whose two datasets *disagree* about the
  transcription. But under this protocol the reference comes from our own readers, not from the
  source label, so a conflicting source annotation costs us nothing — and arguably flags a
  usefully hard item.
- Implemented as `--overlap-policy admit-once`. **This is what the committed V0 pack uses**,
  together with `--language-filter hindi`. The script's bare default remains `exclude` as generic
  machinery — that default is *not* the V0 configuration.

### Option C — mixed composition with a stress subset  ⏸️ **deferred, not rejected**
Option B's pool, explicitly partitioned: a Hindi core reported as the primary result, and Marathi
retained as a **script-general / out-of-language stress subset** reported separately.

- Tests the thing the prompt claims to test, while keeping the ability to notice a checker that
  handles Devanagari letterforms but collapses outside Hindi.
- Costs nothing extra — the same 54 crops, scored in two reported groups.
- Needs a target Hindi/Marathi split from the Controller. A roughly 2:1 Hindi:Marathi split would
  give ~36 Hindi and ~18 Marathi within the same 54-item budget.

## Recommendation as it stood *(superseded by the decision at the top of this file)*

> ⚠️ **Historical.** The text below was the recommendation put to the Controller before the decision
> was taken. **The language split is no longer open.** It is retained to show the reasoning, not to
> invite a choice.

The recommendation was **Option C, built on Option B's admit-once policy**.

**What was actually decided:** Option B's admit-once policy, **narrowed to Hindi only** — 54 Hindi of
173 eligible. Option C's Marathi stress subset is **deferred, not rejected**; it is not part of the
primary V0 human spend and would require Marathi-competent readers and a separately reported
result.

## Not done, deliberately

**No new data was acquired**, and none was needed: the Hindi material was already in the repository
and had been excluded by rule, not missing. Nothing about the battery, ladders, thresholds,
observation units or Registry architecture was affected by this decision.
