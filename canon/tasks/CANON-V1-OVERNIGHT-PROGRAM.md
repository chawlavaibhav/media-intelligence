# Canon V1 overnight program

**Date:** 26 Aug 2026  
**Status:** CONTROLLER-PREPARED FOR USER ASSIGNMENT  
**Read first:** `coordination/plans/2026-08-26-THREE-STREAM-OVERNIGHT-PROGRAM.md`, `canon/CHARTER.md`, `canon/HANDOFF.md`, `canon/knowledge/SPEC-01-creative-ir.md`, SPEC-03/04/05, Audit Gate v0.2, current accepted source directories and audit records.

## 0. Zoom-out: what Canon must become

Canon is the durable creative/production expertise layer. In production it should help the reasoning system turn an incomplete customer request into a better **Creative IR**, preserve explicit user intent, expose trade-offs and acceptance requirements, and later help a creative evaluator diagnose craft-level problems. It must never answer which current model/provider is best; that is Eval/Capability Lab.

Canon V1 is production-usable when:

1. the first-product knowledge coverage is explicitly known rather than inferred from source count;
2. important gaps are filled or visibly unresolved;
3. source-local knowledge has been deliberately synthesised across the product-facing knowledge packs without forcing false agreement;
4. a tested consumption method exists (oracle/automatic retrieval/compiled context/critic-revise comparison);
5. explicit Canon demonstrates planning lift and/or creative-evaluation lift without reducing explicit-intent preservation;
6. Canon can emit capability requirements that Eval understands, while emitting zero model/provider selections;
7. source knowledge remains durable while bindings/compiled views can change with the product.

### Current starting state

- live accepted Canon: **19 sources**;
- historical CANON-003/004 baseline: **16**, immutable as history;
- Audit Gate v0.2 authoritative; 19 active audit records;
- source/system/binding/ontology architecture is mature and should not be redesigned casually;
- no accepted Devanagari-structure source;
- no runtime Canon consumption mechanism has been tested;
- central claims that explicit Canon improves planning/evaluation remain unproven;
- no Canon task is currently open before this program is explicitly assigned.

## 1. Full Canon V1 task queue

| ID | Task | Overnight? | Start | End / quantitative done condition |
|---|---|---|---|---|
| **C1** | Fresh live-19 coverage rebaseline | **RUN TONIGHT** | current 19 accepted audited sources | 19/19 mapped against all 52 legacy domains + 10 product-facing packs; every domain/pack has evidence-backed coverage state, independent-origin count, binding state and gap status |
| **C2** | First-product 30-brief bank + oracle-context set | **RUN TONIGHT** | C1 can be in progress; first-product scope is frozen | exactly 30 underlying briefs across 10 scenario families; exact language/product-scope balance; 12 early-gate briefs selected; audited Canon oracle contexts prepared for the 12 without producing experiment outputs |
| **C3** | Core Canon value-gate execution package | **RUN TONIGHT — PACKAGE ONLY** | C2 | complete reproducible package for 12 briefs × 2 arms = 24 later planning outputs; prompts, matched generic contexts, randomisation, blind-review sheet, thresholds and logging all frozen; **0 LLM experiment calls tonight** |
| **C4** | Gap-closing source portfolio | **RUN TONIGHT — RESEARCH ONLY** | C1 gap map | <=14 proposed source identities, each tied to a specific uncovered/weak product need and documented with legitimate access route, exact scope, expected novelty, lineage risk and acquisition status; **0 ingestion/purchase/download tonight** |
| **C5** | Early value gate | LATER | C3 + approved execution access/human review | 24 planning outputs judged blind; result = continue/mixed/stop under predeclared gate |
| **C6** | Targeted source ingestion/audit | LATER | C4 + C5 continuation decision + explicit source approval | approved sources only, batches <=5; each accepted source passes full Audit Gate; stop early when coverage target met |
| **C7** | Cross-source synthesis by 10 production packs | LATER | C6 or Controller decision to synthesize current corpus only | 10/10 packs receive deliberate synthesis review: agreements, disagreements, trade-offs, scope, refusal/distinctness; no forced concept-count target |
| **C8** | Binding revalidation + Canon compiler/consumer candidates | LATER | C7 | 100% existing/new bindings checked against current SPEC-01/evaluation use; 30/30 briefs compile valid Canon context through each candidate consumption form being tested |
| **C9** | Planning/consumption Experiment A + invariance | LATER | C8 + qualified review protocol | 30 briefs across generic/oracle/automatic/compiled = ~120 outputs; best form gets 30 critic-revise outputs; 10 briefs × 4 extra phrasings × 2 arms = 80 invariance outputs; explicit intent measured separately |
| **C10** | Creative-evaluation Experiment B + production interface | LATER | shared Resources commercial bank + review protocol + C9 | reuse 60 active commercial assets; generic vs Canon = 120 evaluator outputs; final capability-requirement interface maps 30/30 briefs to Eval capability IDs or explicit unresolved states; zero model/provider names |

