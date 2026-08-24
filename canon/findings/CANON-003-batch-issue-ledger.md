# CANON-003 — Batch issue ledger

**Opened:** 24 Aug 2026 · **Task:** `canon/tasks/CANON-003.md`
**Rule for this batch:** the extraction method and SPEC-01/03/04/05 are a **frozen test instrument**.
Problems are logged here and the batch continues. Nothing is fixed mid-batch. Proposed fixes are
proposals only and are not applied during CANON-003.

**Counting rule:** the "distinct books" column counts separate book titles showing the issue. Repeated
occurrences inside one book are **not** independent evidence and are not counted twice.

**Status vocabulary:** OBSERVED = directly seen or measured · INFERRED = reasoned from observations ·
SUSPECTED = plausible, not yet evidenced.

---

## A. Hypotheses carried forward from CANON-001 and CANON-002

Entered as things to watch for recurrence, **not** as established findings. CANON-003 explicitly
forbids resolving them before the batch.

| ID | Plain-English issue | First seen | Distinct books so far | Status |
|---|---|---|---|---|
| H-01 | Plain text can silently destroy the evidence a book argues from. Williams's two flower lists differ only by a blank line; in the text file they are identical, so her explanation describes evidence the file does not contain. | CANON-002 (Williams) | 1 | OBSERVED, awaiting recurrence |
| H-02 | A change can be both an experimental confound and a claim the author teaches. Three Williams claims were missed because the visual pass filed them as "this comparison isn't clean" and never tested them as content. | CANON-002 (Williams) | 1 | OBSERVED, awaiting recurrence |
| H-03 | When a source states two claims in one passage and argues only one, it is unclear which becomes the record. Williams's all-caps passage claims both illegibility and space consumption. | CANON-002 (Williams) | 1 | OBSERVED, awaiting recurrence |
| H-04 | `creative.hierarchy` is a ranked list and cannot express "the reader knows when they are finished". Ranking says what is noticed first; it cannot say where reading ends. | CANON-002, plus historical Williams and Lupton passes | 1 fresh + 2 historical | OBSERVED, awaiting recurrence |
| H-05 | Figures are used to verify text-derived claims rather than read as independent evidence, so a claim visible only in a picture can be missed. | CANON-001 (Bang, p.87) | 1 | OBSERVED, awaiting recurrence |

---

## B. Issues found in CANON-003 so far

### B-01 — An extraction artifact can imitate a provenance failure *(new)*

**Plain English.** When checking whether the repository's *Light: Science & Magic* chapter really came
from the local copy of the book, the first result was a 91.5% match. A 9% gap looks like the two texts
are different editions, which would have blocked a mandatory anchor book.

It was not an edition difference. My own text extraction had left HTML character codes (`&#13;`,
meaning a carriage return) undecoded. Those codes ran into the surrounding words, broke sentences in
half, and made text that was genuinely present look absent. After decoding them the match is 100%.

**Why it matters.** A provenance check is supposed to be the safeguard that stops us extracting from
the wrong book. Here the safeguard nearly produced a false positive and discarded a good source. The
failure was in the measuring instrument, not the thing measured.

**What changes.** Nothing during this batch — the method is frozen. Going forward, a provenance
mismatch should be diagnosed before it is acted on: check whether the "missing" text exists elsewhere
in the book in a slightly different form.

**Uncertainty.** Seen once. Whether it recurs depends on how many EPUBs carry raw entities.

- **Books:** Light: Science & Magic · **Distinct books: 1** · **Status: OBSERVED**
- **Layer:** provenance
- **New / recurrence:** new in this batch
- **Consequence if unchanged:** usable source books wrongly blocked; batch size falls for a reason that is not real
- **Proposed fix (NOT APPLIED):** decode HTML entities before any provenance comparison, and treat any mismatch under ~15% as unproven until the missing text is searched for in normalised form

### B-02 — Matching provenance does not mean the text is faithful *(new, and it corrected my own reasoning)*

