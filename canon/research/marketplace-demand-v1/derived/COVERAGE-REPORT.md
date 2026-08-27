# CANON-011 — Marketplace-derived brief bank, coverage report

**Task:** CANON-011 · **Date:** 27 Aug 2026 · **Spend:** USD 0 · **External calls:** 0
**Status:** PROPOSED WORKER OUTPUT. Not frozen, not merged, not an approved benchmark.

**Every number below is computed**, by `measure_coverage.py`, into
`coverage-measurement.json`. Nothing here is counted by hand. Where a figure comes from the
source research rather than from our banks, it says so.

---

## 0. The one-paragraph version

Eighteen benchmark cases were derived from individual Upwork buyer jobs. Sixteen can be run
without going back to the buyer. Their most useful property is not what they cover but what
they **fail** to cover: **one of eighteen real, paid commercial jobs asks for exact text in
the picture**, against **28 of 30** in the project's authored brief bank. The authored bank is
not wrong — it was built as a probe — but this is the first evidence from people actually
paying for work that its heaviest requirement is not theirs. Two other things stand out. Real
buyers **almost never say what would make them reject the work**: one of eighteen states a
rejection criterion. And the request record the project froze last week **cannot represent four
things these buyers actually said**, most importantly supplied material that must appear in the
output, and a series where each video is approved on its own but the same character has to be
in all of them.

---

## 1. How many source jobs were considered

| | Count | Source |
|---|---:|---|
| Postings recorded by the research | **114** | recounted from the appendix table |
| Classified by the research as addressable by an AI video pipeline | **67** | bold titles, recounted |
| Classified as not addressable | **47** | non-bold titles, recounted |
| Fiverr gig pages recorded | 42 | cleaned Fiverr report |
| Fiverr listing-only rows recorded | ~40 | cleaned Fiverr report |

The three Upwork figures were **recomputed mechanically** rather than taken from the prose:
the appendix holds 114 numbered rows, 67 with a bold title, 47 without, and the appendix states
that bold titles are the addressable ones. The research's own prose says 67 and 47. They agree.

**What this sample is.** One platform, one logged-in account, one day, eleven search queries,
read-only. It shows that a request shape is being paid for. It does **not** show how often,
relative to what, or by how many buyers — and **no count in this report is a market-share
claim**.

---

## 2. What was selected

**18 cases**, drawing on **19 source rows** (MKT-015 combines two postings by the same client).
Sixteen of those rows are ones the research classified as addressable; three are not, and both
disagreements are recorded on the cases themselves rather than smoothed over.

| Case | Source job | Shape |
|---|---|---|
| MKT-001 | Meta ad, talking head + product B-roll | 40 s avatar-plus-product commercial |
| MKT-002 | E-Commerce Product Video Editor (Knox Deco) | furniture catalogue batch, per-approved-video pricing |
| MKT-003 | AI Video Assembly & Polish | 10 videos from supplied scripts |
| MKT-004 | AI Lecture Videos | 48 lectures from a supplied PDF |
| MKT-005 | 35-second app promo (Funngro) | app promo from a supplied script |
| MKT-006 | AI Video Producer, Norway | two recurring characters across a SaaS series |
| MKT-007 | $50k/mo contract | 75–100 scripts weekly, 30 s–300 s |
| MKT-008 | AI influencer avatar, football lab | persistent persona with no reference |
| MKT-009 | Social media, recurring character | established character held across output |
| MKT-010 | ADS Video Creator | two AI UGC Meta ads per week |
| MKT-011 | Pegasus Sports | TikTok UGC + Amazon product video across a range |
| MKT-012 | Short cinematic product ad | 10–20 s product piece |
| MKT-013 | Replace 4 monitor screens | edit inside a supplied video |
| MKT-014 | Stonebridge Leads | animate a supplied still |
| MKT-015 | HSSE safety induction + Hindi/Urdu localisation | 15–20 min, three spoken languages |
| MKT-016 | Faceless Hinglish channel editor | deliberately left incomplete |
| MKT-017 | Church explainer | supplied script, non-commercial register |
| MKT-018 | High-end cinematic ad, India | buyer supplies concept *and* script |

---

## 3. What was rejected, and why

