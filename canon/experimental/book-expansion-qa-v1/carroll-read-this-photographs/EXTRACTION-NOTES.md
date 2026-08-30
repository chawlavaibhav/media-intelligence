# EXTRACTION NOTES — Henry Carroll, *Read This If You Want to Take Great Photographs*

**EXPERIMENTAL — NOT LIVE CANON.** Nothing in this directory is accepted Canon and nothing here may
be described as accepted.

---

## 1. Counts

| | |
|---|---|
| SourceKnowledge objects | **30** |
| SourceConceptSystems | **4** |
| OperationalBindings | **6** (4 evaluation · 2 production · 0 creative_ir · 0 governance · 0 benchmark) |
| Ontology terms | **38** (11 property · 18 problem · 9 remedy) |
| Ontology concepts | **6** (4 source_specific · 2 canonical) |
| Q&A items | **35** |
| Q&A with `requires_application: true` | **17 — 48.6%** |

Source size: **92,763 characters** across 66 spine documents. Sixty-one titled spreads yielded
thirty objects — under one object per two spreads.

## 2. Method

Read the whole book once in the extraction text, spread by spread, with the live neighbour
(`freeman-photographers-eye-graphic-guide`) read first. Then a second pass to separate what Carroll
states in words from what he states about a photograph, because that distinction decides the
`extraction_uncertainty` value on every object.

The unit of extraction is the spread. Carroll's book is sixty-one titled spreads, each with a
sub-heading, a photograph, a paragraph of description and one italicised rule. The italicised rule
is the extractable claim; the description is usually about the image.

## 3. `figure_semantic_binding_lost` — the number

This is the central hazard for this source and the brief asked for the proportion.

