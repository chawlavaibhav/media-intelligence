# Extraction notes — Light: Science & Magic, 5th ed., the chapters BEYOND chapter 3

**EXPERIMENTAL — NOT LIVE CANON.** Lane of `book-expansion-qa-v1`. Non-merge, exploratory. Nothing
here is accepted Canon and nothing here may be described as accepted.

`source_id: light-science-magic-beyond-ch3` · ID prefix `lsmx` ·
`scope_extension_of: light-science-magic-ch3` · `independence: none — same work`

---

## 1. Counts

| | |
|---|---|
| SourceKnowledge objects | **60** |
| SourceConceptSystems | **5** |
| OperationalBindings | **13** (2 creative_ir · 7 evaluation · 1 production · 2 governance · 1 benchmark) |
| Ontology terms | **47** (14 property/entity · 11 problem · 22 remedy) |
| Ontology relationships | **16** · concepts **5** |
| Q&A items | **62**, of which **25 `requires_application: true` = 40.3%** (requirement: ≥ 33.3%) |

Chapter distribution of the SourceKnowledge objects: ch. 4 — 14 · ch. 5 — 10 · ch. 6 — 14 ·
ch. 7 — 11 · ch. 8 — 2 · ch. 9 — 6 · ch. 10 — 3.

Evidence profile: `mechanism_given` on **58 of 60** objects and `mechanism.stated_by_source: true`
on the same 58. Only two objects carry `mechanism_absent` — the source's own division of its subject
matter (`sk_lsmx_0002`) and the hard-shadow visibility claim (`sk_lsmx_0018`), which the authors
assert without explaining. That ratio is the expected one for these authors and was the brief's own
test for whether I was extracting or summarising.

---

## 2. Method

1. Read the Table of Contents at spine 7 and established the real chapter boundaries, because the
   `<<<SPINE … | TITLE …>>>` markers take each document's *last* heading and are therefore misleading
   as chapter titles (see `PROVENANCE.md` §3).
2. Read chapters 4, 5, 6, 7, 9 in full and chapters 8 and 10 in full with a narrow extraction filter.
3. Extracted the EPUB's image directory and built nine labelled contact sheets covering every matched
   pair on which a claim here depends; inspected all nine.
4. Wrote `source-knowledge.yaml` incrementally in four appended chunks, and the Q&A bank in four,
   parsing the file after each. Two earlier attempts at this lane died mid-write on single very large
   writes; nothing here was written in one pass.
5. Ran the mechanical self-checks in §7 and fixed every failure they found.

---

## 3. `figure_semantic_binding_lost` — and why it is *smaller* here than expected

**Audit caution recorded: `figure_semantic_binding_lost`.** This book argues through diagrams and
matched before/after photographs, and a reflowable EPUB gives figures without page layout. The
caution stands. But the honest report is that it bit far less hard here than the brief anticipated,
and the reason is worth recording precisely because it says nothing good about this extraction.

**The live chapter-3 record is `blocked_visual_validation`: all fourteen of its figures went unseen,
because macOS privacy protection over `~/Downloads` made the EPUB unreadable during CANON-003. That
block is gone.** The file opened. I inspected **54 figures**.

| | count |
|---|---|
| Distinct figures cited across the 60 objects | 129 |
| Distinct figures actually opened and looked at | **54** |
| Of those, cited in an object and recorded in `provenance.inspected.figures` | **53** |
| Objects whose `source_support` is `text_and_visual` | **28 of 60** |
| Objects carrying `evidence.characteristics: visually_demonstrated` | **28 of 60** |
| Objects carrying `extraction_uncertainty: figure_not_inspected` | **18 of 60** |
| Objects citing no figure at all | 11 |

**So roughly 47% of the objects rest partly on a figure I saw, 30% cite a figure I did not open, and
the remaining 23% cite none.** Of the 129 cited figures, 76 were not opened. Almost all of those are
lighting *diagrams* whose geometry the prose states explicitly (4.1, 4.4–4.8, 5.7–5.8, 5.19–5.24,
6.1–6.6, 6.13–6.16, 6.18, 6.20–6.22, 6.25, 6.28, 6.30, 6.32, 7.3–7.4, 7.6–7.7, 9.13, 9.17, 9.19), plus
the chapter-9 characteristic-curve graphs and the chapter-10 mixed-colour diagrams. I did not infer any
visual claim from text alone in those cases; where a claim depends on a diagram I did not open, the
object says so in a caveat and the claim is stated as the source states it, not as I would read the
picture.