| Reason | Approx. count | What it looks like |
|---|---:|---|
| Research classified it as not addressable by an AI video pipeline | 44 | wedding editing, games journalism, cold calling, developer work, ad buying |
| A hiring **role or seat**, not a specified deliverable | ~22 | "Full-Time AI Video Creator, $2,000/month, multi-style" |
| Deliverable is not media — text, voice-only, data, consulting | ~14 | scriptwriting, voice-over, translation, annotation, proofreading |
| Too thin to specify without inventing the request | ~8 | a $5 title with no duration, product, script or format |
| Long-form with no content specification | ~3 | 30-minute YouTube story videos; a 6-minute corporate film |

The counts overlap and are approximate; the exhaustive per-row basis is the appendix
classification, which is exact. The bank's `selection_and_rejection` block holds the same list in
machine-readable form.

### The rejection worth arguing about

**UW-107, "Hindi/Hinglish Video Scriptwriter for India-Focused Creatives."** $500 fixed, fewer
than five proposals, a Poland-based buyer with $6K+ spend, 9:16, 15–45 seconds, social casino,
and the research's own note that this buyer clearly produces India-targeted creatives at volume.

It was rejected because **what the buyer is paying for is a script, not a video**. Deriving a
video case from it would invent the production request the buyer did not make — and it would be
the single most misleading invention available in this whole exercise, because it would
manufacture exactly the Hindi/Hinglish video-production demand that the sample does not show.
The format and language facts are real and are recorded; the customer brief is not.

**MKT-016 is the counter-example, kept on purpose.** It is a posting too thin to derive a
complete case from, and instead of dropping it, the bank carries it with the route-neutral brief
explicitly marked *NOT SPECIFIABLE FROM THE SOURCE* and the envelope marked
`envelope_completeness: incomplete_by_design`. One worked example of where the evidence runs
out is worth more than an assertion that the line exists.

---

## 4. Distributions

### Requested operation

| Operation | Marketplace 18 | Authored 30 | Coverage extension 11 |
|---|---:|---:|---:|
| generate | **14** | 30 | 0 |
| edit | **2** | 0 | 4 |
| animate | **1** | 0 | 2 |
| variants | **1** | 0 | 2 |
| restore | 0 | 0 | 1 |
| extend | 0 | 0 | 1 |
| compose | 0 | 0 | 1 |

**Read this correctly.** The 14:4 split is **not** evidence that generation is what buyers mostly
want. It is what an *AI-video-creator job search* returns — the eleven queries were "AI video
creator", "AI product video", "AI avatar video" and similar, so postings framed as generation
were selected for at the point of search. What the marketplace evidence establishes is narrower
and still useful: **edit-a-supplied-artefact and animate-a-supplied-still are things real buyers
pay for**, which until now the project knew only from model-interface corpora and its own
authored extension items.

### Modality

**18 of 18 video. Zero static image.** This is a sampling artefact and must be read as one: every
query in the research was a video query. The absence of static-image cases here says nothing
about whether buyers commission static creative, and the authored bank's 12 static briefs are not
contradicted by it.

### Language

| Spoken language | Cases | Where it comes from |
|---|---:|---|
| English | 12 | **all 12 are experiment fixtures, not customer statements** |
| None / no speech | 4 | genuinely absent from the request |
| English + Hindi + Urdu | 1 | **customer-stated** (MKT-015) |
| Hinglish | 1 | **customer-stated** (MKT-016) |

**Only two of eighteen buyers state a language at all**, and both of those are the Indic ones.
Everywhere else, the "English" in this bank is a benchmark decision labelled
`experiment_supplied_fixture`, made so cases are repeatable — and it would have been very easy,
and wrong, to record it as customer intent because the platform is English-language.

**The Indic finding, stated carefully.** Across 114 postings, the research found ~150 Hindi
postings a month against ~3,000 AI-video postings, and its own reading is that the Hindi demand
on Upwork is voice-over, dubbing, translation and annotation rather than Indic ad production.
This bank agrees from the other direction: **exactly one buyer in the sample pays for an Indic
language as part of producing a video** (MKT-015, Hindi and Urdu localisation of a safety
induction film) and **one more** wants Hinglish content produced (MKT-016). **Both are among the
two cases that are not runnable**, and neither can be scored, because the project holds no audio
material of any kind. That is a fact about this sample and this platform, not about the world —
the research says explicitly that Indian brands buying Hindi ad production are not on this
channel.

### Provenance of every populated request field

