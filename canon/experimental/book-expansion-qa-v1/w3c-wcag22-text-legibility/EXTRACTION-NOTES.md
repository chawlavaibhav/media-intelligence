# Extraction notes — W3C, WCAG 2.2 (Guideline 1.4, glossary, Understanding notes)

**EXPERIMENTAL — NOT LIVE CANON.** Lane 3, `book-expansion-qa-v1`. Nothing here is accepted Canon.

## Counts

| File | Objects |
|---|---|
| `source-knowledge.yaml` | **39** SourceKnowledge objects |
| `source-concept-systems.yaml` | **4** SourceConceptSystems |
| `operational-bindings.yaml` | **10** OperationalBindings (6 evaluation, 2 governance, 2 benchmark) |
| `ontology-mappings.yaml` | **26** terms, **14** relationships, **5** concepts |
| `qa-bank.yaml` | **41** Q&A items |

`requires_application: true` — **16 of 41 = 0.390** (contract minimum 1/3 = 0.333).

Authority split of the SourceKnowledge objects: **29 normative** (`sk_wcag_0001`–`0029`, supported by
Success Criteria or the glossary) and **10 non-normative** (`sk_wcag_0030`–`0039`, supported only by
"Understanding" W3C Working Group Notes).

Answer-type mix: mechanism 10 · boundary_condition 7 · comparison 5 · application 5 ·
concept_definition 4 · source_position 4 · factual 2 · failure_diagnosis 2 · tradeoff 1 · repair 1.
Difficulty: 25 hard, 16 medium, 0 easy — deliberate. An easy question about this source is a question
any model answers from latent knowledge.

## Method

1. Read the whole supplied file. Part 1 (Guideline 1.4 criteria) and Part 2 (glossary) are normative;
   Part 3 is seven non-normative Understanding documents.
2. Extracted along the four axes the brief prioritised — mechanism, decision rule, boundary condition,
   exception — rather than by document order. The exceptions and the notes attached to definitions
   turned out to carry most of the real content, exactly as the brief predicted.
3. Tracked authority level per object from the start rather than as a post-hoc annotation. Every
   SourceKnowledge object carries a `source_stated` caveat naming its level; every Q&A `support` field
   repeats it; the Understanding-only objects are grouped as Part C of the file and their caveats begin
   `NON-NORMATIVE —`.
4. Wrote no locator that was not verified against the source file.

## Locators — no page numbers exist and none was invented

Every `provenance.page_start` and `page_end` is `null` in all 39 objects, mechanically verified. Real
locators live in `provenance.section`: a Success Criterion number and title, a glossary term with the
note number, or an Understanding document with a section heading.

**Verification performed (self-check item 2, exhaustive):**

- Every Success Criterion cited (1.4.1, 1.4.3, 1.4.4, 1.4.5, 1.4.6, 1.4.8, 1.4.9, 1.4.10, 1.4.11,
  1.4.12) was confirmed present in Part 1.
- Every glossary term cited (`contrast ratio`, `relative luminance`, `large scale (text)`,
  `image of text`, `text`, `pure decoration`, `essential`, `normative`, `informative`,
  `user interface component`, `CSS pixel`, `blocks of text`) was confirmed to be a real entry inside
  the Part 2 glossary block, matched as a standalone entry line rather than as an incidental mention.
- Every Understanding section heading cited (18 distinct headings) was confirmed present in the file.
- Every Understanding document cited corresponds to one of the seven actually supplied. No object
  cites an Understanding note for SC 1.4.6, 1.4.9 or 1.4.10, because none was supplied.
- Roughly forty substantive quoted strings and stated values were grep-confirmed against the source,
  including `1pt = 1.333px`, `18.5px and 24px`, `4.499:1`, `2.999:1`, `#FFF000` at `1.2:1`, `#DEDEDE`
  at `15:1`, F24, F83, G148, `law of continuity`, `rivers of white`, the logo `not "essential"`
  sentence, and the `return to the required values` condition.

## Self-check results

1. **All five YAML files parse** (`yaml.safe_load`). Confirmed.
2. **Locators verified** — see above. Every Q&A locator names a real SC number, a real glossary term or
   a real Understanding section, and the cited location supports the answer.
