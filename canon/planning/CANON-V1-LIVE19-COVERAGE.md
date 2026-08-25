# Canon V1 — live-19 coverage rebaseline (C1)

**Task:** CANON-V1 overnight program, work package C1
**Date:** 26 Aug 2026 · **Branch:** `work/canon-v1-overnight` · **Status:** complete, mechanically verified
**Supersedes for planning use:** `canon/experiments/CANON-COVERAGE-MAP-V0.md` (23 Aug 2026)
**Does not modify:** the v0 map, which is retained unchanged as historical evidence

---

## 1. What this replaces, and why it mattered

The old coverage map rated 56 knowledge domains against **the 40-title library we own**. That was
the right question in August, when almost nothing had been extracted. It is the wrong question now,
and using it has become actively misleading, because owning a book and having its knowledge in the
Canon are completely different states.

**The clearest example.** The v0 map rates *Hierarchy / attention / salience* as **strong**, citing
*Picture This*, *The Non-Designer's Design Book* and *Thinking with Type*, each marked with a tick.
**None of those three is in the live accepted Canon.** They were early CANON-001/002 work whose
outputs are not on `main`, and *Thinking with Type* is separately blocked on column interleaving.
The same pattern repeats for *Critique process & language* (rated strong entirely on *Discussing
Design*) and *Judgement quality & bias* (rated strong on *Noise*, *Thinking Fast and Slow* and
*Superforecasting*). **Not one of those five titles is accepted knowledge.**

Both of those domains are still multi-origin in this rebaseline — but on **completely different
evidence**. The old ratings were right by accident. Planning on them would have meant planning on
knowledge the Canon does not hold.

This document rates the same domains against **the 19 accepted, audited sources and nothing else**.
Every contributor was assigned by reading the committed extraction — the source's own declared
subject matter, its concept systems and its ontology terms — never from a title or a shelf position.

## 2. Headline

| Measure | Value |
|---|---|
| Accepted sources | **19** |
| Active audit records | **19**, all `audit_status: complete` |
| Audit Gate validator | **19 records, 0 errors** — re-run in this session |
| Source-knowledge objects | **580** |
| SourceConceptSystems | **63** |
| Ontology terms | **470** |
| Operational bindings | **127** |
| **Independent intellectual origins in the whole corpus** | **17, not 19** |
| Diagnostic domains accounted for | **56 / 56** |
| Product-facing packs accounted for | **10 / 10** |
| Domains with no accepted contributor | **5** |
| Critical domains that are empty | **3** — A14, B11, C13 |
| Critical domains present but not usable as-is | **2** — A13, C09 |

**The live-19 totals (580 / 63 / 470 / 127) have never been published before.** The repository
records only the frozen historical figures for the 16-source CANON-003 set (505 / 54 / 417 / 111),
and those two sets of numbers must never be mixed. The historical instrument
`validate_canon003_integrated.py` still reports its own 16-source figures unchanged, as intended.

**Nineteen sources are seventeen origins.** Two pairs each collapse to one origin: *Grammar of the
Shot* and *Grammar of the Edit* are companion volumes, and *In the Blink of an Eye* and *The
Conversations* are Walter Murch speaking in both. This is not an estimate — it is computed by
calling `independent_origins_ok()` from the committed Audit Gate validator, which fails closed.
Counting titles would have said nineteen.

## 3. How to read the coverage state

These are **inventory terms, not grades.** They say where knowledge came from, not how good it is.

| State | Meaning |
|---|---|
| `present_multi_origin` | Two or more **independent** origins contribute |
| `present_single_origin` | Exactly one independent origin |
| `present_but_application_unbound` | Real knowledge exists, but nothing binds it to how the product would use it |
| `representation_or_evidence_limited` | Knowledge exists but a stated limit blocks using it for this product |
| `absent` | No accepted source contributes |

Three warnings, all of them lessons this project has already paid for:

- **`multi-origin` is not `deep`.** *Visual weight* and *Grids & layout systems* are both
  multi-origin. Samara alone contributes 79 objects and six concept systems on grids; visual weight
  is a handful of observations about tone. The `Contrib` column counts sources, not substance.
- **Never rank a domain by binding count.** The corpus's best-binding source, *StoryBrand*, has its
  weakest evidential support. Bindability is not evidence quality.
- **No decimal "Canon quality" score exists here, deliberately.** Inventing one would encode a guess
  as a finding.

## 4. Full domain table

#### A · Static visual craft

