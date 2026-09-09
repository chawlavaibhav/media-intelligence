# Controller — Spend Authorisation: speech and music pieces, stacked on accepted clips — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION. **Role:** Writer Controller, recording the human Controller's words.
**Parent rules:** `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` §3/§3a; hard limits as in
`CONTROLLER-SPEND-AUTHORISATION-IMAGE-HALF-TWO-AND-VIDEO-PIECE-1-2026-09-09.md` §4;
`CONTROLLER-ELEVENLABS-DIRECT-NOT-FAL-2026-09-09.md` (ElevenLabs on the Controller's own key and plan credits).

## 1. Authority — the Controller's words

On stacking: *"can we not combine one of the video tests with music one so collapsing 2 test classes into one. i think
it is possible for more cases in our system."* — the Writer Controller proposed music judged on the accepted multi-shot
clips, speech feeding the two-speaker chain, per-stage verdicts. Then:

> **"proceed with speech and music pieces too"**

## 2. Scope

**Piece 6 — music (MUS-01, MUS-02)**, routes `lyria` (Vertex, credits, USD 0.06 a clip) and `elevenlabs-music-direct`
(ElevenLabs plan credits), 2 repeats each: 8 tracks of 30 s. Stacked judging view: each accepted track is laid under
an accepted multi-shot clip by code (`stack_audio.py`, USD 0) — MUS-01 (home, warm, bansuri/tabla) under the sleep
story `VID-MS-02` clip, MUS-02 (city running, builds) under the couple story `VID-MS-01` clip. The Controller judges the
raw track against the music contract (duration 28–32 s, no words, instrument colour / build) and notes fit-to-cut on
the stacked view separately. No video is bought.

**Piece 7 — speech (AUD-TTS-01..03)**, routes `sarvam-bulbul-v3` (Sarvam credits, INR) and `elevenlabs-v3-direct`
(plan credits), 2 repeats each: 12 files (Hindi, Hinglish, Indian-English scripts; chirp and Azure rows stay
conditional/unbuilt). Judged on listening against each contract.

**Piece 7b — lipsync (AUD-LIP-01..03)**, route `kling-lipsync-a2v` (fal cash, USD 0.014/s × 10 billed s), 2 repeats
each: 6 clips, on the Controller-accepted `VID-I2V-02` clip with the accepted repeat-1 ElevenLabs drive per script
(frozen rule; the Controller may substitute Sarvam). Runs only after the image-to-video verdicts name the plate.
`sync-lipsync-v3` is unpinned → excluded.

## 3. Caps (each piece its own authorisation file; one ceiling per piece)

| Piece | Cash / Vertex credits ceiling | Sarvam cap | ElevenLabs plan-credit cap | Run ids |
|---|---|---|---|---|
| 6 music | **₹300 = USD 3.14** (Lyria 4 × 0.06 + smoke) | ₹0 | **5 minutes of generated music** (4 × 30 s + smoke; expressed in the pin's credit unit) | `aud-music-lyria(-smoke)` now on the 13-field file; `aud-music-eleven(-smoke)` once the direct adapter and its cap field land |
| 7 speech | **₹100 = USD 1.05** (smoke/contingency; TTS itself is credits) | **₹20** (≈ 268 characters at ₹3 per 1,000) | **2,000 characters** (268 planned + smoke) | `aud-tts-sarvam(-smoke)` now; `aud-tts-eleven(-smoke)` once the direct adapter lands |
| 7b lipsync | **₹150 = USD 1.57** (6 × 0.14 + smoke) | ₹0 | 0 | `aud-lip(-smoke)` |

Retries 0; price verified before every paid call; sealed evidence write-once; keys read by name only, never printed;
blind judging by the Controller; Registry rows only from the deterministic instruments; stacked views are judging
views, never sealed artifacts.

## 4. Package change

The fal-hosted `elevenlabs-v3` / `elevenlabs-music` rows on AUD-TTS-01..03, MUS-01/02 and VID-2SPK-01 are re-pointed to
`elevenlabs-v3-direct` / `elevenlabs-music-direct` (decision above); the resulting commit is these pieces' item basis
commit and is named in each authorisation file.

## 5. Not authorised

Two-speaker piece (caps quoted, not approved); Seedance 2.5; anything beyond the rows above.

## 6. Writer Controller note — run split (2026-09-09)

The Sarvam and Lyria rows run first under 13-field authorisation files (`authorization.tts-sarvam.local.yaml`,
`authorization.music-lyria.local.yaml`, item basis commit 9adc4035d089). The ElevenLabs direct rows run as their own
runs once the adapter, the `elevenlabs_credits` pool and its cap field exist; the same per-piece ceilings apply across
both runs of a piece. Speaker choice for Sarvam: `aditya` (bulbul:v3; recorded via INPUTS `literal:` — see
`price-pins-2026-09/sarvam-bulbul-v3/SPEAKERS-PIN.yaml`).

## 7. Controller — ElevenLabs music skipped (2026-09-09)

The ElevenLabs music smoke was refused: HTTP 402 *"Music API is not available for free users. Please upgrade to a paid
plan to use the API."* (the account is on the free plan; nothing was charged). Put to the Controller:

> **"skip eleven labs music"**

`elevenlabs-music-direct` rows on MUS-01/02 are **not run**; the music piece is carried by Lyria alone (4/4 accepted
by the Controller, 32.8-s tracks). The rows stay in the package as `recorded_not_screened` until a paid plan exists.
