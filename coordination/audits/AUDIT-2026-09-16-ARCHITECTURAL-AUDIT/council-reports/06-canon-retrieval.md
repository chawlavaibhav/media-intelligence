# AGENT 6 — Canon / Retrieval council: inventory and consumption-path audit

Repo: MI `main @ 3bb9a3c3da484e43d4d54ae20543d1d246769ac6` (verified `git rev-parse HEAD`). Read-only. All counts below were computed by commands recorded in the working notes (`scratchpad/audit/agents/work06/`); prose numbers from PROJECT-MEMORY / CONTROL-STATE were not used as evidence.

Labels: **OBSERVED** (computed or read from committed bytes), **INFERENCE**, **HYPOTHESIS**, **UNKNOWN**.

---

## 0. Headline in one paragraph

Canon is a 7.07 MB / 1,300-object library of which exactly two compiled packs (104 objects, 44,644 bytes of cited claim text, 21 decisions) can reach any production code path. The retrieval mechanism in `runtime/canon/packs.py` is a deterministic table lookup (NR fields → pack ids → pre-compiled bytes); there is no keyword, BM25 or embedding retrieval anywhere on `main` (a BM25 module was built at `8115400` on an unmerged branch and dispositioned SUPERSEDE). The only thing that ran a real production — the `/media-agency` skill — did invoke this lookup for the Cumin job (recomputed `prefix_sha256 4d7a5b27…` matches the job record byte-for-byte), and it fired ten packs, of which eight were `selected_uncompiled` — including `commercial_communication`, the pack that holds the ABCD / Ogilvy / Hopkins / StoryBrand knowledge the human then rejected the job for lacking ("did cannon say nothing about product positioning? … canon had this knowledge. how's that possible?"). That knowledge reached state 1 of 8 (exists) and no further: the trigger fired, nothing was compiled, the runtime recorded a gap and continued by design (`packs.py` docstring: "a missing pack never blocks a job"). Two of the six Cumin failures (text over people, voice casting) have **no** accepted Canon knowledge at all — those are content gaps, not retrieval gaps.

---

## 1. INVENTORY TABLE

Counts (OBSERVED, computed at HEAD by `work06/count.py` and follow-ups):

| Layer | Count | Bytes (excl. snapshots) | Command |
|---|---|---|---|
| Accepted sources (`canon/knowledge/current/*/`) | 37 | 7,068,257 | `ls canon/knowledge/current \| wc -l`; `os.walk` sum |
| SourceKnowledge objects | 1,300 (1,273 explicit_source_claim / 27 source_interpretation) | — | yaml walk of `source-knowledge.yaml` |
| Source concept systems | 132 | — | `source_concept_systems` lists |
| Operational bindings | 291 (266 `proposed`, 25 `production_candidate`; 249/291 with no `target_path`; 42 `creative_ir`) | — | `operational_bindings` lists |
| Ontology terms / concepts / relationships | 1,191 / 151 / 422 (0 cross-source) | — | `ontology-mappings.yaml` |
| Remedy terms with `executable_by` | 382 remedy terms; tag membership human_edit 221, physical_production 93, unknown 76, deterministic_composite 19, generative_respecification 11 | — | see §5 |
| Source-stated remedies / problems (inside SK) | 1,289 / 1,260 (862 / 834 SK objects carry ≥1) | — | yaml walk |
| Confidence markers | 1,300 (one per SK) | 237,675 | `canon/compilation/marker-map-v0.yaml @ 5bca547` |
| Compiled packs | 2 of 10 (PA: 10 decisions, 35 cited SK, 11 conflicts, 4 limits; CA: 11 decisions, 69 cited SK, 17 conflicts, 2 limits) | terse text 9,889 + 9,986 chars = 2,473 + 2,497 tokens; 1,371 + 1,395 words | `PACK-*-v0.yaml @ 97ac482` |
| Pack trigger rules | 28 cells (4 modalities × 7 ops), 2 universal packs, 3 modality base sets (+audio = ∅), 4 conditional rules, 1 uncertainty rule, 1 coverage-gap notice | 9,801 | `pack-triggers-v0.yaml @ 515b6db` |
| Injection prefix v1 | 1 fenced block, 1,311 chars = 328 tokens | 5,399 (file) | `runtime/canon/INJECTION-PREFIX-v1.md @ 76c3059` |
| KIND-NR binding | 9 deliverable kinds → (modality, operation, advertising_intent); 2 ambiguity markers | 4,868 | `KIND-NR-BINDING-v0.yaml @ a8754fe` |
| Gate vocab / check registry | 21 check lines loaded from the 2 packs; 10 mechanised pre-dispatch (partial), 1 post-draw (CA-D6) + LIMIT-TEXT | 410,868 (canon/gate incl. pycache) | `canon/gate/doctrine.py @ 47efc09`, `predispatch.py @ da9219d` |
| Context spec (CANON_CONTEXT v0.1) | 1 spec + schema + 1 example (14,240 B) | 56,961 | `canon/context/** @ dda579f` — **no code consumer** (grep over runtime/, canon/gate, tests: 0 hits) |
| Q&A bank | 1,028 items / 23 banks; 796 items belong to accepted sources but **688 of those still carry `source_status: hold`** (stale since DN-06) | 2,257,118 | `canon/qa/canon-014 @ c6f8d91` |
| Domain vocabulary | 583 label→term mappings, 53 queued, 22-term closed enum | 67,081 | `canon/ontology/PROPOSED-domain-vocabulary-v1.yaml @ 6681a81` |
| Cross-source join candidates | 60 records, all `status: proposed` | — | `canon/candidates/ontology-join/cross-source-candidates-v0.yaml @ 62dc3ad` |
| Coverage layer | 10 packs × 56 domains; pack_state: 5 covered, 4 critical_limited (product_appearance, editing, commercial_communication, indian_indic), 1 critical_hole (typography A14) | — | `CANON-V1-LIVE37-COVERAGE.yaml @ a777987` |
| Templates (empirical memory) | 0 templates promoted in `runtime/store/templates` at HEAD (dir absent) | — | `runtime/canon/templates.py @ 0a40542` |