3. **No object claims WCAG endorses a creative or commercial outcome.** A regex scan of every `claim`
   and `mechanism.text` for effectiveness vocabulary returned four hits, all false positives on
   ordinary English: "the halo becomes the *effective* background", "rather than *converted*",
   "prescribing *effective* general use color pairs" (a verbatim source phrase about colour pairs for
   contrast), and "*converts* a contrast question into a comprehension question". The extrapolation to
   creative assets appears only in bindings, all of which carry
   `evidence_basis: extractor_inference` except the three that are about handling the standard itself.
4. **Every object records its authority level.** Verified mechanically: all 39 objects carry a caveat
   with `origin: source_stated` naming normative or non-normative status, and all 41 Q&A `support`
   fields state it.
5. **`requires_application` fraction: 16/41 = 0.390**, above the 1/3 floor.

Schema conformance also checked mechanically: required SourceKnowledge keys present on all objects;
`evidence.characteristics` non-empty and drawn from the fixed list; `source_uncertainty` and
`extraction_uncertainty` from their enums; `intra_source_relations[].relation` from the fixed
vocabulary (an early draft used `related_to`, which is an *ontology* relation and not a SPEC-03 one —
corrected); every `sk_` / `scs_` / `t_` reference resolves inside this lane; `evaluation` bindings all
carry an `observation_unit`; the governance bindings carry consumers from the permitted list; no
binding uses `cross_source_supported` or `empirically_supported`; every `kind: remedy` term carries
`executable_by`; both canonical concepts carry `asserts_equivalence: false` and
`purpose: retrieval_and_aggregation`; no `xs_` concept and no `same_failure_family` relation exists.

## The central caution — how it was handled

The brief's warning was the governing constraint on the whole extraction: these are web-accessibility
conformance thresholds, not commercial-creative legibility rules.

Three mechanisms enforce it:

1. **Scope is stated inside every object.** `scope.domain_discussed_by_source` is
   `web_content_accessibility_conformance` on all 39 objects (with `low_vision_readership`,
   `colour_vision_deficiency` or `cognitive_disability` added where the source names them). It is never
   a creative domain, because the source never discusses one.
2. **The application is quarantined in bindings.** Seven of the ten bindings carry
   `evidence_basis: extractor_inference`, and each `applicability.limits` states the web-versus-creative
   gap in its own terms rather than by boilerplate. `bnd_wcag_008` exists specifically to constrain our
   own use: a WCAG threshold may be applied only with its purpose and authority level attached, and
   never retrieved as a bare number.
3. **Two Q&A items attack the confusion head-on.** `qa_wcag_0036` puts the question a brand team would
   actually ask ("does WCAG say our advertisement is illegible?") and answers it with what the source
   claims and does not claim. `qa_wcag_0022` separates "no contrast requirement" from "is readable" —
   the standard withdraws its test, it does not certify the outcome.

## Normative / non-normative — how the split was handled

This is the first Canon-adjacent source with a formally declared internal authority split, and it
declares it in its own glossary: *normative* is "required for conformance", *informative* is "for
information purposes and not required for conformance", and content identified as informative or
non-normative "is never required for conformance".

The split is not administrative. Almost everything that makes this standard *intelligible* sits at the
weaker level. The criteria state thresholds and exceptions; the reasoning, the worked examples, the
colour values, the testing procedures and every candid admission of the standard's own limits are in
Working Group Notes. An extraction that flattened the two would have produced a corpus that could not
tell a requirement from a rationale.

Handling:

- The file is physically split into Part A (criteria), Part B (glossary) and Part C (Understanding
  only), with Part C's header stating that none of it may be presented as a requirement.
- `sk_wcag_0029` records the source's own definition of its two levels, so the distinction is itself
  extracted knowledge rather than only extractor metadata.
- Where a normative clause and a non-normative note pull against each other, the tension is recorded
  rather than resolved. The clearest case is `sk_wcag_0034`: SC 1.4.3 exempts logotype text
  unconditionally, while the SC 1.4.11 Understanding note says a low-contrast logo presentation chosen
  by the author is not essential and not exempt. The object states both and says plainly that an
  evaluator enforcing the note is applying a Working Group Note as if it were a requirement.
