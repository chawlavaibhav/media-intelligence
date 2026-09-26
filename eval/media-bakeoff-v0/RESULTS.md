# Bake-off v1 results (founder's verdicts, 26 Sep)

Scored by `score.py`. Checked by two independent recomputations, a sensitivity check (64 scoring variants) and a consistency check. Every flagged item was re-derived by a skeptic.

**44 of 45 pairs judged.** Pair 25 (E10 B vs A) was answered by the founder in chat: "both no, as their voice over is wrong", preferring the right one (A). E03's swapped repeat (pair 23) is unanswered; it is a consistency check only.

## The answers

| Question (rule fixed before the run) | Result | Verdict | Robust? |
|---|---|---|---|
| Does our pipeline (B) beat Claude + model (A)? (8 of 12 wins **and** +20 points would-pay) | B won 4, lost 6, tied 2. Would-pay: B 58%, A 46% (+12) | **No** | Yes. Even with every tie going to B, B reaches 6, not 8 |
| Does Pipeline + Canon (C) beat A? | C won 4, lost 7, tied 1. Would-pay: C 38%, A 46% | **No** | Yes. C's best case is 5 wins |
| Does the Canon help? (C beats B more than it loses **and** 7 of 12) | C won 4, lost 6, tied 2 | **No: keep the Canon out of the writer's context** | Yes. Its best case is 6. Without the confounded E08, E10 and E12 it is 4–4–1, still no |
| MAI-Image-2.6 vs Nano Banana 2 (same prompts; a direction only) | MAI won 3, lost 1, tied 1. Would-pay: MAI 5/5, NB2 4/5 | **Leans MAI** | Only 5 pairs, and the aspect ratio differs (MAI followed the photo's shape) |
| Cost (B and C at most 1.5× A) | B 1.25×, C 1.20× (redo clips left out). All-in: B 1.52×, C 1.53× | Within, on the comparable basis | Without E10/E12 the ratio is about 1.00× for both |

## Per kind of ad (B vs A; B needs 2 of every 3; a tie counts as not a win)

| Kind | B vs A | Call | Robust? |
|---|---|---|---|
| Story films E09–E12 | 2–2 (E10 went to A: both voice-overs wrong) | A + our finishing | Settled by pair 25. B's two wins were E11 and E12 (where B had an extra scene) |
| Photo edit E05 | 1–0 ("slightly") | Ship the pipeline | **Fragile.** One pair, and it flips if only "clearly" answers count |
| Product stills E01–E04 | 1–3 | A + our finishing | Yes |
| Animate a photo E06–E07 | 0–1–1 | A + our finishing | Yes |
| Product film E08 | 0–0–1 | A + our finishing | One pair |

## How much to trust this

- **12 pairs per comparison can only show big effects.** No comparison differs from a coin toss (two-sided p: B vs A 1.00, C vs A 0.55, C vs B 0.75). Each 95% range on a win rate is about 50 points wide. A significant result would need 10 of 12.
- **Repeat consistency ("33%") is not a fair measure here.** Only 3 swapped repeats were scorable:
  - E06 was a tie both times.
  - E04 MAI moved one step, from "slightly" to "can't choose".
  - E04 C vs B reversed, from "C slightly" to "B clearly".
  - With 3 repeats, 33% cannot separate a careful judge from a random one.
- **Would-pay answers for the same file shown twice agree 77% of the time** (moderate). A file got a "yes" 80% of the time in pairs it won, and 37% in pairs it lost, so the would-pay answer leans on what it was shown against.
- **"Would pay" is mostly "after one small fix".** Counting only "Yes as-is": A 30%, C 21%, B 4%.
- **Confounds** (AFTER-VERDICTS.md):
  - in E10/E12, B and C made more scenes than A;
  - two E10 films lack scene 2;
  - E08 C has no music;
  - A has no finishing by design.
  - None of these changes a headline answer; they matter only for the story-film class call.

## Bottom line

- Claude + the media model is as good as our pipeline on these 12 briefs.
- The one class where the pipeline won, the photo edit, rests on a single "slightly" answer.
- The Canon in the writer's context did not help.
- The recurring reasons for a No:
  - off-brief or identity drift (A);
  - audio or voice (B);
  - off-brief, boring, or artefacts (C).
- Voice-over quality is what sank the E10 films.
