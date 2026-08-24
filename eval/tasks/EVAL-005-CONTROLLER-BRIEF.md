# Controller Brief — EVAL-005: Devanagari exactness battery, design hardening

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies.

**TASK:** EVAL-005 — design hardening after Controller review of the inherited `work/eval-005`
proposal.
**STATUS:** complete; **awaiting Controller review**. Design only — nothing has been run.
**BRANCH:** `work/eval-005-controller-review` (based on `work/eval-005`, which is untouched)
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
  zero-width character produce **different letter-shape sequences** and **byte-identical images**.
  The old check would have admitted that as a test item and then marked a checker *wrong* for
  correctly saying the two pictures look the same. The check is now on the final image.
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

**Two numbers you should take away.**

The battery's real strength today is **37 genuinely independent hard chances**, giving a **7.8%**
ceiling if a checker never fails one. In plain terms: a checker with a perfect score could still be
wrong about 8 times in 100 on this material and we would not have seen it. Getting that below 5 in
100 needs **84–90 validated words**; the repository holds **53**. That gap is the one thing worth
your attention, and it is a request to Resources, not something Eval should go and solve.

And a caveat that must travel with any future result: even at 90 words this bounds what *this
battery* could have missed. Our words come from one dataset lineage and our error types are a
taxonomy we wrote. **It is never an estimate of a checker's true error rate in the world.**

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

### The corrected battery

| | |
|---|---:|
| Items | **106** — 53 match, 53 mismatch |
| Base words | 53 (every one appears in both strata) |
| Distinct images | 90; **32** items paired on a shared image with opposite verdicts |
| Failure classes / groups | **20 / 5** — unchanged after the independence fix |
| Mismatch items / **distinct mismatch base words** | 53 / **53** |
| **Hard items / distinct hard base-word opportunities** | **37 / 37** |
| Candidates screened | 1,834 valid; 2 rejected `canonical_equal`; **0** rejected `raster_identical` |
| Determinism | two builds → identical `items.jsonl` sha256 `8572ef1cdb97322d…` |
| Blind check | transcribe 106 payloads, **0** violations; verdict 106 payloads, **0** violations |

### Bounds, recomputed

| Stratum | n | 95% upper bound with zero false passes |
|---|---:|---:|
| **Hard — plausible ∧ `corrupt_image`, one per base word** | **37** | **7.8%** |
| All mismatches *(contains the above; not separate evidence)* | 53 | 5.5% |
| Per failure class | ~2.6 mean | **not estimable** |

| Target | Distinct opportunities needed | Validated base words needed |
|---|---:|---:|
| ≤5% | **59** | **84–85** (90 for margin) |
| ≤10% | 29 | 42 |

### Lexical pool — checked, not assumed

| Source in merged `main` | Distinct Hindi strings | Usable |
|---|---:|---|
| `eval/calibration/devanagari-v0/candidate-manifest.jsonl` | **53** | yes, in use |
| `annotator-disagreement.json` | ~50 | **no** — these are the *contested* strings; one of each pair is wrong by construction, several are Marathi |
| `resources/manifests/corpus-pilot-v0.jsonl` (34,786 records) | 0 | no — every record has `source_labels_ref: null` |
| Raw `*_gt.txt` label files | unknown | not available — `resources/corpus/raw/` is git-ignored, absent from merged state |

**53 available, 84–90 needed.**

---

## INFERRED

- **The blind/visible shape comparison is now a real measurement.** Previously both shapes showed
  the model the target, so any difference between them would have been noise. Whether showing the
  target actually increases false passes remains a hypothesis — but it is now a testable one.
- **The font defect had no effect on the built battery, only on its guarantees.** On this machine
  fontconfig resolved to the same Kohinoor file, so no item was mis-screened. The fix converts a
  coincidence into a checkable property.