**Plain English.** Phase 0 verified that the repository's Lupton text genuinely comes from the local
Lupton EPUB: 520 out of 520 sentences matched word for word. I initially read that as "the text is
good."

It is not. Both files share the *same* corruption. The 100% match confirms they have a common origin;
it says nothing about whether either faithfully represents the printed page. Those are two different
questions and the check only answers the first.

**Why it matters.** This is the more dangerous version of B-01. B-01 makes a good book look bad, which
is recoverable. B-02 makes a corrupt book look verified, which is not — it would licence extraction
from text that misrepresents the source.

**Uncertainty.** Whether other repository texts share undetected corruption with their source copies
is **NOT VERIFIED**. It should be checked per book rather than assumed.

- **Books:** Lupton · **Distinct books: 1** · **Status: OBSERVED**
- **Layer:** provenance, source fidelity
- **New / recurrence:** new in this batch
- **Consequence if unchanged:** a provenance check that passes while the extraction is unfaithful
- **Proposed fix (NOT APPLIED):** treat provenance matching and text-fidelity checking as two separate gates. Matching answers "is this the right book"; fidelity answers "does this text represent the page"

### B-03 — Lupton blocked: column interleaving is baked into the source file *(anchor blocked)*

**Plain English.** *Thinking with Type* is printed in two columns. In both the repository text and the
local EPUB, the two columns are merged line by line, so sentences from the left column are spliced
into sentences from the right. The result reads as English but is not what the book says. For example
the file contains:

> "The next step is to create drawings. Some / typeface is an enormous task. However, for people /
> designers start with pencil before working digitally, with a knack for drawing letterforms…"

Two separate sentences, from two separate columns, cut into strips and shuffled together.

I tested whether a more careful extraction could recover the columns. It cannot. In the EPUB each
paragraph element is one *physical line across the page*, not one paragraph — so the information about
where one column ends and the other begins does not exist in the file at all. There is nothing to
recover it from: this EPUB has figures but no page scans.

**Why it matters.** Any claim extracted from this text would be a sentence the author never wrote. That
is not a small fidelity loss, it is fabrication. CANON-003 says to block rather than guess through
corruption, so Lupton is blocked.

**What changes.** Lupton is a *mandatory anchor*, and the task allows an anchor to be dropped only
when source integrity blocks it. This is that case. It is replaced from reserve, and the static-design
domain quota is filled by the other selected books. The historical Lupton work stays sealed and
untouched.

**Uncertainty.** A clean copy of this book may exist elsewhere; **NOT VERIFIED**, and CANON-003
forbids acquiring one.

- **Books:** Lupton · **Distinct books: 1** · **Status: OBSERVED**
- **Layer:** source fidelity
- **New / recurrence:** confirms a risk the Canon handoff and CANON-003 both flagged in advance
- **Consequence if unchanged:** fabricated claims entering the Canon under a verified-provenance label
- **Status:** `blocked_source_integrity`. Not extracted. Replaced from reserve

### B-04 — EPUB sources cannot support a page-layout visual pass at all *(new, structural)*

**Plain English.** The local library splits into two kinds of file, and the kind decides what a visual
check can even see.

- A **PDF** can be rendered as page images. You see the printed page: spacing, position, what sits
  next to what, before-and-after pairs as the reader saw them.
- An **EPUB** has no pages. It reflows to fit whatever screen shows it. It contains the book's
  figures, but no page layout exists in the file to inspect.

**Why it matters.** CANON-002's central finding was that spatial argument disappears in plain text and
that only looking at the page recovers it. For an EPUB there is no page to look at. So for any book
that argues through where things sit — typography and layout books above all — an EPUB gives us the
same blind spot with no remedy.

This is why Lupton was doubly unusable: corrupt text *and* no page-level visual source.

**What changes in this batch.** Books sourced from EPUB will carry visual completeness
`not_verified`, per the task's visual-evidence policy. That is recorded per book rather than treated
as a pass.

