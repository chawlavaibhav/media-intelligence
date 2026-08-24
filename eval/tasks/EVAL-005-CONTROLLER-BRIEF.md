# Controller Brief — EVAL-005: Devanagari exactness battery, design hardening

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies.

**TASK:** EVAL-005 — design hardening after Controller review of the inherited `work/eval-005`
proposal. **Updated after a second review pass** (decoded pixels, independence language, merged
Resources state) and a **third merge-gate pass** (fail-closed PNG contract, two wording corrections).
**STATUS:** complete; **awaiting Controller review**. Design only — **no checker/model/API
qualification run and no human validation have occurred.** Only deterministic local construction,
rendering and test verification have been run (see *Fresh verification*).
**BRANCH:** `work/eval-005-controller-review` (based on `work/eval-005`, which is untouched;
`origin/main` merged in before final verification)
**SEVERITY:** `LOCAL`, with one `CROSS_STREAM` request to Resources.

**Spend:** **₹0 API/model · ₹0 generation · 0 human specialist hours · 0 Capability Registry
entries · BSTD and Marathi reserve untouched · EVAL-004 not resumed and its Reader-A pilot not
promoted.**

---

## HUMAN SUMMARY

The inherited proposal had the right idea. **Draw the test images ourselves**, and what each picture
contains is known without asking anyone — which dissolves the exact problem that stopped EVAL-004.

But four of its guarantees did not actually hold in the code, and its headline statistic was
computed the wrong way. In a battery whose entire purpose is to catch an instrument that
*confidently reports something it did not verify*, shipping instruments that confidently report
something they did not verify would have been the same mistake one level up.

**What was actually broken, in plain terms:**

- **The "blind" test was not blind.** One of the two checker shapes is supposed to make the model
  say what it sees *without* being shown the expected answer — that is the whole point of having
  two shapes. The contract handed every checker the answer anyway. Now there are two genuinely
  different input files, and a mechanical check refuses to write the blind one if a single
  Devanagari character has crept into it.
- **We measured differences in one font and drew the pictures in another.** The screen that decides
  "is this difference visible" used an exact font file; the image was drawn by looking up a font
  *name*. Proven: passing a completely nonexistent font file changed nothing about the output, and
  a nonexistent font *name* rendered happily with no error at all. On this machine both happened to
  land on the same font, so no built item was wrong — but nothing guaranteed it. Both now use one
  file, pinned by fingerprint, and a missing font stops the build instead of quietly substituting.
- **"The difference is visible" was checked on letter shapes, not on the actual picture.** Those are
  not the same claim, and I found a live example: `सुबह` and the same word with an invisible
  zero-width character produce **different letter-shape sequences** and **identical pictures**.
  The old check would have admitted that as a test item and then marked a checker *wrong* for
  correctly saying the two pictures look the same. (The replacement was itself wrong — see the
  second review pass below.)
- **The confidence number was computed over trials that were not independent.** One word was allowed
  to produce up to four test items, and then all four were counted as separate chances to catch a
  checker out. They are not: a model that misreads `सुबह` will misread every version of `सुबह`.
  Every test item now sits on its own word, so the count and the evidence are the same thing.
  Coverage of all 20 error types was kept by solving the allocation properly rather than by
  loosening the rule.
- **A rule I wrote let visibly broken text into the hardest test group.** Two items rendered strings
  the text engine itself marks as invalid with a dotted circle — glaring, and any checker would
  reject them on sight. Counting those as "hard" inflates the number that matters. Fixed by asking
  the text engine what it actually drew rather than asking my own rule what it thinks is legal.

**What the second review pass corrected, and why both corrections matter.**

*The visibility test was still wrong — this time in the opposite direction.* The first pass moved it
off letter shapes and onto the image file's fingerprint. But a PNG file is a container: the same
picture can be saved many different ways, and every one of them has a different fingerprint. Proven
here on a real battery image — one picture, three different file fingerprints. So a file-based test
would call two identical-looking pictures "different" and mark a checker wrong for correctly saying
they match, which is exactly the mistake the letter-shape test made from the other side. The test is
now on the **actual decoded pixels**, and the two kinds of fingerprint are named apart: one answers
*"did the checker read the file we sent"*, the other answers *"do these look different"*.

*And I overclaimed the statistics.* Making every test item use a different word was the right fix,
but I then described the result as "37 genuinely independent chances". It isn't. Using different
words removes the most obvious kind of repetition; it does not make the results behave like
independent coin flips. A checker blind to one Hindi mark is blind to it on every word carrying that
mark, and all 53 of our words come from one dataset. So the two things are now separated:

- **What a checker is actually judged on is a plain count: zero false passes.** No statistics
  involved.
- **The 7.8% figure is a sizing calculation**, valid only under an assumption we have adopted rather
  than demonstrated. Its field names now say so, and the build records
  `independence_status: NOT ESTABLISHED`.

The honest sentence is: *under an idealised model this battery does not establish, a clean sweep of
37 hard opportunities corresponds to a 7.8% reference ceiling.* Not "the checker is wrong less than
8 times in 100".

