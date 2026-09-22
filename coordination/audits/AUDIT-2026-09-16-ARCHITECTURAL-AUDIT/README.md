# Independent Architectural Audit — Media Intelligence programme

**Commissioned:** 2026-09-16, by the Controller. **Completed:** 2026-09-20 (folder keeps its commission-date name). **Auditor:** Lead Independent Architectural Auditor (Claude Fable 5.1, local desktop session) with 15 completed subagent councils; a 16th was stopped by the Controller before writing, and Parts 6–18 were written by the lead alone without further agents at the Controller's instruction.
**Baseline audited:** `chawlavaibhav/media-intelligence` `main` @ `3bb9a3c3da484e43d4d54ae20543d1d246769ac6` (verified `git rev-parse HEAD`; matches the commissioned SHA). PR #103 head `1de2b37` (verified). Cumin evidence commit `de1f978` (verified; branch head moved one sync-only commit to `1aea4d2`).
**Status:** READ-ONLY AUDIT. Nothing implemented, no provider called, no money spent, no Controller state modified, nothing merged. These files are **uncommitted** in the `main` working tree; the Controller decides whether and where they are committed. (Warning: the `/media-agency` workflow §0 refuses to start on a dirty tree — commit or move this directory before the next job.)

## Typed authority used (per the Controller's cross-repository rule)

| Source | Treated as authority for | Location |
|---|---|---|
| media-intelligence (MI) `main` + branches | current architecture, Canon, capability evidence, production-learning truth | `/Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence` |
| media-factory (MF) + handoff bundle (MFH) | historical empirical priors, earlier working techniques | `…/media-factory` (main `7279ec5`, spike `57b2cca`), `…/media-factory-controller-handoff` (non-git) |
| upwork-project (UP) | current commercial proposition | `…/upwork-project` @ `ff06dab` |
| Raw production branches | what actually happened | `work/pilot-upwork-intro-video-v4` @ `f6ca66f`; `work/upwork-portfolio-samples-2026-09-15` @ `b4b77fa`; `work/agency-job-cuminco-chopsticks-001` @ `de1f978` |
| Human verdicts | accepted/rejected quality | `HUMAN-VERDICTS.yaml` ×3, `JOB.yaml versions[]` |

**Discovered supporting evidence (declared, not silently included):**
- Two independent local reviews of 28 Aug 2026 (not in git): `…/media-intelligence-os-review.md`, `…/media-intelligence-project-head-review.md`. Used for the "were prior recommendations adopted" question.
- `…/upwork-portfolio-tiles` (local git, published tiles) and `…/upwork-portfolio-media` (non-git): the actual portfolio bytes.
- `…/rentok-ad` (non-git, 30 Aug): a pre-agency Hinglish multi-scene Veo ad with hand-injected doctrine; historical prior only, no verdict on disk.
- `…/aight-website/assets/gallery`: July 2026 Devanagari textless-plate thesis; historical prior only.
- `…/voice-workshop-agent`: unrelated (Azure voice agent); excluded.
- MF spike judgments live in a Claude memory file outside any repo (`~/.claude/projects/-Users-vaibhavchawla-Vaibhav-Personal-Projects/memory/media-factory-project.md`); cited only as Tier C via MFH.

## Files