**Uncertainty.** Whether figure-only visual evidence is sufficient for *non*-layout books — a lighting
diagram may survive perfectly well without its page — is **not yet established**. Watch across the batch.

- **Books:** affects Lupton, LSM, Ogilvy, Making and Breaking the Grid, Painting With Light, Master Shots, Hey Whipple, The Conversations and other EPUB-sourced titles · **Distinct books: 8+ selected or reserve** · **Status: OBSERVED**
- **Layer:** visual completeness
- **New / recurrence:** new in this batch; extends H-01 from "text loses spatial evidence" to "some file formats cannot restore it"
- **Consequence if unchanged:** silent visual blind spots on exactly the source class where CANON-002 proved they matter most
- **Proposed fix (NOT APPLIED):** record source file format as a first-class provenance field, and treat "EPUB + layout-argued book" as a known-incomplete combination rather than a normal extraction

### B-05 — Four library books are image-only scans with no extractable text *(new)*

**Plain English.** *Grid Systems in Graphic Design*, *Ways of Seeing* and *Understanding Exposure* are
PDFs containing photographs of pages, with zero machine-readable text. *Thinking, Fast and Slow* is in
a format with no reader available locally. Extraction from these would mean reading every page as an
image — a different and far slower method than the one under test.

**Why it matters.** It removes four books from a batch that needs fifteen, and one of them —
*Grid Systems* — is a foundational layout text whose absence measurably weakens the static-design
domain.

- **Books:** 4 · **Distinct books: 4** · **Status: OBSERVED**
- **Layer:** source fidelity, provenance
- **New / recurrence:** new in this batch
- **Consequence if unchanged:** domain coverage narrows for reasons unrelated to the method being tested
- **Proposed fix (NOT APPLIED):** none available without acquiring sources, which CANON-003 forbids

### B-06 — The library contains no animation or motion book *(coverage gap, not a method failure)*

**Plain English.** The task asks for three books covering storytelling / animation / motion / creative
process. The local library has storytelling and creative-process books but no animation title at all —
no *Illusion of Life*, no *Animator's Survival Kit*.

**Why it matters.** Animation and motion books reason about change over time, which is a genuinely
different knowledge shape from everything else in this batch. Its absence means the batch will not
test whether the schema handles time-based craft knowledge — a gap the synthesis must not paper over.

- **Distinct books: 0 available** · **Status: OBSERVED**
- **Layer:** coverage
- **Consequence if unchanged:** the synthesis cannot speak to time-based creative knowledge
- **Proposed fix (NOT APPLIED):** documented as a gap; acquiring a source is out of scope

### B-07 — The historical binding layer over-binds, in every book so far *(recurrence, 3 books)*

**Plain English.** Every historical migration audit attaches roughly one Creative IR binding to every
knowledge object. Bang: 21 bindings for 19 objects. Williams: 12 for 14. Grammar of the Shot: 13 for
13. The fresh passes under the current method produce 5, 2 and 2 respectively, leaving most objects
attached to nothing.

**Why it matters.** SPEC-04 was written on the principle that zero bindings is a normal, healthy state
— it tells you something about the product, not about the knowledge. A near-1:1 ratio is the signature
of the *old* rule, which required every atom to name a Creative IR field and so manufactured bindings
to satisfy it. Seeing it in all three migrated books suggests the migration carried the old rule's
shape forward even though the rule itself was removed.

**What changes.** Nothing during the batch. But this is now the most consistently reproduced
difference between old and new work, and it is direct evidence that the separation SPEC-04 introduced
is doing something rather than merely being asserted.

**Uncertainty.** Three books, all migrated by the same process. This is evidence about that migration,
not proof about binding layers in general.

- **Books:** Bang, Williams, Grammar of the Shot · **Distinct books: 3** · **Status: OBSERVED**
- **Layer:** bindings
- **New / recurrence:** recurrence across all books processed to date
- **Consequence if unchanged:** historical bindings read as product requirements when many were rule artifacts
- **Proposed fix (NOT APPLIED):** none needed for the fresh method; relevant to whether historical bindings should be trusted when the two representations are eventually reconciled

