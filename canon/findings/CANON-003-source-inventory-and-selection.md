# CANON-003 — Source inventory and coverage-driven selection

**Date:** 24 Aug 2026 · **Task:** `canon/tasks/CANON-003.md` · **Branch:** `work/canon`
**Purpose:** establish, before any extraction, whether at least 15 usable distinct books exist in the
already-available local library, and select a set driven by domain diversity rather than by the
issues CANON-001 and CANON-002 happened to surface.

**No book was acquired for this task.** Everything below was already on the local disk or in the
repository.

---

## 1. Headline result

**OBSERVED: 15 usable distinct books exist locally, and considerably more than 15.** Of 37 distinct
titles found, **32 have machine-extractable text** and **4 are blocked** on source integrity.

The whole-task stop condition "fewer than 15 usable distinct books are available locally" **does not
fire.** The batch can proceed.

Plain-English meaning: the library is not the constraint. Every one of the five domain quotas the
task sets can be filled from material already present, and there is enough spare to replace a book
that turns out to be unusable partway through.

---

## 2. Where the library is

Two locations, both already present:

| Location | What is there |
|---|---|
| `canon/sources/*.txt` | 6 pre-extracted chapter texts. Two are already processed (Bang → CANON-001, Williams → CANON-002). The other four are this task's mandatory anchors. |
| `~/Downloads/Books/` | 40 files, 37 distinct titles after removing 3 duplicate copies. Mixed PDF and EPUB. |

**Provenance note, carried forward from CANON-002 and unresolved.** Several filenames in the local
library carry a `libgen.li` marker, indicating a piracy-site origin — including the Lupton and Albers
copies selected below. These files were already on the disk. CANON-003 permits read-only use of
already-available local material and forbids acquiring anything new; nothing has been acquired,
redistributed or committed, and no page images will be committed. Recording this because an inventory
that omits provenance defeats its own purpose. **NOT VERIFIED:** the licence status of any of these
copies. This is a Controller question, not one this extraction can settle.

---

## 3. Blocked books — source integrity

**OBSERVED.** Four titles cannot yield faithful text extraction and are blocked before extraction, so
they do not count toward the 15.

| Book | Why blocked | Status |
|---|---|---|
| Grid Systems in Graphic Design (Müller-Brockmann) | 162 pages, **zero** extractable characters — an image-only scan | `blocked_source_integrity` |
| Ways of Seeing (Berger) | 79 pages, zero extractable characters — image-only scan | `blocked_source_integrity` |
| Understanding Exposure | 157 pages, zero extractable characters — image-only scan | `blocked_source_integrity` |
| Thinking, Fast and Slow | `.mobi` format, no extractor available locally | `blocked_source_integrity` |

Plain-English meaning: these are photographs of pages, not text. A claim could only be extracted by
reading every page as an image, which is a different and much slower method than the one under test.
CANON-003 says to block rather than guess through corruption, so they are blocked and replaced from
reserve. **Grid Systems is the most regrettable loss** — a foundational layout text whose absence
slightly weakens the static-design domain.

---

## 4. Anchor verification — all four pass

CANON-003 makes four books mandatory anchors if usable. Each has a pre-extracted chapter text in the
repository, and each also has a full copy in the local library. I checked whether the repository text
genuinely comes from the local book, by normalising both and testing every sentence over 70
characters for a verbatim match.

| Anchor | Repository text | Local book | Sentences checked | Verbatim match | Verdict |
|---|---|---|---|---|---|
| Lupton — *Thinking with Type* | `lupton_split001.txt` | Thinking with Type (2010) EPUB | 520 | **520 (100%)** | usable |
| *Grammar of the Shot* ch.4 | `gos-ch4-continuity-p93-112.txt` | Grammar of the Shot, 2nd ed., 232pp PDF | 135 | **135 (100%)** | usable |
| Ogilvy ch.2 | `ogilvy-ch2-advertising-that-sells.txt` | Ogilvy on Advertising EPUB | 219 | **215 (98.2%)** | usable |
| *Light: Science & Magic* ch.3 | `lsm-ch3-reflection.txt` | LSM 5th ed. EPUB | 200 | **200 (100%)** | usable |

