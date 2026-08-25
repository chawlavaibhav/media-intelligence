# Resources V1 overnight program

**Date:** 26 Aug 2026  
**Status:** CONTROLLER-PREPARED FOR USER ASSIGNMENT  
**Read first:** `coordination/plans/2026-08-26-THREE-STREAM-OVERNIGHT-PROGRAM.md`, `resources/CHARTER.md`, `resources/HANDOFF.md`, RES-001/002 Controller briefs, generated integrity/bias reports, source registry/manifests, Eval's current battery/plans and Canon Experiment V0 only as consumers—not as truth about how Resources should label media.

## 0. Zoom-out: what Resources must become

Resources is the project's **evidence supply chain**, not a dataset-hoarding stream. It should be able to answer, mechanically:

> For every approved Canon/Eval experiment, do we have the required independent material, with known provenance, rights/access status, lineage, integrity, protected-set role and reproducible retrieval/preservation path?

Resources does not define creative quality, model capability, Canon truth or routing. It supplies evidence without selecting examples because they flatter the theory being tested.

Resources V1 is production-usable when:

1. every Canon/Eval material need has an explicit requirement record;
2. existing material is classified by what it can and cannot validly support;
3. development/calibration/qualification/reserve/regression roles are protected against leakage;
4. byte identity, content lineage and source lineage are separately tracked;
5. missing controlled product/person/AV and commercial-creative packs are supplied or explicitly blocked;
6. external reacquirable archives and irreproducible empirical model outputs use different retention policies;
7. all future Eval benchmark outputs can be preserved once and reused across many measurements;
8. rights/terms are reopened before publication/customer use where current material is internal-eval-only.

### Current starting state

- **34,786 items / 5.70 GB media** across 8 acquired sources;
- **34,786/34,786 decode cleanly**;
- 4 blocked candidates;
- 29,722 photographed Devanagari images dominate item count;
- IndicSTR12 + IIIT-ILST are one CVIT lineage for holdout purposes; BSTD is the independent Devanagari reserve;
- ImageRewardDB, KoNViD-1k, VideoFeedback and VideoGen RewardBench provide useful evaluator-development material but are not current Indian commercial-creative truth;
- no proper controlled product-reference pack;
- no proper controlled person-reference pack;
- no audio/AV calibration pack;
- no professional/commercial creative bank;
- legacy project generation/failure material exists partly outside the Resources corpus;
- current rights posture for RES-001/002 acquisitions is internal research/evaluation only unless separately reviewed.

## 1. Shared required packs

Use these frozen planning targets unless a material flaw is demonstrated and recorded for Controller review:

- existing Devanagari pools, with lineage caveats;
- **>=48 product-reference images = 12 products × >=4 controlled views**;
- **>=32 person-reference images = 8 identities × >=4 controlled views**;
- **36 clean AV clips = 24 single-speaker + 12 two-speaker**, with transcripts; two-speaker also needs turn boundaries; English/Hindi/Hinglish represented;
- **80 commercial creative assets = 40 static + 40 video**, of which 60 active and 20 untouched reserve; target >=50% Indian-market; at least 6 commercial categories;
- durable archive contract supporting **>=1,000 irreproducible generated/processed Eval outputs** without redesign;
- one-time reconciliation of historical production/regression evidence.

Resources owns provenance/integrity/rights/lineage/roles. Eval owns labels and thresholds. Canon owns knowledge, not media selection.

## 2. Full Resources V1 task queue

