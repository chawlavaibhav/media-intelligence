# Blind comparison — result (CANON-DONE-v0 §C)

Run 2026-09-22 on branch `work/canon-done-2026-09-22`. USD 0 (text only, no media call).

## Method, as executed

- Three real briefs, read from their job branches: **M** = MOKOBARA-ODYSSEY-007, **V** = RENTOK-GAME-V2-006, **A** = RENTOK-GAME-A-004.
- Three arms per brief, nine sessions in all, each seeing only its own packet and the shared board
  schema: **packs** = the ten compiled doctrine packs (the full 25,308-token injection payload);
  **handclaims** = the accepted claim texts a producer retrieved by hand on that job (22 / 25 / 32
  claims, full text); **nothing** = brief only.
- Each session wrote a Stage 3 board (`proposition`, beats with feeling / framing / first_frame /
  impact, hero frame, copy deck, mandatory items, brand timeline, deviations) to a code-named file.
- Arm codes sealed before any board was written; the map was held outside the repository and its
  sha256 (`b96ccc484a15378d12a3f3939744fe32fe33768d0cd8b3e88cf11ce431dec9ed`) committed in `SEAL.sha256`.
- Every identifier and citation was stripped from the nine boards (verified: zero id matches) so the
  judge could not tell an arm by its vocabulary.
- One judge session, no author of any board, ranked the three boards per job against
  `JUDGE-RUBRIC.md` — hero frame, beat craft, requirements on beats, **whether the board would have
  prevented that job's recorded failures**, brand and ask, honesty. Its verdict is
  `VERDICT-verbatim.md` (sha256 `76e20c48f1fa87f1…`), committed **before** the map was opened.

## Ranking (judge's words), then the arms

| Job | 1st | 2nd | 3rd |
|---|---|---|---|
| M | 137dd837 = **packs** | ac072eae = handclaims | 8a8d89da = nothing |
| V | 7cb5eaba = **packs** | 081c5a26 = handclaims | f1784420 = nothing |
| A | 8d76de10 = **handclaims** | a4753377 = packs | b2cf7ecc = nothing |

Points (3 / 2 / 1 per job): **packs 8 · handclaims 7 · nothing 3.**

## What this establishes

1. **Knowledge beats no knowledge, decisively.** The brief-only arm came last in all three jobs.
   The judge's profile of the three weakest boards — "a hero frame written in prose that no beat's
   `first_frame` actually orders, one clip carrying three actions, the brand mark arriving past the
   halfway point with no declaration, and a deviations list that is empty or nearly so" — is the
   same diagnosis CQ-001 reached on the flat RentOK film.
2. **Packs and hand-retrieved claims are close.** 8 versus 7 across three jobs; packs won two,
   claims won one. The compiled packs are therefore **not worse** than the retrieval they replace —
   which is the condition §C was written to test — but this is not evidence that they are better.
   n = 3, one judge, one model family.
3. **What actually distinguished the winners was not knowledge at all.** The judge, blind to arms:
   "The three strongest boards … win for the same three reasons, and none of them is knowledge" —
   a `first_frame` that already contains the idea, one job per clip with stated timing, and declared
   deviations. Those are **form** properties: the fields the stage forms require
   (`.claude/skills/media-agency/forms/`, `first_frame` added after the Mokobara retro-fit).
4. **The stop rule (decision ruling 7) does not fire.** The hand-retrieved arm did not beat the
   packs on all three briefs, so compilation stands.

## Honest limits

- n = 3 briefs, 1 judge session, boards and judge from the same model family; no customer saw these
  boards and no media was produced from them.
- Two of the three briefs (V and A) are the same job at different stages, so the three jobs are not
  three independent classes.
- The judge knew each job's recorded failures (that is criterion 4) but not which board came from
  which arm; the criterion rewards boards that address failures the arms could not have known about.
- A board is not a film. This measures the plan, not the outcome.
