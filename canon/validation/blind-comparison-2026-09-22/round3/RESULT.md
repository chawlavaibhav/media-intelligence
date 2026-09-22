# Blind comparison, round 3 — does enforcing the order help, and is the selection intelligent?

Run 2026-09-22 on `main`. USD 0. Twelve boards, four arms × three briefs, one judge who had seen
neither earlier round, ids and direction labels stripped, mapping opened after the verdict was committed.

## Arms

| Arm | What the session was given |
|---|---|
| sheets only | the ten adopted packs |
| deep reading | packs + the 1,300-line claim index + up to 25 self-chosen claims fetched in full (round 2's winner) |
| **directions-first** | the same as deep reading, but forced to write a closed `directions.json` (questions → what it read → specific shootable directions) **before** any beat, with each beat tracing to a direction — the founder's fix for post-hoc citation |
| **random 25 (control)** | packs + 25 claims drawn from the whole corpus **without reference to the brief**, same reading volume, no choosing — ChatGPT's proposed control |

## Result

| Job | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|
| M (Mokobara) | deep reading | random 25 | sheets only | **directions-first** |
| V (RentOK v2) | deep reading | random 25 | directions-first | sheets only |
| A (RentOK lane A) | **directions-first** | deep reading | random 25 | sheets only |

Points (4/3/2/1): **deep reading 11 · random 25 8 · directions-first 7 · sheets only 4.**

## What this says, honestly

1. **Deep reading holds.** First or second on every brief, across two rounds and two independent
   judges. Reading full claims chosen against the brief is the best arm we have tested.
2. **Enforcing the order did not help — and on two briefs it hurt.** The Controller's proposal
   (read → closed directions → board) placed 4th, 3rd, 1st. It is not supported by this test.
   The Mokobara case shows the mechanism: the directions board wrote excellent, specific directions
   and then **dropped the arms gag** and **introduced a pole that exists in no earlier beat** —
   the same magical-object failure (D5) the customer complained about on the real film. Committing
   to directions before holding the whole film in view appears to cost continuity and the ability
   to keep the brief's own joke central. It won job A outright, so it is not refuted, merely
   unsupported on 3 briefs.
3. **The control changes the round-2 story.** 25 claims chosen **at random** placed second overall,
   ahead of sheets-only on every brief. So a large part of round 2's win was *reading full claim
   text at all*, not the intelligence of the selection. Choosing still beat random (11 vs 8), but
   the margin is much smaller than round 2 implied. ChatGPT's control was the right call.
4. **What separates good boards is unchanged across all three rounds** (judge, blind): the
   `first_frame` must carry the argument ("the spear already risen a bag's height out of the main
   compartment"); objects must be accounted for between beats or the gap declared; specificity must
   reach the picture rather than the label.

## Limits

Three briefs (two of them one job at two stages), one judge per round, boards not films, no customer
verdict, single model family. Round 2 and round 3 used different judges and ranked the same
deep-reading arm first — that is the one result with replication behind it.

## Consequence

- The paid film uses **deep reading**: packs injected, claim index supplied, a bounded number of
  self-chosen claims read in full, every fetch logged with what it changed.
- **No change to the adopted packs, the stage forms or P1 architecture** on the strength of these
  planning tests, per the Controller's instruction. The directions-first idea is recorded as tested
  and not supported; it may be worth re-testing as an optional step for jobs with many objects to
  track, where it won.
