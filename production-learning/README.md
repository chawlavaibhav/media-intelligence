# production-learning/

Durable product learning from **real productions** — accepted or rejected commercial work executed for a
purpose outside the Lab. It is neither `eval/` (Capability Lab evidence: sealed, Registry-feeding) nor
`runtime/store/outcomes/` (OUTCOME-EVENT-v1 events written by the runtime loop for the narrow Alpha chain).
A case here never creates a Registry row, never edits Canon, and never claims routing authority; it records
what happened, what the human judged, what the system got wrong, and what is promoted as a deterministic
engineering requirement versus kept as a candidate or directional observation.

```
production-learning/
  README.md
  cases/<CASE-ID>/            one directory per production (schema PRODUCTION-LEARNING-CASE-v0, see check_case.py)
  tools/check_case.py         validator: structure and honesty of ANY case (accepted | rejected | abandoned; template optional;
                              evidence at --source-ref/--source-dir; --pilot-ref/--pilot-dir kept as aliases; an accepted asset is
                              byte-verified against its sha256; a supplied ref that cannot be inspected FAILS) — never a job's outcome
  tools/reconcile_pilot_ledgers.py   append-only JSONL ledger totals per lineage
```

Cases: `UPWORK-INTRO-001` (14 Sep 2026, accepted V4.1 — the baseline for TTAO and full CpAO); `UPWORK-PORTFOLIO-002` (15 Sep 2026, commercial portfolio batch — 9 tiles accepted, 1 skipped after 2 rejected attempts; process non-conformant; complex-production-event trigger MET; evidence on `work/upwork-portfolio-samples-2026-09-15` @ `b4b77fa`).
`RENTOK-GAME-A-004` (20–21 Sep 2026, RentOK game film, lane A autonomous — accepted blind and preferred; TTAO 1:54:18, CpAO USD 0.529, 8 paid calls, 0 model failures at a gate; promoted the MP4 edit-list box walk, graphic↔text disjointness and the brand-colour-on-rendered-frame gate; evidence `work/agency-job-rentok-game-lane-a-001` @ `7dab37a`); `RENTOK-GAME-B-005` (same brief, lane B ChatGPT-directed — accepted blind with the generated announcer noted as robotic; TTAO 1:53:07, CpAO USD 0.58675, 25 paid calls, 3 failed and counted; promoted VO-vs-on-screen-words alignment and validate-before-reserve in the execution bridge; evidence `work/agency-job-rentok-game-lane-b-001` @ `d0a0583`). Both lanes converged on the `code_rendered_side_scroller_with_ai_sprites` template (n = 2 jobs, one customer, one brief); experiment context on `work/experiment-rentok-two-lane-2026-09-20` @ `594e7c9`.
`RENTOK-GAME-V2-006` (21 Sep 2026, the same brief re-made "the Treatment C way" after experiment RENTOK-CREATIVE-QUALITY-001 — a board with feeling / framing / impact per beat executed by a board-driven code renderer, one new 8-pose sheet, everything else reused under verified provenance; accepted first time, "its already good", the checker's USD-0 repair round declined so ten recorded defects stay on the accepted file; 0:51:13 job start → DET-clean deliverable and 5:09:28 → ACCEPT (the difference is the customer's reply time); CpAO USD 0.067 for the job, USD 0.663 for every drawing in the film across three ledgers — stated separately, never blended; promoted hero-occlusion, framing-at-focus, world-fills-frame and sprite-density gates; evidence `work/agency-job-rentok-game-v2-001` @ `b06deaf`). Template `code_rendered_side_scroller_with_ai_sprites` now carries a `directed_board_v2` variant (n = 2 accepted jobs on the skeleton, one customer, one brief).
