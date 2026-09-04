# Controller — CANON-GATE-001 Sixth-Check Disposition — 2026-09-05

**Status:** APPROVED CONTROLLER RULING; one mechanism-removal fix pass is authorised, followed by a
bounded checker pass and then merge.
**Role:** Writer Controller.
**Applies to:** `work/canon-gate-001` at `02e50fa` (Ruling 9 structural fix, two commits) and the
checker's sixth-pass report on it (verdict: **BLOCK on the merge line only**; findings P-01..P-06).
**Parent authority:** `CONTROLLER-CANON-GATE-001-BUILD-AUTHORISATION-2026-09-03.md` and Rulings 1–9.

The sixth pass confirmed every Ruling 9 condition met for the straight-quote mechanism — the
floor no longer discards anything, the invariant test is a genuine oracle for straight runs and
fails on the exact mutation the ruling was written against, the 84-package diff and ten anchors
reproduce to the byte, and nothing moved toward PASS across every prior table. It blocked because
the merge-line hunt found a seventh edge in a **second, separate** mechanism. The Controller was
offered three options and selected one; the selection is recorded as chosen.

## The finding

**P-01 (High).** `canon/gate/package.py:318` pairs curly-quoted runs (`“ … ”`) with a bare regex
that has none of the three fail-closed rules `_straight_runs` now enforces (orphan closer raises;
unclosed run raises; nested opener raises depth). An unclosed curly prompt, a stray curly closer,
or a curly quote nested inside a curly prompt leaves the text-bearing remainder outside any run;
`LIMIT-TEXT` PASSes. Four shapes (C2, C3, C4, C4b). Pre-existing in every generation; 0 of 84
committed packages carry a curly quote inside `GENERATION_PROMPTS`. C4 (a curly run open at end
of section) is a literal violation of Ruling 7 condition 1 for the curly style; C2/C3 are the
curly twins of M-01.

## Ruling 10 — remove curly quotes as a prompt delimiter, then merge

Controller selected: **"Remove curly as a delimiter, then merge."**

The fix is the removal of a mechanism, not the tuning of one. The straight-quote pairer is the
only prompt delimiter; it is proven fail-closed under Ruling 9. A second pairer is a second
surface for the same family of defects and is not needed: production blueprints carry straight
quotes (the schema is under Ruling 3's control) and no committed package uses curly quotes in
the prompts section.

### In scope

**One rule.** Any curly double quote (`“` U+201C or `”` U+201D) inside `GENERATION_PROMPTS` is
an extraction **ERROR** ("curly quote in GENERATION_PROMPTS — straight quotes delimit prompts;
not scanned"). Curly runs are no longer extracted as prompts. The straight pairer, the floor rule,
containment as it applies among straight runs, and the blockquote path are unchanged.

Binding conditions:

1. **Fail closed, mechanism removed.** After the change, `_quoted_runs` yields straight runs only;
   `_straight_runs` is the sole pairer. The presence of `“` or `”` anywhere in the section raises
   before pairing. `ExtractionError` remains the common base; `check_limit_text` reports ERROR
   with the reason; verdict FAIL.
2. **The invariant test is made independent for the only remaining style.** The curly half of the
   Ruling 9 oracle (which reused the implementation's regex — P-02) is removed with the mechanism;
   the invariant asserts, for every section in its set, that a curly quote raises, and otherwise
   that every straight run is scanned or is the cause of an error. No third outcome.
3. **Pins.** P-01's four shapes (C2, C3, C4, C4b) become package tests and battery rows asserting
   ERROR. The existing curly fixtures — A4 (curly outer + inch mark), A5 (curly name inside a
   straight prompt), "straight-in-curly", "curly short" — flip from their current outcome to
   ERROR; the maker updates those pins and records the flip in each test's comment as the
   consequence of this ruling. Every straight-quote pin (K-05, F-12, K-02, L-01, M-01, M-02, the
   seven N-01 shapes, K16) stays at its outcome.
4. **84-package extraction diff** re-derived before (`02e50fa`) and after: expected **0 changed**
   (no committed package has a curly quote in the section); any change is listed and explained;
   the four anchors sha-identical.
5. **Recorded on the plan** by the Controller separately: `extract_prompts` reads straight
   double-quoted runs and `>` blockquote runs; a curly quote is an error.
6. **No vocabulary constant, no negation rule, nothing under `textscan.py` or `vocab.py`**
   changes. P-03 (NUL defeats sentence splitting — textscan), P-04 (weak pins), P-05 (empty
   `""` pair now errors), P-06 (unquoted markdown prompts are never scanned — plan-level) are
   appended to the CANON-GATE-002 register untouched.
7. Rulings 5–9 stand: test-first; stdlib; boundaries; one or two commits; trailer; no push, no
   merge; `eval/` clean.

### Appended to the CANON-GATE-002 register

| id | Substance |
|---|---|
| P-03 | A NUL after a full stop defeats `split_sentences`; a preceding "no text" clause then governs a later text-bearing phrase → PASS on scanned-but-misjudged text. `textscan`; beside L-02. |
| P-04 | Floor boundary (`<` vs `<=`) and curly-floor mutations caught by one assertion each, no battery flip. Weak pins. |
| P-05 | An empty `""` pair before a prompt now errors (was silently dropped). Fail-closed, over-strict; beside M-05. |
| P-06 | **Plan-level:** text in `GENERATION_PROMPTS` outside any quoted run or blockquote is never scanned. Fails closed only when *no* prompt extracts; a section with one quoted prompt and dirty prose around it PASSes on the prompt alone. Design gap accepted by every pass; the production blueprint schema (Ruling 3) should make the prompt boundary unambiguous so extraction is a lookup, not a guess. |

## Sequence

maker fix pass (curly removal) → **bounded checker pass seven**: conditions 1–4 and 6–7, the ten
anchors, the battery, the 84-package diff, the sixth checker's merge-line hunt table (41-row,
28-row, and the C-series) re-run with every row FAIL, ERROR or correct-whole-prompt, and the
single merge line → **Controller merges** on PASS or PASS WITH NON-BLOCKING NOTES with the merge
line reading **none**, by merge commit, never squash or rebase. Anything else returns to the
Controller.

## Not authorised by this decision

Any spend, provider call or media generation; any change beyond the one rule, its pins and the
invariant adjustment; any change under `coordination/`, `eval/`, `canon/compilation/`,
`canon/knowledge/`, `canon/audit/`, `canon/packs/`, `canon/gate/textscan.py`, `canon/gate/vocab.py`
or the plan; any conclusion about whether Canon works.