**What the inspection actually bought.** Every matched pair on which a load-bearing claim rests was
checked, and each confirmed the prose: 4.17/4.19 (raking light versus a large source filling the family
of angles on black leather — the embossed pattern really is invisible in one and fully legible in the
other); 6.7/6.9/6.12/6.17 (bright, dark and compromise metal, and the light-distance pair where the
background lifts and the blade does not move); 6.23/6.24 (the metal box on a dark table losing its
front and bottom, and on a light one not); 6.26/6.27 (the polarizer blacking the glass support and
leaving the metal); 7.1/7.2 and 7.5 (the failed glass, bright field, dark field); 7.21/7.23 (murky beer
and the cut secondary background); 9.11/9.12, 9.22/9.23 (the key asymmetry in both directions);
9.24/9.25 (paper against velvet at identical exposure).

**One place where the picture is weaker than the prose.** 7.24/7.25, the labelled bottle with and
without the gobo, shows a real but subtle improvement — smaller than the text implies. That is recorded
in `sk_lsmx_0049` as an `extractor_observed` caveat and repeated in `bnd_lsmx_007`, because it is the
one case where I would have over-recorded had I not looked.

**The asymmetry must travel with this lane.** The live chapter-3 objects and these objects do **not**
have the same evidential standing. A reader comparing them should not read `visually_demonstrated` here
as a sign of greater care — it is a sign that the file opened. Any later use that pooled the two spans
would silently mix a fully text-only extraction with a partly visual one.

---

## 4. Where the later chapters QUALIFY chapter 3 — the authors qualifying themselves

Recorded faithfully and, in every case, **as one author team revising its own earlier statement within
a stated scope. None of this is cross-source disagreement and none of it may be presented as two
sources conflicting.** All three are also bound as a governance precedent in `bnd_lsmx_011`.

1. **Polarizing the source is demoted from a remedy to a last resort.**
   Live `sk_lsm_c003_0019` states that placing a polarizing filter over the light turns direct
   reflection into polarized reflection, which a lens polarizer can then manage. `sk_lsmx_0009`
   (ch. 4 sidebar) attaches the price the live object does not carry: *"Polarizing the light source has
   serious drawbacks and is a solution to avoid whenever possible."* Four to six stops in practice
   rather than the theoretical two, depth-of-field and movement consequences, heat damage to the
   filters, a colour-balance shift, and the observation that some photographers go for years without
   needing it. `origin: source_stated`.

2. **A polarizer's place in the remedy order is reversed between chapters 4 and 5.**
   Chapter 4 offers the polarizer among the *first* remedies for competing surfaces. Chapter 5's
   glossy-box ladder demotes it to a next-to-last resort, with the optical reason stated: a box carries
   polarized reflection on more than one face, polarized in mutually perpendicular planes, so removing
   one effectively increases another. Recorded in `sk_lsmx_0023` and in `scs_lsmx_003`'s tradeoffs.

3. **The metal chapter's glass-support-plus-polarizer trick is explicitly withdrawn for black subjects.**
   `sk_lsmx_0036` (ch. 6) builds it; `sk_lsmx_0057` (ch. 9) withdraws it, on the stated ground that much
   of a black subject's direct reflection is likely to be polarized too, so the filter that clears the
   support would probably blacken the subject. Recorded as `intra_source_relations: contradicts` between
   the two objects, with the scope difference named.

A fourth, weaker case: chapter 6 states that its glossy-box theory is *identical* to chapters 4 and 5
but that the material difference makes them likely to apply it **the opposite way** — create the direct
reflection rather than avoid it (`sk_lsmx_0035`). That is an inversion of prescription rather than a
qualification of a claim, and is recorded as such.

---

