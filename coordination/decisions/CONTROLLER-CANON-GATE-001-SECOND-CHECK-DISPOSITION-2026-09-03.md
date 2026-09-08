# Controller — CANON-GATE-001 Second-Check Disposition — 2026-09-03

**Status:** APPROVED CONTROLLER RULING; a second bounded fix pass is authorised before merge.
**Role:** Writer Controller.
**Applies to:** `work/canon-gate-001` at `be30c89` (fix pass, seven commits) and the checker's
second-pass report on it (verdict: **BLOCK**, findings K-01..K-10).
**Parent authority:** `CONTROLLER-CANON-GATE-001-BUILD-AUTHORISATION-2026-09-03.md`;
`CONTROLLER-CANON-GATE-001-PLAN-RULINGS-2026-09-03.md`;
`CONTROLLER-CANON-GATE-001-CHECKER-DISPOSITION-2026-09-03.md`.

The checker confirmed thirteen of the fourteen first-pass findings resolved and all ten anchor
verdicts holding, and blocked on regressions the fix pass introduced. The Controller was offered
two options and selected one; the selection is recorded as chosen, nothing added.

## Ruling 6 — second bounded fix pass (checker K-01..K-06)

Controller selected: **"Second bounded fix pass."**

Scope is **K-01 through K-06 only**. K-07, K-08, K-09 and K-10 are recorded limitations and notes;
they are not in scope and are not to be touched.

Binding conditions, in addition to every condition of Ruling 5 (which stand unchanged):

1. **K-01 — the CA-D2 clause-2 negation window is bounded, not sentence-wide.** Plan §B.1's
   4-token window is amended to **6 tokens before the term** (enough for the F-07 phrase "we will
   not compose this using the rule of thirds"), plus the after-term disclaimers
   (`vocab.NEGATED_AFTER`) the fix pass introduced. Sentence-wide negation is withdrawn. The three
   regression sentences the checker reported — "Without clutter, the watch sits on the golden
   ratio point.", "No hard shadows, dial placed on the rule of thirds line.", "Not too tight, the
   crown sits at the intersection of the thirds." — must FAIL (blocking), pinned as tests. The
   F-07 phrasings must still PASS, pinned. **Every negation-window test is written in both
   directions.**
2. **K-02 — quote pairing must accept whitespace inside the quotes.** A closing straight quote
   preceded by whitespace, and an opening quote followed by whitespace, pair normally when a run
   is open. The two maker fixtures the checker found running under LIMIT-TEXT ERROR
   (`tests/test_gate_predispatch.py` around lines 316–320) must assert LIMIT-TEXT is not ERROR.
   The four committed packages must still extract byte-identically (existing test).
3. **K-03 — T3's negation window must not clear a text surface when the negator governs
   something else.** "Avoid cluttering the dashboard", "never crowded, the poster on the wall",
   "A tidy, not busy, receipt on the table", "zero clutter around the invoice" must HIT, pinned.
   The F-02 phrasings ("no secondary messages" etc.) must still CLEAR, pinned. If a lexical rule
   cannot satisfy both sets, the maker keeps the rule that catches text surfaces (the blocking
   direction; the row that caught 3 of 5 EVAL-038 artifacts) and records the F-02 phrasings that
   revert to over-fire in `CHANGELOG` with their outcome pinned as tests — a recorded over-fire is
   acceptable; a silent false PASS on a blocking row is not.
4. **K-04 — every narrowed bare term is pinned in the failing direction.** `fill`, `side`,
   `behind` and bare `°` each get a fixture that FAILs on the old term and PASSes on the narrowed
   one, in a single sentence with no splitter boundary between the light term and the direction
   term. The vacuous `°` test is replaced, not kept.
5. **K-05 — an inch mark inside a prompt must not truncate it.** `6" OLED panel showing chat
   bubbles` and `is 6". It shows chat bubbles` must extract the whole prompt and FAIL LIMIT-TEXT,
   pinned.
6. **K-06 — the F-03 additions must not fire on watch-category numerals.** "Arabic numerals at
   12, 3, 6 and 9 on the dial", "the date digits at 3 o'clock", "Roman numerals, no other
   markings" must CLEAR; "a label-free bottle", "a quiet storefront at dusk, shutters down" must
   CLEAR; each pinned. The F-03 phrasings that motivated `numerals`/`digits`/`storefront` ("a wall
   clock with clear numerals", "the phone number … painted across the shutter") must still HIT,
   pinned. Where the two sets conflict, the maker records the choice in `CHANGELOG` and pins both
   outcomes.
7. **Regression guard.** The maker adds one test module or class that runs the checker's full
   regression table (this decision's phrases plus the first-pass F-02/F-03/F-04/F-05/F-07
   phrases) as a single battery with the intended outcome per phrase, so that a third pass can
   diff intended vs observed mechanically.

## Sequence to merge

maker second fix pass → checker third pass (regression table diffed against intended; anchors;
conditions) → Controller merge decision. No agent approves its own work; the Controller does not
implement.

## Not authorised by this decision

Any spend, provider call or media generation; any change under `coordination/`, `eval/`,
`canon/compilation/`, `canon/knowledge/`, `canon/audit/`, `canon/packs/` or the plan; any
widening of scope beyond K-01..K-06; any conclusion about whether Canon works; merge to `main`.