**14 of 30 objects — 46.7% — carry `extraction_uncertainty: figure_not_inspected.**

That is the honest count of objects whose support in the book is a reproduced photograph that could
not be inspected. The remaining 16 carry `none` because their claims are stated as general
principles or procedures in words, independently of any image.

The rule applied, stated so it can be checked:

- `figure_not_inspected` where the source's evidence for the claim **is** the photograph, and the
  claim is about a visual effect. Example: `sk_crl_0008` (visual weight) — "notice how much heavier
  the dark ground seems compared to the light wall" is a claim about an image.
- `none` where the claim is a decision rule, a procedure or an argument that stands in the prose.
  Example: `sk_crl_0004` (closeness is not croppable) — the argument is verbal and the photograph
  only illustrates it.

**What was NOT done:** no visual claim was reconstructed from the text. Where Carroll says the eye
bypasses a crowd and settles on a framed figure, this lane records *that he says framing draws
attention in a busy scene* and records the image claim as unverified. It does not record what the
photograph shows. Every object carries `source_support: text` and `inspected: {text: true,
figures: []}`, and no `figure_refs` are populated anywhere.

**The honest consequence.** Roughly half this bank rests on claims whose only demonstration is
inaccessible. For a book whose method *is* the photograph, that is not a defect of this extraction —
it is the ceiling of what a text route can recover, and it should be read as a hard limit on the
lane's evidential value rather than as a caveat.

## 4. Locators — `no_authored_page` and `false_page_affordance`

Both audit patterns apply, and the second is the dangerous one.

**`no_authored_page`.** EPUB, reflowable, Case 3 of the locator addendum. There is no page in this
format. Every `page_start` and `page_end` in every YAML file is `null`; every locator is the
spread's own title plus its printed sub-heading plus a spine number in parentheses as a file-position
aid. Verified mechanically: 30/30 objects with null pages, 35/35 Q&A locators free of any `p.`- or
`page`-style number.

**`false_page_affordance`.** This file *looks* paginated and is not. It carries:

- a "For other examples:" list on most spreads, of the form `Alkan Hassan p. 21`;
- direct body cross-references — "the Ansel Adams image on page 8", "turn back to pages 10, 16 and
  22", "see p. 32", "increasing your ISO (p. 50–4)", "use a tripod (p.39)";
- a full Index and Credits with printed page numbers throughout.

Every one of these is a **print-edition** page with no anchor in this reflowable copy. None was used,
none was resolved and none was invented. Two places where this cost real content, recorded rather
than papered over:

1. **`sk_crl_0019` (flat light).** Carroll sets an exercise — "I can spot three [classic
   compositional techniques]. If you need a clue, turn back to pages 10, 16 and 22." Which three he
   means is **not recoverable from this copy** and was not guessed.
2. **`sk_crl_0021` (focal length).** He supplies a table of which focal lengths give which effects
   on which cameras. It is an image and was not inspected, so this lane has no frame of reference
   for "wide" and "long" and does not supply one.

## 5. Genuine addition versus restatement — the Freeman question

The brief asked for this judgement explicitly. The live neighbour
`canon/knowledge/current/freeman-photographers-eye-graphic-guide` occupies the same territory: the
frame and its edges, subject placement, division, symmetry, tonal weight, frame proportion.

**This is recorded here as prose only.** No relationship, equivalence or agreement between Carroll
and Freeman is asserted anywhere in this lane's YAML, no ontology relationship points at a live
term, and nothing below is a claim about the world. It is an observation about what to extract.

**Refused as restatement — one candidate, deliberately dropped.** Carroll's "Landscape or portrait"
spread (spine 9): match the format of the picture to the dominant lines of the subject, because
horizontal pictures move the eye side to side and vertical ones up and down. This is a
single-sentence rule with an asserted eye-movement mechanism and no argument. The live Freeman
extraction holds frame shape and proportion in far more differentiated form — several distinct
objects on vertical framing, the square frame, the wide frame and the panorama. Recording Carroll's
version would have added a thinner statement of material the corpus already holds. **Not extracted.**
Its one arguable addition — the instruction to derive format from the subject's dominant line — is
noted here in prose and nowhere else.

**Kept because it is not Freeman.** Carroll's real contribution to this corpus is not composition
theory. It is three things Freeman's live span does not cover:

1. **The decision under time pressure.** What must be settled *before* the moment (`sk_crl_0024`),
   what to sacrifice when it cannot all be had (`sk_crl_0025`), and how to judge the result
   afterwards (`sk_crl_0026`). This is the strongest material in the lane.
2. **Exposure and light as expressive rather than technical choices** — the whole of
   `scs_crl_001` and `scs_crl_002`, including the one stated interaction between light and
   composition (`sk_crl_0019`).
3. **The photographer's physical position as the decision** (`scs_crl_004`), including the
   relational reading he attaches to it.

**A near-collision that is not one.** Both authors discuss an internal frame. Freeman's live object
concerns a timing reflex the device triggers; Carroll's (`sk_crl_0002`) concerns isolating a subject
in a busy scene. Different claims about the same device. Recorded here so the resemblance is not
proposed again as a merge, and deliberately **not** recorded as a `distinct_from` relationship,
because that would be a cross-lane assertion against live Canon which this task does not authorise.

## 6. Hazards, and how each was handled

**No `empirical_within_source`, anywhere.** Verified in code: 0 of 30 objects. This book contains no
study, no measurement, no reader test and no controlled comparison. The dominant characteristics are
`practitioner_assertion`, `explicitly_stated`, `argued` and `mechanism_given`.

**Survivorship.** Every example in the book is a celebrated photograph by a named photographer, most
in major collections. Nothing that failed is shown, and — this is the point — nothing that failed
*could* be shown, because the book's picture research selected on outcome. This bites hardest on
`sk_crl_0009` (great photographs break the rules) and `sk_crl_0025` (the right moment with the wrong
settings), where the entire evidence base is famous photographs. Recorded as an `extractor_observed`
caveat on both, and stated once in the header of `source-knowledge.yaml` rather than repeated
thirty times.

**Physical camera advice must not become generative instruction.** Enforced three ways:

1. Both production bindings (`bnd_crl_005`, `bnd_crl_006`) carry `status: production_candidate` and
   `target_path: null`, and both state in `applicability.limits` that no generative equivalent is
   asserted.
2. Eight of the nine remedy terms carry `executable_by: [physical_production]`. Not one carries
   `generative_respecification`. The single exception is `t_crl_0023`
   (*write it off as the one that got away*), which carries `[human_edit]` because it is an act of
   assessment, not an act with a camera.
3. `bnd_crl_006` states the reason explicitly rather than merely observing the rule: Carroll's own
   mechanism is that the photographer's real position and real exposure to the subject are what the
   picture carries. That has no meaning where no one stood anywhere. Rewriting "get closer" as a
   generative instruction would keep his words and discard his mechanism.

**Technology contingency.** Six objects carry `historical_claim`: the exposure trio and its
interface, the shutter and shake thresholds, the freeze threshold, the manual-mode argument, the
metering and compensation account, and the flash behaviour. These describe a digital camera of
roughly 2014 — mode dials, P/S(Tv)/A(Av)/M, per-frame ISO, exposure-compensation buttons,
Image Stabilization / Vibration Reduction, RAW versus JPEG. The physics underneath is not
contingent; the interface and the rules of thumb are.

**Numeric thresholds are rules of thumb, not measurements.** About 1/60 for visible subject blur and
for handheld shake, about 1/125 for freezing, ISO 800 and above for visible noise, ISO 400 for an
overcast day. Carroll gives none of them a subject speed, focal length or sensor size, and hedges
several. Recorded with `source_uncertainty: source_hedges` where he hedges, and never presented as
data.

## 7. What was deliberately not extracted

**Refused as settings recipes with no reason given** — the "bish, bash, bosh" operating instructions
for changing shutter speed and aperture (which dial, which button, which direction to scroll); the
f-stop scale; the ISO scale and where to find the setting; the white-balance preset icons; RAW
versus JPEG; the autofocus-mode and focus-point settings in Troubleshooting. All are interface
instructions for a camera generation, and none carries a transferable reason.

**Refused as gear notes** — the zoom/prime and focal length/field of view glossary; the sensor-size
discussion, which Carroll himself refuses to have; the claim that primes are cheaper, lighter and
optically superior; the macro-lens type note.

**Refused as exercises** — every "Now go out and practise", and the several instructions of the form
"don't take my word for it, give it a go yourself".

**Refused as biography or decorative example** — the photographer profiles that carry no principle,
the Hitchcock *Rear Window* aside, the Chris Levine anecdote about the Queen resting her eyes.

**Refused as motivational prose** — the whole of "That extra something" (spine 66), whose content is
that the magic of photography "is you"; "Start by ignoring everything"; "SEEING — Don't look. See.",
whose extractable content is only that seeing is personal.

**Considered and refused on thinness — one case worth naming.** "One subject, one shoot" (spine 63):
focusing attention on a particular subject matter gives more purpose and better results. This is an
outcome claim with no mechanism beyond "it hones your eye", and it is close enough to generic advice
that a competent person would produce it by default. Not extracted, and noted here because it is the
closest call in the lane.

**Refused as restatement of a live neighbour** — "Landscape or portrait" (spine 9). See §5.

**A governance candidate, examined and refused.** Carroll's warning that using the composition
techniques as a checklist makes photographs "safe and predictable" resembles `rule_application` —
whether a principle may be applied in isolation. It is not one. It is advice to a photographer about
their own practice, not a rule about how recorded knowledge may be consumed. Under SPEC-04's
guard-against-a-junk-drawer rule, a candidate that fits none of the six permitted consumers is not a
governance binding, so the knowledge is left unbound. Recorded here as a negative finding.

**A benchmark candidate, examined and refused.** The book's alternating hard/soft light spreads look
like a minimal-pair structure. They are not: different photographer, different subject, different
scene each time, nothing held constant. Building a benchmark from them would manufacture a
controlled comparison the source does not contain. Recorded in `source-concept-systems.yaml` under
`scs_crl_002`'s `system_level_uncertainty` and in the header of `operational-bindings.yaml`.

## 8. Internal tensions preserved, not resolved

Three, all left standing because they are the source's:

1. **Centre versus off-centre.** Symmetry (`sk_crl_0005`) recommends centring the subject; the rule
   of thirds (`sk_crl_0006`) recommends not centring it. Consecutive spreads, no rule for choosing.
   Recorded as a `contradicts` relation in both directions and as a `conflicts` entry in
   `scs_crl_003`.
2. **Deliberate frame-scan versus the decisive moment.** `sk_crl_0007` says these pictures cannot be
   snapped; `sk_crl_0024` says there will be no time to think. Recorded as `trades_off_with` in both
   directions.
3. **Leniency about settings versus severity about results.** `sk_crl_0025` and `sk_crl_0026`,
   four spreads apart. Recorded as `trades_off_with`, and made into a Q&A item that requires the
   reader to reconcile them.

A fourth is recorded on the boundary between assessment units: `sk_crl_0026` judges a single frame
and `sk_crl_0030` says the frame is the wrong unit for a series (`contradicts`).

## 9. Self-check results

1. **All five YAML files parse** under `yaml.safe_load`.
2. **No page number anywhere.** 30/30 objects have `page_start` and `page_end` null; 35/35 Q&A
   locators contain no `p.`/`pp.`/`page N` construction; asserted in code by regex over every
   locator string. 0 failures, 0 fixes required.
3. **Every reference resolves.** All `source_knowledge_refs`, `source_system_refs`,
   `failure_ontology_refs`, `repair_ontology_refs`, `members[].sk_ref`, `children_terms`,
   `relationships[].from/to` and every `intra_source_relations[].target` checked in code against
   this lane's own identifier sets. 0 dangling.
4. **`requires_application` = 17/35 = 48.6%**, computed in code. Required minimum one third: **met**.
5. **Every `kind: remedy` term carries `executable_by`.** Checked in code: 0 missing.
6. **No `xs_` concept and no `same_failure_family` relation** created.
7. **No `empirical_within_source`** on any object. Checked in code: 0.
8. **Honest count, not target count.** The brief's range was 15–30 objects and 20–35 Q&A. This lane
   sits at the top of both, which needs a defence rather than a shrug: the book has sixty-one
   spreads, each with its own titled claim, and thirty objects is a refusal rate of just over half.
   The refusals in §7 are the evidence. One Q&A item was cut after the first draft (the internal-frame
   boundary condition, the thinnest of the set) to bring the bank from 36 to 35 rather than exceed
   the stated ceiling.

## 10. Write boundary

Every file written by this lane is inside
`canon/experimental/book-expansion-qa-v1/carroll-read-this-photographs/`. Nothing under
`canon/knowledge/current/**`, `canon/audit/**`, `coordination/**` or any SPEC file was created,
edited or deleted. Nothing was committed.