| ID | Task | Overnight? | Start | End / quantitative done condition |
|---|---|---|---|---|
| **R1** | Resource requirements matrix | **RUN TONIGHT** | shared Canon/Eval V1 interfaces | 36/36 Eval capabilities + 6/6 evaluator families + Canon planning/evaluation experiments classified as `external_resource_required / constructed_by_eval / existing_resource_sufficient / no_external_resource`; every required row has media type, target count, metadata, independence, rights and consumer |
| **R2** | Existing-corpus rebaseline + legacy evidence reconciliation | **RUN TONIGHT** | current 8 acquired + 4 blocked + known project-history leads | 8/8 acquired and 4/4 blocked sources mapped to R1; all known legacy pools end `recovered / metadata_only / unavailable`; no vague "some old assets exist" state remains |
| **R3** | Allocation, leakage, lineage & storage contract | **RUN TONIGHT** | R1/R2 | role model and validators implemented/design-frozen; exact-hash/content-lineage/source-lineage separated; protected-set overlap checks; reacquirable external vs irreproducible empirical storage classes; artifact manifest ready for Eval |
| **R4** | Missing-pack supply-route portfolio | **RUN TONIGHT — RESEARCH ONLY** | R1 gaps | <=3 candidate legitimate supply routes per missing pack (product/person/AV/commercial), plus controlled-capture/synthetic option where public sourcing is unsuitable; rights/access/scale/cost/limitations documented; **0 new acquisition tonight** |
| **R5** | Existing-resource Eval views | **RUN TONIGHT where possible** | R2/R3 | reusable manifests/views for current Devanagari, image-preference, real-video and generated-video pools; no duplicate media copies; every view states valid/invalid uses and protected-set role is unassigned until Eval decides |
| **R6** | Controlled reference pack acquisition/construction | LATER | R4 + explicit source/capture approval | >=48 product + >=32 person + 36 AV assets; provenance/permission/transcripts/turns complete; independence recorded |
| **R7** | Commercial creative bank | LATER | R4 + explicit source approval | 80 assets = 40 static/40 video; 60 active/20 reserve; >=50% Indian-market target; >=6 categories; selection independent of Canon principles; no Resources-authored creative labels |
| **R8** | Regression & empirical evidence archive | **RUN TONIGHT — SCHEMA/LEGACY; CONTINUES LATER** | R2/R3 | legacy reconciliation complete where accessible; empirical-output archive schema supports >=1,000 outputs; later every Eval paid output stored once with exact provenance and reusable measurement links |
| **R9** | Resource V1 operationalization | LATER | R6/R7/R8 + Eval/Canon integration | every approved resource requirement = available / blocked_with_reason / not_required; 0 unknown critical requirements; pre-benchmark integrity/leakage check automated; rights reopening triggers defined |

## 3. R1 — Resource requirements matrix

### Objective

Convert the cross-stream plans into the single backlog Resources should serve. **Do not discover datasets before knowing which row they serve.**

### Required consumers

Map at least:

- all **36 Eval capability dimensions**;
- all **6 evaluator families**;
- Canon's 30-brief planning/value-gate work where independent media is or is not required;
- Canon Experiment B / Eval creative-commercial calibration shared material;
- Eval's 100-item bank design and later 12-brief end-to-end production benchmark;
- regression/production-failure retention.

### For every requirement row record

- requirement id;
- consuming stream/task/family;
- media type/modalities;
- target quantity or `constructed_by_eval` rule;
- required metadata/labels/reference truth;
- whether source-provided labels are merely observations or can be deterministically validated;
- independence requirement: item / identity / product / speaker / scene / source lineage;
- geography/language/script conditions where relevant;
- rights/access minimum;
- storage/retention class;
- current source(s) that may satisfy it;
- state: `available / partial / missing / blocked / no_external_resource`;
- why.

### Important examples

- exact object count/geometry may be `constructed_by_eval`, not a reason to download a dataset;
- Devanagari reader calibration can use existing real photographed pools, but generated-text correctness must come from Eval-generated outputs;
- model latency/cost/refusal requires no Resources media;
- creative/commercial evaluator calibration and Canon Experiment B share one 60-active-asset resource bank rather than two independent acquisitions.

### Deliverables

- `resources/v1/RESOURCE-REQUIREMENTS-MATRIX.csv`
- `resources/v1/RESOURCE-REQUIREMENTS.md`
- machine-readable `resources/v1/resource-requirements.yaml`

### Done when

36/36 capabilities and 6/6 evaluator families have an explicit resource disposition and every external acquisition target exists because a named requirement needs it.

## 4. R2 — Existing corpus rebaseline + legacy reconciliation

### Objective

Before collecting one more byte, determine exactly how much of R1 is already solved.

### Current source inventory

Account for all 12 existing candidate records:

**Acquired:**

1. BSTD Devanagari;
2. IndicSTR12 Devanagari;
3. IIIT-ILST Devanagari;
4. ImageRewardDB;
5. KoNViD-1k;
6. VideoFeedback;
7. VideoGen RewardBench;
8. YouTube UGC sample.

**Blocked:**

9. PVP;
10. Pitt Ads;
11. LSVQ;
12. AVA.

Do not reopen a blocked source merely because it is unresolved. It must solve a requirement better than legitimate alternatives.

### For each acquired source record

- exact item count/media bytes from generated reports;
- current rights/access state;
- valid V1 uses;
- invalid/misleading uses;
- label provenance and trust limitations;
- generator era/geography/domain skew;
- exact duplicates;
- content/source lineage beyond byte hashes;
- reacquisition method;
- whether any item is currently safe to allocate to development/calibration/qualification/reserve—and why allocation must still be frozen until Eval's experiment split is accepted.

### Devanagari rules

Preserve:

