# Blind comparison, round 2 — five arms (the founder's question: use the packs as notes, then read the right pages)

Run 2026-09-22, same day as round 1, on `main`. USD 0 (text only, no media call).

## The question

Round 1 tested three arms: the ten packs; the claims a producer had **already picked** for that job;
nothing. Nobody was allowed to **choose** what to read. The founder asked: "can we not consider
those 10 cheat sheets as notes and then from those notes, I can choose the right book to read or
right page to read across books and improve the creative angle? did we test it?" We had not.

## Arms (same three briefs, same board schema, same rubric and judge method as round 1)

| Arm | What the session was given |
|---|---|
| sheets only | the ten adopted packs (round 1, `packs`) |
| cards pre-picked | the claim texts a producer retrieved by hand on that job (round 1, `handclaims`) |
| brief only | nothing beyond the brief (round 1, `nothing`) |
| **sheets + index + READ pages** | the ten packs, a one-line index of all 1,300 accepted claims, and permission to fetch up to 25 claims in full by id, recording each one and whether it changed the board |
| **sheets + index, no reading** | the same packs and index, fetching forbidden (isolates *choosing and reading* from *more text*) |

Codes sealed before writing (`MAPPING-OPENED.json`, sha256 `47a7ccf832d92719…`); all fifteen boards
stripped of every id (verified zero matches); one judge, no author of any board, who had not seen
round 1, ranked five boards per job; its verdict (`VERDICT-verbatim.md`) was committed before the
mapping was opened.

## Result

| Job | 1st | 2nd | 3rd | 4th | 5th |
|---|---|---|---|---|---|
| M (Mokobara) | **read pages** | sheets only | index, no reading | cards pre-picked | brief only |
| V (RentOK v2) | **read pages** | index, no reading | cards pre-picked | sheets only | brief only |
| A (RentOK lane A) | **read pages** | index, no reading | sheets only | cards pre-picked | brief only |

Points (5/4/3/2/1 per job): **read pages 15 · index-no-reading 11 · sheets only 9 · cards pre-picked 7 · brief only 3.**

**The reading arm won all three jobs outright.** It is the only arm that placed first every time, and
the only one that beat every other arm on every brief. The brief-only arm came last every time, as
in round 1.

## What the reading sessions actually did

| Job | claims fetched | reported as changing the board |
|---|---|---|
| M | 24 | 20 |
| V | 17 | 16 |
| A | 20 | 17 |

Each recorded the id, the decision it was fetched for, and what changed. On M the session
independently reached for several of the same claims the human producer used in September (humour as
an accent; the product as hero; music channelling an emotion already created; the curiosity gap) —
the repeatability the design was meant to test.

## What the judge said separated the winners (blind to arms)

> "What separated the top boards from the bottom ones was not length, vocabulary or how much the
> board knew — the longest board in job M finished first and the second-longest in job V finished
> fourth."

Three things did: the `first_frame` carrying the argument ("the spear already risen a bag's height
out of the main compartment"); decisions made **with their cost named** ("The ten-second bound is
kept; the never-lapsing bound is not, and this is the deviation"); and feeling written as a specific
person's state ("a PG owner should see his own Tuesday, not a mascot") rather than a mood word.

## Reading, honestly

1. **Choosing and reading beats being handed notes, and beats being handed someone else's picks.**
   15 > 11 > 9 > 7 > 3 is a clean ordering across three jobs, not a one-brief accident.
2. **It is not merely more text.** The no-reading arm had the identical packs and index and placed
   second overall — 4 points behind. The gap between them is the choosing and reading.
3. **The packs still matter**: every arm above "brief only" had them, and the brief-only arm lost
   every job by a distance.
4. **Pre-picked cards are not a substitute for choosing.** The arm given the exact claims a human
   chose for that job placed fourth overall — the same knowledge, without the act of selecting it
   against this board, did less work.
5. **Limits.** Three briefs (two of them the same job at two stages), one judge, one model family,
   boards not films, no customer verdict. A clean sweep on n = 3 is a strong hint, not a law. The
   reading arm also costs more: ~20 claim fetches and roughly double the session tokens of the
   sheets-only arm.

## Consequence for P1

The Stage 3 step should be: **inject the ten packs, supply the claim index, let the producer fetch a
bounded number of claims by judgement, and record every fetch with `retrieved_by` and what it
changed** — which is exactly the "logged model step" the completion decision left open, now with
evidence behind it rather than an assumption. The fetch budget (25 here) and whether a cheaper model
can do the choosing are open questions for the next round.