## 2. C1 — Fresh live-19 coverage rebaseline

### Objective

Replace the stale mental model of the 23-Aug curriculum/coverage map with an evidence-backed map of the **actual 19 accepted source directories now in Canon**.

### Do not do

- do not ingest anything;
- do not edit frozen source knowledge merely to improve coverage;
- do not treat raw object/binding counts as source quality;
- do not call a source independent merely because its id/author differs;
- do not rewrite the historical 16-source counts.

### Required coverage representation

Use the legacy **52 domains** as the detailed diagnostic surface, but also aggregate them into these **10 product-facing knowledge packs**:

1. composition & attention;
2. typography & copy;
3. product appearance;
4. colour & visual register;
5. camera & spatial grammar;
6. editing, pacing & short-form;
7. commercial communication;
8. concept & distinctiveness;
9. Indian/Indic context;
10. critique & effectiveness.

For every domain and pack, report at minimum:

- accepted source ids that materially contribute;
- **independent intellectual-origin count**, using active Audit Gate lineage records;
- whether relevant SourceConceptSystems exist;
- binding state: `creative_ir`, `evaluation`, `benchmark`, `production_candidate`, `governance`, `none`;
- coverage state using non-quality inventory terms only:
  - `absent`;
  - `present_single_origin`;
  - `present_multi_origin`;
  - `present_but_application_unbound` where useful;
  - `representation_or_evidence_limited` where Audit Gate material requires it;
- first-product importance: `critical / useful / peripheral`, justified against the frozen scope;
- concrete gap statement.

Do not invent a decimal "Canon quality" score.

### Deliverables

- `canon/planning/CANON-V1-LIVE19-COVERAGE.md`
- machine-readable companion `canon/planning/CANON-V1-LIVE19-COVERAGE.yaml` or `.csv`
- `canon/planning/CANON-V1-GAP-LEDGER.md`

### Done when

- 19/19 accepted source directories accounted for;
- 52/52 diagnostic domains accounted for;
- 10/10 product packs accounted for;
- no domain's status depends only on a title/library assumption rather than committed accepted knowledge;
- all independence claims resolve through the Audit Gate lineage records.

## 3. C2 — 30-underlying-brief bank and oracle contexts

### Why Canon owns this

This bank is the stable set of commercial intents used across Canon planning experiments and later sampled by Eval's end-to-end workflow benchmark. Eval must not create a competing commercial bank.

### Exact shape

Create **10 scenario families × 3 underlying briefs each = 30 briefs**:

1. typography-led/offer static creative;
2. product packshot/product-hero static;
3. person + product static ad;
4. reference-based campaign/edit brief;
5. product-hero video with external/no-visible-speech VO;
6. actor + product video with no visible dialogue;
7. one visible speaker;
8. two-person dialogue;
9. product handoff/action interaction sequence;
10. multi-shot branded 6–20 second ad.