**The numbers themselves did not change.** 7.8%, and 84–90 words to bring that reference figure
below 5%. The repository holds **53**. More words tighten a calculation; they do not supply the
missing assumption.

**Resources PR #5 is merged and changes the shape of the ask.** It establishes that 3,924
single-word crops are transcription-resolvable — but that means the *labels are recoverable*, not
that the words are in git; the raw strings may still sit only in Resources' local corpus. So the
request now asks Resources to **check what it already has** before anyone considers acquiring
anything.

**What the third pass corrected.**

*The PNG decoder I built in pass two was itself only partly faithful.* It read the chunk that marks
pixels transparent, but only acted on it for one kind of image. For the other kinds it would have
recorded a see-through picture **as if it were solid** — silently, with no error, producing a wrong
answer that looks like a right one. Same class of mistake as the two it was built to fix, arriving a
third time through the component built to fix them. Two smaller versions of the same problem were
alongside it: 16-bit images were being quietly rounded down, and colour-profile information was being
ignored.

The fix is deliberately *narrower*, not bigger. The decoder now states exactly what it handles and
**refuses everything else** rather than approximating it — because the battery's own images are
plain 8-bit grayscale and need none of it. Transparency is now either applied correctly or the file
is rejected; never ignored. **No battery item, count or hash changed** — the manifest is byte-for-byte
what it was.

*Two phrases also needed correcting.* The qualification rule still said passing means "admitted for
further evaluation **at a stated bound**", which quietly reinstated the very claim the second pass
removed — that the 7.8% is a bound on a checker. Passing now means the checker **satisfied the
deterministic gates on this battery**, with the reference calculation reported separately under its
assumption. And several documents said "nothing has been run", which is simply not true: the build,
the rendering and the tests have all been run many times, and this brief quotes their results. What
has **not** happened is any checker/model/API qualification run or human validation, and every active
document now says that precisely.

---

## OBSERVED

*Every figure below is produced by committed code and reproducible by re-running it.*

### Defects measured in the inherited proposal

1. **`render()` ignored the pinned font file.** Rendering `सुबह` with a valid font file and with
   `/nonexistent/NoSuchFont.ttf` produced **byte-identical output** (`faffe232d6430ce4…` both
   times). The rasteriser was resolving a font *family name* through fontconfig.
2. **`pango-view` falls back silently.** Given the family `ThisFontDoesNotExistAnywhere` it rendered
   successfully with no warning and no error.
3. **Different glyph sequences do not imply different pixels.** `सुबह` vs `सु‌बह` (zero-width
   non-joiner): NFC-different, glyph sequences differ by one zero-advance glyph, **PNGs
   byte-identical**. The inherited glyph-only gate would have admitted this pair.
4. **Two hard items rendered strings the shaper marks invalid.** `इं्लीश` and `ॉम्बे` shape with
   U+25CC DOTTED CIRCLE. Both were in the hard stratum.
5. **`nfc()` performed `normalize("NFC", s).strip()`** while the contract said "NFC and nothing
   else".
6. **`MAX_ITEMS_PER_BASE = 4`** permitted up to four mismatch items per base word, over which a
   binomial zero-failure bound was then quoted.
7. **The transcribe payload was never separated from the verdict payload.** No projection code and
   no blind check existed; the discipline was prose only.

### Defects measured in the FIRST fix (second review pass)

8. **The visibility gate compared encoded PNG bytes.** Starting from a real `hb-view` render of
   `सुबह` and re-encoding its own decoded pixels twice (zlib level 1; zlib level 9 plus a `tEXt`
   chunk): **3 distinct file SHA-256 values, 1 distinct pixel fingerprint.**
9. **"37 genuinely independent hard chances"** appeared in the brief, and Clopper-Pearson figures
   were named `hard_bound_if_zero_false_passes_95pct` — a name that reads as a demonstrated bound.

### The corrected battery

| | |
|---|---:|
| Items | **106** — 53 match, 53 mismatch |
| Base words | 53 (every one appears in both strata) |
| Distinct image files / **file hashes** / **pixel fingerprints** | 90 / 90 / **90** |
| Paired items on a shared image with opposite verdicts | **32** |
| Failure classes / groups | **20 / 5** — unchanged by either fix |
| Mismatch items / **distinct mismatch base words** | 53 / **53** |
| **Hard items / distinct hard base-word opportunities** | **37 / 37** |
| Candidates screened | 1,834 valid; 2 rejected `canonical_equal`; **0** rejected `raster_identical` |
| Determinism | two builds → identical `items.jsonl` sha256 |
| Blind check | transcribe 106 payloads, **0** violations; verdict 106 payloads, **0** violations |
| **Items changed by moving from file bytes to decoded pixels** | **0** — item-for-item identical |

### Sizing figures — an iid REFERENCE calculation, not a bound

> Under an iid / exchangeable Bernoulli opportunity model, zero false passes in **37 distinct hard
> base-word opportunities** corresponds to a one-sided 95% **reference** upper bound of **7.8%**.
>
> **EVAL-005 does not establish iid or exchangeability.** 7.8% is not a universal checker error
> bound and not an estimate of real-world error. The qualification gate is the deterministic *zero
> false passes*, which needs no probability model.

