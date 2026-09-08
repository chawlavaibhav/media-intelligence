# Controller — CANON-GATE-001 Third-Check Disposition — 2026-09-04

**Status:** APPROVED CONTROLLER RULING; a third, single-finding fix pass is authorised, followed by
a bounded checker pass and then merge.
**Role:** Writer Controller.
**Applies to:** `work/canon-gate-001` at `d4ddef4` (second fix pass, six commits) and the checker's
third-pass report on it (verdict: **BLOCK**, findings L-01..L-07).
**Parent authority:** `CONTROLLER-CANON-GATE-001-BUILD-AUTHORISATION-2026-09-03.md` and the three
prior dispositions (Rulings 1–6).

The checker confirmed K-01..K-06 resolved as ruled (K-05 partially), all ten anchors byte-identical
to pass two, the regression battery mechanically diffable, and twenty of twenty-one deliberate
code mutations caught by the new tests. It blocked on one finding the K-05 fix introduced. The
Controller was offered three options and selected one; the selection is recorded as chosen.

## Ruling 7 — fix L-01 only, then merge

Controller selected: **"Fix L-01 only, then merge."**

### In scope: L-01 (High, blocking)

`canon/gate/package.py:176`. The K-05 inch-mark rule decides whether a digit-preceded `"` inside
an open run is a closer by inspecting what follows it. A genuine closer followed by a space and
prose (` (8 s)`, ` — 4 s`, ` | 4 s |`, `. Then …`, ` then …`) is swallowed as an inch mark; the run
stays open; the prompt is dropped or a phantom prompt is manufactured, and `LIMIT-TEXT` reports
PASS over text that was never scanned. Demonstrated on the committed package
`eval/experiments/EVAL-038/runs/gemma-packs/packages/E038-gemma-packs-B02-R1.txt` (a poster plan
requesting rendered prices: `"₹9" (massive, bold …) … "₹99" (massive …)`), which both prior
generations failed closed (extraction ERROR) and which now exits **GATE PASS**.

Binding conditions on the fix:

1. **Fail closed on imbalance.** A quote run still open at the end of `GENERATION_PROMPTS` is an
   extraction error (`LIMIT-TEXT` → `ERROR`, reason "unbalanced quotes"; verdict FAIL). The gate
   never guesses a closer.
2. **The K-05 fixtures still hold** (`6" OLED panel showing chat bubbles…`,
   `is 6". It shows chat bubbles…` extract whole and FAIL `LIMIT-TEXT`), and F-12's before-prompt
   inch mark still does not shift pairing.
3. **Pinned both ways:** the `"₹9" (massive…)` idiom from the committed Gemma B02-R1 package (read
   in place) must not exit PASS; the six tail shapes the checker listed
   (` (8 s)`, ` — 4 s`, ` | 4 s |`, `. Then …`, ` 8 s`, ` then …`) after a digit-ending closer must
   each extract the dirty prompt and FAIL `LIMIT-TEXT`; the end-of-line closer must still close.
4. **All 84 committed EVAL-038 packages** are run through extraction before and after; any file
   whose extraction changes is listed in the report with old and new prompt counts. The four
   anchors must remain sha-identical.
5. Every condition of Rulings 5 and 6 stands (CHANGELOG where a vocabulary constant changes;
   boundaries; no file outside `canon/gate/*.py` and `tests/test_gate_*.py`).

### Deferred to a follow-up task (not in scope; recorded, not fixed)

| id | Substance | Owner action |
|---|---|---|
| L-02 | CA-D2 clause-2 negation is bounded by token count (6), not governance; "No hard shadows, dial on the rule of thirds line." passes. Remedy identified: apply the existing `GOVERNANCE_BREAK` rule to CA-D2. | Controller ruling on window semantics, then maker |
| L-03 | `and`/`or` in `GOVERNANCE_STOP_WORDS` make coordinated negation over-fire on T3 ("no chat bubbles or notifications" blocks). Fails closed. Unrecorded, unpinned (mutation M21 survives). | Record + pin |
| L-04 | Dial-numeral exemption masks text-bearing dial copy ("the dial reads ASTER in applied numerals" clears). Silent false PASS. Unrecorded, unpinned. | Record + pin |
| L-05, L-06, L-07 | Pre-existing disclaimer forms outside `NEGATED_AFTER`; bare-modifier gaps; one in-battery sentence copy | Notes |
| K-07..K-10 | Clock-time residual; PA-D10 lead-in without colon; unpinned recorded misses; EXTRACTION-RECORD no longer checked in the gate suite | Notes |
| F-02/F-03 residuals | Recorded misses and over-fires in `vocab.CHANGELOG` | Vocabulary tuning with a fixture corpus |

These are the opening register of **CANON-GATE-002 (vocabulary and negation semantics)**, to be
authorised separately. Nothing here is fixed by this ruling.

## Sequence

maker fix pass (L-01 only) → **bounded checker pass four**: L-01 conditions 1–4, the ten anchors,
the 103-row battery, the 84-package extraction diff, and a regression sweep of the previous
checker's table — nothing wider → **Controller merges** on a checker PASS or PASS WITH
NON-BLOCKING NOTES, by merge commit, never squash or rebase. A BLOCK returns to the Controller.
The Controller's selection "then merge" is the merge authorisation, conditional on that checker
result; no agent approves its own work.

## Not authorised by this decision

Any spend, provider call or media generation; any change to L-02..L-07, K-07..K-10 or any
vocabulary constant not required by L-01; any change under `coordination/`, `eval/`,
`canon/compilation/`, `canon/knowledge/`, `canon/audit/`, `canon/packs/` or the plan; any
conclusion about whether Canon works.