### Language/context balance

Across the 30 underlying briefs target exactly:

- **10 English-primary**;
- **10 Hindi/Devanagari-primary**;
- **10 Hinglish/mixed-language**.

All 30 should be plausible Indian-business commercial briefs; do not make every brief culturally specific merely to satisfy the geography.

Across the bank include meaningful variety in:

- objective: awareness/consideration/conversion/demonstration/offer/brand;
- product category;
- product prominence;
- one/two-person complexity;
- brand/reference assets;
- exact-copy requirements;
- no-copy cases;
- simple and contradictory/underspecified instructions.

### Protect experiment validity

For each underlying brief preserve separately:

1. customer-facing raw brief;
2. authoritative intent/invariants used only for later scoring;
3. tags: scenario family, language condition, knowledge packs required, capability families likely required.

Do **not** author the finished Creative IR in the benchmark input file. That is what Experiment A is measuring.

### Early value-gate subset

Select exactly **12 of 30** for C3/C5. The subset must:

- cover all 10 product-facing Canon packs at least once where applicable;
- include at least 3 static and 5 video briefs;
- include at least 3 Hindi/Devanagari-sensitive briefs and at least 3 Hinglish/mixed briefs;
- include at least 2 briefs from known weak/gap areas and at least 4 from currently better-covered areas;
- be selected **before** any planning outputs are generated.

### Oracle context

For each of the 12 early-gate briefs, hand-select relevant accepted Canon material using only sources that currently pass the Audit Gate. Preserve systems/trade-offs together where isolated retrieval would distort them.

Oracle context should be concise enough to match a generic context by approximate word count later. Log every Canon ref and why it was included.

### Deliverables

- `canon/experiments/v1/brief-bank/briefs.jsonl`
- `canon/experiments/v1/brief-bank/README.md`
- `canon/experiments/v1/value-gate/early-12-manifest.json`
- `canon/experiments/v1/value-gate/oracle-contexts/`

### Done when

30/30 briefs validate, all balance counts are exact, 12/12 early briefs have auditable oracle context, and no experiment output has been generated.

## 4. C3 — Core value-gate package, not execution

### Future experiment question

Does explicit, correctly selected Canon improve planning beyond the same Creative-IR procedure plus a generic craft context?

### Frozen arms

- **Generic:** brief + Creative IR/procedure + generic craft checklist;
- **Oracle Canon:** same brief/procedure + hand-selected relevant accepted Canon.

Match formatting/instruction style and approximate context length. Do not make Oracle better merely by giving it more words or examples.

### Future output count

**12 briefs × 2 arms = 24 planning outputs.**

### Review dimensions

At minimum:

- concept quality;
- hierarchy reasoning;
- proposition clarity;
- objective fit;
- audience fit;
- visual/temporal strategy;
- trade-off awareness;
- contradiction handling;
- appropriate specificity;
- explicit user-intent preservation.

Intent preservation is a safety/gating dimension and must not be averaged away by creative quality.

### Predeclared engineering gate

After valid blind review later:

- **>=9/12 clear Canon wins and no meaningful explicit-intent regression:** continue;
- **7–8/12:** mixed; diagnose before source expansion;
- **<=6/12:** stop source expansion and diagnose Canon noise/redundancy/over-prescription first.

This is an engineering continuation gate, not a population confidence claim.

### Tonight deliverables

- exact prompts/templates;
- generic matched contexts;
- output schema;
- randomisation/blinding script or manifest;
- reviewer packet format;
- scoring/aggregation script that consumes later human verdicts but contains no invented labels;
- dry-run validation with dummy text only.

### Stop tonight

Do not invoke external LLM experiment APIs or fabricate human reviews.

## 5. C4 — Gap-closing source portfolio, research only

### Objective

Use C1 to create a bounded acquisition/ingestion proposal. **Do not build a bigger Canon because a source is interesting.** Every proposed source must solve a named first-product gap.

