# Controller — CANON-GATE-001 Fifth-Check Disposition — 2026-09-05

**Status:** APPROVED CONTROLLER RULING; one structural fix pass is authorised, followed by a bounded
checker pass and then merge.
**Role:** Writer Controller.
**Applies to:** `work/canon-gate-001` at `bbc1351` (M-01/M-02 fix) and the checker's fifth-pass
report on it (verdict: **BLOCK**; merge line: one known PASS-over-unscanned-text family, N-01).
**Parent authority:** `CONTROLLER-CANON-GATE-001-BUILD-AUTHORISATION-2026-09-03.md` and Rulings 1–8.

The fifth pass confirmed every Ruling 8 shape fixed and pinned, the ten anchors byte-identical, the
84-package diff at zero change, and nothing moved toward PASS across 28 + 243 + 126 + 119 rows.
It blocked on a path outside Ruling 8's named shapes but inside the same mechanism. The Controller
was offered three options and selected one; the selection is recorded as chosen.

## The finding

**N-01 (High).** `canon/gate/package.py:248-257` — a could-open quote followed by whitespace is
read as the run's closer (the maker's declared "class 3" guess) — together with
`package.py:267-268`, where `_quoted_runs` silently discards any run shorter than
`PROMPT_MIN_CHARS` (120). A straight-quoted string nested inside a prompt whose opener is
followed by whitespace (space, tab, NBSP or newline) closes the prompt at that opener; the
text-bearing remainder pairs into a sub-floor run that is dropped without trace; `LIMIT-TEXT`
PASS. Seven inputs demonstrated (K11, K11b, K11e, K11f, K12, K12b, K17), e.g.
`she holds " Aster " in gold, chat bubbles and a notification counter on screen`. Pre-existing
in every generation; absent from all 84 committed packages. The docstring's claim that class 3 is
"checked, not trusted" is refuted: what is left outside the run does pair, and the floor hides it.

This is the sixth edge found in the same pairing logic across five passes (F-12, K-02, K-05,
L-01, M-01, N-01). Each lexical patch was correct for its named shapes and surfaced the next.

## Ruling 9 — structural fix, then merge

Controller selected: **"Structural fix, then merge."**

The defect to remove is the **concealment mechanism**, not the trigger: content inside the
generation-prompts section must never be silently discarded. Once that holds, any pairing
mistake — present or future — can only fail closed.

### In scope

**One rule.** A quoted run inside `GENERATION_PROMPTS` that falls under the length floor is an
extraction **ERROR** ("quoted run below the prompt floor — not scanned"), never a silent drop.
`_quoted_runs` (or its caller) raises; `check_limit_text` reports ERROR with the reason; verdict
FAIL. The class-3 whitespace reading may stay as it is — its worst case is now an error, not a
pass.

Binding conditions:

1. **No silent discard.** After the change, every byte inside a straight-quoted run in
   `GENERATION_PROMPTS` is either scanned or the cause of an ERROR. The maker adds an invariant
   test: for any section, the concatenated extracted prompts plus the raised error account for
   every quoted run `_straight_runs` returns.
2. **The seven N-01 shapes and the N-05 short-prompt shape** (a stand-alone quoted prompt under
   120 chars, checker case K16) are pinned as package tests and battery rows asserting ERROR,
   never PASS. Every existing pin (K-05, F-12, K-02, L-01 six tails, M-01 A1/A2/A3, symbol-initial,
   M-02) stays at its outcome.
3. **84-package extraction diff re-derived** before (`bbc1351`) and after. Every changed file
   listed with old→new prompt count and `LIMIT-TEXT` status; the four anchors sha-identical; none
   → PASS. A currently FAIL file that becomes ERROR is acceptable and must be listed; the maker
   reads each such section and states whether a real prompt scan was lost (over-strict) or the
   old FAIL rested on a phantom (honest).
4. **The plan's floor semantics are amended on record, not silently.** Plan §B.1 / §F say
   "double-quoted runs ≥120 chars"; under this ruling runs under the floor are errors, not
   ignored. The maker records this in the `package.py` module docstring citing Ruling 9; the
   Controller amends the plan text separately.
5. **No vocabulary constant, no negation rule, nothing under `textscan.py` or `vocab.py`**
   changes. N-02 (over-strict doubt at depth 2), N-03 (orphan pin by message only), N-04, and all
   prior deferred items stay untouched and are appended to the CANON-GATE-002 register.
6. Rulings 5–8 stand: test-first; stdlib; boundaries; one commit or two; `Co-Authored-By`
   trailer; no push, no merge; `eval/` clean.

### Appended to the CANON-GATE-002 register

| id | Substance |
|---|---|
| N-02 | `doubt` set while `depth==2` makes the outer closer pop only to 1 → over-strict ERROR on `the "Aster 38" model, chat bubbles …` (was whole-prompt FAIL). Fail-closed. |
| N-03 | M-ORPH mutation caught only by a message-asserting test; no battery row flips. Weaker pin. |
| N-04 | Only the space-led M-02 row isolates the second raise. Note. |
| Pairing redesign | Six edges in one mechanism across five passes. GATE-002 should replace lexical closer-guessing with a fail-closed grammar (e.g. prompts must be delimited unambiguously in the production blueprint schema — Ruling 3 already controls that schema) rather than patch a seventh shape. |

## Sequence

maker structural fix → **bounded checker pass six**: conditions 1–5, the ten anchors, the battery,
the 84-package diff, the fifth checker's class-3 attack table re-run (every row must be FAIL,
ERROR or correct-whole-prompt; no PASS), and the single merge line "Known PASS-over-unscanned-text
paths found at HEAD: none | list" → **Controller merges** on PASS or PASS WITH NON-BLOCKING NOTES
with that line reading **none**, by merge commit, never squash or rebase. Anything else returns
to the Controller.

## Not authorised by this decision

Any spend, provider call or media generation; any change beyond the one rule and its tests; any
change under `coordination/`, `eval/`, `canon/compilation/`, `canon/knowledge/`, `canon/audit/`,
`canon/packs/`, `canon/gate/textscan.py`, `canon/gate/vocab.py` or the plan; any conclusion about
whether Canon works.
