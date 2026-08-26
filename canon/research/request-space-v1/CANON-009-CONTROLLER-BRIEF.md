# CANON-009 — Controller Brief

**Task:** `canon/tasks/CANON-009-CLOUD-SCOPE-PROGRAM.md`, packages C9-A to C9-F
**Date:** 26 Aug 2026 · **Branch:** `work/canon-009-request-space` · **Not merged**
**Spend: ₹0.** No generation, no evaluator call, no acquisition, no ingestion. Live Canon remains 19.

---

## 1. All six packages executed

| Package | Status |
|---|---|
| C9-A request-source landscape | Complete — 13 sources registered, 2 unresolved and recorded as such |
| C9-B media request grammar | Complete — 14 components, evidence-labelled, proposed |
| C9-C pattern / co-occurrence analysis | Complete — 10 patterns, bias stated per population |
| C9-D compare project scope | Complete — measured, four lists, rebalance proposal |
| C9-E Creative IR / Canon implications | Complete — 5 proposals, none an edit |
| C9-F value-gate consequence | Complete — recommendation: **keep** |

## 2. The finding, in one table

| | Best-evidenced in the request space | Coverage in our 30-brief bank |
|---|---|---|
| **Edit a supplied asset** | 82,976 real requests (PSR) + 57K (RealEdit) + 52K (SEED) | **0 briefs** |
| **Animate a supplied image** | 1.70M+ real requests (TIP-I2V) | **0 briefs** |
| **Multi-turn refinement** | 95K sequences, up to 5 rounds (SEED) | **0 briefs** |
| **Variant sets** | Qualitative only | **0 briefs** |
| Exact text in image | **no real-user frequency exists anywhere** | **28 / 30 briefs** |
| Speech / voiceover | **no corpus covers audio at all** | **12 / 30 briefs** |

**The two operations the world most demonstrably asks for, we do not test at all. The two
requirements we test most heavily have the weakest external support.**

This is not a failure of the bank. It was built from the first-product scope before this research
existed, and it does one thing **no public corpus does**: it carries objectives, audiences and
acceptance criteria. But its narrowness was invisible until the space was mapped.

## 3. Evidence classification

### SOURCE-SUPPORTED — quantitative

- **DiffusionDB:** 14M images, 1.8M unique prompts, from the official Stable Diffusion Discord.
- **Prompt analysis of >3M prompts:** top subjects woman **22.26%** of images, man **16.2%**, dress
  6.92%, hair 5.51%, room 5.44%, flower 5.33% — and the authors conclude the dominant use is
  **recreational rather than artistic**.
- **PSR:** **82,976** real editing requests, 305,806 human-edited images, 2013–2025, with a
  three-dimension taxonomy (subject / action verb / creativity level).
- **RealEdit:** 57,000+ examples from r/PhotoshopRequest (261K posts) and r/restoration (20K posts).
- **SEED-Data-Edit:** 52K real-scenario pairs; **95K multi-turn sequences, up to five rounds.**
- **VidProM:** 1.67M unique real text-to-video prompts (Pika Discord), NeurIPS 2024.
- **TIP-I2V:** **1.70M+** real text+image prompt pairs, ICCV 2025.
- **Artificial Analysis Arena:** >45,000 human preferences — but on **benchmark-authored** prompts.

### SOURCE-SUPPORTED — qualitative

- Requests split by **operation** before anything else; the three operations have separate corpora,
  model families and user populations.
- An I2V prompt instructs **motion on a supplied image**, not a scene description.
- Users name specific motions — "zoom", "walk", "blink" — which are three different production
  problems.
- Editing datasets converge on one operation vocabulary: add / remove / replace / alter / background
  change / style / action change / extraction.
- Peer-reviewed advertising research places **validation** as a named stage between generation and
  execution.

### INFERRED

- Product + person + brand reference is central to our product — **each part attested, the
  combination not measured.**
- Multi-shot identity continuity matters — preservation is attested for *editing*, not for generated
  sequences.
- Our bank is a **narrow probe of a wide space** — inference from the measured comparison.

### PROPOSED

- The 14-component Media Request Grammar v1.
- Five Creative IR proposals: **requested-operation field** (G-IR-01), output cardinality (G-IR-02),
  multi-turn representation (G-IR-03, flagged not solved), camera-motion separation (G-IR-04), and
  **change nothing** on style vocabulary (G-IR-05).
- Extend the bank to 40 rather than rebalance the 30.
- Keep the value-gate bank unchanged.

### UNKNOWN — seven, four under first-product requirements

| Question | Why it matters |
|---|---|
| How often do real users request **text in an image**? | 28/30 of our briefs demand exact strings |
| How often is the subject a **product** rather than a person? | Our whole product is commercial product media |
| What **duration / shot count** do users request? | 18 of our briefs specify durations |
| Anything about **speech or voiceover** demand | 12 of our briefs carry exact scripts |
| Any **India / Hinglish / Devanagari** request corpus | 20 of our briefs are Hindi or Hinglish |
| Arena-T2I-Hard's construction | Named in the runbook; could not be characterised |
| Artificial Analysis prompt-set selection | Publisher claims broad coverage; no taxonomy visible |