| Stratum | n | iid reference upper bound, zero false passes |
|---|---:|---:|
| **Hard — plausible ∧ `corrupt_image`, one per base word** | **37** | **7.8%** |
| All mismatches *(contains the above; not separate evidence)* | 53 | 5.5% |
| Per failure class | ~2.6 mean | **not estimable** |

| Reference target | Opportunities | Base-word **planning target** |
|---|---:|---:|
| <5% | **59** | **84–85** (90 for margin) |
| <10% | 29 | 42 |

Machine-readable field names carry the assumption:
`iid_reference_upper_bound_if_zero_false_passes_95pct`,
`hard_opportunities_for_5pct_iid_reference`,
`validated_base_words_planning_target_for_5pct_iid_reference`, plus
`independence_status: "NOT ESTABLISHED. …"`.

### Lexical pool — checked against merged `main` (Resources PR #5 included)

| Source in merged `main` | Distinct Hindi strings | Usable |
|---|---:|---|
| `eval/calibration/devanagari-v0/candidate-manifest.jsonl` | **53** | yes, in use |
| `annotator-disagreement.json` | ~50 | **no** — these are the *contested* strings; one of each pair is wrong by construction, several are Marathi |
| `resources/manifests/corpus-pilot-v0.jsonl` (34,786 records) | 0 | no — every record has `source_labels_ref: null` |
| Merged Resources records from PR #5 | 1 (a worked example) | no — they carry counts and method, not the lexicon |
| Raw corpus / distributor label files | **unknown** | not visible to Eval — `resources/corpus/raw/` is git-ignored |

**53 available, 84–90 is the planning target.**

**Merged Resources facts now on record:** IndicSTR12 2,711 crops, all 2,711 transcription-resolvable;
IIIT-ILST 1,214 crops, 1,213 resolvable; **3,924 resolvable single-word crops total**, by two
independent routes. IndicSTR12 and IIIT-ILST remain **one evaluation lineage**; BSTD remains the
genuine cross-lineage reserve.

**Stated precisely:** that establishes the labels are *recoverable*, not that the lexical strings are
in git. How many *distinct* Hindi words they yield is **unknown**, and none of them would be
*validated* words — every candidate still needs the Hindi lexical validation, exactly like the 53.

---

## INFERRED

- **The blind/visible shape comparison is now a real measurement.** Previously both shapes showed
  the model the target, so any difference between them would have been noise. Whether showing the
  target actually increases false passes remains a hypothesis — but it is now a testable one.
- **The font defect had no effect on the built battery, only on its guarantees.** On this machine
  fontconfig resolved to the same Kohinoor file, so no item was mis-screened. The fix converts a
  coincidence into a checkable property.
- **Neither visibility fix changed a single item.** On the current pool the glyph test, the
  file-byte test and the decoded-pixel test all agree — all 90 image files have 90 distinct file
  hashes *and* 90 distinct pixel fingerprints. What changed both times is that the claim the battery
  makes is now the claim it verifies, and the ZWNJ and re-encoding examples show the tests genuinely
  can diverge.
- **A pure-stdlib PNG decoder was the right call, not a compromise.** Neither Pillow nor numpy is on
  this machine. Adding an image library to a battery whose whole premise is pinned local tooling
  would have traded a real property for convenience; `zlib` plus the PNG spec is ~200 lines, is
  strict about what it will not decode, and cross-checks against `sips` for dimensions.
- **The independence overclaim was mine, not the inherited proposal's.** The first review pass fixed
  a real correlation problem and I then oversold the fix. Worth noting because it is the failure mode
  this stream exists to catch: a correction that goes one step further than the evidence supports is
  harder to see than the original error.
- **Three passes, three instances of one pattern — and each fix introduced the next.** The glyph gate
  was too weak; the file-hash gate that replaced it was too strong; the decoder written to settle it
  was itself partly unfaithful. Nothing here was careless in isolation. **A component built to
  enforce a guarantee is not exempt from needing the same scrutiny as the thing it guards**, and on
  this evidence it is where the next defect is most likely to be.
- **Narrowing beat implementing.** Faithfully implementing `tRNS` for every colour type was the
  alternative. Refusing what the battery does not need is smaller, has fewer paths that can be
  wrong, and fails loudly instead of quietly if the renderer ever changes.
- **The corrected figure is slightly *tighter*, not looser** (7.8% at n=37 vs the claimed 8.2% at
  n=35), because the one-per-base rule happens to yield more hard items at this pool size. The
  earlier figure was not comparable in the first place, since it mixed correlated items.
- **"~85–90 words" survives recomputation.** I recomputed it from the corrected selection logic
  rather than inheriting it: 84 is the arithmetic minimum, 85 is what the builder derives, 90 buys
  margin against words failing validation. It is a **planning target for a reference calculation**,
  not a threshold that would prove anything about real-world error.

---

## SURPRISES / BELIEF UPDATES

