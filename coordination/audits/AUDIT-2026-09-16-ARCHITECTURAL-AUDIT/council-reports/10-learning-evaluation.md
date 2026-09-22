# AGENT 10 — Evaluation / Production-learning council

Read-only audit of the production-learning mechanism, failure taxonomy, acceptance contracts, memory systems, experimental design and the runtime empirical-memory loop. MI main verified at `3bb9a3c3da484e43d4d54ae20543d1d246769ac6`; PR #103 branch `work/agency-sync-2026-09-16` @ `1de2b37` (OPEN, not merged — `gh pr view 103` state OPEN); Cumin raw evidence @ `de1f978`; job-branch head `1aea4d2` (sync-mark commit touching 4 fields of JOB.yaml only).

Labels: **OBSERVED** (read in the artifact named), **COMPUTED** (command shown), **INFERENCE**, **HYPOTHESIS**, **UNKNOWN**.

---

## 0. Findings ranked

1. **The learning loop is a bookkeeping loop, not a control loop.** `check_case.py` validates 30-odd schema/provenance properties and zero substance properties (§1.2). All three cases PASS it (COMPUTED). Nothing in the repo checks that a promoted item became code, that a candidate's promotion condition was ever re-evaluated, or that a defect class already recorded in an earlier case is cross-referenced when it recurs. Case 003's queue carries no reference to any case-002 candidate even where it re-derives one (COMPUTED: `git show 1de2b37:…/CUMINCO-CHOPSTICKS-003/PROMOTION-QUEUE.yaml | grep -i "002|TEXT_OVER_IMAGERY|SUBJECT_AWARE|SINGLE_VOICE|SPEAKER_MICRO"` → no hits).
2. **Propagation succeeded exactly where a learning became a deterministic gate with a caller, and nowhere else.** Case 001's eight `promoted_now` items are code with tests on main (`runtime/compositor/gates.py`, `tokens.py`, `runtime/loop/frame_hygiene.py`, `runtime/execute/pools.py`, `provider_errors.py` — commits 344f517, c6c39b8, dcddedb, fc806c3) and the Cumin job tool imported and called five of them (`de1f978:agency/jobs/…/tools/compose.py:30-31,174-352`). Case 002's five `promoted_now` items are prose in `.claude/skills/media-agency/**` (commit 3488bdb) and no runtime code (COMPUTED: `grep -rn -E "QA_COVERAGE_ENFORCEMENT|FORMAT_SPECIFIC_REVALIDATION|CROSS_CLIP_VOICE|DESIGN_REUSE_PROVENANCE|PAID_PRODUCTION_PREFLIGHT" runtime/ --include='*.py'` → 0 hits). Case 003's one promoted gate `check_vo_schedule` has no caller anywhere on the PR branch (COMPUTED: `git grep -n check_vo_schedule 1de2b37` → gates.py + its test only).
3. **Every case-003 rejection that recurred from 001/002 stopped at the same place: a candidate pattern with an unmet promotion condition, or a prose row that the producing agent self-marked PASS.** Text-over-subject: 002 candidate `TEXT_OVER_IMAGERY_CONDITIONAL` (condition "an obstruction check exists in the compositor") → never built → 003 `CF2: PASS on 9:16 (copy on empty wall, nothing over bowl/hands/faces)` written by the operator (`de1f978:…/JOB.yaml:326`) → the human: "the text is coming on figures". Robotic voice: 001 `RO-05` recorded with `routing_authority: none` by design → 003 plan's first voice micro-qualification route is again `sarvam-bulbul-v3 vs elevenlabs-v3-direct` (`JOB.yaml:247`) → 8 Sarvam takes rejected "consistent with case 001 RO-05" (003 `ROUTE-OBSERVATIONS.yaml RO-04`).
4. **The project's taxonomy cannot express the failure it keeps having.** Three separate vocabularies coexist (3 defect classes; 11 root-cause classes; 10 skill defect classes) and none has a slot for "knowledge existed and was not retrieved", "the operator's own check line was wrong", "no one owned the stop decision", or "learning recorded but not propagated". Case 002's `known_defect_classes_that_recurred` is the closest thing to K13 and it is filed as `QA_COVERAGE_ENFORCEMENT` (a workflow-bypass, K12). Internal inconsistencies (COMPUTED, §3.1): case 001 states `media_model_failures_that_reached_the_controller: 0` while its REVISION-TRACE codes two Controller-observed defects `model_generation` / `model_audio`; case 003 states 5 pipeline failures reached the human while its rows carry 6 (`SD-09 reached_human: true`).
5. **Humans reject on criteria the acceptance contracts never name.** Strict computation (§4.3): 3 of 42 rejection reasons across the three cases map to a pre-declared, job-specific acceptance criterion (7 %); 14 of 42 (33 %) under a lenient reading that counts partial matches and QA-checklist rows. Case 002 and case 003 had **no** acceptance contract at all (002 `PD-01`; 003 `JOB.yaml` has no such field and `JOB-TEMPLATE.yaml` defines none). The runtime's `ACCEPTANCE-STYLE-v0` bans, by design, every statement not decidable from the artifact alone — which is exactly the register the human uses ("does not look like an ad at all", "competent, not extraordinary").
6. **The runtime empirical-memory mechanism is not connected to production.** `runtime/store/` does not exist on main or in any of 20 worktrees (COMPUTED); the only OUTCOME-EVENT files are 8 battery results, all `dry_run: true`; `OutcomeStore.write` is reached only from `runtime/loop/driver.py` under the dry alpha chain; `runtime/ALPHA-1.md:145-149` says live dispatch does not exist. None of the three cases emitted an event; the job tools (`compose.py`, `dispatch.py` @ de1f978) import gates and `provider_errors`, never `memory`, `acceptance` or `templates`. `TemplateLibrary` holds zero templates.
7. **The evidence being generated cannot distinguish the hypotheses.** EVAL-037 varied "access to Canon" rather than "Canon in context" (Gemma FULL_CANON used it 0/18; unbounded Sonnet overflowed 16/18) and judged plans, not media. EVAL-038 ran weak+2-packs vs strong-alone (0/6, single reviewer, blinding scars biased against treatment) and never ran strong+packs. The one well-designed experiment (value-gate PROTOCOL.md: oracle vs length-matched generic control, two reviewers by unanimity, stratified position balance) was never executed (`FRESH_CONTROL_SESSION_REQUIRED`). Production learning is n = 3, one unblinded judge who authored the briefs, no control, and no constant across cases.
8. **The two diagnoses of "weak creative architecture" contradict each other and the contradiction was never reconciled.** Case 001 `not_promoted`: "no new Canon need was proven by this pilot: the failures were creative architecture, orchestration…"; case 002 `NO_CANON_CHANGE`: "not missing Canon knowledge"; case 003: `commercial_communication` is a Canon gap and "the real runtime failure C-10 waits for". The sync skill's class table forces this: a creative-direction failure is class 2 (candidate) unless someone calls it class 4 (Canon gap); there is no class for "knowledge exists in accepted Canon, was selected by the trigger table, and was not injected because 8 of 10 packs are uncompiled" — which is what `JOB.yaml canon:` shows (`packs_selected` 10, `packs_injected` 2, `missing_domains` 8).

---

## 1. Production-learning mechanism: designed vs executed

### 1.1 What a case contains (OBSERVED)