- IndicSTR12 + IIIT-ILST as one CVIT lineage for independence;
- BSTD as genuine cross-lineage reserve candidate;
- crop labels are largely recoverable, but media-category counts must partition correctly;
- filter script, not only `language == hindi`;
- distributor labels are candidate calibration observations until Eval validates as required.

### Legacy evidence reconciliation

Inspect all legitimately accessible project history, including `chawlavaibhav/media-factory`, current repo references, known Finding-01 material and the previously referenced 64 human-scored generations.

For every expected legacy asset/set, end in exactly one state:

- `recovered` — bytes accessible, hash/provenance captured;
- `metadata_only` — record/evaluation exists but media bytes not available;
- `unavailable` — concrete search performed and no retrievable project artifact found.

Do not search indefinitely. Document the exact locations checked.

Resources may not silently promote historical human labels to current ground truth; preserve them as historical observations with provenance.

### Deliverables

- `resources/v1/EXISTING-CORPUS-FIT-GAP.md`
- `resources/v1/legacy-evidence/LEGACY-EVIDENCE-RECONCILIATION.md`
- updated machine-readable lineage/fit companion if needed without corrupting historical manifests.

## 5. R3 — Allocation, leakage, lineage and storage contract

### Resource roles

Define these experiment-relative roles:

- `development`;
- `calibration`;
- `qualification`;
- `reserve`;
- `regression`.

Role is not a property of the asset forever. It is an allocation in a named experiment/version. One file should not be duplicated on disk merely to represent two metadata roles.

### Leakage checks

Implement/design checks at three levels:

1. **byte identity** — SHA256 or equivalent exact hash;
2. **content lineage** — crop/transform/encode of the same parent scene/media;
3. **source lineage** — same collection/lab/project/derivative ancestry even when no bytes overlap.

A protected reserve should fail closed if a known development/calibration lineage collision exists under the experiment's independence rule.

### Storage classes

#### A. Reacquirable external material

Use current transient-acquisition policy where appropriate. Retain selected members, hashes, full remote member list, selection rule, official URL/remote metadata and retrieval script. Do not fabricate full-archive hashes for archives never held.

#### B. Controlled/permissioned reference material

Retain durable originals plus permission/provenance records required for repeated identity/product/audio use.

#### C. Irreproducible empirical model output

**Never treat as safely reacquirable.** Future provider/model/version behaviour may drift. Preserve output bytes plus:

- trial/attempt id;
- Eval item id;
- exact provider/model/version/endpoint/workflow;
- prompt/config/ref hashes and recoverable config location;
- seed/settings when exposed;
- timestamps;
- output hash;
- generation/transform/evaluator cost refs;
- API status/error/refusal;
- evaluator/result references.

Resources stores evidence; Eval owns interpretation.

### Capacity requirement

The schema/manifest must support at least **1,000 empirical outputs** without redesign. Do not guess a byte budget; later Eval E2 pricing/model roster should provide duration/resolution and Resources can forecast bytes before paid execution.

### Deliverables

- `resources/v1/RESOURCE-ALLOCATION-SPEC.md`
- `resources/v1/resource-allocation-schema.yaml`
- `resources/v1/EMPIRICAL-ARTIFACT-MANIFEST-SCHEMA.yaml`
- validators/tests where practical;
- dry-run manifests using dummy metadata only.

## 6. R4 — Missing-pack supply-route portfolio, research only

### Purpose

Give the morning Controller explicit ways to fill the four important missing resource packs without allowing overnight acquisition to create rights/consent mistakes.

### A. Product reference pack

Target later: **12 products × >=4 views = >=48 images**.

Research up to **3 legitimate supply strategies/routes**. Prefer, in order:

1. project/user-owned or permissioned product assets;
2. purpose-built controlled objects/packaging with clear ownership;
3. clearly licensed/open product/object datasets if they genuinely preserve repeated product identity.

Do not assume copyrighted e-commerce catalog photography is usable simply because it is public.

### B. Person identity pack

Target later: **8 identities × >=4 views = >=32 images**.

Research up to 3 strategies. Strong preference for:

- consented internal capture;
- purpose-created/synthetic identity references with clear rights if scientifically suitable;
- explicitly licensed identity datasets only if terms and privacy/biometric implications fit internal evaluation.

Do not acquire random public people's faces tonight. Flag privacy/biometric implications explicitly.

### C. AV pack

Target later: **24 single + 12 two-speaker = 36 clips**.

Need trustworthy transcript; two-speaker needs turn boundaries. Desired planning balance:

- single: 8 English, 8 Hindi, 8 Hinglish;
- two-speaker: 4 English, 4 Hindi, 4 Hinglish.