- **"Do these look the same" has one right test and two tempting wrong ones, and I used both wrong
  ones in turn.** Letter shapes are too weak — the ZWNJ pair differs there and draws identically.
  File fingerprints are too strong — one picture written three ways gives three fingerprints. Only
  the decoded pixels answer the question asked. Any future visibility claim in this project should
  be settled on the artefact as *rendered*, not on any representation upstream or downstream of it.
- **De-correlating a sample is not the same as making it independent, and the gap is easy to miss
  precisely because the fix was correct.** One item per word was right. Calling the result
  "independent" was not, and it converted a sizing calculation into an implied claim about a
  checker's real error rate.
- **The plausibility rule broke twice on the same word.** Widening the vowel-sign set to catch
  `ॉम्बे` immediately reintroduced the old `तोड़ा` bug, because U+093C NUKTA sits inside the numeric
  run of vowel signs. The regression test from the first design pass caught it within a minute. That
  is the second time `तोड़ा` has caught a rule change, and it argues for keeping character-level
  rules empirical — ask the shaper, do not encode a grammar.
- **Two tests I wrote were initially tautologies or self-matches.** The nukta pair written as source
  literals is indistinguishable on disk (both forms look identical, and an editor may normalise
  one), so the invisible-difference test silently compared a string with itself; and the
  "no network call" scanner matched its own pattern literal. Both are now built from explicit
  codepoints and assembled fragments. **A test that cannot fail is worse than no test**, because it
  reports safety.

---

## FAILURES / BLOCKERS

**One stop condition fired and is reported, not resolved.**

> *"the corrected sample-size requirement needs new external lexical material"*

Bringing the reference figure below 5% needs 84–90 validated Hindi words; merged repository-local
material yields 53. Per the task's scope, Eval did **not** go source-hunting.

**Reordered after the second review pass.** Now that Resources PR #5 is merged, the first step in
`eval/tasks/EVAL-005-RESOURCES-REQUEST.md` is a **check of existing local material** — 3,924 crops
are transcription-resolvable and their strings may already be in Resources' hands. **No new
acquisition is requested**; that would need separate Controller authorisation.

**This does not block a run.** A run at 53 words is possible and reports the figure at 37
opportunities.

No other blocker. Seven defects were found and fixed across the two passes; each is pinned by a
test.

---

## UNKNOWN / NOT VERIFIED

- **Whether the 53 base words are all real, well-formed Hindi.** Still the most important open
  question. The sheet is prepared and blank; no reader has seen it.
- **Whether every raster-visible difference is perceptible to a person** at 40 point. Unmeasured.
- **Whether "plausible" is strong enough.** The rules test whether a string is a well-formed
  Devanagari *cluster*, not a lexically likely misspelling. `ककालका` (doubled initial consonant, from
  `कालका`) passes, though no Hindi word looks like that. Defensible — duplicated letters are a real
  generator failure — but the hard stratum is "well-formed and visually subtle", not "a mistake a
  human would plausibly make".
- **Whether font choice changes results.** One font, now pinned by hash. Unmeasured.
- **Whether the transcribe/verdict difference behaves as hypothesised.** Untested.
- **Whether passing predicts anything about malformed generated glyphs.** Untestable here by
  construction; that is Class B.
- **How many distinct Hindi words Resources can actually supply.** 3,924 single-word crops are
  transcription-resolvable per merged PR #5, but the strings are not in git, may repeat one another,
  may repeat the 53 in use, and are candidate lexical items rather than validated words. Eval cannot
  see the git-ignored raw tree.
- **How correlated a checker's errors actually are** across words, diacritics and failure classes.
  Unmeasured — and it is exactly what would have to be understood before any figure from this
  battery could become a real-world error estimate.
- **Real per-call pricing.** The cost estimate rests on an old recorded figure.
- **Whether the proposed thresholds are right.** 0.95 repeat consistency, ≤10% false fail, ≤5%
  refusal have no empirical backing in this repository.
- **Whether the decoder is faithful on paths the battery never exercises.** It is tested on what
  `hb-view` emits plus hand-built edge cases; the accepted contract is narrow precisely because
  everything outside it is refused rather than trusted.

---

## CORRECTIONS MADE AFTER CONTROLLER REVIEW