This is the number that says whether the bank kept its promise.

| Label | Count |
|---|---:|
| `absent` | 138 |
| `customer_stated` | 125 |
| `customer_implied` | 63 |
| `experiment_supplied_fixture` | 62 |
| `system_derived` | 47 |

Counting sub-field labels as well as field labels. **138 absent** is the important one: more than
a third of all grammar slots across the bank record that the buyer said nothing, and were left
that way rather than filled. And **62 fixtures are labelled as fixtures**, including every
aspect-ratio choice, every language choice and every identity-invariant list — the three places
where a benchmark most easily invents a customer requirement.

Two fields are worth calling out individually:

- **R08 text requirements: `absent` in all 18 cases.** Not one buyer specified on-screen copy.
- **R18 acceptance intent: `customer_stated` in all 18.** Every posting says something about what
  it wants, even when it says nothing else.

---

## 5. Coverage of the things the project cares about

| | Cases | Note |
|---|---:|---|
| Supplied asset recorded | 16 of 18 | 8 customer-stated, 6 benchmark fixtures, 2 customer-implied |
| Supplied asset as **subject of operation** | 3 | the two edits and the animate |
| Supplied asset whose **role the grammar cannot express** | **8** | see §7 |
| Product identity | 7 | |
| Person / character identity | 3 | |
| Voice identity across assets | 5 | |
| Any identity requirement | **13 of 18** | |
| **Exact text in the picture** | **1 of 18** | MKT-005, the app name |
| Speech present | 13 of 18 | |
| Deliverable set larger than one | 10 of 18 | |
| Set-level invariant alongside per-item acceptance | 3 | |
| Buyer states a **rejection** criterion | **1 of 18** | MKT-006 |
| Ambiguity markers recorded | 37 | contradictions and underspecifications, recorded not resolved |
| Fixtures declared | 43 | 4 of them block runnability |

### Batch and set-level acceptance

| Acceptance basis | Cases |
|---|---:|
| per deliverable | 14 |
| per deliverable **with a set-level invariant** | 3 |
| unresolved | 1 |

**Two buyers state their acceptance basis outright** — Knox Deco's "$30–45 per approved video"
and the university's "$20 per video" both mean each output is accepted on its own and only
approved ones are paid for. That is the first evidence in the project of a real buyer
pre-structuring a deal the way whole-outcome Cost per Accepted Outcome is defined, and MKT-002
carries a real unit price to compute it against.

---

## 6. Evaluator dependencies — and the gate that applies to every case

| Evaluator family | Cases depending on it | Qualified |
|---|---:|---|
| creative / commercial judgement | 15 | **no** |
| structured visual (VLM) | 12 | **no** |
| temporal video | 12 | **no** |
| speech / audio / AV | 11 | **no** |
| deterministic CV & geometry | 11 | **no** |
| operational logging | 6 | **no** |
| text OCR | 1 | **no** |

**`instruments_qualified: 0`, project-wide.** Eleven dependencies across the bank are marked
`hard_blocker` — meaning the material needed to qualify them is not merely unbuilt but unheld.
`runnable_now: true` on sixteen cases means *the inputs can be assembled without contacting the
buyer*. **It does not mean any of them can be judged.** Those are two different gates and the
bank keeps them apart deliberately.

The cheapest paths out, from the project's own qualification map rather than from this task:
temporal truth can be **injected** (a known freeze, a known identity swap) and so needs zero
human labels, only clean base clips; and edit preservation against a base video the benchmark
authored itself is **deterministic** — which is why MKT-013 is the one case here with real
Stage-A value.

### Two things real buyers need that no capability measures

- **CO-01 · Fidelity of a deliverable to a supplied source document.** MKT-004's buyer supplies a
  course PDF; whether the lecture teaches it is their entire acceptance test. This is not
  `spoken_script_correctness`, which compares speech to an exact expected string — here there is
  no expected string, there is a document. A lecture video that is fluent, well-paced and about
  the wrong material passes every capability in the contract.
- **CO-02 · Sustained throughput as an acceptance condition.** MKT-007's buyer asks about team
  size, capacity and workflow rather than about a reel, and wants 75–100 videos a week.
  `reliability_pass_at_k` measures whether one attempt succeeds; nothing measures whether a rate
  can be held.

