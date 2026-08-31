# PROPOSED — G3b expert elicitation spec: the operational half of Indian-market knowledge

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

**What this is.** A structured questionnaire specification for eliciting the operational
Indian-market knowledge no book in the corpus carries (GAP-19): festival codes by
occasion/region, price framing, Hinglish register rules, and category conventions. Answers would
be versioned and admitted under a VARIANT of the Audit Gate as **elicited-expert knowledge, never
book knowledge**. This document creates no knowledge, elicits nothing, admits nothing, and
proposes the gate variant for a Controller decision. USD 0. Gaps addressed: GAP-19.

## 1. Why elicitation, and scope exclusion

The 5 accepted India sources (bijapurkar-we-are-like-that-only, dwyer-patel-cinema-india,
jain-gods-in-the-bazaar, pandey-pandeymonium, parameswaran-nawabs-nudes-noodles — all under
`canon/knowledge/current/`) are 2002–2016 cultural history: they supply register, iconography and
consumer meaning-making, and they are the corpus slice most dated by technology contingency.
**Out of scope for elicitation (already covered by those sources):** cultural register,
iconography, calendar-art/bazaar visual tradition, middle-class meaning-making, film-culture
grammar. **In scope (covered by no source):** current operational codes a media-production run
must get right — the four question banks below. The demand is buyer-proven: 20/30 marketplace
briefs are Devanagari-primary or Hinglish, and MKT-015/MKT-016 are `runnable_now: false` for
exactly this knowledge (`canon/repair/CANON-REPAIR-GAP-REGISTER-v1.md`, GAP-19 evidence).

## 2. Respondent and method

Respondent: the human India-market practitioner the Controller designates (the acceptance
authority is the natural first respondent). Method: written structured questionnaire, one bank at
a time; every answer captured with the metadata in §5; no answer paraphrased by the eliciting
agent — verbatim capture, clarifying questions allowed, leading questions not. An "I don't know /
it varies" answer is recorded as such; unanswered cells stay empty rather than being filled by
model knowledge — a model-generated answer in an elicitation artifact is a fabrication.

## 3. Question banks

### Bank F — festival codes by occasion × region

For each of: Diwali, Holi, Eid (both), Raksha Bandhan, Navratri/Durga Puja, Ganesh Chaturthi,
Onam, Pongal, regional new years (Baisakhi/Ugadi/Gudi Padwa/Poila Boishakh), Christmas,
Independence/Republic Day, and the wedding season:

- F1. Which regions/communities is this occasion commercially live in, and where is it a mistake
  to lead with it?
- F2. Colour and motif codes: what reads right, what reads wrong or offensive (colours, symbols,
  deities — when is deity imagery acceptable in a commercial context, when never)?
- F3. Greeting conventions: exact phrasings by language/script, formal vs familiar.
- F4. Commercial timing: when do promos start and end relative to the date; what does
  "festival price" signal in this occasion?
- F5. Category fit: which product categories own this occasion (sweets, gold, appliances,
  apparel, vehicles), and which look opportunistic?

### Bank P — price framing

- P1. Rupee display: ₹ symbol vs "Rs.", lakh/crore vs million, digit grouping (1,00,000 vs
  100,000) — by audience and formality.
- P2. Endings and levels: where do 99/999-endings help vs read as cheap; category norms for
  round-number pricing.
- P3. EMI framing: when to lead with EMI vs total price; typical phrasing; what must legally or
  conventionally accompany it.
- P4. MRP conventions: strike-through-MRP-plus-offer-price display rules; "X% off" vs "flat ₹Y
  off" vs "starting at ₹Z" — which frame per category and audience.
- P5. Value vs discount register: when "value/quality" framing outperforms discount framing;
  festival vs non-festival differences.

### Bank H — Hinglish register rules

- H1. Language ladder: for a given audience (metro/tier-2/tier-3, age band, category), when
  English, Hindi, Hinglish, or a regional language; who must never be addressed in Hinglish.
- H2. Script choice: Devanagari vs Latin script for the same Hinglish line — where does each
  belong (on-screen text, VO subtitles, thumbnails, packaging)?
