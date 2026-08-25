# Canon V1 — gap-closing source portfolio (C4)

**Task:** CANON-V1 overnight program, work package C4 · **Date:** 26 Aug 2026
**Status:** RESEARCH ONLY. **Nothing acquired, purchased, downloaded, logged into or ingested.**
**Input:** `canon/planning/CANON-V1-GAP-LEDGER.md` · **Portfolio size: 12 candidates (cap 14)**

---

## 0. Read this before anything else — what this session could and could not verify

**Outbound web fetching is blocked in this cloud session.** Web *search* works; opening a page does
not. Every attempt returned `EGRESS_BLOCKED` from the network proxy — including `dsource.in`,
`type-together.com` and `w3.org` — and direct `curl` to any host returns no response.

The practical consequence, stated plainly:

- Candidate **identities** below come from search results and are labelled with a confidence level.
- Candidate **access routes and licence terms are `not_verified_in_cloud_session`.** I could not open
  a single official page to confirm what is actually published, at what price, under what terms.
- **No candidate here is cleared for acquisition.** Each needs its access route confirmed before any
  ingestion decision, which is a Controller step in any case.

This is an execution-environment limitation, not a stop condition, and not a reason to guess. Where a
slot has no candidate I could establish with reasonable confidence, it says so rather than being
filled to look complete.

**One further caution, and it is the reason this section exists.** A search for official platform
creative guidance returned almost entirely third-party agency blogs, several repeating widely
circulated statistics with no traceable origin. **None of that is recorded below as fact.** Only
frameworks that search results consistently attribute to a named publisher appear here, and their
substance is still unverified.

## 1. The rule this portfolio follows

**Every candidate must close a named gap from the ledger.** Not "this is a good book" — "this
addresses G2, which blocks eighteen video briefs". Interest is not a reason.

Two gaps deliberately have **no** candidates, and that is the finding rather than a shortfall:

| Gap | Why no source is proposed |
|---|---|
| **G10 — cross-source synthesis not done** | Trade-off reasoning, principle interaction, context dependence and failure vocabulary all have strong multi-origin raw material and no synthesis across it. Adding sources makes an unsynthesised corpus **larger, not better**. This is C7 work. |
| **G11 — physical-to-generative translation not done** | The lighting and material knowledge is real and bound only as physical-production candidates. SPEC-04 requires that translation be deliberate. No book supplies it. C7/C8 work. |

**These two are why the runbook puts the value gate before source expansion.** If the Canon's problem
is unsynthesised knowledge rather than missing knowledge, buying twelve more books makes it worse.
C5 is what distinguishes the two cases, and it has not run.

---

## 2. Slot 1 — Devanagari / Indic typography (cap 2, used 2) · gap **G1**

### D1 · Dalvi, "Anatomy of Devanagari Typefaces" — RECOMMENDED

| Field | Value |
|---|---|
| Identity | Girish Dalvi, *Anatomy of Devanagari Typefaces*, in **Design Thoughts**, IDC IIT Bombay, 2009, pp. 30–36 |
| Identity confidence | **Medium-high** — search results consistently report this citation, including page range |
| Proposed scope | The whole paper. It is short by design |
| Gap / pack | G1 · `typography_and_copy`, `indian_indic_context` |
| Why not already covered | The Canon holds **no** non-Latin script material of any kind |
| Source type | Peer-context academic paper; evidence is scholarly analysis, not practitioner assertion |
| Access route | Design Thoughts is IDC IIT Bombay's own publication. **Route not verified in this session** |
| Access state | `not_verified_in_cloud_session` |
| Rights | `not_verified` |
| Lineage | **`derivative_of` the blocked CANON-008 thesis.** Same author, same conceptual model. Must be declared at ingestion, not discovered after |
| Contingency | `durable_mechanism` expected — letterform structure, not technology |
| Extraction hazards | Typography papers are figure-heavy. Expect `figure_semantic_binding_lost`, the category CANON-007 added, where a diagram's labels survive but which label belongs to which letterform part does not. Every structural claim will need reading from a page render |
| Cost | Unknown; institutional journals of this kind are frequently free |
| Disposition | **RECOMMENDED** |