### Maximum portfolio

At most **14 source identities** across these slots; fewer is better if sufficient:

- Devanagari/Indic typography: <=2;
- short-form/feed-native creative grammar: <=3;
- Indian cultural/market context: <=2;
- product/packshot photography: <=2;
- modern effectiveness evidence: <=2;
- motion design/animated typography: <=1;
- accessibility/thumbnail legibility: <=1;
- consumer imagery/semiotics: <=1.

### Each candidate record must contain

- exact source identity and creator/publisher/institution;
- exact section/chapter/course module proposed, not merely a title;
- gap/knowledge pack it addresses;
- why current accepted sources do not already cover the same need;
- source type and likely extraction/visual hazards;
- official/creator/publisher/institution-authorised access route;
- current access state: free/open, purchase required, login/gated, streaming-only, DRM, blocked, unknown;
- rights/terms relevant to internal knowledge extraction;
- expected intellectual lineage/dependence with current Canon;
- technology/time/context contingency;
- whether evidence is practitioner assertion, empirical research, curriculum, critique, etc.;
- cost if discoverable, but **no purchase**;
- explicit `recommended / reserve / blocked / reject` disposition and reason.

### Research rules

Official/creator/publisher/institution routes only. No pirate PDFs, mirrors, torrents, unauthorized Drive links, course rips or access-control bypasses.

### Done when

Every `critical` gap from C1 has either at least one legitimate candidate route or an explicit `no suitable source found / non-source work needed` conclusion. Portfolio <=14.

## 6. Later tasks — boundaries so tonight does not create rework

### C5 early value gate

Do not run until morning review confirms the experiment package and a valid independent review path. Source expansion remains unexecuted until this gate says continue/mixed with explicit Controller disposition.

### C6 source ingestion

Only Controller-approved identities from C4. Batch <=5. Full existing extraction → systems/ontology → bindings → snapshot → Audit Gate order. No new schema merely to force a source through.

### C7 synthesis

Run after expansion decision so it does not need to be redone. Every 10-pack gets a deliberate review; refusal/distinctness is valid.

### C8 compiler/consumption candidates

Test consumption forms before building retrieval infrastructure. Do not assume vector RAG.

### C9/C10 experiments

Reuse the same 30-brief bank and the shared 60 active commercial assets from Resources. No new media generation for Canon experiments unless separately justified.

## 7. Autonomous decisions tonight

The Canon worker may decide:

- detailed mapping of accepted objects to domains/packs;
- brief wording inside frozen balance/coverage constraints;
- which accepted Canon refs belong in oracle context, with rationale;
- which legitimate source candidates merit `recommended/reserve/reject` status under C4;
- implementation details of dry-run experiment tooling.

The worker may **not** decide:

- to ingest a source;
- to spend money;
- to redefine SPEC-01/03/04/05 or Audit Gate;
- to create a new product architecture layer;
- to execute C5+;
- to merge to main.

## 8. Stop conditions

Stop the affected work package and document the exact blocker if:

- current accepted-source state cannot be reconciled mechanically;
- an Audit Gate record is stale or invalid;
- C1 reveals a material contradiction in the frozen product scope;
- a required source route is gated/restricted/legally ambiguous;
- experiment validity would require inventing human judgements or using an unapproved external API;
- another stream's file must be changed to proceed.

Continue other independent work packages when safe.

## 9. Morning Controller brief

Create `canon/findings/CANON-V1-OVERNIGHT-CONTROLLER-BRIEF.md` with exactly:

1. work packages attempted/completed;
2. quantified deliverables and verification;
3. current live-19 coverage headline;
4. 30-brief bank balance summary;
5. value-gate package readiness;
6. <=14 source portfolio summary and blocks;
7. assumptions/decisions made locally;
8. cross-stream dependencies for Eval/Resources;
9. files/commits;
10. explicit list of what was **not** executed.
