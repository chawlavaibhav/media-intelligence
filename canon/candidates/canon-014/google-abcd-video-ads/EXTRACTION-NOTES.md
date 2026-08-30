# Extraction notes — `google-abcd-video-ads` (experimental lane 4)

**EXPERIMENTAL — NOT LIVE CANON.** Nothing here is accepted Canon and nothing here may be
described as accepted.

## Method

Three Google-owned pages, retrieved 30 August 2026, read in full from
`scratchpad/src/SRC-google-abcd.txt`. Navigation chrome, account and consent dialogue, footer link
lists and language pickers were skipped entirely; roughly 1,100 words of substantive guidance
remain across the three pages.

Order of work: read the schema contract and SPEC-03/04/05 first; read the Binet record for
calibration on a source with a declared commercial interest; read the dump; re-fetch the Google Ads
Help page to repair a table the dump had flattened; then extract, bind, map and write the bank;
then verify every locator and every quoted string against the source.

## The two cautions, and where they live

**1. Declared publisher interest.** The publisher sells advertising on the platform whose creative
guidance this is, and whose effectiveness the cited research validates. The source's own disclosed
third-party involvement — Ipsos as research partner, Nielsen and Kantar as independent reviewers —
**moderates this and does not remove it**, for three reasons readable off the source: the
reviewer language describes how the framework was derived rather than auditing the lift figures;
the source never says what the reviewers reviewed or concluded; and the study behind the figures
is named but not published.

Recorded in: `PROVENANCE.md` (a dedicated section); a caveat on **all 26** SourceKnowledge
objects; `applicability.limits` on **all 9** bindings; governance binding `bnd_abcd_008`
(`evidence_interpretation`); and Q&A items `qa_abcd_0001`, `qa_abcd_0003`, `qa_abcd_0022`,
`qa_abcd_0026`.

**2. Platform and time contingency.** This describes one platform's ad products at one time under
one set of playback behaviours. Every SourceKnowledge object carries `historical_claim` in
`evidence.characteristics` and a platform-contingency caveat. Governance binding `bnd_abcd_009`
(`rule_application`) constrains application outside YouTube video advertising.

The sound-on claim (`sk_abcd_0014`) is the case that most needed care. It is extracted faithfully
**as a claim about YouTube**, made once, on one page, with no measurement attached, and it is
explicitly **not** generalised — the object's own caveat says it points the opposite way from the
sound-off default common on other feed surfaces. Q&A items `qa_abcd_0004` and `qa_abcd_0005` test
exactly that boundary, and `qa_abcd_0005` answers "the source says nothing about that case at all"
rather than supplying muted-feed practice from elsewhere.

## What was extracted, and how much

| Artefact | Count |
|---|---|
| SourceKnowledge | 26 |
| SourceConceptSystem | 2 |
| Ontology terms | 28 |
| Ontology relationships | 32 (3 of them `distinct_from`) |
| Concepts | 4 — 2 `source_specific_concept`, 2 `canonical_concept`, **0 cross-source** |
| Operational bindings | 9 — 5 evaluation, 2 benchmark, 2 governance |
| Q&A items | 26, of which **10 `requires_application: true` (38.5%)** |

26 objects sits just above the suggested 15–25 band, and the reason is structural rather than
padding: the source names its techniques discretely (11 in the Google Ads Help table alone) and its
objective matrix contributes four separate decision rules that are individually retrievable and
individually wrong to merge. Every object corresponds to something the source states in its own
words. Nothing was created to reach a number.

## The two systems, and why only two

`scs_abcd_001` — the four principles as one jointly-applied framework. **The task asked whether
the source treats them as jointly necessary or as a menu; it was checked before being asserted.**
Three pieces of evidence, all the source's own, and the whole-system claim is therefore marked
`source_explicit`:

1. "By factoring four simple principles into **each** decision, your work is more likely to
   achieve your marketing goals."
2. The effectiveness figures are stated for "the ABCDs" as a set and are **never** decomposed by
   principle on any page.
3. The objective matrix is where a menu reading would show up, and it never drops a principle:
   every one of the sixteen cells carries an instruction, and where an objective calls for no
   special treatment the cell reads "Apply core principles".

What is **ours** in that system is recorded as ours: the decision to record **no ordering**. The
source always prints A, B, C, D in that sequence, but the lettering is a mnemonic — it never says
an earlier letter outranks a later one, nor that the letters map to positions in the ad's timeline.
Recording A–D as a priority order or a sequence would assert something the source does not.

