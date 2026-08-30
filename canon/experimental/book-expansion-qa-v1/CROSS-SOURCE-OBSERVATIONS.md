# Cross-source observations — experimental

> ## OBSERVATIONS ONLY. NOTHING HERE IS PROMOTED.
>
> This file records apparent agreements, contradictions and relationships noticed while extracting
> seventeen sources in parallel. **None of it is a `cross_source_concept`, and none of it may become
> one on the strength of this file.**
>
> SPEC-05 governance rule 5 requires that independence be established from **Audit Gate lineage
> records**, and no source in this run has an audit record — none has passed the gate. Under
> `canon/audit/AUDIT-GATE-v0.2.md` step 7, that blocks cross-source promotion outright.
>
> Several relationships below would be **disqualified anyway** by pairwise dependence. They are
> recorded so that a later reviewer can adjudicate them, not so that anyone can act on them now.

---

## 1. The strongest observation: the evidence-supply gap

This is the run's most consequential finding, and it is **computed, not asserted**. Every extraction
lane independently classified its own objects against the frozen SPEC-03 `evidence.characteristics`
vocabulary, with no lane seeing another's work. Aggregating afterwards:

| Source | Objects | `empirical_within_source` | `controlled_comparison` | `practitioner_assertion` | `outcome_claimed` |
|---|---:|---:|---:|---:|---:|
| Ogilvy, *on Advertising* beyond ch.2 | 70 | 30 | 4 | 70 | 14 |
| Berger, *Contagious* | 54 | 19 | 13 | 1 | 10 |
| Hopkins, *My Life in Advertising* | 70 | 11 | 3 | 70 | 47 |
| Kahneman/Sibony/Sunstein, *Noise* | 50 | 9 | 6 | 2 | 0 |
| Hopkins, *Scientific Advertising* ch.8–21 | 48 | 8 | 1 | 45 | 21 |
| Airey, *Logo Design Love* | 50 | 1 | 0 | 47 | 6 |
| Google, ABCD video ads | 26 | 1 | 0 | 1 | 3 |
| Sullivan, *Hey Whipple* | 70 | **0** | **0** | 70 | 3 |
| Connor & Irizarry, *Discussing Design* | 55 | **0** | **0** | 55 | 0 |
| Ries & Ries, *22 Immutable Laws* | 49 | **0** | **0** | 49 | 25 |
| Samara, *Breaking the Grid* ch.2 | 45 | **0** | 0 | 44 | 0 |
| Carroll, *Read This…* | 30 | **0** | 0 | 30 | 0 |
| Freeman, *Photographer's Eye* beyond 1–3 | 55 | **0** | 8 | 54 | 1 |
| Hunter et al., *Light: Science & Magic* beyond ch.3 | 60 | **0** | 16 | 20 | 0 |
| Godin, *This Is Marketing* | 11 | **0** | 0 | 11 | 2 |
| W3C, WCAG 2.2 | 39 | **0** | 0 | **0** | 0 |
| **Total** | **782** | **79 (10.1%)** | **51** | **569 (72.8%)** | **132** |

**What this says in plain terms.** Across seventeen sources and 782 extracted knowledge objects,
roughly **one object in ten** rests on a measurement the source itself performed and reported. Nearly
**three in four** rest on a practitioner asserting something from professional experience. Six
sources report **no measurement of their own at all**.

**Why it matters to this project.** The Canon exists to supply *requirements* — what a good outcome
must achieve and what to inspect — while the Capability Registry supplies *empirical* fact about what
models can do. The separation is a frozen decision (`coordination/PROJECT-CONTRACT.md`, separations
5 and 6). This table is the first quantified evidence of **how thin the evidential base of the craft
literature actually is**, and it strengthens that separation rather than weakening it: a corpus that
is 73% practitioner assertion is a corpus of well-informed opinion about what to aim for, not a body
of measurement. Treating any of it as capability evidence would be a category error, and now there
is a number attached to why.

**Three qualifications, stated so the table is not over-read:**

1. **The counts are extractor judgements, not audited facts.** Each lane applied the vocabulary in
   good faith and several reported borderline calls explicitly. Nothing has verified them.
2. **A low count is not a criticism of a source.** WCAG scores zero on both because it is a
   *standard* — it specifies thresholds rather than reporting experiments, and its derivation cites
   studies it does not reproduce. *Light: Science & Magic* scores zero on `empirical_within_source`
   but 16 on `controlled_comparison`, because it argues by minimal-pair demonstration — one variable
   changed — which is a different and entirely legitimate evidential form.
3. **Ogilvy's 30 needs review before anyone relies on it.** He reports many specific figures, which
   is why the count is high. But at least one object rests on a **Starch** readership finding, which
   is a third party's measurement reported by the source, not the source's own. SPEC-03 has only one
   slot here, and the Audit Gate design already documents this exact failure on *Made to Stick*
   ("reports measurement constantly, almost none of it their own"). **Flagged for audit; not
   corrected in this run**, because deciding it is an audit-layer question, not an extraction one.

### 1.1 The counter-case, and why it makes the aggregate more trustworthy

