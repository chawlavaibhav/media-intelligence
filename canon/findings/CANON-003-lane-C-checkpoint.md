# CANON-003 — Lane C checkpoint

**Lane:** C — advertising / persuasion · **Branch:** `work/canon-003-c` ·
**Worktree:** `media-intelligence-canon-c`
**Method:** frozen. No schema, granularity rule, visual-pass method or ontology vocabulary has been
changed. **Updated after each completed book.**

---

## Status

| Book | Title | State | Fresh checkpoint | Historical comparison |
|---|---|---|---|---|
| 13 | Claude C. Hopkins, *Scientific Advertising* | **complete** | `1222919` | **none exists** — verified by search after the checkpoint; recorded as `no historical comparator` |
| 14 | Chip Heath & Dan Heath, *Made to Stick* | not started | — | — |
| 15 | Rory Sutherland, *Alchemy* | not started | — | — |

**Books blocked:** none.
**Partially extracted books:** none. Book 13 is finished, validated, committed and pushed.

## Latest commits

| What | SHA |
|---|---|
| Book 13 fresh pre-history checkpoint (knowledge files + provenance) | `1222919` |
| Book 13 lane issues + this checkpoint | see `git log -1` on `work/canon-003-c` |

## What book 13 produced

`canon/knowledge/current/hopkins-scientific-advertising-ch1-7/`

| File | Contents |
|---|---|
| `visual-evidence-ledger.yaml` | pass performed, `verified_page_level`, 0 demonstrations — the source has no visual layer |
| `source-knowledge.yaml` | 54 objects |
| `source-concept-systems.yaml` | 5 systems |
| `ontology-mappings.yaml` | 37 terms (15 problems, 16 remedies, 6 properties), 10 relationships including 3 `distinct_from`, 4 source-specific concepts |
| `operational-bindings.yaml` | 8 bindings, all `proposed` |
| `PROVENANCE.md` | identity, integrity, OCR profile, visual result, scope limits, rights |

**Section processed:** chapters 1–7, printed pp.1–24 of 21 chapters. Chapters 8–21 not processed;
chapter 15 "Test Campaigns" is the notable exclusion and is stated in `PROVENANCE.md`.

**Mechanical validation:** passes SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer
constraints. The same validator was run against all five pre-parallel books and passes on each, so
this extraction is being held to the same rules they were.

## Unresolved local issues

None blocking. Seven new issues and four pieces of evidence *for* the frozen design are recorded in
`canon/findings/CANON-003-lane-C-issues.md`. All proposed fixes are proposals only; nothing has been
applied.

The two most consequential, in plain terms:

- **C-01** — the evidence vocabulary has one slot for two different facts: a source that *reports* a
  measurement, and a source that *says* one was made. Hopkins is almost entirely the second kind.
  Handled by applying `empirical_within_source` only where a result is reported, and writing every
  asserted-but-unreported measurement into a caveat. Nothing is lost for a human reader, but nothing
  can count it either.
- **C-02** — the mail-order copy rules are held together by one shared evidential warrant, and no
  available `system_type` means that. `interacting_set` was used as the least assumptive option and
  the mismatch recorded rather than resolved.

## Open questions this lane cannot settle

- Whether C-05(a) — using `related_to` where `broader_than`/`narrower_than` was meant — is a genuine
  recurrence of a pre-parallel item or a separate observation of the same shape. This lane has not
  read the earlier book's working files and does not assert a count.
- Whether *Scientific Advertising* chapter 15, "Test Campaigns", supplies the measurement detail
  chapters 1–7 do not. Outside the processed section. **NOT VERIFIED.**
- Rights status of the local library files, carried forward unresolved from the batch inventory.

## Remaining assignments

Books 14 and 15, in order, under the same frozen method: fresh extraction → mechanical validation →
commit and push the fresh checkpoint → only then search for and compare historical material → update
the lane issue file and this checkpoint.

Per the amendment's context-window rule, the lane stops at a completed-book boundary if context
becomes crowded and resumes from this branch in a fresh session. Lane C does not merge itself, does
not touch the shared batch ledger, synthesis, Controller Brief or `canon/HANDOFF.md`, and does not
read other lanes' fresh findings.
