# Stage 4 — Production selection (an independent route decision for THIS film)

Job `AGY-2026-09-21-MOKOBARA-ODYSSEY-001`. Requirement: a live-action-style cinematic film, 9:16, ~30 s, with ONE consistent human protagonist and ONE consistent branded bag across 6 generated beats, no in-model text, native ambience welcome, no speech. Code-rendered animation (the RentOK route) is ruled out: the brief is photographic survival cinema; nothing in it is a game or a graphic.

## Candidates (routing table on this base: `eval/capability-map/TAINT-REGISTER-v1.yaml`; prices from the runtime PriceBook via `tools/dispatch.py quotes`)

| Route | Cell | Evidence | prod | Price | Fit for this film |
|---|---|---|---|---|---|
| `veo-3.1-fast` t2v | VID-T2V/veo-3.1-fast | clean_observed 4/8 | true | 0.10/s | cinematic look + native audio, but identity is text-only: a bearded man and a navy bag will drift between 6 clips |
| **`veo-3.1-fast-i2v`** | VID-I2V/veo-3.1-fast-i2v | clean_observed 5/8 | true | 0.10/s | the first frame is fixed by a still → identity and bag likeness anchored per beat; the pilot's mechanism (hero still → i2v) |
| `veo-3.1-fast-ref2v` | VID-REF/veo-3.1-fast-ref2v+native | clean_observed 2/4 | true | 0.10/s | up to 3 "asset" references (a protagonist still + the product photo) with a free first frame — the designed cell for a consistent subject; weakest evidence (n=4) |
| `gemini-omni-1.1-flash` t2v | VID-T2V/gemini-omni-1.1-flash | clean_observed 8/8 | true | 0.10136/s | strongest t2v evidence, but no image conditioning in the registered cell → same identity-drift problem as Veo t2v |
| `nano-banana-2` | IMG-CORE/nano-banana-2 | clean_observed 7/8 | true | 0.067/img | the beat stills; with the product photos as reference images (the pilot's mechanism; **not a registered IMG-REF cell → micro-qualify**) |
| multi-shot (veo extend chain, omni 10 s), two-speaker | VID-MS/*, VID-2SPK/* | directional_only | manual_only | — | not authorised; not needed (per-beat clips stitched by code) |
| `lyria` | MUS/lyria+native | clean_observed 4/4 | true | 0.06/clip | the music bed |

## Decision — topology

**Hero still → per-beat stills → `veo-3.1-fast-i2v` per beat → stitch by code.**

1. One **hero still** (`nano-banana-2`, 9:16, references = two product photos: front view `…Private_Island_1.jpg`, open view `…Private_Island_6.jpg`): the protagonist crouched beside the bag on the grey shore. This is the identity master.
2. One **still per beat** (`nano-banana-2`, references = the hero still + the product front photo), each prompt restating the verbatim anchors: the first frame of each clip.
3. One **`veo-3.1-fast-i2v`** clip per beat (4/8/6/8/4/4 s, 9:16, 720p, native audio on, negative prompt: text, logos, speech, music), the prompt restating the anchors and the beat's action/camera/light.
4. Assembly by ffmpeg: trim to the board, stitch, wordmark super + end card by code, Lyria bed + native ambience mixed and normalised.

Why this over ref2v: i2v has the better evidence (5/8 vs 2/4) and gives the first frame — the bag's likeness is decided in a cheap USD 0.067 still that can be inspected before any USD 0.40–0.80 clip is bought. Fallback per beat (one recorded change): `veo-3.1-fast-ref2v` with the hero still + the product photo as assets.

**Riskiest capability: the gag (beat 4)** — Veo must animate a man pushing his arm into a backpack to the shoulder, then both arms, then draw out a paddle longer than the bag, without the geometry breaking (hands merging with fabric, extra limbs) and without lettering. Second: bag likeness from reference photos in nano-banana-2 (unregistered IMG-REF use). Third: face continuity across 6 clips. **Micro-qualification first, one draw each:** (a) the hero still (bag likeness + protagonist) → inspect; (b) the beat-4 still → inspect; (c) the beat-4 i2v 8-s clip → inspect against: identity kept, bag likeness kept, no lettering, cinematic look, the gag reads (arm in to the shoulder; something long comes out). PASS → proceed; FAIL → one recorded fallback (ref2v for beat 4, or the paddle-only version of the gag: one arm to the shoulder + the paddle) then stop and report if it fails again.

## Expected spend vs the USD 12.00 cap

| Item | Qty | USD |
|---|---|---|
| Micro-qual: hero still + beat-4 still + beat-4 clip (8 s) | 2 × 0.067 + 0.80 | 0.93 |
| Remaining beat stills (1, 2, 3, 5, 6) | 5 × 0.067 | 0.34 |
| Remaining clips (4 + 4 + 6 + 4 + 4 s) | 22 s × 0.10 | 2.20 |
| Music bed | 1 | 0.06 |
| **First full pass** | | **3.53** |
| Re-takes (one change each), ≤ 3 clips + ≤ 3 stills | ≤ 2.40 + 0.20 | ≤ 2.60 |
| Headroom (refusals count; hard stop at the cap) | | 5.87 |

Text by code (hb-view/Pillow, Avenir Next; wordmark from the SVG). End card by code. QA by code (`tools/qa_checks.py`), LJ for the human checker.
