# Controller — Programme Reset After Media Factory Evidence Recovery — 2026-08-29

## Status
**APPROVED PROGRAMME RESET.**

This decision supersedes the strategic direction in
`coordination/plans/2026-08-28-PROGRAMME-PLAN-T2-T8-v1.md` for T2 onward.

It does **not** reopen PILOT-001, authorise paid work, populate the Capability Registry, create
Production IR, or authorise a Planner.

The USD 25 T2 workflow/model screen remains declined and must not be revived under another name.

## Why this reset exists

The programme incorrectly behaved as if:

> zero Registry-qualified workflows = zero empirical workflow knowledge.

That was false.

A user-provided recovery package from the earlier `chawlavaibhav/media-factory` project contains
206 recoverable historical artifacts/tests, including 67 human-scored rows and the July 2026
consistency/routing experiments. The Controller inspected the manifest, routing prior,
prompt-enrichment evidence, cost reconstruction, representative stills/contact sheets and
representative video frame strips.

The package is **external historical evidence pending a bounded import into this repository**.
Until that import is completed and provenance/hashes are recorded under Eval ownership, it does not
become a Capability Registry source.

The earlier project itself is independently visible in GitHub and confirms the architectural
mechanism: provider abstraction, reference-conditioned image/video adapters, image-first recipes,
a natural-language LLM intake/creative-director layer, and deterministic composition.

## Corrected historical findings

These are the conclusions the reset must preserve. Strength refers to the recovered evidence tier,
not current August-2026 capability.

### Strong historical priors

1. **Reference-conditioned character still generation was commercially usable in the tested
   conditions.** The recovered scored set contains 64 stills:
   - Seedream 4.5 edit: 29/32 pass (90.6%);
   - Nano Banana Pro edit: 25/32 pass (78.1%).
   These are July-2026 historical observations, not current-model certification.

2. **The two image routes failed differently.**
   - Nano failures clustered around identity/object drift and logo/craft defects.
   - Seedream failures clustered around text/layout defects.
   Therefore routing/evaluation should be condition-specific, not a single generic model score.

3. **Image-first -> minimal image-to-video is a proven historical production pattern.**
   Media Factory recipes explicitly generate/select the hero still first and animate it with a
   small motion instruction rather than asking the video model to invent the entire creative.

4. **Lip-sync workflow choice mattered.**
   The recovered record contains a rejected SadTalker route and an accepted/directionally useful
   LatentSync-class route under the July conditions.

5. **Provider policy asymmetry mattered.**
   Veo refused a stylised emotional scene that Wan executed. Policy/pre-flight is therefore a
   production requirement, not an edge case.

### Corrected over-broad memories

6. **"Models cannot render text" is false as a blanket rule.**
   In the scored still set, exact in-scene English headlines succeeded repeatedly. The historical
   weakness was more specific: exact text that must remain stable through motion was fragile.
   Deterministic composition guarantees exactness but can reduce aesthetic integration if used as
   a banner-like universal solution.

7. **"Two-person dialogue had no route" is too broad.**
   The failure concerned multi-turn/chained dialogue. A short single-beat dialogue was judged a
   candidate recipe. Historical limits remain a freshness-flagged prior, not a current refusal rule.

8. **No automated intelligent router existed.**
   Media Factory had provider capability descriptors, configurable endpoints and a human-learned
   routing policy. There is no router algorithm to port. The new project still has to turn these
   learned policies into runtime intelligence.

### Prompt enrichment — crucial unresolved question

9. **The prompt-enrichment mechanism definitely existed.**
   Media Factory production code used an LLM "creative director" before media generation:
   customer conversation -> structured/product-visible brief -> category craft defaults -> recipe
   prompt -> image/video model.

10. **The production LLM path preferred OpenAI, not Claude.**
    `packages/whatsapp/src/llm.ts` selects OpenAI when `OPENAI_API_KEY` exists and otherwise
    Anthropic; default OpenAI model in that code is `gpt-4o-mini`. Claude Code also authored many
    spike prompts interactively, but this is different from the production runtime chain.

11. **The causal claim "LLM enrichment beats raw prompting" is NOT recovered as a controlled A/B.**
    No same-input/same-model raw-vs-enriched pair and no runtime enrichment log survives.
    Directional prompt-iteration evidence exists, including a counterexample where excessive
    choreography made the result worse.

This unresolved question is now a first-class programme question rather than an assumption.

## Architectural correction

### Historical empirical priors are legitimate evidence, but not Registry qualification

Create and use this distinction:

- **Historical empirical prior:** an observed result from an earlier real production/experiment
  with known date/conditions/provenance. It informs where to start and what not to rediscover.
- **Current qualified capability:** evidence that has passed the current Capability Lab admission
  process and may populate the Registry.

A historical prior may guide a targeted freshness check.
It may **not** create a Registry row by itself.

The practical meaning of "Registry = 0" is therefore:

> zero current rows admitted under the new qualification contract,

not:

> the project knows nothing about media workflows.

### No universal generate-vs-deterministic dogma

Production planning must choose the lowest-entropy method justified by the requirement.

- Hard exact contractual copy / price / legal claim / exact logo:
  deterministic by default unless a future strict-qualified route proves a better safe method.
- Non-critical decorative/in-scene text in a still:
  model generation is allowed when the job can tolerate inspection/rejection.
