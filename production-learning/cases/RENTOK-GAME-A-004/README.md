# RENTOK-GAME-A-004 — production-learning case

**What it is.** Lane A of a two-lane live experiment on 20–21 Sep 2026: the same frozen customer brief (a 30-second
vertical "Mario-style" game film for RentOK, a PG-management app) was produced twice in isolation, and the customer
judged both films blind. Lane A worked from the brief alone; lane B (case `RENTOK-GAME-B-005`) also received a
ChatGPT-written creative direction. This film — a code-rendered pixel-art side-scroller with seven textless AI stills, a
Lyria chiptune bed and no voice — was presented as **Video Y** and **accepted and preferred**: "both accepted. vidoe one has
robotic voice over althouh. video 2 is better".

**Two conclusions, kept apart.**
Final quality: **SUCCESS** — accepted on first presentation, no customer-flagged defect.
Pipeline efficiency: **MET_BASELINE** — 1 h 54 m 18 s from job start to the customer's accept (case 001: 7 h 54 m);
USD 0.529 of a USD 10 cap, 8 paid calls, 0 failed, 0 paid repairs (case 001: USD 15.39); one review cycle (case 001: five).
Process conformance: **CONFORMANT** — five stages, a non-author checker at gates 1–4 and stage 5, frozen plan before
spend, written cap, USD-0 animatic first. These numbers describe what a code-rendered class costs; they do not show that
the pipeline improved on case 001's class.

**The core finding.** Zero media-model failures reached a gate. Every one of the 18 defects closed before presentation was
in the code around the models — layout collisions (caught by the runtime gates on the animatic at USD 0), a container that
carried edit lists the lane's own spec forbade, the customer's flag hidden behind text, board-fidelity drift, and a repair
that regressed the end card to black while its statement said "#0239FF". The independent checker found eleven of them,
including the regression. **Quality was won in the checker → repair loop, and the repairs were free because the film was
code.** Three of those misses had no deterministic check anywhere and now do (below).

| File | Answers |
|---|---|
| `OUTCOME.yaml` | accepted, version 1 of 1, final asset by sha256 at the immutable commit `7dab37a`, spend from the ledger, what this is not evidence for |
| `HUMAN-VERDICTS.yaml` | the customer's one sentence, chat-only, with the Controller's reading of "video 2" labelled INFERRED; the blindness limitation |
| `REVISION-TRACE.yaml` | one presented version; the 18 defects (R1–R5, D-1..D-11) with root-cause classes; USD 0 repairs; the mechanical clock |
| `TIME-AND-COST.yaml` | `date -u` anchors, TTAO 1:54:18 with its one chat-anchored end, CpAO 0.529 with missing components, generation wait ≈ 1.5 % of the time |
| `SYSTEM-DEFECTS.yaml` | 18 pipeline defects, 0 model failures; three promoted to code; cross-references to the same defects in case 005 |
| `ROUTE-OBSERVATIONS.yaml` | six directional rows, exact n, `routing_authority: none` |
| `PROMOTION-QUEUE.yaml` | promoted: CONTAINER_EDIT_LIST_CHECK, GRAPHIC_TEXT_DISJOINT, BRAND_COLOUR_ON_RENDERED_FRAME · nine candidates · two Canon-gap candidates (report only) · not promoted |
| `ACCEPTED-TEMPLATE.yaml` | `code_rendered_side_scroller_with_ai_sprites` — both lanes converged on it independently; n = 2 jobs, one customer, one brief; `evidence_scope: this_accepted_template` |
| `EVIDENCE-MAP.md` | every claim → path @ `7dab37a` + sha256; the experiment branch cited separately; what is not on disk |

## Engineering promoted from this case (class 1, on the sync branch, each with a regression test)

| Defect | What a deterministic check would have caught | Where it now lives |
|---|---|---|
| D-1 two `elst` atoms | walk the MP4 box tree and refuse any edit list when the spec says none | `runtime/loop/container.py` `assess_edit_lists` |
| D-2 flag hidden behind the checklist | a critical graphic and a text box may not overlap (the text-only disjoint gate cannot see it) | `runtime/compositor/gates.py` `check_graphic_text_disjoint` |
| D-11 black end card recorded as "#0239FF" | measure the rendered, encoded pixels against the declared brand hex; no samples is a refusal | `runtime/compositor/gates.py` `check_brand_colour` |

Tests: `runtime/tests/test_j_rentok_game_004_005.py` (values are the checker's measurements).

## Experiment context

Contract, spend authorisation (USD 10 per lane, credits only, pool attested by the human), sealed blind packet, verbatim
verdict record and the Controller's comparison are on `work/experiment-rentok-two-lane-2026-09-20 @ 594e7c9` under
`experiments/RENTOK-TWO-LANE-2026-09-20/`. Both lanes chose the same production method without seeing each other; the
Controller's reading (INFERRED there) is that the convergence came from the shared evidence base, not from either creative
input, and that the customer's preference tracked one execution choice (the other lane's voice), not the direction. The
blind judgment had a recorded limitation: the human had seen per-lane progress facts in chat (contract §8).

## What this case is not evidence for

Capability Registry, Alpha-1, Canon effectiveness, Stage A/B/C, any routing rule (n ≤ 7 per route, one job), a general
preference for voiceless films, or CpAO completeness (Google credits unreconciled; session tokens and human time unpriced).
n = 1 customer, 1 brief: no general winner between the two lanes is established.

**Validate.** `JOB_COMMIT=$(git rev-parse origin/work/agency-job-rentok-game-lane-a-001); python3
production-learning/tools/check_case.py --case production-learning/cases/RENTOK-GAME-A-004 --source-ref "$JOB_COMMIT"
--source-dir agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-A-001` — PASS with the accepted film byte-verified.
