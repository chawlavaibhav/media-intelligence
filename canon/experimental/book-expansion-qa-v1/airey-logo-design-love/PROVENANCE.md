# Provenance — David Airey, *Logo Design Love: A Guide to Creating Iconic Brand Identities*

**EXPERIMENTAL — NOT LIVE CANON.** Extraction lane of the non-merge `book-expansion-qa-v1`
expansion. Nothing in this directory is accepted Canon and nothing here may be described as
accepted, corroborated or admitted.

## Source identity

| Field | Value |
|---|---|
| Title | Logo Design Love: A Guide to Creating Iconic Brand Identities |
| Author | David Airey |
| Publisher | New Riders, Berkeley CA — an imprint of Peachpit, a division of Pearson Education |
| Copyright | © 2010 by David Airey |
| Cover and interior design | David Airey (stated on the copyright page) |
| `source_id` | `airey-logo-design-love` |
| ID prefix | `logo` |
| Local PDF | `/Users/vaibhavchawla/Downloads/Books/Logo Design Love_ A Guide to Creating Iconic Brand Identities.pdf` |
| PDF SHA-256 | `bbd6e5e1292ebdb451b33b8abec80e7c2333bbe22538de4da790a0cebc7d5285` |
| PDF size | 5,968,474 bytes · 217 PDF pages |
| Page-marked text | `scratchpad/src/PDF-logo-design-love.txt` (6,506 lines) |
| Text SHA-256 | `b366ee795862e571130f8360a2b93e285cc67c4ff6554d797e1f10a3fce37601` |

## The single most important provenance fact: this copy is a degraded Spanish translation

**The local copy is not the English original.** Its title page reads *"Logo Design Love: Una Guía
para crear identidades marca icónica"* and the entire body — front matter, all eleven chapters,
captions, footnotes and index — is in Spanish. The bibliographic block (New Riders, Berkeley;
copyright 2010; David Airey) is intact and identifies the work, but no translator, translation
copyright or Spanish ISBN is named anywhere in the file.

The translation is **machine-produced and visibly degraded**. Diagnostic evidence, all observed
directly:

- Proper nouns and studio names are translated as though they were common nouns: the London studio
  **Bunch** appears throughout as *"Manojo"*; **Someone** as *"Alguien"*; **UnderConsideration** as
  *"Bajo consideración"* / *"su examen en"*; **Scion** as *"Vástago"*; **Cool Machine** as
  *"Máquina fresca"*; **Moon Brand** as *"Marca Luna"* / *"la luna Marca"*; **Lindon Leader** as
  *"el líder de Lindon"* / *"Líder Lindon"*; **TIME** magazine as *"HORA"*; the **NAAs** awards as
  *"Anás"*; **TalkMore** as *"HablaMás"*.
- Ligature loss from the underlying text extraction is carried into the translation as word
  breakage: *"una fi signi cativamente precio más barato"*, *"de fi nitivamente"*, *"fi nal"*,
  *"fl ujo"*, *"identi fi ca"*. This is `ocr_degraded`-class corruption of the text layer, not a
  translation choice.
- Occasional sentence-level incoherence where the English syntax has been mangled
  (*"Es las historias que contamos"*, *"Ninguno genuina sin esta firma"*, the page-65 folio rendered
  as the word *"sesenta y cinco"*).

**Consequence for this extraction, stated plainly.** Airey's own English wording is **not
recoverable from this copy**. Every `source_terms` entry in `source-knowledge.yaml` is therefore a
*back-translation into English of the Spanish text actually present*, and is marked
`label_origin: extractor_assigned` and `verbatim: false` in `ontology-mappings.yaml`. The one place
where the brief asked for verbatim vocabulary — Airey's distinction between a *logo*, an *identity*
and a *brand* — is recorded as the **substance** of the distinction with an explicit note that the
exact English words could not be verified here. Any downstream use that needs Airey's actual phrasing
must go to an English edition.

The figures, by contrast, are **unaffected**: the logos, sketches and photographs are the original
artwork and were inspected directly (see below).

## Page mapping and span

The supplied text file header records:

```
PAGE MAPPING DETECTED: printed page = PDF page - 13 (folio agreement on 193 pages).
USE THE PRINTED NUMBER IN LOCATORS.
```

This is **Case 1** of the locator addendum: a PDF with a verified authored folio. All locators in
this lane use the **printed** page number.

- **Offset verified independently by this lane** by rendering pages and reading the printed folio:
  PDF 20 → folio `7`; PDF 36 → `23`; PDF 38 → `25`; PDF 45 → `32`; PDF 50 → `37`; PDF 86 → `73`;
  PDF 124 → `111`; PDF 126 → `113`; PDF 153 → `140`; PDF 201 → `188`. All agree with
  printed = PDF − 13. No disagreeing folio was found.