- Exact text that must remain stable through motion:
  deterministic/tracked composition remains the historical prior until a targeted freshness check
  shows a current generator can satisfy the requirement reliably.
- Deterministic composition is a tool, not an aesthetic default. It must not automatically become
  a flat banner that makes the asset look amateur.

This supersedes any blanket project shorthand saying a generative model is *never* used for text.

Exactness remains requirement-specific.

## What is no longer an open research question from zero

Do NOT launch broad experiments merely to rediscover:

- whether reference-conditioned image workflows can ever work;
- whether image-first -> I2V can ever work;
- whether models have different failure profiles;
- whether provider price/policy matters;
- whether deterministic composition can guarantee exact text;
- whether separate voice/lip-sync routes can be viable;
- whether routing should be conditional on job requirements and cost.

These may need **targeted freshness checks when a current production decision depends on them**.
They do not need blank-slate qualification batteries first.

## What actually remains unanswered

The highest-value unanswered intellectual questions are now:

1. Does a strong reasoning LLM materially improve a production specification over an un-enriched
   brief for the same downstream workflow?
2. Does giving the **same reasoning model** relevant Canon knowledge improve its production
   decisions beyond its latent knowledge alone?
3. Does Canon reduce important decision variance across repeated runs without making the plan
   rigid or worse?
4. Does any reasoning improvement propagate into better human-accepted media when the downstream
   production workflow is held constant?
5. If Canon adds value, can a cheaper reasoning model + Canon match a more expensive frontier
   reasoning model closely enough to lower CpAO?
6. Which historical routing priors have gone stale enough to require current re-measurement?

## New programme — T2 onward

T0 demand/population work and T1's failed vertical slice remain historical completed work.

### T2 — Recover priors + isolate reasoning/Canon

**T2A — zero-spend historical-prior import**

Import the Media Factory evidence into Eval as a provenance-preserving **historical prior** set.

Requirements:
- preserve evidence tiers;
- preserve dates/model versions/conditions;
- preserve contradictions and unknowns;
- preserve artifact hashes and original paths;
- do not copy 800 MB blindly;
- do not infer missing prompts/scores;
- do not create Registry rows;
- clearly mark every route observation freshness-required.

This task should also record the 206-row recovered manifest and compact representative evidence
references sufficient for audit.

**T2B — reasoning-only controlled experiment**

Before more media generation, freeze a small experiment on real briefs comparing:

- **B — strong reasoning model, no Canon retrieval**
- **C — the same exact reasoning model + relevant Canon retrieval**

The media-generation model is not involved in this first experiment.

Use multiple independent repeats per brief to test:
- requirement coverage;
- production feasibility;
- contradiction rate;
- stability of production-critical decisions;
- whether important creative decisions are sharper/more specific;
- blind human preference/fitness for the brief.

Do not judge Canon using only a Canon-authored checklist; that would be circular.
Brief-grounded hard requirements and blind human review are required.

A raw-direct-prompt arm may be retained only as a cheap contextual reference if useful. The core
business comparison is **same LLM without Canon vs same LLM with Canon**.

No paid API execution is authorised by this decision.

### T3 — Does Canon improvement propagate into media?

Only if T2B shows a credible reasoning-level advantage.

Use a historically proven production shape rather than inventing another workflow:

brief
-> reasoning specification
-> hero still / reference-conditioned still
-> still acceptance gate
-> minimal I2V motion where video is required
-> requirement-specific deterministic composition
-> human acceptance.

Hold the downstream models/workflow constant between B and C.

Start with the smallest set that can falsify the thesis; do not begin with 48 outputs.

Primary question:
**does LLM + Canon increase first-pass human acceptance or reduce repair relative to the same LLM
alone when production execution is held constant?**

### T4 — Cost compression / keep-kill

Only if Canon adds value in T2/T3.

Compare:
- frontier reasoning model + Canon;
- cheaper reasoning model + the same Canon.

Test whether explicit knowledge lets the cheaper model preserve the production decisions that
matter.

Also decide which Canon components earned their keep. Remove components that add cost/context but
no outcome lift.

### T5 — Targeted current Capability Lab

Refresh only those historical priors that the winning T3/T4 workflow actually needs.

Example:
if the winning route needs current image-to-video with one speaking character, freshness-test that
condition; do not benchmark unrelated models/capabilities.

Registry admission bar stays unchanged.
Historical prior != Registry row.

### T6 — Runtime v0

Automate the winning architecture and the production rules actually supported by evidence.

Production IR should be extracted from the successful recipes/decisions at this point, not designed
in the abstract beforehand.

### T7 — untouched holdout

Freeze the development/holdout policy first.
Run the resulting runtime against untouched real buyer-shaped cases and the strongest simpler
baseline.

### T8 — ship / simplify / research / stop

Decide on accepted-outcome rate, CpAO, repeatability, and whether Canon/production intelligence
earns enough value over the simpler baseline.

## Immediate Controller queue

1. Zero-spend Media Factory historical-prior import under Eval ownership.
2. After that import, design/freeze T2B — the small reasoning-only **same LLM vs same LLM + Canon**
   experiment.
3. Ask for user spend approval only after the T2B protocol names the exact model, call count and
   maximum cost.
4. Do not generate any new media before T2B unless the user explicitly changes direction.

## Spend

**No paid tranche is active or authorised.**

PILOT-001 remains closed.
Its residual authority remains lapsed.
The declined USD 25 screen remains declined.