**Why this is the most valuable single candidate in the portfolio.** It is precisely
**CANON-008 Controller Option 2** — a different bibliographic identity carrying knowledge derived
from the blocked thesis. The brief said selecting a replacement source was the Controller's call and
declined to go looking. C4 is authorised to look, and this is what looking found. It does not require
the IIT Bombay credential that blocked CANON-008.

**Its limit, stated honestly:** a six-page paper is not a 200-page thesis. It should be expected to
establish letterform anatomy and vocabulary — which is exactly what the Canon lacks — and not the
full conceptual model. That may be enough. It is not the same thing.

### D2 · TypeTogether, "Devanagari Type Anatomy" — RESERVE

| Field | Value |
|---|---|
| Identity | *Devanagari Type Anatomy*, attributed in search results to **Pooja Saxena**, published by **TypeTogether** |
| Identity confidence | **Medium** — publisher and title consistent; exact form (article, guide, series) unconfirmed |
| Proposed scope | The anatomy reference itself |
| Gap / pack | G1 · `typography_and_copy` |
| Why not already covered | As D1 |
| Source type | Practitioner/foundry reference — a working type designer's account |
| Access route | TypeTogether's own site. **Blocked in this session** (`EGRESS_BLOCKED`) |
| Access state | `blocked_in_this_session` — the site was reachable in principle, not from here |
| Rights | `not_verified`. A commercial foundry's editorial content may restrict reuse; must be checked |
| Lineage | Independent of D1 as far as can be told — different author, different institution. **Both draw on the same shared body of Devanagari type practice**, so a shared-informant relation must be considered at ingestion rather than assumed absent. The corpus has been caught by exactly this twice |
| Contingency | `durable_mechanism` expected |
| Extraction hazards | Likely to be a web resource with interactive or image-based diagrams — a harder extraction target than a PDF, and possibly one where the structure lives entirely in images |
| Cost | Unknown; foundry editorial content is often free |
| Disposition | **RESERVE** — take only if D1 proves too thin, and only after checking lineage against it |

---

## 3. Slot 2 — short-form / feed-native creative grammar (cap 3, used 3) · gaps **G2, G5**

### S1 · Google/YouTube "ABCDs of effective video ads" — RECOMMENDED

| Field | Value |
|---|---|
| Identity | Google's **ABCD** framework — Attention, Branding, Connection, Direction — published via Think with Google and Google Ads Help |
| Identity confidence | **High** — multiple independent results, including Google's own domains, agree on the framework and its four terms |
| Proposed scope | The published playbook, plus the Attention section specifically for gap G5 |
| Gap / pack | G2, G5 · `editing_pacing_and_short_form`, `commercial_communication` |
| Why not already covered | The Canon's newest source is 2013 and every moving-image source is about film. Nothing addresses opening seconds, sound-off viewing or feed placement |
| Source type | **Platform-authored empirical research.** Search results consistently describe validation with Ipsos, and review involving Nielsen and Kantar, across a large campaign set |
| Access route | Google's own published documentation. Free as far as can be told. **Not verified in this session** |
| Access state | `not_verified_in_cloud_session` |
| Rights | `not_verified` |
| Lineage | Independent of everything in the corpus |
| Contingency | **`technology_contingent` — and this must be recorded at ingestion, not later.** It describes one platform's ad products at one time. Platform behaviour changes; the Canon's audit gate has a class for exactly this |
| Extraction hazards | Presented as a playbook with heavy figure use. Same `figure_semantic_binding_lost` risk as D1 |
| Evidence caution | **The publisher sells advertising on the platform the research validates.** This is the same shape as the caution already recorded against *Effectiveness in Context*, whose percentages are self-graded from a declaredly biased sample. Record as `mixed_own_and_third_party`. The third-party review involvement moderates this; it does not remove it |
| Cost | Believed free |
| Disposition | **RECOMMENDED** — the strongest short-form candidate, with its interest declared |

### S2 · Meta official creative guidance — RESERVE (identity unresolved)

| Field | Value |
|---|---|
| Identity | **Not established.** Meta publishes creative guidance across several properties. Search returned overwhelmingly third-party agency blogs restating it, not the official artifact |
| Identity confidence | **Low** — no specific citable document identified |
| Gap / pack | G2, G5 · `editing_pacing_and_short_form` |
| Access state | `unknown` |
| Disposition | **RESERVE, pending identification.** Do not approve a slot for "Meta guidance" in the abstract |

