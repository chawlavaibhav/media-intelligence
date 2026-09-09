# EVAL-040 — Day 2 summary (2026-09-09): video pieces 2–5, speech, music, lipsync

All verdicts are the Controller's, blind (names hid route and arm), against each case's acceptance contract. Human
acceptance is product evidence in the routing map; the Capability Registry holds only the deterministic rows
(format, cost, latency/errors, reliability, repeat consistency), 459 rows at the end of the day, validator PASS.
Spend records: `CONTROLLER-SPEND-AUTHORISATION-VIDEO-PIECES-2-TO-5-CHEAP-FIRST-2026-09-09.md` (+ addenda),
`…-VIDEO-PIECE-1-NB-PLATES-ADDENDUM-…`, `…-SPEECH-AND-MUSIC-STACKED-…`. Seedance 2.5 left out on the Controller's word.

## Results by piece

| Piece | Route | Accepted | Cost per clip / file | Controller's words |
|---|---|---|---|---|
| Text in motion, arm A2 (addendum) | Nano Banana 2 plate → MiniMax H3 Max | 2 / 2 | ≈ USD 0.61 per accepted clip | "both correct" |
| Knee (product hero, strict physics) | Veo 3.1 full | 1 / 2 | USD 2.40 | one "no slow camera" |
| | Veo 3.1 lite | 0 / 2 | USD 0.30 | "no slow camera", "got a label" |
| | MiniMax H3 Max 480p | 0 / 2 | USD 0.30 | "no condensation", "got a label" |
| Multi-shot 15 s (couple story) | Kling v3 Pro | 2 / 2 | USD 1.68 | clean |
| | Veo 3.1 fast extend chain | 2 / 2 | USD 2.00 | one "a little visually bad" |
| Multi-shot 10 s (sleep story) | Gemini Omni 1.1 Flash | 2 / 2 | USD 1.01 | "clean" |
| | Kling v3 Pro | 2 / 2 | USD 1.12 | "technically correct but visually not amazing" |
| Image-to-video (4 accepted stills) | Kling v3 Pro | 8 / 8 | USD 0.67 | two "expression turns angry" |
| | Wan 3.0 Prime | 8 / 8 | USD 0.84 | one "angry" |
| | MiniMax H3 Max | 7 / 8 | USD 0.48 | "label appeared out of thin air"; one "angry" |
| | Veo 3.1 fast | 5 / 8 | USD 0.60 | 0/2 on the phone still: "zooms in"; "hand appeared" |
| Reference-to-video (8 s) | Veo 3.1 fast ref2v | tin 2 / 2; person 0 / 2 | USD 0.80 | person: "some different language" (stray script) |
| Speech (3 scripts) | Sarvam bulbul:v3 | 6 / 6 | INR 0.13 | — |
| | ElevenLabs v3 direct (premade male voice) | 4 / 6 | 298 plan credits for six | Hinglish 0/2 "rejected for accent" |
| Music (2 briefs, 30 s) | Lyria 2 | 4 / 4 | USD 0.06 | tracks 32.8 s (trim by code) |
| | ElevenLabs Music direct | not run | — | HTTP 402 on the free plan; "skip eleven labs music" |
| Lipsync (3 scripts on the accepted lobby clip) | Kling lipsync a2v | pending (5 of 6 sealed) | USD 0.14 | one trial refused: fal balance exhausted |

## What the day says

1. **Cheap-first holds for animation and stories.** Kling and Wan animated every accepted still cleanly; Kling 15 s and
   Gemini Omni 10 s carried three-shot stories at a third of Seedance's price. Seedance 2.5 was never needed.
2. **The boundary of cheap-first is physical detail on a product hero.** The knee brief (condensation, blank label, slow
   camera) failed on every cheap draw and only half of the premium draws. That is RR-10: premium tier plus re-draws, or
   set the label by code.
3. **Veo's recurring weakness is text hygiene**, not identity: fabricated Devanagari (piece 1), stray script in the
   cafe scene (reference), a label from thin air (H3 Max once). Where a scene must carry no lettering, post-check it.
4. **The whole cheap chain for text in motion is now proven end to end**: Nano Banana 2 plate (USD 0.067) into
   H3 Max (USD 0.48) passed 2/2 where Veo 3.1 full and Kling v3 Pro scored 0/4.
5. **Speech: Sarvam is the Indian-language default** (6/6 at a paisa scale); ElevenLabs on the account's American
   premade voice passes Hindi and English but not Hinglish. **Music: Lyria on credits** at USD 0.06 a track.
6. **Stacked productions work as a judging method**: music was judged raw and under the accepted clips; lipsync rode on
   the accepted image-to-video clip with the ElevenLabs drives; no video was bought for the audio pieces.

## Infrastructure facts recorded today

- Vertex reference-to-video supports only 8-s clips (6 s refused); Lyria returns `bytesBase64Encoded`, not the pinned
  `audioContent`; Gemini Omni caps a clip at 10 s (the 15-s row was refused by the planner, not run).
- ElevenLabs Music API is paid-plan only; the account is on the free plan. fal balance ran out during lipsync.
- Harness additions: `--arms` planner filter, literal choice inputs (voice ids), ElevenLabs direct adapter and
  `elevenlabs_credits` pool, `stack_audio.py`, Lyria response-key tolerance; 268+ tests green.

## Open

Lipsync verdicts (set P) and the one refused lipsync draw after a fal top-up; an Indian voice on the ElevenLabs
account for the Hinglish retry; the two-speaker piece (caps quoted, not approved); Seedance 2.5 as a premium reference
only where the cheap routes failed (the knee brief).