- **The raster gate changed no items either.** On the current pool the pixel test and the glyph test
  never disagreed. What changed is that the claim the battery makes is now the claim it verifies —
  and the ZWNJ example shows the two genuinely can diverge.
- **The corrected bound is slightly *tighter*, not looser** (7.8% at n=37 vs the claimed 8.2% at
  n=35), because the one-per-base rule happens to yield more hard items at this pool size. The
  earlier figure was not comparable in the first place, since it mixed correlated items.
- **"~85–90 words" survives recomputation.** I recomputed it from the corrected selection logic
  rather than inheriting it: 84 is the arithmetic minimum, 85 is what the builder derives, 90 buys
  margin against words failing validation.

---

## SURPRISES / BELIEF UPDATES

- **The ZWNJ case is the strongest single result here.** I expected the glyph-vs-pixel distinction
  to be a technicality. It is not: a real, easily-constructed pair passes the glyph gate and fails
  the pixel gate. Any future visibility claim in this project should be settled on the artefact
  being shown, not on an intermediate representation of it.
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

Reaching a ≤5% bound needs 84–90 validated Hindi words; merged repository-local material yields 53.
Per the task's scope, Eval did **not** go source-hunting. The precise requirement is filed as
`eval/tasks/EVAL-005-RESOURCES-REQUEST.md`.

**This does not block a run.** A run at 53 words is possible and reports 7.8%.

No other blocker. Five defects were found and fixed during the work; each is pinned by a test.

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
- **How many distinct Hindi words Resources can actually supply.** 119 EVAL-003 transcriptions were
  enumerated but never committed; their distinct-word yield is unknown and Eval cannot see the
  git-ignored raw tree.
- **Real per-call pricing.** The cost estimate rests on an old recorded figure.
- **Whether the proposed thresholds are right.** 0.95 repeat consistency, ≤10% false fail, ≤5%
  refusal have no empirical backing in this repository.

---

## CORRECTIONS MADE AFTER CONTROLLER REVIEW

| # | Required fix | What changed | Pinned by |
|---|---|---|---|
| 1 | Remove target leakage from `transcribe` | New `checker_input.py`: separate per-shape projections; allow-list that fails closed; `verify_blind()` rejects any Devanagari in a blind payload; `write_checker_inputs()` refuses to write a failing file; evaluator-side `scoring-key.jsonl` kept separate | 5 tests, incl. injecting a target as a field **and** smuggling one into the prompt |
| 2 | Pin shaping and rendering to one font | `hb-view` replaces `pango-view`; same font **file** + `--face-index` as `hb-shape`; `FontMissing` on a missing font, no fallback; provenance records font sha256, tool versions, size, margin, colours; portability claims corrected; **no font binary committed** | 4 tests, incl. a `subprocess` spy asserting both commands carry the same file, and a check that no font is in `git ls-files` |
| 3 | Verify visible difference on final pixels | Gate is now the final PNG bytes; reasons `canonical_equal` / `raster_identical` / `rendering_error`; glyph comparison retained as a diagnostic and recorded on rejections; screening renders to a process-lifetime scratch dir deleted on exit | 5 tests, incl. the nukta pair, the ZWNJ pair, and सुबह/सुवह accepted |
| 4 | Make normalisation semantics true | `nfc()` is NFC only; `strip_outer_whitespace()` is a separate named transport rule (ingest + response parsing); `canonical_equal()` is the predicate and does not strip; docs say *canonical* exactness, not codepoint identity | 3 tests, incl. internal whitespace being a real difference |
| 5 | Fix the independence claim | One mismatch item per distinct base word; deterministic maximum bipartite matching preserves all 20 classes; both counts reported; bound derived from the opportunity count; sample-size target recomputed; epistemic limit stored **in the build summary**, not only in prose | 5 tests, incl. `hard_items == distinct_hard_base_words` and the bound being derived |
| 6 | Qualification / repeat logic | Screening pass produces **no status**; any checker given a status completes ≥3 full passes in both shapes itself; "screened, not qualified" is an explicit outcome; gates 1 and 2 merged into one rule with the hard stratum named as the primary disqualifying subset and the bound-bearing one; thresholds marked proposed; cost estimate raised accordingly | doc-level |
| 7 | Formalise and prepare | `eval/tasks/EVAL-005.md`; `make_validation_sheets.py` + `native-validation/` with 53/25/20 blank rows and stable ids; `EVAL-005-RESOURCES-REQUEST.md`; findings, HANDOFF and this brief updated; inherited `PROPOSED-*` files kept and banner-marked superseded | 1 test (sheets exist, ids stable) |

