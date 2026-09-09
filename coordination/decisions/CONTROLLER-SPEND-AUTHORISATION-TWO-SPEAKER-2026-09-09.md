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
| kling-v3-pro-audio | fal, cash | USD 0.168/s × 8 s | 2 | USD 2.69 | runs now (Controller: "fal balance added") |
| wan-3.0-prime | fal, cash | USD 0.14/s × 8 s | 2 | USD 2.24 | runs now |
| seedance-2.5 | fal | — | — | — | left out ("leave seedance 2.5 for now") |
| B_chain rows (plate, H3 Max i2v, TTS, lipsync) | fal / credits | — | 0 | — | recorded_not_screened in the package; fal-bound |

Runs now: **8 clips on four routes, USD 8.15 + one smoke on a fal route (Wan, USD 1.12, proving the topped-up balance)
= USD 9.27 of the USD 9.96 cap.** (The Controller added the fal balance after the interrupt: "fal balance added".)

## 3. Cap and hard limits

Cap **₹950 = USD 9.96 USD-equivalent** (`max_consumed_usd_equivalent`; `cap_1a_usd` = `cap_1b_usd` = 9.96; Sarvam 0;
ElevenLabs credits 0). Retries 0; price verified before every paid call; sealed evidence write-once; keys by name only;
blind judging by the Controller; Registry rows only from the deterministic instruments. Run ids `vid-2spk(-smoke)`;
authorisation file `eval/harness-v2/authorization.2spk.local.yaml` (gitignored), item basis commit 0ba06b92ee27
(the package is unchanged since).

## 4. Not authorised

Seedance 2.5; the B_chain arm; anything beyond the rows above.

## 5. Writer Controller note — Kling refused again (2026-09-09)

After the Controller's "fal balance added", the Wan smoke and both Wan draws went through (USD 3.36 on fal), then both
Kling v3 Pro audio draws were refused with HTTP 403 *"Exhausted balance"* — the added balance ran out before the
Kling rows (USD 1.34 each). Infrastructure refusal, nothing generated or charged. Six clips sealed (Veo fast, Gemini
Omni, Wan); spend USD 9.27 of the USD 9.96 cap. The Kling rows can run under this record's headroom (USD 0.69 —
insufficient for two draws at 1.34; a further top-up AND a ₹150 cap addendum would be needed) — the Controller decides.

## 6. Controller — "blance exits on fal." (2026-09-09): Kling rows retried under a ₹150 addendum

The Controller states the fal balance exists. The two Kling v3 Pro audio draws are retried (a Kling smoke first, then the
lane rows) under a cap addendum of **₹150: the piece cap becomes ₹1,100 = USD 11.53**. If fal refuses again with the same
message while Wan dispatches on the same key, the refusal is recorded as a per-model balance hold on fal's side, with the
exact message, for the Controller to take up with fal.

## 7. Kling smoke went through; lane rows under a further ₹200 (2026-09-09)

The Kling smoke (USD 1.34) dispatched cleanly on the same key that was refused twice minutes earlier — the earlier
refusals were fal-side (balance propagation after the top-up), recorded as infrastructure. The Controller: *"fal
currently has 20 dollars"*. The smoke consumed the addendum's headroom, so the two Kling lane draws (USD 2.69) run under
a further **₹200: piece cap ₹1,300 = USD 13.63**; expected total USD 13.30. Run id `vid-2spk-kling`.
