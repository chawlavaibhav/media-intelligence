# Media Intelligence P1 — independent assessment and execution plan

Controller, 2026-09-22. Read-only. No paid call, no repository mutation (one housekeeping deletion: the runtime's own untracked fixture spill in the sync worktree, created while reproducing the Mokobara Canon lookup).

Evidence base: main @ `c88c0d5`; PR #104 (`work/agency-sync-2026-09-21` @ `f57246f`, unmerged); PR #103 (case 003, unmerged); PR #84 (CANON-015 retrieval, draft, unmerged); job branches for Lane A, Lane B, V2, CQ-001, Mokobara, Cumin; `runtime/` (16,099 lines Python, 520 unit tests passing); Canon (`canon/`); capability map and taint register. Labels: **OBSERVED** = read in the repo or reproduced by command; **INFERRED** = my judgement; **UNKNOWN** = not in the repo.

---

## A. Independent assessment

### The one-paragraph answer

**Yes, build P1 now — but not the P1 that the documents imply.** The evidence that matters is real: seven production cases in six weeks, six of them accepted by the customer (five in the last three days), each with a ledger, a frozen brief, deterministic checks and an independent checker; a 1,300-claim accepted knowledge corpus; and a runtime with sound contracts and 520 passing tests. What is *not* real is the premise that "the runtime does the five stages and just needs a customer front-end". The runtime today performs stage 2 (normalise), a fraction of stage 3 (two of ten Canon packs), stage 4 in dry mode, and the deterministic gates. It contains no reasoning-model call, no live provider transport, no persistence beyond a temp directory, and it has never produced a customer artifact. Every accepted film was made by a Claude session reading the skill documents and running ~850 lines of per-job tooling copied branch to branch. P1 is therefore not "wire the runtime to a UI"; it is **"turn the Claude-operated agency workflow into a product in which code holds the state and the LLM is a component"**. That is a 4–5 week build on the existing code, not a rebuild, and not a research programme.

### LLM operating a repository vs product orchestrating LLMs — where we are

| Role today (OBSERVED on all five recent jobs) | Who does it today | Who must do it in P1 |
|---|---|---|
| Hold job state, remember what stage we are at | The Claude session's context; Markdown/YAML on a branch | A job store + state machine (code) |
| Decide the next step, resume after a drop | The session; a human re-briefs a new session after a drop | The orchestrator (code); resume is a restart |
| Understand the brief, list mandatory items, ask questions | Claude, as prose in `01-INTENT.md` | An LLM call with a fixed output schema, driven by code |
| Retrieve Canon | Code for 2 packs; Claude grepping YAML for the rest | Code for all ten (see C) |
| Write the board, copy deck, prompts | Claude, as JSON + text files | LLM call (board/copy deck) + deterministic prompt builder (code) |
| Choose routes, quote prices | Claude, using `PriceBook` + taint register by hand | Code (already exists in `runtime/route`) |
| Send paid calls, keep the ledger, enforce the cap | `tools/dispatch.py` on the job branch, run by Claude | The same code, moved into the runtime, called by the orchestrator |
| Render text, assemble, run DET checks | Per-job `render_text.py`, `assemble.py`, `qa_checks.py`, run by Claude | The same code, generalised, called by the orchestrator |
| Independent check | A second Claude session, by process rule | An isolated LLM call with DET outputs + contact sheets, by construction |
| Accept / repair / release | The customer in chat; Claude edits and re-runs | The customer in the product; the orchestrator runs a bounded repair |
| Learn | `/media-agency-sync` by Claude, promoted by Controller | Auto-captured case skeleton; promotion stays human |

### What I agree with in the founder's framing

- Five stages, in that order, with Canon at stage 3 and code gates at stage 5. The Mokobara trace (C.3) shows the doctrine reaching the film; the structure works.
- One closed-beta company with an experienced marketing team. They will tell us where the creative ceiling is faster than any internal eval.
- Narrow, evidenced scope. "Not a universal creative agency."
- The customer must review and revise inside the product. The "specific repair" round on Mokobara (v1 → v2, one beat at a time, USD 2.6) is the model of what a revision should be.
- LLMs as components, founder not in the loop for ordinary jobs.

### Assumptions I challenge

1. **"The current runtime can execute the five-stage process."** It cannot, by design and by its own docstrings (`runtime/execute/bridge.py` L432: "live dispatch is not wired in this tranche … Plain statement, not a bug"; `runtime/spec/planner_seam.py`: "There is no live client here on purpose"). Running the Mokobara brief through it refuses at `spec` with `PLANNER_FIXTURE_MISSING`. The claim "Alpha-1 chain proven end-to-end" is true only for a recorded fixture, a synthetic PNG and a scripted detector.
2. **"Canon retrieval is deterministic and the model never decides what to read."** True for two packs. On the Mokobara job the trigger table selected all ten packs, injected two, and the producer session then read 22 raw claims from 13 sources by hand. The retrieval that produced accepted media is the pattern CANON-SHAPE-v1 §4 says was "designed out".
3. **"Successfully producing RentOK and Mokobara proves the classes."** It proves two *methods* once each. The RentOK method (code-rendered game film) depends on a 700–936-line renderer written for one side-scroller; it is not a product class. The Mokobara method (still → Veo i2v per beat, composed supers, music bed) is generalisable and is the film class P1 should ship. The static-image class — the only one the runtime targets — has **zero** accepted production cases (the still-generation step inside every job is proven; a delivered static ad is not).
4. **"P1 should support image and video jobs broadly."** Case 003 (Cumin, PR #103) is the counter-evidence: a spec video ad with voice-over, three versions all rejected at USD 5.09 — "the gates that existed passed; the defects were in what no gate covered (VO scheduling, subject obstruction, ad structure)". Every voiced film so far drew a "robotic" or "overlapping" complaint (001, 005, 003). P1 should exclude spoken voice.
5. **"Promoted gates mean the system now checks for those things."** PR #104's eight promoted gates have no caller outside their tests; case 002's five "promoted" items are workflow prose. Promotion so far means *exists with tests*, not *runs on jobs*.
6. **"The founder must state every spend cap in a terminal."** The rule is right; the mechanism is wrong for a product. In P1 the cap is stated by the customer's account admin in the product, within an account ceiling the founder sets once, and every paid call still reserves against it before sending. Same rule, different surface.
7. **"Compile the eight packs first" / "never compile them" (both positions exist).** Neither is right for P1. See C.

I did not adopt any scope or architecture proposed by ChatGPT; nothing below is derived from it.

---

## B. Evidence-backed readiness matrix

Legend: **OPERATIONAL** = runs on real jobs today; **PARTIAL** = code exists, does part of the job or runs only in dry mode/tests; **SPECIFIED** = contract or document only; **MISSING**.

| # | Component | Status | Evidence (OBSERVED) | Consequence for P1 |
|---|---|---|---|---|
| 1 | Brief contract (intake schema) | PARTIAL | `runtime/contracts/PRODUCTION-JOB-v1.yaml` (FROZEN); `runtime/intake/intake.py` 310 lines: schema, consent, kind ∈ profile. No revision/parent field, no brand kit, `ambiguity_markers` refused in `deliverable_request` (Mokobara `_provenance.schema_note`) | Additive v2 needed: revisions, brand kit, ambiguity markers. Small. |
| 2 | Intent understanding + question generation | MISSING (code) / OPERATIONAL (by hand) | No code derives mandatory items, decisions or questions from `brief.text`; `01-INTENT.md` on every job is Claude prose following `PRODUCTION-WORKFLOW.md` §5. No `QUESTION-TEMPLATE` file exists in the repo | Build as an LLM component with a fixed output schema; the five job records are the training/acceptance set. |
| 3 | Normalised Request | OPERATIONAL | `runtime/canon/normalize.py`; reproduces producer's NR on Mokobara | Reuse as is. |
| 4 | Canon pack lookup | PARTIAL | `runtime/canon/packs.py`: 10 triggers, 2 packs injectable, 8 return `missing_domain`; `canon_gap: True` on an ordinary Indian video ad | Blocker for the LLM component (it would see 2 packs). See C. |
| 5 | Canon raw-claim retrieval | SPECIFIED (unmerged code) | PR #84 CANON-015 `canon/retrieval/` (bundle, budgets, fixed question catalogue, BM25 within kind, accepted-only), 25 files, draft, PROPOSED, built on the 24-source corpus; not on main | Closest existing code to what Mokobara's producer did by hand; rebase + re-evaluate on LIVE37 rather than write new. |
| 6 | Creative board / copy deck generation | MISSING (code) / OPERATIONAL (by hand) | `runtime/spec/planner_seam.py` replays fixtures only; Mokobara `board.json` (feeling/framing/impact per beat) and `copy-deck.json` were written by Claude | LLM component with the Mokobara/V2 board schema as the output contract. |
| 7 | Prompt construction | OPERATIONAL (per job) | Mokobara `gen/prompts/*.txt`, RentOK `tools/prompts.py`; product description block verbatim in every prompt; guard word-list | Generalise into a deterministic builder from board + product dossier. |
| 8 | Route selection + price quotes | PARTIAL | `runtime/route/decision.py` 592 lines, `PriceBook.quote()`, taint register 61 cells; jobs called only `quote()` | Reuse; add a fixed P1 route table (nano-banana-2, veo-3.1-fast-i2v, lyria). |
| 9 | Live provider dispatch | MISSING (runtime) / OPERATIONAL (job tools) | `bridge.py` refuses live; `tools/dispatch.py` (253–407 lines) + `_common.py` (135, byte-identical Lane A ↔ V2) did every paid call; ledger reserve/settle, cap, guard, `provider_errors.classify` | Move the job tool into `runtime/execute/live.py` once; delete the copies. |
| 10 | Ledger, cap, attempt ids | OPERATIONAL with a known race | `next_attempt_id()` = line count of a file appended at settle → att-020 collision, 48–74 s window (`SYSTEM-DEFECTS.yaml` 007) | Store-backed reservation with a lock; the fix is one function. |
| 11 | Still generation with references, paint-out, contact sheet | OPERATIONAL (per job) | Mokobara `paintout.py`, `dispatch.py` ref2img; case 007 notes the ref route is `manual_only`/unregistered in the taint register | Generalise; register the IMG-REF cell from beta evidence. |
| 12 | Still → i2v clips, take selection, bounded re-takes | OPERATIONAL (per job, by hand) | Mokobara `RETAKES.md`, att-001…020b; take chosen by Claude against beat fields | Take selection becomes a checker-LLM call per clip; re-take budget in code. |
| 13 | Exact-text composition (Mechanism B) | OPERATIONAL | `runtime/compositor/gates.py` (bounds/contrast/fit/geometry/disjoint) called by Mokobara `render_text.py` at render time | Reuse directly. |
| 14 | Assembly (EDL, loudnorm, edit-list flags, end card) | OPERATIONAL (per job) | `assemble.py` 65–69 lines per job; flags carried V2 → Mokobara | Generalise: EDL from board + copy deck. |
| 15 | Deterministic QA | PARTIAL | `qa_checks.py` per job (102–224 lines); `runtime/loop/frame_hygiene.py`, `container.py`; PR #104 gates (hero_visible, framing_target, world_fills_frame, sprite_density, graphic_text_disjoint, vo_text_alignment, brand_colour) **have no caller outside tests** | Wire into one `det.py` the orchestrator always runs. |
| 16 | Canon gates (pre-dispatch / post-draw) | PARTIAL | `canon/gate/run_gate.py`, `runtime/loop/predispatch.py`, `postdraw.py`; not run on Mokobara (no gate output in `stages/evidence/`) | Wire into the loop. |
| 17 | Independent checker | OPERATIONAL (process) / MISSING (code) | "Checker: a fresh session that wrote none of the job" (`CHECK-STAGE-5.md`); nothing enforces independence; LJ items (identity continuity, gag readability, likeness, audio) by eye/ear | Isolated LLM call with DET outputs + contact sheets + beat fields; structured defect list; ideally a different model from the producer. |
| 18 | Human acceptance / release | PARTIAL | `runtime/loop/acceptance.py` states + `release()` by a named person; used only in dry runs; real verdicts live in `HUMAN-VERDICT-V1.md` | Reuse the state model behind a customer button. |
| 19 | Revision / targeted repair | OPERATIONAL (by hand) / PARTIAL (code) | Mokobara `06-REPAIR-ROUND-1.md` (per-beat repair, USD 2.6); `runtime/loop/repair.py` bounded by profile allowance | Customer comment → beat/asset → bounded repair plan; code. |
| 20 | Persistence / resume / lock / queue | MISSING | grep `runtime/` for lock/resume/queue/sqlite: none; state = files on a branch; runtime `--store` is a temp dir; CQ-001 drop recovered by a human re-briefing (not recorded) | Core P1 build. |
| 21 | Failure handling | PARTIAL | `provider_errors.classify` (retry flag only, re-send by hand); cap exhaustion = `sys.exit`; brief change = no path | Orchestrator semantics: counted retry, pause-on-cap, reopen-at-stage. |
| 22 | Customer surface (UI/API/auth/storage) | MISSING | No fastapi/flask/http.server in `runtime/`; three argparse CLIs; storage = git branches; ALPHA-1 "Does not exist: a customer-facing API" | Build small. Customer assets must leave git. |
| 23 | Deployment | MISSING | Everything runs on the founder's 8 GB Mac | One cloud VM (credits). |
| 24 | Production learning capture | OPERATIONAL (by hand) | 7 cases; `check_case.py` validates structure; nothing reads cases at job time; `templates.py` reads its own dry store only | Auto-generate the case skeleton from the store; promotion stays human. |
| 25 | Capability registry / routing authority | SPECIFIED | Every ROUTE-OBSERVATIONS row `routing_authority: none`; five accepted jobs moved the map by nothing, by design | Fine for P1 with a fixed route table; beta evidence feeds the register through the existing rule. |

---

## C. Canon readiness

### C.1 Exact state (OBSERVED)

| Pack | Compiled | Decisions/checks | Injected on Mokobara | Accepted claims reachable only by reading files |
|---|---|---|---|---|
| composition_and_attention | yes (`PACK-…-v0.yaml`, status PROPOSED) | 11 | yes | 69 of 356 in its domains are cited by the pack |
| product_appearance | yes (PROPOSED) | 10 | yes | 35 of 310 |
| camera_and_spatial_grammar | no | 0 | gap | 190 (6 sources) |
| colour_and_visual_register | no | 0 | gap | 328 (10) |
| commercial_communication | no | 0 | gap | 555 (15; 7 critical domains) |
| concept_and_distinctiveness | no | 0 | gap | 542 (17) |
| critique_and_effectiveness | no | 0 | gap | 987 (28) |
| editing_pacing_and_short_form | no | 0 | gap | 172 (5) |
| indian_indic_context | no | 0 | gap | 97 (5) |
| typography_and_copy | no | 0 | gap | 271 (7) |

- Trigger table (`canon/packs/pack-triggers-v0.yaml`, PROPOSED) fires all ten on a video ad with text, a product, market IN and advertising intent; the runtime injects two (5,298-token prefix, sha `4d7a5b27…`, identical to the producer's record) and records eight `missing_domain` gaps; the job continues. Audio → zero packs plus a gap notice. Animation/game → no pack, no domain.
- The compiled packs say PROPOSED in their headers; the runtime calls them `compiled_accepted` because the corpus digest matches (`runtime/canon/packs.py` L156–176). Two meanings of "accepted".
- C-10 (2026-09-14): "Do NOT compile the remaining eight packs unless a real runtime failure later demands one." No production job has run through the runtime, so that trigger has never been able to fire. The eight packs were read by hand instead.
- Question generation and answer sourcing: manual (Claude prose per the skill's blueprint table). Not implemented in code.

### C.2 Does the pipeline invoke Canon at the right decisions?

By hand, yes: NR → pack lookup (code) at stage 2/3; claims by id at board-writing time (Claude); compiled check ids applied as prose at stage 3 (`03-CREATIVE.md` A3); `canon/gate/run_gate.py` **not** run at stage 5 on Mokobara (UNKNOWN whether run unrecorded). In code, only the lookup and the gate library exist; nothing calls the gate in the production path.

### C.3 Retrieval-and-application trace — Mokobara (OBSERVED)

22 raw `sk_` ids from 13 sources were cited on the job; none is in a compiled pack; the prompts contain zero Canon ids (doctrine reaches the model as the producer's English). Twelve opened and traced from claim → board/copy-deck decision → prompt or code → frame in the accepted v2 file (sha `71850d1c…`):

| Claim (source) | Decision | Carrier | In the final | Class |
|---|---|---|---|---|
| sk_abcd_0007 (Google ABCD) "beginning in the middle of the action… close-up" | beat 1 opens on the tally-mark ECU | `b1-still.txt` | 0–1.5 s; then a hard cut the checker flagged | APPLIED (partial) |
| sk_ogx_0040 (Ogilvy) first frame as the gate | hundreds of marks in frame 1 | same prompt | same frame | APPLIED |
| sk_abcd_0010 / sk_ogx_0039 brand early, often, richly; name in first 10 s; end on the package | wordmark super 5.0–7.5 s; end card | `assemble.py` L42 reads `copy-deck.json` and composites the SVG **by code** | super at 5.5 s, end card 28.5 s, wordmark pixel-identical to the site SVG | APPLIED, code-carried |
| sk_ogl_c003_0014 product as hero | bag in every beat | verbatim bag block in every prompt | bag present 5.5/16.5/22.5/26 s | APPLIED |
| sk_whip_0058 "funny is an accent" | beat 4 played dry | `b4-clip-take2.txt` "completely deadpan… no movement" | register visible; gag half-delivered (D1 unrepaired) | APPLIED (register) |
| sk_whip_0031 exaggeration must rest on a truth | truth = 30 L capacity | copy deck `product_line` | end card | APPLIED |
| sk_gos_c003_0007 screen direction | left-to-right in beats 1 and 6 | `b6-clip-take2.txt` | not measured | PLAN ONLY |
| sk_alt_c003_0018 comedy is lit high | recorded deviation: stays low grey (survival story) | every prompt's light line | 4/5 cinematic look | APPLIED as deviation |
| sk_vig_c003_0013 identity is a system, keep the logo | wordmark is the site's SVG, not a string | `assemble.py` rasterises the SVG | pixel-identical | APPLIED |
| sk_abcd_0012 audio brand mention | deviation: no VO | — | absent | CITED-NOT-USED (honest) |
| sk_mla_0064 vs sk_ogx_0032 humour tension | arbitrated by the brief | — | — | CITED-NOT-USED |

9 applied-visible, 1 plan-only, 2 honestly not used. **The knowledge influences the output; the mechanism that delivered it was a model reading files.** For P1 that mechanism has to be code, logged, and repeatable.

### C.4 What happens when a domain is unavailable

Today: a `missing_domain` gap line and the job continues; the producer compensates by hand or does not. In P1 without a change: the LLM component receives two packs and no compensation. That is the material difference between the hand-run jobs and an automated P1, and it is why item C.5-1 is a blocker.

### C.5 Genuine P1 blockers (must be done before beta)

1. **Code-carried retrieval for the eight uncompiled packs.** Reuse PR #84's `canon/retrieval` (fixed question catalogue keyed to NR cues → BM25 within object kind → bounded, accepted-only bundle) rebased on LIVE37, wired as: compiled pack text where it exists, bounded raw bundle where it does not; every included id logged to the job record; every id the model cites parsed back into the record (the automatic version of `03-CREATIVE.md` A2). Deterministic given the NR, so CANON-SHAPE §4's principle holds. ~3 days.
2. **`ambiguity_markers` (and revision/brand-kit fields) in an additive PRODUCTION-JOB-v2** so the uncertainty rule can fire at intake. ~½ day.
3. **Wire the gates**: `canon/gate` pre-dispatch and post-draw + compositor gates + PR #104 gates into the orchestrator's check step. ~1 day.

### C.6 Non-blocking research gaps (do not put on the critical path)

- Compiling the eight packs. Recommendation: lift C-10 for **three named packs** that the P1 classes lean on and where the Mokobara trace showed application — `commercial_communication`, `editing_pacing_and_short_form`, `typography_and_copy` — as a parallel Canon-stream task, adopted only after a blind comparison on beta jobs (compiled pack vs raw bundle). Not before beta.
- Adopting the two compiled packs (one Controller line to close the PROPOSED/`compiled_accepted` split).
- Audio pack absence (P1 has no speech; music is a route choice, not doctrine).
- Animation/game domain (excluded from P1).
- The retired-vocabulary notice in the two compiled packs.

No new Canon ingestion is proposed. The 37 accepted sources are sufficient for the P1 classes.

---

## D. P1 product definition

### D.1 Supported media classes (evidence-bounded)

| Class | Method | Evidence | Boundaries |
|---|---|---|---|
| **P1-IMG — Static product/brand ad** (1:1, 4:5, 9:16, 16:9; 1–4 variants) | nano-banana-2 still from supplied product photos + logo; exact text composed by code (Mechanism B); brand colour check | Still step proven on every job; runtime's own class; **no accepted delivered case yet** — must pass validation (G) before beta | One product, supplied photos, ≤ 3 exact strings, no people |
| **P1-FILM — Short product story film** 15–30 s, 9:16 or 16:9 | 4–7 beats; still per beat (references) → Veo 3.1 Fast i2v; composed supers + end card; Lyria music bed; native ambient audio allowed; no speech | Mokobara 007 (accepted v2, USD 7.86, ~43 min to v1); V2 006 board fields; CQ-001 Treatment D | ≤ 7 beats, ≤ 30 s, one hero product, one human character at most (no identifiable real person), no dialogue/VO/lip-sync, no customer footage |

**Explicit exclusions (refused at intake, USD 0):** spoken voice-over or dialogue; lip-sync; talking heads (C-7); editing or extending customer-supplied footage; code-rendered animation/game styles (RentOK method); identifiable real people (consent path not built); more than one product per job; multi-language text variants (P2); anything requiring a named IP likeness (the prompt guard already blocks named-IP tokens; "in the mood of" is allowed).

### D.2 Customer journey

1. **Start a job.** Web form: idea or brief (free text), or upload an approved script/storyboard/deck (PDF/images); product photos (≥ 3), logo (SVG/PNG), brand palette + typeface (optional), references (optional, tagged "mood" or "must match"); deliverable (image / film), format, duration; exact text strings (optional); deadline; spend cap for this job (pre-filled from the account default; hard ceiling from the account).
2. **Understanding (autonomous, ≤ 2 min, USD 0).** The intent component lists what it understood, the mandatory items, and the decisions it will take by default. Supplied decisions (script beats, copy, references marked "must match") are locked. If ambiguity is high or an exclusion is detected, the job pauses **before any spend** with either up to five questions (each with a "decide for me" default) or a refusal with the reason and the nearest supported alternative.
3. **Creative plan (autonomous, USD ≤ 0.5).** The board (beats with feeling / framing / impact), copy deck, product likeness anchors, and a **cost quote** (from the PriceBook: stills × 0.067 + seconds × 0.10 + re-take allowance + 0.06 music). For films, the hero still of the riskiest beat is generated now (micro-qualification). Customer sees a plan card + that still: **Approve / Edit plan / Change still**. Accounts can set "auto-approve plans" to skip this gate.
4. **Production (autonomous).** Progress page: stages (Understanding → Plan → Stills → Motion → Checking → Ready), spend so far vs cap, ETA from the running average. No provider names, no Canon ids; the details exist on the operator view.
5. **Check (autonomous).** DET checks + independent checker run on every candidate. The preview page shows the film/image, a plain-English check report ("what we verified; what the reviewer flagged; what we could not judge by machine") and the provenance sheet.
6. **Review.** Accept / Request changes (per beat or per element, free text) / Reject. Requests map to a targeted repair (one beat, one element) within the remaining cap; up to two repair rounds per job by default. Accept = release (C-8: the customer releases).
7. **Delivery.** Download MP4/PNG (+ variants), provenance sheet (what was generated, what was composed, spend), and the job's brief and plan for their records.
8. **Failure handling, visible to the customer.** Unsupported → refused at step 2 with USD 0. Provider outage → "paused, retrying" with counted attempts; resumes automatically. Cap reached → "paused: needs more budget" with the exact amount; resumes on raise. Brief change → "reopen at Plan" (cost of already-produced assets is shown; assets that still fit are reused). Worker crash → resumes from the last persisted step; the customer sees nothing but a longer ETA.

### D.3 Decisions: customer vs autonomous

Customer decides: what the product is and the facts about it; exact copy (or approves generated copy); plan approval (unless auto-approve); accept/repair/reject; cap. Autonomous: beat structure, framing, camera, colour, music choice, routes, re-takes, text placement, assembly, check thresholds.

### D.4 Interfaces

- **Customer web app** (invite-only accounts for the beta company; magic-link sign-in; per-account isolation): job list, new job, questions, plan approval, progress, preview + report, feedback, delivery. Email notifications at each customer-facing step.
- **Operator view** (founder/Controller role, same app): everything the customer sees plus ledger, gate outputs, checker report, Canon trace, attempt log; an optional "hold before customer preview" toggle for the first beta jobs.
- **No public API in P1** (P2 candidate once the job contract has survived beta).

---

## E. Engineering plan

Conventions: reuse paths are on main or PR #104 unless stated; "job tools" = Mokobara/V2 `tools/`. Builders: Claude Code / Codex sessions, TDD, one builder per workstream, sequential on the Mac (8 GB) or in cloud sessions; the product itself runs on a cloud VM. Effort in builder-days (one agent, one focused session-day).

### W0 — Base (Controller, 1 day)
- **T0.1** Merge PR #104 then PR #103 (both add cases + gates; #103 touches `gates.py` and its test — expect a small conflict). Acceptance: `runtime/tests` green on main.
- **T0.2** Controller decisions in H recorded; C-10 amended for the three named packs (parallel, non-blocking).

### W1 — Job core: persistence + orchestration (critical path, 5 days)
- **T1.1 Job store.** SQLite (WAL) + per-job artifact directory + append-only `events.jsonl` (OUTCOME-EVENT-v1 shape). Tables: accounts, users, jobs, stages, attempts (ledger: reserve/settle), assets, decisions, verdicts. Reuse: AGENCY-JOB-v1 fields, `runtime/loop/acceptance.py` states, `runtime/loop/memory.py` event writer. New: `product/store.py`. Acceptance: round-trip a Mokobara-shaped job; every write is a transaction.
- **T1.2 State machine.** `intake → clarify → plan → qualify → produce_stills → produce_motion → compose → check → review → repair → deliver` (+ `paused_budget`, `paused_provider`, `refused`). Each step is an idempotent function keyed by (job, stage, attempt) reading inputs from the store and writing outputs atomically. Reuse: `runtime/alpha/run.py` stage sequencing pattern, `runtime/loop/repair.py` allowance. New: `product/orchestrator.py`. Acceptance: table-driven transition tests; illegal transitions refused.
- **T1.3 Worker + resume.** One process loop that claims the next runnable step with a store lock; on restart it re-reads the store and continues. Acceptance: `kill -9` mid-`produce_motion` in dry mode, restart, job reaches `check` with no duplicated attempt id and no duplicated reservation.
- **T1.4 Budget semantics.** Reserve-before-send against the store; atomic attempt ids under the lock (closes the att-020 race); cap reached → `paused_budget` (never `sys.exit`); provider `infrastructure_transient` → counted retry with backoff up to N, then `paused_provider`. Reuse: `runtime/execute/provider_errors.py`, the job tools' `reserve()/settle()` logic. Acceptance: injected 503 ×3 produces three ledger lines and one pause.

### W2 — Reasoning components (LLM as component; parallel with W1 after T1.1; 5 days)
- **T2.1 Intent + clarification.** Prompt from `PRODUCTION-WORKFLOW.md` §5 blueprint table + the shape of the five `01-INTENT.md` records; output schema: mandatory items with verification method, decisions with "cost if wrong", locked customer decisions, ≤ 5 questions with defaults, supported-class verdict with exclusion reasons, ambiguity score. Model: Claude via `ANTHROPIC_API_KEY` (present in `~/.mi-keys`). Acceptance: on the six frozen briefs (001, 003, 004, 006, 007 + one synthetic talking-head brief) → schema-valid; Mokobara reproduces ≥ 5 of its 7 mandatory items; the talking-head brief is refused; USD 0 provider spend.
- **T2.2 Board + copy deck.** Output contract = Mokobara `board.json` + V2 BOARD-v2 fields (feeling/framing/impact, renderer-free) + `copy-deck.json`; Canon prefix from W3; product dossier block. Acceptance: schema-valid on the same briefs; passes `canon/gate` pre-dispatch and the prompt guard; cited Canon ids parsed into the store.
- **T2.3 Deterministic prompt builder.** From board + dossier → per-beat still prompt and i2v prompt using the Mokobara/V2 prompt shapes (verbatim product block, light line, one dominant cue). Reuse: RentOK `tools/prompts.py` pattern. Acceptance: replaying the Mokobara board yields prompts that differ from the accepted ones only in whitespace/ordering (diff recorded).
- **T2.4 Checker component.** Isolated call (no producer context; different model where possible — Gemini via Vertex credits is the natural second opinion) given DET outputs, contact sheets at 2 fps, beat fields and the brief → structured defects (id, beat, severity, earliest stage, one repair each) in the `CHECK-STAGE-5.md` shape, plus per-clip take selection during production. Acceptance: on the Mokobara v1 frames, finds ≥ 4 of the 6 checker defects that the human checker found (D1, D5, oar continuity, tear, font, logo).

### W3 — Canon in code (parallel; 4 days)
- **T3.1 Raw-bundle retrieval.** Rebase PR #84 `canon/retrieval/` on main; re-index on LIVE37 (37 sources / 1,300 accepted objects); map pack → domains (`CANON-V1-LIVE37-COVERAGE.yaml`) → question catalogue → bounded bundle per uncompiled pack; token budget per pack and total; deterministic given NR. Acceptance: Mokobara NR → 10 non-empty packs; total prefix ≤ 25k tokens; sha-stable across runs; bundle ids logged.
- **T3.2 Citation logging.** Parse ids cited by T2.2 into the store; produce the trace table (C.3 shape) automatically. Acceptance: Mokobara replay yields a trace file.
- **T3.3 Gate wiring.** `canon/gate` pre-dispatch + post-draw, `runtime/compositor/gates.py` (all, including PR #104's eight), `frame_hygiene`, `container.assess_edit_lists` into `product/det.py`, always run in `check`. Acceptance: Mokobara v2 file → same DET results as `qa_checks.py` recorded; the eight gates now have a caller.
- **T3.4 PRODUCTION-JOB-v2 (additive).** `ambiguity_markers`, `revision_of`, `brand_kit{palette, typeface, tone}`, `supplied_creative{script, storyboard, locked: bool}`. Acceptance: v1 briefs still validate.

### W4 — Production execution (after T1.4; 6 days)
- **T4.1 `runtime/execute/live.py`.** Promote `tools/dispatch.py` + `_common.py` once: stdlib transport, key-by-name, scrub, bounded poll, PriceBook quote, guard, routes nano-banana-2 (t2i + ref), veo-3.1-fast i2v, lyria; ledger via T1.4. Delete nothing on job branches (archival). Acceptance: dry replay of the Mokobara attempt bodies is byte-identical; live micro-test deferred to validation (needs a stated cap).
- **T4.2 Stills pipeline.** References + paint-out (`paintout.py`) + contact sheet + likeness verdict from T2.4; micro-qualification of the riskiest beat first (from CQ-001/Mokobara practice). Acceptance: dry run produces the plan card assets.
- **T4.3 Motion pipeline.** Per-beat i2v with take selection by T2.4 against feeling/framing/impact; re-take allowance from the profile (from `RETAKES.md` discipline). Acceptance: dry run schedules ≤ N attempts per beat and respects the cap.
- **T4.4 Compose + assemble.** Generalise `render_text.py` (LayoutRefused on gate failure) and `assemble.py` (EDL from board; supers from copy deck; loudnorm two-pass; `-use_editlist 0 +faststart`; end card). Static class: compositor over the still. Acceptance: Mokobara clips + copy deck → file with identical DET profile to v2.
- **T4.5 DET → check → review.** Orchestrator runs `det.py`, then T2.4, writes the plain-English report, moves to `review`. Repair: customer comment → (beat, element) → bounded repair plan → back to the right stage. Acceptance: a "beat 4 arms deeper" comment on the Mokobara replay re-plans only beat 4.

### W5 — Customer surface + deployment (parallel with W4; 5 days)
- **T5.1 Web app.** FastAPI + server-rendered pages (Jinja/HTMX; no SPA): job list, new job (uploads), questions, plan card, progress, preview + report, feedback, delivery; operator view. Auth: invite-only magic link; account-scoped queries everywhere. Acceptance: a second account cannot read the first account's job by URL.
- **T5.2 Storage + secrets.** Assets and outputs under `/data/<account>/<job>/` on the VM with nightly GCS backup; secrets from an env file on the VM; **no customer asset committed to git**. Acceptance: backup restore drill.
- **T5.3 Deployment.** One GCE VM (e2-standard-2, 8 GB; credits), ffmpeg + rsvg, systemd for web + worker, HTTPS. Acceptance: fresh-VM install script runs the dry end-to-end.
- **T5.4 Notifications.** Email on question / plan / preview / delivery / pause.

### W6 — Learning loop (2 days, after W1)
- **T6.1 Case auto-capture.** From the store, generate the case skeleton (EVIDENCE-MAP, TIME-AND-COST with mechanical clocks, HUMAN-VERDICTS verbatim, REVISION-TRACE, ROUTE-OBSERVATIONS with `routing_authority: none`) → `production-learning/cases/`; `check_case.py` must pass. Promotion stays with `/media-agency-sync` and the Controller — nothing auto-promotes.
- **T6.2 Beta comparison fields.** Optional per job: "how would you have made this; time; cost" captured at delivery.

### W7 — Validation (after W4 + W5; 5 days; needs a stated validation cap)
- **T7.1** Dry end-to-end on the six frozen briefs, USD 0.
- **T7.2** Live shakedown by the founder acting as a customer through the UI: 2 × P1-IMG, 2 × P1-FILM (one from a one-line idea, one from a supplied storyboard). Proposed cap USD 40 total provider spend + LLM tokens (H-5).
- **T7.3** Chaos: worker kill mid-motion; injected 503; cap exhaustion and raise; brief change at plan; unsupported request.
- **T7.4** Beta gate (G).

---

## F. Timeline and critical path

| Week | Engineering | Integration | Validation |
|---|---|---|---|
| 1 | W0; W1 (T1.1–T1.4); W3 (T3.1, T3.4) start; T4.1 in dry | — | unit tests |
| 2 | W2 (T2.1–T2.4); W3 finish; W4 (T4.2–T4.4) | first dry end-to-end on a frozen brief | T7.1 |
| 3 | W5; T4.5; W6 | live shakedown job #1 (static) through the UI | T7.2 start |
| 4 | fixes | shakedown films; chaos | T7.2, T7.3 |
| 5 (buffer) | — | beta onboarding | T7.4 gate |

**Totals:** engineering ≈ 24 builder-days (≈ 3 weeks with two builders in parallel, one on W1/W4, one on W2/W3/W5); integration ≈ 5 days; validation ≈ 5 days. **Shortest credible route: 4 weeks to the gate run, 5 with buffer.**

**Critical path:** T1.1 store → T1.2/T1.3 orchestrator → T1.4 budget → T4.1 live dispatch → T4.3/T4.4 motion + assemble → T4.5 check/review → T5.1 UI → T7.2 shakedown → G. W2 and W3 are off the critical path until T4.5 needs them (end of week 2).

**What could delay beta:**
1. Creative quality of P1-FILM on the beta customer's product (identity drift across i2v clips, gag/beat readability) needing more re-take rounds than the allowance — a creative limit, not a code one; mitigated by micro-qualification and plan approval.
2. The checker component judging worse than a fresh Claude session (T2.4 acceptance may need model/prompt iteration).
3. Vertex/Gemini quota or credit exhaustion mid-validation (credits are the only funding; check balances before week 3).
4. Canon bundle size vs cache/latency (T3.1 budget tuning).
5. Hosting and account decisions not made by the end of week 1 (H-3, H-4).
6. PR #103/#104 merge conflicts in `gates.py`.
7. Founder availability for the shakedown verdicts (TTAO on Mokobara was 10 h 23 m, of which ~9 h was waiting for the verdict).

---

## G. Beta-release gate

Run on the deployed VM by a person who is not the founder, using a customer account, with the founder's operator log open. Pass = all of the following in one continuous run, with no terminal command by the founder:

1. **Submit.** A P1-FILM brief (one-line idea + 3 product photos + SVG logo + palette) and a P1-IMG brief (supplied storyboard + exact copy) with per-job caps stated in the product.
2. **Clarify.** The film job pauses with ≤ 5 questions before any spend; the answers change at least one board decision (verified in the store).
3. **Plan.** Plan card + quote + hero still delivered ≤ 15 min after answers, spend ≤ USD 0.5; customer edits one beat's copy; the change is locked and appears in the final.
4. **Produce.** Film ≤ 30 s delivered to preview with DET report and checker report; provider spend within cap; every attempt has a ledger line with reserve before settle; zero unclassified provider errors.
5. **Independent verification.** The checker report was produced by a call with no producer context (verified by the store's call log) and lists ≥ 1 defect with an earliest stage.
6. **Revise.** Customer requests one specific change on one beat; only that beat is re-produced (attempt log shows no other beat re-dispatched); v2 delivered within the remaining cap.
7. **Accept and deliver.** Customer accepts; download works; provenance sheet lists every generated and composed element and the total spend; the ledger reconciles to the provider consoles within USD 0.10.
8. **Persistence.** During step 4 the worker is killed once by the tester; on restart the job continues with no duplicate attempt id and no duplicate reservation.
9. **Provider failure.** One injected 503 during step 4 appears as a counted attempt and the job continues without human action.
10. **Budget.** A third job with a deliberately low cap pauses at `paused_budget` with the exact shortfall; raising the cap in the product resumes it.
11. **Unsupported.** A talking-head brief is refused at intake with the reason and USD 0 spend.
12. **Isolation.** A second account cannot open the first account's job.
13. **Learning.** The case skeleton for each job is generated and passes `check_case.py`; nothing was auto-promoted.
14. **Quality bar.** Both P1 classes have ≥ 2 accepted shakedown outcomes (T7.2) from a non-author reviewer before this gate, and the P1-IMG class has its first accepted delivered case.

---

## H. Decisions required from the founder

| # | Decision | My recommendation | Alternative | Why it matters |
|---|---|---|---|---|
| H-1 | P1 scope | **Two classes: P1-IMG static ad + P1-FILM 15–30 s still→i2v story film, no speech** | Film only (drops the class with zero cases but loses the cheapest, highest-volume deliverable); or add voice-over (cases 001/003/005 say no) | Sets the beta customer's expectations and the validation budget |
| H-2 | Canon mechanism | **Raw-bundle retrieval (reuse PR #84) for the eight packs now; lift C-10 for three named packs in parallel, adopted only after a blind comparison on beta jobs** | Compile before beta (+2–3 weeks, no evidence it beats bundles); or ship with two packs (repeats the escalation failure) | Determines whether the automated producer sees the knowledge the hand-run producer used |
| H-3 | Where P1 runs | **One GCE VM on Vertex credits, SQLite + disk + GCS backup** | Cloud Run + Cloud SQL (more moving parts, no benefit for one customer); the Mac (no — 8 GB, not customer-facing) | Deployment is on the critical path from week 3 |
| H-4 | Reasoning models and their budget | **Claude API (key present) for intent/board; Gemini on Vertex credits for the checker (independence + credits)**; expect USD 1–5 of tokens per job, measured in T7.2 | Claude for both (less independence); Gemini for both (unmeasured board quality) | First paid LLM-as-component spend; needs a stated monthly ceiling |
| H-5 | Validation spend | **Authorise a USD 40 provider cap for T7.2 + the LLM token ceiling at week 2** (not now) | Lower cap → fewer shakedown jobs → weaker gate | Nothing paid happens until this is stated in-session and recorded |
| H-6 | Human gates in beta | **Customer plan approval on; operator "hold before preview" on for the first 10 jobs, then off**; release = customer accept (C-8) | Fully autonomous from job 1 (higher risk of a poor first impression) | Founder time per job drops from operating to one review click |
| H-7 | Merge order | **#104 then #103, this week** | Leave unmerged (P1 branches then stack on an unmerged base) | P1 code depends on #104's gates |
| H-8 | Beta data terms | **Customer assets and outputs stay on the VM (never in git); case records use the opaque `customer_ref`; the customer agrees their briefs/verdicts feed production learning** | Case records without customer material (weaker learning) | Must be in the beta agreement before job 1 |

Everything else in E is an implementation decision I will take, and record, without returning it to you.

---

### Appendix — what would surprise you (condensed from the investigation)

1. "Canon retrieval is deterministic" holds for 2 packs; real jobs retrieved by Claude reading YAML.
2. The 2-of-10 state is a ruling (C-10) whose release condition can never fire while jobs bypass the runtime.
3. The trigger table fires all ten packs on an ordinary Indian video ad and delivers two; `canon_gap: True` is the normal state.
4. Compiled packs are PROPOSED in their headers and `compiled_accepted` in the runtime.
5. "Alpha-1 proven end-to-end" = recorded fixture + synthetic PNG + scripted detector; no reasoning-model call exists in the runtime; a new brief refuses at `spec`.
6. Every accepted deliverable came from per-job `tools/` copied branch to branch; the ledger/cap/id/guard code exists in ≥ 3 copies with a known race.
7. The only class the runtime is built for has zero accepted production cases.
8. "Independent checker" = a second Claude session by process rule; identity, gag, likeness and audio are judged by eye/ear.
9. PR #104's eight promoted gates have no caller; case 002's five promotions are workflow prose.
10. Production learning is write-only at job time.
11. No persistence, resume, lock or queue; a dropped session is recovered by a human; the CQ-001 drop is not recorded anywhere.
12. Cap exhaustion is `sys.exit`; retry is a person re-running a command.
13. A brief change mid-job has no path.
14. `ambiguity_markers` cannot be carried in the frozen contract, so the uncertainty rule was inert on Mokobara.
15. The taint register is descriptive; Mokobara's core still route (with reference photos) is a `manual_only`/unregistered use.
16. CpAO is provider spend only (no LLM tokens, no human time); Mokobara's 10 h 23 m TTAO is mostly waiting for the verdict.
17. Case 003 exists — on unmerged PR #103 — and is the strongest negative evidence: a voiced spec ad, three versions rejected at USD 5.09, defects in what no gate covered.
18. A bounded, accepted-only Canon retrieval implementation already exists (PR #84, 31 Aug, draft) and was never adopted; it is the nearest thing to what P1 needs.
