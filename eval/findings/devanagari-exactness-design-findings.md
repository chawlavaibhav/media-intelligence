# Devanagari exactness battery — design findings

**Date:** 25 Aug 2026 · **Task: EVAL-005** *(Controller-assigned; design hardening only)*
**API/model spend:** ₹0 · **Human specialist time:** 0 h · **Generators run:** 0 · **Registry entries:** 0

What was built, what was learned building it, what the Controller review corrected, and what
remains uncertain.

**Revision note.** §§1–4 and §8 carry forward from the first design pass and still hold. §5 and §7
were **materially wrong** in the first pass and are corrected here. §6 and §9–10 are updated.

---

## 1 · The reframing that makes this tractable

EVAL-004 was stopped because reading photographed signage is a weak proxy for the failure that
matters. The redesign changes the question:

> **Does the evaluator report a match when the visible text differs from the requested target?**

And it changes where ground truth comes from. Instead of *finding* images and trying to establish
what they say, we **construct** them: render a chosen string locally with a pinned font, and what
the image contains is known by construction.

**This dissolves the problem that stopped EVAL-004.** No annotator, no dataset label, no
reader-agreement reference, no adjudication. The human requirement falls from 3.5–4.5 hours across
two readers to **~1.5 hours once**, and none of it establishes ground truth (§6).

---

## 2 · Two different Unicode strings can produce identical pixels — measured

**OBSERVED.** On the pinned font, precomposed क़ (U+0958) and क + nukta (U+0915 U+093C) shape to
the **same glyph sequence** and render to **byte-identical PNGs**:

```
क़  (U+0958)        -> [uni0915093C=0+770]
क + nukta          -> [uni0915093C=0+770]
```

**Why it matters.** An item built from that pair would ask a checker to report a difference that is
not on the page, and mark it wrong for correctly describing what it saw. That measures Unicode
pedantry, not visual faithfulness.

**A related detail that lines up.** NFC collapses the precomposed nukta letters onto their
decomposed forms, which is also what the renderer draws — so comparing in NFC **agrees with the
pixels**. This is why the contract's exactness is *canonical* exactness rather than raw-codepoint
identity, and saying so plainly is one of the review corrections (§5.6).

---

## 3 · Direction decides what is being measured

A mismatch can be built two ways, and they are not the same test:

| Direction | Construction | Autocorrect pressure |
|---|---|---|
| **`corrupt_image`** | render the perturbed string, ask about the **real word** | **high** — malformed text, plausible target; every pull of the prior says "yes" |
| `corrupt_target` | render the real word, ask about the perturbed string | low — clean image, odd target |

**INFERRED:** only the first reproduces the production failure. It is 70% of the mismatch stratum
(37 of 53); the second is retained as a control. They are reported separately, because a good score
on the easy direction would otherwise conceal blindness on the hard one.

---

## 4 · Neither trivial strategy survives

- **50/50 match/mismatch** — "always match" and "always mismatch" both score exactly 50%.
- **Every base word appears in both strata**, so recognising the word does not reveal the answer.
- **32 paired items** — identical pixels, different target, **opposite** expected verdict. A checker
  cannot be right on both by judging the image alone, nor by ignoring it.

---

## 5 · What the Controller review found, and what it changed

Seven fixes were required. Five of them found something the code actually did wrong, not merely
prose that read badly. Each is now pinned by a regression test.

### 5.1 · The blind checker shape was not blind — **contract defect**

**OBSERVED.** The contract said every checker receives "one image and one target string", while
also describing shape 1 (`transcribe`) as an *indirect* test in which the model commits to what it
sees and our code does the comparison. Both cannot be true.

**Why it matters.** Showing the model the target is precisely the autocorrection pressure the
indirect shape exists to remove. Run that way, the two shapes measure the same thing and the
comparison between them — which is a measurement in its own right, about prompt design — evaporates.

**What was done.** `checker_input.py` now produces two different payloads. The transcribe payload
carries the image and a frozen transcription-only prompt, and nothing else. The verdict payload
carries the target, by design. A pre-run check, `verify_blind()`, enforces an **allow-list** (fails
closed on any field added later), rejects every ground-truth field, and — the check that catches a
leak arriving through a field nobody anticipated — rejects **any Devanagari character anywhere in a
transcribe payload**. `write_checker_inputs()` refuses to write a file that fails, so a leaking file
cannot be produced and then used by mistake. The evaluator-side target lives in a separate
`scoring-key.jsonl` that never goes to a checker. Regression tests inject a target as a field and
smuggle one into the prompt text; both are caught.

### 5.2 · Shaping and rendering used different fonts — **reproducibility defect**

