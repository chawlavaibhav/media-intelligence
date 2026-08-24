# M1b — Devanagari generation-test item set: structure and coverage design

**Task:** EVAL-002 · **Date:** 24 Aug 2026
**Status: DESIGN ONLY, for Controller review. No items were created. No Hindi phrase was authored
or selected. No linguistic judgement was made.**

Populating or freezing this set requires Controller approval (EVAL-002 human-approval triggers).

---

## 1 · What M1b is, and the distinction that makes it necessary

"M1b" is shorthand for **the prompts we will give image and video generators to see whether they can
draw Hindi text correctly.**

It must not be confused with **M1a**, which is a different thing for a different purpose:

| | What it contains | What it tests | Where it comes from |
|---|---|---|---|
| **M1a** | existing Devanagari images that already have human transcriptions | whether **our checker can read** Hindi | published recognition datasets — reusable if Resources clears them |
| **M1b** | prompt → target-string pairs | whether **a generator can draw** Hindi | must be built for V0 — no suitable public set identified so far |

**Reading and drawing are different capabilities.** Public benchmarks for reading Devanagari out of
a photo are plentiful. **No suitable public benchmark for generative Devanagari rendering has been
identified in our search so far**, so our V0 item set still needs to be built.

⚠️ **Wording corrected 24 Aug 2026 at Controller direction.** An earlier draft said such a benchmark
"does not exist" and that "nothing public contains this." **That is stronger than the evidence
supports.** What we have is a search that did not find one — a bounded review conducted during
EVAL-001, not an exhaustive survey of everything published. Absence of evidence in our search is not
evidence of absence, and the practical conclusion is unchanged either way: **we still have to build
the set.** If a suitable public set is later identified — including anything Resources surfaces
under RES-002 — this design should be revisited before items are built, not after.

**They cannot substitute for each other.** Using recognition images as capability items would
measure the wrong thing entirely — it would tell us about our checker while appearing to tell us
about the model.

---

## 2 · What one item looks like

Fields, with plain-English meaning:

| Field | Meaning |
|---|---|
| `item_id` | stable identifier |
| `dimension` | `exact_text_devanagari`, or `text_stability_across_frames` for clip items |
| `difficulty_level` | 1–3 in V0 (level 4 defined but not run) |
| `target_string` | **exactly** what must appear in the image |
| `target_string_source` | where the phrase came from — see §5. Never blank |
| `script` | `devanagari` |
| `prompt_template` | the instruction to the generator, holding scene wording constant so the only thing varying is the string and its placement |
| `placement_context` | how the text sits in the scene — see the ladder in §3 |
| `observation_unit` | `frame` for stills; `sequence` for clips |
| `coverage_tags` | which typographic features this item deliberately exercises (§4) |
| `expected_observable` | what a correct result looks like, in words a reviewer can check |
| `latin_control_id` | the matched Latin item — see §6 |
| `native_reader_status` | `pending` until a Hindi first-language reader verifies it (§7) |
| `conditions` | resolution, aspect ratio, word count, character count |

**Nothing in an item may be a judgement about Hindi.** The item records a string, its source, and
the features it is intended to cover. Whether the string is correct, natural or well-formed is a
question only a native reader can answer, and that step is explicitly outside EVAL-002.

---

## 3 · Difficulty ladder — inherited, not invented

The approved battery already fixes this ladder and the rule behind it: **each level adds exactly one
named, independently observable stressor**, so a failure at level 3 isolates the specific thing the
model cannot do. This design does not change it.

| Level | Added stressor | Placement context |
|---|---|---|
| 1 | none — baseline | single word, plain rendering, high contrast |
| 2 | multi-word line | 3–5 word phrase on one line |
| 3 | text on an in-scene surface | same phrase on a signboard or packaging inside the scene |
| 4 *(defined, not run in V0)* | perspective or occlusion | signboard angled or partly hidden |

For clip items under `text_stability_across_frames`, the approved ladder is: static camera with a
Latin string (level 1), the same with a Devanagari string (level 2), then camera or subject motion
(level 3).

---

## 4 · Coverage — what the set must deliberately exercise

These categories are carried over from EVAL-001's justification. **Coverage means the set
deliberately includes items tagged for each category. It does not mean the category is exhaustively
or correctly covered — only a native reader can establish that.**