| # | Required fix | What changed | Pinned by |
|---|---|---|---|
| 1 | Remove target leakage from `transcribe` | New `checker_input.py`: separate per-shape projections; allow-list that fails closed; `verify_blind()` rejects any Devanagari in a blind payload; `write_checker_inputs()` refuses to write a failing file; evaluator-side `scoring-key.jsonl` kept separate | 5 tests, incl. injecting a target as a field **and** smuggling one into the prompt |
| 2 | Pin shaping and rendering to one font | `hb-view` replaces `pango-view`; same font **file** + `--face-index` as `hb-shape`; `FontMissing` on a missing font, no fallback; provenance records font sha256, tool versions, size, margin, colours; portability claims corrected; **no font binary committed** | 4 tests, incl. a `subprocess` spy asserting both commands carry the same file, and a check that no font is in `git ls-files` |
| 3 | Verify visible difference on final pixels | Gate moved off glyph sequences; reasons `canonical_equal` / `raster_identical` / `rendering_error`; glyph comparison retained as a diagnostic and recorded on rejections; screening renders to a process-lifetime scratch dir deleted on exit. **Superseded in part by fix 8 below** — the first version compared encoded PNG bytes | 5 tests, incl. the nukta pair, the ZWNJ pair, and सुबह/सुवह accepted |
| 4 | Make normalisation semantics true | `nfc()` is NFC only; `strip_outer_whitespace()` is a separate named transport rule (ingest + response parsing); `canonical_equal()` is the predicate and does not strip; docs say *canonical* exactness, not codepoint identity | 3 tests, incl. internal whitespace being a real difference |
| 5 | Fix the independence claim | One mismatch item per distinct base word; deterministic maximum bipartite matching preserves all 20 classes; both counts reported; figure derived from the opportunity count; sample-size target recomputed; epistemic limit stored **in the build summary**, not only in prose. **Extended by fix 9 below** — the result was then over-described as independence | 5 tests, incl. `hard_items == distinct_hard_base_words` and the figure being derived |
| 6 | Qualification / repeat logic | Screening pass produces **no status**; any checker given a status completes ≥3 full passes in both shapes itself; "screened, not qualified" is an explicit outcome; gates 1 and 2 merged into one rule with the hard stratum named as the primary disqualifying subset and the one the reference figure is quoted on; thresholds marked proposed; cost estimate raised accordingly | doc-level |
| 7 | Formalise and prepare | `eval/tasks/EVAL-005.md`; `make_validation_sheets.py` + `native-validation/` with 53/25/20 blank rows and stable ids; `EVAL-005-RESOURCES-REQUEST.md`; findings, HANDOFF and this brief updated; inherited `PROPOSED-*` files kept and banner-marked superseded | 1 test (sheets exist, ids stable) |

### Second review pass

| # | Required fix | What changed | Pinned by |
|---|---|---|---|
| 8 | Compare decoded pixels, not encoded PNG bytes | New `pngraster.py`: stdlib-only PNG decoder to a canonical RGBA8 raster; `pixel_fingerprint()` hashes dimensions + format + pixel data; `is_valid_mismatch()` decides `raster_identical` on it. Two hashes kept and renamed apart — `image_file_sha256` (artifact identity, still recorded and still what a checker run should log) vs the pixel fingerprint (visual identity). Decoder raises `UnsupportedPNG` rather than guessing | 4 tests: three encodings of one picture → 3 file hashes / 1 pixel fingerprint; dimensions separated from payload in the fingerprint; ZWNJ rejection preserved; सुबह/सुवह still accepted; decoder refuses a non-PNG and an interlaced header |
| 9 | Correct the independence claim | "Genuinely independent" and equivalents removed everywhere; wording is now "distinct hard base-word opportunities"; **zero false passes** stated as the deterministic gate; Clopper-Pearson kept as an explicit iid **reference** calculation; fields renamed `iid_reference_upper_bound_…`, `…_for_5pct_iid_reference`, `…_planning_target_…`; `independence_status: "NOT ESTABLISHED. …"` added to the build summary; the Checker Contract's "each item is independent" corrected to execution isolation ≠ statistical independence | 2 tests: every statistical field names its assumption, and a grep over **all** EVAL-005 sources and documents fails on independence language |
| 10 | Update Resources state | `origin/main` merged in; every "PR #5 open/not merged" statement removed; merged composition facts recorded (2,711/2,711 · 1,213/1,214 · 3,924 resolvable · one lineage · BSTD the reserve); the request reordered so **step 1 is a check of existing local material** and no acquisition is requested; explicit that recoverable labels ≠ lexical strings in git, and that crop labels are candidates needing validation, not validated words; BSTD/Marathi explicitly excluded from count-filling | doc-level |

### Third review pass — merge gate

| # | Required fix | What changed | Pinned by |
|---|---|---|---|
| 11 | PNG decoder must fail closed on features it does not faithfully decode | `tRNS` was parsed but applied to indexed images only, so grayscale/truecolour transparency was silently decoded as opaque. The supported contract is now explicit and narrow — accepted: non-interlaced, bit depths 1/2/4/8 in spec-legal colour-type combinations, colour types 0/2/3/4/6, **`tRNS` for indexed only** (faithfully applied), and ancillary chunks that cannot alter a raster (`bKGD` — which is what `hb-view` emits — `tEXt`, `pHYs`, …). Refused: `tRNS` on grayscale/truecolour (changes alpha, not implemented), `tRNS` on types 4/6 (spec forbids it), **bit depth 16** (was truncated to the high byte, so two images could collide), illegal depth/colour combinations, indexed without a palette, `gAMA`/`sRGB`/`iCCP`/`cHRM`/`acTL`, and any unrecognised **critical** chunk. Unrecognised *ancillary* chunks are still skipped — what the spec's ancillary bit is for. **Not expanded into a general PNG library** | 3 tests / 34 checks: indexed + `tRNS` decodes with alpha applied and yields a **different** fingerprint from the same image without it; grayscale/truecolour/RGBA + `tRNS` all refused; every narrowed case refused; every accepted case still decodes with an unchanged fingerprint; all 90 real battery images decode |
| 12 | Statistical wording | *"admitted for further evaluation at a stated bound"* removed — passing now means **the checker satisfied the deterministic qualification gates on this battery**, with the iid reference calculation reported separately under its stated assumption. All EVAL-005 docs swept for the same slippage (*"the only stratum a bound is quoted on"*, *"to support a ≤5% bound"*, *"the bound-bearing one"*) and rewritten to name the reference figure | doc-level + the independence guard, now also allowing code spans |
| 13 | "Nothing has been run" | Replaced everywhere with: **no checker/model/API qualification run and no human validation have occurred; only deterministic local construction, rendering and test verification have been run.** Applied to the README, taxonomy, contract, metrics, task file, HANDOFF, this brief and the PR description | doc-level |