**OBSERVED, measured before the fix:**

```
render() with a VALID font_file  -> faffe232d6430ce4…
render() with a BOGUS font_file  -> faffe232d6430ce4…    (identical — the file was ignored)
pango-view with a family name that does not exist -> rendered anyway, no error
```

The validity screen shaped with `hb-shape --font-file=<exact file>`; the rasteriser called
`pango-view --font="<family name>"`, which resolves through fontconfig. `render()` ignored the
pinned file entirely, and a nonexistent family produced a silent fallback rather than an error.

**Why it matters.** Every "this difference is visible" decision was made in one font while the
committed PNG was drawn through whatever another lookup happened to return. On this machine both
landed on Kohinoor, so nothing was actually wrong in the built battery — but nothing guaranteed it,
and on a different machine the two could diverge without any error being raised.

**What was done.** `hb-view` replaces `pango-view`. It is HarfBuzz's own rasteriser, takes a font
**file** rather than a family, and accepts the same `--face-index`, so the shaping behind the
pixels is the shaping we measured. A missing font raises `FontMissing` and stops the build; there
is no fallback face by design. Provenance — font path, **font SHA-256**, face index, `hb-shape` and
`hb-view` versions, point size, margin, colours — is recorded in every `build-summary.json`.

**The font is deliberately not committed.** `/System/Library/Fonts/Kohinoor.ttc` is a proprietary
macOS asset and redistributing it is a licence question we have no basis to answer. Its identity is
pinned by hash instead, so a future run can prove it used the same bytes or discover that it did
not. Documentation that claimed portability has been corrected: the battery is deterministic *for a
given environment*, and that environment is now stated with hashes.

### 5.3 · Visibility was gated on glyphs, not pixels — **logical defect, with a live example**

**OBSERVED.** Different glyph sequences do not imply different pixels:

```
सुबह         -> [uni0938=0+680|uni0941=0+0|uni092C=2+567|uni0939=3+507]
सु‌बह (ZWNJ)  -> [uni0938=0+680|uni0941=0+0|space=2+0|uni092C=3+567|uni0939=4+507]
```

Genuinely different after NFC. **Different glyph sequences** — there is an extra zero-advance glyph.
**Byte-identical PNGs.**

**Why it matters.** The glyph-only gate would have admitted this as a valid mismatch, and then
scored a checker wrong for correctly reporting that the two pictures are the same — the same defect
the nukta screen was built to prevent, arriving through the door that was supposed to prevent it.

**What was done.** The gate is now the final PNG bytes. Rejection reasons are `canonical_equal`,
`raster_identical` and `rendering_error`. Glyph comparison is retained and recorded as a diagnostic,
so disagreements between the two are visible. Screening renders into a process-lifetime scratch
directory that is deleted on exit, so no temporary image reaches the repository.

**Honest note on impact:** on the current 53-word pool the two criteria never disagreed —
1,834 candidates pass, 2 are rejected `canonical_equal`, **0** `raster_identical`. The built
battery would have been the same either way. What changed is that the claim the battery makes is
now the claim it verifies.

### 5.4 · A plausibility hole put broken strings in the hard stratum — **found while fixing 5.3**

**OBSERVED.** Two hard items rendered strings the shaper marks as invalid with a dotted circle
(U+25CC): `इं्लीश` (deleting the first consonant of `इंग्लीश` leaves a virama hanging off an
anusvara) and `ॉम्बे` (from `बॉम्बे`, opening with U+0949 — a vowel sign the rule's list did not
contain).

**Why it matters.** A dotted circle is unmistakable; any checker rejects it on sight. Counting such
an item as an autocorrection opportunity inflates the hard stratum with items that test nothing.
Both were in the hard stratum, which is the only stratum a bound is quoted on.

**What was done.** Two rules, with the shaper having the final word: the string rule now requires a
virama to sit *between* consonants, and **any string the shaper draws with a dotted circle is
implausible by definition**. Asking the shaper what it actually drew beats asking us what we think
is legal. Visibly-broken strings are still kept — a checker that misses them is unusable — but they
are always assigned `corrupt_target`, so the malformation sits in the string we ask about and never
in the image. The hard stratum is now entirely plausible with clean shaping.

**A near-miss worth recording.** Widening the vowel-sign set to catch `ॉम्बे` reintroduced the old
`तोड़ा` bug within minutes, because U+093C NUKTA sits inside the numeric run of vowel signs. The
regression test from the first design pass caught it immediately. That is the second time this
exact word has caught a rule change.

### 5.5 · `nfc()` did not do what the contract said

**OBSERVED.** `nfc()` performed `unicodedata.normalize("NFC", s).strip()`, while the contract said
"NFC and nothing else".

