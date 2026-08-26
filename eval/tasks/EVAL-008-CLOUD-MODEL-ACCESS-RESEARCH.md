# EVAL-008 — Cloud Model Selection & Sourcing Research

**AUTONOMY MODE:** autonomous  
**Environment:** Claude Web/cloud only  
**Branch:** `work/eval-008-model-access`  
**Budget:** ₹0  
**Relationship to EVAL-007:** parallel and independent. EVAL-007 studies capability/evaluator/workflow semantics. EVAL-008 selects the serious model universe first, then maps how to source those models. Neither authorizes paid benchmark execution.

## Controller principle — model list first, sourcing second

**The model list must be independent of current sourcing convenience, credits or account access.**

The work order is mandatory:

1. **Decide which models we should test and why.**
2. For every selected model, check whether it is available through **Frontier Clouds**.
3. If not, check **fal**.
4. If not, identify the best legitimate source: direct vendor API or another production-grade provider.
5. Only after the model roster is complete, produce the account/access actions needed to obtain uncovered models.

Do not omit a strategically important model because it is unavailable on Frontier Clouds or fal. Do not add a weak/redundant model merely because credits make it cheap to access.

## User sourcing preference

The user's preferred sourcing order is:

`Frontier Clouds (existing credits) -> fal (existing access) -> new/direct accounts only when required`

This ordering is a **route preference**, not a model-selection criterion.

The user has explicitly reported:

- access/credits on **Frontier Clouds**;
- access to **fal**.

The exact public identity/URL of the service named `Frontier Clouds` has not been established in repository evidence. Preserve the user's literal service name. Do not substitute another provider because its name sounds similar. If public research cannot unambiguously identify the platform, finish the independent model roster and mark Frontier Clouds route verification as needing the exact service URL/catalog later.

Do not inspect or assume laptop credentials/API keys.

## Objective

Produce an evidence-backed answer to two sequential questions:

### Question A — what should we test?

Build a compact but strategically complete roster of current image/video and supporting media-generation models that are worth empirical testing for the product.

A model belongs because it represents one or more materially distinct hypotheses, for example:

- frontier overall quality;
- strong commercial-image composition;
- exact text/typography;
- image editing/instruction following;
- person/product/reference consistency;
- controllability;
- T2V quality;
- I2V/reference-conditioned video;
- multi-shot/state continuity;
- video editing/extension;
- native audio/dialogue;
- low-cost/high-throughput production;
- open/self-hostable economics;
- specialist workflow such as lip-sync/voice where it could materially reduce CpAO.

Selection must be based on current model capability/relevance evidence, not provider availability.

### Question B — how do we source each selected model?

Only after Question A is frozen inside the task output, map each selected model through the sourcing ladder:

`Frontier Clouds -> fal -> direct/other legitimate API`

For each route, distinguish the underlying model from the provider wrapper. If the same model is exposed through multiple routes, note differences in version, controls, price, limits and reproducibility, but do not count route duplicates as different model candidates unless the route itself materially changes the workflow.

## Research evidence rules

### For deciding what models deserve testing

Use a triangulation of current evidence:

- official model/vendor documentation and release information;
- high-quality current independent benchmark/arena results where comparable;
- credible current evaluations/reviews that expose methodology;
- evidence of materially distinct controls/workflow capabilities;
- relevance to the product's commercial image/video production problem.

Do not select from leaderboard rank alone. A model may deserve a slot because it uniquely covers a production method even if it is not #1 overall.

### For sourcing/access claims

Use provider documentation/catalogs for what each provider actually exposes. Use official vendor docs for underlying model identity and native capabilities where possible.

- Frontier Clouds availability must be verified from Frontier Clouds itself once the exact service/catalog is identifiable.
- fal is authoritative for the endpoints fal exposes and their route-specific controls/pricing.
- direct vendor documentation is authoritative for direct access.

Do not infer availability from blog posts or model-name similarity.

No paid calls. No account creation. No terms acceptance.

## Work packages — execute in this order

### E8-A — Independent model universe

Research the current serious model families across these production lanes:

1. image — text-to-image/commercial creative;
2. image — editing/inpainting/outpainting/instruction edits;
3. image — reference/person/product/identity conditioning;
4. image — text/typography/design/vector where materially distinct;
5. video — text-to-video;
6. video — image/reference-to-video;
7. video — video-to-video/edit/extend/first-last-frame/keyframe/multi-shot controls;
8. video — native audio/dialogue where available;
9. supporting media — TTS/voice/lip-sync/avatar only where it is plausibly part of our production route.

Build the universe **without considering which provider we already use**.

For every candidate record:

- vendor/model family;
- exact current version/model id where established;
- lane(s);
- distinctive production capabilities;
- evidence for why it is currently serious;
- hypothesis it would test in our Capability Lab;
- likely redundancy with another candidate;
- status: `must_test | should_test | reserve | exclude`;
- exclusion/reserve reason.

### E8-B — Roster selection