| ID | Domain | Imp. | State | Contrib | Indep | Bound to | Contributing sources |
|---|---|---|---|---|---|---|---|
| A01 | Composition & framing | crit | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, production, governance | Freeman, Kenworthy, Alton |
| A02 | Hierarchy / attention / salience | crit | multi-origin | 6 | 6 | creative_ir, evaluation, benchmark, production, governance | Freeman, Samara, Kenworthy, Murch, GoEdit, Vignelli |
| A03 | Visual weight | crit | multi-origin | 2 | 2 | creative_ir, evaluation, benchmark, production, governance | Freeman, Alton |
| A04 | Grouping / gestalt | usef | multi-origin | 2 | 2 | creative_ir, evaluation, benchmark, production, governance | Freeman, Samara |
| A05 | Colour | crit | multi-origin | 4 | 4 | creative_ir, evaluation, benchmark, production, governance | Albers, Alton, Kenworthy, Vignelli |
| A06 | Typography | crit | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, production, governance | Samara, Vignelli, Albers |
| A07 | Grids & layout systems | usef | multi-origin | 2 | 2 | creative_ir, evaluation, benchmark, production, governance | Samara, Vignelli |
| A08 | Imagery & subject choice | usef | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, production, governance | Freeman, Hopkins, Alton |
| A09 | Lighting | crit | multi-origin | 2 | 2 | creative_ir, evaluation, benchmark, production, governance | Alton, LSM |
| A10 | Material appearance | crit | multi-origin | 2 | 2 | creative_ir, evaluation, benchmark, production, governance | LSM, Alton |
| A11 | Photography craft | usef | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, production, governance | Freeman, LSM, Alton |
| A12 | Spatial relationships & depth | usef | multi-origin | 4 | 4 | creative_ir, evaluation, benchmark, production, governance | Freeman, Kenworthy, Murch, GoShot |
| A13 | Product / packshot photography | crit | **unbound** | 2 | 2 | creative_ir, evaluation, benchmark, production, governance | LSM, Alton |
| A14 | Devanagari & Indic typography | crit | **absent** | 0 | 0 | none | — |

#### B · Moving image

| ID | Domain | Imp. | State | Contrib | Indep | Bound to | Contributing sources |
|---|---|---|---|---|---|---|---|
| B01 | Shot grammar & shot types | crit | multi-origin | 3 | 2 | creative_ir, evaluation, benchmark, production, governance | GoShot, GoEdit, Kenworthy |
| B02 | Camera placement & movement | usef | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, production, governance | Kenworthy, GoShot, Alton |
| B03 | Continuity | crit | multi-origin | 4 | 2 | creative_ir, evaluation, benchmark, production, governance | GoShot, GoEdit, Murch, Ondaatje |
| B04 | Editing & cut logic | crit | multi-origin | 3 | 2 | creative_ir, evaluation, benchmark, governance | GoEdit, Murch, Ondaatje |
| B05 | Pacing & rhythm | crit | multi-origin | 3 | 2 | creative_ir, evaluation, benchmark, governance | Murch, GoEdit, Ondaatje |
| B06 | Temporal hierarchy | usef | multi-origin | 2 | 2 | creative_ir, evaluation, benchmark, governance | Murch, GoEdit |
| B07 | Visual storytelling | crit | multi-origin | 4 | 3 | creative_ir, evaluation, benchmark, production, governance | Murch, Ondaatje, Kenworthy, Miller |
| B08 | Performance & direction | peri | multi-origin | 2 | 2 | creative_ir, evaluation, production, governance | Kenworthy, Ondaatje |
| B09 | Dialogue presentation | usef | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, production, governance | GoEdit, Ondaatje, Kenworthy |
| B10 | Sound / audiovisual relation | usef | multi-origin | 3 | 2 | creative_ir, evaluation, benchmark, governance | Ondaatje, GoEdit, Murch |
| B11 | Short-form / feed-native grammar | crit | **absent** | 0 | 0 | none | — |
| B12 | Motion design & animated type | usef | **absent** | 0 | 0 | none | — |
| B13 | Colour grading | peri | **absent** | 0 | 0 | none | — |

#### C · Commercial communication