**Recorded deliberately rather than dropped**, because Instagram Reels is a primary surface for the
first product and the gap is real. What is missing is a specific artifact to point at. **The agency
blogs that dominate the search results are not a substitute** — several repeat unsourced statistics,
and admitting them would breach the standing rule that the Canon holds what a source establishes, not
what circulates.

### S3 · TikTok Creative Center official best practices — RESERVE (identity unresolved)

Same position as S2: a plausible official route exists, no specific artifact was identified from this
session, and the platform's relevance to the Indian first-product market needs checking separately
given TikTok's status in India. **Access state `unknown`. Do not approve without an identified
artifact.**

---

## 4. Slot 3 — Indian cultural / market context (cap 2, used 2) · gap **G3**

### I1 · Cayla & Elson, "Indian Consumer Kaun Hai?" — RECOMMENDED

| Field | Value |
|---|---|
| Identity | Julien Cayla & Mark Elson, *Indian Consumer Kaun Hai? The Class-Based Grammar of Indian Advertising*, **Journal of Macromarketing**, 2012, DOI `10.1177/0276146712442547` |
| Identity confidence | **High** — a DOI was returned directly |
| Proposed scope | The full article |
| Gap / pack | G3 · `indian_indic_context`, `commercial_communication` |
| Why not already covered | Every one of the 19 accepted sources is Anglo-American. `indian_indic_context` has **zero** contributors and is required by **20 of the 30 briefs** |
| Source type | **Peer-reviewed academic research** — a different evidence basis from anything currently in the Canon, which is dominated by practitioner assertion |
| Access route | Journal publisher. **Not verified.** Likely paywalled; author copies are sometimes available through institutional repositories |
| Access state | `not_verified_in_cloud_session`, **probable purchase or institutional access required** |
| Rights | `not_verified` |
| Lineage | Independent of the corpus |
| Contingency | **`historical_convention` risk is real and should be declared.** A 2012 analysis of Indian advertising describes a market that has changed substantially. Useful for durable register and class grammar; must not be treated as current market fact |
| Extraction hazards | Standard academic prose — the cleanest extraction target in the portfolio |
| Cost | Unknown; single-article purchase typically modest. **Not purchased** |
| Disposition | **RECOMMENDED** — closes the most-demanded empty pack, with an explicit currency caveat |

### I2 · Bhatia, *Advertising in Rural India* — RESERVE

| Field | Value |
|---|---|
| Identity | Tej K. Bhatia, *Advertising in Rural India: Language, Marketing Communication and Consumerism*, 2000 |
| Identity confidence | **Medium-high** — consistent across a review record and a database listing |
| Proposed scope | The chapters on language and code-mixing specifically |
| Gap / pack | G3 · `indian_indic_context`, `typography_and_copy` |
| Why proposed | It addresses the **language-mixing** half of G3 directly, which matters because **10 of the 30 briefs are Hinglish** and several mix scripts *within a single line*. No accepted source says anything about when mixing is natural or what it signals |
| Access route | Academic publisher / library. **Not verified** |
| Access state | `not_verified_in_cloud_session` |
| Contingency | **`historical_convention`, strongly.** A 2000 study of *rural* advertising against a first product aimed largely at urban small business. Useful on code-mixing mechanics; weak on current market |
| Disposition | **RESERVE** — take only if the Hinglish gap proves material at the value gate |

**Alternate considered and not proposed:** Kumar & Krishnamurthy, *Advertising, Brands and Consumer
Behaviour: The Indian Context* (SAGE India). Broader and more current, but it overlaps heavily with
commercial-communication material the Canon already holds from five independent origins. It would add
Indian *examples* to knowledge the Canon already has, where I1 adds a cultural grammar it lacks
entirely. Recorded so the choice is visible and reversible.

---

## 5. Slot 4 — product / packshot photography (cap 2, used 1) · gap **G4**

### P1 · *Light: Science & Magic* — chapters beyond ch3 — RECOMMENDED (scope extension)