Also recorded: **CO-03**, that cross-asset identity — handled deliberately as an observation
*scope* rather than as its own capability — turns out to be the primary acceptance condition in
three of eighteen cases and present in five; and **CO-04**, that three buyers state an aesthetic
**prohibition** ("avoid the AI-avatar look", "don't look like stock AI", "look unpolished"), and
the creative family measures achievement of a positive quality rather than avoidance of a named
negative.

---

## 7. Where the frozen request grammar could not hold what a buyer said

Four gaps, all **observations routed to the Controller**. Nothing was invented, no field or value
was added, and every affected slot carries the sentinel `unresolved_not_in_grammar_v1` with a
gap reference rather than being forced into a wrong existing value.

| ID | Gap | Cases | Why it matters |
|---|---|---|---|
| **GG-01** | No asset role for **material the customer supplies that must appear in the output** of a `generate` request | MKT-005, MKT-006, MKT-013 | The natural workaround is to call it a "reference" — and a reference may legitimately be departed from. That would silently turn "this exact footage must be in the video" into a soft preference, and an output that omitted it entirely could pass. |
| **GG-02** | No asset role for a **document supplying the content the deliverable must convey** — a script, a course PDF, a creative concept, visual guidance | MKT-003, MKT-004, MKT-007, MKT-017, MKT-018 | Five of eighteen cases, five different buyers. Supplied source material is the most frequently attested buyer input in this sample and it has nowhere to live in the request record. |
| **GG-03** | `acceptance_basis` offers per-deliverable *or* set-level, with no way to say **per-deliverable acceptance with a set-level invariant** | MKT-006, MKT-008, MKT-009 | This is the requirement the research identifies as the thing that flips an AI-video job from routine pipeline work to expensive custom work. If the request record cannot express it, the benchmark cannot test what decides the product's commercial value. |
| **GG-04** | `deliverable_set` has a cardinality but no **ongoing rate** | MKT-002, MKT-007, MKT-010 | Three buyers state a rate rather than a total — two a week, 75–100 a week, "a substantial portion of our catalog". A rate is a different economic object from a total, and it is the shape the research says is worth selling into. |

GG-01 is the strongest evidenced. MKT-006's buyer says "integrated live SaaS dashboard footage":
that footage is not a reference informing a new artefact, and it is not the artefact being
edited. The grammar has no third option.

---

## 8. Runnable now, and attemptable now — two different questions

| | Cases |
|---|---:|
| **Runnable now** (all inputs assemblable without contacting the buyer) | **16 of 18** |
| Not runnable | 2 — MKT-015, MKT-016 |
| **Attemptable without a Production Planner** | 10 |
| Partially attemptable | 4 |
| Not attemptable | 4 |

**Why the two not-runnable cases fail is worth reading.** MKT-015 needs verified Hindi and Urdu
speech material the project does not hold, and its 15–20 minute duration cannot be shortened
without a Controller scope decision. MKT-016 could only be made runnable by inventing the source
material, the change, the length and the content — which is authoring a brief and calling it
marketplace evidence.

**The attemptability column is the more uncomfortable one.** Four cases — 10 videos of 3 minutes,
48 lecture videos, a 20-minute safety induction, and the 300-second end of a scripted batch — are
ordinary, cheaply-priced commercial jobs that the project currently **has no object capable of
planning**. Production IR does not exist, and these are what its absence costs in real work.

---

## 9. Strongest Stage-C candidates

Ten cases are marked primary for Stage C. Five stand out, and for different reasons:

1. **MKT-002 — Knox Deco catalogue batch.** The only case with a **real per-unit price from the
   buyer** ($30–45 per approved video) plus a revision allowance, a duration band, a master
   format and export formats. It is the only place a genuine Cost per Accepted Outcome can be
   computed against a commercial rate the buyer set rather than one we invented. Best client in
   the sample: 100% hire rate, $180K spent.
2. **MKT-006 — Thomas and Anna.** Identity that must hold across a series **in both the visual
   and the vocal channel at once**, plus supplied live footage that must appear, plus a
   customer-stated aesthetic prohibition, plus a customer-stated register. Nothing in the
   authored bank or its extension combines these. It is also the source of GG-01 and GG-03.
3. **MKT-005 — Funngro app promo.** The **cheapest complete commercial outcome** here: 35
   seconds, one deliverable, fully specified, attemptable today, and the only case carrying an
   exact-text requirement — so it is the natural first Stage-C attempt and the one that connects
   to the exact-text instrument work already under way.
