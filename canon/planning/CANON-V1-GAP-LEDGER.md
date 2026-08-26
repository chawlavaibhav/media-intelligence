# Canon V1 — gap ledger (C1 output, C4 input)

**Date:** 26 Aug 2026 · **Derived from:** `CANON-V1-LIVE19-COVERAGE.md` / `.yaml`
**Purpose:** the bounded list of things the live 19-source Canon does not cover well enough for the
first product. **C4 may propose a source only against a gap on this list.**

Ordered by what each blocks, not by how interesting it is.

---

## Tier 1 — critical and empty (3)

No accepted source contributes at all. Each sits directly under a stated first-product requirement.

### G1 · Devanagari & Indic typography — domain A14, pack `typography_and_copy`

**What is missing.** How Devanagari is actually built and judged: the headline (shirorekha), matra
placement above and below the line, conjunct formation, vertical stacking, counter shapes, and what
makes a setting correct rather than merely legible.

**Why it matters commercially.** Ten of the thirty first-product briefs are Hindi/Devanagari-primary.
Without this, the Canon cannot state what a *correct* Devanagari creative must achieve, so it cannot
tell Eval what to measure beyond "the characters match". Eval's exactness battery already shows the
expensive failure mode: a generator produces something *subtly* wrong and a checker calls it a match.

**Why the slot is still empty.** CANON-008 stopped at its acquisition gate. The official D'source/IDC
record for Girish Dalvi's *Conceptual Model for Devanagari Typefaces* publishes only a 3-page
abstract (50,197 bytes); the full thesis sits behind IIT Bombay authentication, which was not
attempted. **That is the gate working.** Four Controller options remain open in
`canon/findings/CANON-008-CONTROLLER-BRIEF.md`.

**Blocks:** Canon-side correctness criteria for all Devanagari briefs; any Canon contribution to
Eval's text-and-brand capability family beyond exact-string matching.

### G2 · Short-form / feed-native grammar — domain B11, pack `editing_pacing_and_short_form`

**What is missing.** Hook windows, sound-off viewing, safe zones, vertical framing, the
first-second decision, feed-native pacing.

**Why it matters commercially.** The entire video half of the first product is 6–20 second
feed media. **The newest accepted source is 2013 and the domain postdates all nineteen.** No amount
of further reading in the current library can fix this — it is not a processing backlog.

**Compounding factor.** Every accepted moving-image source writes about film, where one scene often
runs longer than a whole commercial. So this gap is not only *missing* knowledge; it also puts a
scale question over the moving-image knowledge the Canon *does* hold. **Whether film pacing
knowledge transfers to six seconds is untested, and must not be assumed either way.**

**Blocks:** credible planning for all video briefs; hook/opening guidance for feed placement.

### G3 · Indian market & cultural context — domain C13, pack `indian_indic_context`

**What is missing.** Festival codes, colour meaning by context, family and aspiration register,
price framing, language-mixing norms, category conventions for Indian businesses.

**Why it matters commercially.** The first product is *for Indian businesses*. Every accepted source
is Anglo-American. This is the only pack in the entire map with **zero** contributors.

**Honest caveat.** Unlike G1 and G2, this one is probably **not fixable by books at all.** The v0
map reached the same conclusion independently, assigning it to "expert + customer memory +
empirical". C4 should propose a book candidate only if a genuinely suitable one exists, and should
otherwise return `no suitable source found / non-source work needed` rather than manufacturing a
portfolio entry.

**Blocks:** cultural correctness for all 30 briefs; any claim that Canon planning suits an Indian
audience.

---

## Tier 2 — critical, present, but not usable as-is (2)

Knowledge exists. Something specific stops the product from using it. **These may not need a new
source at all** — read the remedy before proposing one.

### G4 · Product / packshot photography — domain A13, pack `product_appearance`

**What exists.** Light Science & Magic's family-of-angles model, which predicts where a reflection
lands on a glossy surface, and Alton's named light functions. Genuinely relevant physical knowledge.

**What is missing.** Two different things, and conflating them would waste a source:

1. **Convention** — hero angle, label legibility, scale cues, surface and finish rendering, and the
   commercial packshot's obligation to show the product as it actually is. Both contributors are
   cinema/studio sources, not product-photography sources. *A source could fix this.*
2. **Translation** — every binding from both sources is a **production candidate**: instructions for
   placing a physical light. Nothing says what to ask for, or what to inspect, in a *generated*
   packshot. SPEC-04 deliberately forbids auto-translating physical-production advice into
   generative instruction, so this cannot be closed by reading harder. **A new source will not fix
   this half.** It is C7/C8 synthesis work.

**Blocks:** product-hero briefs (scenario families 2 and 5); Canon input to Eval's product-appearance
capabilities.

### G5 · Hooks & openings — domain C09, pack `commercial_communication`

**What exists.** Three independent origins with real hook knowledge: Hopkins's blind headline, Heath's
curiosity gaps, Ogilvy's "passing like a ship in the night".

**What is missing.** All of it assumes **a reader who has already stopped on a page.** The feed hook
is a different problem: the first 1–2 seconds, sound-off, thumb-stopping, competing against an
infinite scroll.

**The tempting error, named so it is not made.** The underlying attention principle may well
transfer. **That transfer is untested.** Treating print hook knowledge as feed hook knowledge would
be exactly the kind of silent promotion of inference to fact the Communication Standard forbids.
Overlaps G2 — a single good short-form source could close both.

**Blocks:** the opening of every video brief; the highest-leverage single moment in short-form.

---

## Tier 3 — useful gaps, real but lower priority (4)

| ID | Gap | Domain | State | Note |
|---|---|---|---|---|
| G6 | Motion design & animated type | B12 | absent | One incidental mention on a print-structure object. Relevant to typography-led video and animated offer creatives. |
| G7 | Semiotics of consumer imagery | D02 (thin) | thin | Metaphor/symbolism rests on Ondaatje's hat and Vignelli's semantics. No accepted source treats how consumer imagery signifies. |
| G8 | Accessibility & legibility at thumbnail scale | spans A02/A06/C12 | not a domain row | Not its own domain in the v0 taxonomy, but a real first-product need: small-screen, low-attention legibility. Partially addressed by Miller's grunt test, which was written about websites. |
| G9 | Grouping / gestalt mechanism | A04 | applications without mechanism | The Canon has the practices (Samara's modules, Freeman's backgrounds) but not the perceptual principles behind them. Note that the v0 map's cited source for this, *Picture This*, is **not accepted**. |

---

## Tier 4 — gaps that are NOT source problems (2)

**Recorded so C4 does not propose a source against them.** Buying a book would not close either.

| ID | Gap | Why a source will not fix it |
|---|---|---|
| G10 | **Cross-source synthesis is not done** | D05 trade-off reasoning, E06 principle interaction, E05 context dependence and E04 failure vocabulary all have strong multi-origin raw material and **no synthesis across it**. This is C7 work. Adding sources first would make it *larger*, not better. |
| G11 | **Physical-to-generative translation is not done** | A09, A10, A11, A13 hold real physical-production knowledge bound as production candidates. The missing step is translation, which SPEC-04 requires be deliberate. This is C7/C8 work. |

**These two are the reason the runbook orders the value gate (C5) before source expansion (C6).** If
Canon's problem is unsynthesised knowledge rather than missing knowledge, buying fourteen more books
makes the problem worse. The value gate is what tells the difference.

---

## Summary for C4

| Tier | IDs | C4 may propose sources? |
|---|---|---|
| 1 — critical, empty | G1, G2, G3 | **Yes** — highest priority. G3 may legitimately return "no suitable source". |
| 2 — critical, unusable as-is | G4, G5 | **Partly** — only the convention half of G4; the translation half is synthesis work. |
| 3 — useful | G6, G7, G8, G9 | Yes, within slot caps, only if a strong candidate exists. |
| 4 — not source problems | G10, G11 | **No.** Proposing a source here is a scope error. |