| ID | Domain | Imp. | State | Contrib | Indep | Bound to | Contributing sources |
|---|---|---|---|---|---|---|---|
| C01 | Advertising strategy | crit | multi-origin | 5 | 5 | creative_ir, evaluation, benchmark, governance | Ogilvy, Hopkins, Binet&Field, Miller, Sutherland |
| C02 | Objective setting | crit | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, governance | Ogilvy, Binet&Field, Hopkins |
| C03 | Audience understanding | crit | multi-origin | 5 | 5 | creative_ir, evaluation, benchmark, governance | Sutherland, Hopkins, Binet&Field, Miller, Heath |
| C04 | Proposition & positioning | crit | multi-origin | 4 | 4 | creative_ir, evaluation, benchmark, governance | Ogilvy, Miller, Hopkins, Heath |
| C05 | Persuasion | crit | multi-origin | 5 | 5 | creative_ir, evaluation, benchmark, governance | Sutherland, Heath, Hopkins, Binet&Field, Ogilvy |
| C06 | Branding & identity | usef | multi-origin | 4 | 4 | creative_ir, evaluation, benchmark, governance | Ogilvy, Vignelli, Binet&Field, Miller |
| C07 | Product communication | crit | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, governance | Hopkins, Ogilvy, Miller |
| C08 | Emotional target | usef | multi-origin | 4 | 4 | creative_ir, evaluation, benchmark, governance | Binet&Field, Sutherland, Heath, Miller |
| C09 | Hooks & openings | crit | **limited** | 3 | 3 | creative_ir, evaluation, benchmark, governance | Heath, Hopkins, Ogilvy |
| C10 | Memorability & stickiness | usef | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, governance | Heath, Sutherland, Ogilvy |
| C11 | CTA & response | usef | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, governance | Miller, Hopkins, Binet&Field |
| C12 | Information hierarchy | crit | multi-origin | 4 | 4 | creative_ir, evaluation, benchmark, production, governance | Samara, Vignelli, Miller, Freeman |
| C13 | Indian market & cultural context | crit | **absent** | 0 | 0 | none | — |
| C14 | Effectiveness evidence | usef | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, governance | Binet&Field, Hopkins, Ogilvy |

#### D · Creative thinking

| ID | Domain | Imp. | State | Contrib | Indep | Bound to | Contributing sources |
|---|---|---|---|---|---|---|---|
| D01 | Concept development | crit | multi-origin | 4 | 4 | creative_ir, evaluation, benchmark, production, governance | Ogilvy, Heath, Catmull, Bayles |
| D02 | Metaphor & symbolism | usef | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, governance | Ondaatje, Vignelli, Heath |
| D03 | Novelty & distinctiveness | usef | multi-origin | 4 | 4 | creative_ir, evaluation, benchmark, governance | Sutherland, Heath, Ogilvy, Vignelli |
| D04 | Working within constraints | usef | multi-origin | 4 | 3 | creative_ir, evaluation, production, governance | Vignelli, Bayles, Ondaatje, Murch |
| D05 | Trade-off reasoning | crit | multi-origin | 5 | 5 | creative_ir, evaluation, benchmark, production, governance | Murch, Binet&Field, GoShot, Samara, Freeman |
| D06 | Style & register | usef | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, production, governance | Vignelli, Ogilvy, Samara |
| D07 | Intentional rule-breaking | peri | multi-origin | 5 | 4 | creative_ir, evaluation, benchmark, production, governance | Samara, GoShot, Freeman, GoEdit, Murch |

#### E · Evaluation & critique

| ID | Domain | Imp. | State | Contrib | Indep | Bound to | Contributing sources |
|---|---|---|---|---|---|---|---|
| E01 | What to look for, by objective | crit | multi-origin | 5 | 5 | creative_ir, evaluation, benchmark, governance | Ogilvy, Binet&Field, Miller, Hopkins, GoEdit |
| E02 | Observational unit | crit | multi-origin | 5 | 4 | creative_ir, evaluation, benchmark, production, governance | GoShot, GoEdit, Murch, Freeman, Samara |
| E03 | Diagnostic questions | crit | multi-origin | 5 | 5 | creative_ir, evaluation, benchmark, production, governance | Catmull, GoEdit, LSM, Miller, Vignelli |
| E04 | Common craft failures | usef | multi-origin | 10 | 9 | creative_ir, evaluation, benchmark, production, governance | GoEdit, Samara, Freeman, Hopkins, GoShot, Alton, LSM, Murch, Miller, Heath |
| E05 | Context dependence & exceptions | usef | multi-origin | 5 | 5 | creative_ir, evaluation, benchmark, production, governance | Binet&Field, GoShot, Freeman, Samara, LSM |
| E06 | Interaction among principles | crit | multi-origin | 5 | 5 | creative_ir, evaluation, benchmark, production, governance | Murch, Albers, Samara, Freeman, LSM |
| E07 | Critique process & language | peri | multi-origin | 3 | 3 | creative_ir, evaluation, benchmark, production, governance | Catmull, Vignelli, LSM |
| E08 | Judgement quality & bias | usef | multi-origin | 5 | 5 | creative_ir, evaluation, benchmark, production, governance | Sutherland, Catmull, Bayles, Binet&Field, Heath |

