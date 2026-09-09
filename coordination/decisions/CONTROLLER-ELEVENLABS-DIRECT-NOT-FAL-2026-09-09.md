# Controller — ElevenLabs is used directly (own key and plan credits), never through fal — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION. **Role:** Writer Controller, recording the human Controller's words.

## Authority — the Controller's words

After adding `ELEVENLABS_API_KEY` to `~/.mi-keys` (name only ever read by the harness; the value is never printed):

> **"use eleven labs from the key added. not from fal"**

## Decision

1. Every ElevenLabs route in the programme dispatches to ElevenLabs' own API with the Controller's key and is billed
   to the Controller's ElevenLabs plan credits — a new billing pool `elevenlabs_credits` with its own cap field in the
   authorisation record (`elevenlabs_cap_credits`; 0 = forbidden), handled like `sarvam_credits`.
2. The fal-hosted ElevenLabs routes (`elevenlabs-v3`, `elevenlabs-music` via fal) are **retired from the frozen
   package**: their rows in `TEST-CASES.yaml` (AUD-TTS-01..03, MUS-01/02, VID-2SPK-01 chain arm) and their
   `COST-TABLE.yaml` catalogue records are re-pointed to `elevenlabs-v3-direct` / `elevenlabs-music-direct` when the
   direct adapter lands (a package change → new item basis commit → each later spend record names it).
3. Price basis for the direct routes is ElevenLabs' own pricing page (pinned bytes under
   `eval/empirical-planning/price-pins-2026-09/elevenlabs-direct/`), expressed in plan credits; the USD-equivalent
   shown against caps is the plan's per-credit rate, recorded on the pin, never a fal price.
4. No ElevenLabs call is made until a speech or music piece has its own signed spend record.

Not decided here: which speech/music piece runs next, or its cap.