| Category | Plain-English meaning | Why it is on the list |
|---|---|---|
| **Conjuncts** (joined letter forms) | two or more consonants fused into a single combined glyph | the most structurally complex thing Devanagari asks a generator to draw; a plausible failure point |
| **Vowel marks (matras)** | marks attached above, below, before or after a consonant to change its vowel | they attach in several directions, so a generator can place one on the wrong side and still produce something that looks like Devanagari |
| **Nukta** | a dot below a consonant that changes which sound it is | a single small mark that changes meaning — exactly the kind of detail a checker that "reads for sense" would silently correct |
| **Observed confusion families** | the specific substitutions we have already watched happen: **ब→व** and **य→थ** | these are ours, from real recorded failures, and they are single-character errors — the hardest case any checker has to catch |
| **String length** | short vs longer strings within the approved word counts | distinguishes "cannot draw the script" from "loses coherence as the string grows" |
| **Visual context** | plain rendering vs busier in-scene surfaces | already the level 1→3 axis; tagged so failures can be attributed to context rather than script |

**What is deliberately NOT claimed.** This is not a linguistic coverage model of Devanagari. It has
no coverage of regional orthographic variation, numerals, punctuation conventions, or
typography-specific behaviour across fonts. **Do not describe this set as representative of Hindi.**
It is a set of deliberately chosen stress cases.

---

## 5 · Where the strings come from — sourced, not authored

The Controller established that we do **not** need to author every Hindi phrase from scratch.
Ordinary Hindi text is not scarce, and sourcing it reduces the work to selection plus verification.

- `target_string_source` records, per item, whether the phrase was **sourced** from an existing
  permissible Hindi text resource (with that resource named) or **constructed** to force a specific
  typographic feature that sourcing did not supply.
- **Any external text source is subject to Resources clearing it** for bounded internal evaluation
  under the current Resources policy, exactly as M1a is. **Eval performs no rights assessment.**
- Where a coverage category cannot be filled from sourced text, the item is marked
  `constructed_pending_native_review` and carries **no presumption of correctness** until reviewed.

**What must be constructed rather than sourced is the *coverage*, not the language:** which features
each item is chosen to exercise, and how items ladder in difficulty.

---

## 6 · Latin control items — how the matching works

Every Devanagari item has a matched Latin partner under `exact_text_latin`.

**Why.** Without it a Hindi failure rate cannot be interpreted. If a model renders our Hindi items
badly, there are two possible explanations — the model is bad at rendering text in general, or it is
bad at *Devanagari specifically* — and those lead to opposite routing decisions. If it is uniformly
bad at text, we composite the text separately for every language. If it is Devanagari-specific, the
model is still usable for Latin copy. **Only the difference between the two scores separates them.**

Matching rules:

- same difficulty level, same placement context, same prompt template;
- same word count, and character count as close as the two scripts permit;
- identical scene wording apart from the string itself;
- linked by `latin_control_id` in both directions.

**Limit, stated honestly:** Devanagari and Latin cannot be matched on "difficulty" in any principled
way — they are different writing systems and a four-word phrase is not equally hard in both. The
control supports the comparison *general text vs this script*. It does **not** support a claim that
the two item sets are of equal difficulty.

---

## 7 · What a Hindi first-language reader must check later

**None of this was done in EVAL-002.** Listing it so the requirement is visible and budgeted.

1. **Every `target_string` is well-formed and means something ordinary** — not a plausible-looking
   sequence that is actually malformed.
2. **The reference rendering is correct** — the specific letterforms a correct result must show.
3. **Coverage tags are accurate** — that an item tagged as containing a conjunct actually does.
4. **The confusion-family items genuinely isolate that confusion** and not some other difference.
5. **Sourced strings are appropriate** — no register, spelling or regional oddity that would make a
   correct generation look wrong or vice versa.

Until step 1 is complete, **no item may be used to score a model**, because the target would not be
established ground truth. The approved calibration plan estimates 2–4 hours of native-reader time
across this and the checker calibration; that time is **not budgeted** and is a Controller decision.

---

## 8 · Size, and why no number is proposed here

The approved battery works to 12 independent items per dimension per level with 2 repeats. Applying
that to three levels of `exact_text_devanagari` implies roughly 36 Devanagari items plus 36 matched
Latin controls, before clip items.

**That is arithmetic from the approved design, not a proposal to build that many.** Actual size
depends on the model roster and the human-time budget, both of which are unapproved.

---

## 9 · What this design does not settle

- **Whether these coverage categories are the right ones.** They are the ones EVAL-001 could justify
  from observed failures and published methodology. No claim of completeness.
- **Whether sourced Hindi text will fill them.** Unknown until someone tries; the fallback is
  constructed items needing more native-reader time.
- **Whether clip items can hold a target string steady enough to be fair.** Video generators may
  fail for reasons unrelated to script; the approved battery separates *correctness* from
  *stability* partly for this reason, but the interaction is untested.
- **Anything about model capability.** Not one item exists, and none has been run.