**Additional defect found while fixing #3, not in the required list:** the plausibility rule let two
shaper-invalid strings into the hard stratum. Now decided by the shaper's dotted circle plus a
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

**One request to Resources**, `eval/tasks/EVAL-005-RESOURCES-REQUEST.md`: ~31–37 additional distinct
Hindi lexical items, as plain text strings — no images, no transcriptions, no new corpus. Optional;
it moves the bound from 7.8% to below 5% and does not block a run.

**No Resources or Canon file was edited.** Resources PR #5 was **open, not merged**; nothing here
depends on it, and if it merges its records should be checked against the request first.

## ARCHITECTURAL IMPLICATIONS

None. No battery dimension, ladder, pass criterion, observation-unit term or Registry field is
changed. `coordination/WORKSTREAM-STATUS.md` was **not** edited — a proposed replacement row is
below.

---

## PROPOSED REPLACEMENT ROW FOR `coordination/WORKSTREAM-STATUS.md`

*Controller-owned file; offered, not applied.*

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Eval | **EVAL-004 remains stopped. EVAL-005 opened as design hardening only and is complete, awaiting review.** A constructed-Devanagari exactness battery exists, is tested locally, and **has not been run**; no checker is qualified. | EVAL-005 design hardening on `work/eval-005-controller-review`. | Controller decisions on: (a) approve/reject the hardened design; (b) ~1.5 h of one Hindi reader; (c) checker roster + API budget; (d) whether to ask Resources for ~31–37 more Hindi words to move the bound from 7.8% to <5%; (e) the proposed qualification thresholds. No run without all of (a)–(c). |

---

## FRESH VERIFICATION — commands, exit codes, results

Run on `work/eval-005-controller-review` after `rm -rf build __pycache__`. The prior session's
claim that its tests passed was **not** relied on; the inherited suite was also re-run first and did
pass (36 checks) before being replaced.

```
$ python3 build_items.py --total 120
exit 0 — 106 items (53 match / 53 mismatch), 53 base words, 20 classes,
         37 hard / 37 distinct hard base words, bound 0.0778,
         screened 1834 valid, rejected {'canonical_equal': 2}

$ python3 test_devanagari_exactness.py
exit 0 — ALL CHECKS PASSED
         121 checks across 37 test functions, 0 failures

$ python3 make_validation_sheets.py --from-build build
exit 0 — word-validation-sheet.csv 53 rows · perceptibility-sheet.csv 25 rows
         · rendering-sanity-sheet.csv 20 rows · every answer column blank

$ python3 build_items.py --total 120 --out-dir <tmp>   # determinism
   both items.jsonl sha256 = 8572ef1cdb97322d31d9f88a0234cdd903905888f312bf6411559ff359f471f5

$ verify_blind on both written checker-input files
   transcribe  n=106  violations=0
   verdict     n=106  violations=0
```

### Environment and rendering provenance

