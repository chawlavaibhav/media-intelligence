# Controller — CANON-GATE-001 Fourth-Check Disposition — 2026-09-04

**Status:** APPROVED CONTROLLER RULING; one further single-scope fix pass is authorised (M-01 and
M-02), followed by a bounded checker pass and then merge.
**Role:** Writer Controller.
**Applies to:** `work/canon-gate-001` at `d3f5948` (L-01 fix) and the checker's fourth-pass report
on it (verdict: **PASS WITH NON-BLOCKING NOTES**, findings M-01..M-06).
**Parent authority:** `CONTROLLER-CANON-GATE-001-BUILD-AUTHORISATION-2026-09-03.md` and Rulings 1–7.

The fourth pass confirmed every Ruling 7 condition met (condition 3 with the caveat below), the ten
anchors byte-identical across three independent runs, the 84-package extraction diff reproduced
file-for-file, and the deferred register untouched. It returned the merge-trigger verdict under
Ruling 7 and, in the same report, handed one question back to the Controller: a pre-existing
silent false-PASS path in the quote-pairing mechanism (M-01). The Controller was offered "merge
now" and "fix first"; the selection is recorded as chosen.

## Ruling 8 — fix M-01 and M-02 first, then merge

Controller selected: **"Fix M-01 + M-02 first, then merge."**

The Controller's standard from Ruling 6 condition 3 — a silent false PASS on a blocking row is
not acceptable — is read as a merge bar for a *known* path, whether or not the path is a
regression of the current fix or occurs in committed evidence.

### In scope

**M-01 (High).** `canon/gate/package.py:207-214` (nested opener `continue`) and `:198` (orphan
closer skipped). A legitimate inner straight-quoted string inside a prompt closes the run at the
inner closer; the remainder of the prompt is never scanned; `LIMIT-TEXT` PASSes. Observed:
`… the "Aster Meridian" on her wrist, chat bubbles and a notification counter on screen"` → one
prompt ending at `"Aster Meridian`, PASS; the same followed by another prompt → PASS with the
tail lost; `she holds "₹9" and "₹99" in gold, chat bubbles …` → PASS. Pre-existing in every
generation; absent from all 84 committed packages. Remedy named by the checker: a nested opener
inside an open run sets the same doubt state a digit-preceded quote does, never a silent close.

**M-02 (Medium, test gap).** `package.py:216-221`, the second raise (`doubt is not None and
could_open and not definite`) is unpinned — mutation M-F disabling it passes the whole suite; it is
the only thing converting the symbol-initial price shape `"₹9" and "₹99" and "₹999" in gold, chat
bubbles …` from a false PASS into ERROR. Remedy: one battery row and one package test with a
symbol-initial string after a doubt point asserting ERROR.

Binding conditions:

1. **Fail closed, never guess.** The only forbidden outcome remains PASS over unscanned text. An
   inner quoted string that cannot be disambiguated ends in ERROR ("unbalanced quotes"), not a
   truncated prompt. Where the design can legitimately keep a prompt whole (the inner string is
   provably nested), it may; where it cannot, it errors.
2. **Pinned both ways.** Each of the checker's M-01 shapes (A1, A2, A3, the symbol-initial variant)
   and the M-02 shape becomes a package-level test and a battery row asserting ERROR-or-FAIL and
   never PASS; the K-05, F-12, K-02 and L-01 fixtures and the six tails remain at their pinned
   outcomes. Mutation "nested opener closes silently" must be caught.
3. **84-package extraction diff re-derived** before and after (as in Ruling 7 condition 4); the
   four anchors sha-identical; every changed file listed with old→new; none → PASS.
4. **No vocabulary constant, no negation rule, nothing under `textscan.py`** changes. M-03, M-05,
   M-06 and everything deferred by Ruling 7 stay untouched and are added to the CANON-GATE-002
   register below.
5. Rulings 5–7 conditions stand.

### Deferred to CANON-GATE-002 (appended to the Ruling 7 register)

| id | Substance |
|---|---|
| M-03 | K-05 "definite closer" set closes a run mid-prompt on `)` `,` `]` `;` `:` after a digit (`a small (6") panel showing chat bubbles …` → truncated → PASS). Pre-existing; same family as M-01. |
| M-04 | Ruling 7 condition 3(b) wording ("extract the dirty prompt and FAIL") cannot be met without guessing a closer; behaviour pinned as ERROR. Record: the condition text is amended to "never PASS". |
| M-05 | Over-strict ERRORs: short quoted labels in prose after a well-formed prompt error the section (two committed Sonnet B02 packages lose a real scan; verdict unchanged); tab after a digit closer; multi-line prompt with inner line-start quote. All fail-closed. Pairing tuning. |
| M-06 | Cosmetic: test placement; `nxt in ")],;:"` true on EOF by substring semantics. |

## Sequence

maker fix pass (M-01 + M-02 only) → **bounded checker pass five**: this ruling's conditions 1–4,
the ten anchors, the battery, the 84-package diff, a mutation check that a silently closing
nested opener is caught, and a regression sweep of the fourth checker's attack table — nothing
wider → **Controller merges** on PASS or PASS WITH NON-BLOCKING NOTES **provided no finding is a
known PASS-over-unscanned-text path**, by merge commit, never squash or rebase. A BLOCK, or any
newly reported false-PASS path, returns to the Controller.

## Not authorised by this decision

Any spend, provider call or media generation; any change beyond M-01/M-02; any change under
`coordination/`, `eval/`, `canon/compilation/`, `canon/knowledge/`, `canon/audit/`, `canon/packs/`,
`canon/gate/textscan.py`, `canon/gate/vocab.py` or the plan; any conclusion about whether Canon
works.