**Why it matters.** In a battery whose entire subject is *exactness*, a comparison primitive that
quietly does more than its name says is the wrong kind of surprise. Hidden here, it also meant the
whitespace decision was never argued or tested.

**What was done.** Three separately named, separately tested rules: `nfc()` is NFC only;
`strip_outer_whitespace()` is a **transport** rule applied at ingest (annotation-file artefacts) and
at response parsing (chat-transport artefacts), never internally; `canonical_equal()` is the
comparison predicate and does **not** strip. Internal whitespace is a real difference: `सुबह की`
and `सुबहकी` compare unequal.

### 5.6 · The language was "exact"; the operation is *canonically* exact

Corrected in the contract and README. Two encodings of the same nukta letter draw the same pixels,
so treating them as different would penalise a checker for correctly reporting what it saw. Saying
"character-for-character identity" without that caveat would have been a promise the code
deliberately does not keep — for a good reason that should be stated rather than buried.

### 5.7 · Repeat consistency was attached to "the leading checker"

**Why it matters.** That wording left open the reading that a checker could inherit a qualification
from another checker's stability. It cannot: stability is a property of the instrument.

**What was done.** A screening pass may rank and shortlist but produces **no qualification status of
any kind**. Any checker that receives a status must itself complete ≥3 full passes across the whole
battery in both shapes. A checker that was only screened is recorded as **"screened, not
qualified"**. The cost estimate rose accordingly (§ METRICS), because repeats now attach to every
qualifying checker rather than to one leader.

---

## 6 · The human requirement, and why it is small

**Not needed at all**, because ground truth is constructed: establishing what an image says,
resolving reader disagreement, adjudication, exact-agreement reference, the second reader.

**Still needed — ~1.5 hours, once**, and now **prepared as blank sheets** in
`eval/battery/devanagari-exactness/native-validation/`:

| Task | Time | Why |
|---|---|---|
| Validate the base word list (53 rows, stable ids) | 45–75 min | autocorrection only happens *toward* a plausible word; if a base is not a real word, the item does not test what we think |
| Perceptibility sample (25 pairs, round-robin across groups, hard items first) | ~20 min | the build proves the final pixels differ; it does not prove a person can **see** it at 40pt |
| Rendering sanity check (20 clean renders) | ~10 min | so we are not testing checkers against a broken font |

**Zero of it has been consumed.** Every answer column is blank; no person has been asked anything.

**One reader suffices**, and that is structural rather than a compromise: **none of these three
tasks produces ground truth.** A mistake degrades the battery; it cannot corrupt the answer key,
because the answer key does not come from a human.

**Word ids are stable** (`w-<12 hex of sha256(NFC(word))>`), so validation done today survives the
list being expanded — which it will need to be (§7).

---

## 7 · What the battery can support statistically — **corrected**

### The error in the first pass

The builder allowed **up to four mismatch items from one base word** (`MAX_ITEMS_PER_BASE = 4`) and
then quoted a binomial zero-failure upper bound over the item count. **That bound was computed over
correlated trials.** Four deterministic perturbations of `सुबह` are not four independent chances to
catch a checker out: a model that reads toward the plausible word will do it for all four. The
sample looked larger than the evidence was.

### The rule now, and it is structural

> **Every mismatch item sits on a distinct base word.**

So hard items and distinct hard base words are equal by construction, and a test asserts it. Class
coverage was **not** sacrificed to get there: the allocation is solved as a deterministic maximum
bipartite matching between failure classes and base words, so scarce classes claim a word before
common ones crowd them out. All **20 classes across 5 groups** remain represented at 53 words.

### The corrected numbers

| | Value |
|---|---:|
| Items | 106 (53 match / 53 mismatch) |
| Mismatch items / **distinct mismatch base words** | 53 / **53** |
| Hard items / **distinct hard base-word opportunities** | 37 / **37** |
| 95% upper bound, zero false passes, hard stratum | **7.8%** |
| 95% upper bound, all mismatches — *contains the above, not separate evidence* | 5.5% |
| Distinct opportunities needed for ≤5% | **59** |
| Validated base words needed for ≤5% | **84–85** |

**The earlier "~85–90 words" recommendation survives recomputation.** It was not carried over: 84 is
the arithmetic minimum, 85 is what the builder derives (`ceil(59 / 0.7)`), and 90 buys margin
against words being rejected during validation. It now rests on an opportunity count that is
genuinely one-per-word.

### ⚠ The epistemic limit, which must travel with the number

This is a **binomial upper bound over the opportunities this battery constructs**, conditional on
its word list, its operators and its font. The words are 53 lexical items from one dataset lineage;
the operators are a taxonomy we wrote. Neither is a probability sample of the Hindi a generator will
be asked to draw.

