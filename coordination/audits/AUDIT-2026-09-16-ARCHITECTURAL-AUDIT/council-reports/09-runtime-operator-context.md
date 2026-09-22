# Agent 9 — Runtime / Media Agency Operator / Context-window council

Read-only audit. MI main @ 3bb9a3c3 (verified `git rev-parse HEAD`). Cumin job evidence @ `de1f978` (branch head 1aea4d2 adds one sync commit). PR #103 branch head `1de2b37`. Case-001 raw @ `work/pilot-upwork-intro-video-v4` (f6ca66f); case-002 raw @ `work/upwork-portfolio-samples-2026-09-15` (b4b77fa).

Working files (scratch only): `agents/a09/` — `classify_skill.py` + `classify_dump.json` (paragraph classifier), `measure_bootstrap.py` + `bootstrap_measure.json` (read-list measurement), `cumin/` (extracted job files), `cases/` (case files from 1de2b37).

Process note: one accidental write occurred — `classify_skill.py` v1 dropped `classify_dump.json` into the two skill directories (untracked); both files were deleted in the same minute and `git status --short` is clean. No tracked file was touched.

Label key: **OBSERVED** (read from bytes / computed), **INFERENCE**, **HYPOTHESIS**, **UNKNOWN**.

---

## Findings ranked

1. **The operator is a bookkeeper by instruction mass.** Keyword-vote classification of the five `/media-agency` files (8,035 words): PROCESS/BOOKKEEPING 48.3 %, QA-CHECK 25.2 %, TOOL/ROUTE 14.7 %, EXPERT/CREATIVE 11.7 % (upper bound; a hand-strict count of paragraphs that actually say what makes an ad work is ≈ 360 words ≈ 4.5 %). The sync skill is 94 % process. OBSERVED (`agents/a09/classify_skill.py`).

2. **What the operator must hold before it reads the brief is ~85–120 k tokens, and the largest single block (PROFILE.md, 98.9 KB ≈ 22–25 k tokens) is commercial positioning, not craft.** The expert content it is given for the creative decision is one 14-row table in the middle of PRODUCTION-WORKFLOW (§5 of 14) plus 21 pack CHECK lines loaded once per session at bootstrap. OBSERVED (`measure_bootstrap.py`: 479 KB / 63 k words across the read list).

3. **Every human rejection in case 003 landed on a dimension no gate measured; every gate that ran passed.** V3's 9:16 had 15 text boxes, 0 deviations (`gen/final/v3/cuminco-chopsticks-9x16.qa.json`) and was rejected for "voices overlapping" and, one version earlier, "does not look like an ad at all". Across the three cases, 0 of 7 (003), ~8 of 13 (002: obstruction/reuse/voice), and the entire V1/V2 verdicts of 001 were outside every mechanised check. OBSERVED (HUMAN-VERDICTS ×3; `acceptance_learning` line in 003).

4. **The runtime loop (intake → spec → inject → route → bridge → predispatch → postdraw → repair → acceptance → memory → template) was never executed by any real production.** Of 17 runtime components, 5 were touched by case 003 (Canon lookup, PriceBook, provider_errors, compositor gates+tokens, canon.gate pre via CLI); 0 by cases 001/002 (their 30 and 40 job scripts import nothing from `runtime.*` or `canon.gate`). By LOC: 1,456 of 8,853 runtime lines (16 %) were imported by a production. No OUTCOME-EVENT was ever written for a real job. OBSERVED (import greps).

5. **Role collapse is total and no independent challenge step is mandated or executed.** One Claude session played strategist, creative director, copywriter, VO writer, casting, producer, router, dispatch engineer (450-line `dispatch.py`), compositor engineer (414-line `compose.py`), audio engineer, QA (self-rendered 20 of 21 check lines "pass"), ledger clerk and — in a second session under the same skill set — sync author of the case that judged its own job and of the gate that fixes it. `blueprint.reviews: []`; Karl/Ezra review is optional prose ("when the job is customer-facing copy"); the runtime's only critic is the human at release. OBSERVED.

6. **PA-D7 was self-certified "pass" by the operator although the Canon gate itself prints PA-D7 as NOT-MECHANISED ("remains a human / blueprint-model check").** This is the mechanism by which "does not look like an ad" reached the human: a semantic judgment recorded as a check line. OBSERVED (`prompts/packages/clip-1.gate.txt` vs `JOB.yaml blueprint.check_lines.PA-D7`).

7. **Human approvals in case 003 happened at the wrong level and time (K14).** Plates were accepted (13:46–14:06 Z) and clips 1/3/4 dispatched (14:06–14:09 Z) while the voice — the register-defining element — was still being rejected across rounds 1–4 (13:58–14:17 Z); the timeline was fixed from an 18-s plan before any VO existed (VO 14:21 Z); the ad proposition (brand early/throughout, product close, CTA) was never a separate approval and was first challenged at V2 after USD 5.08 of the USD 5.09. OBSERVED (`gen/ATTEMPTS.jsonl` timestamps; HUMAN-VERDICTS).

8. **The runtime's own "no frames → NOT-RUN, never PASS" doctrine is overridden by the skill.** `frame_hygiene.assess` returns NOT-RUN without a detector; QA-CHECKLIST D1 says "the human-eye frame pass is the release check today"; JOB.yaml D1 rows read "PASS (human eye…)". No post-draw gate report exists in the job tree (only 10 pre-dispatch `*.gate.txt`). Gates existed and were bypassed in 002 (PD-06) and, for post-draw, in 003 too. OBSERVED.