- `qa_wcag_0020` is built entirely on this: it gives an auditor's over-claim ("WCAG requires you to
  exceed 4.5:1 when using a thin typeface") and asks for the correction.
- `bnd_wcag_007` binds the distinction to `evidence_interpretation` governance, because a retrieval
  layer that cannot represent "the source states this, but only in material it itself classifies as
  not required" will eventually serve a rationale note as a rule.

## Where I was tempted to over-claim, and did not

1. **The 80-character line length.** This is the single most quotable line in the source for a
   typography corpus, and the temptation was to extract it as "WCAG says lines should be at most 80
   characters." It does not. SC 1.4.8 requires that *a mechanism be available* to achieve that width,
   its Note 1 says content is not required to use the value, and the mechanism may be supplied by the
   browser rather than by the content. It is Level AAA. `sk_wcag_0013` and `qa_wcag_0018` state the
   availability framing explicitly, and `qa_wcag_0014` names it again.

2. **The four SC 1.4.12 spacing values.** Same trap, same shape — 1.5x line height reads like a
   typographic specification and is not one. `sk_wcag_0012` leads with the resilience framing and
   carries an extractor caveat saying these are the most commonly misread values in the criterion.

3. **A `creative_ir` binding.** SPEC-01 was not supplied to this lane. Several bindings would have been
   natural fits for a text-overlay or hierarchy path, and I could have guessed at plausible path names.
   Guessing would have produced a binding that resolves to nothing. **Zero `creative_ir` bindings**, as
   the brief anticipated.

4. **A cross-source concept.** The adjacency to Albers is genuinely interesting — one source says a
   colour cannot be pinned down by name, the other computes one colour property to two decimal places.
   Writing that up as a `cross_source_concept` was tempting and is forbidden here; it would also have
   been wrong on the merits, since the two are answering different questions rather than agreeing or
   disagreeing. Recorded as prose in `PROVENANCE.md` under "Overlap with live Canon", nowhere else. No
   `xs_` concept exists, and no cross-lane ontology relationship was written, since the parallel lanes'
   term ids are not resolvable from here.

5. **The "thin strokes are harder to read" note.** This is the most useful sentence in the source for a
   creative corpus, and it is *normative in placement* — Note 1 to the glossary definition of large
   scale. The temptation was to treat it as a rule. It is not: no criterion converts it into a test,
   and `sk_wcag_0022` says so in its own caveat. `qa_wcag_0033` is built on exactly this gap — a
   hairline face at 4.6:1 passes, the source raises two concerns about it, and the source stops short
   of saying it fails anything.

6. **Text over photographs.** The obvious move was to write an evaluation binding that computes a mean
   background luminance and reports a ratio. The source does not define one: it names the situation as
   failure F83 and defines its measurement against a *specified* background. `bnd_wcag_003` therefore
   flags the condition as unmeasurable-as-specified rather than manufacturing a number, and
   `qa_wcag_0035` asks directly what the source gives you and what it does not.

7. **`empirically_supported` on the ratio derivation.** The Understanding note cites real studies
   (ARDITI-FAYE, GITTINGS-FOZARD) for the contrast-sensitivity figures, which briefly looked like
   grounds for that `evidence_basis` value. It is forbidden in this task and would have been wrong
   anyway: the studies are cited, not reproduced, and no Empirical Memory reference exists. The
   citations are recorded as a caveat on `sk_wcag_0030` instead.

## Deliberately not extracted

- **SC 1.4.2 Audio Control** and **SC 1.4.7 Low or No Background Audio** — audio criteria, outside the
  brief.
- **SC 1.4.13 Content on Hover or Focus** — a pointer-interaction criterion. Its subject matter appears
  only where the SC 1.4.11 note discusses hover states in contrast terms (`qa_wcag_0029`).
