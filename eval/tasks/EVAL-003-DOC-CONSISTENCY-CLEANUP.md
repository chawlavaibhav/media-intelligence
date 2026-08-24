# EVAL-003 — final documentation consistency cleanup

**Status:** Controller-approved bounded cleanup · 24 Aug 2026  
**Task identity:** remains **EVAL-003**; this does not open EVAL-004  
**Spend:** ₹0 / $0 API · 0 human specialist hours · 0 generations · 0 acquisition

## Controller assessment

The finalization return is substantively successful. The Hindi-primary pack exists and is mechanically coherent; the matcher regression exists; the two-reader protocol and altered-target rule are corrected; crop identity is materialised and hashed; the Eval→Resources proposal contains all three required reconciliation points; no human/API/model/generator work has begun.

**Do not reopen any of those decisions.**

The return is not merge-ready for one bounded reason: several active operator-facing documents still contain pre-finalization statements that contradict the committed Hindi-primary/materialised-crop state. The Controller Brief says these contradictions were removed, but they remain followable in current files.

## Required cleanup

### 1. `eval/findings/EVAL-003-calibration-readiness-findings.md`
Rewrite the active current-state sections so they describe the committed V0 configuration, while preserving the old state only in clearly historical/correction text.

At minimum fix:
- §5 still presents `551 - 346 - 3 = 202` / overlap-excluded pool as the current candidate pool. Current primary V0 is `admit-once + hindi`, **173 eligible / 54 selected / 54 Hindi**.
- §5 says no excluded overlap file entered the pool. Current V0 deliberately admits each shared photograph **once**.
- §8 says no images are copied/transformed and browser display crops the originals. Current V0 uses **materialised canonical crop files** for both reviewer and checker.
- §9 says crop materialisation is unresolved. It is solved and verified.
- §10/current stop-condition prose must not describe the old 202-item/zero-Hindi configuration as current.
- Any `53 Marathi + 1 unlabelled + 0 Hindi` statement may remain only when explicitly labelled as the **superseded pre-finalization configuration**.

### 2. `eval/calibration/devanagari-v0/README.md`
Make this file safe for a fresh operator to follow without rebuilding the wrong pack.

At minimum fix:
- `PROPOSED-V0-COMPOSITION.md` is no longer awaiting a Controller decision; it is a retained decision record.
- The primary reproduction command must include the committed V0 arguments: `--overlap-policy admit-once --language-filter hindi --target-n 54`. If generic/default reproduction is also shown, clearly distinguish it from the committed primary V0 build.
- Remove/update stale statements that `202 eligible is ample`, explain “why exclude the 173”, or say the current pool includes Marathi-labelled files.
- Rewrite the stale “53 of 54 / after removing overlap only 3 IIIT items remain” current-pool description. For the approved V0, shared photos are admitted once and deterministically attributed; dataset-name counts are provenance, not independent-source evidence.
- Recompute any difficulty/coverage numbers that were copied from the old pack (region-area range, frame-share range, regions-per-photo, conjunct/matra/nukta counts). Do not retain old-pack metrics as current unless mechanically verified against the current 54.
- Wherever code defaults remain `exclude`, say explicitly that this is a **generic default**, not the committed V0 configuration.

### 3. `eval/calibration/devanagari-v0/annotator-disagreement.json`
The current note says the 173 shared files are excluded from the candidate pool. That is false for the committed primary V0. Change it to distinguish:
- the **superseded `exclude` configuration**, which excluded them; from
- the **approved Hindi-primary `admit-once` configuration**, which admits each shared photograph once.

Do not change the disagreement measurements.

### 4. `eval/calibration/devanagari-v0/PROPOSED-V0-COMPOSITION.md`
The header correctly says the decision is made, but later prose still says “Controller decision”, recommends Option C, and says nothing has been switched. Preserve the options as historical reasoning, but mark the recommendation section explicitly **superseded by the Controller decision above** or rewrite it as historical. A fresh reader must not infer the language split is still open.

### 5. `eval/calibration/devanagari-v0/build-candidate-pool.py`
Documentation/help text only unless a real bug is found.
- The module-level guarantees currently say cross-source-identical files are excluded entirely. Update this to describe both overlap policies and identify the committed V0 configuration separately.
- The `--overlap-policy` help still calls `admit-once` “PROPOSAL ONLY”. Controller approval now exists. Keep the generic default if desired, but remove the obsolete “proposal only” wording and state that primary V0 explicitly invokes `admit-once`.

Do **not** change the matching rule, sample-selection algorithm, source set, target count, language decision, crop implementation, checker semantics, or human protocol in this cleanup.

### 6. `eval/tasks/EVAL-003-CONTROLLER-BRIEF.md`
Keep the good finalization section, but reconcile later stale decision text:
- language composition is **already decided**;
- do not recommend C or ask the Controller to choose A/B/C;
- human reader approval and later checker roster/API spend remain future Controller decisions;
- status should say finalization completed and this documentation cleanup applied, then awaiting Controller merge review.

### 7. Sweep other current EVAL-003 operator-facing files
Search current EVAL-003 files for stale variants of:
- `202 eligible` as current primary pool;
- `53 Marathi`, `0 Hindi` as current primary pool;
- `crops ... not materialised`, `browser crops`, `no images are copied`;
- `composition ... needs Controller decision`;
- `admit-once ... proposal only`;
- an instruction to exclude all shared photographs in the committed primary V0;
- machine-specific absolute paths.

Historical/correction text may retain old numbers only when unmistakably labelled as historical/superseded.

## Verification before return

No need to rerun API/model/human work. Re-run only local/mechanical checks needed to ensure documentation matches the existing committed artifacts:

- `selection-summary.json` still reports **173 eligible Hindi / 54 selected Hindi**;
- candidate manifest still has 54 records and 54 distinct image hashes;
- review/checker crop identity remains 54/54;
- matcher `--self-test` still passes;
- 27 historical checker regression remains 0 mismatches if any code text change touches executable content; otherwise record not rerun because executable semantics were unchanged;
- no absolute machine paths;
- no human/API/model/generator work;
- BSTD untouched.

Update the Controller Brief with the cleanup result, commit/push `work/eval`, and STOP.

**Do not start human review, API checker qualification, EVAL-004, Registry work, or any new research.**