9. **`check_vo_schedule` (PR #103) has zero callers.** It is the second gate family (after the compositor five) that exists only as a library function plus tests; the skill says "run the existing runtime gates" but no shared compositor or assembler calls them — every job writes its own. `wall_obstruction` lives only in the job's `compose.py` with a film-specific wall model ("the top 8 % of the frame, which is always wall in this film"). OBSERVED.

10. **The learning loop is prose-only.** Outside `.claude/skills/**` and `docs/media-agency-operator.md`, `git grep pending_sync|learning_status|LEARNING-PACKET` on main returns nothing; no `.github/workflows`; `check_case.py` validates case structure and the accepted asset's sha (n/a for a rejected job); tests run it only on case 001. Whether the next job reads the cases, applies candidate patterns, or calls promoted gates is enforced by nothing. OBSERVED.

11. **Instruction-hierarchy conflicts exist at HEAD.** (a) PRODUCTION-WORKFLOW §7 still instructs a workaround for the per-1000-characters PriceBook bug that PR #102 fixed at 3bb9a3c (the job noted "PR #102 fix verified") — by SKILL.md's own rule "HEAD wins and this skill is defective"; (b) SKILL.md forbids one-off gates while §9/§10 make a one-off dispatcher and compositor the only production path; (c) PROJECT-MEMORY §7 trap 8 ("No mandatory human-in-the-loop step exists in the production API architecture") vs runtime `acceptance.py` (C-8, human-only release) — the operator reads both. OBSERVED.

12. **The retrieval → decision chain is demonstrably leaky in the one place it can be traced.** `template.learning_applied` lists SPEAKER_MICROQUALIFICATION and CROSS_CLIP_VOICE_CONTINUITY as applied (knowledge retrieved, entered context), yet dependent clips were dispatched before the voice gate, and `qa.voice_continuity.narrator_identity_same` was pre-filled "PASS by construction… human ear to confirm". Entered context ≠ changed the decision. OBSERVED.

---

## Q1. What the operator receives when `/media-agency` is invoked

### 1a. Read list, in order, with sizes

Token estimates: bytes/4 and words×1.33 (both shown; prose in this repo sits between them). Command: `agents/a09/measure_bootstrap.py` (USD 0, local; the routing-table and pack-check commands from BOOTSTRAP.md were executed as written).

| # | When | File / command output | Bytes | Words | Tokens (b/4 – w×1.33) |
|---|---|---|---|---|---|
| 0 | always (memory) | `CLAUDE.local.md` | 364 | 48 | 64–91 |
| 1 | on invoke | `SKILL.md` | 10,157 | 1,468 | 1,952–2,539 |
| 2 | first job | `BOOTSTRAP.md` | 5,907 | 706 | 939–1,477 |
| 3 | every job | `PRODUCTION-WORKFLOW.md` | 19,869 | 2,803 | 3,728–4,967 |
| 4 | every job | `QA-CHECKLIST.md` | 9,547 | 1,554 | 2,067–2,387 |
| 5 | every job | `JOB-TEMPLATE.yaml` | 14,893 | 1,504 | 2,000–3,723 |
| | | **skill files subtotal** | **60,737** | **8,083** | **10.7–15.2 k** |
| 6 | bootstrap §2.1 | `PROJECT-MEMORY.md` §1,§2,§5,§7 | 21,286 | 2,864 | 3,809–5,322 |
| 7 | §2.2 | `coordination/CONTROL-STATE.md` §2,3,5,6,8 | 18,407 | 2,477 | 3,294–4,602 |
| 8 | §2.3 | `canon/CANON-SHAPE-v1.md` §4–5 | 3,241 | 483 | 642–810 |
| 9 | §2.4 | `canon/packs/pack-triggers-v0.yaml` | 9,801 | 997 | 1,326–2,450 |
| 10 | §2.5 | pack decision ids + CHECK lines (command output) | 4,556 | 728 | 968–1,139 |
| 11 | §2.6 | routing table (command output, 79 lines) | 13,859 | 1,389 | 1,847–3,465 |
| 12 | §2.7 | `runtime/ALPHA-1.md` §What exists / does not | 3,374 | 448 | 596–844 |
| 13 | §2.8 | `production-learning/README.md` | 1,619 | 195 | 259–405 |
| 14 | §2.8 | case 001: README, PROMOTION-QUEUE, ACCEPTED-TEMPLATE, ROUTE-OBSERVATIONS | 19,288 | 2,387 | 3,175–4,821 |
| 15 | §2.8 | case 002: README, PROMOTION-QUEUE, ROUTE-OBSERVATIONS | 17,904 | 2,261 | 3,007–4,477 |
| 16 | §2.9 | `$UPWORK/PROFILE.md` (named sections; whole file measured) | 98,870 | 16,865 | 22,430–24,718 |
| 17 | §2.10 | `$UPWORK/LOG.md` last entry | 5,729 | 925 | 1,230–1,432 |
| | | **bootstrap subtotal** | **217,934** | **32,019** | **42.6–54.5 k** |
| 18 | workflow §3 | case 001 + 002 `SYSTEM-DEFECTS.yaml` | 17,967 | 2,130 | 2,833–4,492 |
| 19 | workflow §2 | `runtime/canon/KIND-NR-BINDING-v0.yaml`, `runtime/contracts/DELIVERABLE-KINDS.yaml` | 10,113 | 1,229 | 1,635–2,528 |
| 20 | job end | `cases/UPWORK-INTRO-001/TIME-AND-COST.yaml` (baseline) | 11,213 | 1,333 | 1,773–2,803 |
| | | **grand total named by the skill** | **≈ 318 KB** | **≈ 44.8 k** | **≈ 60–80 k** |
| — | *not* read as text | the two compiled packs (whole) | 87,529 | 8,854 | 11.8–21.9 k |
| — | *not* read as text | `INJECTION-PREFIX-v1.md` | 5,399 | 785 | 1,044–1,350 |

OBSERVED. Notes: (i) the 87 KB of compiled pack text is what the runtime *injects* (prefix sha recorded in JOB.yaml, "5298 tokens"), but BOOTSTRAP instructs the operator to load only decision ids + CHECK lines (4.6 KB); nothing in the job tree proves the operator read the pack bodies — UNKNOWN whether the doctrine text itself ever entered the operator's context. (ii) PROFILE.md is by far the largest item and is loaded before any brief. (iii) The JOB.yaml the operator writes and re-reads reached 65.9 KB (≈ 16 k tokens) by V3 — larger than all five skill files together.

### 1b. Paragraph classification (Red-team Q8/Q9)

Method: blank-line / table-row / list-item paragraphs; weighted keyword vote per paragraph; words counted per class; ties → PROCESS. Reproducible via `agents/a09/classify_skill.py`. This is a heuristic; the EXPERT bucket is inflated by QA rows that mention "headline/CTA/crop" and by the frontmatter description.

| File | Paragraphs | Words | PROCESS | QA | TOOL | EXPERT |
|---|---|---|---|---|---|---|
| SKILL.md | 56 | 1,468 | 48.8 | 23.7 | 9.3 | 18.1 |
| PRODUCTION-WORKFLOW.md | 91 | 2,803 | 54.1 | 12.7 | 18.7 | 14.5 |
| QA-CHECKLIST.md | 80 | 1,554 | 19.7 | 66.0 | 4.4 | 9.8 |
| JOB-TEMPLATE.yaml | 22 | 1,504 | 56.1 | 17.0 | 19.4 | 7.5 |
| BOOTSTRAP.md | 35 | 706 | 70.8 | 6.2 | 22.9 | 0.0 |
| **all five** | **284** | **8,035** | **48.3** | **25.2** | **14.7** | **11.7** |
| media-agency-sync/SKILL.md | — | 1,304 | 94.3 | 2.1 | 3.5 | 0.0 |

Hand-strict EXPERT count (paragraphs that state advertising craft rather than name a field): WORKFLOW §5 table + "Canon constrains; it does not direct" (~115 w), Karl/Ezra line (20), Hindi origination (25), portfolio-batch "spread" paragraph (~60), TEMPLATE §5 field names (113), SKILL overview "a technically perfect picture can still be a bad ad" (~30) ≈ 360 words ≈ **4.5 %**. INFERENCE: the honest range for expert content is 4.5–11.7 %; every number above ~5 % is field names, not craft.

What the operator is *not* given anywhere in the skill: what a product hero is, what an opening does, how an end card / CTA / brand mention are structured, how VO pacing is derived, what "hierarchy" means beyond a field name. The ABCD knowledge that would have prevented DF-07 sits in accepted Canon (`google-abcd-video-ads`, per LEARNING-PACKET) inside the uncompiled `commercial_communication` pack. OBSERVED (LEARNING-PACKET `canon_gaps`).

---

## Q2. Role collapse (Q11)

Roles the single operator played in `AGY-2026-09-15-CUMINCO-CHOPSTICKS-001` (all OBSERVED in `JOB.yaml`, `tools/`, `prompts/` @ de1f978):

| Role | Evidence |
|---|---|
| Source researcher | `source/blog.html`, `pdp-ramen-bowl.html`, `collection-ramen-bowls.html`, `pins/gemini-api-pricing.html` |
| Strategist / account | `intake.commercial_objective` (founder-facing capacity demo), `audience`, `channel`, `package` mapping to PROFILE.md |
| Creative director | `blueprint.concept`, `first_read`, `hook`, `attention_order`, `brand_world`, 5 beats with shot/action |
| Copywriter | `mandatory_text` (verbatim blog fragments chosen), V3 additions t6/t7; the film's 6 VO lines |
| Prompt writer | `prompts/PROMPTS.yaml` (126 lines, 10 prompts) |
| Casting / voice director | 26 TTS takes over 5 rounds across 3 providers; style prompts ("bubbly") |
| Producer / planner | `plan.assets[]` with dependencies, deliverables, micro-qualifications, expected spend |
| Router | route cells, evidence status and prices chosen by hand from the bootstrap table (`plan.assets[].route`) |
| Dispatch engineer | `tools/dispatch.py` (450 lines: ledger, cap check, 10 provider endpoints, Vertex/Gemini/fal/Sarvam/ElevenLabs transports) |
| Compositor engineer | `tools/compose.py` (414 lines), `overlay_text_video.py` (189), `adcomp_pilot.py` (261) |
| Audio engineer | ffmpeg chain: edge trim, atempo, loudnorm, sidechain duck, limiter |
| QA | rendered PA-D1..D10 / CA-D1..D11 (20 pass, 1 n-a, 0 deviations); B rows; D rows on 12 sampled frames per clip; CF rows per geometry |
| Ledger clerk | ATTEMPTS.jsonl (51 records), LEDGER.jsonl, TTAO stamps, KPIs |
| Learning author | LEARNING-PACKET.yaml (244 lines: 8 defects, 6 observations, 5 patterns, 7 engineering changes, 1 Canon gap) |
| Sync author (second session, same skill set) | PR #103: 10 case files (574 lines), `check_vo_schedule` (35 lines) + tests (29 lines) |

**Independent challenge/critique step mandated?**
- Skill: PRODUCTION-WORKFLOW §5 — "Consult Canon persona review (Karl disconfirmer, Ezra copy) **when** the job is customer-facing copy; their verdicts are input, not acceptance." Conditional, advisory. JOB-TEMPLATE `blueprint.reviews: []` field exists. OBSERVED.
- Runtime: `runtime/loop/acceptance.py` forbids `judge:`/`model:` in the release path (ACCEPTANCE_AUTOMATED_JUDGE); `repair.py` proposes bounded repairs from failed check ids; no critique/disconfirmation stage exists in `runtime/loop/__init__.py`'s seven steps. OBSERVED.
- Canon: `critique_and_effectiveness` fired for the Cumin job and is uncompiled (`canon.missing_domains`). The one Canon domain literally named "critique" was absent in all three productions. OBSERVED.

**Executed in the three cases?** Case 003: `blueprint.reviews: []` — no. Cases 001/002: verdict files are `chat_only_human_evidence`; no review artifact other than the human's. **No independent critique ran in any of the three.** OBSERVED (absence).

INFERENCE: the only adversarial signal in the whole system is the human at release, which is why the proposition-level failure (DF-07) surfaced at V2 after the money was spent.

---

## Q3. Runtime vs production reality

Runtime non-test code: 8,853 lines in 58 files; 480 test functions in 34 files; 14-run dry battery (`runtime/battery/results/2026-09-14/SUMMARY.yaml`: 6 accepted, 2 abandoned on PRE_DISPATCH_GATE_FAIL, 1 abandoned on repair exhaustion, 3 refused at intake, 1 at spec, 2 manual_route_required). OBSERVED.

"Invoked by case" = a job-branch script imports it or a job artifact proves it ran. Greps: case 001 (30 pilot `.py`) and case 002 (40 pilot `.py`) contain **zero** `runtime|run_gate|canon.gate` references; case 003 `tools/*.py` import `runtime.compositor.{gates,tokens}`, `runtime.errors`, `runtime.execute.provider_errors`, `runtime.route.cli.build_router`. No `*.gate.txt/json` exists under `pilots/**` on either raw branch (only EVAL-040 lab runs carry gate reports). OBSERVED.

| Component | Code | Tests | Dry battery | 001 | 002 | 003 |
|---|---|---|---|---|---|---|
| Intake (`intake/intake.py`) | yes | yes | yes | no | no | no (hand-filled `intake.*`) |
| Spec compiler / planner seam / blueprint planner / text strategy / acceptance style | yes | yes | yes | no | no | no |
| Canon lookup + injection prefix (`canon/packs.py`, `normalize.py`) | yes | yes | yes | no | no | **yes** — `lookup(normalize(brief.job.json))`, prefix sha recorded |
| Template library (`canon/templates.py`) | yes | yes | B14 | no | no | no (template read by hand; `reused: none`) |
| Router decision/evidence (`route/decision.py`, `evidence.py`) | yes | yes | yes | no | no | no (cells chosen by hand) |
| PriceBook (`route/price.py` via `build_router`) | yes | yes | yes | no | no | **yes** (`dispatch.py`; A5 quotes) |
| Execution bridge / manifest / authorisation | yes (dry-only; `live` refuses) | yes | yes | no | no | no (job-local `dispatch.py` + pilot transports) |
| Pools (`execute/pools.py`) | yes | yes | yes | no | no | no (shape copied into JOB.yaml by hand) |
| Provider errors (`execute/provider_errors.py`) | yes | yes | — | no | no | **yes** |
| Package renderer (`loop/package.py`) | yes | yes | yes | no | no | no (packages written by hand) |
| Pre-dispatch gate (`loop/predispatch.py` over `canon.gate`) | yes | yes | yes | no | no | partial — `canon/gate/run_gate.py pre` CLI ×10, not the runtime wrapper |
| Post-draw gate + frame hygiene | yes | yes | yes (synthetic) | no | no | **no** (human eye; no post report) |
| Repair (`loop/repair.py`) | yes | yes | B12/B13 | no | no | no |
| Acceptance state machine | yes | yes | yes | no | no | no (verdicts in `versions[]`) |
| Memory / OUTCOME-EVENT | yes | yes | yes (`dry_run: true`) | no | no | no |
| Compositor gates + tokens | yes | yes | — | no (created from 001 afterwards) | no (bypassed, PD-06) | **yes** (6/6 functions called) |
| Alpha runner / CLI / policy profiles / evidence map | yes | yes | yes | no | no | no |

**Fractions.** Components touched by any real production: 5 of 17 (29 %), all in case 003. LOC imported by a production: `compositor/gates.py` 199 + `tokens.py` 39 + `execute/provider_errors.py` 88 + `route/price.py` 270 + `route/cli.py` 241 + `canon/packs.py` 346 + `canon/normalize.py` 229 + `errors.py` 44 = **1,456 / 8,853 = 16 %**. The loop package (`runtime/loop/*`, 1,470 lines) and the bridge (`execute/bridge.py` 426): **0 %**. Separately, `canon/gate` (3,276 lines) ran once in production, pre-dispatch only, via CLI. OBSERVED.

**Did `compose.py` reimplement runtime gates?** No — it *imports* them and calls `check_fit`, `check_text_bounds`, `check_contrast`, `card_geometry`, `check_geometry`, `check_disjoint`. What it implements itself, and the concept diff:

| compose.py concept | Runtime / canon.gate equivalent | Diff |
|---|---|---|
| `luminance_samples` (5×5 grid + extremes over 4-fps probe frames) | `check_contrast` takes samples; "the gate never opens an image" | Sampling correctness (V1's 4-frame probe, DF-04) is by design outside the gate; the failure lived in the caller |
| `wall_obstruction` (per-column wall model from the top 8 % rows; > 2 % non-wall fails) | none (CF2 is a checklist row; case 002 wanted SUBJECT_AWARE_CROP_ANCHORING) | New, film-specific heuristic; not a subject mask |
| word-wrap + candidate bands + stacking (`y_cursor`, `min_gap_px + 10`) | none (case 002 candidates STACK_LEVEL_FIT / READABILITY_MARGIN not in runtime) | Job-local layout engine |
| backing card inside safe area (`top_min`) | `check_text_bounds` with `container` | Candidate BACKING_CARD_IN_SAFE_AREA — caller must pre-inset |
| `DECK` byte-check (C6) | none | Job-local |
| C8 ffprobe export facts | canon.gate DISPATCH-ASPECT (NOT-RUN: no descriptor supplied) | Job-local |
| audio chain (trim, LUFS, duck, limiter) | none | No runtime audio module exists |
| VO placement `VO = {beat: (file, start_s)}` hand-set | none at the time; `check_vo_schedule` after PR #103 (0 callers) | The gate now exists but nothing calls it |
| timeline `BEATS` fixed in code before VO measured | none | DF-05 / VO_FIRST_TIMELINE candidate |

Case 002's `compose_v4.py`/`compose_pf.py` import only `adcomp`; they do not import the pilot's own `design4.py` (which had tokens/contrast/bounds) nor the runtime — three copies of the same gate ideas existed (runtime, pilot design4, job compose) and the deliverable path used the one without gates. OBSERVED.

---

## Q4. Gates bypassed vs gates passed-but-rejected

**Bypassed (case 002):** TEXT_BOUNDS, CONTRAST, CROP_FIT existed in `runtime/compositor` and in pilot `design4.py`; `compose_v4/compose_pf` used neither (SD-HD-01/02/04/06/11 "gate existed; NOT RUN on this path"). **Bypassed (case 003):** post-draw gate + `frame_hygiene.assess` (no post-draw report; D1 by eye); `run_gate pre` ran without a dispatch descriptor, so DISPATCH-ASPECT was NOT-RUN on all 10 packages. OBSERVED.

**Passed-but-rejected (case 003):** V2 9:16 — 8 boxes, 0 deviations, CF2 PASS, rejected on structure; V3 9:16 — 15 boxes, 0 deviations, C6/C8 PASS, rejected on VO overlap. The 4:5 / 1:1 files carried 8–11 deviations each and CF2 FLAGGED on every version and were never the reason for rejection. OBSERVED (`*.qa.json` counts above).

**Table — what humans actually judged vs what any gate checks**

| Human criterion (verbatim source) | Case/version | Mechanised anywhere? |
|---|---|---|
| "commercially clear / strong sales logic" | 001 V1 | no |
| "actual video proof too small"; "too much phone/mockup framing" | 001 V1/V2 | no (CA-D2 zone check is prompt-vocabulary only) |
| "opening not visually exceptional enough" | 001 V1/V2; 003 V2 "the opening is missing" | no |
| "presenter blocks too long"; "pacing too rushed" | 001 V1/V3 | no (CA-D10 checks that a duration is *stated*) |
| "creative range insufficient" | 001 V1/V4 | no |
| text cut off / colour lost / cropped / mixed card geometry | 001 V3; 002 B1 | **yes** — C1–C4 (created after 001; bypassed in 002) |
| "voice horribly robotic" / "voice is shit" / "all three are robotic" / "shrillness… missing" | 001 V3; 002 N2; 003 voice rounds | no (D10 transcript is presence; D14 human ear) |
| direct-to-camera speaker missing → hard requirement | 001 V3 | no |
| offer/code collision | 001 V4 | **yes** — C5 disjoint |
| "and it can't suck" phrase lost | 001 V4 | no (C6 byte-check only covers strings in the deck) |
| text over figure/product; banner overlapping photos | 002 HD-03/05/07/08/09/10; 003 V1 "text is coming on figures" | no in runtime; CF2 checklist; job-local `wall_obstruction` in 003 |
| "voice not continuous", two narrators | 002 N1/N2 | no (D14 human ear) |
| "images that are scrappy" | 002 N1 | no |
| "random audio" (levels, pumping, shifted lines) | 003 V1 | no (LUFS/duck are measurable; no module) |
| "her lips are moving" under VO | 003 V1 | no (D3/D5 identity/face rows exist; no mouth-motion row) |
| "closing shot should have cumin product and final caption" | 003 V2 | no; PA-D7 NOT-MECHANISED per gate; Canon pack uncompiled |
| "does not look like an ad at all" | 003 V2 | no |
| "the voices are overlapping" | 003 V3 | **now yes** — `check_vo_schedule` (0 callers) |

INFERENCE: the gates measure *layout arithmetic on numbers the caller supplies*; acceptance depends on delivery (voice), structure (ad-ness), obstruction and continuity — none of which the gates see, and two of which (structure, delivery) are not gate-shaped at all. The 003 case file says it in one line: "every gate that existed passed on every version; the user rejected on what no gate measured."

---

## Q5. Deterministic vs judgment — classification of the three cases' defects

| Class | Defects |
|---|---|
| **DETERMINISTIC (should be code)** | 001 SD-01 bounds, SD-02 contrast, SD-03 crop declaration, SD-04 tokens, SD-07 disjointness, SD-09/10 transient classification, SD-11 pool liquidity; 002 HD-01/02 bounds+margin, HD-04 contrast, HD-06 crop anchor, HD-11 contain for product proof, HD-12 stack-level fit, PD-01/03/08/09 preflight/ledger existence; 003 DF-02 audio levels (LUFS/duck measurable), DF-05 duration vs plan, DF-06 attempt-id collision, DF-08 VO overlap/overrun, 4:5/1:1 copy-zone absence (given a wall/subject model), plus sampling density for contrast (V1's 4 frames) |
| **RETRIEVAL-SUPPORTED REASONING** | 003 DF-07 ad structure (ABCD in accepted Canon, uncompiled); 001 V1/V2 proof size / phone framing / opening (craft doctrine); 002 HD-03/05 type over the figure (CA-D2/D3 exist as doctrine); DESIGN_REUSE_PROVENANCE (bookkeeping + reasoning); route choice for long narration (RO-05 existed before 003 chose Sarvam takes again) |
| **LEARNED JUDGMENT (operator craft)** | VO-first timeline (DF-05 as pacing craft), CLOSED_MOUTH_UNDER_VO prompt craft, GEOMETRY_NEEDS_ITS_OWN_PLATES, hierarchy-survives-fit (CF5), candidate copy-band ordering |
| **HUMAN JUDGMENT** | "does it look like an ad", "competent not extraordinary", voice naturalness/"bubbly", narrator identity by ear (D14), plate acceptance on sight, "creative range" |
| **EMPIRICAL MODEL CAPABILITY** | 003 DF-01 embossed mark garbled from reference, DF-03 Veo animates mouths under VO, Gemini TTS false-positive refusal; 002 RO-01 Veo extend restructures narration, RO-02 native voice varies across generations; 001 RO-05 Sarvam long-read cadence, RO-06 Kling signage sharpening |

**Conversions judged right / wrong:**
- `check_vo_schedule` from DF-08 — **right** (pure interval arithmetic on measured durations); defect: no enforcement path (0 callers), so it is a rule without a place to run.
- `wall_obstruction` — **right in kind, wrong in form**: obstruction of the subject by copy is deterministic *given a subject mask*; the job's model ("median of the top rows, which is always wall in this film") is a per-film assumption; promoting it verbatim would encode this film into the runtime. Case 002's SUBJECT_AWARE_CROP_ANCHORING asks for the same input (a subject box) — the two candidates should share one primitive.
- PA-D7 rendered "pass" in `blueprint.check_lines` — **wrong direction**: a human/semantic check (per the gate's own NOT-MECHANISED line) was self-certified as a check line, and A2 then reported "20 pass, 1 n-a, 0 deviations". Same for `muted_test: yes` and `hook` — recorded as fields, never challenged.
- `voice_continuity.narrator_identity_same: "PASS by construction… human ear to confirm"` — **wrong**: a human-ear row pre-filled by the operator.
- D1 frame text: runtime says NOT-RUN without a detector; checklist converts to PASS-by-eye — **doctrine inverted by prose**.
- "does it feel like an ad" — correctly *not* a gate; but nothing else carries it either (no compiled pack, no critique step, no AD_STRUCTURE_MINIMUM fields in the template at HEAD).

---

## Q6. Human-in-the-loop model — actual intervention points

Estimates are mine (INFERENCE) unless a timestamp is cited (OBSERVED from `ATTEMPTS.jsonl` / JOB.yaml / HUMAN-VERDICTS).

| # | Intervention (case 003 unless noted) | UTC | Information gain | Review cost | Cost of being wrong if skipped | Downstream spend that depended |
|---|---|---|---|---|---|---|
| 1 | Start-of-job bundle: cap USD 8, freeze 5-string deck + 5 VO lines, pool attestation, ending choice — four questions in one turn | 13:28:37 | high (money, words) but **bundled** — the blueprint was never approved separately | ~5 min | unauthorised spend / rework | USD 5.09 |
| 2 | MQ1 plate-H1 r1/r2 → "r2" | 13:42–13:46 | medium (bowl fidelity, grip) | ~3 min | wasted clip | clip-2 0.60 + 4 plates 0.27 |
| 3 | MQ1 clip-2 → "accpet" | ~13:50 | medium-high (grip animates) | ~3 min | 4 bad clips | clips 2.40 |
| 4 | plates A r2 / H2 / H3 "good to go"; plate-B "accepted" | ~13:57–14:06 | medium (visual world) | ~5 min | all clips redrawn | clips 3.00 + music + VO |
| 5 | Voice rounds 1–5 (26 takes; verdicts "all three are robotic" → direction → "leda… slower" → "bubbly") | 13:58–14:17 | **high** — the film's register — but clips 1/3/4 were dispatched 14:06–14:09 during rounds 2–4 | ~20 min | film re-cut around a rejected voice | VO 0.16 + music 0.06 + (in practice) nothing, because dependents were already bought |
| 6 | V1 REJECT ("random audio", lips, text on figures) | ~14:52 → 15:0x | high (3 defect classes) | ~5 min | — | 1.20 redraws + 35 min |
| 7 | V2 REJECT ("does not look like an ad", no close, no opening) | ~15:2x → 15:3x | **very high; proposition-level**; arrived after USD 5.08 of 5.09 | ~5 min | — | 0.01 + V3 build |
| 8 | V3 REJECT ("voices overlapping") | 16:0x → 03:45 (+1 d) | low (a deterministic defect) | ~3 min + overnight | — | 0 |
| 001 | presenter judged only at V4 after V1/V2 built around it (SD-12) | 14 Sep | high, late | — | USD 8.08 on unqualified presenter | — |
| 002 | "go" → dispatch in the same turn (PD-03); copy invented during execution (PD-02); B2 acceptance implicit | 15 Sep | — | — | 10 known-class defects in one export | USD 4.66 |

**Where approval happened at the wrong level/time (K14), OBSERVED:**
1. Plates and clips approved/dispatched (13:46–14:09) before the ad proposition (brand early/throughout, product close, Direction) was ever put to the human; the proposition was first challenged at V2 (15:3x). The blueprint was shown only inside the start-of-job bundle with the cap question.
2. Timeline fixed (18-s plan; `BEATS` windows in `compose.py`) before any VO existed; VO lines generated 14:21 after every clip (14:06–14:17); V3 then placed VO by hand from the 18-s plan → DF-05, DF-08.
3. Voice — the element the brief named first ("a very calm empathetic voice") — was qualified last; `plan.micro_qualifications[1].human_gate_verdict: null` while dependents were already bought.
4. Copy deck "frozen" at 13:28 with five strings; V3 needed two more (product name, cuminco.com) because the structure that needed them did not exist at freeze time.
5. `human_review_cycles: 10`, of which 4 component gates + 5 voice rounds preceded the one review (V2) that carried the decisive information.

---

## Q7. Context-window diagnosis

**Tokens held at the creative-direction decision (stage 5):** skill files ≈ 11–15 k; bootstrap reads ≈ 43–55 k (PROFILE.md alone 22–25 k); workflow §2–§4 references (KIND-NR-BINDING, DELIVERABLE-KINDS, SYSTEM-DEFECTS ×2) ≈ 4.5–7 k; the brief, `brief.job.json`, intake/NR/template/canon sections of JOB.yaml as written so far ≈ 3–5 k; the runtime lookup output (sha + counts, not text). **≈ 62–82 k tokens** before the first creative sentence, if the session is fresh; more in a long-lived session (BOOTSTRAP §Refresh keeps the loaded context across jobs). OBSERVED sizes; INFERENCE on the sum.

**Positioning:**
- *Start*: `CLAUDE.local.md` (48 words, role + "invoke /media-agency"), then SKILL.md (overview, authorities, non-negotiables, resolved failure classes, red flags) — process and prohibitions.
- *Early-middle*: BOOTSTRAP reads — project map, control state, Canon shape, trigger table, 21 CHECK lines, routing table, Alpha limits, two cases, PROFILE.md, LOG.md. The 21 CHECK lines (the only doctrine the operator is told to hold) are ~4.6 KB inside a ~218 KB block, loaded once per session.
- *Middle*: PRODUCTION-WORKFLOW §5 (the 14-row blueprint table) sits at roughly line 150–175 of 330, after §0–§4 (git, clock, intake, template, lookup) and before §6–§14 (plan, route, preflight, dispatch, composition, QA, repair, release, packet).
- *End*: the brief and the job's own record — the most task-specific material arrives last and is then continuously re-read as JOB.yaml grows (65.9 KB by V3).

**Instruction-hierarchy conflicts (OBSERVED at HEAD 3bb9a3c):**
1. PRODUCTION-WORKFLOW §7: "Known defect (15 Sep 2026)… PriceBook multiplies a per-1000-characters price by the raw character count… until it is fixed, cross-check against `eval/harness-v2/pricing.py`" — PR #102 (cf8f02f, in HEAD) fixed it; JOB.yaml A5 says "PR #102 fix verified". Skill instructs a workaround for a non-existent defect; by SKILL.md's rule this makes the skill "defective".
2. SKILL.md "run the existing runtime gates, never a weaker one-off version" vs §9 ("paid dispatch today is done the way the accepted pilot did it: per-route recipes…") and §10 (composition in the job's own script). There is no shared assembler; a one-off is the only path. `wall_obstruction` and the audio chain are one-off gates by necessity.
3. QA-CHECKLIST D1 ("the human-eye frame pass is the release check today") vs `runtime/loop/frame_hygiene.py` ("No sampled frames → NOT-RUN, never PASS"; no detector → NOT-RUN). JOB.yaml D1 rows are "PASS (human eye…)".
4. PROJECT-MEMORY §7 trap 8 ("No mandatory human-in-the-loop step exists in the production API architecture") vs `runtime/loop/acceptance.py` (C-8: only a person accepts; automated judge refused). Both are on the read list.
5. SKILL.md "Alpha-1 bounds what `runtime/alpha` auto-routes; it does not bound what the agency may produce" vs ALPHA-1.md / C-7 (`multi_shot_story` excluded) — resolved by the job as "outside Alpha-1, under the user's job-specific authorisation" (JOB.yaml `deliverable_type` comment); consistent, but the operator carries two authorities for one question.
6. `CLAUDE.local.md` "Current repository authority overrides memory" and SKILL.md "HEAD wins" agree with each other; both are silent on what to do when HEAD's own files disagree (1, 3, 4 above).

HYPOTHESIS (not provable from bytes): with ~70 k tokens of process/authority text ahead of it and the craft content a 14-row table, a model asked "render PA-D7 pass|n-a|deviation" will render "pass" — the instruction format asks for a verdict token, not for the argument. The 003 case file's own root cause ("PA-D7 rendered 'pass' on a thin line") is consistent with this.

---

## Q8. Sync workflow — what `/media-agency-sync` produces and what enforces the loop

**PR #103 (1de2b37 vs 3bb9a3c) produced:** `production-learning/cases/CUMINCO-CHOPSTICKS-003/` — README, OUTCOME, HUMAN-VERDICTS (55 lines), REVISION-TRACE (92), TIME-AND-COST (85), SYSTEM-DEFECTS (80), ROUTE-OBSERVATIONS (61), PROMOTION-QUEUE (88), EVIDENCE-MAP (37); `production-learning/README.md` case list (+1 line); `runtime/compositor/gates.py` `check_vo_schedule` (+35) with 4 tests (+29). Then on the job branch (1aea4d2): exactly four JOB.yaml fields changed (`learning_status: synced`, `sync.case_id`, `sync.integration_branch`, `sync.integration_pr`). Five-class table: 1 promoted (VO_SCHEDULE_GATE), 8 candidate patterns, 6 directional observations, 1 Canon gap (report only), 4 not-promoted. OBSERVED.

**Mechanical enforcement of "production → learning → next production":**
- `check_case.py`: structural + honesty checks; byte-verifies the accepted asset (n/a for 003, rejected) — mechanical, but run by hand (no CI; `.github/workflows` absent). Tests exercise it on case 001 only.
- `runtime/tests` (480 functions): run by hand per the sync skill §5.
- Job-branch discovery: a shell snippet in the skill (prose).
- "The job is not closed on ACCEPT until the packet exists": prose; nothing on main reads `learning_status` (grep: 0 hits outside skills/docs).
- "Next job's startup refresh receives the merged learning": prose (BOOTSTRAP §2.8); nothing verifies a case was read or a candidate pattern applied; `template.learning_applied` is free text.
- Promoted gate → production: nothing calls `check_vo_schedule`; the next job's `compose.py` will be a new file.
- Canon gap → Controller decision: PR text only (by design).

Verdict: **prose-only loop with two manual mechanical stations** (case validator, unit tests). The one traceable "learning → decision" link in 003 (`learning_applied` 13 items) shows retrieval happened; the same job shows the retrieved rule (speaker/voice micro-qualification before dependents) did not govern dispatch order.

**Eight-state ledger for the two decisive 003 failures:**

| State | DF-07 "not an ad" | DF-08 VO overlap |
|---|---|---|
| knowledge exists | yes (ABCD in accepted Canon) | yes (interval arithmetic; text overflow analogue existed) |
| retrieved | no (`commercial_communication` uncompiled; recorded as missing domain) | no (no rule existed) |
| entered context | no | no |
| model understood | — | — |
| changed a decision | no | no |
| decision correct | no | no |
| survived production | n/a | n/a |
| QA detected | no — human did | no — human did; gate written afterwards, uncalled |

---

## Open questions / unknowns

1. **UNKNOWN** whether the operator ever read the two compiled pack bodies (87 KB) in any job; BOOTSTRAP loads only ids + CHECK lines; no artifact records a pack read.
2. **UNKNOWN** the exact PROFILE.md section sizes the bootstrap names (whole file measured: 98.9 KB); the named sections are likely 30–50 % of it — still the largest read.
3. **UNKNOWN** how many tokens the long-lived session actually held at V2 (chat transcript not in the repo); the estimate here is the instructed floor.
4. **UNKNOWN** whether Karl/Ezra persona review exists as an executable artifact anywhere (the skill names it; no file was located in this audit's scope).
5. Cases 001/002: whether `canon/gate/run_gate.py` was run by hand (no report files, no case mention) — treated as not run.
6. PR #103's GitHub body was not fetched (no network); the commit message and branch diff were used instead.
7. The `verdict` field of every ATTEMPTS.jsonl record is `pending` (never settled) — a small ledger-closure gap not investigated further.
8. Whether any repo test would fail if `check_vo_schedule` were deleted from every caller (there are none) — trivially no; recorded as the enforcement gap it is.