- H3. Code-switch position: which sentence slots carry the English (brand terms, numbers, CTAs?)
  and which the Hindi; what does inverting them signal?
- H4. Honorifics and address: aap/tum/tu selection by audience and category; consequences of
  getting it wrong.
- H5. CTA phrasing: current, non-cringe CTA idioms per platform; which borrowed-English CTAs are
  dead.

### Bank C — category conventions

- C1. For each priority category (from the marketplace demand bank: real-estate/rentals, D2C
  food & beverage, skincare, watches/premium accessories, industrial/safety, faceless
  explainer content): the visual and copy conventions a local buyer expects.
- C2. Trust markers: which certifications, badges, guarantees actually carry weight per category.
- C3. Premium coding: what makes a frame read "premium" to an Indian metro audience vs "export
  premium" vs "loud local" — concrete markers (pace, palette, VO accent, music).

### Bank A — acceptance questions from buyer-proven briefs (asked first; they gate real work)

From MKT-015 (Industrial HSSE Safety Video Producer, Hindi/Urdu VO + localisation; Upwork rows
89+95) and MKT-016 (Faceless Video Editor — Mystery/Explainer/Historical, Hinglish; Upwork row
83), both in `canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml`:

- A1. Hindi vs Urdu VO for industrial safety content: how does the choice map to workforce,
  region and client expectation; is a single neutral register acceptable, and what is it called?
- A2. Safety-critical VO norms: register, pace, sentence length, and terminology handling
  (English technical terms retained vs translated) for HSSE content; what makes a safety VO
  sound authoritative rather than theatrical?
- A3. Localisation acceptance: what does a buyer like MKT-015's expect "localised" to include
  (on-screen text, signage in footage, units, examples)?
- A4. Hinglish faceless-channel conventions (MKT-016): hook phrasing idioms for
  mystery/explainer/historical content; retention-line placement; subtitle script choice
  (Devanagari, Latin, dual) and caption density norms.
- A5. For both: what would make the buyer reject a technically clean deliverable — the H1/H6-type
  acceptance criteria in their own words.

## 4. Versioning

Each completed bank is a dated, versioned artifact (e.g. `G3B-BANK-F-v1.yaml`), superseded by new
versions, never edited in place. Answers carry per-answer review-by dates: festival and platform
codes rot; an answer past its review-by date is stale and must not enter a newly compiled pack
until re-confirmed. Proposed home: `canon/knowledge/elicited/` — the Controller decides the actual
location; nothing is created by this spec.

## 5. Admission under a variant gate — elicited-expert knowledge, never book knowledge

The Audit Gate v0.2 is source-file-shaped (byte fingerprints, visual-evidence ledger). Elicited
knowledge has no source file, so a variant gate is required — a Controller decision, proposed
here, would define it with at minimum:

- `knowledge_class: elicited_expert` on every object — never mixed silently with book-derived
  doctrine; a compiled pack that includes elicited items must label them as elicited, with date.
- Provenance per answer: questionnaire version, question id, respondent identity, elicitation
  date, verbatim answer text, and the respondent's own confidence (knows / believes / guesses).
- No corroboration claim: an elicited answer corroborates nothing and is corroborated by nothing
  until a second independent respondent answers the same question; single-respondent answers are
  marked so.
- Snapshot + validator: the variant record still takes a file snapshot of the bank artifact in
  `canon/audit/records/` and must pass an extended validator before any pack consumes it.
- Review-by enforcement: the validator rejects packs citing elicited answers past review-by.

**Boundary rule (restated from the corpus's own hygiene):** elicited answers are the expert's
testimony about current practice — not measurements, not research findings, and not Canon book
doctrine. They fill G3's operational half precisely because no admissible source covers it; the
moment a published, admissible source does cover a cell, the source supersedes the elicitation
for that cell.

## 6. What this spec does not do

It does not elicit (no questionnaire has been sent), does not create the variant gate, does not
create `canon/knowledge/elicited/`, does not modify the gap ledger, and does not claim the
Controller has agreed to any of it.
