# Controller — CANON-GATE-001 Eighth-Check Disposition — 2026-09-07

**Status:** APPROVED CONTROLLER RULING; one tightening of the Ruling 11 rule is authorised,
followed by a bounded checker pass and then merge.
**Role:** Writer Controller.
**Applies to:** `work/canon-gate-001` at `235b2a2` (Ruling 11 unknown-heading rule) and the checker's
eighth-pass report on it (verdict: **PASS WITH NON-BLOCKING NOTES**; merge line **none**; findings
R-01..R-05, with R-01 flagged NEW-CLASS on the deferred heading).
**Parent authority:** `CONTROLLER-CANON-GATE-001-BUILD-AUTHORISATION-2026-09-03.md` and Rulings 1–11.

The eighth pass met Ruling 11's merge condition: every condition in scope survived refutation, the
known set reproduced by two independent derivations, 27 heading variants and five line-separator
forms could not open a section the rule does not see, and nothing in 84 packages, ten anchors,
243 gen3 rows or four hunt tables moved anywhere but toward ERROR. The checker flagged one gap
between Ruling 11's stated principle and its stated operationalisation, and placed it on the
deferred heading because Ruling 11's own text makes a known heading a genuine section. The
Controller was offered "merge now" and "tighten first" and selected one; the selection is recorded
as chosen.

## The finding

**R-01 (Medium, NEW-CLASS).** `canon/gate/package.py:456-471` with the constant at `:84-107`. The
rule checks *membership* in the 15-heading union, not *structure*. A known heading reused as a
divider after `GENERATION_PROMPTS` hides a quoted prompt: a heading repeated
(`FAILURE_PREVENTION … "dirty" … FAILURE_PREVENTION`; `DELIVERABLE` after the prompts;
`DOCTRINE_DEVIATIONS` twice), or a heading the corpus only ever places *before* the prompts
(`FINAL_PRODUCTION_PACKAGE`, the banner; `CORE_CREATIVE_IDEA`). Checker's census: 0 of 84 files
repeat any heading; 8 of the 15 known headings never occur after `GENERATION_PROMPTS` in any file;
only 7 do. Pre-existing; identical at `0c21d76`.

The sub-case that survives any membership rule — a known post-prompts heading in schema order
with a quoted run under it — is content of that section by definition and is closable only by the
production blueprint schema (GATE-002). It is not in scope here and stays on the register.

## Ruling 12 — tighten to the after-prompts set and refuse repeats, then merge

Controller selected: **"Tighten R-01 first (after-GP set + refuse repeats)."**

### In scope

**Two refinements of the Ruling 11 rule, both derived mechanically, both zero-corpus-change by
construction:**

1. **The known set for the post-prompts position is the after-prompts set**, not the full union:
   the union of headings that appear *after* the first `GENERATION_PROMPTS` heading in at least
   one of the 84 committed packages (the checker counted 7). It is frozen as a second constant
   beside `KNOWN_SECTION_HEADINGS`, derived by script, and asserted equal to a live recomputation
   in the same test pattern. A heading after the prompts that is in the full union but not in the
   after-prompts set is an ERROR ("section heading not observed after GENERATION_PROMPTS in the
   committed schema — prompts may be hidden; not scanned"), naming the heading.
2. **A repeated heading after the prompts is an ERROR** ("section heading repeated after
   GENERATION_PROMPTS — prompts may be hidden; not scanned"), naming the heading and both line
   numbers. "Repeated" means any heading (known or not) appearing more than once at or after the
   first `GENERATION_PROMPTS` line, *except* a second `GENERATION_PROMPTS` heading itself, whose
   observed merge behaviour Ruling 11 condition 2 preserved and which stays as it is.

Binding conditions:

1. **Parsing untouched** (`SECTION_RE`, `parse_package` byte-identical to `235b2a2`; parity test
   green). Both refinements are post-parse, in the same place as the Ruling 11 rule.
2. **Pinned both ways.** The checker's R-01 rows (3a-1, 3a-3, 3a-4, 3a-6, 3a-8, 3d-1, 3d-2, 3d-3,
   3d-4, 3d-5) become package tests, predispatch tests and battery rows asserting ERROR with the
   correct reason (after-set vs repeat). Counter-pins: each of the 7 after-prompts headings, in
   schema order, once, still extracts (the four anchors' after-prompts headings among them); a
   heading that appears once before and never after the prompts still extracts; a second
   `GENERATION_PROMPTS` heading behaves as recorded under Ruling 11. The ruled boundary — a known
   post-prompts heading in schema order with a quoted run under it (3a-2) — is recorded as a test
   that documents the behaviour and cites the register, not as a pass to be tuned away.
3. **Both frozen constants asserted equal to recomputation** over the 84 committed packages; the
   after-prompts set must be a strict subset of the full union.
4. **84-package extraction diff** re-derived before (`235b2a2`) and after: 0 changed; anchors
   sha-identical.
5. **Invariant extended:** the heading branch checks after-set membership and repeats, first in
   order, independent of the production helper; asserted exercised for each new reason.
6. **R-02 addressed while in the file:** `section_headings` either becomes the production path or
   the docstring stops claiming it is; one line-walk, not two. No other cosmetic change.
7. No vocabulary constant, no negation rule, nothing under `textscan.py` or `vocab.py`, no change
   to `SECTION_RE`. R-03, R-04, R-05 stay on the register untouched.
8. Rulings 5–11 stand: test-first; stdlib; one or two commits; trailer; no push, no merge; `eval/`
   clean.

### Appended to the CANON-GATE-002 register

| id | Substance |
|---|---|
| R-01 (residual) | A known post-prompts heading in schema order with a quoted run under it is content of that section, not a prompt. Only the production blueprint schema (Ruling 3) closes this; it is the first GATE-002 design item. |
| R-03 | Five new tests pin pre-existing behaviour or test-only helpers and are falsified by no mutation. Guards, not evidence. |
| R-04 | The full `tests/` directory does not run green in this environment: two modules import `pytest`, one hard-codes a foreign path. Environmental; untouched by this task. Reports must say "gate suite". |
| R-05 | `check_limit_text` docstring omits the Ruling 10 and 11 error classes. Cosmetic. |

## Sequence

maker fix pass (the two refinements) → **bounded checker pass nine**: conditions 1–6 and 8, the ten
anchors, the battery, the 84-package diff, the eighth checker's attack table re-run (3a/3d rows
must ERROR with the right reason; 3b/3c/4/C2/LS rows unchanged), the two-heading merge line →
**Controller merges** on PASS or PASS WITH NON-BLOCKING NOTES with the first heading reading
**none**, by merge commit, never squash or rebase. Anything else returns to the Controller.

## Not authorised by this decision

Any spend, provider call or media generation; any change beyond the two refinements, their pins,
the invariant branch and the R-02 docstring/helper reconciliation; any change to `SECTION_RE` or
`parse_package`; any change under `coordination/`, `eval/`, `canon/compilation/`,
`canon/knowledge/`, `canon/audit/`, `canon/packs/`, `canon/gate/textscan.py`, `canon/gate/vocab.py`
or the plan; any conclusion about whether Canon works.
