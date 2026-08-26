# CANON-009 — Creative IR and Canon implications (C9-E, C9-F)

**Task:** CANON-009 / C9-E and C9-F · **Date:** 26 Aug 2026
**Everything here is a PROPOSAL. No frozen spec was edited. No source was ingested.**

---

## Part 1 — where Creative IR cannot cleanly represent observed requests

The test applied throughout: **can the observed request be recorded without confusing what the
customer asked for with what the Planner decided?** That separation is the spine of the architecture
— Normalized Request and Creative IR are kept side by side precisely so "did the parser misread the
user, or did creative reasoning decide badly?" stays answerable.

Where a component has no home, it will end up smuggled into a field that means something else. That
is the failure mode each gap below describes.

### G-IR-01 · No requested-operation field — **the significant one**

**Observed:** requests split by operation before anything else. Generate from nothing (DiffusionDB,
VidProM), edit a supplied asset (82,976 real PSR requests), animate a supplied asset (1.70M+ TIP-I2V
requests). TIP-I2V states the structural difference explicitly — its prompts instruct motion on the
supplied image rather than describing a scene.

**Creative IR today:** describes *what should exist*. It has `assets[]` with roles, and
`entities[].invariants`, but **no field saying what operation the customer requested.**

**Why the existing fields do not cover it.** One could argue an edit request is expressible as
"a Creative IR whose entities have an identity_reference and tight invariants". That is exactly the
smuggling this architecture exists to prevent:

- *"Make this photo's background a studio white"* is a **customer instruction**. Operation: edit.
- *"A product on studio white, and we happen to have a reference photo"* is a **Planner decision** to
  use img2img.

Both would render as similar Creative IR. **The first is `preserve`; the second is `decide`.** With no
operation field, the six-operation annotation cannot distinguish them, and the project loses the
ability to tell a parser error from a judgement error — the one thing the two-object split is for.

**Proposal (not an edit):** a `requested_operation` field on the **Normalized Request**, not on
Creative IR. It is something the customer said, so it belongs in the object that is preserved
forever. Candidate values, from converging evidence: `generate`, `edit`, `animate`, `extend`,
`compose`, `variant`, `restore`.

**Why Normalized Request rather than Creative IR:** the operation is a fact about the ask. How to
*achieve* it — img2img, inpaint, generate-and-composite — is a Production IR decision that will
change as models change. Putting it in Creative IR would repeat the `render_method` mistake SPEC-01
already refused to make.

**Consequence if not resolved:** Eval's capability map will be built assuming generation from
nothing, and the largest attested operation in the request space stays untested.

### G-IR-02 · No output cardinality — one Creative IR describes one artefact

**Observed:** "creative versioning" — many variants of one creative across markets, formats and
placements — recurs as a named commercial activity in practitioner reports. *(Qualitative only; no
frequency established.)*

**Creative IR today:** `delivery` carries `aspect_ratios[]`, which is the closest thing — but that
is one artefact delivered several ways, not several artefacts.

**Why it matters more here than elsewhere:** the product's primary metric is **Cost per Accepted
Outcome**. A request yielding twelve variants where three must be accepted has completely different
economics from one yielding a single asset. We cannot currently express the difference, so we cannot
price it.

**Proposal:** an `output_set` concept — cardinality, the axis of variation (market / placement /
format / message), and whether acceptance is per-variant or for the set. Placement between Normalized
Request and Creative IR is a genuine architecture question and is **flagged, not decided**.

### G-IR-03 · No representation of a request that arrives in rounds

**Observed:** SEED-Data-Edit part 3 — **95K multi-turn editing sequences, up to five rounds.**

**Creative IR today:** a single complete statement. Normalized Request is "preserved forever", which
handles *history* but not *a request still being formed*.

**The subtle part:** round three of a conversation is not a new request. It inherits everything
unstated from rounds one and two. Modelling each round as an independent Normalized Request would
lose the inheritance; modelling it as a mutation would break the "never overwritten" rule.

**Proposal:** treat this as an open architecture question and **do not invent a mechanism now**. The
mandatory stop conditions in the Canon charter are explicit — a source appearing to require an IR
field that does not exist is an ARCHITECTURE matter, not something a worker adds. **Flagged for the
Controller.**

### G-IR-04 · Camera motion is not separable from subject motion

**Observed:** TIP-I2V annotates action and camera motion as **separate dimensions**, and users request
"zoom" (camera), "walk" (subject locomotion) and "blink" (micro-expression) — three different
production problems and three different failure modes.

**Creative IR today:** `VideoCreativeExtension` has `temporal_structure`, `temporal_hierarchy`,
`dialogue_intent`, `continuity_requirements`. Camera motion has no explicit home; it would land in
`visual_language` or in a beat's free-text `purpose`.

**Proposal:** a minor, additive extension separating camera motion from subject action within the
video extension. **Lowest-risk proposal in this document** — additive, no existing field changes
meaning.

### G-IR-05 · Style vocabulary — a gap SPEC-01 correctly refuses to fill