- **Printed range present in the file:** −11 (PDF 2) to 204 (PDF 217). Negative and zero numbers are
  the marker's arithmetic on the unfoliated front matter, not authored page numbers.
- **Author's own text:** printed **1–191** (Part I opens at printed 1; the last chapter ends at
  printed 191). Printed **192–197** is the "Design resources" appendix (blog and book lists);
  printed **198–204** is the index. **Nothing was extracted from printed 192–204.**
- **Every locator used in this lane falls inside printed 7–191**, and every cited page was read in
  the page-marked text; the pages carrying figures that a claim depends on were additionally
  rendered and looked at.
- **Printed 99–100 (PDF 112–113) contain no extractable text** — they are full-bleed images from the
  Tenth Church project. This is why the page markers jump from 98 to 101. Recorded rather than
  silently passed over.

## Exact material processed

| Part / chapter | Printed pages | Treatment |
|---|---|---|
| Introduction | x–xi | read; not extracted (author's blog credentials, self-promotion) |
| Ch. 1 — There's no escape | 2–7 | extracted (saturation argument, negative-space example) |
| Ch. 2 — It's the stories we tell | 8–21 | extracted selectively (perceived value, consistency, symbols across languages, versatility); the individual client narratives were read for the principle only |
| Ch. 3 — Elements of iconic design | 22–39 | **extracted in full** — the core of this lane |
| Ch. 4 — Laying the groundwork | 42–61 | extracted (brief, questions, field research, competitor research, adjectives, cultural permission) |
| Ch. 5 — Skirting the dangers of a redesign | 62–75 | extracted (redesign risk, Tropicana, New Coke, focus groups, CIGNA, refinement) |
| Ch. 6 — Pricing design | 76–89 | **read and refused in full** — fees, hourly vs fixed rates, print mark-ups, deposits, currency risk, spec work. Business-of-design, out of brief. |
| Ch. 7 — From pencil to PDF | 90–117 | **extracted in full** — mind mapping, sketching, presenting only strong concepts, black and white before colour, context mock-ups |
| Ch. 8 — The art of conversation | 118–141 | extracted (decision-maker access, Enns's four rules, ground rules, strategic-input/execution-freedom, the Yellow Pages comparison method) |
| Ch. 9 — Staying motivated | 144–159 | **mostly refused** — motivational prose and peer quotations. Four items extracted: the Chermayeff qualification (145), stepping away from the computer (149), lateral-thinking manipulations (155), the "dozens of equally valid solutions" claim (153–154) |
| Ch. 10 — Answers to your questions | 160–177 | extracted selectively (look-alike marks, how many concepts, revision rounds, timeframes, competitor research, scalable vector artwork). Refused: portfolio construction, blogging, internships, friends-and-family pricing, workload, employment contracts |
| Ch. 11 — 25 practical logo design tips | 178–191 | **extracted in full apart from tips 1, 3 and 23**, which restate earlier process points already carried by other objects |
| Design resources; Index | 192–204 | not extracted |

## Deliberately not extracted

Per the lane brief: pricing, contracts, invoicing and deposits; spec work and design-contest
argument; self-promotion, blogging and portfolio guidance; hardware and software recommendations as
recommendations; internship and employment advice; and the long client narratives whose only content
is who the client was. Where a narrative carries a reusable mechanism, the mechanism is extracted and
the narrative is not.

## Overlap with live Canon

**None.** This work does not appear in `canon/knowledge/current/` in any span or edition. It is an
**independent origin** against all nineteen live sources. It is **not** a scope extension of
anything live, so no `scope_extension_of` is declared.

Two live sources are near neighbours and were skimmed so that agreement could be distinguished from
restatement. Both relationships are recorded as **observations only**, in prose, in
`EXTRACTION-NOTES.md` — never as ontology relationships, never as `cross_source_supported` evidence,
and never inside a SourceKnowledge object:

- `vignelli-canon-intangibles` — design discipline, aphoristic, normative. Genuinely adjacent on
  simplicity, timelessness and the designer's authority over the client.
- `miller-storybrand-sb7` — brand communication. Adjacent only on the "find the story and tell it"
  line at printed 8; the two works mean quite different things by "story".

## Access basis

The Controller authorised **read-only** use of a copy already present on this machine. The file was
opened for reading and rendering only; it was not copied, redistributed or modified.

**Licence status was not independently verified.** No purchase record, licence, or rights grant for
this copy was checked, and none is claimed. The file additionally appears to be an **unattributed
translation** — it names no translator and no translation copyright, which is itself a reason not to
assert that this copy is a properly licensed edition. This is stated plainly rather than papered over
with an ownership claim that cannot be checked.

## Figure inspection

This is a book about marks, so a text-only pass would lose the evidence. **Twenty-two pages were
rendered with `pdftoppm` at 100–300 dpi and looked at directly.** The full inventory, and the honest
count of which objects rest on an inspected figure versus on text alone, is in `EXTRACTION-NOTES.md`.