**Additional defect found while fixing #3, not in any required list:** the plausibility rule let
two shaper-invalid strings into the hard stratum. Now decided by the shaper's dotted circle plus a
tightened virama rule. 2 tests.

---

## ASSUMPTIONS CHALLENGED

None promoted or demoted; no experiment was run. Consistent with `coordination/ASSUMPTIONS.md` §12 —
the cost model separates evaluation cost from human time, and human time still dominates.

## LOCAL IMPLICATIONS

Eval has a checker-qualification design whose ground truth needs no human, and whose own instruments
are now verified rather than asserted. The EVAL-003 pack, crops and two-reader protocol are
untouched and remain available if the photographed-signage screen is ever wanted.

## CROSS-STREAM IMPLICATIONS

**One request to Resources**, `eval/tasks/EVAL-005-RESOURCES-REQUEST.md`, in two ordered steps:

1. **A check, not an acquisition** — Resources checks its existing legitimate local corpus and
   distributor label files for additional unique Hindi lexical strings already in hand.
2. **Only if that falls short**, report the gap and stop. New acquisition needs separate Controller
   authorisation and is **not** requested.

The likely shortfall is ~31–37 distinct Hindi words as plain text — no images, no transcriptions, no
new corpus. Optional; it tightens the reference figure from 7.8% to below 5% and does not block a
run.

**No Resources or Canon file was edited.** Resources PR #5 is **merged** and `origin/main` was
merged into this branch before final verification; the request is written against those merged facts.

## ARCHITECTURAL IMPLICATIONS

None. No battery dimension, ladder, pass criterion, observation-unit term or Registry field is
changed. `coordination/WORKSTREAM-STATUS.md` was **not** edited — a proposed replacement row is
below.

---

## PROPOSED REPLACEMENT ROW FOR `coordination/WORKSTREAM-STATUS.md`

*Controller-owned file; offered, not applied.*

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Eval | **EVAL-004 remains stopped. EVAL-005 opened as design hardening only and is complete after two review passes, awaiting review.** A constructed-Devanagari exactness battery exists and has been built and tested locally; **no checker/model/API qualification run and no human validation have occurred**, and no checker is qualified. Its qualification gate is deterministic (zero false passes); the Clopper-Pearson figure is an explicitly-labelled iid reference calculation, not a demonstrated bound. | EVAL-005 design hardening on `work/eval-005-controller-review`. | Controller decisions on: (a) approve/reject the hardened design; (b) ~1.5 h of one Hindi reader; (c) checker roster + API budget; (d) whether to ask Resources to **check existing local material** for ~31–37 more Hindi words, tightening the reference figure from 7.8% to <5%; (e) the proposed qualification thresholds. No run without all of (a)–(c). |

---

## FRESH VERIFICATION — commands, exit codes, results

Run from the final PR head after `rm -rf build __pycache__`. No prior session's or prior pass's claim
was relied on: each pass re-ran the full suite from scratch (inherited 36 checks → 121 → 141 → 165).

```
$ python3 build_items.py --total 120
exit 0 — 106 items (53 match / 53 mismatch), 53 base words, 20 classes across 5 groups,
         37 hard items / 37 distinct hard base words,
         iid_reference_upper_bound_if_zero_false_passes_95pct = 0.0778,
         hard_opportunities_for_5pct_iid_reference = 59,
         validated_base_words_planning_target_for_5pct_iid_reference = 85,
         independence_status = "NOT ESTABLISHED. …",
         screened 1834 valid, rejected {'canonical_equal': 2}

$ python3 test_devanagari_exactness.py
exit 0 — ALL CHECKS PASSED
         165 checks across 43 test functions, 0 failures
         (121/37 after pass 1 · 141/41 after pass 2 · +2 tests, +24 checks in pass 3)

$ python3 make_validation_sheets.py --from-build build
exit 0 — word-validation-sheet.csv 53 rows · perceptibility-sheet.csv 25 rows
         · rendering-sanity-sheet.csv 20 rows · every answer column blank

$ python3 build_items.py --total 120 --out-dir <tmp>      # determinism
   both items.jsonl sha256 = 9c69cac28c3123713652a26548eb09aabdd36966a44a433a9069b787fea6d09d

$ verify_blind on both written checker-input files
   transcribe  n=106  violations=0
   verdict     n=106  violations=0
```

