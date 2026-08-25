# Three-stream overnight program — Canon, Eval, Resources

**Date:** 26 Aug 2026  
**Status:** CONTROLLER-PREPARED FOR USER ASSIGNMENT  
**Purpose:** give the three domain agents enough end-to-end context and a finite task queue to work independently for a long session with minimal Controller interaction.

## 1. Product end-state

The product is an API-native media production intelligence layer optimising **Cost per Accepted Outcome**.

The stable responsibility split is:

- **Canon** defines what a good commercial-media outcome should accomplish, what craft/creative decisions matter, what trade-offs apply, what to inspect, and which capabilities a job requires. Canon never ranks current models.
- **Eval / Capability Lab** measures what current models/workflows can actually do, qualifies evaluators, produces empirical Capability Registry entries, and maintains current capability/failure/cost evidence.
- **Resources** supplies independent, rights-documented, lineage-aware, integrity-validated media/reference/evaluation material required by Canon and Eval. It does not define creative quality or Eval's metrics.
- **Production Planner** is downstream and remains out of scope. It will eventually join Canon-derived requirements to Eval's Capability Registry.

## 2. Why this program exists

The streams have individually made progress but were being advanced task-by-task. That created three risks:

1. local optimisation without a complete end-state;
2. duplicate work, especially generating or collecting one asset per metric instead of reusing assets across valid measurements;
3. repeated Controller questions because future dependencies were not frozen in advance.

This program makes the dependency graph explicit before more empirical spend or source expansion.

## 3. Shared V1 interfaces frozen for planning

These are planning interfaces for the overnight tranche. Workers may propose changes but may not silently change them.

### 3.1 First-product scope

Short-form commercial media for Indian businesses:

- static commercial creatives;
- product/brand imagery;
- short product/brand videos, approximately 6–20 seconds;
- people + product media;
- voiceover, one-speaker and two-speaker cases where relevant;
- English, Hindi, Hinglish and Devanagari-sensitive use cases.

### 3.2 Eval capability map

Eval V1 is planned around **36 capability dimensions** in eight families:

1. constraint fidelity;
2. text & brand;
3. identity & references;
4. human & physical realism;
5. temporal / continuity;
6. speech / audio;
7. commercial / creative fitness;
8. operational / workflow behaviour.

Eval owns the exact definitions and measurement contract.

### 3.3 Eval instrument families

Six planned evaluator families:

1. text/OCR;
2. deterministic/CV geometry;
3. structured visual VLM;
4. temporal/video evaluator;
5. speech/audio/AV evaluator;
6. creative/commercial evaluator.

### 3.4 Shared resource requirements

Unless a worker finds a material flaw, use these as the planning targets:

- existing Devanagari pools for text-reader calibration, respecting BSTD vs CVIT lineage;
- **12 products × >=4 views = >=48 product-reference images**;
- **8 identities × >=4 views = >=32 person-reference images**;
- **24 single-speaker + 12 two-speaker = 36 clean AV clips**, with transcript; two-speaker clips also need turn boundaries; English/Hindi/Hinglish represented;
- **80 commercial creative assets = 40 static + 40 video**, split into 60 active + 20 untouched reserve; target >=50% Indian-market representation; selection must be independent of Canon principles;
- legacy production/regression assets reconciled once and then preserved;
- all future paid/irreproducible benchmark outputs preserved durably with exact provenance.

### 3.5 Shared brief reuse

Canon owns the first-product **30-underlying-brief bank**. Eval must not independently create a competing 30-brief commercial bank. Eval may design capability-specific atomic/compound benchmark items tonight, but the later 12 end-to-end production-workflow briefs must be selected from Canon's accepted 30-brief bank after integration.

Resources does not label those briefs or select media to flatter their Canon principles.

## 4. Shared benchmark economy rule

**Generate once, measure many valid dimensions.**

A generated asset may feed every independent measurement for which it is a valid observation unit. Do not regenerate an asset merely because a second metric needs to inspect it.

Use two test classes:

- **atomic probes** when causal isolation is required;
- **compound production scenarios** when several capabilities can be measured legitimately from one asset.

Repeats measure reliability. Repeats never count as distinct base items.

## 5. Overnight tranche — what may run

The user intends to assign the three runbooks independently. Once a user explicitly assigns a stream's runbook, that stream may execute its marked **RUN TONIGHT** work packages autonomously on its own branch.

### Allowed tonight