`scs_abcd_002` — the objective-weighted ABCDs. Its whole-system claim is marked
`extractor_synthesis` with an `interpretation_basis`, because the observation that membership is
constant while emphasis moves, and the count of where "Apply core principles" falls, are our
reading of a published table rather than the source's statement about it.

No third system was created. The audio-pairing pattern that recurs across three of the four
principles is real, but the source never groups those guidelines, so it is recorded where it
belongs — as a `canonical_concept` (`cc_abcd_audio_visual_pairing`) with
`asserts_equivalence: false`, labelled as ours.

## Evidence characteristics — how they were assigned

`empirical_within_source` is used **once**, on `sk_abcd_0003`, and only because the lift figures
are genuinely reported measurement results. It is used alongside `outcome_claimed` and beneath five
caveats saying exactly what kind of result it is: reported by an interested party, from a study the
source does not let the reader inspect, with no method, baseline, definition or dispersion, and
stated at three different strengths on the publisher's own three pages.

`outcome_claimed` also carries `sk_abcd_0002` (the NCSolutions claim, third-party-reported by the
publisher with no study detail) and `sk_abcd_0012` ("audio brand mentions enhance onscreen brand
visuals' performance", a performance claim with no figure attached).

`mechanism_absent` is used a great deal, and that is a finding about the source rather than an
extraction shortfall: the ABCDs mostly assert. Eight objects carry `mechanism_given`; sixteen carry `mechanism_absent`.

`historical_claim` is on every object. `culturally_bounded` is on the two objects where the source
reaches for cultural content without scoping it — humanising and representing the consumer, and the
humour/surprise/intrigue levers.

## How the figure discrepancy was handled

**Reported, not resolved.** Three phrasings of one finding, on three Google pages:

- Google Ads Help: "**as much as** a 30% lift ... and a 17% lift" — an upper bound.
- Think with Google: "**On average**, the ABCDs deliver a 30% lift ... and a 17% lift" — a central
  tendency.
- The resources article: the two numbers as **bare callouts with no qualifier at all**, above a
  footer line reading "Actual results will vary by advertiser".

The brief flagged the first two; the third turned up in the reading and is recorded with them,
because a bare number is a third position and not a restatement of either. Citation detail differs
too: **n=11,000 ads appears on the resources article only**; Ads Help gives the study, publisher,
scope and month without a sample; Think with Google names "Google/Kantar Link AI", drops the month
and gives no sample.

Nothing on any page settles which is correct, so nothing here does either. It is recorded as
caveats on `sk_abcd_0003`, as the subject of `bnd_abcd_008`, and in `qa_abcd_0001`, `qa_abcd_0002`
and `qa_abcd_0026`. The two Q&A items that turn on it name the pages, so a wrong answer is
detectable.

## The table repair

The plain-text dump linearises the Google Ads Help objective matrix and destroys the
cell-to-column binding. Two rows — awareness and consideration — carry **two bullets in one
Connection cell**, so reading order yields five instructions for four columns with no signal that
anything is uncertain. A reading-order reconstruction would have bound "Be different, yet simple"
and "Be relatable" to the wrong principles with full apparent confidence.

The page was re-fetched with `curl` and the table markup read directly. The resolved matrix:

| Objective | Attention | Branding | Connection | Direction |
|---|---|---|---|---|
| Awareness: Get noticed | Pump up the volume by using audio to get viewers to pay attention | Put your brand front and center | Make the people core to the story · Be different, yet simple | Apply core principles |
| Consideration: Show users how your product fits into their lives | Apply core principles | Hero the product | Show how it works · Be relatable | Plant the seed of urgency |
| Action: Present an enticing call-to-action with the right context | Apply core principles | Make the product the ad | Be exact and tangible | Present the ask after the context is set |
| Full funnel: Maximize effectiveness by incorporating all objectives | Hook attention with audio and focus on elements that deliver the message | Start with a mix of branding elements and finish with the product | Establish a connection with your audience to help support your product | Use CTAs throughout your ad, and be more direct as you go |

`scs_abcd_002` carries `extraction_uncertainty: inferred_from_layout` and says how the mapping was
resolved. This is the same shape as the live Canon's chart-linearisation finding for Binet: values
survive, bindings do not.

## What was deliberately not extracted

- **The "ABCDs Playbook"** that Think with Google links for the objective-driven variants. It was
  not downloaded and is not represented here. Whatever detail it holds about the objective-specific
  ABCDs is **unavailable** to this extraction, and the four objective rows come from the published
  Google Ads Help table only.
- **The Scribd reupload of a Google "ABCD reference guide".** Not used and not visited — it is a
  third-party reupload, not the publisher's route.
- **The linked "About video ad specs" page**, which the source defers specs and safe zones to. It
  is outside the retrieved span, so no specification, timing or safe-zone figure enters this
  extraction from it.
- **The fourteen named brand vignettes** (Cheetos, Fastrack, Silmäasema, Pokémon, Ruffles,
  Weekendesk, Oi, Gojek, BareMinerals, M&M'S, Fanta, Halodoc, Shopee, Air Up) are recorded as
  `examples.positive` on the objects they illustrate, in one line each. The linked videos were not
  watched, so no object claims visual support and none carries `visually_demonstrated`.
- **Navigation chrome, consent text, footer and language lists** — the great bulk of the dump.
- **Cross-lane ontology relationships.** The contract permits `related_to`,
  `potentially_equivalent_to` and `distinct_from` across lanes, and there are obvious candidates
  (this source's `focus_the_message` against a Hopkins or WCAG analogue). None was written, because
  the parallel lanes run concurrently and their term identifiers are not knowable here; any such
  relation would be a dangling reference. Recorded as a gap for consolidation, not guessed.
- **Any cross-source claim, `xs_` concept or `same_failure_family` relation.** Forbidden in this
  task; none exists in the output.

## Where I was tempted to pad or over-claim, and did not

1. **A twenty-seventh object for the figure discrepancy.** It would have made the finding directly
   retrievable, which was tempting. But SourceKnowledge records what a source *teaches*, and "the
   publisher states one result three ways" is an observation *about* the source, not a claim *by*
   it. Making it an object would have smuggled an extractor observation into the source layer. It
   went into caveats, a governance binding, this file and three Q&A items instead.

2. **Reading A–B–C–D as a timeline.** Attention-then-Branding-then-Connection-then-Direction maps
   so naturally onto the shape of an ad that asserting a sequence would have passed unnoticed. The
   source never says it. The ordering scheme is `none`, and the reason is written into
   `scs_abcd_001`'s `system_level_uncertainty`.

3. **A five-second branding rule.** The source prints "Weekendesk introduces its brand in the first
   5s" in an illustrative caption. The widely circulated five-second rule would have slotted in
   effortlessly. It is a caption about one ad, not a rule, and `sk_abcd_0011` says so; two Q&A items
   list borrowing it as a confounder.

4. **Filling the sound-off gap.** `qa_abcd_0005` asks what to do on a muted surface. Standard
   muted-feed practice — burn-in captions, text-first storytelling — was the obvious answer and
   would have been wrong, because this source says nothing at all about that case. The answer says
   so.

5. **Resolving the humanise / "make the product the ad" tension.** The source publishes both and
   never addresses the conflict. `qa_abcd_0025` puts both to the reader and answers that the source
   does not settle it; the conflict is recorded in `scs_abcd_002` as `extractor_inferred`.

6. **Decomposing the 30% lift.** Attributing a share of it to audio branding or to any principle
   would have made the source far more useful. It is never decomposed on any page. `qa_abcd_0026`
   exists specifically to make that over-claim detectable.

7. **A creative_ir or production binding.** The evaluation and benchmark bindings came easily and
   more could have been manufactured. None was: this source describes evaluable properties of
   finished ads, not fields of an intermediate representation, and it prescribes no physical
   production procedure that a production binding would park.

## Q&A bank — construction and known shape

26 items; **10 `requires_application: true`, 38.5%**, above the one-third floor. Every item has
non-empty `confounders`.

The bank was built against the failure mode the brief named: questions a model answers from latent
marketing knowledge. The load-bearing items turn on things only this text supports — which page
says what (`qa_abcd_0001`, `qa_abcd_0002`, `qa_abcd_0007`, `qa_abcd_0013`, `qa_abcd_0021`), the
exact contents of the objective matrix (`qa_abcd_0008`, `qa_abcd_0009`, `qa_abcd_0011`,
`qa_abcd_0012`, `qa_abcd_0020`), where the source files a fault (`qa_abcd_0017`), and what it
declines to quantify (`qa_abcd_0015`, `qa_abcd_0023`, `qa_abcd_0024`). Several confounders name
the plausible-but-wrong modern default explicitly — the mute-by-default assumption, the
five-second rule, the CTA-at-the-end rule, a WCAG-style contrast ratio.

**Mix, against the contract's target.** Definitions/facts 4 (~15%), mechanisms 3 (~12%),
comparisons/trade-offs 5 (~19%), diagnosis/application 8 (~31%), boundaries 4 (~15%),
source position 2 (~8%). Mechanisms sit below the ~25% target, and that is honest rather than
lazy: this source states a mechanism on only eight of twenty-six objects, and sixteen carry `mechanism_absent`. Forcing three more mechanism items
would have required inventing mechanisms the source does not give. Application and boundary items
are correspondingly over-represented, which is where a thin, assertive, heavily-caveated source
actually supports hard questions.

Difficulty skews hard (15 hard, 10 medium, 1 easy). The one easy item is the four principle
statements, and it is framed around the source's exact one-line wording rather than the acronym,
so it is not answerable by knowing that the ABCDs exist.

## Self-check results

1. **Every YAML file parses.** `source-knowledge.yaml`, `source-concept-systems.yaml`,
   `operational-bindings.yaml`, `ontology-mappings.yaml`, `qa-bank.yaml` all load under
   `yaml.safe_load`. Schema validated mechanically: SPEC-03 required keys present with no extras
   and no invented fields; all `evidence.characteristics`, `source_uncertainty`,
   `extraction_uncertainty`, `intra_source_relations[].relation`, `caveats[].origin`,
   `label_origin`, `claim_type` and `source_support` values drawn from the fixed vocabularies; all
   26 `sk_id` unique; every `intra_source_relations.target` resolves to an object or system in this
   lane; SPEC-04 rules 1–9 checked, including `observation_unit` on all five evaluation bindings and
   a permitted `governance_consumer` on both governance bindings; every ontology reference in a
   binding resolves to a term in this lane's `ontology-mappings.yaml`; every `kind: remedy` term
   carries `executable_by`; both canonical concepts carry `asserts_equivalence: false` and
   `purpose: retrieval_and_aggregation`. No `cross_source_supported` or `empirically_supported`
   `evidence_basis`. No Creative IR path, `informs` field, product vocabulary or decimal confidence
   anywhere.

   One defect was found and fixed during the check: a first pass wrote apostrophes as `''` inside
   folded block scalars in `qa-bank.yaml`, where `''` is literal rather than an escape. All 39
   affected lines were corrected and the file re-parsed.

2. **Every Q&A locator was checked exhaustively — all 26 items.** Every page name, section heading
   and table row cited resolves in the source. Every double-quoted string of six characters or more
   across all questions, answers, locators and support fields was matched against the source text
   programmatically. All matched except: strings the dump splits across lines where the HTML runs
   them together (the guideline label, its colon and its text; the objective row label and its
   description) — each of these was verified verbatim against the re-fetched table markup instead;
   one deliberate elision, `"enhance ... performance"`; and one invented scenario string, `"Buy
   now"`, in `qa_abcd_0010`, which is part of the hypothetical and not a quotation. Four
   near-verbatim quotations were corrected to exact source wording during this pass (`qa_abcd_0008`
   trailing periods, `qa_abcd_0018` two guideline quotations, `qa_abcd_0025` one). The cited
   location supports the answer in every case.

3. **Every effectiveness object carries both cautions.** Verified programmatically: all 26 objects
   carry a caveat containing the publisher-interest statement and a caveat containing the
   platform-contingency statement. This is stricter than the requirement, which named effectiveness
   objects only — every guideline in this source is presented as data-backed, so the interest
   applies throughout, and every object is YouTube-scoped, so the contingency does too.

4. **Nothing infers a generative model capability.** No binding assumes any generative model can
   execute these guidelines; both benchmark bindings state so in `applicability.limits`, and
   `bnd_abcd_007` says explicitly that the source's own before/after pair is two human-authored
   versions with no measurement attached. No term carries
   `executable_by: generative_respecification`; the ten remedy terms are `human_edit` (8) or
   `physical_production` (2 — bright/high-contrast visuals, and featuring people, both of which are
   camera-and-casting actions and are left unbound rather than translated). The file header of
   `ontology-mappings.yaml` and the header of `operational-bindings.yaml` both state this.

5. **Counts and fraction** — see the table above. 26 SourceKnowledge · 2 systems · 28 terms ·
   32 relationships · 4 concepts · 9 bindings · 26 Q&A with **10 `requires_application: true`
   (38.5%, floor 9)**.

## Write boundary

Everything written by this lane is inside
`canon/experimental/book-expansion-qa-v1/google-abcd-video-ads/`. Nothing under
`canon/knowledge/current/`, `canon/audit/`, `coordination/`, `eval/`, `resources/`, `governance/`,
`PROJECT-MEMORY.md` or any `SPEC-*` file was created, edited or deleted. Nothing was committed.