### Did the narrower PNG contract change the battery?

**No — and this is the measured result, not an assumption the fix was constrained to produce.**

| | Before narrowing | After narrowing |
|---|---|---|
| `items.jsonl` sha256 | `9c69cac2…fea6d09d` | `9c69cac2…fea6d09d` — **byte-identical** |
| Items / match / mismatch | 106 / 53 / 53 | 106 / 53 / 53 |
| Hard items / distinct hard base words | 37 / 37 | 37 / 37 |
| Classes / groups | 20 / 5 | 20 / 5 |
| Image files / file hashes / pixel fingerprints | 90 / 90 / 90 | 90 / 90 / 90 |
| Candidate screening | 1,834 valid; 2 `canonical_equal`; 0 `raster_identical` | unchanged |
| Battery images decoding under the contract | — | **90 of 90** |

The reason is that `hb-view` emits 8-bit grayscale, non-interlaced, with `bKGD` and **no** `tRNS` —
comfortably inside the accepted contract. Everything the narrowing now refuses is something the
battery never produced; what changed is that a file which *did* carry it would now stop the build
instead of being fingerprinted wrongly.

### Transparency regression — the disjunction, demonstrated

| Case | Result |
|---|---|
| Indexed + `tRNS` | **decoded correctly** — index 0 alpha 0, index 1 alpha 255, and a **different** fingerprint from the same image without `tRNS` |
| Grayscale + `tRNS` | **refused** (`UnsupportedPNG`) |
| Truecolour + `tRNS` | **refused** |
| RGBA + `tRNS` (spec-forbidden) | **refused** |
| 16-bit · illegal depth/colour · indexed without palette · unknown **critical** chunk · `gAMA` / `sRGB` / `cHRM` / `acTL` | **refused** |
| `bKGD` (what `hb-view` emits) · `tEXt` · unknown **ancillary** chunk | **accepted, fingerprint unchanged** |

Never fingerprinted as if transparency did not exist.

### Preserved through the narrowing

- different PNG encodings / same decoded pixels → **same pixel fingerprint** (3 file hashes, 1
  fingerprint, from a real battery render);
- ZWNJ visually-identical pair → **rejected**;
- `सुबह` / `सुवह` → **accepted**;
- `image_file_sha256` retained **separately** as encoded-artifact identity.

### Stale-claim grep

Every EVAL-005-owned source and document was grepped for `PR #5 open`, `open, not merged`,
`genuinely independent`, `independent chances`, `independent trials`, `statistically independent`,
`final PNG bytes`, `raster_sha256`, `image_sha256`, `hard_bound_if_zero`,
`zero_failure_upper_bound`, `admitted for further evaluation`, `at a stated bound`,
`Nothing has been run`.

**No live claim survives.** Remaining occurrences sit inside quotation marks or code spans, citing
the wording that was removed — and a committed test enforces exactly that rule for the independence
language: it may appear only inside a quotation or a code span, never in bare prose, in either
direction.

### Environment and rendering provenance

| | |
|---|---|
| Python | 3.14.6 (`/opt/homebrew/bin/python3`) |
| Shaper | `hb-shape (HarfBuzz) 14.2.1` |
| Renderer | `hb-view (HarfBuzz) 14.2.1` — same library, takes a font file, no fontconfig |
| PNG output from `hb-view` | 8-bit grayscale, non-interlaced, `bKGD`, no `tRNS` |
| PNG decoding | `pngraster.py` — stdlib `zlib` only. **Pillow and numpy are not installed**, and no image library was added |
| Font file | `/System/Library/Fonts/Kohinoor.ttc`, face index 0 |
| **Font SHA-256** | `8b508b160d4573963c064e951af48c33c6381901253ec6ae0feb86d80fde1f31` |
| Font size on disk | 1,397,704 bytes (5-face collection) |
| Point size / margin | 40 / 24 |
| Background / foreground | `FFFFFF` / `000000` |
| Font committed to repo | **No.** Proprietary system asset; identity pinned by hash instead. |
| Platform | macOS (Darwin 23.6.0), Apple silicon |

`pango-view` is no longer used anywhere; a test asserts it. Decoder output was cross-checked against
`sips -g pixelWidth -g pixelHeight`.

---

## EVIDENCE WORTH HUMAN INSPECTION

- **`eval/battery/devanagari-exactness/build/images/`** — the rendered items, after
  `python3 build_items.py --total 120`. Worth looking at three or four; it is the whole design in
  one glance.
- **`build/checker-input-transcribe.jsonl` next to `build/checker-input-verdict.jsonl`** — the
  clearest demonstration that the two shapes are different experiments. The first contains no
  Devanagari at all.
- **`build/build-summary.json` → `opportunity_model`** — worth reading in full. It is where the
  distinction between the deterministic gate and the iid reference calculation is stored in
  machine-readable form, including `independence_status: "NOT ESTABLISHED. …"`.
