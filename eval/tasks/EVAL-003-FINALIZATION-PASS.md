# EVAL-003 — Controller finalization pass

**Status:** Controller-approved bounded finalization · 24 Aug 2026  
**Task identity:** remains **EVAL-003**; this does not open EVAL-004  
**Autonomy:** autonomous only for the mechanical/protocol changes below  
**Spend:** ₹0 / $0 API · 0 human specialist hours · 0 generations · 0 acquisition

## Controller assessment of the correction return

The correction return fixed the important first-review problems: the cross-dataset disagreement is no longer presented as human performance; the matcher is now one-to-one; the Unicode mark-removal result is described mechanically; candidate arithmetic is stated in consistent units; crop materialisation now gives human readers and future checkers the same hashed pixels; machine-specific paths are removed; and the first-pass reference protocol now uses two independent readers.

Do **not** reopen those questions or redesign the battery. EVAL-003 is close to ready, but it is not yet merge-ready or approved for human/API calibration because the return has a small number of concrete remaining defects.

## 1. Synchronize the branch first

`work/eval` did not merge current `main` before the correction work. The Controller correction contract is therefore absent from the branch, and the branch is behind later Controller commits.

Before any other edit:

- fetch `origin/main`;
- merge current `origin/main` into `work/eval` normally;
- do not rebase, squash, force-push, or rewrite the EVAL-003 history;
- preserve the returned Eval work while accepting current Controller files as authoritative.

This is branch hygiene, not a reason to repeat the correction pass.

## 2. Add the missing adversarial regression for one-to-one matching

The corrected production matcher is one-to-one, but the Controller-required fabricated regression is not present in the returned builder/tests.

Refactor only as much as needed so the matching rule can be tested directly. Add a deterministic synthetic case where **two A regions both have IoU ≥ threshold with, and prefer, the same B region**. The test must prove that B is used at most once.

Do not use the real-corpus observation that no contested partners happened to occur as a substitute for this regression. The point of the test is to catch the bug on data where the bug actually matters.

If the findings keep the claim that `0 of 1,778` real regions were contested, make that count reproducible in committed code/metadata; otherwise remove the precise count and simply report that corrected and superseded totals happened to match.

## 3. Controller decision: make the primary V0 pack Hindi-focused

The correction pass discovered that the current `exclude` policy produces a 54-item pack with **0 Hindi** (53 Marathi + 1 language-unstated item), because all 173 Hindi-labelled IndicSTR12 records are in the cross-dataset overlap.

For the **primary V0 I1 qualification pack**, the Controller approves admitting shared photographs **once** and selecting **Hindi-labelled items only**.

### Required primary V0 composition

- target: **54 Hindi-labelled candidate photographs** if the 173 unique shared hashes can supply 54 valid candidates under the existing geometry/integrity rules;
- each image SHA-256 may appear **once only** in the pack;
- a photograph appearing in both CVIT releases is one item, never two independent items;
- attribute it deterministically to one source record for provenance, but do not treat the two dataset names as independent evidence;
- source transcriptions remain provenance/selection metadata only and stay hidden from first-pass readers and checkers;
- our two-reader protocol, not either source label, establishes the later reference;
- preserve BSTD untouched as the independent source-lineage reserve.

Why: the checker implementation and observed production failure are Hindi-facing. Spending the first human calibration budget on a pack with zero Hindi would create an avoidable transfer assumption. A Hindi-primary pack gives the narrow claim we actually need and keeps reviewer qualification simple. Do **not** claim the result automatically transfers to Marathi or all Devanagari-language use.

Keep `--overlap-policy` or equivalent generic machinery if useful, but make the **committed V0 manifest/run plan explicit about the approved Hindi-primary configuration**. Do not silently change unrelated generic defaults without recording it.

The previously proposed Marathi stress subset is **deferred**, not rejected. It may be useful later, but it is not part of the primary V0 human spend. If a future Marathi stress run is opened, its readers must have appropriate Marathi competence and its result must be reported separately.

