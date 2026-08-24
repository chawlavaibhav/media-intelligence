# Proposed Integration Change — CANON-002

**Filed by:** Canon · **Date:** 24 Aug 2026 · **Severity:** CROSS_STREAM
**Affects:** Eval / Capability Lab · **Status:** PROPOSED — not an approved decision
**Source evidence:** `canon/findings/CANON-002-williams-current-schema-extraction-findings.md` §2;
`canon/knowledge/current/robin-williams-proximity/operational-bindings.yaml` → `bnd_rw_c002_0007`;
`canon/knowledge/current/robin-williams-proximity/visual-evidence-ledger.yaml` → `vis_flowers`

Filed because the Runbook requires a worker tagging `CROSS_STREAM` to also file this file. Canon
proposes; it does not act on another stream.

---

## OBSERVATION

Williams's opening demonstration is the most strictly isolated comparison found in either current
schema extraction so far.

Two lists sit side by side on printed page 15. They are identical in word content, word order,
typeface, type size, colour, box tint and box dimensions. Exactly one thing differs: the right-hand
list has a blank line after its sixth item.

The author's stated expected reading: the last four items appear to be a different group, and the
reader understands this instantly and without conscious effort.

## EVIDENCE

**OBSERVED** — inspected as a rendered page image during CANON-002 Phase 1. Provenance verified in
Phase 0: 3rd edition, ISBN 0321563077, printed page 15 = PDF page 16.

**OBSERVED** — exactly one variable differs. This is stricter isolation than any of the four Molly
Bang pairs approved on 24 Aug 2026, two of which change more than one attribute.

**NOT VERIFIED** — the expected reading is Robin Williams's assertion. No human response data exists
for it. It is a candidate expected answer, not ground truth.

**IMPORTANT CONSTRAINT ON REUSE** — the pair does not survive plain-text extraction. In
`canon/sources/williams-proximity-p15-32.txt` the two lists are character-for-character identical.
Any use of this stimulus must work from page images. A pipeline that passes it as text is passing two
identical inputs and will produce a meaningless result that looks like a valid negative.

## PROPOSED CHANGE

Record this pair as a **candidate calibration stimulus for the deferred creative-evaluation list**,
under the same terms the Controller set for the Molly Bang pairs on 24 Aug 2026.

It is not proposed for Capability Battery V0. EVAL-001's Controller clarification §2 places
creative-judgement evaluation outside V0 and asks that deferred creative dimensions be documented so
absence is not mistaken for irrelevance. This belongs in that deferred list.

**Mandatory marking**, carried with the stimulus:
`expected reading: source-asserted by Robin Williams; NOT validated human ground truth`
`must be presented as images; the pair is destroyed by text extraction`

## EXISTING DECISION AFFECTED

None reopened. Project Contract separation 5 holds: this is stimulus material with a hypothesised
answer, not a capability claim. Nothing here asserts what any model can do.

## EXPECTED BENEFIT

A candidate stimulus, not an instrument, and not usable as-is. What it offers that the Bang pairs do
not is genuinely strict isolation: any difference in an evaluator's response can be attributed to the
one variable, once the expected reading has been independently validated. Until that validation
exists, the pair can be shown to an evaluator but the evaluator's answer cannot be marked correct or
incorrect.

## RISK

The expected reading hardening into ground truth through reuse. The stricter the isolation looks, the
more tempting it is to treat the author's prediction as established. Isolation and validation are
different properties; this pair has the first and not the second.

Secondary and specific to this item: silent failure if it is ever passed through a text pipeline,
because the two identical inputs will not error.

## FALSIFIER

Show the pair to human viewers. If grouping judgements do not follow the stated reading at better
than chance, the stimulus is not usable and this proposal fails.

## WHAT CANON IS NOT CLAIMING

- Not claiming any model can or cannot produce or judge this difference.
- Not proposing a new benchmark dimension; that is Controller-only.
- Not proposing any change to EVAL-001's approved scope.