*Contagious* is the one source that inverts the pattern, and its lane did the work that makes the
number defensible: it built an **attribution ledger from the book's own Notes before writing any
evidence field**, then checked each candidate against it. Result — 19 objects carry
`empirical_within_source`; 16 rest on formal studies Berger conducted or co-authored, 3 on informal
demonstrations he ran himself (each flagged as informal, with the stricter count of 16 stated so a
reviewer can adopt it instead). **21 distinct third-party studies were identified and excluded**,
including several of the book's most quotable figures — the 7% online figure, the sale-sign result,
the Rule of 100, the 70% rumour decay. Roughly **45% of identifiable measurement in that book is the
author's own.**

That matters twice over. It shows the classification can discriminate — the low counts elsewhere are
not an artefact of a lazy default. And it is the exact inverse of the live *Made to Stick* case the
Audit Gate cites, which means the corpus now holds both poles of the same distinction: a trade book
that reports measurement constantly and almost none of it its own, and one that reports measurement
constantly and nearly half of it its own. **That contrast is the reason the origin question needs its
own audit field rather than one shared characteristic.**

---

## 2. Dependence relationships that would defeat promotion

Recorded first, because they constrain everything else.

| Pair | Relation | Consequence |
|---|---|---|
| `hopkins-my-life-in-advertising` ↔ live `hopkins-scientific-advertising-ch1-7` | `shared_author` | **Not independent.** *My Life* ch.17 is *about* the other book. Agreement between them is one man restating himself across four years. |
| `hopkins-scientific-advertising-ch8-21` ↔ live `hopkins-scientific-advertising-ch1-7` | same work | **Zero independence.** A scope extension, not an origin. |
| `hopkins-my-life-in-advertising` ↔ `hopkins-scientific-advertising-ch8-21` | `shared_author` | **Not independent.** Both lanes recorded recurrences between them; the *My Life* lane flagged two a reviewer should resolve, including a test episode that is probably one event told twice. |
| `light-science-magic-beyond-ch3` ↔ live `light-science-magic-ch3` | same work | **Zero independence.** |
| `samara-breaking-the-grid-ch2` ↔ live `samara-making-breaking-grid-ch1` | same work | **Zero independence.** |
| `ogilvy-beyond-ch2` ↔ live `ogilvy-ch2-advertising-that-sells` | same work | **Zero independence.** |
| `freeman-photographers-eye-beyond-parts1-3` ↔ live `freeman-photographers-eye-graphic-guide` | same work | **Zero independence.** |
| `sullivan-hey-whipple` ↔ live `ogilvy-ch2-advertising-that-sells` | **unresolved** | The Hey Whipple lane **declined to assert independence**: Sullivan quotes an Ogilvy-published book across three chapters, a dependency it judged heavier than a citation. Left open rather than claimed. |

**Net effect: this run adds twelve independent origins, not seventeen.** Five are scope extensions
with zero independence, and *My Life in Advertising* is a new work by an author already in Canon.

---

## 3. Recorded contradictions — none resolved

### 3.1 Ries & Ries versus live Binet & Field (the sharpest)
Five direct contradictions, recorded by the `ries-22-immutable-laws-branding` lane:

- **What advertising does.** Ries: advertising cannot build a brand, is a defence budget, "may not
  pay for itself." Binet & Field report ESOV efficiency and ROMI figures pointing the other way.
- **How brands grow.** Ries rejects widening appeal and caps a brand at roughly half a market.
  Binet & Field make penetration the main driver. *(The lane flagged a frame mismatch — product
  scope versus buyer numbers — rather than treating the clash as clean.)*
- **Universality.** Ries assert the laws apply equally everywhere; Binet & Field explicitly refuse
  universal application.
- **Category context.** Ries: same laws everywhere. Binet & Field: consideration is the master
  context variable.
- **Evidential standard.** Recorded as an asymmetry **without using it to dismiss either side.**

The same lane also recorded **one place the two may agree**, and left that unadjudicated too —
manufacturing agreement is forbidden for the same reason as manufacturing disagreement.

### 3.2 Sullivan versus live Ogilvy and Hopkins
Four judged genuine: whether sales is a sufficient criterion; whether clever headlines help or
attract the wrong readers; whether copy should be cut; and whether practitioner judgement can be
trusted at all — the methodological one, with the most at stake. **Two look opposed and are not**
(where big ideas come from; durability criteria). The lane additionally flagged **three places a
careless consolidator would manufacture a disagreement that does not exist** — product-as-hero
versus brand-is-not-the-hero, superlatives, and committees — recorded precisely *because* the
sources agree there. That negative work is as valuable as the positive.

**Caution:** this pair's independence is unresolved (§2). If the dependency holds, this is not
cross-source disagreement at all.

### 3.3 Same-author self-revision — NOT cross-source disagreement
Three sources revise their own earlier, already-live claims. Each is **one author qualifying
themselves** and must never be presented as two sources disagreeing:

- **Light: Science & Magic** — polarising the source is demoted from a live ch.3 remedy to "a
  solution to avoid whenever possible"; the polariser's place in the remedy order reverses between
  ch.4 and ch.5; the glass-support trick is withdrawn for black subjects in ch.9.
- **Samara** — ch.2 is the book's own counter-argument to the ch.1 material already in Canon.
- **Hopkins** — *My Life* (1927) qualifies a free-sample rule stated in *Scientific Advertising*
  (1923).

### 3.4 Internal tensions inside a single source
The `22 Immutable Laws` lane recorded **six unresolved internal tensions**, sharpest being
"dominate the category" citing 95/80/70% approvingly against a ~50% ceiling stated twice — with
Coca-Cola carrying two different figures in the same book. Recorded, not reconciled.

---

## 4. Apparent convergences — flagged, deliberately not promoted

Each of these is the kind of thing that looks like corroboration and must be adjudicated before it
is treated as such.

1. **Judge the work against a stated objective, not against taste.** *Discussing Design* requires
   every critique to name the objective it judges against. *Hey Whipple* insists on "what's the
   idea?" before execution. *This Is Marketing* asks "who's it for? what's it for?" before anything
   is made. Three independent origins, apparently the same move. **But the mechanisms differ** — one
   is about making feedback checkable, one about separating concept from execution, one about
   audience selection — and SPEC-05 warns that repair follows the mechanism, not the appearance.
2. **Simplify to one idea.** Airey's count-the-devices rule ("one, not two, three or four"),
   Sullivan's reduction arithmetic, Google's "focus the message", Hopkins's specificity doctrine.
   Superficially one principle; four different justifications, and the Hopkins pair is not
   independent.
3. **Comprehension has a time budget.** Sullivan's fuse length / speed-of-the-get, Google's "jump
   in", Airey's silhouette recognition, WCAG's legibility thresholds. **The tempting synthesis is
   almost certainly wrong** — WCAG's thresholds are accessibility conformance criteria and make no
   claim about attention or appeal, a caution its own lane recorded emphatically.
4. **Human judgement of the same artefact varies more than the judges believe.** *Noise* supplies
   the mechanism and the vocabulary; *Discussing Design* supplies the practitioner-side remedy
   (independent judgement before discussion). Genuinely independent origins, genuinely adjacent —
   **the most promising pair in this run for a future promotion**, and still not promoted here.

---

## 5. Gaps this run did NOT close

- **Indic / Devanagari typography** — zero contributors, unchanged. The Dalvi paper's publisher route
  returned HTTP 503 throughout; the thesis remains behind institutional authentication.
- **Indian cultural context** — zero contributors, unchanged. The Cayla & Elson article is paywalled.
- **Physical → generative translation (G11)** — explicitly not attempted. *Light: Science & Magic*
  had six live temptations and parked every one. No source supplies this translation and none was
  invented.
- **Motion design / animated typography** — no source in the library.
- **Steam and food-texture packshot** — the portfolio brief named it; *Light: Science & Magic* has no
  treatment of steam. Recorded as absent rather than manufactured.

---

## 6. Method observations worth carrying forward

1. **Figure loss is the dominant extraction hazard, and it is unevenly distributed.** Samara: 205
   image references, none inspectable, 58% of objects flagged. Carroll: the argument *is* the
   photograph. Freeman: a calibre conversion destroyed the designed spread. Against that,
   *Light: Science & Magic* opened cleanly and 54 figures were inspected — **contradicting the live
   ch.3 audit record, which reports its visual pass as blocked.** That live record now rests on a
   condition that has changed. **Routed for Controller attention; not modified.**
2. **Rendering pages caught errors text alone would have passed through.** The *Logo Design Love*
   caption on printed p.64 calls a failed redesign "successfully renamed" — a translation artefact
   that a text-only pass would have extracted as a confident claim.

2a. **A live Canon finding was extended with new evidence, and sharpened.** The live
   `freeman-photographers-eye-graphic-guide` audit records `false_page_affordance` on the strength
   of **five** broken internal cross-references in Parts 1–3. The scope-extension lane found
   **eight more** in Parts 4–10 and every one is wrong — **nine for nine**, plus the index. It also
   found an asymmetry the live record does not have: the book's **title-level cross-references are
   correct** while its **numeric ones are uniformly wrong**, which is exactly what a conversion that
   re-paginates but preserves text would produce. Notably, the lane **refused the folio mapping its
   own source header asserted** (a detector had reported "printed = PDF − 0" with agreement on 302
   pages) on the correct ground that a calibre conversion matching its own injected folios against
   its own pagination proves nothing. **Routed as an observation; the live record was not modified.**
3. **A copy can be the wrong artefact entirely.** *Logo Design Love* is an unattributed Spanish
   machine translation; the author's English terminology is unrecoverable, and all its ontology terms
   are marked `verbatim: false`. Filename and title were not enough to establish source identity.
4. **Three validators of mine produced false failures before they were right** — chapter numbers read
   as page numbers, `...` elisions, and hyphenation across line breaks. In every case the instinct
   was to "correct" the data, and in every case the data was already right. A validator that has not
   been tested against known-good input is a liability.