- **The Techniques and Failures lists as objects.** G-numbers and F-numbers are cited inside objects and
  Q&A items where they carry a decision (G148's specify-neither strategy, F24, F83), but the technique
  catalogue was not extracted wholesale — the source itself states that techniques are informative,
  that a technique may go beyond the minimum, and that other ways of meeting a criterion exist.
- **Non-visual glossary entries**, the Input Purposes list, the Change Log and the Acknowledgments —
  read for context, no reusable principle.
- **SC 1.4.11's focus-indicator material** (Relationship with Focus Visible, Figures 8–14). It is rich
  and precisely drawn, but it is about interaction state in web components with no analogue in the
  static or time-based creative surfaces this Canon addresses, and extracting it would have padded the
  object count without adding transferable mechanism.

## Hazards and known limits

**`figure_semantic_binding_lost` — assessed, and NOT triggered.** The Understanding documents reference
48 numbered figures and none was inspected; the supplied file carries their captions and surrounding
prose only. This would ordinarily be a serious loss for a visual source. It is not here, because this
source's captions are unusually self-sufficient: they state the hex values and the computed ratios in
words (`#767676` on white; `2.7:1`; `#FFF000` to white at `1.2:1`; grey `#949494` at `3:1`), so the
figures illustrate propositions the text states rather than carrying meaning the text omits. Objects
resting on caption content carry `extraction_uncertainty: figure_not_inspected` — `sk_wcag_0034`,
`sk_wcag_0036`, `sk_wcag_0038` and `scs_wcag_004` — and the Q&A items drawing on them say so in their
`support` fields. The one place a figure might carry something the text does not is
Understanding SC 1.4.11 Figure 41 (a gradient behind an "i"), where the point is visual by nature; no
object depends on it.

**The measurement procedure does not survive the surface change.** Several of the source's most precise
instructions presuppose a live rendering pipeline: obtain the point size from the user agent; refer to
the colours in the markup rather than the pixels on screen; evaluate the pairs an author expects to
appear adjacent. A delivered raster has no user agent to ask and no stylesheet to read, and the source
itself warns that point sizes set inside an image editor are unreliable because applications default to
different pixel densities. `bnd_wcag_002` records this gap as ours rather than as a defect in the
source.

**Two threshold regimes that look like one.** SC 1.4.3 measures against "the specified background";
SC 1.4.11 measures against "adjacent color(s)". The glossary note fixing the background rule names
SC 1.4.3 and SC 1.4.6 explicitly and so does not, on its face, govern SC 1.4.11. Recorded as a caveat
on `sk_wcag_0016`. Anything consuming both criteria must keep the two comparisons distinct.

**The Understanding notes are a moving target.** They are Working Group Notes and are revised
independently of the Recommendation. This extraction reflects the supplied capture. The Recommendation
itself carries a 2024-12-12 republication with errata, recorded in `PROVENANCE.md`.

**Negative findings recorded rather than discarded.** Four `distinct_from` relationships in the
ontology exist because a resemblance was examined and rejected: colour-alone encoding versus
insufficient contrast (the source separates them explicitly with worked examples); insufficient
contrast versus the nominal-pass problem (same appearance to a reader, opposite verdicts under the
standard); image of text versus text; and F24 versus F83 (a failure of specification versus a failure
of the specified pair against an image). Without these, the same false merges get proposed again.

## What this source contributes that the corpus did not have

Three things, stated as observations about the corpus rather than as claims about the world.

1. **A checkable numeric criterion with a published derivation.** Not just the number, but where it
   came from, what it compensates for, and where its authors say it stops working. Live Canon holds no
   numeric acceptance criterion of any kind.
2. **Formally drawn exceptions.** The exception structure is the most valuable material here and it is
   drawn with a precision practitioner texts do not attempt: four incidental situations, a two-part
   essential test, a substitution test for decoration, and a boundary between a picture containing text
   and text made into a picture. A single stimulus — letterforms inside an image — routes to four
   different verdicts on facts that are stated rather than visible.
3. **A source that marks its own authority levels.** Every other Canon source states everything at one
   level and leaves the extractor to distinguish assertion from demonstration. This one does the work
   itself, and `bnd_wcag_007` proposes that the precedent inform how evidence is weighted generally.

The honest limit on all three: it is a web-accessibility conformance standard, and it does not claim,
anywhere, to be a theory of what reads well.