### 1.1 Per-asset consumption matrix

Legend for "state reached in cases 001/002/003": E=exists, R=retrieved, C=in context, U=understood, D=changed a decision, K=correct, S=survived, Q=QA-detected.

| Asset | WHAT IT KNOWS | WHO CONSUMES / WHEN | HOW RETRIEVED | HOW MUCH ENTERS CONTEXT | HOW IT CHANGES A DECISION | HOW WE KNOW | USED IN 001/002/003? | IF NOT, WHY IT EXISTS |
|---|---|---|---|---|---|---|---|---|
| **Source books** (`canon/sources/*.txt`, 6 files, 725 KB; the other 31 sources exist only as extractions) | raw chapter text for the CANON-003 six | nobody at runtime | none | 0 | none | — | No | provenance for the extraction; `canon/sources/figures/*.jpg` back the visual-evidence ledgers |
| **SourceKnowledge** (1,300 objects) | one claim each with mechanism, scope, caveats, source-stated problems/remedies, examples, intra-source relations, evidence flags, provenance | (a) the offline compiler `compile_pilot_packs.py` renders 104 of them by id into the two packs; (b) humans reading YAML | by id only, offline | 0 bytes directly; indirectly ≤ the pack terse text | only via a pack decision | pack `compiled_from[]` lists the ids | 104/1,300 reachable; 0 read directly by the operator (INFERENCE: job record cites no sk_ id) | the corpus the packs are compiled from; 92% of it is inert today |
| **Concept systems** (132) | ordered/causal groupings of SK with dependencies, tradeoffs, conflicts | compiler (scs_ ids cited in 2 packs: `scs_lsm_c003_001/002`, `scs_alt_c003_002`, `fre_001..005`, `murch_001`, `gos_001`, `ms_002/003`) | by id, offline | 0 directly | pack default text cites them | `compiled_from` kind=concept_system | via packs only | intended seed for pack compilation (domain-system map) |
| **Ontology** (1,191 terms, 151 concepts, 422 relationships, all intra-source) | problem/remedy/property/entity vocabulary per source; `executable_by` tags on remedies | nothing at runtime; `validate_domain_vocabulary.py`; HOLD-id scan in `doctrine.py` uses sk_/scs_ id shapes only | none | 0 | none | — | No | SPEC-05 join layer; the 60 cross-source candidates are its only cross-source edges and all are `proposed` |
| **Operational bindings** (291) | "how today's system could use this SK" — target_type ∈ {evaluation 102, governance 89, creative_ir 42, benchmark 33, production 25}; role; applicability | nothing at runtime (grep `operational_bindings\|binding_id` in runtime/, canon/gate: 0 hits) | none | 0 | none | — | No | SPEC-04 design artefact; 266/291 literally `status_reason: not reviewed` / `experimental; not reviewed` |
| **Compiled packs** (2) | 21 questions-with-defaults + checks + 28 pre-arbitrated conflicts + 6 limit lines | (a) `runtime/canon/packs.py` → `PlannerPrompt.system` (only a FixturePlanner / NoCallPlanner exists — no live model on `main`); (b) `canon/gate/doctrine.py` loads the 21 check lines; (c) the media-agency operator reads decision id + question + CHECK via BOOTSTRAP §2 | deterministic table lookup by NR → pack ids → verbatim `terse_injection_text` | runtime payload for the Cumin NR: 21,190 chars = 5,298 tokens (prefix + both packs); operator context: BOOTSTRAP command prints 4,520 chars = ~1,130 tokens (questions + checks only; the 6,185 chars of DEFAULT text, the 28 conflict rules and the limit lines are **not** printed by that command) | the model "edits a default, never composes from principle"; the gate then tests literal clauses | job record `canon.prefix_sha256`, `blueprint.check_lines`, 10 `*.gate.txt` GATE PASS | Case 003: R ✔ (sha matches), C ✔ (checks + questions; DEFAULTs UNKNOWN), U ✔ (check_lines rendered with pack vocabulary), D **partial** (typed VISUAL_SYSTEM subfields in every package: `surface_finish_per_key_object`, `implied_light_source`, `placement_zone`, `attention_order`), K ✘ for PA-D7 ("pass — 'the bowl on a noodle night' sells at a glance" — human: not an ad), Q ✘ (PA-D7 NOT-MECHANISED) | — |
| **Pack triggers** (28 cells) | which NR fields fire which pack ids | `packs.py select()`; `doctrine.py select_packs()` (mirror, compiled packs only); operator §4 | table lookup | 0 (metadata) | selects packs; records gaps | `canon.packs_selected` (10) / `packs_injected` (2) / `missing_domains` (8) in JOB.yaml | Case 003: ✔ fired correctly, incl. `commercial_communication` via `advertising_acceptance_intent` | — |
| **Injection prefix v1** (328 tokens) | how to treat DEFAULT / CONFLICT / CHECK; marker legend | `packs.py` prepends it to every payload | constant | 1,311 chars | frames doctrine as "decision already made" | payload bytes | Case 003: only if the operator read the payload (UNKNOWN — the job record shows sha + token count, not the text) | — |
| **CANON_CONTEXT spec + example** | a hand-packaged per-brief context shape (R1–R8 rules) | nobody (no importer) | — | 0 | — | — | No | superseded design; `CANON-SHAPE-v1 §5` keeps its rules by reference |
| **Gate vocab / check registry** | regex vocabularies for 10 partial pre-dispatch checks + LIMIT-TEXT; 11 checks declared NOT_MECHANISED with reasons | `canon/gate/run_gate.py` — operator QA-CHECKLIST A1 / D1 | loads packs at runtime | 0 to the model; a report to the operator | blocks dispatch on LIMIT-TEXT / DISPATCH-* / CA-D2 clause 2 / ERROR | `*.gate.txt` | Case 003: ✔ ran ×10 pre-dispatch, all PASS; 11 of 21 doctrine ids NOT-MECHANISED on every report | — |
| **Templates** (`templates.py`) | an accepted plan as a slot-filled reusable asset; exact-identity match on one sha | nothing yet — no accepted job has been promoted; case 003 `template_status: none` | exact sha match, no search | 0 | would skip the reasoning pass | — | No (001's template lives as `ACCEPTED-TEMPLATE.yaml` in the case, not in the runtime store) | authorised USD-0 build under C-10 |
| **KIND-NR binding** (9 kinds) | modality / operation / advertising_intent per deliverable kind | `normalize.py` | row lookup by `deliverable_request.kind` | 0 | determines which packs fire (`multi_shot_story` → video/generate/advertising) | recomputed: Cumin `brief.job.json` → video/generate | Case 003 ✔ | — |
| **Q&A bank** (1,028) | grounded, ungraded questions+answers per source, incl. 'application' items | nobody at runtime (`packs.py`: "no Q&A corpus") | — | 0 | — | — | No | a companion asset "so a claim like 'Canon knows what this book teaches' can be checked" |

---

## 2. The retrieval mechanism as it exists in code

**OBSERVED** — `runtime/canon/normalize.py @ a8754fe` and `runtime/canon/packs.py @ 76c3059`:

1. `normalize(job)` is a pure function of the PRODUCTION-JOB-v1 dict plus `KIND-NR-BINDING-v0.yaml`. It reads `deliverable_request.kind` → a binding row (modality R05, requested_operation R01, `advertising_acceptance_intent`), derives `text_requirements` from `exact_text_strings[]` (script detected by Unicode names), `entities` from `reference_assets[].role ∈ {product, logo, prior_creative}` or `subject.entity ∈ {product, packshot}`, `language_topology` from `brief.language` or a non-Latin script, `market` from `brief.market`, and two ambiguity markers. No model. No text of the brief is read semantically — the `brief` field contributes only `language` and `market`.
2. `CanonCorpus.select(nr)`: universal packs (2) + `modality_base_packs[nr.modality]` (or the union under the uncertainty rule) + the four `conditional_packs` evaluated by `_conditional_fires` on NR fields (`text_requirements` non-empty; `facets.product_entity_present`; `language_topology or market == "IN"`; `acceptance_intent.advertising`). Any condition string the code cannot evaluate raises `Refusal(CANON_TRIGGER_TABLE_HOLE)`.
3. `CanonCorpus.inject(nr)`: payload = system block (v1) + (audio only) coverage-gap notice + each selected pack's `terse_injection_text` **if and only if** its `corpus_digest == fingerprints.accepted_canon.combined_digest` from `CANON-CORPUS-INDEX.yaml`. Selected-but-uncompiled packs go to `gap_pack_ids`; `canon_gap=True`; `missing_domain` string; **the job continues**. One sha256 over the payload. Token ceiling 45,000.
4. Downstream: `runtime/spec/compile.py` → `planner_seam.build_prompt()` puts `canon.payload` in `PlannerPrompt.system`. The only planners on `main` are `NoCallPlanner` (refuses) and `FixturePlanner` (looks up a recorded response by prompt sha; 5 fixtures in `runtime/fixtures/planner/`). **No live model receives the payload from `runtime/` on `main`** (grep for any provider SDK in `runtime/**/*.py`: 0 hits).

Therefore: **deterministic lookup by kind→NR fields; no keyword, no embeddings, no ranking, no per-request reading of the 37 sources.** Retrieval over full knowledge existed once — CANON-015 (`8115400`, BM25 per object kind, diversity caps; reachable only via `origin/claude/canon-retrieval-maturity-lwwaey`) — and was dispositioned SUPERSEDE / SALVAGE-OFFLINE in `COMPILED-PACK-CONTRACT-v0.1.md §9`; `tests/test_canon_retrieval.py @ 6889282` is explicitly a "SALVAGE-OFFLINE remnant" keeping one boundary test. The EVAL-037 recount (`python3 canon/validation/recount_eval037_retrieval.py`, run here) reproduces why: 3 searches, 0 reads, 4,082,082 bytes returned, 962 HOLD vs 411 accepted items.

**Fraction of accepted Canon reachable by any production code path (OBSERVED):**

| Measure | Reachable | Total | % |
|---|---|---|---|
| SK objects cited in a compiled pack | 104 | 1,300 | **8.0%** |
| Cited claim bytes (pack `counts.cited_claim_bytes`) | 44,644 | 7,068,257 | **0.63%** |
| Sources with ≥1 cited object | 10 | 37 | 27% |
| Bytes of those 10 sources (generous upper bound) | 1,693,642 | 7,068,257 | 24.0% |
| Domains touched by the two packs | 11 | 56 | 20% |
| Packs compiled | 2 | 10 | 20% |

By LIVE37 contributor mass, the uncompiled `commercial_communication` pack alone spans 15 sources / 555 SK / 3.0 MB — the deepest pack in the map (12 independent origins) and the one every advertising job fires.

**Is `commercial_communication` compiled, triggerable, or injectable?** Triggerable: yes — `pack-triggers-v0.yaml @ 515b6db`:

```
conditional_packs:
  - condition: advertising_acceptance_intent
    nr_field: acceptance_intent
    pack: commercial_communication
```
and 8 of 9 `KIND-NR-BINDING` kinds set `advertising_acceptance_intent: true`, so it fires on essentially every job. Compiled: **no** (`glob("PACK-*-v0.yaml")` finds two files). Injectable: **no** — `packs.py` injects only accepted compiled packs, and `doctrine.py` `EXPECTED_DECISIONS` hard-codes exactly `{"product_appearance": 10, "composition_and_attention": 11}`, so the gate cannot even load a third pack without a code change. The trigger table's own `notes:` say it "selects packs; it asserts nothing about their quality", and its token budget row for `commercial_communication: 4096` is "the uncompiled default envelope". Controller ruling C-10 (`ae5ba7d`): "Do NOT compile the remaining eight packs unless a real runtime failure later demands one."

---

## 3. Does the media-agency skill read Canon at all?

**OBSERVED** (`.claude/skills/media-agency/* @ 3488bdb`, committed 15 Sep 13:56 IST; the Cumin job opened 15 Sep 13:17 UTC = 18:47 IST, so the skill was in force):

| Step | File(s) read | Bytes | Evidence it happened in case 003 |
|---|---|---|---|
| BOOTSTRAP §2 | `canon/CANON-SHAPE-v1.md` §4–§5; `canon/packs/pack-triggers-v0.yaml` (9,801 B); a python one-liner printing `decision_id | question` + `CHECK:` for both packs (4,520 chars ≈ 1,130 tokens) | ≈ 14 KB + the shape doc excerpt | `JOB.yaml.skill_version 7e324b0…`, `production_base_sha 3bb9a3c` |
| Workflow §4 | `runtime.canon.normalize` + `lookup` on `brief.job.json` → prints selected/injected/gaps/prefix sha/tokens/check-id count — **not the payload text** | 0 bytes of doctrine text printed | `canon.prefix_sha256 4d7a5b27…` in JOB.yaml; recomputed here: identical sha, 5,298 tokens, 21 check ids, 10 selected / 2 injected / 8 gaps |
| Workflow §5 | render `PA-D1..D10`, `CA-D1..D11` check lines by id against the blueprint | — | `blueprint.check_lines` has 21 entries, all `pass`/`n-a`, `deviations: []` |
| QA A1 / D1 | `canon/gate/run_gate.py pre/post` | — | 10 `*.gate.txt`, all `GATE PASS`; CA-D7 non-blocking FAIL on single-shot clips |

So the skill reads Canon **through the compiled layer only**: shape doc, trigger table, the two packs' questions and checks, and the gate. It does not read `canon/knowledge/current/**`, the Q&A bank, the ontology, or the bindings; nothing in SKILL/BOOTSTRAP/WORKFLOW names them. The skill's own red-flag row says "No Canon pack covers this brief" → "Run the trigger table … `composition_and_attention` fires on every still/video; `product_appearance` fires on any product entity" — it tells the operator what fires, not what is missing.

**Is the runtime injection used or bypassed?** Both, precisely: the *lookup* is used (sha proves it); the *injection into a reasoning model* is bypassed, because in this workflow the reasoning model is the operator session itself, and the workflow hands it questions + CHECK lines rather than the 21,190-char payload. Whether the operator additionally opened `PACK-*.yaml` to read DEFAULT text is **UNKNOWN** (not recorded). INFERENCE from the job record: the blueprint's `brand_world` ("one soft window source camera-left … matte surfaces everywhere except the glaze (PA-D1)") and `PROMPTS.yaml` line 4 ("PA-D4 one source; PA-D1 finishes; CA-D2 zones") show decision-level vocabulary, consistent with having read at least the questions/checks; the DEFAULTs' distinctive content (e.g. Murch's Rule of Six weights, "zones are regions, never grids") does not appear in the record.

---

## 4. Which Canon knowledge would have prevented each Cumin failure — and how far it got

Human verdicts (OBSERVED, `de1f978:…/JOB.yaml versions[]` and `1de2b37:production-learning/cases/CUMINCO-CHOPSTICKS-003/HUMAN-VERDICTS.yaml`): V1 "the text is coming on figures … random audio"; V2 "did cannon say nothing about product positioning? the closing shot should have cumin product and final caption. it does not look like ad at all. the opening is missing too. canon had this knowledge. how's that possible?"; V3 "the voices are overlapping".

Eight states: 1 exists → 2 retrieved → 3 in context → 4 understood → 5 changed decision → 6 correct → 7 survived → 8 QA-detected.

| Failure | Canon knowledge that addresses it (`path @ sha`, ≤2 lines each) | State reached | Why it stopped |
|---|---|---|---|
| **Tutorial, not an ad** (HD-06) | `sk_abcd_0010` `google-abcd-video-ads/source-knowledge.yaml @ 711163e` — "Brand early, often, and richly" / "Make use of a broad range of branding elements to show and tell viewers who you are". `sk_abcd_0013` (same file) — "Draw on all your branding assets … product shots, pack shots, in situ branding, graphic elements, voice-overs". `sk_hop_sa_0008` `hopkins-scientific-advertising-ch1-7/… @ dc64ff8` — "Advertising is salesmanship carried out in print … every advertising question should therefore be answered by the salesman's standards". `sk_ogl_c003_0010` `ogilvy-ch2-… @ dc64ff8` — "Unless your advertising contains a big idea, it will pass like a ship in the night." Concept: `scs_abcd_001 abcd_four_principle_execution_framework` (decision_framework, 6 members). QA: `qa_abcd_0010` (application item: "brings the logo up only at the very end … what is wrong") | **1 (exists)**. Trigger fired (`commercial_communication` in `packs_selected`), nothing retrieved (`selected_uncompiled`), gap recorded at 13:23Z *before* any dispatch | Pack not compiled (C-10); `packs.py` continues on gap by design; skill §4 says "record the gap … only if the production actually fails for want of it" — i.e. after the human sees it |
| **No opening** (HD-05) | `sk_abcd_0005` — "Hook and sustain attention with an immersive story" / "Drop viewers in from the start". `sk_abcd_0007` — "You can start your ad in the middle of the action, or open with a close-up … Start big!". `sk_abcd_0006` — "Get to the heart of the story faster, and use engaging pacing and tight framing". `sk_ogx_0004` `ogilvy-beyond-ch2` — "a headline which does not sell the product wastes ninety per cent of the money" (print-era; C09 is `critical_limited`) | **1 (exists)** | Same pack; note the skill's blueprint *has* a `hook` field and the operator filled it ("A noodle slips back into the bowl in the first second") — a field without doctrine behind it produced a hook the human did not see as an opening |
| **Weak product role** (HD-04) | `sk_abcd_0010`, `sk_abcd_0013` as above; `sk_abcd_0026 full_funnel_objective_weighting` ("finish with the product" per the job's own gap note). Compiled and *in context*: **PA-D7** `PACK-product_appearance-v0.yaml @ 97ac482` — "Treat the picture as a salesman that must earn its space (sk_hop_sa_0026); … CHECK: State in one line what the hero image sells at a glance; if that line needs the body copy, the image fails." | PA-D7: **4 (understood)** — operator wrote "PA-D7: pass — 'the bowl on a noodle night' sells at a glance"; **5/6 ✘** (SD-07: "the operator rendered PA-D7 pass on a thin line"); **8 ✘** — `predispatch.py NOT_MECHANISED_PRE["PA-D7-check"]`: "the decisive check is a semantic judgment … remains a human / blueprint-model check". ABCD items: **1** | The only compiled advertising decision is a one-line self-attested check with no mechanical test; the rest is uncompiled |
| **Weak close / CTA** | `sk_abcd_0019` — "Ask them to take action and give clear, concise direction that's easy to follow"; `sk_abcd_0020` — "Be intentional and add a CTA to drive a specific objective. Say what you'd like viewers to do."; `sk_abcd_0021` — "Reinforce your onscreen CTA with voice-over to ensure the next step is clear". `sk_sb_c003_0011` `miller-storybrand-sb7/… @ dc64ff8` — "CUSTOMERS DO NOT TAKE ACTION UNLESS THEY ARE CHALLENGED TO TAKE ACTION". Binding `bnd_abcd_003` (target_type `evaluation`, `diagnoses`, refs 0019–0021, `proposed`, no target_path) | **1 (exists)** | Same pack; the blueprint `cta_placement` = "brand line 'Cumin Co.' bottom-centre of the end beat … no other CTA" — a placement, not a Direction; V3 added "Ramen night at home. Cumin Co." spoken close citing "ABCD 'see and say'" (`sk_abcd_0012`) — the *first* moment any ABCD item reached state 5, after two rejections |
| **Text over people** (HD-01/03, DF-04) | Searched all 37 sources for subject-obstruction / copy-over-figure knowledge (regex over label+claim+terms): **0 relevant hits**. Adjacent only: `sk_abcd_0008` — "Reinforce your message with audio and text. Avoid competing elements."; `sk_wcag_0001` `w3c-wcag22-… @ 3aac324` — "contrast ratio of at least 4.5:1". CA-D1 (in context) — "no two cues compete for one beat" | **0 — does not exist in Canon** as a rule; CA-D1/abcd_0008 are at most 4 (understood) and did not bind the compositor | Content gap, not retrieval. Was caught by the human at V1 and by an engineering candidate (`WALL_OBSTRUCTION_GATE`, `SD-04`) — the right home per the skill's own five-authority split |
| **Voice casting** (26 takes, 5 rounds; RO-03/04/05) | Searched: **0 hits** for voice casting / narrator / timbre / accent; 1 ontology term matches "narrat" (`t_ctg_0066 trojan_horse_narrative`, unrelated). Adjacent: `sk_abcd_0014` — "YouTube is almost entirely a sound-on experience"; `sk_abcd_0012`/`0021` (VO brand mention). Audio modality: `modality_base_packs.audio: []` and the coverage-gap notice: "no accepted Canon source covers audio production" | **0 — does not exist** | Content gap; DF-08 (overlap) is engineering, promoted as `check_vo_schedule` |

**Summary of the six:** three failures (tutorial-not-ad, no opening, weak CTA) had knowledge at state 1 blocked at 2 by the two-pack policy; one (product role) had a compiled decision that reached state 4 and failed at 5–6 with no mechanical check; two (text over people, voice casting) have no Canon knowledge at all. The user's "canon had this knowledge. how's that possible?" is correct for four of six and the job record's own `canon_gaps` entry names the mechanism exactly (`LEARNING-PACKET.yaml`: "the relevant pack was never injected").

---

## 5. Representation critique — can objective → media type → required decisions → failure modes → knowledge be traversed?

**OBSERVED structure of the edges that exist:**

- objective → media type: `KIND-NR-BINDING` (kind → modality/operation/advertising flag). Adequate for 9 kinds; no `objective` (awareness/consideration/action) field exists anywhere in the NR, although `sk_abcd_0023..0026` (objective-weighted ABCDs) and `scs_abcd_002` are keyed on exactly that.
- media type → packs: `pack-triggers-v0.yaml` — by modality + 4 NR facts. Explicit, total, tested.
- pack → required decisions: only for 2 packs (`decisions[]` with `feeds_sections`). For the other 8 there is no decision list, only a domain list (`LIVE37 packs[].domains`) and a `domain-system-map-v0.yaml`.
- decision → failure mode: `check` text (21 lines) and `failure_ontology_refs` on bindings (a field, present on all 291 bindings, content not audited here). No edge from a *check* back to an ontology `problem` term.
- failure mode → knowledge: SK `source_stated_problems` / `remedies` (1,260 / 1,289) and ontology `problem`/`remedy` terms (381/382) — but **0 of 422 relationships cross a source boundary** (computed), and the 60 cross-source candidates are all `proposed`. So "the same failure family" cannot be traversed across books.

**Missing edges, concretely:**

1. `acceptance_intent.advertising` → `commercial_communication` → *nothing*: the edge ends at a pack id with no decisions. Consequence: `compile.py._gate_requirements` emits the string "canon gap: no compiled pack answers commercial_communication …" — a warning, not a decision list.
2. No edge from NR `temporal_structure` / `deliverable_set.kind == multi_shot_story` to an *ad structure* requirement (opening, product presence, close). `scs_abcd_001` encodes it as a 6-member decision framework; nothing maps it to a `feeds_sections` slot.
3. No `objective` in the NR grammar, so `scs_abcd_002 objective_weighted_abcds` has nothing to bind to.
4. `bnd_abcd_001..009`: 5 `evaluation`, 2 `benchmark`, 2 `governance`, **0 `creative_ir`, 0 `production`**, all `target_path: None`. The ABCD source has no binding pointing at any producible field.
5. Text-over-subject and voice/register: no SK, no term, no domain row (audio: "zero packs and zero accepted sources").
6. `PA-D7` cites only `sk_hop_sa_0026/0035` (1926 print) — the one compiled advertising decision has a `CULTURE-BOUND|MEDIUM-UNTESTED` marker and no video-era source behind it, although `google-abcd` is accepted and marked `platform_contingent`.

**Recount of the 28-Aug review claim** ("all 127 operational bindings are unreviewed, 89 of 127 point at no schema field"): OBSERVED at `e6474dc` (last main commit on 28 Aug, extracted with `git archive`): 19 sources, 580 SK, **127 bindings, 89 with no `target_path`**, status 119 proposed / 8 production_candidate — the review's numbers reproduce exactly. At HEAD: **291 bindings, 249 with no `target_path` (85.6%, up from 70.1%)**, 266 `proposed` (231 of them with `status_reason` "not reviewed"/"experimental; not reviewed"), 25 `production_candidate` all with reason "Production IR does not exist". So the claim is **still true and has grown**: not one binding has been reviewed since. The review's "fewer than 7% of remedies executable by a generative pipeline" recomputes at HEAD as 11/382 remedy terms tagged `generative_respecification` (2.9%) and 19/382 `deterministic_composite` (5.0%); `human_edit` 221 (58%), `physical_production` 93, `unknown` 76. Note the tag lives on ontology remedy *terms* (`ontology-mappings.yaml`), not on SK remedies as the task prompt assumed.

---

## 6. Prompt / instruction architecture — in what FORM does Canon reach a model?

Three forms exist on disk; only one reaches anything:

| Form | Where | Shape | Reaches a model? |
|---|---|---|---|
| **Compiled decision** (questions-with-defaults) | `PACK-*.yaml terse_injection_text` | `PA-Dn [markers] / Q: … / DEFAULT: imperative, id-cited / CHECK: yes-no over own output`, then `CF-nn` conflict rules, then `PACK LIMITS` | Yes via `packs.py` payload (no live consumer on main); partially via the operator (Q + CHECK only) |
| **SourceKnowledge claim** | `source-knowledge.yaml` | claim + mechanism + scope + caveats + problems/remedies + examples + relations + evidence + provenance (~330 chars claim, ~5 KB per object) | No |
| **Q&A item** | `canon/qa/canon-014/*-qa-bank.yaml` | question (often a scenario), answer (~900 chars, source-scoped, states what is *not* wrong), support quote, confounders, `requires_application` | No (`packs.py`: "no Q&A corpus"; EVAL-037 saw them only through search) |
| **Oracle context** (prose) | `canon/experiments/v1/value-gate/oracle-contexts/*.md` | 3–4 concept-system paragraphs, 2.5–3.7 KB | No (experiment artefact) |

**Comparison for consumability at decision time** (INFERENCE from the artefacts; no experiment on main measures this):

- The compiled form is *constraint + procedure*: it presupposes the decision has already been posed ("Where may the highlight sit on each glossy surface?") and asks the model to accept or override. Its strength is O(1) size and a mechanical check; its weakness is visible in case 003: PA-D7's CHECK ("state in one line what the hero image sells at a glance") is a self-attestation that a weak or hurried reasoner passes trivially, and its DEFAULT carries 1926 print doctrine into a 2026 Reels film with a `MEDIUM-UNTESTED` marker the legend tells the model to "assume neither way".
- The Q&A form is *example + counter-example*: `qa_abcd_0010` describes almost exactly the Cumin V2 structure ("brings the logo up only at the very end … closes on a 'Buy now' end card") and answers with the three ABCD principles missed *and* the one that is not a fault. For an LLM at decision time, that is a worked negative example with scope discipline — arguably the most directly transferable form in the corpus for the "does this look like an ad?" judgement — and it is the only form explicitly excluded from every production path ("grounded, ungraded, uncalibrated"; 688 of its accepted-source items still flagged `source_status: hold`).
- The SK form is *evidence*: right for compilation and audit, wrong for injection (5 KB per object; 1,300 objects).
- The prefix (INJECTION-PREFIX-v1) is *meta-instruction* about how to treat markers; 328 tokens that presuppose the packs exist.

The retro-test `EVAL-038-RETRO-TEST-PILOT-001.md @ 4d68b82` shows the compiled form working where its domain matches (lighting/composition defects of PILOT-001); the Cumin case shows it inert where the domain is advertising structure.

---

## 7. Red-team Q6 — is the two-pack strategy making most of Canon inert? Quantified

**OBSERVED:**

- 2/10 packs compiled → 8/10 fire as gaps on a typical advertising video (Cumin: 10 selected, 2 injected).
- 104/1,300 SK (8.0%), 44.6 KB / 7.07 MB cited (0.63%), 10/37 sources, 11/56 domains reachable.
- The largest single SK domain label in the accepted corpus is `advertising` (223 mentions), followed by `brand_communication` (62), `marketing` (49), `print_advertising` (48), `advertising_concept_development` (41), `copywriting` (37) — **none** of it compiled. The compiled packs draw from `photographic_lighting`, `film_editing`, `photography`, `product_rendering`.
- Demand-weighted priority (`PROPOSED-demand-weighted-pack-priority-v1.md @ da7da99`): `commercial_communication` demanded by 53/54 briefs (P2, "deepest pack … the highest-leverage moment of every video brief leans on it"); `composition_and_attention` demanded by 15/54 (P4, "strongest supply relative to recorded demand"). The two compiled packs are the two *lowest-demand* packs in Canon's own ranking (product_appearance 15/54, composition 15/54).
- Of the 21 compiled check lines, the pre-dispatch gate mechanises 10 as *partial* literal-clause tests and 11 are `NOT_MECHANISED`; post-draw mechanises 1 (CA-D6) + LIMIT-TEXT. In case 003 every doctrine row that could be measured passed on every version, and every rejection landed on an unmeasured dimension (case README: "every rejection landed on a dimension no gate measured").
- EVAL-038 (`PROPOSED-EVAL-038-CONCLUSION.md @ 12b91ae`) already reported the packs "made weak models disciplined. They did not make them good"; the blind notes cite "thin copy, no dialogue … generic concepts" — commercial-communication failures, with the commercial pack uncompiled.

**Verdict (INFERENCE):** yes. The policy is not "compile what production needs"; it is "compile two pilots, then wait for a real runtime failure" (C-10), and the first real runtime failure arrived within a day of the operator going live, in the exact pack the demand analysis ranked P2 and every advertising job fires. The inertness is structural: the runtime is designed to continue silently on a gap (`canon_gap` is metadata; `_gate_requirements` adds a sentence), the skill defers gap recording until after a human rejection, and the gate cannot load a third pack without editing `EXPECTED_DECISIONS`. Canon is not inert because retrieval is weak — the lookup is correct and provably ran — but because 92% of the corpus has no compiled form to be looked up.

**HYPOTHESIS (not testable from committed bytes):** even a compiled `commercial_communication` pack in the current questions-with-defaults form would have needed a *structural* check (brand present by beat n; product hero shot present; Direction present) to have blocked V1/V2; a self-attested CHECK like PA-D7's would have been rendered "pass" the same way. The job's own candidate `AD_STRUCTURE_MINIMUM` (blueprint fields shown to the human before dispatch) is the cheapest version of that.

---

## Findings ranked

1. **The Cumin failure was a compile-policy failure, not a retrieval failure.** Lookup ran and matched (`prefix_sha256 4d7a5b27…` recomputed identical); `commercial_communication` fired via `advertising_acceptance_intent`; it is uncompiled by ruling C-10; `packs.py` continued by design. Knowledge for 3 of 6 failures sat at state 1 (`sk_abcd_0005/0006/0007/0010/0013/0019/0020/0021`, `sk_ogl_c003_0010`, `sk_sb_c003_0011`). OBSERVED.
2. **Two of the six failures have no Canon knowledge at all** (text-over-subject obstruction, voice casting/register; audio has zero sources). Compiling packs would not have helped; these belong to engineering gates and the empirical layer — which is where the case put them. OBSERVED (regex search over all 1,300 objects and 1,191 terms).
3. **8.0% of SK / 0.63% of bytes / 10 of 37 sources / 11 of 56 domains are reachable by any production path; the compiled two are Canon's own two lowest-demand packs.** OBSERVED.
4. **The operator never sees the pack DEFAULTs or conflict rules by the documented path.** BOOTSTRAP §2 prints question + CHECK (4,520 chars); workflow §4 prints sha and counts. The 6,185 chars of DEFAULT text and 28 CF rules reach the operator only if it opens the YAML, which is not recorded. UNKNOWN whether it did; OBSERVED that the documented commands do not print them.
5. **PA-D7 is the only compiled advertising decision and is self-attested**: NOT_MECHANISED in both gates; operator rendered "pass"; human rejected on exactly that dimension. OBSERVED.
6. **Bindings are still 100% unreviewed and now 85.6% target-less** (291; 249 no `target_path`; 28-Aug figures 127/89 reproduce exactly at `e6474dc`). Nothing in runtime/ or the gate reads a binding. OBSERVED.
7. **Ontology has zero cross-source relationships** (0/422); the 60 join candidates are all `proposed`; the failure-family traversal the SPEC-05 vocabulary promises does not exist across books. OBSERVED.
8. **Stale flags on the Q&A companion corpus**: README says "108 accepted / 920 hold"; corpus index says 796/232; 688 items of accepted sources still carry `source_status: hold` inside the banks (e.g. every `google-abcd` item). Any future consumer keyed on that field would refuse accepted material. OBSERVED.
9. **`canon/context/**` and `canon/ontology/**` have no code consumer**; `CANON_CONTEXT` survives only as rules cited by reference in `CANON-SHAPE-v1 §5`. OBSERVED.
10. **The runtime's "injection" has never reached a live model on `main`**: only `NoCallPlanner`/`FixturePlanner` (5 fixtures). The receipt vocabulary retired by CANON-SHAPE-v1 §5 is still in both packs' terse text (runtime records a notice). OBSERVED.
11. **The retro-test and EVAL-038 already showed the shape of this outcome** (packs enforce discipline in lighting/composition; lose on creative substance) three weeks before the first real job. OBSERVED.

## Open questions / unknowns

- **UNKNOWN**: whether the operator session read `PACK-*.yaml` DEFAULT/conflict text or only the BOOTSTRAP print. Not recorded in the job branch; the skill does not require recording it.
- **UNKNOWN**: whether a compiled `commercial_communication` pack in the present form would have changed the V1/V2 blueprint — no experiment exists; EVAL-038 suggests discipline ≠ quality.
- **UNKNOWN**: the intended consumer of the 291 bindings now that Production IR "does not exist" (their own status_reason) and the runtime uses PRODUCTION-JOB-v1/NR instead of SPEC-01 Creative IR; 24 of 42 `creative_ir` target paths name SPEC-01 leaves, but SPEC-01 is not what the runtime reads.
- **UNKNOWN**: why `google-abcd` bindings are all `evaluation`/`benchmark`/`governance` with no `creative_ir`/`production` target when the source is the only feed-native video source in Canon.
- **Conflict to record**: `canon/qa/canon-014/README.md` (108/920) vs `CANON-CORPUS-INDEX.yaml` (796/232) vs the banks' own `source_status` fields (108 say accepted). The index is right about source status; the banks and README are stale.
- **Conflict to record**: `pack-triggers-v0.yaml` header says pack ids come from `CANON-V1-LIVE24-COVERAGE.yaml`; the live map is LIVE37. Same ten ids, but the citation is stale.
- Not examined: cases 001/002 job records in depth (this council read their case READMEs via the skill only); the MF predecessor's Canon usage; whether any worktree carries an uncommitted third pack (`git worktree list` not enumerated here).