| Part | File |
|---|---|
| 1 Executive diagnosis | `PART-01-EXECUTIVE-DIAGNOSIS.md` |
| 2 Persona expectation map | `PART-02-PERSONA-EXPECTATION-MAP.md` |
| 3 Project archaeology | `PART-03-PROJECT-ARCHAEOLOGY.md` |
| 4 Intelligence asset inventory | `PART-04-INTELLIGENCE-ASSET-INVENTORY.md` |
| 5 Knowledge-flow map | `PART-05-KNOWLEDGE-FLOW-MAP.md` |
| 6 Real-production failure trace (cases 001/002/003) | `PART-06-PRODUCTION-FAILURE-TRACE.md` |
| 7 Q&A investigation | `PART-07-QA-INVESTIGATION.md` |
| 8 External research | `PART-08-EXTERNAL-RESEARCH.md` |
| 9 Requirement model by media job class | `PART-09-REQUIREMENT-MODEL.md` |
| 10 Keep / change / defer / delete | `PART-10-KEEP-CHANGE-DEFER-DELETE.md` |
| 11 Competing architectures | `PART-11-COMPETING-ARCHITECTURES.md` |
| 12 Root-cause ranking | `PART-12-ROOT-CAUSE-RANKING.md` |
| 13 What we still do not know | `PART-13-UNKNOWNS.md` |
| 14 Decision tree | `PART-14-DECISION-TREE.md` |
| 15 Recommended architecture | `PART-15-RECOMMENDED-ARCHITECTURE.md` |
| 16 Minimum decisive experiments | `PART-16-MINIMUM-DECISIVE-EXPERIMENTS.md` |
| 17 Two-week recovery plan | `PART-17-TWO-WEEK-RECOVERY-PLAN.md` |
| Closing return (agents, evidence, findings, disagreements) | `PART-18-CLOSING-RETURN.md` |
| Council reports (full evidence: agent-rules preamble, 15 reports, raw marketplace-case extract = 17 files) | `council-reports/` |
| Addendum A — Canon interrogation: assessment of the "wrong-question" hypothesis (2026-09-20) | `ADDENDUM-A-CANON-INTERROGATION-ASSESSMENT.md` |
| Addendum B — Paper experiment: existing vs decision-driven pathway on the Cumin brief, with a blind fresh-context checker run | `ADDENDUM-B-PAPER-EXPERIMENT-CUMIN.md`, `ADDENDUM-B-checker-input.md` |
| Addendum C — Judge-reliability packet (E6): 15 artefacts, blind order, scoring sheet, κ | `ADDENDUM-C-E6-JUDGE-PACKET.md` |
| Addendum D — Five-brief questioning experiment (Controller order steps 1–4): frozen inputs, five-stage producer records, blind checker input, checker output verbatim, reconciliation; then the second checker (Opus) and the no-hindsight producer with its own checker run | `ADDENDUM-D-FIVE-BRIEF-EXPERIMENT/00-FROZEN-INPUTS.md` … `07-SECOND-CHECKER-AND-NO-HINDSIGHT-RESULTS.md` |
| Question template v0 (reusable per-stage question layer, authorised 2026-09-20; v0.1 corrections from Addendum D §7 applied) | `QUESTION-TEMPLATE-v0.md` |

## Evidence standard

Every important statement in Parts 1–17 carries one of **OBSERVED** (read from bytes or computed by a shown command), **INFERENCE**, **HYPOTHESIS**, **RECOMMENDATION**, **UNKNOWN**. Repository claims cite `path @ sha` (line where possible). Media cite path + sha256 (Part 6, council report 12). External claims cite source + date. Where two sources conflict, the conflict is reported, not harmonised (see Part 13 §conflicts). PROJECT-MEMORY.md and CONTROL-STATE.md were used as maps only; every load-bearing figure was recomputed (Part 3 §0).

## Agent organisation actually used

| # | Council | Personas | Report |
|---|---|---|---|
| 1 | Project Archaeologist (MI) | — | `council-reports/01-archaeology-mi.md` |
| 2 | Media Factory Archaeologist | — | `02-media-factory-priors.md` |
| 3 | Customer / Commercial Council | 1–6, 70 | `03-commercial-council.md` |
| 4 | Case 003 (Cumin) forensic | 73, 74 | `04-case-003-cumin.md` |
| 5 | Cases 001/002 forensic + Recurrence Auditor | 73, 74 | `05-cases-001-002-recurrence.md` |
| 6 | Canon / Retrieval / Ontology | 47–50, 55, 57 | `06-canon-retrieval.md` |
| 7 | Q&A Corpus | 53, 54, 56 | `07-qa-corpus.md` |
| 8 | Model / Capability / Routing + Lab evaluation | 41–46, 58 | `08-capability-routing.md` |
| 9 | Runtime / Operator / Context-window | 36–40, 51, 57, 28, 35 | `09-runtime-operator-context.md` |
| 10 | Evaluation / Production-learning / Memory | 52, 58–63 | `10-learning-evaluation.md` |
| 11 | Adversarial Simplicity + Economics | 64–72, 75 | `11-adversarial-economics.md` |
| 12 | Craft Jury (on the actual media) | 7–35 | `12-craft-jury.md` |
| 13A | External research: context, RAG, memory, SLM, roles, checklists | 49, 51–54 | `13a-external-research-context-memory.md` |
| 13B | External research: agency practice, platforms, pipelines, TTS | 12–20, 36–40 | `13b-external-research-agency-pipelines.md` |
| 14 | Canon Prosecutor | 76 | `14-canon-prosecutor.md` |
| 15 | Canon Defender / Failure-to-consume | 77 | `15-canon-defender.md` |
| 16 | Requirement-model builder | 6, 13, 36, 38, 39, 40, 61 | **stopped before writing** (quota); Part 9 written by the lead from councils 03, 04, 05, 09, 12, 13B and the raw case extract `16-marketplace-cases-raw.txt` |

Neither 14 nor 15 issued the verdict; the lead did (Part 12 §2). Councils 14 and 15 completed their briefs before being stopped; both are in `council-reports/`.