After rebuilding, report exact language-label composition for **both the eligible Hindi-primary pool and the selected 54**, not only the selected set. If 54 valid Hindi candidates cannot be produced, STOP and report the exact shortfall rather than filling with Marathi silently.

## 4. Fix the impossible altered-target confirmation rule

The returned protocol says both readers independently transcribe every item, then says a broken target may not be checked by a reader who established that item's original reading. With two readers reading every item, that rule leaves **no eligible person** to perform stage 4 unless a third specialist is added.

Do not add a third reader or extra human budget in EVAL-003.

Correct the protocol as follows:

- both first-pass reader responses are frozen before intact/broken assignment;
- only items with the required agreed reference may enter the primary gate set;
- after freeze, **either one of the two readers may perform the short altered-target validity check** because that check cannot edit or replace the frozen reference;
- the checker's purpose is only to confirm that the proposed broken target is visibly different from the agreed reference/image; if there is doubt, drop/reclassify the item rather than changing the reference;
- record who performed the check;
- if a future Controller wants a third independent adjudicator, that is a separate human-time decision.

Update the run plan, human guide and human-time estimate consistently. The primary planned human team remains **two independent Hindi-competent readers**.

## 5. Make current-state documents internally consistent

The findings currently retain pre-correction statements such as crops being unmaterialised / browser-only while a later correction section says crop identity is solved. Historical trace is useful; contradictory current state is not.

Rewrite current sections so the active description is correct now. Keep the history in a clearly marked correction/revision section rather than leaving false statements in the main current-state narrative.

At minimum scan the current EVAL-003 artifacts for stale variants of:

- `crops were not materialised` / `crop materialisation unresolved`;
- `no images are copied or transformed` when canonical crops now exist locally;
- the old one-reader protocol;
- the impossible `not by the reader who read that item` rule;
- claims that the current primary V0 pack contains no Hindi after the Controller-approved rebuild;
- generic wording implying a Hindi reader is automatically competent for Marathi material.

Preserve evidence of what was corrected, but make it impossible for a later operator to follow an obsolete instruction by accident.

## 6. Complete the Eval → Resources proposal

`eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md` correctly covers the scene-photo-versus-word-crop discrepancy, but it does not yet include all three Controller-required reconciliation points.

Add, without editing Resources directly:

1. the existing full-scene / multiple-region correction;
2. the observed locally usable pairing counts: **375 IndicSTR12 + 176 IIIT-ILST image/annotation records**, and a request that Resources distinguish media acquired from locally paired image+annotation records where its wording could imply all acquired media has a locally usable transcription;
3. the denominator-specific overlap result: **173 of the 176 locally paired IIIT-ILST records** are byte-identical to an IndicSTR12 file, leaving 3 unique in that locally paired subset. State explicitly that this is a different denominator from Resources' full-source 12.4% duplicate figure, not a contradiction.

Do not ask Resources to change rights or reacquire anything.

## 7. Re-run only the bounded verification suite

Before return, verify and record fresh outputs for:

- candidate builder determinism for the approved Hindi-primary configuration;
- 54 selected items = 54 distinct hashes;
- selected language-label composition = 54 Hindi, or STOP with the evidenced shortfall;
- one-to-one adversarial synthetic regression;
- crop geometry self-test;
- crop count/hash identity between review pack and checker-item template;
- blind-pack scan;
- all 27 historical checker cases = 0 judgement mismatches;
- malformed per-item inputs rejected as before;
- no machine-specific absolute paths in current EVAL-003 committed evidence;
- BSTD reserve still untouched under the permitted metadata-only operations;
- no human/API/model/generator work performed.

## Return to Controller

Update `eval/tasks/EVAL-003-CONTROLLER-BRIEF.md` with a short finalization section stating:

- branch sync completed;
- adversarial matching regression added and result;
- final Hindi-primary eligible and selected counts;
- final reviewer qualification and human-time estimate;
- stage-4 rule corrected without a third reader;
- stale contradictions removed;
- Resources proposal completed;
- verification outputs and any remaining blocker.

Commit and push `work/eval`, then STOP. **Do not start human review, checker APIs, BSTD inspection/selection, EVAL-004, or any Registry work.**