`production-learning/tools/check_case.py @ 3bb9a3c`, `REQUIRED_FILES`: `README.md, OUTCOME.yaml, REVISION-TRACE.yaml, TIME-AND-COST.yaml, ROUTE-OBSERVATIONS.yaml, SYSTEM-DEFECTS.yaml, HUMAN-VERDICTS.yaml, PROMOTION-QUEUE.yaml, EVIDENCE-MAP.md`; optional `ACCEPTED-TEMPLATE.yaml`. Schema label `PRODUCTION-LEARNING-CASE-v0` (no schema file exists; the validator is the schema). Upstream of a case: `agency/jobs/<id>/LEARNING-PACKET.yaml` (`AGENCY-LEARNING-PACKET-v1`, skill-owned) written by the operator at job close (`PRODUCTION-WORKFLOW.md §14`).

### 1.2 What `check_case.py` validates (OBSERVED, from the source; every check listed)

| Function | Checks | Kind |
|---|---|---|
| `_check_outcome` | keys `case_id, class, final_outcome, not_evidence_for, versions_produced, two_conclusions` present; `final_outcome ∈ {accepted, rejected, abandoned}`; accepted → `final_asset.{path,commit,sha256}` (64-hex), `accepted_version`, `accepted_by`; rejected/abandoned → `final_outcome_reason`; `two_conclusions.{final_quality, pipeline_efficiency_time_to_accepted_outcome}` non-empty; `template_status ∈ {reusable_candidate, job_specific, none}` consistent with file presence | schema |
| `_check_trace` | each version has 8 keys; `human_verdict ∈` 4-word vocab; every `root_cause_class ∈` the 11 classes; `elapsed.source` present; version list == OUTCOME's | schema |
| `_check_verdicts` | `evidence_class ∈ {chat_only…, file_backed…}`; versions match; verdict vocab | schema |
| `_check_routes` | `evidence_class == directional_production_observation`; `routing_authority == none`; `n` is int; `context` present | schema (enforces the *label*, not the *n*) |
| `_check_defects` | `class ∈ {media_model_failure, pipeline_failure, infrastructure_transient}`; `root_cause` present | schema |
| `_check_template` | `not_a_canon_rule: true`; `structure` non-empty; pacing `evidence_scope == this_accepted_template` | schema |
| `_check_queue` | four sections exist; `promoted_now[].where` non-empty; `candidate_patterns[].promotion_condition` non-empty | schema |
| `_check_time_cost` | one mechanical clock with `source` or `{value: null, reason}`; human estimate non-numeric; cost shape; CpAO shape; two integer counts; two conclusions | schema / honesty |
| `_check_evidence_map`, `_check_final_asset_bytes` | every `path @ commit` resolves under `--source-dir`; every hashed row's blob sha256 matches; the accepted asset's bytes hash to `OUTCOME.final_asset.sha256` and a matching hashed row exists; a supplied ref that does not resolve FAILS | provenance |

**Substance checks: none.** Specifically absent: (a) `promoted_now.where` is a free string — case 002's `where: "media-agency workflow (PR #99, /media-agency) — the deliverable path"` passes; (b) no check that a `promoted_now` id appears in any file under `runtime/` or has a test; (c) no check that a `candidate_patterns[].promotion_condition` has been evaluated, or that an id already queued by an earlier case is referenced rather than re-created; (d) no cross-case index at all — the validator takes one `--case`; (e) `n` is checked for type, never against the ledger; (f) `ROUTE-OBSERVATIONS` may say anything as long as it is labelled directional.

COMPUTED — the validator on all three cases:
```
python3 production-learning/tools/check_case.py --case production-learning/cases/UPWORK-INTRO-001 --pilot-ref f6ca66f
  → PASS 0 problem(s), 1 note (final_asset byte-verified)
python3 production-learning/tools/check_case.py --case production-learning/cases/UPWORK-PORTFOLIO-002 --source-ref b4b77fa --source-dir pilots/upwork-intro-video-2026-09-14
  → PASS 0 problem(s), 1 note
check_case.run(<case 003 extracted from 1de2b37>, 'de1f978…', 'agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001', root=MI)
  → PROBLEMS [] → PASS
```

### 1.3 How learning is meant to propagate (OBSERVED)

`.claude/skills/media-agency-sync/SKILL.md @ 3bb9a3c §3` — five classes, exactly one per item:

| Class | Destination | Enforcement surface |
|---|---|---|
| 1 PROMOTE — deterministic | `SYSTEM-DEFECTS.promoted_as` + `PROMOTION-QUEUE.promoted_now` + code/test in `runtime/compositor|loop|execute` on the integration branch | code + unittest |
| 2 CANDIDATE PATTERN | `PROMOTION-QUEUE.candidate_patterns` with `promotion_condition` (structure → `ACCEPTED-TEMPLATE.yaml`) | none (prose; re-read at the next bootstrap) |
| 3 DIRECTIONAL MODEL OBSERVATION | `ROUTE-OBSERVATIONS.yaml`, `routing_authority: none` | none by design ("human acceptance never enters the Registry") |
| 4 CANON GAP CANDIDATE | `PROMOTION-QUEUE.canon_gap_candidates` + PR text, "report only" | Controller decision under C-10 |
| 5 JOB-SPECIFIC | `not_promoted` | none |

Then "MAIN → this operator → real production → … → reviewed PR → MAIN → the next job's startup refresh" (`media-agency/SKILL.md` "The closed loop"). The "startup refresh" is `BOOTSTRAP.md §2`: the operator *reads* `production-learning/README.md + every cases/*/README.md, PROMOTION-QUEUE.yaml, ACCEPTED-TEMPLATE.yaml, ROUTE-OBSERVATIONS.yaml` and `PRODUCTION-WORKFLOW.md §3` asks it to list `template.learning_applied`. INFERENCE: propagation to the next job of anything in classes 2–4 is therefore an LLM reading YAML and deciding whether it applies — no lookup key, no gate, no test.

Class 1's test ("must name a deterministic check that would have caught it and a file where that check lives; if it cannot, it is class 2") makes class 1 unavailable to anything perceptual (voice, ad structure, obstruction judged by eye) — i.e. to the majority of what humans rejected on (§4).

### 1.4 What actually propagated for cases 001 and 002 by the time case 003 ran (main @ 3bb9a3c)

**Case 001 → runtime code (all eight `promoted_now`), OBSERVED at path@sha:**

| Pattern id (001 `PROMOTION-QUEUE.yaml`) | Became | Commit |
|---|---|---|
| TEXT_BOUNDS_GATE (SD-01) | `runtime/compositor/gates.py @ 3bb9a3c` §A `check_text_bounds` (line 44 marker "A. text bounds (SD-01)") + `runtime/tests/test_i_compositor_gates.py::TextBounds` | 344f517 (14 Sep) |
| CONTRAST_GATE (SD-02) | `gates.py` §B `check_contrast` (min ratio over every sample after fc806c3 blocker 1) | 344f517, fc806c3 |
| CROP_FIT_DECLARATION (SD-03) | `gates.py` §C `check_fit` | 344f517 |
| GEOMETRY_TOKENS (SD-04) | `runtime/compositor/tokens.py` `DesignTokens`; `gates.py` §D `check_geometry` | 344f517 |
| ELEMENT_DISJOINTNESS (SD-07) | `gates.py` §E `check_disjoint` | 344f517 |
| VIDEO_FRAME_TEXT_HYGIENE (SD-06) | `runtime/loop/frame_hygiene.py`; `driver.py:100`; `test_i_frame_hygiene.py` | c6c39b8 |
| PROVIDER_POOL_AVAILABILITY (SD-11) | `runtime/execute/pools.py`, `bridge.py:22` | dcddedb, fc806c3 |
| TRANSIENT_ERROR_CLASSIFICATION (SD-09/10) | `runtime/execute/provider_errors.py:3,64` | dcddedb |