## 5. What is deliberately NOT extracted

**Chapter 3, entirely.** The three reflection types, the angle-independence of diffuse reflection, the
mirror-image property of direct reflection, the inverse-square behaviour of each, the polarization
mechanism, the family of angles itself, and the refusal of the word *specular* are all live Canon and
are **referenced, never restated**. Twelve objects carry an `extractor_observed` caveat naming the live
`sk_lsm_c003_*` object they build on. A mechanical diff of concept labels against the live
`source-knowledge.yaml` returns **zero exact collisions**; the highest string similarity across the
60 × 20 comparison is 0.56, between
`copy_work_wants_diffuse_reflection_only_so_the_light_goes_outside_the_family` and
`diffuse_reflection_follows_the_inverse_square_law` — a coincidence of shared words, not of content.
**No near-duplicate was kept**, because none was found.

One benign artefact of the check: `sk_lsmx_0001` has `provenance.section: "opening"`, which is also the
section string of live `sk_lsm_c003_0001`. The chapters differ (`4 — Surface Appearances` versus `3`),
so there is no locator collision.

**Live-ontology correspondences, recorded as prose rather than as relationships.** Several terms here
plainly extend live chapter-3 terms — `t_lsmx_0002`/`t_lsmx_0003` (bright and dark field) are
applications of the live `family_of_angles`; `t_lsmx_0005` (effective size of the light) extends the
live account of source size; `t_lsmx_0021` (disappearing metal edge) is a consequence of the live claim
that a direct reflection is as bright as its source. **No relationship object was written to any of
them.** This lane is the *same work*, so a mapping asserting anything about those terms would be the
book agreeing with itself dressed as evidence. Recorded here, in prose, where it cannot be mistaken for
corroboration.

**Refused outright**, per the extraction stance:
- Chapter 11, *Setting Up Your First Studio* — studio-space logistics, what stands and modifiers to buy.
- The Appendix of reliable suppliers.
- Most of chapter 10: the hot-shoe flash and LED hardware survey, battery packs, flash extenders,
  feathering as a property of particular reflector designs, the Omni-Bounce.
- Most of chapter 8: posing, wardrobe, the broad/short stylistic preference, the low-key/high-key mood
  taxonomy, and the light-by-light catalogue (fill, background, hair, kicker, rim). Only three
  mechanism-bearing claims survived, and they collapsed into two objects.
- Chapter 9's histogram and curves material as *software instruction*; the parts retained are the
  characteristic-curve mechanism and the unrecoverability of compression, both labelled
  `historical_claim`.
- Chapters 1 and 2, which precede the live span.

---

## 6. Technology contingency — optical geometry versus gear

Kept apart deliberately. **Six objects carry `historical_claim`**, and each says in a caveat what
exactly is contingent:

| Object | What is contingent |
|---|---|
| `sk_lsmx_0009` | film colour-compensating-filter advice; the heat behaviour of period polarizing material |
| `sk_lsmx_0034` | named perspective-control lens manufacturers and their movement range versus view cameras |
| `sk_lsmx_0052` | the S-shaped characteristic curve is a property of film and of this edition's sensor generation; the source itself notes Raw straightens it |
| `sk_lsmx_0053` | the noise argument for over-exposing black-on-black is sensor-generation dependent, and the source says so |
| `sk_lsmx_0058` | the catalogue of nonstandard sources — mixed-age fluorescent tubes, early LED panels the authors say they are not satisfied by |
| `sk_lsmx_0060` | the prepress and image-editing workflow remarks |

Everything else in the lane is optical geometry — families of angles, reflection channels, source size
and distance, refraction — and is durable. The one perceptual claim that is neither
(`sk_lsmx_0015`, learned reading of perspective distortion) carries `culturally_bounded`, as does
`sk_lsmx_0024`'s note that flare is currently fashionable in fashion and glamour work.

Two objects carry `anecdotal`: the department-store catalogue cover camouflaged with ribbon and greenery
(`sk_lsmx_0037`) and the report of other photographers tenting glass (`sk_lsmx_0043`).

---

## 7. Self-check results

Run mechanically. Every check below was executed in code against the written files, not asserted.

