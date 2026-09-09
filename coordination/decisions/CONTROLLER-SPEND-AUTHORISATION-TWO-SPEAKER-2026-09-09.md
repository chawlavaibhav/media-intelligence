# Controller — Spend Authorisation: two-speaker piece, cheap-first — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION. **Role:** Writer Controller, recording the human Controller's words.
**Parent rules:** `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` §3/§3a; hard limits as in
`CONTROLLER-SPEND-AUTHORISATION-IMAGE-HALF-TWO-AND-VIDEO-PIECE-1-2026-09-09.md` §4.

## 1. Authority — the Controller's words

Caps were quoted on 2026-09-09 (two speakers: full ₹1,700; cheap-first without Seedance 2.5 ₹950). After the day-2
reveal, having skipped the fal top-up and the ElevenLabs Indian voice ("i am skipping 1 and 2"):

> **"the two speaker we can do now."**

## 2. Scope — `VID-2SPK-01`, arm A_native (two people talking in Hindi, 8 s, 9:16), cheap-first

| Route | Surface / pool | Unit | Repeats | Cost | Status now |
|---|---|---|---|---|---|
| veo-3.1-fast | Vertex, credits | USD 0.10/s × 8 s | 2 | USD 1.60 | runs now |
| gemini-omni-1.1-flash | Vertex, credits | USD 0.10136/s × 8 s | 2 | USD 1.62 | runs now |
| kling-v3-pro-audio | fal, cash | USD 0.168/s × 8 s | 2 | USD 2.69 | **deferred** — fal balance exhausted (Controller skipped the top-up) |
| wan-3.0-prime | fal, cash | USD 0.14/s × 8 s | 2 | USD 2.24 | **deferred** — same |
| seedance-2.5 | fal | — | — | — | left out ("leave seedance 2.5 for now") |
| B_chain rows (plate, H3 Max i2v, TTS, lipsync) | fal / credits | — | 0 | — | recorded_not_screened in the package; fal-bound |

Runs now: **4 clips, USD 3.22 + one smoke (USD 0.81) = USD 4.03.** The two fal routes run under this same record if
and when the Controller tops up fal; until then the piece is a two-route screen and is reported as such.

## 3. Cap and hard limits

Cap **₹950 = USD 9.96 USD-equivalent** (`max_consumed_usd_equivalent`; `cap_1a_usd` = `cap_1b_usd` = 9.96; Sarvam 0;
ElevenLabs credits 0). Retries 0; price verified before every paid call; sealed evidence write-once; keys by name only;
blind judging by the Controller; Registry rows only from the deterministic instruments. Run ids `vid-2spk(-smoke)`;
authorisation file `eval/harness-v2/authorization.2spk.local.yaml` (gitignored), item basis commit 0ba06b92ee27
(the package is unchanged since).

## 4. Not authorised

Seedance 2.5; the B_chain arm; anything beyond the rows above.