And these reached production in 003: `de1f978:agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/tools/compose.py:30-31` imports `DesignTokens` and `gates`; calls `check_fit` (174, 197), `check_text_bounds` (234, 330, 332), `check_contrast` (235, 297, 318, 336, 339), `check_disjoint` (253, 348), `check_geometry` (352), `card_geometry` (325); `tools/dispatch.py:35` imports `provider_errors`. `frame_hygiene` and `pools` are **not** imported (frame text was judged by "human eye; Cloud Vision not invoked", `JOB.yaml:313-316`; pool liquidity was an attestation, `intake.questions_asked[2]`).

**Case 001 candidates / directional → prose only:**

| Item | Where it landed | Applied in 003? |
|---|---|---|
| SPEAKER_MICROQUALIFICATION (condition "≥ 2 more real productions") | `media-agency/SKILL.md:71`; `PRODUCTION-WORKFLOW.md:164-167`; `QA-CHECKLIST.md` A9 | Yes — `JOB.yaml template.learning_applied[0]`, `plan.micro_qualifications` (plate-H1 + clip-2, then voice). The condition was never re-evaluated by the 003 sync; 003 instead queues `VOICE_BY_EAR_FIRST`, a restatement, as a new candidate. |
| SERVICE_INTRO_TEMPLATE | `cases/UPWORK-INTRO-001/ACCEPTED-TEMPLATE.yaml` (`status: accepted_once`; not a `TEMPLATE-v0`) | `template.reused: none`; one number carried (`important_still_min_hold_s 3.3`) |
| TTAO_PRIMARY_KPI | adopted (PR #98 audit comment, per queue); `JOB-TEMPLATE.yaml ttao.*` | Yes (stamps present) — a measurement, not a bound |
| COMPLEX_PRODUCTION_EVENT | deferred; 002 says trigger MET; 003 does not mention it | No |
| RO-05 Sarvam long-read cadence | `QA-CHECKLIST.md:80` D10 "long narration is not accepted on transcript alone (RO-05)" | Listed in `learning_applied[1]` with the rationalisation "VO here is ≤ 5 short lines"; Sarvam re-tried ×8, rejected |

**Case 002 → prose only (all five `promoted_now`, commit 3488bdb, 15 Sep 13:56 IST, i.e. ~35 min after 002's case-index commit 022dfab):**

| Id | Kind in 002 queue | Landed at |
|---|---|---|
| QA_COVERAGE_ENFORCEMENT | production_system_requirement | `SKILL.md:100-102` (one sentence) |
| FORMAT_SPECIFIC_REVALIDATION | process_requirement | `SKILL.md:86-89`; `PRODUCTION-WORKFLOW.md:151, 244-248`; `QA-CHECKLIST.md` §C-final CF1–CF5; `JOB-TEMPLATE.yaml:148` |
| PAID_PRODUCTION_PREFLIGHT | process_requirement | `SKILL.md:102-103`; workflow §8 |
| CROSS_CLIP_VOICE_CONTINUITY | qa_requirement | `SKILL.md:90-93`; `QA-CHECKLIST.md:84` D14; `JOB-TEMPLATE.yaml:150` |
| REJECTED_DESIGN_REUSE → renamed DESIGN_REUSE_PROVENANCE | process_requirement | `SKILL.md:94-99`; workflow §3 table; `QA-CHECKLIST.md` §G; `JOB-TEMPLATE.yaml:100-105` |

Case 002 candidates (READABILITY_MARGIN, STACK_LEVEL_FIT, SUBJECT_AWARE_CROP_ANCHORING, SINGLE_VOICE_SOURCE, STILLS_FIRST, TEXT_OVER_IMAGERY_CONDITIONAL): none in runtime; two have prose shadows (CF2 obstruction, CF5 stack-level fit) in the checklist. Their promotion conditions ("a compositor fit routine in runtime with a test", "an obstruction check … exists in the compositor", "a subject box … with a test on a known plate") were not actioned before 003 and are not referenced by 003.

**Case 003 (PR #103 @ 1de2b37, OPEN):** `check_vo_schedule` + 4 tests in `gates.py`/`test_i_compositor_gates.py` (diff +35/+29); `production-learning/README.md` one line; nothing under `.claude/` (COMPUTED: `git diff main...1de2b37 --stat -- .claude` → empty). `WALL_OBSTRUCTION_GATE` stays as `wall_obstruction()` in `de1f978:…/tools/compose.py:135` on the archival branch. `AD_STRUCTURE_MINIMUM` is a "proposal … a skill edit, proposed, not made here" (PR body). The job branch was marked `learning_status: synced` (1aea4d2) before the PR merged.

### 1.5 Designed vs executed, in one line each

- Designed: packet → five classes → gate/test | candidate | directional | gap | none → PR → main → next job reads. 
- Executed: the mechanics ran three times and validated three times; class 1 items became code (9 gates in two days); classes 2–4 became prose and PR text; no promotion condition was ever closed; no candidate was ever promoted; no Canon gap was ever decided; and the class-1 gate promoted for the most recent failure has no caller.

---

## 2. K13 analysis — defect classes that recurred in case 003

Format per class: learning record in 001/002 → promotion state at 3bb9a3c → what 003 did → exact stop point.

### 2.1 Text over people / subject obstruction

- **001:** contract `plan/ACCEPTANCE-CONTRACT.md @ f6ca66f` B3 "supers are never over busy picture" (a criterion existed); V4 defect "offer/code collision" → SD-07 → ELEMENT_DISJOINTNESS — disjointness *among text regions*, not text-vs-subject.
- **002:** HD-03 (headline over the figure), HD-05/07 (copy over food), HD-08/09/10 (pill/banner over plant/photos) → `SD-HD-03…10` `promoted_as` FORMAT_SPECIFIC_REVALIDATION / REJECTED_DESIGN_REUSE; candidate `TEXT_OVER_IMAGERY_CONDITIONAL` with `promotion_condition: "an obstruction check (subject box vs text box) exists in the compositor"`; candidate `SUBJECT_AWARE_CROP_ANCHORING`; tally names "ELEMENT_DISJOINTNESS-adjacent (obstruction)" as a recurred known class.
- **Promotion state at 3bb9a3c:** prose row `QA-CHECKLIST.md` CF2 "no text or UI element sits over the product, face or hero object" (human eye); no code.
- **003:** operator ran CF2 by eye and wrote `CF2: PASS on 9:16 (copy on empty wall, nothing over bowl/hands/faces)` (`JOB.yaml:326`, stamped 14:37:21Z); the automated probe was contrast on 4 frames with no obstruction test; the human: "the text is coming on figures" (V1). The operator then wrote `wall_obstruction()` inside the job tool; PR #103 re-queues `WALL_OBSTRUCTION_GATE` as a candidate with condition "ported into runtime/compositor with a test on a known clip".
- **Stop point:** recorded (002) → candidate with a build condition nobody owned → prose check executed by the producing agent and self-passed (K7) → fix built on an archival branch → re-queued as a candidate (second time). Propagation halted at *class assignment*: obstruction was never class 1 because no deterministic check existed, and the class table has no "build the check" work item with an owner.

### 2.2 Robotic voice

- **001:** SD-05 "narration judged horribly robotic" → class `pipeline_failure`, subsystem `routing_voice_selection`, `promoted_as: SPEAKER_MICROQUALIFICATION (candidate)`; RO-05 (`n=16`, "all 16 verbatim on transcript; the Controller rejected the voice as robotic") with `routing_authority: none`; `not_promoted: any Capability Registry change (575 rows unchanged)`. Contract C2 "no robotic cadence" existed.
- **002:** HD-13a/b → CROSS_CLIP_VOICE_CONTINUITY (prose D14); candidate SINGLE_VOICE_SOURCE whose own condition text records "no proven single-voice route exists today (Sarvam narration rejected in case 001 V3; ElevenLabs premade voice not Indian; native per-clip narration not identity-stable)".
- **Promotion state at 3bb9a3c:** D10 sentence + D14 row + micro-qualification prose. The routing evidence map still carries Sarvam bulbul:v3 as a clean cell on ≤ 70-char lines (per 001 SD-05 root cause), and the skill forbids production verdicts from touching it ("A production success is not Registry evidence. An n=1 model observation is directional only" — the same rule silences an n=16 rejection).
- **003:** `plan.micro_qualifications[1].route: "sarvam-bulbul-v3 vs elevenlabs-v3-direct, one line each"`; 5 rounds, 26 takes, USD 0.2947 (`TIME-AND-COST.yaml spent_on_voice_search_usd`); Sarvam ×8 "all rejected by ear as robotic … consistent with case 001 RO-05"; ElevenLabs ×6 rejected + quota exhausted; user: "all three are robotic … eleven labs speically have vocies that feel human and so does sarvam" (the human's own prior disagrees with the record — a human-belief conflict the system has no place to store).
- **Stop point:** recorded twice → representation forbids it from changing route rank (F: the only route-quality store is the Registry, which production verdicts may not touch) → operator read it (`learning_applied[1]`) and reasoned it away (K5: "VO here is ≤ 5 short lines") → route re-tested → same verdict → 003 queues VOICE_BY_EAR_FIRST, which is 001's SPEAKER_MICROQUALIFICATION with the word "voice". The 001 promotion condition ("≥ 2 more real productions") was met or nearly met by 003's own application and nobody evaluated it.

### 2.3 Iteration count (versions and review cycles)

- **001:** 5 versions / 5 cycles / 7 h 54 m → SD-13 → `promoted_as: TTAO metric (candidate KPI)`; TTAO adopted as a KPI. The 001 contract itself said "one bounded repair cycle is authorised … No second repair without the Controller" (`ACCEPTANCE-CONTRACT.md:4-5,45-46`) and five versions were built — the bound existed in the contract and was not enforced (K12/K14).
- **002:** 5 cycles; PD-03 "paid calls began immediately after each human 'go'" → PAID_PRODUCTION_PREFLIGHT (prose).
- **Promotion state at 3bb9a3c:** runtime profiles carry `repair_allowance: 1|2` (`POLICY-PROFILES.yaml:91,162`) but the agency path is not the runtime; `PRODUCTION-WORKFLOW.md §12` says "the repair allowance is finite — say when it is spent and stop" with no number; §13 on REJECT: "ask what to change before spending again" — USD-0 re-assemblies are not "spending".
- **003:** 10 cycles (4 component gates, 5 voice rounds, 3 versions); the plan said "a second repair round would not fit; the user is told so" (`plan.expected_spend_usd.cap`), yet V2 and V3 were assembled at USD 0.0096 and USD 0 after two REJECTs. 
- **Stop point:** the learning became a *measurement* (TTAO) and never a *bound* with an owner; the only hard bound (spend cap) does not bind re-assembly; K6 (no decision owner for "stop and re-brief") and K14 (component-level accepts — 5 plates, 1 clip, 1 voice — gave a false sense of progress; the human then rejected on assembly and structure, i.e. approval was taken at the wrong level).

### 2.4 Weak creative architecture / ad structure

- **001:** `creative_direction` is the largest root-cause class — 8 of 25 REVISION-TRACE defects (COMPUTED: histogram in `REVISION-TRACE.yaml summary`, 32 %); SD-13 root cause "creative architecture was re-litigated across V1/V2/V3". Promotion: nothing except the accepted structure as a template; `not_promoted[0]`: "any new Canon doctrine … no new Canon need was proven by this pilot: the failures were creative architecture…".
- **002:** HD-05/07/08/09/10 coded `creative_direction` → REJECTED_DESIGN_REUSE (provenance bookkeeping); `not_promoted NO_CANON_CHANGE`: "not missing Canon knowledge".
- **Promotion state at 3bb9a3c:** blueprint fields in `PRODUCTION-WORKFLOW.md §5` (first_read, hook, offer, product, proof, cta, attention_order, brand_world, remember, muted_test) + pack check lines PA/CA from the two compiled packs; no field for opening, end card, brand presence over time, or "Direction" (ABCD terms); `commercial_communication` uncompiled under C-10.
- **003:** `canon.packs_selected` includes `commercial_communication`; `packs_injected: [composition_and_attention, product_appearance]`; blueprint check line `PA-D7: "pass — 'the bowl on a noodle night' sells at a glance; the hero image needs no copy"` (self-review); human on V2: "did cannon say nothing about product positioning? … it does not look like ad at all. the opening is missing too. canon had this knowledge. how's that possible?". The knowledge is in the accepted corpus: `canon/knowledge/current/google-abcd-video-ads/source-knowledge.yaml:737 concept_label: brand_shows_up_early_and_throughout` (OBSERVED).
- **Stop point:** two consecutive cases declared creative-architecture failure "not a knowledge problem", so no rule, field or gate was promoted for it; the third case declares it a Canon gap and can only "report"; the class table has no path from "knowledge exists, uncompiled, not injected" to a fix other than a Controller decision that C-10 makes conditional on this very failure. This is K2/K3 (retrieval/context) diagnosed as K0 (absent) in 003 and as "not knowledge" (K5/K10) in 001/002 — three cases, three diagnoses, no reconciliation step.

### 2.5 Timeline fixed before VO

- **001/002:** no learning record says "measure VO before fixing beats". Nearest: 001 RO-05 "output not deterministic across calls (pace 1.08 produced longer reads on two paragraphs)"; V4 contract "speaker audio never time-stretched"; ACCEPTED-TEMPLATE `narration_distribution`; 002 HD-13a (2.9-s hole inside a generated clip) → an ear check. UNKNOWN whether the pilot's assembly tools scheduled narration from measured durations (not investigated; on the pilot branch).
- **003:** DF-05 at V1 (23.5 s vs 18-s plan, "slow VO read drove the length") → repair dropped a line and set tempo 1.06; V3 restored the line at hand-set times → DF-08 (b1→b2 overlap 0.92 s; b6 overrun 0.94 s); `qa.voice_continuity` rows left `cadence_continuous: "pending human ear"`, `human_ear_verdict: null` when V3 was presented (`JOB.yaml:336-339`).
- **Verdict:** not a cross-case K13 (no prior record); an **intra-job** K13 (V1's diagnosis did not change V3's mechanism) plus K11 (the declared D14 check was not run before presenting) plus K1 (the blueprint stores VO `t:` as hand-set plan values, not measured ones — the representation invites the error).

---

## 3. Failure taxonomy

### 3.1 What the project's taxonomy distinguishes and what it collapses

Vocabularies in force (OBSERVED):
- `SYSTEM-DEFECTS.class`: `media_model_failure | pipeline_failure | infrastructure_transient` (check_case.py).
- `REVISION-TRACE.root_cause_class` (11): creative_direction, model_generation, model_audio, routing, compositor, deterministic_qa, pacing_edit, product_fidelity, commercial_positioning, infrastructure, orchestration.
- Skill defect classes (`QA-CHECKLIST.md §F`, 10): creative_direction, generation, audio, route, compositor, crop, text, product_fidelity, pacing, infrastructure — a third list; the 003 packet uses hybrids ("audio (compositor scheduling)") and the sync re-codes them into the 11.
- Promotion classes (5) and verdict vocabulary (4).

| K | Meaning | Project slot | Verdict |
|---|---|---|---|
| K0 knowledge absent | — | "Canon gap candidate" (class 4) | distinguished, but conflated with K2/K3 (003 calls an uncompiled-but-present source a "gap") |
| K1 knowledge unstructured | — | none | collapsed (candidate patterns are K1 by construction and never graduate) |
| K2 retrieval failed | — | none | collapsed into K0 or into `creative_direction` |
| K3 not in useful context | — | none (`canon.missing_domains` records it as data, no class) | collapsed |
| K4 ignored/diluted | — | none | collapsed (003 `learning_applied` rationalisations have no class) |
| K5 wrong reasoning | — | `creative_direction` / `orchestration` | collapsed with K0/K7 |
| K6 no decision owner | — | none | absent |
| K7 self-review | — | none | absent — the operator's wrong PASS lines are filed as `compositor`/`deterministic_qa` |
| K8 wrong route | — | `routing` / `route` | distinguished; but 003 uses two routes with no Registry cell (Nano Banana 2 + refs; Gemini TTS) under human OK — a K12-by-policy with no class |
| K9 model failed | — | `media_model_failure`, `model_generation`, `model_audio`, `generation` | distinguished; boundary with route choice is unstable (001 SD-05 = pipeline/route; REVISION-TRACE = model_audio) |
| K10 assembly failed | — | `compositor`, `pacing_edit`, `crop`, `text` | distinguished |
| K11 QA missed | — | `deterministic_qa` | distinguished; but "check declared, not run" (003 D14 pending) has no slot |
| K12 workflow bypass | — | 002 `process_conformance`, `orchestration`, PD-xx | distinguished (002 only) |
| K13 learning failed to propagate | — | 002 `known_defect_classes_that_recurred` (tally field, not a class) | collapsed into K12 (QA_COVERAGE_ENFORCEMENT) |
| K14 approval at wrong level/time | — | 003 "components, not an outcome" (prose) | absent as a class |
| K15 unnecessary process | — | none (26 voice takes, 5 rounds recorded as cost only) | absent |

COMPUTED inconsistencies inside the project's own coding:
```
001 SYSTEM-DEFECTS: media_model_failures_that_reached_the_controller: 0
001 REVISION-TRACE defects coded model_*: [('V2','presenter quality degraded…','model_generation'), ('V3','voice horribly robotic…','model_audio')]
003 SYSTEM-DEFECTS rows by (class, reached_human): {('pipeline_failure', True): 6, ('media_model_failure', True): 1, ('media_model_failure', False): 1, ('infrastructure_transient', False): 1}
003 stated tally: pipeline_failures_reaching_the_human: 5
```
(`SD-09` 4:5/1:1 has `reached_human: true` and is not in the tally.) Also DF-06 (attempt-id collision from a line count, no lock) is classed `infrastructure_transient` — the class reserved for provider outages — which is a tooling defect (K10/K12).

### 3.2 Re-coding of the Cumin material into K0..K15

| Item | Project's diagnosis | My coding | Where it differs |
|---|---|---|---|
| DF-01 garbled embossed mark, curry (plate-A r1) | `product_fidelity`, media_model_failure, caught before review | **K9** (model) + K4 (001 RO-04 "Nano Banana 2 environmental-text redraw" existed; not in `learning_applied`; prompt did not turn the mark) ; K14 correct (human gate caught it) | project drops the prior-knowledge angle |
| DF-02 "random audio" (silenceremove inside lines; single-pass loudnorm) | `audio` / compositor, pipeline | **K10** + K11 + **K7** (`D11: "music ducked under VO (sidechain), loudnorm −14 LUFS"` self-PASS on V1, `JOB.yaml:317`) | project has no K7 |
| DF-03 mouths moving under VO | `generation`, media_model_failure reached human | **K5 planning** (i2v prompts did not forbid speech although 001 RO-01/002 RO-02 record Veo speaking/animating mouths) + K9 secondary | project: model; mine: foreseeable prompt omission |
| DF-04 text over chopsticks/noodles | `compositor`, pipeline | **K13** (002 TEXT_OVER_IMAGERY_CONDITIONAL / CF2) + **K7** (CF2 self-PASS) + K11 | project: compositor |
| DF-05 23.5 s vs 18-s plan | `pacing` | **K5** (beats fixed before VO measured) + **K1** (blueprint `voice_over.lines[].t` are plan values) | project: pacing |
| DF-06 attempt-id collision | `infrastructure` (transient) | **K10/K12** tooling (job-local script, unshared) | misclassed as provider transient |
| DF-07 no ad structure | `creative_direction` → Canon gap (K0) | **K2/K3** (source present in `canon/knowledge/current`, selected by the trigger table, not injected because uncompiled) + **K7** (PA-D7 "pass") + **K13** (001/002 declared creative failure "not knowledge") | project: K0 |
| DF-08 voices overlapping | `audio (compositor scheduling)` → gate | **K10** + **K11** (D14 declared, `pending human ear`, not run) + intra-job **K13** (DF-05 → same mechanism) | project: compositor only |
| 4:5 / 1:1 no copy zone | `crop` | K13 (002 SUBJECT_AWARE_CROP candidate) + **K14/K6** (rows "FLAGGED for the human" on V1/V2/V3, presented anyway, never ruled on) | project: crop |
| VO_FIRST_TIMELINE (cand.) | pattern | K5/K1 — a planning-order rule needing a representation (measured durations in the blueprint) | — |
| CLOSED_MOUTH_UNDER_VO (cand.) | prompt rule | K1 (unstructured prompt clause) over a K9 trait | — |
| AD_STRUCTURE_MINIMUM (cand.) | blueprint fields | K1 stand-in for K2/K3 (a prose paraphrase of an uncompiled pack — what C-10 and the skill forbid, in disguise) | project calls it an operator field |
| GEOMETRY_NEEDS_ITS_OWN_PLATES (cand.) | pattern | K5 planning; K13 (002 FORMAT_SPECIFIC_REVALIDATION found it, three times) | — |
| VOICE_BY_EAR_FIRST (cand.) | workflow ordering | **K13** (restates 001 SPEAKER_MICROQUALIFICATION) + **K15** (26 takes) | project treats as new |
| RO-01 NB2 + refs (n=6, 5 accepted) | directional | K9 observation; K8/K12 (no Registry cell; used under human OK) | — |
| RO-02 Veo i2v mouths (n=7) | directional | K9 + K1 (the "nobody speaks" clause is the knowledge; stays a note) | — |
| RO-03 Gemini TTS Leda (n=12) | directional | K8/K12 (no cell, job-pinned price) — the route that *worked* is outside the evidence system | — |
| RO-04 Sarvam ×8 rejected | directional, "consistent with 001 RO-05" | **K13** + K15 | project labels it consistent and leaves it directional |
| RO-05 ElevenLabs ×6 rejected, no Indian voice, quota | directional | **K13** (002 SINGLE_VOICE_SOURCE condition already said "ElevenLabs premade voice not Indian") + K15 | — |
| RO-06 Lyria 1/1 | directional | K9 positive | — |

Summary of the divergence: the project codes 6 of 9 defects as `pipeline_failure` and 1 as model; my coding puts **K13 or K7 on 6 of the 9** (DF-04, DF-07, DF-08, 4:5/1:1, DF-02, DF-01/K4) and K5 planning on 2 (DF-03, DF-05). "Pipeline failure" is where the project files everything the taxonomy cannot name.

---

## 4. Acceptance contracts

### 4.1 What one looks like

- **request-space-v1** (`canon/research/request-space-v1/MEDIA-REQUEST-GRAMMAR-v1-PROPOSAL.yaml @ 3bb9a3c`, `status: PROPOSED_NOT_APPROVED`): component G14 `objective_audience_acceptance` — "ABSENT FROM EVERY REAL-USER CORPUS IN THE REGISTER… neither has an acceptance contract"; `project_status: represented — objective.class, audience, acceptance contract, success_criteria` (lines 266-282). Header caveat (23-26): commercial components "rest on qualitative practitioner evidence or on our own product scope — never on measured demand". So in the request grammar an acceptance contract is a slot with no external evidence of its shape.
- **Runtime/job template**: `PRODUCTION-SPEC-v1.yaml:125-132` `acceptance_contract: list[string]` — "Three to six statements, decidable from the artifact alone, phrased ACCEPT only if … / REJECT if …, carrying no route name, arm, cost or rule id … frozen BEFORE the first draw". `ACCEPTANCE-STYLE-v0.yaml` bans route/Canon/pack ids/price/provider words and derives four statement types (exact strings read exactly; no other lettering; identity line-up; nothing added). `TEMPLATE-v0.yaml blueprint.acceptance_statements` carries them forward. Stage-A examples (`eval/empirical-planning/STAGE-A-FREEZE-2026-09/ACCEPTANCE-CONTRACTS.md`): "ACCEPT only if exactly one bottle is in frame…", "REJECT if any lettering…".
- **Agency job record**: `JOB-TEMPLATE.yaml` has **no** acceptance-contract field (COMPUTED: `grep -n -i accept` → `advertising_acceptance_intent`, `reviews … input, not acceptance`, `versions[].verdict`). `brief.job.json` (PRODUCTION-JOB-v1) has no acceptance keys. The 001 pilot had a 28-line contract (`plan/ACCEPTANCE-CONTRACT.md @ f6ca66f`) and a V4 addendum with 20 conditions and a 60-point speaker score; 002 had none (PD-01); 003 had none.

INFERENCE: the runtime contract is designed for a blind first-language judge on a static artifact; it cannot, by its own style guard, carry "looks like an ad", "extraordinary", "warm voice", "brand early and throughout" — the register of every terminal rejection in the three cases.

### 4.2 Do human verdicts map onto contract fields?

Case 001 (contract present). Negative feedback items from `HUMAN-VERDICTS.yaml` (positives excluded; 22 items, COMPUTED from the 25-item list):

| # | Human item | Contract line | Match |
|---|---|---|---|
| 1 | video proof too small | — | no |
| 2 | too much phone/mockup framing | — | no |
| 3 | opening not visually exceptional | — (B5 is "not a generic showreel") | no |
| 4 | presenter blocks too long | — | no |
| 5 | creative range insufficient | — | no |
| 6 | 24h/4h differentiation undersold | A2 (ordering only) | partial |
| 7 | presenter quality degraded later (V2) | C1/C2 identity/speech | yes |
| 8 | still cautious phone/mockup | — | no |
| 9 | opening still not strong | — | no |
| 10 | competent, not extraordinary | — (V4 addendum later adds "pretty good is a reject") | no |
| 11 | text getting cut off | D6 (ad text inside phone frames) | partial |
| 12 | text colour disappearing | D4 contrast ≥ 4.5:1 | yes |
| 13 | creatives/images cropped | D6 | partial |
| 14 | inconsistent card geometry | B1 "one type system in the cards" | partial |
| 15 | voice horribly robotic | C2 "no robotic cadence" | yes |
| 16 | pacing too rushed | — | no |
| 17 | direct-to-camera speaker missing | B2 presupposes a presenter | partial |
| 18 | offer/code collision | B3 "one boss element" | partial |
| 19 | "and it can't suck" lost | — | no |
| 20 | speaker bubble persisted | — | no |
| 21 | not enough creative-range proof | — | no |
| 22 | 4-Hour Express too weak | A2 | partial |

001: yes 3, partial 7, no 12 of 22.

Case 002: 13 human-flagged defects (`defect_register`, COMPUTED n=13); job contract: none → 0 of 13. Note (INFERENCE): 9 of the 13 would have been covered by the *previous* job's contract (D4 contrast, D6 crops, B3 "supers never over busy picture", C2 voice) — the criteria existed and were not carried, a K13 on the contract itself.

Case 003: 7 named defects (HD-01..07); job contract: none → 0 of 7. Against the QA checklist rows as "pre-declared criteria": HD-01 ↔ D11 (self-PASS), HD-03 ↔ CF2 (self-PASS), HD-07 ↔ D14 (pending), HD-06 ↔ PA-D7 (weak) → 4 partial; HD-02, HD-04, HD-05 nothing.

### 4.3 Fraction of rejection reasons with a pre-declared acceptance criterion (COMPUTED from the tables above)

- Strict (job-specific contract line clearly names the criterion): **3 / 42 = 7.1 %**.
- Lenient (partial matches + QA-checklist rows counted): **14 / 42 = 33 %**.
- Contract lines the human never invoked (001): ≥ 18 of 28.
- Terminal rejections ("reject" / "rebuild_direction" verdicts: 001 V2, V3; 002 N1, N2; 003 V1, V2, V3 = 7) whose *stated* reason was contract-named: 001 V3 partially (contrast, voice), otherwise 0 → 1 of 7.

The pattern the question names ("this is a tutorial not an ad") is literally 003 V2: "it does not look like ad at all" — no contract, checklist row or blueprint field for it; the blueprint field that came closest (PA-D7) was self-marked pass.

---

## 5. Memory systems

### 5.1 Classification of what exists (OBSERVED)

| Type | Store | Writer | Reader / retrieval trigger at job time |
|---|---|---|---|
| **Episodic** | `production-learning/cases/*` (2 on main, 1 in PR #103); raw job branches (`work/agency-job-*`, archival, unmerged); pilot branches; `coordination/audits/*` | LLM operator via `/media-agency-sync` (per job) | `BOOTSTRAP.md §2` once per session: read all case READMEs / queues / templates / route observations; `PRODUCTION-WORKFLOW.md §3`: LLM decides `learning_applied`. No key, no index, no query. |
| Episodic (runtime) | `runtime/store/outcomes/*.json` (OUTCOME-EVENT-v1) — **directory does not exist**; 8 dry battery events under `runtime/battery/results/2026-09-14/*/10-outcome-event.json` | `runtime/loop/driver.py:184-190` (dry chain only) | `TemplateLibrary.promote` reads an accepted event; nothing else reads events |
| **Semantic** | `canon/knowledge/current/**` (accepted corpus, e.g. google-abcd), 2 of 10 compiled packs (`canon/compilation/PACK-*`), `canon/packs/pack-triggers-v0.yaml`; Capability Registry / `ROUTING-EVIDENCE-MAP-v0.yaml` (semantic about models); `ROUTE-OBSERVATIONS.yaml` (episodic notes with a semantic ambition and `routing_authority: none`) | Canon streams; Lab; sync | Deterministic trigger table on NR fields → pack ids → only compiled packs injected (003: 10 selected, 2 injected, 8 `missing_domains`); routing table read at bootstrap; route observations "tie-breakers only" |
| **Procedural** | `.claude/skills/media-agency/{SKILL,PRODUCTION-WORKFLOW,QA-CHECKLIST}.md`, `JOB-TEMPLATE.yaml` (prose); `runtime/compositor/gates.py`, `tokens.py`, `runtime/loop/frame_hygiene.py`, `runtime/execute/pools.py`, `provider_errors.py`, `canon/gate/*` (code); `runtime/canon/templates.py` (`TemplateLibrary`, exact-identity match, empty store); `cases/*/ACCEPTED-TEMPLATE.yaml` (prose, `status: accepted_once`) | sync PRs; runtime lanes | Prose: read by the operator LLM. Code: called only if the job-local script chooses to call it (`compose.py` called 5 gates, not `frame_hygiene`/`pools`). `TemplateLibrary.match`: never called on the agency path (`template.reused: none`; the library has no entries). |

### 5.2 Consolidation / reflection beyond the sync PR

None found. Evidence: `check_case.py` is single-case; no tool reads two cases; PROMOTION-QUEUE conditions are never re-evaluated (SPEAKER_MICROQUALIFICATION "≥ 2 more" — 003 applied it and did not touch 001's queue; TEXT_OVER_IMAGERY_CONDITIONAL — 003 rebuilt the check and queued it under a new name without citing 002; COMPLEX_PRODUCTION_EVENT — 002 "trigger MET", 003 silent); Governor refreshes (`PROJECT-MEMORY.md`, `CONTROL-STATE.md`) update maps, not rules; the CLAUDE.local.md operator memory rule says "Auto-memory holds operational discoveries only … Never project truth" — i.e. the one place an LLM could consolidate is forbidden from holding anything that matters.

### 5.3 Why recurrence prevention is failing structurally (INFERENCE, each point tied to evidence above)

1. **The only enforcement surface (runtime gates) is opt-in from a job-local script.** `compose.py` decides which gates run; a new gate with no caller (`check_vo_schedule`) prevents nothing; an obstruction gate that exists only on an archival branch prevents nothing.
2. **The class table routes every perceptual learning into prose or a candidate, and prose is consumed by the agent that also self-reviews it.** CF2 PASS, PA-D7 pass, D11 PASS, D14 "pending" — four self-marked lines sit directly under the four human rejections of 003 (K7 with no independent check).
3. **Promotion conditions have no owner and no evaluation step.** Conditions of the form "one more production confirms…" are never checked by the next sync; candidates are re-derived under new names.
4. **Production verdicts are forbidden from touching the route store by design**, so a route rejected by ear for the same requirement in two cases keeps its Lab rank (robotic voice recurred with n = 16 + 8).
5. **The semantic layer is 80 % unretrievable and the gate on compiling more is the failure itself** (C-10: "unless a real runtime failure later demands one"); two cases declined to call their creative failures knowledge failures, so the trigger never fired until 003 — and 003 can only "report".
6. **Episodic memory is keyed by CASE-ID, not by requirement or defect class**, so "text over subject" in 002 (HD-03/05/07/08/09/10) and 003 (DF-04) are not linked by anything except a reader's memory.
7. **Approval is taken at the component level** (plates, clip, voice accepted) while rejection happens at assembly/structure level; there is no pre-assembly structural review artifact for the human (the blueprint was shown once at 13:28Z as "concept + routes + spend").
8. **The runtime's empirical memory (events → templates) is disconnected from where production happens** (§7), so nothing learned in production ever reaches the runtime's own memory, and nothing in the runtime's memory (all dry) is real.

---

## 6. Experimental design

### 6.1 Can the evidence being generated distinguish the hypotheses?

| Programme | n / controls / blinding / outcome (OBSERVED) | What it can and cannot separate |
|---|---|---|
| EVAL-037 (`eval/experiments/EVAL-037/experiment.yaml`, `CONCLUSION.md`) | 6 briefs × 4 models × 2 conditions × 3 reps = 144 planned; asymmetric completion; 4 blind judgment streams over *packages* (plans), no media; conditions = NO_CANON vs FULL_CANON *access* (tools), plus supplemental CONTROLLED_CANON; Gemma FULL_CANON used Canon 0/18; unbounded Sonnet overflowed 16/18; controlled Sonnet 53 searches, 1 read | Cannot separate A (knowledge weak) from B (retrieval) from C (context overload): the treatment did not control what entered context. Cannot speak to accepted media (packages only). Controller conclusion: "Canon helps, but retrieval immature" — a programme-direction read, not an effect size. |
| EVAL-038 (`RESULTS.md`, `JUDGING-PROTOCOL.md`, decision 2026-09-01) | weak (Haiku, Gemma) + 2 compiled packs, forced injection, 2 reps vs Sonnet NO_CANON 3 reps; 6 briefs; single blinded reviewer (design asked two by unanimity); blinding scrub scars penalised treatment; media n = 2 pairs; 0/6 | Tests only "weak + packs substitutes for strong alone" — refuted. Confounds D (model) with H (packs abstract/incomplete: 2 of 10) and L (strong LLM wins). The informative cell — strong + packs vs strong alone — was never run (baseline was never re-run by order). |
| Value gate (`canon/experiments/v1/value-gate/PROTOCOL.md`) | 12 pairs (7 coverage vote, 5 gap diagnose); oracle Canon vs length-matched (≤ 15 %) generic control; two reviewers by unanimity; stratified position balance; 9 dimensions | The only design in the repo that isolates F/H (representation and structure vs generic craft). **NOT EXECUTED** — blocked on `FRESH_CONTROL_SESSION_REQUIRED`; 0 of 24 outputs. |
| Judge qualification (EVAL-040, cited in `CONTROLLER-ALPHA-1-…-2026-09-14.md`) | automated judge vs Controller: kappa 0.33, false-accept 22 % → C-8 human release | Establishes that the automated judge is not an outcome measure; no inter-human reliability exists (one judge). |
| Production learning (3 cases) | n = 3 jobs, different families (57-s presenter film; tile batch; 18-s two-character VO ad), different route sets, different process conformance; one judge = brief author, unblinded; no repeated draws; outcome = chat verdict | Generates hypotheses only. Nothing is held constant; every difference between cases is confounded with every other. Its strongest signal is the *recurrence* pattern (§2), which is about the loop, not about Canon or models. |

INFERENCE: nothing run or planned distinguishes A/B/C/D/E/F/H/J/L/M-N. EVAL-038 weakly supports L against "packs as substitute" and nothing else.

### 6.2 Minimum decisive experiment set (recommendation, clearly marked)

Common substrate: the 6 EVAL-037 briefs + the 3 real briefs (Upwork intro, one tile, Cumin) = 9 briefs; a **rejection checklist** derived from the 42 human items in §4.2 (the "known human rejection reasons" list, ~25 distinct); two blind reviewers by unanimity (value-gate rule), position-balanced; a strong reasoning model fixed throughout unless the arm varies it. Costs assume ~USD 0.05–0.20 per reasoning package and pinned media prices from the cases (image ≈ 0.07; 6-s Veo fast ≈ 0.60).

| # | Question | Arms (same model, same prompt, same briefs unless stated) | n | Cost ceiling | Outcome measure | Reading |
|---|---|---|---|---|---|---|
| E1 Context ladder (A, C, F, H) | Does *what* is in context matter, and does more hurt? | (a) no Canon; (b) oracle hand-picked *compiled-form* doctrine ≤ 2.5k tokens; (c) same content as raw source excerpts ≈ 10k tokens; (d) union of all 10 packs' sources ≈ 35k+ tokens | 9 briefs × 3 reps × 4 arms = 108 packages | USD 25 | value-gate 9 dimensions + rejection-checklist hit rate (fraction of the ~25 known rejection reasons the plan pre-empts) | b > a & c ≈ a → structure/representation (F/H) is the lever; d < b → overload (C); b ≈ a → knowledge not the bottleneck (A false; go to E4/E5) |
| E2 Retrieval (B) | Does the trigger-table/lookup lose what the oracle finds? | (b) oracle vs (e) `runtime.canon.lookup` output for the same NR, with all 10 packs *compiled for the experiment only* (not merged) | 9 × 3 × 2 = 54 | USD 12 | same | e < b → retrieval/compilation loses value (B); e ≈ b → retrieval fine, go to E3 |
| E3 Short checklist (L, M/N) | Does a 40-line rejection-derived checklist match oracle Canon? | (b) oracle vs (f) strong model + checklist only vs (g) strong model + checklist + oracle | 9 × 3 × 3 = 81 | USD 18 | same | f ≥ b → L (strong LLM + short checklist wins); g > f → Canon adds beyond the checklist; build the checklist two ways — (m) from human Q&A/rejection transcripts, (n) from eval accept/reject data — and compare f_m vs f_n for M/N |
| E4 Role collapse (E, K7) | Does an independent reviewer catch what the producer self-passes? | Replay the 3 Cumin versions + 5 case-002 B1 tiles: (i) producer's own QA rows as recorded; (ii) a fresh session (no job context) given the artifact + checklist; (iii) a second human | 8 artifacts × 3 reviewers | USD 5 (no media) + ~2 h human | fraction of human-named defects (§4.2) flagged before presentation; producer-self-PASS lines overturned | (ii) or (iii) catches ≥ 50 % of what (i) missed → E dominates; fund an independent QA role before more Canon |
| E5 Assembly-only replay (J) | Were the rejections assembly problems? | Re-assemble Cumin V1–V3 from the same accepted components under `check_vo_schedule` + `wall_obstruction` + edge-trim audio; also 002 B1 tiles under the runtime gates; blind A/B originals vs replays | 6 pairs × 3 judges | USD 0 media; ~1 h human | per-defect flip rate on the 7 HD / 13 HD criteria; overall accept | ≥ 5/7 flips → J (assembly) dominates 003; structural rejections (opening, end card) will not flip → those are E1's domain |
| E6 Human-preference reliability (prerequisite) | Is the single judge a usable instrument? | 3 judges (author + 2 non-authors), blind, on the 15 versions/tiles from the three cases: accept/reject + defect class | 15 × 3 | ~2 h human | Cohen/Fleiss kappa on accept/reject; agreement on named defect class | kappa < 0.4 → no other experiment's outcome is interpretable; write the checklist with the judges first |
| E7 Model sufficiency (D) | Reasoning: does a strong model with oracle Canon beat a weak one with the same? Media: already bounded (1–2 model failures/case) | E1 arm (b) with strong vs weak reasoning model | 9 × 3 × 2 = 54 | USD 8 | same | strong+b ≫ weak+b and strong+a ≈ strong+b → D over A (consistent with EVAL-038); otherwise A/F |

Total ceiling ≈ USD 70 of API/media plus ~5 h of human judging; every arm reuses committed briefs and accepted components, no new route qualification, no Registry effect. Order: E6 → E4/E5 (USD 0 media, decide whether the loop or the knowledge is the problem) → E1 → E2/E3/E7. What each outcome implies is in the last column; the decisive pair is E4/E5 vs E1 — if independent review and re-assembly recover most rejections, the programme's bottleneck is the loop (K7/K13/J), not Canon.

---

## 7. Is OUTCOME-EVENT / empirical memory connected to production?

**No — OBSERVED/COMPUTED:**
- `ls runtime/store` → "No such file or directory" on main; no `runtime/store` in any of 20 worktrees (`git worktree list` + loop).
- Only events on disk: 8 × `runtime/battery/results/2026-09-14/B*/10-outcome-event.json`, all `dry_run: true` (B01/B04/B05/B12/B14 accepted by "controller" in a scripted battery; B02/B03/B13 abandoned). `grep -rl '"dry_run": false'` → none.
- `OutcomeStore.write` is called only from `runtime/loop/driver.py:190`; `runtime/alpha/run.py:312-328` promotes templates from `loop.event`; `runtime/ALPHA-1.md:145-149`: "A live dispatch … does not exist; `dispatch_mode: live` refuses".
- Cases 001 and 002 were produced by pilot scripts (`OUTCOME.yaml job_family_note` in both); 003 by job-local `tools/compose.py` / `dispatch.py` whose imports are `runtime.compositor.{tokens,gates}`, `runtime.errors`, `runtime.execute.provider_errors`, `runtime.route.cli.build_router` — never `runtime.loop.memory`, `acceptance` or `runtime.canon.templates`.
- Case 001 README documents the v1 mapping gap; 002 declares `COMPLEX_PRODUCTION_EVENT trigger condition: MET`; 003 does not mention events. No event, template or `runtime/store` entry exists for any real production. The accepted V4.1 "template" is `ACCEPTED-TEMPLATE.yaml` in the case directory (`status: accepted_once`), not a `TEMPLATE-v0`, so `TemplateLibrary.match` could never return it.

Eight-state proof for the two claims that matter most:
- *Compositor gates (001 → 003)*: knowledge exists (gates.py) → retrieved (imported, compose.py:31) → in context (called) → understood (rows written) → changed decisions (backing cards added where contrast failed, V1 4:5 "8 boxes") → correct (no human complaint on bounds/contrast/geometry in 003) → survived production (qa.json PASS) → **QA detected failure: NO for obstruction and audio — no gate existed**. Proven through "survived"; the failure was outside the gates' scope.
- *ABCD ad structure (Canon → 003)*: knowledge exists (`canon/knowledge/current/google-abcd-video-ads/source-knowledge.yaml:737`) → **retrieved: NO** (selected by trigger table, uncompiled, `packs_injected` excludes it) → never in context → (rest unreachable) → human detected. Chain broke at retrieval, not at knowledge.

---

## 8. Open questions / unknowns

1. UNKNOWN whether the 001 pilot's assembly tools scheduled narration from measured durations (would make VO_FIRST_TIMELINE a cross-case K13 rather than intra-job); the pilot branch tools were not opened.
2. UNKNOWN whether the Controller ever evaluated any `promotion_condition` outside the sync PRs (no decision record found under `coordination/decisions/` mentioning a production-learning candidate; PR #98 audit comment adoption of TTAO is cited in the queue but the comment itself was not read).
3. UNKNOWN whether the routing evidence map's Sarvam cell carries any note from 001 RO-05 (not inspected; the skill and the cases say production verdicts never touch it).
4. The 003 `plan.micro_qualifications[].human_gate_verdict` fields are `null` at de1f978 although the gates were passed in chat (`versions[]` MQ1 rows exist) — bookkeeping left inconsistent inside the job record; not material to the findings.
5. Whether the 003 human's stated belief ("eleven labs … feel human and so does sarvam") reflects a different brief register than 001's is a human-preference question no artifact can settle; it is why E6 is the prerequisite.
6. PR #103 is OPEN; if it merges unchanged, `check_vo_schedule` enters main with no caller and `WALL_OBSTRUCTION_GATE` remains a candidate for the second time.
