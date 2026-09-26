# After verdicts: which version is which, and every known confound

**Open only after verdicts.json is exported.** These notes name versions.

## Per brief

- **E01 (launch poster):** no version made both 1:1 and 4:5.
  - A is 1:1 (1024×1024): the code default is the first ratio in the brief.
  - B and C used the brief-reading step's single ratio, 1:1 (1080×1080), so all three main versions are square.
  - The MAI version follows the photo's shape (928×1120), because MAI's photo endpoint takes no size.
- **E02 (sweet shop):** A is 1:1 (no ratio in the brief). B and C are 9:16.
- **E04 (Crypto Sunray drop):** A is 1:1. B and C are 4:5 (1080×1350).
- **MAI side check:** the MAI version is 928×1120 on E01, E04 and E05, while A is 1:1 on all three.
- **E05 (photo edit):** no copy and no logo, so B and C show the edited photo as drawn.
- **E06–E07 (animations):** no finishing in any version, even though the B and C writers asked for music.
- **E08 (cold brew):** Lyria refused C's music line, so C's film has no music bed and B's has one. E08 C vs B is not a clean Canon test.
- **E09 (iPhone Duo):** B's scene 1 was re-made with its spoken line ("Wow, so clear!"). C's line was already in its prompt, in quotes.
- **E10 (Ascend Foods):**
  - A made 2 scenes (16.0 s).
  - B planned 5 scenes and C planned 4, because the brief-reading step guessed 30 s.
  - Veo blocked scene 2 on audio in both B and C. In both, the one retake went to scene 1, whose first take had failed the text check. So neither B nor C has scene 2.
  - B shows scenes 1, 3, 4 and 5 (34.6 s); C shows scenes 1, 3 and 4 (24.6 s).
  - B and C used more Veo clips than A. This breaks the "same number of media calls" rule.
- **E12 (Mokobara island):**
  - A made 2 scenes (16.0 s). B and C made 3, because the brief-reading step guessed 20 s: B is 22.6 s, C is 26.6 s.
  - Re-made with their spoken lines: B's scenes 1–2 and C's scenes 1, 2 and 3. C's scene 2 ("How much more?") was found by the final check and re-made last.
  - Both takes of C's scene 2 failed the text check (Veo drew garbled brand text), so C's retake shipped without a pick.
  - B's retake went to scene 1 (the riskiest), and the pick kept take 1.
  - B and C used more Veo clips than A.

## Across all briefs

- **Finishing:**
  - A gets none by design: whatever text the model drew, no logo overlay, no end card.
  - B and C get code finishing on E01–E04 and on the films E08–E12: exact copy, logo, end card, and (films only) music when the writer asked.
- **How films start:** A's films are Veo text-to-video, with the brief's photos as references where the brief has photos (E09, E12). B's and C's films start from a first-frame still.
- **Retakes in B and C:** when a scene's first take failed the code checks, the retake was used without a pick, even when it also failed. A's retake always goes to its riskiest scene, with a pick.
- **Luna's labels:** the brief-reading step (Luna) mislabelled the story films' class in its notes. The writers of B and C saw those notes.
- **Voice:** voice lines in B and C reach Veo only in quotes inside the scene prompt (fixed during the run; 6 scenes re-made). Practice T3's two lost lines were not re-made (practice is not judged).
- **Checks:** loudness is measured but never triggers a retake, and there is no audio-overlap check.

## Judge-screen tells that exist by design

- End cards, logos and exact copy appear only in B and C.
- Film lengths and scene counts differ in E10 and E12.
- Aspect ratios differ in E02, E04 and the MAI side check.
- In the still briefs, the A image appears in more pairs than the MAI image.

Everything the runner did differently from TEST-FLOWS.md is in RUN-LOG.md, with the founder's words for every override.