- **`eval/battery/devanagari-exactness/native-validation/`** — exactly what a reader would be asked,
  and how little of it there is.
- **`GENERATED-GLYPH-STRESS-LAYER.md`** — what this battery deliberately **cannot** test, and why
  that boundary is stated rather than blurred.

## FILES CHANGED

**New:** `eval/tasks/EVAL-005.md`, `eval/tasks/EVAL-005-CONTROLLER-BRIEF.md`,
`eval/tasks/EVAL-005-RESOURCES-REQUEST.md`,
`eval/battery/devanagari-exactness/{checker_input.py, pngraster.py, make_validation_sheets.py}`,
`eval/battery/devanagari-exactness/native-validation/{README.md, word-validation-sheet.csv, perceptibility-sheet.csv, rendering-sanity-sheet.csv}`.

**Modified:** `eval/battery/devanagari-exactness/{devtext.py, perturb.py, build_items.py,
test_devanagari_exactness.py, README.md, CHECKER-CONTRACT.md, METRICS-AND-QUALIFICATION.md,
FAILURE-TAXONOMY.md, NATIVE-VALIDATION.md}`,
`eval/findings/devanagari-exactness-design-findings.md`, `eval/HANDOFF.md`.

**Banner-marked superseded, otherwise unedited:**
`eval/tasks/PROPOSED-EVAL-005-CONTROLLER-BRIEF.md`,
`eval/battery/devanagari-exactness/PROPOSED-TASK-SPEC.md`.

**Untouched:** every EVAL-001/002/003 artifact, every EVAL-004 record, all Canon files, all
Resources files (including everything that arrived with PR #5), `coordination/WORKSTREAM-STATUS.md`,
BSTD, the Marathi reserve, and the `work/eval-005` branch itself. The `origin/main` merge brought
Canon and Resources changes into the branch's base; **none of them was edited.**

---

## DECISIONS NEEDED FROM CONTROLLER

Each blocks something different.

1. **Approve or reject the hardened design.** Blocks everything downstream.
2. **Approve ~1.5 hours of one Hindi-competent reader** against the prepared blank sheets. Blocks
   the run. Note the structural point: none of the three tasks establishes ground truth, so a
   mistake there degrades the battery but cannot corrupt the answers.
3. **Approve a checker roster and API budget.** Blocks the run. Order of **₹600–2,100 / $7–24** for
   a first pass across both shapes — higher than the earlier estimate because repeats now attach to
   every checker that is given a status, not to one leader. The price per call is an old recorded
   figure and must be re-verified before any run. **No roster is selected here; that is
   deliberately yours.**
4. **Decide whether to ask Resources to check for ~31–37 more Hindi words.** Optional. It is the
   difference between a 7.8% and a sub-5% **reference** figure — not between an unproven and a proven
   error rate. Resources may already hold the words: merged PR #5 records 3,924 transcription-
   resolvable single-word crops, though the strings are not in git and their distinct-word yield is
   unknown. **The request asks for a check, not a download**; acquisition would be a separate
   decision.
5. **Approve or amend the proposed qualification thresholds** — 0.95 repeat consistency, ≤10% false
   fail, ≤5% refusal. They are judgement calls with no empirical backing in this repository, and
   they should probably be revisited once we have seen what real checkers do.
6. **Decide separately on the Class B generated-glyph layer.** Specified, not built, needs
   generation spend.
7. **Note before any result exists** what a pass does and does not mean. It is *zero false passes
   across N distinct hard base-word opportunities on this battery's material* — a deterministic
   result. Any percentage quoted alongside it is an **iid reference calculation under an assumption
   EVAL-005 does not establish**: never an accuracy claim, never a real-world error rate, and silent
   about malformed generated glyphs.

## RECOMMENDED NEXT STEP

*A recommendation, not an action taken.*

Approve the design and the reader time first, and have the reader validate the word list before
anything is bought. If Resources turns out to already hold the extra words, expand the list in the
same sitting — the sheet ids are stable, so nothing done now is wasted. Roster and API spend can
follow; they are cheap and are not the constraint.

## EPISTEMIC CHECK

Every figure is produced by committed code and reproducible by re-running it. Interpretations are
confined to INFERRED. Unknowns are listed rather than filled. Nothing is presented as approved: the
battery is a design, the thresholds are proposals, and no checker has been run, qualified or ranked.
The one stop condition that fired is reported rather than resolved.

## CONFIRMATION

**No checker/model/API qualification run and no human validation have occurred.** Only deterministic
local construction, rendering and test verification have been run — the commands above, none of which
makes a network call, and a test asserts that no module in the battery references a network client, a
URL or an API key.

No paid checker call. No free checker call. No model API call of any kind. No image or video
generation. No human specialist time consumed — every answer column in every prepared sheet is blank.
No Capability Registry entry. No BSTD or Marathi reserve use. No Canon or Resources file edited.
EVAL-004 not resumed, its Reader-A pilot not promoted to ground truth, and no checker qualified,
disqualified or ranked from it or from anything else. EVAL-006 not started.
