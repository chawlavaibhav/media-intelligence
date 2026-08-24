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
| 14 | Chip Heath & Dan Heath, *Made to Stick* | **complete** | `a699a49` | **no prior extraction exists** — verified by search after the checkpoint. One prior *prediction* in `CANON-CURRICULUM-V0.md` was compared instead; see C-21 |
| 15 | Rory Sutherland, *Alchemy* | not started | — | — |

**Books blocked:** none.
**Partially extracted books:** none. Book 13 is finished, validated, committed and pushed.

## Latest commits

| What | SHA |
|---|---|
| Book 13 fresh pre-history checkpoint (knowledge files + provenance) | `1222919` |
| Book 13 lane issues + lane checkpoint | `df1a490` |
| Book 14 fresh pre-history checkpoint (knowledge files + provenance) | `a699a49` |
| Book 14 lane issues + this checkpoint update | see `git log -1` on `work/canon-003-c` |

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

## What book 14 produced

`canon/knowledge/current/heath-made-to-stick-introduction/`

| File | Contents |
|---|---|
| `visual-evidence-ledger.yaml` | pass performed, `not_verified_page_layout`, 0 figures in the whole book, 1 visual-only observation — the section title exists only as an image of the word |
| `source-knowledge.yaml` | 28 objects |
| `source-concept-systems.yaml` | 3 systems, two of them with `whole_system_claim.origin: source_explicit` |
| `ontology-mappings.yaml` | 22 terms (7 problems, 10 remedies, 5 properties), 9 relationships including 1 `distinct_from`, 3 source-specific concepts |
| `operational-bindings.yaml` | 9 bindings, all `proposed` |
| `PROVENANCE.md` | identity, integrity, visual result, the EPUB locator limitation, the evidence-vocabulary note, scope limits, rights |

**Section processed:** the complete Introduction, "What Sticks?". Chapters 1–6 and the epilogue not
processed, so each principle object records what the Introduction supports rather than the book's
full case. Stated in `PROVENANCE.md`.

**Framework preservation, which was the specific instruction for this book.** The six principles are
one object each because the principle is the unit the checklist operates on; sub-claims with their
own mechanism and their own support are separate objects that `specialise` their principle. Three
systems carry the parts that live above the objects — the checklist, the Curse of Knowledge and the
only escape from it, and the argument that stickiness is learnable at all. Without that layer the
extraction would have been six commonsense rules; see C-16.

**Mechanical validation:** passes SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the SPEC-05 layer
constraints. The same validator was run against all five pre-parallel books and passes on each, so
this extraction is being held to the same rules they were.

## Unresolved local issues

None blocking. Thirteen new issues and six pieces of evidence *for* the frozen design are recorded
in `canon/findings/CANON-003-lane-C-issues.md`. All proposed fixes are proposals only; nothing has
been applied.

### The finding this lane would most want read

**Two books, same domain, broke the same field in opposite directions.** SPEC-03 has one evidence
characteristic for measurement, `empirical_within_source`, defined as "the source reports its own
measurement". Hopkins claims measurement constantly and supplies almost none. The Heaths supply
measurement constantly and almost none of it is their own — it is Newton's Stanford study, Best and
Horiuchi's, a 1999 Israeli experiment. Neither can be recorded honestly, and there is no
neighbouring value in the fixed list that would work. Both were handled by writing the truth into
prose caveats, which is faithful and cannot be counted. Issues C-01 and C-13.

### Also consequential

- **C-01** — the evidence vocabulary has one slot for two different facts: a source that *reports* a
  measurement, and a source that *says* one was made. Hopkins is almost entirely the second kind.
  Handled by applying `empirical_within_source` only where a result is reported, and writing every
  asserted-but-unreported measurement into a caveat. Nothing is lost for a human reader, but nothing
  can count it either.
- **C-02** — the mail-order copy rules are held together by one shared evidential warrant, and no
  available `system_type` means that. `interacting_set` was used as the least assumptive option and
  the mismatch recorded rather than resolved.
- **C-15** — SPEC-05's governance section and the Canon charter give different answers about which
  relationship types a worker may set without review. The narrower reading was followed, and the
  cost is that a relation the source states outright — the tapper/listener gap *is* the Curse of
  Knowledge — is recorded in the structured layer as an unspecified connection. The cheapest fix
  needs no schema change, only a decision about which document governs.
- **C-16**, on the other side of the ledger, is the strongest evidence in this lane *for* the
  current design. Made to Stick's contribution lives almost entirely above its individual claims,
  and the system layer held all of it.

## Open questions this lane cannot settle

- Whether C-05(a) — using `related_to` where `broader_than`/`narrower_than` was meant — is a genuine
  recurrence of a pre-parallel item or a separate observation of the same shape. This lane has not
  read the earlier book's working files and does not assert a count.
- Whether *Scientific Advertising* chapter 15, "Test Campaigns", supplies the measurement detail
  chapters 1–7 do not. Outside the processed section. **NOT VERIFIED.**
- Whether C-19 — a heading that exists only as an image — is a recurrence of the pre-parallel
  finding about a graphic disturbing a named section, or a separate pattern. Not asserted.
- Whether the coverage map's and curriculum's confidence ratings elsewhere are similarly
  directionally right and materially overstated. One was checked here (C-21); the rest are not
  this lane's to audit.
- Rights status of the local library files, carried forward unresolved from the batch inventory.

## Remaining assignments

Book 15 — Rory Sutherland, *Alchemy* — under the same frozen method: fresh extraction → mechanical validation →
commit and push the fresh checkpoint → only then search for and compare historical material → update
the lane issue file and this checkpoint.

Per the amendment's context-window rule, the lane stops at a completed-book boundary if context
becomes crowded and resumes from this branch in a fresh session. Lane C does not merge itself, does
not touch the shared batch ledger, synthesis, Controller Brief or `canon/HANDOFF.md`, and does not
read other lanes' fresh findings.
