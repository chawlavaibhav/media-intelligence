# RENTOK-GAME-V2-006 — the RentOK game film, re-made "the video 4 way" (accepted, 21 Sep 2026)

**What this is.** The third accepted film on the RentOK brief. After the two-lane experiment (cases 004/005) the customer
ran a creative-quality experiment on one 6.8-s beat (CQ-001) and ranked four treatments blind: a video-model clip first,
then **Treatment C** — the same code renderer with per-beat *direction* (a feeling, a framing target and named impact
primitives for every beat) and one new expression sheet — then the prompt-only rewrite, then the accepted Lane A beat last.
He then asked for the full 30 s "the video 4 way" (= Treatment C). This job did that: Lane A's skeleton, copy and timings
kept byte-for-byte; a new board (BOARD-v2) with `feeling / framing / impact` on all fifteen beats; a renderer that executes
those fields; **one** paid draw (an 8-pose sheet, USD 0.067); everything else reused from Lane A and Treatment C under
verified provenance. Presented once. **ACCEPT: "its already good"** — and, on the offer of a free repair round for the
independent checker's findings, **"not required"**.

**The two numbers, side by side, never blended** (TIME-AND-COST.yaml):
- **0:51:13** from job start to a deliverable that passed every deterministic check (the pipeline's clock);
  **5:09:28** from job start to the customer's ACCEPT (the outcome's clock; the 4 h 01 m between is the customer's reply time).
- **CpAO USD 0.067** for this job (one call, none failed). On a separate line: **USD 0.663** for every drawing that appears in
  the film across three ledgers (Lane A 0.529 + Treatment C 0.067 + this 0.067) — the packet's "USD 0.66".
- Baseline case 001: 7 h 54 m / USD 15.39 / 5 cycles. Lane A (the film this supersedes): 1:54:18 / USD 0.529 / 1 cycle.

**What the evidence shows.** (1) The gates promoted from cases 004/005 and the job's two new gates found seven defects at
USD 0 before spend or before presentation — the paid call was the only paid call. (2) What reached the independent checker
was what no gate covered: the flag rising *through* the cheering owner (26 frames), the phone over his face at the wind-up
(6 frames), the dazed pose off the left edge, and a grain change at every swap between the old run poses and the new sheets
(the sheets stand at 61 % of the base sheet's pixel height — the producer had the number and read it as invisible at phone
size; the checker found it visible). Those are now runtime gates with tests. (3) The customer accepted the file **with** the
checker's ten recorded defects on it, by choice. The case records them as unrepaired; it does not pretend the file is clean.

**What the evidence does not show.** That the `feeling / framing / impact` schema improves films in general: one customer,
one brief; Lane A was accepted without it. The evidence that isolates the schema is CQ-001's blind rank on one beat
(C above B and A), not this acceptance. Promotion condition: one more accepted job on a different brief.

## Files

| File | What it holds |
|---|---|
| `OUTCOME.yaml` | accepted; final asset `0e76b7b1…` @ `b06deaf`; why the job exists; two conclusions; template `reusable_candidate` |
| `HUMAN-VERDICTS.yaml` | the three chat messages verbatim; the declined repair round; what the words do not say |
| `REVISION-TRACE.yaml` | one version: five animatic defects + two final-v1 defects closed at USD 0; ten checker defects unrepaired |
| `TIME-AND-COST.yaml` | both clocks with sources; CpAO 0.067; the USD 0.663 line kept separate; counts |
| `SYSTEM-DEFECTS.yaml` | every defect classed; four promoted as code (N1/N2, A-4/R-1/N4, LJ-15, N5); the packet's "six" vs the checker's ten |
| `ROUTE-OBSERVATIONS.yaml` | nano-banana-2 8-pose sheet 1/1 with one pose miss; latency; AAC + limiter; renderer limits — `routing_authority: none` |
| `PROMOTION-QUEUE.yaml` | the five classes: 4 promoted, 12 candidates (board schema, animatic-before-spend n = 4, primitives, declined-repair rule…), 4 directional, 1 Canon gap, 6 job-specific |
| `ACCEPTED-TEMPLATE.yaml` | Lane A's skeleton + the direction layer, per-beat feelings verbatim from the board, per-pose framing targets; `evidence_scope: this_accepted_template` |
| `EVIDENCE-MAP.md` | 55 hashed rows @ `b06deaf`; what is chat-only |

## Engineering changes on this branch (class 1)

`runtime/compositor/gates.py`: `check_hero_visible` (a declared hero region may not be covered by a graphic drawn in front of
it — N1, N2), `check_framing_target` (read at one named focus frame; missing frame refuses; per-pose target; hero inside the
canvas — A-4, R-1, N4), `check_world_fills_frame` (every camera scale ≥ 1.0; none logged refuses — LJ-15),
`check_sprite_density` (one character's sheets within a stated standing-height ratio — N5). Tests:
`runtime/tests/test_k_rentok_game_v2_006.py` (17 tests, every number from the job's layout log and cut-out records).

## Validation

```
python3 production-learning/tools/check_case.py --case production-learning/cases/RENTOK-GAME-V2-006 \
  --source-ref b06deaf7907de9c64d574a5f042a014c2e519ce6 --source-dir agency/jobs/AGY-2026-09-21-RENTOK-GAME-V2-001
```
The job branch `work/agency-job-rentok-game-v2-001` was local-only at sync time; the commit must be present for the
validator to byte-verify the accepted film.