**It is therefore not an estimate of any checker's universal true error rate**, and no number of
extra words makes it one. "No false pass in 37 distinct opportunities, 95% upper bound 7.8% on this
material" is legitimate. "The checker's true error rate is ≤5%" is not.

**Per-class figures are not rates.** At ~2.6 items per class, one miss moves a "rate" by 30–50
points. They are diagnostic signals only.

### The pool cannot supply what the bound needs — **new finding**

**OBSERVED.** Merged repository-local material yields **53** distinct Hindi lexical items, all from
the EVAL-003 candidate manifest. The corpus manifest's 34,786 records all carry
`source_labels_ref: null` and hold no transcriptions; the raw `*_gt.txt` label files are git-ignored
and absent from merged state. The only other committed Devanagari of any volume is the
annotator-disagreement file (~50 strings) — and those are *specifically the contested ones*, where
at least one member of every pair is wrong by construction and several are Marathi. Using them would
put non-words at the base of items whose premise is that the base is a real word.

**Consequence.** Reaching ≤5% needs roughly **31–37 more Hindi lexical items**, which is a request
to Resources rather than something Eval should go and find. Filed as
`eval/tasks/EVAL-005-RESOURCES-REQUEST.md`, with a note that Resources may already hold them
uncommitted: 173 Hindi-labelled photographs were eligible in EVAL-003 and only 54 were selected, so
119 transcriptions were enumerated and never committed. How many *distinct* words that yields is
**unknown** and is Resources' to check.

This is optional, not blocking. A run at 53 words is possible; it simply carries 7.8%.

---

## 8 · What this battery cannot do — the boundary

A renderer always draws **well-formed** glyphs. No string will make it produce a half-formed
ligature, fused letters, a broken headline bar, or a stroke between two identities. Those are real
generator failures — one of ours is a sign whose misspelling **drifted between frames of a single
clip** — and no Unicode substitution reproduces them.

They are specified as **Class B** in `GENERATED-GLYPH-STRESS-LAYER.md`, with a recommended route
(deterministic corruption of clean renders, so the pixels stay known by construction) and an honest
note that programmatic damage is not the same distribution as a diffusion model's failures.

**Consequence for any result:** a checker that fails this battery cannot be trusted — it
autocorrects *well-formed* wrong text, the easier case. A checker that passes has cleared a
**necessary but not sufficient** bar, and that sentence must travel with the number.

---

## 9 · What remains uncertain

- **Whether the base words are all real, well-formed Hindi.** Still the single most important open
  question. The sheet is prepared; no reader has seen it.
- **Whether every raster-visible difference is perceptible** to a person at 40 point. Unmeasured.
- **Whether "plausible" is strong enough.** The plausibility rules test whether a string is a
  well-formed Devanagari **cluster**, not whether it is a lexically likely misspelling. `ककालका`
  (doubled initial consonant, from `कालका`) passes, though no Hindi word looks like that. Defensible
  — duplicated letters are a real generator failure and the question is about drawing, not the
  lexicon — but it means the hard stratum is "well-formed and visually subtle" rather than "a
  mistake a human would plausibly make". The perceptibility sample is where a reader could tell us
  some items are too easy.
- **Whether font choice changes results.** One font, pinned by hash. A different face could make a
  difference easier or harder to see; unmeasured, and now at least auditable.
- **Whether the shape-1 / shape-2 comparison behaves as hypothesised** — that showing the target
  invites autocorrection. Both shapes are now genuinely different experiments, which is what makes
  the comparison meaningful; the outcome is still a hypothesis.
- **Whether passing predicts anything about malformed generated glyphs.** Untested by construction.
- **How many distinct Hindi words Resources can actually supply**, and whether the ≤5% bound is
  worth the effort at all.
- **Whether the proposed thresholds are right.** 0.95 repeat consistency, ≤10% false fail, ≤5%
  refusal are judgement calls with no empirical backing in this repository.
- **Real per-call pricing.** The cost estimate rests on an old recorded figure that must be
  re-verified before any run.

---

## 10 · Scope and stop state

No paid checker call, no image or video model call, no network request to any model, no human time,
no Capability Registry entry, no BSTD use, no Marathi reserve use, and no change to any approved
EVAL-001/002/003 artifact.

EVAL-004 remains stopped: its Reader-A pilot is not promoted to ground truth, and no checker is
qualified, ranked or entered from it.

One stop condition fired and is **reported, not resolved**: the corrected sample-size requirement
needs lexical material the repository does not hold. Eval did not go looking for it.