**Observed:** style and quality modifiers dominate prompt text ("cinematic", "highly detailed",
"8k"), and **decay** — "trending on artstation" was top-prominent in 2022 and out of the top 10 by
2023.

**Creative IR today:** has `visual_language` for genuine creative direction and deliberately excludes
`render_method`.

**This is not a gap. It is external evidence that an existing decision was right.** A Creative IR that
had absorbed 2022's prompt folklore would now be carrying dead weight. **Recommendation: change
nothing, and record the corroboration** — a durable specification correctly refused a component that
proved to have a shelf life of about a year.

### Where Creative IR is ahead of the evidence

Worth stating, because it is the opposite of a gap:

- **`assets[].role`** distinguishes identity / style / composition / brand / campaign / character /
  location / inspiration references. **No corpus found makes this distinction at all.**
- **`entities[].invariants` and `allowed_variation`** specify *which dimensions constitute identity*.
  Every editing corpus treats preservation as monolithic.
- **The six operations** (preserve / derive / decide / delegate / ask / flag) are a per-field record
  of how much latitude the customer granted. PSR's *creativity level* — over 82,976 real requests —
  is a coarse, one-dimensional version of the same idea, arrived at independently. **That is genuine
  convergent corroboration of the spec's design.**

## Part 2 — Canon knowledge implications

Read against `canon/planning/CANON-V1-LIVE19-COVERAGE.md` (live 19 sources, 17 independent origins).

### High-recurrence areas where Canon knowledge is thin

| Request area | Evidence | Canon coverage today |
|---|---|---|
| **Editing and preservation craft** | Strongest in the register | **Effectively absent.** The 19 sources teach how to *make* things, not how to *modify* an existing image while keeping it credible. No accepted source addresses this. |
| **Motion on a static image** | 1.70M+ real requests | **Absent as such.** Canon holds film-scale continuity and editing knowledge; nothing about animating a still. |
| **Short-form / feed-native** | Structural — a whole modality of brief | Already a known critical hole (gap G2 in the C1 ledger). **CANON-009 independently confirms it from the demand side.** |
| **Human subject realism** | Best-attested subject finding | Partially covered — lighting, framing, continuity — but nothing about whether a *generated* person reads as plausible. |
| **Variant and campaign-set craft** | Qualitative | **Absent.** Nothing on maintaining coherence across a family of creatives. |

**Two of these are new.** Editing craft and animate-a-still were not in the C1 gap ledger at all,
because that ledger was derived from *product scope*, and CANON-009 derived these from *observed
requests*. Coming at the corpus from a second direction found holes the first direction missed —
which is the strongest argument that this research was worth doing.

**No acquisition is proposed and no source is named.** The task forbids starting acquisition, and the
standing C1/C4 finding still holds: the Canon has 49 multi-origin domains and **no synthesis across
any of them**. Adding sources against a newly-found gap before the value gate runs would repeat the
error the gate exists to prevent.

## Part 3 — value-gate consequence (C9-F)

**Question: is the existing value-gate bank still a defensible test surface?**

**Answer: yes, for the question it asks — with one boundary that must now be stated.**

The gate asks whether explicit Canon improves *planning* over a generic craft control, on twelve
briefs. Nothing in CANON-009 undermines that. The twelve briefs are real commercial intents with
objectives, contradictions and exact requirements; Canon either helps a planner handle them or it
does not.

**The boundary CANON-009 adds:** the gate tests Canon's value on **generate-from-nothing commercial
briefs only**. It says nothing about Canon's value on editing requests, animation requests, variant
sets or multi-turn refinement — because the bank contains none of those. A `continue` verdict would
license Canon expansion **for the generation slice of the request space**, not across it.

That is a scoping statement, not a defect. But without it, a `continue` would quietly be read as
broader than it is.

### Recommendation: keep / rebalance / replace

**KEEP. Do not rebalance, do not replace, do not re-select the twelve.**

Three reasons:

1. **The gate's question is unchanged.** CANON-009 changes what we know about the *request space*,
   not about whether explicit Canon improves planning.
2. **Re-selecting would cost real work for no gain.** The early-12 selection, the twelve rendered
   oracle contexts and the ±15% length matching are all frozen against these briefs. Changing the
   set invalidates all three — and the selection was deliberately made *before* any generation, so
   changing it now, after new information, is precisely the experiment mutation the protocol forbids.
3. **The blocker is elsewhere.** The gate is already blocked on `FRESH_CONTROL_SESSION_REQUIRED` —
   independent generic controls. Nothing in CANON-009 changes that, and nothing here should be
   allowed to look like a second reason to delay.

### What to add instead — after the gate, not before

If Option B of the coverage audit is approved and the bank extends to 40, **a second gate wave** on
the edit / animate / variant briefs would test Canon's value on the operations it has never faced.
That is a **later task**, gated on the first gate's verdict.

**Explicitly not done here, per the task:** the value gate was not run, no Canon-naive controls were
authored, and no output was generated.