### B-08 — The fresh method finds governance knowledge the historical passes missed *(recurrence, 2 books)*

**Plain English.** "Governance" here means knowledge about how the system should handle its own
knowledge — for example, whether a rule may be applied on its own or must be used with others.

Both historical audits report zero governance findings. The Williams audit explicitly considered one
and rejected it. Both fresh passes found one, and in both cases from the same kind of statement: the
author telling the reader how their own rules should be treated. Williams says take the principles one
at a time and start with proximity. Grammar of the Shot says there are very few absolutes and a
creative reason justifies breaking any rule in the book.

**Why it matters.** This is a class of knowledge that authors state plainly and that the older method
consistently dropped. It bears directly on whether Canon knowledge should ever be enforced as a
constraint rather than offered as a default.

**Uncertainty.** Two books. Whether it recurs in sources that do not editorialise about their own
rules is unknown — Bang, notably, produced governance material too but of a different kind.

- **Books:** Williams, Grammar of the Shot · **Distinct books: 2** · **Status: OBSERVED**
- **Layer:** bindings, Creative IR fit
- **New / recurrence:** recurrence first seen inside this batch
- **Consequence if unchanged:** the project keeps rediscovering that its craft sources have opinions about their own authority
- **Proposed fix (NOT APPLIED):** none; the fresh method already captures it

### B-09 — The historical passes keep catching product-schema fit points the fresh passes miss *(recurrence, 2 books)*

**Plain English.** Twice now, the older work has noticed something about how craft knowledge does or
does not fit the product's Creative IR schema, and the fresh pass has walked straight past it while
holding the same evidence.

- **Williams:** the historical audit noticed that `creative.hierarchy` is a ranked list and therefore
  cannot express "the reader knows when they are finished". I extracted that exact claim and bound it
  to that exact field without noticing the mismatch.
- **Grammar of the Shot:** the historical audit binds sight lines to the `relationships` field,
  correctly, because a sight line is literally one entity looking at another — SPEC-01's own example
  for that field. I bound sight lines only to continuity requirements and never considered it.

**Why it matters.** This is the reverse of what the batch was expected to show. The fresh method is
better at source fidelity — it finds more of what the author actually said. The historical method
appears better at product fit. If that holds, the two passes are good at different things and the
weakness is specific: **the fresh method is under-attentive to how knowledge meets the product
schema, precisely because it was designed to stop the product schema distorting extraction.**

**Uncertainty.** Two books. It may be that the historical passes had an advantage here because they
were *required* to name a Creative IR field, which forced the question. That would make this a
side-effect of the very rule that caused the distortions SPEC-03 was written to fix — a genuine
trade-off rather than a simple defect. **Not established.**

- **Books:** Williams, Grammar of the Shot · **Distinct books: 2** · **Status: OBSERVED, interpretation INFERRED**
- **Layer:** Creative IR fit
- **New / recurrence:** recurrence first seen inside this batch; extends H-04
- **Consequence if unchanged:** the fresh Canon is more faithful and less usable than it could be
- **Proposed fix (NOT APPLIED):** possibly a separate binding-review step that asks, per object, which SPEC-01 fields it touches — deliberately after the source pass, so it cannot contaminate it

### B-10 — A third distinct kind of visual dependence *(extends H-01, 3 books)*

**Plain English.** How figures matter differs by book, and the difference decides what text extraction
destroys.

- **Bang:** figures corroborate prose that already carries the argument. Little is lost.
- **Williams:** the evidence *is* the spacing. Everything is lost, and lost silently — the two
  demonstration lists become identical.
- **Grammar of the Shot:** figures pair an overhead plan of the camera with the resulting image. What
  is lost is the *correspondence between the two halves*. But the text names each figure and says what
  it shows, so a text-only reader can tell they are missing something.

**Why it matters.** The dangerous case is not "figures matter". It is "figures matter and the text does
not admit it." Williams is dangerous; Grammar of the Shot is merely incomplete.