**A false alarm worth recording, because it will recur.** On the first pass LSM matched only 91.5%
and appeared to be an edition mismatch — which would have blocked an anchor. It was not. My own
extraction had left HTML character entities (`&#13;`) undecoded, which broke sentences apart and made
present text look absent. After decoding entities the match is 100%.

Why this matters beyond LSM: **a text-extraction artifact can imitate a provenance failure.** Had I
trusted the first number, a perfectly good anchor book would have been wrongly blocked. Logged in the
batch ledger as a method hazard. Ogilvy's remaining 4 unmatched sentences are the same class of
artifact — running text merged across captions — confirmed because their opening fragments are all
findable elsewhere in the book.

---

## 5. Visual evidence availability — a structural split

CANON-002 established that plain text can silently destroy a spatially-argued source. So visual
availability is recorded per book. **OBSERVED:** the library splits into two classes, and the class
determines what a visual pass can even see.

| Class | What a visual pass can recover | Books |
|---|---|---|
| **PDF with a page-image render** | The actual printed page: layout, spacing, position, before/after pairs as the reader saw them | Grammar of the Shot, Grammar of the Edit, In the Blink of an Eye, Albers, The Photographer's Eye, Scientific Advertising, My Life in Advertising, Art & Fear, The Vignelli Canon, Logo Design Love, Discussing Design, 22 Immutable Laws |
| **EPUB with embedded figures** | The figures only. **Page layout does not exist** — an EPUB reflows, so there is no page to inspect | Lupton (293 images), LSM (262), Ogilvy (243), Making and Breaking the Grid (442), Painting With Light (329), Master Shots (124), Hey Whipple (145), The Conversations (144), and others |

Plain-English meaning, and it matters for this batch: for an EPUB I can see the pictures but not the
page. If a book argues through *where things sit on the page* — which is exactly what defeated the
text extraction in CANON-002 — an EPUB cannot support a full visual pass at all. **Lupton is the
sharpest case:** a typography book, in EPUB, whose argument is substantially about page layout, and
whose repository text is already known to have column-interleaving corruption. Its visual completeness
will be recorded as `not_verified`, per the task's visual-evidence policy.

---

## 6. Selection

Coverage quotas are set by the task: at least 3 books in each of five domains across the first 15.
Anchors are marked ★.

### Domain A — static visual design / typography / composition (quota 3)
| # | Book | Source | Visual | Why selected |
|---|---|---|---|---|
| 1 | ★ Lupton, *Thinking with Type* | repo text + EPUB | figures only | Mandatory anchor. Known interleaving corruption — a deliberate test of whether the method detects bad text rather than extracting through it |
| 2 | Albers, *Interaction of Color* | PDF 108pp | page renders | Teaches almost entirely by demonstration; tests a source whose argument is visual by construction |
| 3 | *The Vignelli Canon* | PDF 49pp | page renders | Short, opinionated, aphoristic — a different knowledge shape from a textbook |
| 4 | Samara, *Making and Breaking the Grid* | EPUB | figures only | Partial replacement for the blocked Grid Systems |

### Domain B — photography / lighting / image-making (quota 3)
| # | Book | Source | Visual | Why selected |
|---|---|---|---|---|
| 5 | ★ *Light: Science & Magic* ch.3 | repo text + EPUB | figures only | Mandatory anchor. The most mechanism-heavy source in the library — physical causation, not heuristics |
| 6 | *The Photographer's Eye* | PDF 214pp | page renders | Composition for photography; overlaps Bang's territory from a different craft |
| 7 | Alton, *Painting With Light* | EPUB | figures only | 1949 practitioner text; tests whether an older, discursive voice survives the method |