| Field | Value |
|---|---|
| Identity | *Light: Science & Magic*, **already an accepted Canon source at chapter 3 only** |
| Proposed scope | The later chapters treating specific surface classes — metal, glass, liquids — and product cases |
| Gap / pack | G4 (convention half) · `product_appearance` |
| Why this before a new book | The Canon already holds this book's **theory** (family of angles, three reflection types) and stops before its **application**. The briefs need glass (BR-F02-EN), a metal tin (BR-F02-HI), a foil wrapper (BR-F02-HG) and steam on food (BR-F09-HG). Extending a source already audited and accepted is cheaper and lower-risk than acquiring an unknown one |
| Access route | The physical or licensed copy already used for CANON-003's chapter 3 |
| Access state | **`not_available_in_cloud_session`** — the copy is not in GitHub and I do not assume a laptop copy exists |
| Lineage | **Same work as an accepted source.** Zero independence with `light_science_and_magic_ch3`, and must never count as convergence with it |
| Schema question, flagged not answered | A new chapter span of an already-accepted work needs a decision: a new `source_id` with a declared relation, or an extension of the existing one. The Audit Gate binds a record to **exact bytes**, so extending in place would invalidate the existing record. **This is a Controller/schema question and I have not decided it** |
| Cost | None if the copy is already held |
| Disposition | **RECOMMENDED**, subject to the scope question above |

### Second packshot slot — **NO CANDIDATE PROPOSED**

I could not establish a specific product-photography source with enough confidence to name one, and
naming a plausible-sounding title I had not verified would be inventing a citation. The slot stays
open. **Note that P1 addresses only the *convention* half of G4; the *translation* half is G11 and no
source closes it.**

---

## 6. Slot 5 — modern effectiveness evidence (cap 2, used 2) · gap **G14 context**

### E1 · Binet & Field, *The Long and the Short of It* — RECOMMENDED

| Field | Value |
|---|---|
| Identity | Les Binet & Peter Field, *The Long and the Short of It* |
| Identity confidence | **High** — already named in `canon/HANDOFF.md` |
| Gap / pack | Deepens `commercial_communication`; strengthens objective-setting |
| Lineage | **`shared_author` AND `same_series` with the accepted *Effectiveness in Context*.** The handoff already records this as a dependency **to declare at ingestion rather than discover afterwards** — this candidate exists partly to make sure that declaration actually happens |
| Independence consequence | Zero independence with `binet_field_effectiveness_in_context_ch1`. It deepens one origin; it does not add one |
| Access state | `not_verified_in_cloud_session` |
| Contingency | `technology_contingent` in part — media-mix conclusions age |
| Extraction hazards | Chart-heavy. `figure_semantic_binding_lost` is near-certain; numbers must be read from page renders, as CANON-007 required |
| Disposition | **RECOMMENDED** — lowest-risk candidate in the portfolio, because the corpus already knows exactly what it is getting |

### E2 · Sharp / Ehrenberg-Bass, *How Brands Grow* — RESERVE

| Field | Value |
|---|---|
| Identity | Byron Sharp, *How Brands Grow*, Ehrenberg-Bass Institute |
| Identity confidence | **Medium-high** — widely cited; not verified from an official page in this session |
| Why proposed | An empirical tradition that **partly disagrees** with Binet & Field. That is the point: the Canon's most useful property is holding both sides of an argument, which is what makes trade-off reasoning possible (see D03 in the coverage map) |
| Lineage | Independent of Binet & Field — different institution, different data, genuinely different conclusions |
| Access state | `not_verified_in_cloud_session`; purchase likely |
| Disposition | **RESERVE** — take after E1, and only if cross-source synthesis (C7) is actually going to happen. **An unsynthesised disagreement is worse than no disagreement**, because a retrieval system would surface contradictory advice with nothing to adjudicate it |

---

## 7. Slot 6 — motion design / animated typography (cap 1, used 0) · gap **G6**

**NO CANDIDATE PROPOSED.** No source identity was established with enough confidence from this
session, and the slot is not important enough to justify a guess. G6 is a Tier-3 gap. The need is
recorded; the slot stays empty until a real candidate exists.

---

## 8. Slot 7 — accessibility / thumbnail legibility (cap 1, used 1) · gap **G8**

### A1 · W3C, WCAG 2.2 — text contrast and text-in-image criteria — RECOMMENDED