Listed rather than estimated. An estimate here becomes a number someone plans against later.

## 4. What the Controller must decide

### Decision 1 — the requested-operation field (**highest consequence**)

Creative IR has **no field recording what operation the customer asked for.**

Without it, *"make this photo's background white"* (customer instruction, `preserve`) and *"a product
on white, and we have a reference photo"* (Planner decision, `decide`) render as similar Creative IR.
The six-operation annotation cannot separate them, and the project loses the ability to distinguish a
parser error from a judgement error — which is the entire reason Normalized Request and Creative IR
are kept side by side.

**Proposal:** `requested_operation` on the **Normalized Request** — it is something the customer said.
Values from converging evidence: generate / edit / animate / extend / compose / variant / restore.
**How** to achieve it stays a Production IR concern.

**This is an architecture decision and is flagged, not made.**

### Decision 2 — extend the bank to 40, or relabel only

- **Option A (₹0):** relabel which components are evidence-backed vs scope-derived. **Should happen
  regardless** — it stops an over-claim propagating into Eval's benchmark design.
- **Option B (recommended):** keep all 30, add 10 covering edit / animate / variant / multi-turn.
  Extension rather than rebalancing, because the 30 are the frozen input to the value-gate package
  and swapping briefs invalidates the early-12 selection, the oracle contexts and the length matching.
- **Timing that matters:** Eval must sample its twelve end-to-end production briefs from this bank.
  If it samples before extension, its capability map inherits a blind spot covering the two
  best-evidenced operations in the request space.

### Decision 3 — output cardinality

The product optimises **Cost per Accepted Outcome**. A request yielding twelve variants where three
must be accepted has completely different economics from one yielding a single asset. **We cannot
currently express the difference, so we cannot price it.**

### Decision 4 — multi-turn (flag only)

Real requests arrive in rounds — 95K sequences of up to five. Round three inherits everything unstated
from rounds one and two. Modelling each round as an independent Normalized Request loses the
inheritance; modelling it as a mutation breaks "never overwritten".

**No mechanism is proposed.** The charter's stop condition is explicit: a request appearing to need an
IR field that does not exist is an ARCHITECTURE matter, not something a worker adds.

## 5. Cross-stream notes

**To Eval —** the twelve end-to-end briefs must come from Canon's bank (per the shared plan). Two
things to weigh: the bank currently has **zero edit and zero animate** briefs, and the register's
benchmark sources (Arena, text-rendering benchmarks, instruction-editing benchmarks) are **model
comparison surfaces, not demand evidence** — useful to Eval as methodology, not as scope.

**To Resources —** the strongest real-request corpora are public and rights-visible in at least one
case (DiffusionDB is CC0 1.0). Rights for the others were **not verified** and no acquisition is
proposed here.

**To Canon (later) —** two knowledge gaps surfaced that the C1 ledger did not have: **editing and
preservation craft**, and **motion on a static image**. C1 derived gaps from product scope; CANON-009
derived them from observed requests, and the second direction found holes the first missed. **No
acquisition proposed** — the standing finding holds that the Canon has 49 multi-origin domains and no
synthesis across any of them.

## 6. Method limitations — read before acting on any number

**Web fetching was blocked throughout.** Search worked; opening a page did not. Every fetch returned
`EGRESS_BLOCKED` and direct `curl` returned nothing from any host.

So every figure here is **`search_verified`**: drawn from search results that surfaced first-party
pages — arXiv listings, project sites, dataset cards — with **no primary page opened in this session.**
Figures were consistent across independent result sets. That is worth something. It is not the same as
having read the paper.

**Treat these numbers as good enough to plan with and not good enough to spend on.**

Three further limitations:

- **Three editing sources are one population.** PSR, RealEdit and SEED part 2 all draw on
  r/PhotoshopRequest. They are **not** three independent corroborations — the same lineage trap the
  Canon already knows from companion volumes and shared informants.
- **No percentage was pooled across corpora.** Different populations, no global prevalence figure,
  deliberately.
- **Search returned unattributed statistics** for commercial adoption (a "34% / 25% / 25%" split with
  no traceable source). **None was recorded as fact**, and the register says so explicitly so a later
  reader does not assume they were missed.

## 7. Not done

- **No source ingested, no acquisition, no purchase, no login, no gated access.** Live Canon: **19**.
- **No spec edited.** SPEC-01 and the Audit Gate untouched. All five IR items are proposals.
- **No brief edited.** `briefs-source.yaml` is byte-identical.
- **No value gate run.** No Canon-naive controls authored. No planning output generated.
- **No model or provider selected. No Production IR. No routing.**
- **No paid or free generation / evaluator API call.**
- **No other stream's files touched.** Everything new sits under `canon/research/request-space-v1/`.
- **No large dataset payload downloaded** — papers, dataset cards and project pages sufficed.
- **No merge to `main`.**

---

### The one thing worth deciding first

**The requested-operation field.** Everything else on this list can wait for the value gate; this one
cannot, because Eval is about to build a capability map from this bank. If it does that while
Creative IR still cannot say whether a customer asked us to *make* something or to *change* something,
the blind spot gets baked into the measurement architecture — and the two best-evidenced operations in
the entire request space go unmeasured.