#### Sources

| Source | Objects | Systems | Terms | Bindings |
|---|---|---|---|---|
| Samara | 79 | 6 | 53 | 12 |
| GoEdit | 60 | 5 | 48 | 11 |
| Hopkins | 54 | 5 | 37 | 8 |
| Murch | 39 | 4 | 23 | 8 |
| Freeman | 34 | 5 | 46 | 8 |
| Sutherland | 32 | 3 | 22 | 7 |
| Binet&Field | 28 | 3 | 20 | 4 |
| Heath | 28 | 3 | 22 | 9 |
| Alton | 27 | 3 | 22 | 6 |
| Ondaatje | 27 | 3 | 16 | 6 |
| Bayles | 23 | 3 | 18 | 3 |
| Ogilvy | 22 | 3 | 20 | 5 |
| Catmull | 21 | 2 | 23 | 5 |
| Kenworthy | 20 | 3 | 17 | 6 |
| LSM | 20 | 3 | 14 | 5 |
| Albers | 18 | 2 | 14 | 5 |
| Miller | 18 | 2 | 22 | 7 |
| GoShot | 17 | 3 | 16 | 8 |
| Vignelli | 13 | 2 | 17 | 4 |

| TOTAL (19) | 580 | 63 | 470 | 127 |

#### Packs

| Pack | Domains | Contrib | Indep origins | State |
|---|---|---|---|---|
| composition and attention | 6 | 8 | 7 | covered |
| typography and copy | 4 | 5 | 5 | critical hole |
| product appearance | 5 | 4 | 4 | critical limited |
| colour and visual register | 3 | 6 | 6 | covered |
| camera and spatial grammar | 4 | 6 | 4 | covered |
| editing pacing and short form | 7 | 4 | 3 | critical hole |
| commercial communication | 9 | 6 | 6 | critical limited |
| concept and distinctiveness | 7 | 11 | 10 | covered |
| indian indic context | 1 | 0 | 0 | absent |
| critique and effectiveness | 10 | 18 | 16 | covered |

`Indep` is the largest set of contributors that are mutually independent origins. Where it is lower
than `Contrib`, a dependence relation is blocking — the machine-readable companion names which pair
and why, per domain.

## 5. What changed against the v0 map

### Corrections — v0 was right for the wrong reason

| Domain | v0 said | Actually |
|---|---|---|
| A02 Hierarchy / attention | strong, via Picture This / Non-Designer's / Thinking with Type | Multi-origin, but **none of those three is accepted**. Rests on Freeman, Samara, Kenworthy, Murch, Grammar of the Edit, Vignelli. |
| E07 Critique process & language | strong, via Discussing Design | **Discussing Design is not accepted.** Rests on Catmull's Braintrust and Light Science & Magic's terminological discipline. |
| E08 Judgement quality & bias | strong, via Noise / Thinking Fast and Slow / Superforecasting | **None of the three is accepted.** Rests on Sutherland, Catmull, Bayles & Orland, Binet & Field, Heath. |

### Upgrades — genuinely better than v0 recorded

| Domain | v0 said | Now | Why |
|---|---|---|---|
| D05 Trade-off reasoning | weak; "scattered, no single source" | multi-origin (5) | Still true that no source *teaches* trade-offs. But five sources carry explicit trade-off machinery: Murch's ranked Rule of Six with sacrifice rules, Binet & Field's budget shift toward the harder task, Grammar of the Shot's rules held defeasible, Samara's "regularity is the value and the danger", Freeman's refusal of a placement rule. **The raw material for cross-source synthesis exists. The synthesis has not been done.** |
| E02 Observational unit | weak; Grammar of the Shot only | multi-origin (4 indep) | Five sources establish that the inspection unit varies — frame, spread, transition pair, cut. |
| E06 Interaction among principles | weak | multi-origin (5) | Albers is an entire source arguing colour has no fixed appearance in isolation; Murch ranks six criteria that routinely conflict. |
| D07 Intentional rule-breaking | medium | multi-origin (4 indep) | Five sources state when their own rules should be broken. |
| C14 Effectiveness evidence | weak; newest source 1923 | multi-origin (3) | CANON-007 added Binet & Field (2013) and aggregate econometric evidence. |