Produce `MODEL-ROSTER-FIRST.md` before doing sourcing analysis.

Use three priority levels:

- **Must test:** excluding it would leave a meaningful frontier or production-method blind spot.
- **Should test:** useful differentiated challenger, specialist or cost frontier.
- **Reserve:** relevant, but largely redundant or lower priority for first paid admission.

For every Must/Should model answer in plain English:

> What different thing will we learn by testing this model?

If two models answer effectively the same hypothesis, justify keeping both or move one to reserve.

Do not impose an arbitrary model count. Compactness comes from eliminating redundancy, not from a fixed quota.

### E8-C — Frontier Clouds sourcing pass

Now take the already-selected Must/Should roster and check **Frontier Clouds first**.

For each model record:

- available: yes / no / not verified;
- exact model/version exposed;
- operations/endpoints exposed;
- route-specific limits/controls;
- pricing where public/current;
- whether this appears to be the same underlying version selected in E8-B;
- evidence source/date.

If the exact Frontier Clouds service cannot be unambiguously identified from public evidence, do not guess. Produce the complete roster anyway and create a compact `FRONTIER-CLOUDS-VERIFY.md` containing the model names that need checking once the exact catalog/URL is available.

### E8-D — fal fallback pass

For every selected model not verified on Frontier Clouds, check fal.

Record the same fields and explicitly distinguish:

- exact selected model available;
- same family but different version;
- materially different wrapper/workflow;
- unavailable.

Do not replace a selected model with a fal alternative merely because the selected model is absent.

### E8-E — Direct/other sourcing pass

Only for selected models still uncovered after Frontier Clouds and fal, identify the best legitimate production source.

Preference within this final step:

1. official/direct vendor API;
2. established production API/provider if direct is unavailable;
3. other legitimate access only when provenance/version is sufficiently clear for empirical evidence.

Record:

- exact source/provider;
- signup/API access route;
- model/version availability;
- any access/business/geographic constraints stated publicly;
- pricing/minimum commitment if public;
- why a new account is actually necessary.

### E8-F — Source-optimized execution map

Create a final matrix where rows remain **models**, not providers:

`selected model -> preferred source -> fallback source -> last-resort source -> account action`

Apply the user's route preference mechanically:

- if equivalent selected version is on Frontier Clouds, prefer Frontier Clouds;
- otherwise, if equivalent selected version is on fal, prefer fal;
- otherwise source the selected model elsewhere.

If provider wrappers materially alter capabilities/versioning, flag them for later route-equivalence testing rather than silently treating them as identical.

### E8-G — User action checklist

Create `ACCOUNT-ACTIONS.md` only after all sourcing passes.

Three buckets:

1. **No action — Frontier Clouds**: selected models covered by existing preferred credits.
2. **No/new-minimal action — fal**: selected models not covered on Frontier Clouds but covered by existing fal access.
3. **New access required**: selected models unavailable through both, with the exact account/API route needed.

For new access state what to create, why that model is worth the extra account, and whether payment can wait until benchmark authorization.

Do not recommend prepaid credits yet.

## Deliverables

Create under `eval/model-access/2026-08-26/`:

1. `MODEL-UNIVERSE.md`
2. `MODEL-ROSTER-FIRST.md` — **must be logically independent of sourcing findings**
3. `model-selection-evidence.yaml` or `.jsonl`
4. `FRONTIER-CLOUDS-AVAILABILITY.md` or `FRONTIER-CLOUDS-VERIFY.md` if identity/catalog cannot be verified
5. `FAL-AVAILABILITY.md`
6. `DIRECT-AND-OTHER-SOURCES.md`
7. `SOURCE-OPTIMIZED-EXECUTION-MAP.md`
8. `ACCOUNT-ACTIONS.md`
9. `EVAL-008-CONTROLLER-BRIEF.md`

## Required anti-bias check

The Controller Brief must explicitly prove that sourcing did not determine selection:

- artifact structure showing `MODEL-ROSTER-FIRST.md` was completed before provider-route recommendations;
- list any Must/Should models that are **not** available through Frontier Clouds/fal;
- list any attractive Frontier Clouds/fal models deliberately excluded because they did not earn a model slot.

This is important: credits can optimize execution cost, but must not distort what the Capability Lab chooses to learn about.

## Stop / escalation

Stop and report rather than deciding if:

- the model universe is too ambiguous to distinguish underlying model versions;
- a supposedly important model has no legitimate/version-identifiable production access route;
- provider access requires accepting terms/payment/business verification to merely inspect availability;
- evidence materially contradicts the current product architecture;
- completing research requires paid API calls.

Otherwise continue through all packages autonomously.

## Completion standard

The Controller should be able to answer, in this order:

1. **Which models should we test, independent of sourcing, and why?**
2. **Which of those are available on Frontier Clouds?**
3. **Of the remainder, which are on fal?**
4. **For the remainder, exactly where do we source them?**
5. **Which new accounts, if any, does the user actually need?**

No benchmark execution. No paid calls. No Registry rows. No merge.