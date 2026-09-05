# Controller — CANON-GATE-001 Seventh-Check Disposition — 2026-09-05

**Status:** APPROVED CONTROLLER RULING; one post-parse fail-closed rule is authorised, followed by a
bounded checker pass and then merge.
**Role:** Writer Controller.
**Applies to:** `work/canon-gate-001` at `38f4295` (Ruling 10 curly removal) and the checker's
seventh-pass report on it (verdict: **PASS on every Ruling 10 condition; BLOCK on the merge line
only**; findings Q-01..Q-04).
**Parent authority:** `CONTROLLER-CANON-GATE-001-BUILD-AUTHORISATION-2026-09-03.md` and Rulings 1–10.

The seventh pass confirmed Ruling 10 executed exactly as ruled and refutation-proof for the curly
mechanism: the invariant is an honest oracle, the flipped pins name their true prior outcomes, the
cross-battery isolates exactly the curly rows, and nothing in 84 packages, ten anchors, 243 gen3
rows or 119 prior hunt rows moved anywhere but toward ERROR. It blocked on one path in a **third**
mechanism — the section parser. The Controller was offered two options and selected one; the
selection is recorded as chosen.

## The finding

**Q-01 (High).** `canon/gate/package.py:58` (`SECTION_RE`) and `:125-133` (`parse_package`). A
bare ALL-CAPS line of four or more characters between two straight-quoted prompts inside
`GENERATION_PROMPTS` matches the section-heading regex and opens a new section; the second,
text-bearing prompt is assigned to that section, never extracted, never scanned; `LIMIT-TEXT`
PASS on the first prompt alone; `GATE PASS`. Observed with `IMPORTANT`, `VIDEO`, `NOTE:`,
`### PROMPT_B`, and a dirty `>` blockquote after `NOTES`. Pre-existing in every generation. The
regex is pinned by the plan (§B `package.py` row) to equal
`eval/experiments/EVAL-038/tools/strip_blind.py::SECTION_RE` for parity with the blinding tool,
and tested as such. Across all 84 committed packages every heading is a genuine schema section;
zero bare ALL-CAPS lines occur inside any `GENERATION_PROMPTS`.

Borderline shapes the checker filed under the already-deferred P-06 class but flagged for the
Controller: a straight quote glued to a digit on both ends (`Shot 1"…99"`, both read as inch marks
under the F-12 rule Ruling 7 pins, so the span between is prose); a CommonMark lazy-continuation
line after a `>` line. Both recorded on the CANON-GATE-002 register below.

## Ruling 11 — fail closed on unknown headings after the prompts section opens, then merge

Controller selected: **"Fail closed on unknown headings, then merge."**

Parsing is not changed — the plan's parity with the blinding tool stands. The rule is
**post-parse**: it inspects the parsed section list and refuses a package whose structure the
gate does not recognise, exactly where that structure could have hidden a prompt.

### In scope

**One rule.** After `parse_package`, if any section heading that is **not in the known schema
set** appears **after** `GENERATION_PROMPTS` has opened, extraction is an ERROR
("unrecognised section heading after GENERATION_PROMPTS — prompts may be hidden; not scanned"),
naming the heading. `check_limit_text` reports ERROR with the reason; verdict FAIL.

The **known schema set** is derived mechanically, not hand-typed: the union of every section
heading that `parse_package` yields over the 84 committed EVAL-038 packages (`baseline/`,
`runs/*/packages/`, `judging/packages/**`), computed by a scratch script and then committed as a
frozen constant in `package.py` with the script's output reproduced in a test that recomputes the
union and asserts equality. Zero corpus change is therefore guaranteed by construction. Any
heading outside that set, after the prompts section opens, is unknown.

Binding conditions:

1. **Parsing untouched.** `SECTION_RE` and `parse_package` are byte-identical to `38f4295`; the
   parity test with `strip_blind.py` stays green.
2. **Rule placement.** The check runs in `extract_prompts` (or its caller) before pairing, on the
   parsed section order; it raises an `ExtractionError` subclass. Headings *before*
   `GENERATION_PROMPTS` opens are not affected. A second `GENERATION_PROMPTS` heading remains
   whatever the parser makes of it today (the checker found it merges — record in the test).
3. **Pinned both ways.** Q-01's shapes (`IMPORTANT`, `VIDEO`, `NOTE:`, `### PROMPT_B`, `NOTES` +
   dirty blockquote) become package tests and battery rows asserting ERROR. Counter-pins: every
   known heading after `GENERATION_PROMPTS` in the four anchors still parses and extracts
   identically; a package whose only unknown heading is *before* `GENERATION_PROMPTS` still
   extracts. The frozen known-set constant is asserted equal to the recomputed union.
4. **84-package extraction diff** re-derived before (`38f4295`) and after: **0 changed** by
   construction; the maker proves it; the four anchors sha-identical.
5. **Invariant extended.** `N01NoSilentDiscardInvariantTest` gains the branch: unknown heading
   after the prompts section ⇒ raises; asserted exercised.
6. **No vocabulary constant, no negation rule, nothing under `textscan.py` or `vocab.py`, no
   change to `SECTION_RE`.** Q-02, Q-03, Q-04 and the two borderline shapes are appended to the
   register untouched.
7. Rulings 5–10 stand: test-first; stdlib; boundaries; one or two commits; trailer; no push, no
   merge; `eval/` clean.

### Appended to the CANON-GATE-002 register

| id | Substance |
|---|---|
| Q-02 | OPENONLY mutation (detect `“` only) caught by package tests, no battery flip; NOCURLY does not flip the C-shape rows (they error for a different reason). Pin-strength note. |
| Q-03 | `check_limit_text` docstring omits the Ruling 10 error class. Cosmetic. |
| Q-04 | A curly quote inside a `>` blockquote line errors (whole-section check). Over-strict by design. |
| Digit-glued quotes | `Shot 1"{DIRTY}99"` — both quotes digit-preceded, both inch marks under F-12; span unscanned. P-06 class by the gate's ruled definition of a run; flagged. |
| Lazy continuation | A CommonMark lazy-continuation line after a `>` line is blockquoted under CommonMark but not a `>` line under the plan's definition. P-06 class; flagged. |
| Root cause | Three mechanisms (pairing, curly, section parser) have each yielded a PASS-over-unscanned path because the gate extracts prompts from free prose. GATE-002's first design item stands: an unambiguous prompt boundary in the production blueprint schema (Ruling 3) so extraction is a lookup, not a guess. |

## Sequence

maker fix pass (the post-parse rule + frozen known set) → **bounded checker pass eight**: conditions
1–5 and 7, the ten anchors, the battery, the 84-package diff, the seventh checker's hunt tables
re-run (every PASS row classified as correct-whole-prompt / ruled-deferred by name / NEW), and the
two-heading merge line ("not already ruled deferred" / "ruled-deferred observed") → **Controller
merges** on PASS or PASS WITH NON-BLOCKING NOTES with the first heading reading **none**, by
merge commit, never squash or rebase. Anything else returns to the Controller.

## Not authorised by this decision

Any spend, provider call or media generation; any change beyond the one rule, the frozen known
set, its pins and the invariant branch; any change to `SECTION_RE` or `parse_package`; any change
under `coordination/`, `eval/`, `canon/compilation/`, `canon/knowledge/`, `canon/audit/`,
`canon/packs/`, `canon/gate/textscan.py`, `canon/gate/vocab.py` or the plan; any conclusion about
whether Canon works.
