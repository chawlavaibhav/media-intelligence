# PART 14 — DECISION TREE

What evidence would imply which architectural direction. Each node names the experiment from Part 16 (or a record action from Part 13), the reading rule, and the branch. Nodes are ordered so that the cheapest, most decisive tests run first and the expensive questions are only asked if the cheap ones leave them open. Everything below is RECOMMENDATION structured around OBSERVED facts already established in Parts 6–12.

```
NODE 0  Is the human judge a usable instrument?                       [E6: 3 judges, blind, 15 artefacts; ~2 h]
        ├─ κ ≥ 0.6 on accept/reject and agreement on defect class
        │      → proceed; the author-judge may be one of the two reviewers in later experiments
        ├─ 0.4 ≤ κ < 0.6
        │      → proceed with two non-author reviewers by unanimity (value-gate rule); the author advises
        └─ κ < 0.4
               → STOP all outcome experiments. Write the rejection checklist WITH the judges first,
                 re-run E6 on the checklist items. No verdict-based claim in this audit is interpretable
                 until this passes.

NODE 1  Was the loop or the knowledge the bottleneck?                 [E4 + E5 + E0; USD ≈ 5 media, ~3 h human]
        E4: fresh-context reviewer with the rejection checklist replays the 3 Cumin versions + 5 case-002 B1 tiles
        E5: gated re-assembly of Cumin V1–V3 from the same accepted components (VO schedule, obstruction, edge trim)
        E0: Cumin brief verbatim → strong model, no repo context, ≥ 5 samples
        ├─ E4 catches ≥ 50 % of what the producer self-passed AND E5 flips ≥ 5/7 HD criteria
        │      → ROLE COLLAPSE + ASSEMBLY dominate (causes 1, 5). Direction: checklist-and-challenge layer
        │        + gates on the mandatory path (Part 15 §2–3). Canon question deferred to NODE 3 at leisure.
        ├─ E4 catches ≥ 50 % but E5 does not flip the structural items (opening, end card, product role)
        │      → expected: structure is not an assembly problem. Same direction; NODE 2 decides the
        │        knowledge source for the structural questions.
        ├─ E4 catches < 50 %
        │      → a non-author with the checklist is NOT enough; either the checklist is wrong (rewrite from
        │        the 42 items with the judges) or the failures need doctrine the checklist lacks → NODE 2 first.
        └─ E0 ≥ 4/5 samples propose product end card + brand from frame 1 unprompted
               → the tutorial failure was the instruction set ("proceed on the brief"), not the prior.
                 Delete WORKFLOW L118-119 first; Canon's structural content is redundant for a strong model
                 on this class → NODE 2's expected result is "b ≈ f".
           E0 ≤ 2/5
               → the prior is brief-dominated; a REQUIRED structural question is necessary regardless of source.

NODE 2  Does the knowledge source matter, and in what form?           [E1 + E3; USD ≈ 43; 9 briefs × 3 reps]
        E1 arms: (a) nothing · (b) oracle compiled doctrine ≤ 2.5 k tokens · (c) same content as raw excerpts ≈ 10 k · (d) all ten packs' sources ≈ 35 k+
        E3 arms: (b) oracle · (f) strong + 40-line checklist · (g) strong + checklist + oracle; checklist built two ways, (m) from human rejections, (n) from Q&A/eval data
        ├─ b > a, c ≈ a, d < b (by unanimity)
        │      → FORM is the lever (F/H): compile the advertising material in CHECKLIST form (binary,
        │        instance-level, id-cited), never as raw excerpts or ten packs. Keep Canon as the source library.
        ├─ b ≈ a
        │      → knowledge is not the bottleneck for these briefs (A false in the "Canon adds value" sense;
        │        L supported). Do not compile more packs; keep Canon as reading; the ≤12-line checklist is
        │        written from the 42 rejection items and the model's own prior.
        ├─ f ≥ b
        │      → L: strong LLM + short checklist matches oracle Canon. Canon becomes provenance for the
        │        checklist lines, not a runtime asset. Canon Prosecutor's charges 3 and 7 stand.
        ├─ g > f by a margin the reviewers agree on
        │      → Canon adds beyond the checklist: compile `commercial_communication` (checklist form) as the
        │        source of the questions; Defender's §3 stands.
        └─ f_m ≠ f_n
               → the checklist SOURCE matters: if f_m > f_n, build from human rejections (N: Q&A stays eval data);
                 if f_n > f_m, the ~15 production-shaped Q&A items earn a place as negative examples (M narrowly).

NODE 3  Does retrieval lose what an oracle finds?                     [E2; USD ≈ 12; only if NODE 2 says knowledge matters]
        e = `runtime.canon.lookup` with all ten packs compiled FOR THE EXPERIMENT ONLY (not merged)
        ├─ e ≈ b → retrieval/compilation is fine; the policy (C-10) was the only block → compile, on a decision.
        └─ e < b → the trigger-table lookup loses value (B in its narrow form) → job-time assembly of the
                    ~2.5 k tokens that matter (by NR fields + objective) replaces the pack lookup; the
                    ontology/bindings stay archived (nothing in E2 uses them).

NODE 4  Does the reasoning model matter?                              [E7; USD ≈ 8; only if NODE 2 found b > a]
        ├─ strong+b ≫ weak+b and strong+a ≈ strong+b
        │      → D over A: model strength dominates; oracle context is decoration for a strong model;
        │        the Lab's reasoning-model half stays closed; EVAL-038's result generalises.
        └─ weak+b ≈ strong+b
               → context carries the model: a cheaper reasoning model + the checklist is viable for
                 first drafts; keep the strong model for the reviewer role (different information).

NODE 5  Is the agency path or the runtime the product?                [record decision, not an experiment]
        Facts: 0 % of `runtime/loop` LOC used by any job; live dispatch does not exist; the per-job
        dispatcher/compositor produced every accepted asset.
        ├─ Agency path is the product
        │      → consolidate the per-job tools ONCE into a shared dispatcher + compositor with the gates
        │        on the path; salvage `acceptance.py` (C-8) and the ledger; freeze `runtime/loop`.
        └─ Runtime is the product
               → it must (1) call the gates, (2) dispatch live, (3) run one real job end-to-end before
                 any other runtime work; until then the agency path continues.

NODE 6  Does the Lab reopen?                                          [only after NODE 4 and one real job]
        ├─ a real job demands a route with no cell AND the human accepted on it (e.g. Gemini TTS)
        │      → roster/pin it from the job; one micro-qualification cell; no battery.
        ├─ NODE 4 says model strength dominates
        │      → a reasoning-model comparison on real briefs, not media routes.
        └─ otherwise → closed. Naturalness/structure/hero are not Lab-measurable today (κ 0.33 vision judge;
                       no audio judge); they are E6/E4 questions.

NODE 7  Learned judgment?                                             [only after E6 labels exist on ≥ 10³ items]
        ├─ a recurring binary judgment (tutorial-vs-ad; voice naturalness) has ≥ 10³ reliable labels
        │      → train a narrow checklist-formatted judge (RocketEval/CheckEval form); validate against
        │        the two human reviewers; deploy as a pre-P1/P3 flag, never as release authority (C-8).
        └─ otherwise → not an option. Do not fine-tune the operator; do not train on the Q&A corpus.
```