| Field | Value |
|---|---|
| Identity | **W3C Web Content Accessibility Guidelines 2.2**, specifically the contrast and text-presentation success criteria |
| Identity confidence | **High** — a formal, stable W3C standard |
| Proposed scope | The contrast criteria and their Understanding documents, not the whole specification |
| Gap / pack | G8 · spans `composition_and_attention`, `typography_and_copy` |
| Why not already covered | Every accepted typographic source assumes a held page or a print surface. Nothing addresses legibility at feed scale on a phone. The Canon's nearest instrument is Miller's grunt test, **written about websites** |
| Source type | **A published standard with numeric thresholds** — a different kind of knowledge from anything in the Canon, which currently holds no numeric acceptance criteria at all |
| Access route | W3C publishes openly. **`w3.org` was blocked from this session**, so not verified here |
| Access state | `blocked_in_this_session`; expected open |
| Rights | W3C document licence — permissive, but **`not_verified`** |
| Lineage | Independent of everything in the corpus |
| Contingency | `historical_convention` in part — thresholds are versioned and revised |
| Extraction hazards | Low. Structured normative prose, the cleanest target in the portfolio |
| Important caution | **These are web accessibility thresholds, not commercial-creative legibility rules.** Adopting them as creative criteria without saying so would import an unstated assumption. They should enter as what they are — an external standard with a stated origin and scope |
| Cost | None expected |
| Disposition | **RECOMMENDED** — cheap, open, precise, and it gives Eval something the Canon has never supplied: a checkable numeric criterion |

---

## 9. Slot 8 — semiotics of consumer imagery (cap 1, used 1) · gap **G7**

### C1 · Williamson, *Decoding Advertisements* — RESERVE

| Field | Value |
|---|---|
| Identity | Judith Williamson, *Decoding Advertisements: Ideology and Meaning in Advertising* |
| Identity confidence | **Medium** — a standard work in the field; **not verified from a publisher page in this session** |
| Gap / pack | G7 · `concept_and_distinctiveness` |
| Why proposed | The Canon's metaphor and symbolism knowledge is thin: Ondaatje's hat and Vignelli's semantics. Nothing analyses how consumer imagery *signifies* |
| Source type | Critical/theoretical analysis |
| Contingency | **`historical_convention`, strongly.** A late-1970s analysis of advertising imagery. Its method may transfer; its examples will not |
| Honest caution | The v0 coverage map already warned that Berger and Sontag are **critique, not craft**. The same warning applies here. This is a reading method, not a production method, and admitting it risks importing analysis the product cannot act on |
| Access state | `not_verified_in_cloud_session` |
| Disposition | **RESERVE** — lowest priority in the portfolio. G7 is Tier-3 and the risk of adding unusable material is real |

---

## 10. Every gap accounted for

| Gap | Tier | Route |
|---|---|---|
| G1 Devanagari | 1 | **D1 recommended**, D2 reserve |
| G2 short-form | 1 | **S1 recommended**; S2/S3 reserve pending identification |
| G3 Indian context | 1 | **I1 recommended**, I2 reserve |
| G4 packshot | 2 | **P1 recommended** (convention half only); translation half is G11, non-source |
| G5 hooks | 2 | **S1** (its Attention material) |
| G6 motion design | 3 | **No candidate found** — slot left empty |
| G7 semiotics | 3 | C1 reserve, with a stated risk of unusable material |
| G8 accessibility | 3 | **A1 recommended** |
| G9 gestalt mechanism | 3 | **Non-source, and possibly already solved.** The v0 map credits this to *Picture This*, which is CANON-001/002 output sitting on **unmerged branches**. Recovering that work may close G9 at zero acquisition cost. Routed, not proposed as a purchase |
| G10 synthesis | 4 | **No source. C7 work** |
| G11 physical→generative | 4 | **No source. C7/C8 work** |

## 11. If only three are approved

**D1 (Devanagari), S1 (short-form), I1 (Indian context)** — one per Tier-1 empty domain, each the
cheapest credible route into a pack the first product needs and the Canon has nothing for.

**E1 is the safest** but adds no independent origin, and **A1 is the cheapest** but addresses a
Tier-3 gap.

## 12. What was not done, explicitly

No acquisition, purchase, download, login, account creation, click-through acceptance, gated access
or DRM interaction. No unofficial mirror, rip, torrent or unauthorised copy was sought or used. No
source was ingested and no source directory was created. **Live Canon remains 19.**

No access route was verified, because none could be opened from this session. Every route above is a
proposal to be confirmed before any acquisition decision — which is a Controller decision regardless.