- **Books:** Bang, Williams, Grammar of the Shot · **Distinct books: 3** · **Status: OBSERVED**
- **Layer:** visual completeness
- **New / recurrence:** extends H-01 with a third pattern
- **Consequence if unchanged:** visual loss is treated as one problem when it is at least three, with different severities
- **Proposed fix (NOT APPLIED):** record a visual-dependence class per book rather than a yes/no completeness flag

### B-11 — The relation vocabulary a worker may use is narrower than the schema's *(new)*

**Plain English.** SPEC-05 defines ten relation types for connecting terms. The Canon Charter grants a
worker two of them (`related_to`, `potentially_equivalent_to`), and the Controller added a third
(`distinct_from`) on 24 Aug 2026.

In this book two relations genuinely wanted `broader_than` and `narrower_than`: jumping the line is one
cause of reversed screen direction, and a sight line is the specific thing an axis of action is traced
from. Both are ordinary, low-risk structural facts. I recorded them as `related_to` and put the
intended stronger reading in the note.

**Why it matters.** The information is preserved but downgraded, so the ontology understates what is
known. The Controller's stated reason for permitting `distinct_from` — that it is already part of the
vocabulary — would apply equally to these two. This looks like an unintended gap rather than a
deliberate restriction, but assuming that mid-batch would be inventing policy, which CANON-003 forbids.

- **Books:** Grammar of the Shot · **Distinct books: 1** · **Status: OBSERVED**
- **Layer:** ontology
- **New / recurrence:** new in this batch
- **Consequence if unchanged:** relations recorded weaker than the evidence supports; later aggregation sees a flatter graph than it should
- **Proposed fix (NOT APPLIED):** Controller ruling on whether the purely structural relation types are within worker authority

### B-12 — A source copy carried a previous reader's highlighting *(new, minor)*

**Plain English.** The local Grammar of the Shot PDF has yellow highlighter on printed page 110, over
one phrase and two figure captions, applied by whoever owned the file before.

It does not corrupt anything — extracted text matched the repository file exactly. But highlighting
directs the eye, so a visual pass over an annotated copy risks inheriting a previous reader's sense of
what mattered.

**Uncertainty.** Whether this influenced my reading of that page is unknown and unknowable from here.

- **Books:** Grammar of the Shot · **Distinct books: 1** · **Status: OBSERVED**
- **Layer:** provenance, visual completeness
- **Consequence if unchanged:** small, hard-to-detect attention bias in visual passes
- **Proposed fix (NOT APPLIED):** record artifact condition in the per-book provenance file, which was done here

---

## C. Evidence *against* earlier concerns

**H-01 partially answered, and the answer is reassuring.** Grammar of the Shot depends heavily on its
figures, but the text names every figure and states what it shows. The silent, undetectable loss seen
in Williams did **not** recur. One book is not enough to conclude that Williams was exceptional, but
it is the first evidence that catastrophic silent visual loss is not universal. See B-10.

**H-02 did not recur.** Grammar of the Shot narrates changes between its own before-and-after figures,
but those changes are the subject of the demonstration rather than incidental confounds, so the
classification trap that lost three Williams claims did not arise. Not yet evidence that it was
source-specific — this source simply does not have the shape that triggers it.

---

## D. Running counts

| | Count |
|---|---|
| Books completed under the frozen method | **1** (Grammar of the Shot ch.4) |
| Books blocked before extraction | 5 (Lupton + 4 image-only/format) |
| Issues logged | 12 new, 5 carried forward |
| **Issues seen in 2+ distinct books** | **4** (B-07 ×3, B-08 ×2, B-09 ×2, B-10 ×3) |

### Book 1 method-integrity note
The frozen method held. No schema, granularity rule, visual-pass method or ontology vocabulary was
changed. Two errors of mine were caught and corrected **before** the checkpoint: an unauthorised
relation type, and a validator regex that wrongly rejected a digit in a source-derived term.
