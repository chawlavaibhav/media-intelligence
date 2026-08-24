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

---

## C. Evidence *against* earlier concerns

Nothing yet. This section exists so that a concern failing to recur is recorded as a result rather
than quietly forgotten.

---

## D. Running counts

| | Count |
|---|---|
| Books completed under the frozen method | 0 |
| Books blocked before extraction | 5 (Lupton + 4 image-only/format) |
| Issues logged | 6 new, 5 carried forward |
| Issues seen in 2+ distinct books | 0 so far |