## Reading the tree

- **The expected path** on current evidence (Parts 6, 12): NODE 0 passes at 0.4–0.6 (HYPOTHESIS); NODE 1 lands on "role collapse + assembly dominate" with E0 ≤ 2/5 (the Cumin operator is the existing data point); NODE 2 lands on "form is the lever, f ≈ b" (Prosecutor and Defender both predict this); NODE 3 is skipped or confirms the policy block; NODE 5 → agency path. That path is Part 15.
- **The path that would vindicate the current architecture**: NODE 1 E4 < 50 % and NODE 2 g > f by unanimity and NODE 3 e ≈ b. Then the right move is to compile the eight packs in checklist form under a decision and keep the runtime injection. Nothing observed so far predicts this path; it is the honest alternative and E1/E3 are cheap enough to run.
- **The path that would justify deleting Canon**: NODE 2 b ≈ a *and* f ≥ b *and* U9's plate ablation shows no lighting/finish loss. Even then the provenance library stays on disk; what is deleted is the runtime path, the bindings, the ontology and the compile policy.
- **Kill rule** (from the 28-Aug head review, never adopted): if after E4/E5/E1/E3 the checklist-and-challenge layer over the kept tools does not pre-empt ≥ 60 % of the ~25 known rejection reasons on the 9 briefs by unanimity, the remaining hypothesis is that the human's taste is not capturable in this form and the product should be scoped to what deterministic gates can guarantee (statics, variants, exact text) with the human as CD — Baseline A for video.

## What no node can decide

Whether a buyer other than the owner accepts anything: Upwork revenue is USD 0 and no external acceptance exists. Every node above uses the owner's (or two reviewers') acceptance as the outcome. The first paid order is the only test of the commercial promise (Part 13 R15–R17), and the tree does not wait for it.