1. **Every YAML parses.** All five YAML files load under `yaml.safe_load`. ✅

2. **No page number anywhere; every `page_start`/`page_end` null.**
   - `page_start`/`page_end` non-null in any SourceKnowledge or SourceConceptSystem object: **0**.
   - Regex `\b(pp?\.|page)\s*\d` swept across **all seven files** in this directory: **0 hits**.
   - **Spot-check of cited locators, all 60 objects, not merely 20**: every `provenance.section` was
     normalised and searched for verbatim in the source text. **60/60 found; 0 failures.** The section
     names are the book's own headings.
   - **Quotation check, 161 `source_terms` strings**: first pass found **3 failures**, all of the same
     kind — I had joined two separated sentences with an ellipsis, which is not verbatim. All three were
     split into their two exact quotations (`sk_lsmx_0036`, `sk_lsmx_0051`, `sk_lsmx_0055`). Re-run:
     **161/161 found verbatim.** ✅

3. **No chapter-3 duplication.** Concept labels diffed against the live
   `canon/knowledge/current/light-science-magic-ch3/source-knowledge.yaml`: **0 exact collisions**,
   highest similarity 0.56 and semantically unrelated. **No near-duplicate kept, because none exists.**
   See §5. ✅

4. **Every physical-production binding is parked, not translated.** Verified in code:
   - Bindings with `target_type: production`: **exactly 1** (`bnd_lsmx_010`), carrying
     `status: production_candidate` and `target_path: null`. It references 33 SourceKnowledge objects
     and 2 systems — the whole physical procedure set of these chapters — and its
     `applicability.limits` states the refusal explicitly.
   - Remedy terms: **22**, of which **20** carry `physical_production` and **18** carry it as their only
     value. The other four are `human_edit` where the source's own remedy is a person editing an image
     or making an editorial decision (retouch the reflection; decide the principal subject) or both
     (`expose_toward_the_middle_of_the_curve_and_correct_afterwards`,
     `compose_out_the_highlights_that_a_global_correction_will_colour`).
   - `generative_respecification` appears **nowhere in the lane**, on any term.
   - A regex sweep for generative vocabulary (`prompt`, `regenerate`, `negative prompt`, `seed`,
     `inpaint`, `controlnet`, `diffusion model`) over all seven files returns hits **only inside the
     refusal statements themselves** — the header of `operational-bindings.yaml`, the header of
     `source-knowledge.yaml`, and `bnd_lsmx_010`'s `limits`. No occurrence is a translation. ✅

5. **Application fraction, computed in code: 25 of 62 = 40.3%**, above the required one third. ✅

6. **Reference integrity.** All binding `source_knowledge_refs` / `source_system_refs` resolve inside
   the lane; all `failure_ontology_refs` / `repair_ontology_refs` are SPEC-05 term ids from this lane's
   own `ontology-mappings.yaml`, never raw source strings; all system `members[].sk_ref` and all
   ontology `arising_from` resolve; all intra-source relation targets resolve. **0 dangling.** ✅

7. **Vocabulary.** All `evidence.characteristics`, `answer_type`, `difficulty`, `knowledge_type`,
   `observation_unit`, `governance_consumer`, `evidence_basis` and relation values are from the fixed
   lists. No `xs_` concept, no `same_failure_family`, no `cross_source_supported`, no
   `empirically_supported`, no decimal confidence anywhere. ✅

8. **Figure-inspection honesty.** Every figure recorded in any `provenance.inspected.figures` was
   checked against the list of images actually opened. First pass found **one over-claim**: six
   chapter-9 figures were listed as inspected on `sk_lsmx_0056` from a contact sheet I had built but not
   opened. I opened it, confirmed the claims, and re-ran. **Claimed-but-not-viewed: 0.** ✅

9. **Project validator.** `validate_experimental.py` reports this lane clean; the only errors it emits
   for `light-science-magic-beyond-ch3` were the missing `EXTRACTION-NOTES.md`, which this file
   resolves. Other lanes' errors are their own.

---

## 8. Where I was tempted to translate physical advice into generative advice — and did not

