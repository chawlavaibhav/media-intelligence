# Morning: media bake-off v1, 26 Sep

**Status:** all 16 briefs made. 45 blind pairs are ready to judge. Nothing is scored yet.

## What ran

- One customer message per brief, sent to three ad makers:
  - **A**: Claude writes the prompts, the media model makes the ad. Nothing added.
  - **B**: Claude plus our pipeline: understand, write, check, retake, finish.
  - **C**: B plus the Canon notes in Claude's reading.
- **Side check** on the 5 still briefs (E01–E05): A's exact prompts sent to MAI-Image-2.6 instead of Nano Banana 2.
- 4 practice briefs (T1–T4) on B and C. Not judged.
- 12 exam briefs (E01–E12) on A, B and C. These are judged.

| Kind of ad | Made with |
|---|---|
| Ad stills E01–E04 · photo edit E05 | Nano Banana 2 |
| Animate a photo E06–E07 · product film E08 | Veo 3.1 Fast |
| Story films E09–E12 | Veo 3.1 standard |
| First frames of some films | Nano Banana 2 |
| Music beds, when the writer asked | Lyria |
| Side check E01–E05 | MAI-Image-2.6 |
| Writing and picking takes | Claude Sonnet 5 on the Claude subscription (set on the command line; not recorded per call) |
| Reading the brief | GPT-5.6 Luna |
| Text checks | Google Vision OCR |

## Spend

- **US$209.66** on the ledger, of the US$215 cap.
- Likely bill about **US$203.11**. The ledger counts two Veo clips Google blocked at full price (US$6.40; Google normally does not charge for those), plus US$0.15 reserved by stopped processes that never ran.
- Practice US$13.67 · stills and animations US$18.36 · films US$177.63. Claude calls cost US$0 cash (subscription).
- US$28.95 is kept out of each version's cost when costs are compared:
  - US$28.80 for 9 Veo clips thrown away because of a runner bug (below);
  - US$0.15 for two stills and small checks from attempts stopped by the budget change.
- Average cost per exam ad: A US$4.01 · B US$5.02 · C US$4.81. This counts the last attempt of each call, with blocked Veo clips at full price. Some films have more scenes than others (below).

## What went wrong, and what changed

- **Runner bug, fixed and re-made:** in 6 story-film scenes the writer's spoken line never reached Veo, so those scenes had no spoken line. They were re-made with the line in quotes in the Veo prompt, as the design says. The founder approved (US$215 cap).
- **Film lengths differ in E10 and E12:** the customers gave no length, so the films in those two briefs differ in length. Judge each film as a customer would.
- **Two films are missing a scene:** Veo blocked the same scene in two E10 films (audio). In both, the one retake went to an earlier scene that had failed the text check, so those two films have a gap.
- **Blocked by the services:** Veo refused 2 clips and Lyria refused 1 music line. The films were made without them.
- The Mac slept 11:27–12:51. Practice stalled, then restarted. Since then the Mac is kept awake.
- The founder's calls, all in RUN-LOG.md:
  - Claude on the subscription.
  - MAI-Image-2.6 on a new Azure resource.
  - Apple's own iPhone Duo photos for E09, the same for every version.
  - Cap raised to US$165, then US$215.
  - Briefs run side by side; only the total cap stops the run.
  - Stopped briefs resume where they left off.
  - The silent scenes re-made.
  - Two scoring clarifications (below).
- Notes that say which version is which are in **AFTER-VERDICTS.md**. So are the runner's differences from the written design. RUN-LOG.md and MANIFEST.sha256 name versions too. **Open all three only after exporting verdicts.**

## How to judge: 45 pairs, about 40 minutes

1. In Terminal, paste:
   ```
   cd ~/Vaibhav_Personal_Projects/bakeoff-media/run-2026-09-26/judge
   python3 -m http.server 8766 --bind 127.0.0.1
   ```
2. Open **http://127.0.0.1:8766/viewer.html** in Chrome.
3. The line under the title must say **Pair 1 of 45 · 0 judged**.
4. Make the window phone-narrow. Sound on, headphones in.
5. Each pair shows the customer's message, their answers, the photo count, the must-haves and the deal-breakers. Play both sides to the end.
6. Pick the side you'd rather pay for (clearly or slightly; "Can't choose" is a tie).
7. For each side, answer "would you pay the anchor price?" (Yes as-is / Yes after one small fix / No). If no, pick one reason. Answers save on every click.
8. At the end, click **Export verdicts.json**. Stop the server with Ctrl+C, then paste:
   ```
   mv ~/Downloads/verdicts.json ~/Vaibhav_Personal_Projects/bakeoff-media/run-2026-09-26/
   ```
   The file must be named exactly `verdicts.json`.

## What happens next

```
python3 ~/Vaibhav_Personal_Projects/media-intelligence/eval/media-bakeoff-v0/cost_report.py ~/Vaibhav_Personal_Projects/bakeoff-media/run-2026-09-26
python3 ~/Vaibhav_Personal_Projects/media-intelligence/eval/media-bakeoff-v0/score.py ~/Vaibhav_Personal_Projects/bakeoff-media/run-2026-09-26
```

This writes **SCORECARD.md**, using the rules fixed before any output existed (START-HERE §5, TEST-FLOWS §6):
- The pipeline beats Claude alone if B or C wins 8+ of 12 against A **and** gets 20+ points more "would pay".
- Per kind of ad: B wins 2 of every 3 → ship the pipeline for that kind. Otherwise ship A plus our finishing.
- The Canon stays only if C beats B more often than it loses **and** wins 7+ of 12. Then a 30-brief check.
- MAI vs Nano Banana 2: a direction only (5 pairs).
- Two clarifications the founder fixed at 18:07, after the outputs were made but before any judging:
  - a tie counts as not a win in the "2 of every 3" rule;
  - the MAI side-check answers stay out of A's "would pay".
- The cost line uses COSTS.json, so the re-made clips are left out.

The text records are committed on GitHub on `claude/magical-volta-q45jee`. The media stays on the laptop in `~/Vaibhav_Personal_Projects/bakeoff-media/run-2026-09-26`, with a fingerprint for every file in MANIFEST.sha256.
