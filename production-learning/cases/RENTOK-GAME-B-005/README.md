# RENTOK-GAME-B-005 — production-learning case

**What it is.** Lane B of the two-lane live experiment of 20–21 Sep 2026 (sister case: `RENTOK-GAME-A-004`). Same frozen
customer brief — a 30-second vertical "Mario-style" film for RentOK — but this lane also received a ChatGPT-written creative
direction to verify and refine. It produced a code-rendered pixel-art side-scroller from seven textless AI stills, a Lyria
bed and a three-line generated arcade announcer, and was presented blind as **Video X**. The customer's one sentence covered
both films: "both accepted. vidoe one has robotic voice over althouh. video 2 is better" — this film **accepted**, with the
voice noted as robotic, and not preferred.

**Two conclusions, kept apart.**
Final quality: **SUCCESS with one customer-noted defect** (the announcer).
Pipeline efficiency: **MET_BASELINE** — 1 h 53 m 07 s to the customer's accept; USD 0.587 of a USD 10 cap across 25 paid
calls (3 failed, all counted), 0 paid repairs; one review cycle. Case 001 for comparison: 7 h 54 m, USD 15.39, five cycles —
a different production class, read side by side.
Process conformance: **CONFORMANT with two recorded gaps** — the pre-dispatch prompt gate was not run (the no-lettering
clause was honoured by construction, and the stills were clean), and no human heard the voice audition before the voice was
frozen.

**The core findings.**
1. The one defect that reached the customer was the one thing no human had checked: the voice was cast by transcript and
   duration because neither the producer nor the checker session can listen. Sarvam bulbul:v3 had already been heard as
   robotic once (case 001); it was chosen here because it was the only candidate to finish all three lines after ElevenLabs
   hit an invisible per-key quota and Gemini TTS refused one line. `VOICE_CAST_BY_A_HUMAN_EAR` is the candidate.
2. Sixteen defects were closed at USD 0 before presentation: the runtime gates caught the layout collisions on the first
   render; the independent checker caught a graphic riding over the name tag, a voice line 1.2 s ahead of its own words, a
   sprite cell missing an identifier, and an empty lower third from a 16:9 plate in a 9:16 frame. Three of those had no
   deterministic check anywhere and now do (below). A fourth — the dispatcher reserving before it validated its input —
   turned out to have a twin in the runtime bridge, now fixed with a test.
3. Both lanes converged on the same production method without seeing each other; the direction under test neither helped
   nor hurt the structure on this one job (Controller comparison, INFERRED). n = 1 customer, 1 brief: no general winner.

| File | Answers |
|---|---|
| `OUTCOME.yaml` | accepted, version 1 of 1, final asset by sha256 at `d0a0583`, spend from the checker-reconciled ledger, what this is not evidence for |
| `HUMAN-VERDICTS.yaml` | the customer's sentence, chat-only; HD-01 the voice, with why no ear heard it earlier |
| `REVISION-TRACE.yaml` | one presented version; R1–R5, T1, D-1..D-9, N-1 with root-cause classes; the mechanical clock; the three failed attempts kept apart |
| `TIME-AND-COST.yaml` | `date -u` anchors, TTAO 1:53:07, CpAO 0.58675 with missing components, cost by route (the USD 0.058 over lane A is the voice audition and QA transcripts) |
| `SYSTEM-DEFECTS.yaml` | 16 pipeline defects, 1 model failure at a gate (D-4), 1 at the customer (HD-01), 2 provider transients, the roster pool-label discrepancy (PD-02, verified) |
| `ROUTE-OBSERVATIONS.yaml` | nine directional rows incl. the customer's ear on bulbul:v3 (n = 1), the ElevenLabs per-key quota, the Gemini TTS refusal |
| `PROMOTION-QUEUE.yaml` | promoted: GRAPHIC_TEXT_DISJOINT, VO_TEXT_ALIGNMENT, VALIDATE_BEFORE_RESERVE · nine candidates · two Canon-gap candidates · two proposals for a Controller decision · not promoted |
| `ACCEPTED-TEMPLATE.yaml` | the same `code_rendered_side_scroller_with_ai_sprites` template as case 004 with this lane's beat times; n = 2 jobs, one customer, one brief |
| `EVIDENCE-MAP.md` | every claim → path @ `d0a0583` + sha256; experiment branch cited separately; the roster/routing-map labels verified in this checkout |

## Engineering promoted from this case (class 1, on the sync branch, each with a regression test)

| Defect | What a deterministic check would have caught | Where it now lives |
|---|---|---|
| D-1, D-9 phone / beam over the name tag | a critical graphic and a text box may not overlap | `runtime/compositor/gates.py` `check_graphic_text_disjoint` (shared with case 004 D-2) |
| D-3 "RentOk mode: on" spoken 1.2 s before the words | a paired voice line may not start before its string's first on-screen time | `runtime/compositor/gates.py` `check_vo_text_alignment` |
| T1 / att-016 reserved before the input was checked | a harness-refused attempt reserves neither ceiling nor pool | `runtime/execute/bridge.py` `_attempt`; the committed dry battery B05 re-recorded (reserved 2.16 → 0.96 USD, two Veo-aspect-refused fallbacks) |

Tests: `runtime/tests/test_j_rentok_game_004_005.py`.

## Proposals that need a Controller decision (written here, not applied)

- **Roster pool labels.** `ROSTER-REFRESH-2026-09.yaml` says `billing_pool: cash` for `sarvam-bulbul-v3` and `elevenlabs-v3`;
  the routing map says `sarvam_credits` / `elevenlabs_credits`; the Controller ruled on 20 Sep that they are credits pools.
  Reconcile under the roster's refresh process. Verified in this checkout; not edited here.
- **Gemini TTS** ran under a job-local pin with no Registry cell; directional evidence only (2/3 + one refusal).
- **Canon gap**: no accepted Canon on game/arcade readability, pixel art or chiptune (both lanes; no failure followed);
  and a checker step to verify a declared gap against the accepted-claim index (this lane declared audio/colour gaps that
  existed).

## Experiment context

Contract, spend authorisation (USD 10 per lane, credits only, pool attested), sealed blind packet, verbatim verdicts and
the Controller's comparison: `work/experiment-rentok-two-lane-2026-09-20 @ 594e7c9`, `experiments/RENTOK-TWO-LANE-2026-09-20/`.
The ChatGPT direction is `input/02-CHATGPT-DIRECTION-LANE-B-ONLY.md` on this job's branch; the lane logged ten material
changes from it with reasons. Blindness limitation recorded before presentation (contract §8).

## What this case is not evidence for

Capability Registry, Alpha-1, Canon effectiveness, Stage A/B/C, any routing rule, that bulbul:v3 is unusable (one ear,
three short lines, film accepted), that the ChatGPT direction helped or hurt, or CpAO completeness.

**Validate.** `JOB_COMMIT=$(git rev-parse origin/work/agency-job-rentok-game-lane-b-001); python3
production-learning/tools/check_case.py --case production-learning/cases/RENTOK-GAME-B-005 --source-ref "$JOB_COMMIT"
--source-dir agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-B-001` — PASS with the accepted film byte-verified.