4. **MKT-011 — Pegasus Sports.** The only `variants` case sourced from a real buyer, and the only
   one where the variation axis is **placement** rather than message. One product identity has to
   survive two genuinely different treatments.
5. **MKT-018 — supplied concept and script.** The only buyer who supplies the **creative concept**
   as well as the script. That reframes the hardest question in the project — creative quality —
   into the far more tractable "was this stated intention executed", which no authored item does.

Separately, **MKT-013 is the strongest Stage-A candidate in the bank**: an edit whose preservation
ground truth is held by construction, whose evaluator family is the cheapest to qualify, and whose
operation the authored 30 never exercise.

---

## 10. What this adds beyond the existing 41 authored items

The 30-brief bank and the 11-item coverage extension stay **byte-identical**. Nothing here
replaces them, and the comparison below is structural, not a quality judgement.

**What the authored banks have and this one does not.** Every one of the 41 carries an
objective, an audience and acceptance criteria — which the research confirms no public corpus
has, and which most of these real postings do not have either. Ten of the 30 are Devanagari-primary
and ten Hinglish; this bank has almost no Indic material because the sample has almost none. The
30 cover static image; this bank has none.

**What this bank adds.**

1. **Evidence rather than design.** Every requirement in these 18 cases traces to a verbatim
   string in a committed file, checked mechanically. The 41 are authored probes — legitimately so,
   and never claimed otherwise. This is the first request material in the project that someone
   was actually paying for.
2. **The exact-text correction.** 1 of 18 here against 28 of 30 there. The project already knew
   from CANON-009 that **no corpus anywhere reports how often users ask for text in an image**.
   This does not supply that number and does not claim to — but it is the first direct observation
   that a set of real, fully specified, paid commercial video jobs mostly do not ask for it.
3. **The rejection-criteria observation.** 1 of 18 buyers states what would make them reject the
   work. The authored bank's defining strength is that every brief carries acceptance criteria.
   Real buyers largely do not supply them, which means a live system will have to derive or ask
   for what the authored bank always has.
4. **Commercial structures the authored banks have no concept of.** Per-approved-unit pricing,
   revision allowances inside a unit price, ongoing weekly rates, paid tests before volume,
   two-placement variant pairs, and identity that must persist across a series. Several map
   directly onto Cost per Accepted Outcome, which is the project's primary business metric.
5. **Four concrete limits of the frozen request grammar**, each attested by a paying buyer rather
   than by a design review.
6. **A worked example of refusing to derive** (MKT-016) and **two recorded disagreements with the
   source research** (MKT-013, MKT-015), so the bank's own judgement is auditable rather than
   invisible.

---

## 11. What this report does not claim

- **No prevalence or market-share claim.** One platform, one account, one day, eleven queries.
- **No claim that generate dominates.** The queries selected for it.
- **No claim about static image demand.** The queries excluded it.
- **No claim that Hindi demand is small in the world.** The research says explicitly that this
  channel is the wrong place to look for it.
- **No claim that any case can be scored.** Zero evaluator families are qualified.
- **No claim that any figure here is a budget.** No spend of any kind is proposed.
- **The $50,000 headline in MKT-007 is not money.** That client has 133 postings against $16K of
  recorded spend and a 46% hire rate; the bank records it as aspirational.

---

## 12. Files

| File | What it is |
|---|---|
| `marketplace-brief-bank-v1.yaml` | The 18 cases. Source of truth. |
| `marketplace-prompt-ready-bank-v1.yaml` | Generated envelope view. Do not hand-edit. |
| `COVERAGE-REPORT.md` | This file. |
| `SOURCE-DISCREPANCIES.md` | Four cleaned-vs-raw Fiverr disagreements, recorded not reconciled. |
| `coverage-measurement.json` | Every number in this report. |
| `measure_coverage.py` | Computes it. |
| `build_prompt_ready_bank.py` | Generates the envelope bank from the brief bank. |
| `validators/validate_marketplace_bank.py` | Fourteen gates, fails closed. |
| `validators/test_negative_fixtures.py` | 28 negative controls proving each gate fires. |

**PyYAML is required and is not installed system-wide on this machine.** Create a local virtual
environment with `pyyaml` before running anything above; the Canon handoff already records this.