Research up to 3 source/capture strategies. Prefer permissioned/creator-authorised material or controlled recording where possible. Audio rights and voice/identity permissions must be visible separately.

### D. Commercial creative bank

Target later: **80 = 40 static + 40 video; 60 active + 20 untouched reserve**; target >=50% Indian-market and >=6 commercial categories.

Research up to 3 source strategies. Possible routes may include explicitly licensed ad/creative archives, creator/brand permissions, research datasets with acceptable internal-use terms, or controlled first-party material. Do not select assets because Canon predicts they are good/bad; selection axes may be product category, media type, market/language, duration, platform etc., never the theory under test.

### For every candidate route record

- exact source/strategy identity;
- official/creator route;
- access state;
- rights/terms for media, annotations, audio/voice and redistribution separately where relevant;
- expected obtainable count;
- geography/language fit;
- independence/lineage risk;
- privacy/biometric issue if people appear;
- cost/manual effort if known;
- `recommended / reserve / blocked / reject`.

### Hard overnight rule

**No new material download/acquisition from a materially new source family. No login/account, no forms, no terms acceptance, no purchase.**

## 7. R5 — Existing-resource Eval views

### Objective

Make current material easier for Eval to consume without copying/relabeling it.

Prepare reusable selection/view manifests for current resources, such as:

- Devanagari candidate development/calibration pools, with CVIT/BSTD lineage visible;
- ImageRewardDB development view;
- KoNViD technical-video-quality development view;
- VideoFeedback generated-video score view;
- VideoGen RewardBench cross-generator pairwise view.

Each view must include:

- source item ids/hashes, not duplicate media bytes;
- valid uses;
- invalid uses;
- label provenance;
- lineage group;
- rights status;
- no final protected role unless Eval's experiment assigns it.

Do not create a holdout just because a convenient publisher split exists.

## 8. R8 — Regression/empirical archive tonight and later

### Tonight

- finish legacy reconciliation from R2;
- implement/freeze empirical artifact manifest/storage rules from R3;
- prove with dummy manifests that one output can link to many Eval measurements without storing duplicate media;
- define how a production failure becomes a candidate regression resource without Resources deciding the failure label.

### Later

Before Eval E7 paid generation begins, confirm the archive destination has enough storage for the exact forecast. Every paid/irreproducible output should be ingested durably as part of execution, not cleaned up after scoring.

## 9. Later R6/R7/R9 boundaries

### R6 controlled references

Requires exact Controller-approved source/capture strategies from R4. No substitutions. Validate permission/provenance/transcripts/turns before handing to Eval.

### R7 commercial bank

Acquire 80 under the approved strategy. Freeze the 20 reserve before evaluator/Canon tuning. Resources must never write creative-quality labels.

### R9 operationalization

Produce a single current report where every approved cross-stream requirement is `available`, `blocked_with_reason`, or `not_required`, with automated integrity/leakage checks before a benchmark run.

## 10. Autonomous decisions tonight

Resources may decide:

- exact R1 matrix representation;
- how current sources map to valid/invalid uses;
- implementation of role/lineage/storage schemas and validators;
- which legitimate routes are `recommended/reserve/reject` under R4 research constraints;
- bounded reconciliation mechanics for already accessible legacy project assets.

Resources may **not**:

- acquire a new source family;
- cross a gate/login/terms/paywall/form;
- spend money;
- collect random public faces/voices;
- invent creative-quality labels;
- decide Eval thresholds or Canon truth;
- change another stream's files;
- merge to main.

## 11. Stop conditions

Stop the affected package and document rather than ask overnight if:

- a candidate route has unclear/explicitly restrictive rights or gated access;
- identity/voice sourcing raises unresolved consent/privacy/biometric issues;
- a new acquisition would be required;
- a legacy artifact reference cannot be resolved after bounded repository/location checks;
- source/content lineage cannot be established sufficiently for a claimed protected split;
- another stream's file must be edited to proceed.

Continue independent work packages where safe.

## 12. Morning Controller brief

Create `resources/reports/RESOURCES-V1-OVERNIGHT-CONTROLLER-BRIEF.md` containing:

1. R1–R5/R8 attempted/completed status;
2. exact requirements/gap counts;
3. current 34,786-item corpus fit summary;
4. legacy evidence reconciliation counts (`recovered / metadata_only / unavailable`);
5. role/leakage/lineage/storage verification;
6. candidate routes for product/person/AV/commercial packs and rights/privacy blocks;
7. existing Eval views created;
8. cross-stream dependencies;
9. files/commits;
10. explicit confirmation of **0 new source-family acquisition and ₹0 spend**.