### Domain C — filmmaking / cinematography / editing / continuity (quota 3)
| # | Book | Source | Visual | Why selected |
|---|---|---|---|---|
| 8 | ★ *Grammar of the Shot* ch.4 | repo text + PDF | page renders | Mandatory anchor. Between-shot claims — the known hard case for frame-by-frame evaluation |
| 9 | *Grammar of the Edit* | PDF 225pp | page renders | Companion volume; tests whether two books by the same authors produce near-duplicate knowledge |
| 10 | Murch, *In the Blink of an Eye* | PDF 81pp | page renders | Editing theory with an explicit priority ordering — a rare ranked decision framework |

### Domain D — advertising / commercial communication / persuasion (quota 3)
| # | Book | Source | Visual | Why selected |
|---|---|---|---|---|
| 11 | ★ Ogilvy ch.2 | repo text + EPUB | figures only | Mandatory anchor. Outcome-claim heavy — assertions about sales, rarely with controls |
| 12 | Hopkins, *Scientific Advertising* | PDF 88pp | page renders | 1923; claims to be empirical. Tests how the schema records a source asserting measurement |
| 13 | Heath, *Made to Stick* | EPUB | few figures | Explicit named framework with six principles — a highly structured source shape |

### Domain E — storytelling / motion / creative process (quota 3)
| # | Book | Source | Visual | Why selected |
|---|---|---|---|---|
| 14 | Catmull, *Creativity, Inc.* | EPUB | few figures | Process and organisational craft, almost no visual argument |
| 15 | Bayles & Orland, *Art & Fear* | PDF 136pp | page renders | Creative process; philosophical rather than procedural |
| 16 | Miller, *Building a StoryBrand* | EPUB | few figures | Explicit narrative framework applied commercially |

**Coverage gap, documented not invented:** the library contains **no animation or motion-graphics
book** — no *Illusion of Life*, no *Animator's Survival Kit*. Domain E is therefore filled with
storytelling and creative-process titles. The task permits using the nearest legitimate available
domain and documenting the gap. Recorded.

### Reserve (books 17–20, and replacements if a selected book blocks)
Prioritised by *different knowledge shape*, not more of the same: Kenworthy *Master Shots* (procedural
recipes), Sutherland *Alchemy* (anti-rational heuristics), Berger *Contagious* (empirical social
claims), Ondaatje *The Conversations* (interview transcript — an unusual form), Hopkins *My Life in
Advertising* (autobiographical), Sontag *On Photography* (essayistic theory), *Logo Design Love*,
*Discussing Design*, *The 22 Immutable Laws of Branding*, *This Is Marketing*, Carroll *Read This If
You Want to Take Great Photographs* (instructional, image-led).

---

## 7. Depth calibration for this batch — stated, not silent

CANON-003 says full cover-to-cover extraction is not required, and asks for "a coherent representative
section large enough to expose the author's reasoning system."

**This batch therefore processes one substantial chapter or equivalent span per book, not the whole
book, and its per-book object counts will be smaller than CANON-001's 55 or CANON-002's 31 where the
section is smaller.** That is a deliberate calibration to the task's stated purpose, which is to
stress the *method* across many source shapes rather than to build maximal knowledge from each.

Stating it here so that a lower object count per book is read as scope, not as declining quality. Where
a section is too small to expose an author's reasoning, the section is enlarged rather than the count
accepted.

---

## 8. Status summary

| Status | Count |
|---|---|
| Distinct titles found locally | 37 |
| Already processed (CANON-001/002) | 2 |
| Blocked on source integrity | 4 |
| **Usable and available** | **31** |
| Selected for the first 16 | 16 |
| Held in reserve | 11 |

**Minimum of 15 is satisfiable. Target of 18 is satisfiable. Maximum of 20 is satisfiable.**