Recorded because the brief asked, and because these were real temptations rather than hypothetical ones.

1. **"Move the light outside the family of angles."** The single most reusable sentence in the book, and
   the one the project has been burned on. It is a statement about a light stand in a room. It appears in
   this lane only inside `bnd_lsmx_010` (parked) and as ontology term
   `t_lsmx_0028`/`t_lsmx_0026` with `executable_by: [physical_production]`. It is not paraphrased as a
   lighting-direction prompt token anywhere.

2. **The metal exposure rule.** "Spot meter the metal and open two to three stops" reads like a
   parameter, and the pull to write it as a brightness target for a rendered surface was strong. It is a
   statement about a meter and a physical camera and stays in `sk_lsmx_0029` in that frame. What *is*
   bound, in `bnd_lsmx_005`, is only the observable consequence: metal sitting at a plausible mid grey
   across its whole area is showing the tonal signature of a diffuse surface, which is something you can
   look at in a finished image.

3. **The 10–25× dark-field source size.** A number, attached to a subject dimension, in a book that gives
   almost no numbers. It is very easy to restate as a ratio for a described lighting setup. It describes a
   physical panel around a physical bottle and is left there (`sk_lsmx_0041`).

4. **The half-to-one-stop background separation window.** The most quotable figure in the extremes
   chapter. I bound it in `bnd_lsmx_008` as something to *measure in a finished frame*, and the binding
   says in terms that the source states it for its own examples and not as a universal. It is not offered
   as a target to specify.

5. **"Light black-on-black as if it were metal."** Reads almost like a style instruction. It is a
   procedure — find the family of angles and fill it — and both halves are physical. Kept in
   `sk_lsmx_0057` and parked.

6. **The cut secondary background behind a glass of liquid.** The most valuable single procedure in the
   span for the product/packshot gap, and the one where the temptation to write "specify a bright
   controlled surface behind the liquid" was strongest. It is five physical steps involving a test light,
   a felt-tip marker, a pair of scissors and a wire. `bnd_lsmx_006` binds only the *diagnosis* — a liquid
   reading murky, and the container's wider field of view — and says explicitly that the remedy is not
   bound.

In every case the discipline was the same: **the observable consequence in a finished image can be
bound as an evaluation; the physical act that produces it cannot be bound at all, and is parked in the
source's own frame.** The gap ledger's G11 — physical-to-generative translation — is not closed by this
book, and I have not pretended otherwise.

---

## 9. What this lane is actually for, stated plainly

The gap ledger records **G4 (product / packshot appearance)** as open, and the CANON-V1 portfolio names
this span as candidate **P1** on the grounds that the Canon holds the theory and stops before the
application. That is what this lane closes, and the highest-value material is, in order:

1. **Metal (ch. 6) as the complete worked product case.** The bright-or-dark decision, the test-light
   procedure, the independence of metal tone from background tone and the lens bound on it, the metal box
   whose table becomes its own light source, invisible light, and the disappearing-edge failure. This is
   the chapter a foil wrapper and a metal tin brief actually needs.
2. **Glass (ch. 7) as the second complete case**, and the source of the single most inspectable
   acceptance criterion in the corpus: does the glass have continuous defined edges, and are they defined
   the same way all the way round.
3. **The conflict cases**, which are what the brief called the most valuable and which I agree are the
   most valuable: the label versus the glass highlight (`sk_lsmx_0049`), the sponge versus the leather
   (`sk_lsmx_0011`/`sk_lsmx_0012`), even versus glare-free illumination (`sk_lsmx_0008`), the metal box
   whose three faces demand three different things at once (`sk_lsmx_0035`).
4. **Liquids and food** (`sk_lsmx_0048`): the liquid lens, the liquid taking its background's colour, and
   the cut secondary background. Note honestly: **the book contains no treatment of steam**, which the
   portfolio brief named. It is not there, and I have not manufactured it.

What this lane does **not** supply, and should not be read as supplying: any evidence about what a
generative model can do; any route from a physical lighting act to a generative one; and any
corroboration of the live chapter-3 Canon, which it cannot provide, being the same book.