### Downgrades — the honest ones

| Domain | v0 said | Now | Why |
|---|---|---|---|
| C09 Hooks & openings | weak | `representation_or_evidence_limited` | Three origins hold real hook knowledge, but **all of it assumes a reader who has already stopped on a page.** The feed hook — first 1–2 seconds, sound-off, thumb-stopping — is a different problem. The attention principle may transfer; that is untested and must not be asserted. |
| A13 Product / packshot photography | weak | `present_but_application_unbound` | Reflection control and lighting function are real and relevant, but **every binding from both contributors is a physical-production candidate.** Nothing is translated into what to ask for, or inspect in, a generated packshot — and SPEC-04 forbids auto-translating physical advice into generative instruction. |
| B12 Motion design, B13 Colour grading | absent / weak | `absent` | One incidental domain tag each, on objects about something else. A passing mention is not knowledge. Recorded as `incidental_only` rather than counted. |

### A discrepancy in the legacy artifact, recorded and not silently fixed

**The v0 map's own summary block does not match its own tables.** Counting its rows directly:

| v0 summary claims | Actual rows in v0 |
|---|---|
| Domains mapped **52** | **56** |
| critical importance **22** | **27** (22 plain + 5 bolded) |
| strong or medium **37** | **40** |
| weak **10** | **12** |
| absent **5** | **4** |

The percentage happens to survive (37/52 and 40/56 both round to 71%), which is probably why it was
never caught. The Canon V1 runbook inherits the "52" from this summary and asks for 52/52 domains
accounted for; **this rebaseline accounts for all 56 actual rows**, which satisfies that
requirement as a superset.

**I have not edited the v0 map.** Historical baselines are never rewritten to match current numbers,
and this is a defect in a historical artifact, not a discrepancy to argue about. It is recorded here
and routed in the Controller Brief.

## 6. What this means for the first product

**The Canon is strong where craft is old, stable and Anglo-American. It is weakest exactly where the
first product lives.** That was true in August and it is still true — but the shape has changed.

Three things are genuinely good news:

1. **Evaluation and critique is the strongest pack** — 18 contributing sources, 16 independent
   origins across 10 domains. The Canon is currently better at *judging* creative work than at
   *making* it. That is an asset, because the product needs both and the judging half is what feeds
   Eval's creative evaluator.
2. **Failure vocabulary is the most harvestable unused asset.** Ten of nineteen sources name craft
   failures explicitly, with named terms throughout the ontology. It has never been consolidated.
3. **Trade-off material is present** where v0 said it was not, which is the one thing a Canon can
   do that no individual book can.

And three that are not:

1. **`indian_indic_context` is an empty pack.** One domain, zero contributors. It is the only pack
   in that state.
2. **`editing_pacing_and_short_form` has four contributors and only three independent origins**, and
   its short-form domain is empty. This is the pack most exposed to the first product's video scope.
3. **Every moving-image contributor writes about film**, at a scale where a single scene is longer
   than an entire 6–20 second commercial. The knowledge is real; the scale is wrong. Whether it
   transfers is a question for the C5 value gate, not an assumption to make now.

## 7. Verification

Everything in this document was produced and checked in this session.

| Check | Result |
|---|---|
| `python3 canon/validation/validate_audit_gate_v02.py` | **19 records, 0 errors**, exit 0 |
| 19/19 accepted source directories accounted for | pass — `sources_contributing_to_no_domain` is empty |
| 56/56 domains accounted for | pass — generator fails if any domain is missing |
| 10/10 packs accounted for | pass — every domain in exactly one pack, enforced |
| Every named contributor is a real accepted directory | pass — generator fails closed on an unknown name |
| Independence via the committed validator, not by author name | pass — `independent_origins_ok()` imported, not reimplemented |
| No domain status rests on a title or library assumption | pass by construction — contributors assigned from committed extraction only |

Reproduce with `python3 canon/planning/build_live19_coverage.py`. Authored input is
`live19_domain_map.yaml`; everything mechanical is computed, not typed.

**Not done here:** no source was ingested, no extraction was modified, no audit record was touched,
no spec was changed, and the historical 16-source instrument was not run or altered.