| | |
|---|---|
| Python | 3.14.6 (`/opt/homebrew/bin/python3`) |
| Shaper | `hb-shape (HarfBuzz) 14.2.1` |
| Renderer | `hb-view (HarfBuzz) 14.2.1` — same library, takes a font file, no fontconfig |
| Font file | `/System/Library/Fonts/Kohinoor.ttc`, face index 0 |
| **Font SHA-256** | `8b508b160d4573963c064e951af48c33c6381901253ec6ae0feb86d80fde1f31` |
| Font size on disk | 1,397,704 bytes (5-face collection) |
| Point size / margin | 40 / 24 |
| Background / foreground | `FFFFFF` / `000000` |
| Font committed to repo | **No.** Proprietary system asset; identity pinned by hash instead. |
| Platform | macOS (Darwin 23.6.0), Apple silicon |

`pango-view` is no longer used anywhere; a test asserts it.

---

## EVIDENCE WORTH HUMAN INSPECTION

- **`eval/battery/devanagari-exactness/build/images/`** — the rendered items, after
  `python3 build_items.py --total 120`. Worth looking at three or four; it is the whole design in
  one glance.
- **`build/checker-input-transcribe.jsonl` next to `build/checker-input-verdict.jsonl`** — the
  clearest demonstration that the two shapes are genuinely different experiments. The first
  contains no Devanagari at all.
- **`eval/battery/devanagari-exactness/native-validation/`** — exactly what a reader would be asked,
  and how little of it there is.
- **`GENERATED-GLYPH-STRESS-LAYER.md`** — what this battery deliberately **cannot** test, and why
  that boundary is stated rather than blurred.

## FILES CHANGED

**New:** `eval/tasks/EVAL-005.md`, `eval/tasks/EVAL-005-CONTROLLER-BRIEF.md`,
`eval/tasks/EVAL-005-RESOURCES-REQUEST.md`,
`eval/battery/devanagari-exactness/{checker_input.py, make_validation_sheets.py}`,
`eval/battery/devanagari-exactness/native-validation/{README.md, word-validation-sheet.csv, perceptibility-sheet.csv, rendering-sanity-sheet.csv}`.

**Modified:** `eval/battery/devanagari-exactness/{devtext.py, perturb.py, build_items.py,
test_devanagari_exactness.py, README.md, CHECKER-CONTRACT.md, METRICS-AND-QUALIFICATION.md,
FAILURE-TAXONOMY.md, NATIVE-VALIDATION.md}`,
`eval/findings/devanagari-exactness-design-findings.md`, `eval/HANDOFF.md`.

**Banner-marked superseded, otherwise unedited:**
`eval/tasks/PROPOSED-EVAL-005-CONTROLLER-BRIEF.md`,
`eval/battery/devanagari-exactness/PROPOSED-TASK-SPEC.md`.

**Untouched:** every EVAL-001/002/003 artifact, every EVAL-004 record, all Canon files, all
Resources files, `coordination/WORKSTREAM-STATUS.md`, BSTD, the Marathi reserve, and the
`work/eval-005` branch itself.

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
4. **Decide whether to ask Resources for ~31–37 more Hindi words.** Optional. It is the difference
   between a 7.8% and a sub-5% ceiling. Resources may already hold them uncommitted — 119 EVAL-003
   transcriptions were enumerated and never committed — so the first step is a check, not a
   download.
5. **Approve or amend the proposed qualification thresholds** — 0.95 repeat consistency, ≤10% false
   fail, ≤5% refusal. They are judgement calls with no empirical backing in this repository, and
   they should probably be revisited once we have seen what real checkers do.
6. **Decide separately on the Class B generated-glyph layer.** Specified, not built, needs
   generation spend.
7. **Note before any result exists** that a pass is a qualification at a stated bound on this
   battery's material — never an accuracy claim, never a universal error rate, and silent about
   malformed generated glyphs.

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

No paid checker call. No free checker call. No model API call of any kind. No image or video
generation. No network request to any model. No human specialist time consumed — every answer column
in every prepared sheet is blank. No Capability Registry entry. No BSTD or Marathi reserve use.
EVAL-004 not resumed, its Reader-A pilot not promoted to ground truth, and no checker qualified,
disqualified or ranked from it or from anything else.
