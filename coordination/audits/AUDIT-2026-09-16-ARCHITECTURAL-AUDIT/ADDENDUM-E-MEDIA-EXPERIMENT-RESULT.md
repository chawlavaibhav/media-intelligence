# Addendum E — Controlled media experiment: result (2026-09-20)

Step 7 of the Controller's execution order. Same brief (Cumin Co. chopsticks film), same cap (USD 5.00 per job), credits only, no fal, both jobs run through the `/media-agency` mechanics in the experiment worktree from `origin/main` 4d919c9. Job A = the existing pathway (86ec183 blueprint and V1 compositor re-run unchanged). Job B = the five-stage pathway (QUESTION-TEMPLATE v0.1, checker at the gates, measured-VO timeline, gated compositor). Job records, ledgers, QA outputs and learning packets are on the branches `work/agency-job-cumin-exp-a-existing` (44f2c95) and `work/agency-job-cumin-exp-b-fivestage` (5c33173), committed, not pushed.

## Release-level result

| | Job A (existing) | Job B (five-stage) |
|---|---|---|
| Presented | 9:16, 4:5, 1:1 | 9:16 only (4:5, 1:1 held by the obstruction gate) |
| Review cycles | 2 (SPECIFIC REPAIR → REJECT) | 1 (REJECT) |
| Verdict verbatim | "all three rejected." | "rejected" |
| Reason stated | none | none |
| Spend reserved | USD 4.19 (21 paid calls) | USD 4.33 (25 paid calls) |
| Time to decision | 4 h 42 m | 4 h 46 m |

**Both films were rejected without a stated reason.** At the release level the experiment therefore does not separate the pathways. The blind judging planned in Addendum C (E6) has not run; without it and without reasons, no claim about final quality is supported either way.

## Process-level result (facts from the records)

| Observation | Job A | Job B |
|---|---|---|
| Defects caught before spend | 0 | 2 (wrong packshot on the end card at the animatic; wrong bowl on plate H2 at the still) |
| Defects that reached the reviewer | 1 generation defect (second pair of chopsticks) that the operator had accepted from a contact sheet showing it | 0 found on a 0.6-s frame sweep; the reviewer's "2 pair" note could not be located in this film and no timestamp was given |
| Deterministic defect found in the tooling | hard-coded clip names made a repair re-run byte-identical (caught by sha256) | none found |
| Geometries with copy over the subject | 4:5 and 1:1 shipped with backing cards over the hand/sticks (no obstruction gate) | 4:5 and 1:1 withheld by the obstruction gate |
| Provider refusals | 2 TTS content-filter refusals under the emotive direction; 1 music HTTP 500 | 1 music recitation-check refusal |
| Continuity defects the gates permit | — | super position jumps once (beat 3), wordmark alignment jumps once (two-shot) |

## What the result supports and what it does not

1. **Supported:** the five-stage path caught two asset errors at USD 0 and refused two geometries it could not compose cleanly; the existing path shipped its flagged geometries and one duplicated-prop clip. This matches the audit's K7/K14 findings (self-attestation; approval at the wrong altitude) and Addendum D's paper result.
2. **Supported:** the missing question on both paths was a prop count per sampled clip. It is added to the template as a candidate line with these two case ids, not as a rule (Question-template §Learning).
3. **Not supported:** any statement that either film was better. Both were rejected; reasons were asked for and not given; the blind panel has not run.
4. **Cost:** the five-stage path cost USD 0.14 more and about four minutes longer to the decision on this job; the auditions and the second plate account for the difference.

## Open items for the Controller

- Whether to run the E6 blind judging on the two rejected films anyway (the packet is ready), or to treat the rejection as the end of the media experiment.
- Whether to commit this audit folder (still untracked in `main`) and push the two job branches.
- The rejection reasons, if the release authority chooses to give them; both learning packets carry `reason_stated: null`.