- repository analysis and re-baselining;
- design/specification/manifests;
- public web research and official-document verification where needed;
- current model/API/pricing inventory **without making generation/evaluator API calls**;
- current corpus reclassification/integrity analysis;
- source discovery/access-route research **without purchasing, logging in, accepting terms, or downloading a materially new source family**;
- local code/tests/harnesses using synthetic/dummy fixtures;
- reconciliation of already accessible historical project artifacts;
- task/experiment packages that are ready for later execution.

### Not allowed tonight

- any paid generation or paid checker/evaluator API call;
- any empirical Capability Registry score;
- any claim that a model/workflow is qualified;
- new account creation, login, gated-source access, click-through terms, purchases, course enrolment or DRM bypass;
- materially new Resources acquisition;
- new Canon ingestion;
- human judgement invented by the agent;
- Production IR or Planner/routing implementation;
- merging the worker branch to `main`.

## 6. Branch and write isolation

Use one branch per worker, based on the current `main` after this program is committed:

- Canon: `work/canon-v1-overnight`
- Eval: `work/eval-v1-overnight`
- Resources: `work/resources-v1-overnight`

Workers write only inside their stream plus explicitly permitted cross-stream proposal files. They must not edit another stream's outputs.

Each work package should end in its own commit where practical so morning review can accept/reject pieces independently.

## 7. Cross-stream dependency graph

```text
                 ┌────────────────────────────┐
                 │ first-product scope        │
                 │ shared V1 interfaces       │
                 └──────────────┬─────────────┘
                                │
       ┌────────────────────────┼────────────────────────┐
       │                        │                        │
       ▼                        ▼                        ▼
CANON rebaseline         EVAL capability map      RES requirements map
+ 30-brief bank          + test architecture      + corpus rebaseline
       │                        │                        │
       │                        ├──────────┐             │
       │                        │          │             │
       ▼                        ▼          ▼             ▼
Canon value-gate       resource reqs   model/API      allocation/
package                + bank spec     inventory      leakage/storage
       │                        │                        │
       └──────────────┐         │                        │
                      ▼         ▼                        ▼
             MORNING INTEGRATION GATE
                      │
       ┌──────────────┼──────────────────────────────┐
       ▼              ▼                              ▼
Canon value gate   Resources targeted packs     Eval evaluator qualification
(human/text)       + commercial bank            + harness finalisation
       │              │                              │
       └──────────────┼──────────────────────────────┘
                      ▼
             empirical Eval waves
          admission → deep qualification
          → production workflow benchmark
                      │
                      ▼
          Capability Registry + feedback
```

## 8. Morning integration gate

Before any new empirical spend or acquisition, Controller review should answer only these finite questions:

1. Did all three agents preserve the responsibility boundaries?
2. Do Canon's 30 briefs and Eval's capability/scenario map cover the same first-product scope without duplication?
3. Does Resources' requirement matrix exactly satisfy Canon/Eval needs, with no speculative collection?
4. Are the six evaluator families measurable with the proposed resources, and which remain blocked?
5. What exact current APIs/models are genuinely accessible, and what would the frozen paid benchmark cost?
6. Which new source identities, if any, deserve explicit acquisition/ingestion approval?

No paid run begins until the exact model/version/access/pricing forecast is reviewed.

## 9. Morning expected state

A successful overnight session should leave us with:

- Canon: fresh live-19 coverage baseline; 30-brief bank; oracle-context/value-gate package; gap/source portfolio ready for review;
- Eval: complete V1 capability/measurement contract; current model/workflow inventory and cost sheet; evaluator qualification specification; reusable atomic/compound bank design; harness/storage interface implementation and tests where possible;
- Resources: exact requirement matrix; existing-corpus fit/gap map; protected-set/lineage/storage design; legacy evidence reconciliation; candidate supply routes for missing controlled/commercial packs without unauthorized acquisition;
- zero paid API spend;
- zero new empirical Registry claims;
- zero unauthorized source access.

## 10. Full V1 end-state

The overnight tranche is not V1 completion. It is the specification/infrastructure tranche that should eliminate most future back-and-forth.

V1 is operational only when:

- Canon has demonstrated useful planning and/or critique lift and has a tested consumption form;
- Eval has qualified instruments, current empirical workflow capability entries, production-workflow comparisons and maintenance cadence;
- Resources can mechanically answer whether every approved experiment has valid independent evidence, protected reserves and rights/integrity records;
- the three streams expose clean interfaces to the later Production Planner without crossing responsibility boundaries.
