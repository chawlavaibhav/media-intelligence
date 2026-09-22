# Addendum D — Reconciliation (Controller order step 4)

What the five-stage mechanism actually improves, what remains broken, and which improvements come from independent checking rather than from question generation. Labels: OBSERVED (from the checker output, `03-CHECKER-OUTPUT.md`, or the frozen inputs) · INFERENCE · UNKNOWN. No media was generated; nothing here says anything about media quality.

## 1. Scores, unblinded (OBSERVED)

| Brief | Existing pathway: A (Controller's 4 questions, /8) · B (structure checklist, /12) | Five-stage pathway: A · B |
|---|---|---|
| B1 Cumin (the `86ec183` blueprint) | 4/8 · 5/12 | 7/8 · 12/12 |
| B2 Nivaas (as executed, no prior plan) | 3/8 · 3/12 | 8/8 · 9/12 |
| B3 Upwork intro (CONCEPT-v2) | 6/8 · 3/12 | 7/8 · 8/12 |
| B4 RentOK (Sonnet no-Canon package) | 3/8 · 3/12 | 7/8 · 9/12 |
| B5 Skincare (Sonnet no-Canon package) | 4/8 · 6/12 | 8/8 · 8/12 |
| **Total** | **20/40 · 20/60** | **37/40 · 46/60** |

Blind labels varied by brief (X was the existing plan in B1, B2, B4 and the five-stage plan in B3, B5); the checker scored the five-stage plan higher in all five regardless of label. One checker, one run.

## 2. What the five-stage mechanism improved, by kind (OBSERVED, from the per-line evidence)

**a. Establishing the ask and surfacing what must be confirmed (Controller Q1, Q2).** The existing plans scored A2 = 0 on three of five (Nivaas: no plan existed; RentOK and Skincare: "no open questions to the customer are raised anywhere; proceeds straight to a full locked deliverable") and A1 ≤ 1 on four of five (added a "founders" framing; put a real person on screen against a "no presenter" brief; misspelt the brand; turned "one purchase reason" into three). The five-stage plans scored A1–A2 = 2 on every brief except one (Cumin A4). The checker's evidence is the same each time: the mandatory list matches the brief, additions are flagged for veto, contradictions are flagged and block the stage ("this contradiction blocks the creative stage until the customer answers").

**b. Structural rules that were factually knowable and were not applied (lines 2, 3, 4, 5).** Brand early and throughout: existing 1/5 YES, five-stage 4/5. An ask on card and/or spoken: existing 3/5, five-stage 5/5. Opening mid-action rather than wide or on a logo: existing 3/5, five-stage 4/5. These are Stage-2 facts (the ABCD/Ogilvy rules cited by id in the records), not creative judgement. The RentOK existing package placed the brand at ~11.5 s and closed on a logo animation — the exact shape of Canon's own negative example `qa_abcd_0019`; the Nivaas execution had no brand mark at all.

**c. Order-of-work rules (lines 8, 9, 12).** Voice measured before timings: existing 0/5, five-stage 3/5. Voice cast by ear before pictures: existing 1/5, five-stage 4/5. Riskiest shot named and tested first: existing 1/5, five-stage 5/5. These are Stage-4 decisions; every existing plan fixed timings first and picked the voice last, which is the mechanism behind two of the three real rejections (001 V3 robotic narration; 003 V3 overlap).

**d. Concreteness (Controller Q3).** No difference: A3 = 2 for nine of ten plans. The existing plans were as specific as the new ones (shot lists, second ranges, prompts). **The problem was never vagueness; it was which decisions were specified.** This answers the ChatGPT handoff's §8 hypothesis directly: the existing plans already resolved composition, subject scale, lighting and camera; what they left unresolved was proposition, brand timing, the ask, the close, and the order of production.

## 3. What remains broken in the five-stage pathway (OBSERVED)

**a. The producer forgets reusable questions when they are not templated.** Line 7 (name the frame that sells the product without copy) was answered for Cumin only: 1/5. Line 10 (text off hands/faces/product in every format, formats composed separately): 1/5 — stated for Cumin, omitted for the other four. Line 8 (voice measured first): omitted for RentOK and Skincare. These are exactly the "reusable questions" the Controller's §8 asks for. Written by hand, brief by brief, the producer applied them where the previous rejection made them salient and dropped them elsewhere. INFERENCE: the per-stage question set must be a fixed template that the Stage Controller enforces, not producer memory. This is the strongest single argument in this run for the Controller's "build a question system, not a static questionnaire" — with the qualification that the *reusable* layer must be static.

**b. The producer states facts it has not verified.** The checker found unsupported items in four of five five-stage plans: "cuminco.com" not in the permitted facts (B1); "not Sarvam" as a vendor constraint not in the file (B3); "RentOK app" capitalisation against "RentOk" (B4); a "[brand]" placeholder (B5). Before the checker ran, the producer had also asserted that the RentOK site carried no statistics; a grep of the frozen snapshot proved the opposite and the record was corrected (`01-FIVE-STAGE-RECORDS.md` B4). None of these is large; all of them are the class of error that reaches a customer as a wrong URL, a wrong brand spelling or an invented claim. The Stage-2 rule "every fact carries a source and a verification method" was written into every record and not followed by the producer in four places.

**c. The checker accepts a plan's own risk label.** Line 12 was rephrased after Addendum B to require "names that shot and tests it first". The checker still answered YES for the Cumin existing plan on the strength of the plan's own words "the brief's hardest requirement" (the grip clip), although the shots that failed on the plates were the miss and the notch. A checker with only the plan cannot know which shot is riskiest; that answer needs the capability evidence (case notes: hands, contact, faces under VO) in the checker's input. INFERENCE: line 12 belongs to Stage 4 with evidence attached, not to a plan-only read.

**d. Verification methods were not scored.** The Controller's §3 ("every requirement needs a verification method before production") was written into each five-stage intent contract but the checker format did not ask about it, so nothing here shows whether those methods are adequate. UNKNOWN.

**e. Two structural limits of the comparison.** The Nivaas "existing plan" is the executed sequence, because no plan existed (A2 = 0 is a description, not a finding). The RentOK and Skincare existing plans were EVAL-037 packages produced with no customer to ask, so A2 = 0 partly reflects the experiment's protocol, not the model's judgement; their B-line failures (brand timing, ask, order of work) are not protocol artefacts.

## 4. Which improvements come from independent checking rather than from question generation (Controller step 4)

Separable in this run:

| Effect | Source | Evidence |
|---|---|---|
| Structural and order-of-work decisions present in the plan (lines 2–5, 8–9, 12; A1–A2) | **question generation** (the five-stage producer) | the plans differ on these before any checker sees them |
| Errors caught in the *new* plans (unsupported URL, vendor reference, capitalisation, placeholder) and in the existing plans (RERA claim, "founders" framing, "Sharma PG for Boys" signage, brand misspelling, three reasons instead of one) | **independent checking** | the producer did not catch any of these; the checker caught nine across ten plans with the plan text alone |
| The RentOK statistics correction | **verification against the permitted source** (a grep), not a model | it caught the producer, who was wrong, not the plan |
| Line 7 and line 10 omissions across four new plans | **neither** — a template gap; a fixed per-stage question list would have forced them | see §3a |

INFERENCE: question generation moves the *decisions*; independent checking moves the *errors*; deterministic verification against sources moves the *facts*. All three did work in this run that the others did not, and none substitutes for another. That is the Controller's three-responsibility distinction, observed.

## 5. What this run cannot say (UNKNOWN)

- Whether any of these plans produces better media. Plan quality has fooled this project before (EVAL-037 judged packages). Nothing here touches states 6–7 of the chain.
- Whether the effect survives a producer without hindsight. The five-stage records were written by a session that knew every recorded rejection.
- Whether the effect survives a different checker. One Sonnet run; no second checker; the checker file's form (the new plans written in checklist-adjacent prose) may favour the new plans on B-lines even though A-lines and C-lines are form-neutral.
- Whether the checker's harsh reading of some existing-plan items is fair: "RentOK" vs "RentOk" (the brief itself writes "RentOK"); asking for a spend cap the file listed as a fact (the real job did ask it). Two of the existing plans' A4 deductions are arguable.

## 6. Recommendation to the Controller (RECOMMENDATION)

1. Treat the mechanism as demonstrated at plan level for four things: the intent contract with flagged asks; brand-early / ask / close / opening as Stage-2 facts; voice-first and riskiest-first as Stage-4 order; and a checker that catches producer errors. Treat "concreteness" as not the problem.
2. Before any media: (a) make the reusable Stage-2 and Stage-4 questions a fixed template enforced by the Stage Controller (lines 7, 8, 10, 12 were the ones a hand-written producer dropped); (b) give the checker the capability evidence for line 12; (c) add the verification-method column to the checker format; (d) run a second checker (different family if available) on the same file; (e) re-run with a producer that has no case history in context, on the two EVAL-037 briefs where no rejection history exists.
3. Then the controlled media experiment on one brief (Cumin, cap ≈ USD 10): the `86ec183` plan and the five-stage plan through the same route, judged blind by two non-author reviewers on first-pass acceptance and the known-rejection list, after the judge-reliability packet (Addendum C). Preserve both plans and every post-checker intervention so the three effects stay distinguishable.

Nothing in this addendum authorises spend, changes Controller state, or touches `main`.
