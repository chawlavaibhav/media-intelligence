# Stage 3 — Creative · AGY-2026-09-20-RENTOK-GAME-LANE-B-001 (lane B)

Author: lane-B producer session. Date: 2026-09-20. Cost: USD 0.
Gate rule: a board exists (numbered frames, timecodes summing to 30.0 s, a copy deck, a numbered hero frame); every mandatory event from Stage 1 sits on a numbered frame; a non-author answers the structure checklist against it.

---

## 3.0 — Deterministic Canon pack lookup (PRODUCTION-WORKFLOW §4)

`brief.job.json` (PRODUCTION-JOB-v1, hand-written; kind `multi_shot_story`, operation `generate`, modality `video`, one `logo` reference asset = the wordmark) → `runtime.canon.lookup(normalize(job))`. Output saved verbatim to `stages/evidence/canon-lookup.txt`:

- selected: concept_and_distinctiveness · critique_and_effectiveness · composition_and_attention (compiled_accepted) · colour_and_visual_register · camera_and_spatial_grammar · editing_pacing_and_short_form · typography_and_copy · product_appearance (compiled_accepted) · indian_indic_context · commercial_communication
- injected: `composition_and_attention`, `product_appearance` · gaps: the other eight (fired, not compiled — recorded, never invented)
- prefix sha256 `4d7a5b27e17c5ff3b0561521b0b1b540b995562bb0dc94b6f188a5ebcec1c8fe`, 5,298 tokens, 21 check ids.

`product_appearance` fired because the brief carries a `logo` reference asset (KIND-NR-BINDING `product_entity_roles`); the "product" here is an app and a wordmark, so several PA lines are `n-a` below, each with the reason.

## 3.0b — Canon actually retrieved for this brief (claim text in `stages/evidence/canon-claims-*.txt`)

Rule applied: a domain is listed as consulted only where the claim text was retrieved from `canon/knowledge/current/**/source-knowledge.yaml` and is quoted or paraphrased here with its id. Where nothing accepted exists, `GAP` with the alternative source.

| Domain | Retrieved ids + the claim text used | How it shaped the plan |
|---|---|---|
| Advertising structure (hook, brand-early, ask, close) | sk_ogx_0040 "the first frame as the gate … when advertising fire extinguishers, open with the fire" · sk_abcd_0007 "beginning in the middle of the action" · sk_abcd_0010/0011 brand "early, often, richly … an early appearance that then lapses does not satisfy it" · sk_ogx_0039 "use the name within the first ten seconds … Commercials that end by showing the package" · sk_abcd_0019 the ask may be carried by "a scene from the story itself" · sk_abcd_0020 CTA tied to a specific objective · sk_abcd_0021 on-screen CTA paired with a voice saying the same · sk_abcd_0026 "start with a mix of branding elements and finish with the product … calls to action throughout … more direct as it proceeds" · sk_abcd_0013 branding assets include "graphic elements, voice-overs and musical treatments" | No start screen: F1 opens mid-run with the first obstacle by 1.2 s. The brand is on screen at 0.0 s as a greyed HUD slot `RENTOK MODE: OFF` (in-story, no claim), recurs at the cheat code, the install, every beam hit, the flag and the end card. The ask is the story (the cheat code IS "install RentOk"), then explicit on the end card with a spoken twin. Last frame = wordmark + CTA. |
| Narrative progression | sk_sb_c003_0008 "the customer occupies the hero role and the brand occupies the guide role" · sk_whip_0015 the brand is "the archetype the hero meets — the figure who … grants a power before the hero returns transformed" · sk_whip_0011 "a brand story requires an opposing force … most briefs remove it" · sk_sb_c003_0012 "stakes must be named and dosed … failure is like salt" · sk_sb_c003_0004 story "identifies an ambition, defines what stands in the way, and provides a plan" · sk_sb_c003_0015 grunt test: what you offer, how life gets better, what to do — within five seconds · sk_ctg_0053 "the thing you want transmitted must be load-bearing in the story, such that removing it makes the story unretellable" · sk_hea_mts_0012 concreteness: "explaining the idea in terms of human actions and sensory information" · sk_hea_mts_0016 "we are wired to feel things for people, not for abstractions" | The PG owner is the hero; RentOk is the power-granting guide, never the hero. The opposing force is real and dosed: hearts fall 3→1 across five obstacles, then one freeze (`CONTINUE?`) — no longer. The phone loaded with the app is the weapon, so the brand is load-bearing (take the phone away and there is no second half). Every obstacle is a concrete PG event, every clear is a concrete product state from Stage 2's permitted list. One named individual (the owner), not "owners". |
| Attention / hierarchy | sk_ms_c003_0016 "a colour established earlier identifies a figure the frame cannot resolve" · sk_ms_c003_0019 "two competing attention cues confuse rather than direct" · sk_ms_c003_0017 blocking alone can direct attention with a static wide camera · sk_fre_c003_0024 a figure supplies scale "but only above a size that depends on the print" · sk_fre_c003_0017 placement is three zones (centre / off-centre / edge), not a coordinate · sk_vig_c003_0009 "difference of scale within the same page gives strong impact" | The owner wears one warm colour (ochre shirt) against a blue/dusty world so he is found instantly at phone size; obstacles are each one silhouette + one label, never two cues at once; camera is a plain side-scroll (blocking does the work). Character height ≈ 1/7 of frame (≈ 270 px), the "print size" being a phone. Hierarchy by scale: card > label > HUD. |
| Editing / pacing / motion | sk_gote_c003_0004 "each shot cut to must give the viewer information it did not already have" · sk_gote_c003_0006 every departure from a shot is motivated · sk_gote_c003_0053 shot length = the time it takes to describe the shot aloud · sk_gote_c003_0052 the fast-cut short-form norm ("a shot longer than three seconds as boringly long") · sk_gote_c003_0017/0018 and sk_gos_c003_0007 screen direction and side-of-frame persist · sk_gote_c003_0048 "sound establishes a reality more quickly than picture" · sk_gote_c003_0037 the fade marks an act boundary · sk_murch_c003_0020/0027 emotion first; sacrifice from the bottom of the list · sk_ms_c003_0002 a camera move must have a reason, and so must stillness | One continuous side-scroll (no cuts) through the struggle; the only hard cuts are the freeze (F7), the world change (F9) and the end card (F17), each carrying new information. Every label holds ≥ 1.2 s (describe-aloud rule); beats 1.6–2.0 s inside the short-form norm. Direction is left→right throughout. The freeze is a stillness with a reason. SFX carry the hits before the eye confirms them. |
| Typography / readability | sk_wcag_0001 4.5:1 minimum contrast for text · sk_wcag_0031 large bold text may drop to 3:1 · sk_wcag_0022 thin or unfamiliar letterforms are harder to read · sk_wcag_0007 colour must not be the only visual means · sk_wcag_0004 logotype text is exempt · sk_sam_c003_0021 text over an image needs value contrast and still follows the structure · sk_whip_0033 exclamation marks read as desperation · sk_whip_0029 puns have no persuasive value · sk_ogx_0007 name the audience in the headline · sk_ogx_0009 specifics beat generalities; superlatives convince nobody | All in-game text is bold, wide-stroke, caps, on an opaque dark plate (contrast measured ≥ 4.5:1 by the compositor gate, not assumed); every state change is a shape + a tick/colour, never colour alone; no exclamation marks anywhere in the deck (the ChatGPT title's "!" and "LEVEL COMPLETE!" are dropped); the audience is named in the HUD (`PG OWNER`) and the closing line (`PG OWNER? LEVEL UP.`); no superlatives, no statistics. |
| Shot design (2-D world) | sk_gos_c003_0006 "the film world must obey constant physical rules" · sk_fre_c003_0008 a vertical frame is not by itself a sense of tallness; opposing elements at the frame's extremes make it read | The level obeys one gravity, one ground line, one run direction. The 9:16 frame is justified by a tall PG building facade filling the height (sky above, street below), with the action band in the middle. |
| Indian context / register | sk_ppm_0001 "say it with respect for the audience, in a context the audience can understand … to delight rather than to intimidate" · sk_dpci_0040 props carry class/modernity codes (a mobile phone as a modernity marker) · sk_dpci_0070 clothing is a grammar the audience already holds | The owner is never the joke; the phone is the modernity marker that changes his state; his dress is everyday Indian (checked shirt, trousers, chappals, keys at the belt) so PG owners recognise themselves. |
| Counter-evidence honestly recorded | sk_ogx_0038 "Cartoons can sell to children but are below average with adults, holding the viewer less well than live action" · sk_mla_0064 (Hopkins) "amusement buys attention from the wrong people" | These argue against a cartoon game for a B2B-ish buyer. The customer mandated the game concept (M1), so this is a recorded tension, not a reason to change concept. Mitigation: the obstacles are the buyer's literal daily problems and each clear is a literal, cited product state (concreteness), so the amusement is not detachable from the sale (sk_ctg_0053). |
| Animation / game-art craft | **GAP — no accepted Canon on animation, sprite design, game feel or motion design.** Alternative source: explicit reasoning from platformer conventions (side-scroll, HUD, hit flash, knock-back, power-up glow, flagpole finish), all genre-generic and not owned; the IP do/don't list at Stage 2 §2.5 is the constraint. | Stage 4 records the conventions used in the animation script. |
| Audio (music, SFX, voice) | **GAP — Canon's own coverage-gap notice: no accepted source covers audio production.** Alternative: routing evidence (RR-12 Sarvam default voice, RR-13 Lyria default music), cases 001/002 (RO-05 long narration cadence; RO-09 Lyria wording sensitivity) and explicit reasoning. | Audio decisions are attributed to evidence/reasoning, not Canon. |
| Colour | **GAP** (colour_and_visual_register fired, not compiled). Alternative: the brand's own palette (Stage 2 §d) and sk_ms_c003_0016 for identification by colour. | Palette below. |

---

## 3.1 — Proposition (one sentence)

**For a PG owner, RentOk is the cheat code: install it and the day's five obstacles — the unverified tenant, the unpaid rent, the tenant who left owing, the accounts mess, the complaint calls — turn into tracked, handled tasks.**

Grunt test (sk_sb_c003_0015) at 5 s of the film: what is offered — a game about a PG owner's problems (the app is named in the HUD slot); how life gets better — not yet (deliberately: the struggle must be felt first); what to do — not yet. By 16 s all three are answered on screen. Recorded as a knowing deviation from "within five seconds", forced by the customer's structure (struggle → cheat code → power).

## 3.2 — Hero frame

**F10** (16.0–17.8 s): the owner, phone raised, fires the blue OK beam at the blank-ID `UNVERIFIED TENANT` creature; on the hit the creature turns into a tenant card with a photo and a green tick. Without any copy a viewer sees: the man with the phone made the unknown tenant known. PA-D7 one line: *the app verifies the tenant.* If that line needed the label, the frame would fail — it does not.

## 3.3 — Opening frame

F1: mid-action close on the owner already running right along a PG street; the first obstacle enters by 1.2 s. Event in frame: the run + the HUD popping in (hearts, `PG OWNER`, `LEVEL 1`, `RENTOK MODE: OFF`). No start screen, no title card (CHANGE from the supplied direction, see table).

## 3.4 — Brand timeline

| t (s) | element | form |
|---|---|---|
| 0.0 | `RENTOK MODE: OFF` | HUD power-up slot, greyed, top band inside the safe box (code-set) |
| 12.6 | `CHEAT CODE: INSTALL RENTOK` | typed-in cheat bar (code-set) + announcer line V1 |
| 14.4 | app icon + `RENTOK MODE: ON` | phone rises, icon fills, slot lights up; hearts refill; world palette shifts; announcer V2 |
| 16.0–25.0 | OK beam | brand-blue/cyan beam and a cyan "OK" glyph on every hit (code-drawn; the glyph is set in type, not the wordmark) |
| 25.0 | flag | flagpole with a blue flag carrying the wordmark |
| 27.8–30.0 | end card | wordmark (with its tagline) + `PG OWNER? LEVEL UP.` + `Get the app`; announcer V3 |

Brand-early (0.0 s), often (six beats), richly (HUD, type, icon, beam, flag, wordmark, voice, music) — sk_abcd_0010/0013.

## 3.5 — The ask

In the story: the cheat code `INSTALL RENTOK` (F8) — the viewer is told what to do by the game itself (sk_abcd_0019). Explicit: end card `Get the app` (the site's own CTA, PC6a), spoken by the announcer in V3 ("Level complete. Get the app.") so the on-screen line and the spoken line are identical (3.8, sk_abcd_0021). Objective: app-install intent (Stage 1 §1.2).

## 3.6 — Last frame

F17 end card, held 2.2 s: brand-blue panel, `PG OWNER? LEVEL UP.` (84 px caps), the wordmark centred (its tagline "India's renting superapp" is part of the mark), `Get the app` as a rounded button-style card (64 px). Nothing else. sk_abcd_0026 / sk_ogx_0039 "finish with the product / the package".

## 3.7 — Mandatory events ↔ frames

| Stage 1 id | frames |
|---|---|
| M1 game reads as a platform game | F1–F16 (game frame runs 0.0–27.8 s = 27.8 of 30 s; ≥ 24 s required) |
| M2 PG owner recognisable | F1 (identifiers + HUD `PG OWNER`), continuous |
| M3 five obstacles = five problems | F2 O1 · F3 O2 · F4 O3 · F5 O4 · F6 O5 (labels on introduction) |
| M4 cheat code = install RentOk, central turning point | F7 (freeze) → F8 (cheat code) → F9 (install) at 11.2–16.0 s, the film's middle |
| M5 visibly enhanced ability | F9 (phone + glow + hearts refill + `RENTOK MODE: ON`) |
| M6 overcomes all obstacles, reaches the flag | F10–F14 (five clears) · F15 (flag) · F16 (`LEVEL COMPLETE`) |
| M7 30 s | timecodes sum to 30.0 |
| M8 platform fit / safe zones | every text box inside x 65–1015, y 269–1248 (Stage 4 code check) |
| M9 original | Stage 2 §2.5 rules applied to every design and prompt |
| M10 relevance | the five obstacles are the owner's five named problems; the end line names him |
| M11 no unverified claim | copy deck scanned against the forbidden list (below: clean) |

## 3.8 — On-screen = spoken

| VO id | frame | spoken (announcer) | on-screen twin |
|---|---|---|---|
| V1 | F8 | "Cheat code: install RentOk." | `CHEAT CODE: INSTALL RENTOK` |
| V2 | F9 | "RentOk mode: on." | `RENTOK MODE: ON` |
| V3 | F16–F17 | "Level complete. Get the app." | `LEVEL COMPLETE` (F16) + `Get the app` (F17) |

No other speech. Register: arcade announcer (short, declarative, Indian English) — a game convention that carries the brand name in audio (sk_abcd_0012) without turning the film into a narrated advertisement (customer: "not a conventional promotional video"). Muted test passes without it.

## 3.9 — Copy zones per frame

All copy sits inside the Meta safe box (x 65–1015 · y 269–1248 on 1080×1920). Zones (y ranges are the layer's vertical centre band):
- HUD strip: y 290–380 (top of the safe box) — hearts left, `LEVEL 1` centre-left, `RENTOK MODE: OFF/ON` right (x ≤ 1015).
- Name tag `PG OWNER`: floats 40 px above the character's head (character head at ≈ y 880 when standing on the ground line y ≈ 1150); never over his face (tag is above, not on).
- Obstacle labels: 40 px above each obstacle (obstacle tops ≈ y 850–950 → labels ≈ y 780–850), inside the box; a label may wrap to two centred lines (`may_reflow: true` for C04–C08 only).
- Transformation cards: centred at x 540, y 700 (above the action, below the HUD) — never over the character (character stays left-third, cards centre).
- Cheat bar / `CONTINUE?` / `LEVEL COMPLETE`: centred at y 760 on a dark opaque plate.
- End card: line at y 640, wordmark y 880–1080, CTA button y 1180 (bottom edge ≤ 1248).
- Right-edge rule (Stage 2): no critical text with x > 950 in y > 960.

## 3.10 — Voice casting (answer format: audition)

Line for the audition: V3 "Level complete. Get the app." is the longest (28 chars) and carries the CTA. Candidates (≥ 2): (A) Sarvam bulbul:v3, an English male speaker at default pace (AUD-TTS clean 6/6, RR-12 default; ≈ USD 0.0001 by the harness figure) · (B) ElevenLabs v3 on a premade English voice (AUD-TTS clean 4/6; plan credits, USD 0 cash; RR-12: fails Hinglish on accent, but V1–V3 are English) · (C, USD 0) a code-synthesised "vocoder-style" announcer is NOT a candidate (no evidence, and it would read as cheap). The audition happens at Stage 5 before any plate is animated, judged by ear on the assembled three lines for: crisp consonants, no cadence wobble on "RentOk", reads as an arcade announcer not a narrator. Frozen once chosen (one source for all three lines — SINGLE_VOICE_SOURCE candidate pattern).

## 3.11 — Visual system (compiled pack fields)

- World: a 2-D side-scrolling PG street in an Indian city — a three-storey PG building facade with balconies, a water tank, a parked scooter, a "PG" nameplate (the letters "PG" are not brand text; if the generated plate shows lettering it is text-scanned and, if wrong, painted out by code); ground = pavement tiles; sky = flat gradient.
- Two palettes: **before** (dusty warm: sand `#E8C9A0`, haze `#C9A57A`, sky `#F2D9B4`, shadows `#5A3E2B`) · **after** (brand-clean: sky `#0239FF`→`#5E7CFF`, cyan accents `#03FFF1`, white `#FFFFFF`, ground `#1F2A5A`). The owner's ochre shirt `#E39B2B` reads in both. Palette values are ours (Canon colour GAP); brand values from Stage 2.
- Player: a man in his 40s, ochre half-sleeve checked shirt, dark trousers, chappals, reading glasses pushed up on the head, a big key ring at the belt, a red cloth-bound rent register under the arm. **No cap, no moustache, no overalls, no gloves** (Stage 2 §2.5). Flat cel-shaded, thick dark outlines, side view.
- Obstacles (original creatures, each one silhouette): O1 blank-ID-card creature (white card body, dark featureless head silhouette, short legs) · O2 red flip-calendar creature with angry brows and stubby arms (no digits on it — the digit would be in-model text) · O3 sheet-ghost carrying a suitcase and a rolled mattress (not round, no tongue) · O4 rolling tangle-ball of receipts, ledger strips and bank slips (no legible marks) · O5 three winged old-style telephone handsets buzzing in a swarm.
- Cleared states: O1 → tenant card with a face and a green tick · O2 → calendar becomes a calm blue calendar with a tick · O3 → ghost outlined and pinned with a big visible price-tag (the dues made visible; it may still drift — knowledge, not recovery) · O4 → a neat stacked report with a tick · O5 → the handsets become three ticket cards with ticks.
- Power-up: the RentOk phone — a phone in the owner's raised hand, screen glowing brand blue with the app icon; a soft cyan shield glow around him (the immunity); the projectile is a cyan "OK" glyph beam (code-drawn type in the brand cyan). Not a firearm silhouette (D6/FL3).
- Flag: a plain pole with a blue flag carrying the wordmark; a pixel firework burst on capture.
- HUD: hearts (three, pixel style), `LEVEL 1`, score digits (decorative), the power-up slot.
- Finish: everything matte flat-shade; one implied light (upper-left), hard-edged cel shadows to the lower-right; the code pixelation pass (Stage 4) unifies all generated assets into one retro texture.

Pack check lines rendered by id against this blueprint:

| id | status | reason |
|---|---|---|
| PA-D1 | pass | one finish declared for every object: matte flat-shade; no glossy surface anywhere |
| PA-D2 | n-a | no glossy surface (the phone screen is a flat glowing plane, not a reflection) |
| PA-D3 | pass | hard-edged cel shadows with a small hard highlight — agree |
| PA-D4 | pass | one nameable source: sun upper-left; all shadows lower-right; checked on every plate |
| PA-D5 | pass | ochre figure vs blue/dusty ground survives grayscale (to be measured on the plate, QA B3) |
| PA-D6 | pass | key level declared: high-key, bright; mood from palette temperature, not brightness |
| PA-D7 | pass | hero F10: "the app verifies the tenant" — needs no copy |
| PA-D8 | n-a | no glass, dark-glossy or mirror object |
| PA-D9 | pass | side view is the platformer's only angle; the phone shows its front face (icon) — the most surfaces that read |
| PA-D10 | pass | no PA deviation |
| CA-D1 | pass | 1st the owner (colour + scale), 2nd the obstacle + its label, 3rd the HUD |
| CA-D2 | pass | subject in the left third of the action band because he runs right and obstacles enter from the right (a reason, not a ratio) |
| CA-D3 | pass | edge treatment: the world bleeds off all four edges; obstacles enter from off-frame; cards keep ≥ 65 px margin; no accidental tangency |
| CA-D4 | pass | cards and the cheat bar carry a thin dark border, thinner and darker than what they frame |
| CA-D5 | pass | declared deliberately restless F1–F7 (pressure from frame right), balanced F15–F17 |
| CA-D6 | pass | 9:16 justified by the tall PG facade filling the height with the street at its foot |
| CA-D7 | pass | per beat the new information and device are named in the board (side-scroll blocking; three cuts) |
| CA-D8 | pass | if a beat overruns, sacrifice rhythm (shorten the approach), never the label hold or the emotion of the hit |
| CA-D9 | pass | left→right throughout; the freeze and the end card change nothing |
| CA-D10 | pass | holds set by label read time (≥ 1.2 s); pace named: short-form fast-cut norm |
| CA-D11 | pass | the side-scroll is motivated by the run; stillness on the freeze, the install and the end card is chosen |

## 3.12 — Cuts and holds

Continuous side-scroll F1–F6 (one "shot"; new information per beat = a new obstacle); cut 1 at F7 (freeze — new information: the owner is out of hearts); cut 2 at F9 (world change — new information: the app is on; motivated by the install completing); the power run F10–F14 is again continuous; cut 3 at F17 (end card; motivated by the flag capture and the `LEVEL COMPLETE` banner). No dissolves (they carry a languid register, sk_gote_c003_0031) — a one-frame white flash on each hit and a fade to the end card.

---

## STORYBOARD (numbered; timecodes sum to 30.0 s)

| # | in–out (s) | dur | on screen | copy (exact strings from the deck) | sound | new information / device |
|---|---|---|---|---|---|---|
| F1 | 0.0–1.2 | 1.2 | Owner already running right on the PG street; HUD pops: ♥♥♥, level, greyed power-up slot; name tag above him | C01 `PG OWNER` · C02 `LEVEL 1` · C03 `RENTOK MODE: OFF` | music in hard on beat 1; run-step loop | a platform game with a PG owner; side-scroll |
| F2 | 1.2–3.2 | 2.0 | O1 blank-ID creature enters from the right with its label; owner jumps, clips it, hit-flash, knocked back | C04 `UNVERIFIED TENANT` | hurt blip | ♥♥♡ — obstacle 1 named |
| F3 | 3.2–5.2 | 2.0 | O2 red calendar creature charges, shoves him back; he keeps running | C05 `RENT NOT PAID` | thud | obstacle 2 |
| F4 | 5.2–7.2 | 2.0 | O3 ghost with suitcase drifts through him; hit-flash | C06 `LEFT WITHOUT PAYING` | hurt blip | ♥♡♡ — obstacle 3 |
| F5 | 7.2–9.2 | 2.0 | O4 paper-tangle ball rolls at him; he ducks, slips on strips | C07 `ACCOUNTS MESS` | rustle-thud | obstacle 4 |
| F6 | 9.2–11.2 | 2.0 | O5 three phone-creatures swarm; he is pushed against the level's wall | C08 `COMPLAINT CALLS` | ring-buzz | obstacle 5; cornered |
| F7 | 11.2–12.6 | 1.4 | Freeze; colour drains; hearts blink; dark plate | C09 `CONTINUE?` | music drops out; heartbeat blip | stillness: out of hearts |
| F8 | 12.6–14.4 | 1.8 | Cheat bar types the code letter by letter; slot pulses | C10 `CHEAT CODE: INSTALL RENTOK` | key blips; V1 | the cheat code = install RentOk |
| F9 | 14.4–16.0 | 1.6 | Phone rises into his hand; icon fills; slot lights; hearts refill ♥♥♥; palette flips dusty → brand-clean; cyan shield glow | C11 `INSTALLING...` → C12 `RENTOK MODE: ON` | power-up chime; music returns brighter; V2 | the enhanced ability (M5) |
| **F10** | 16.0–17.8 | 1.8 | **HERO.** Runs right, phone raised, cyan OK beam hits O1 → tenant card with face + tick | C13 `TENANT: VERIFIED` | beam + stamp | clear 1 (product in use) |
| F11 | 17.8–19.6 | 1.8 | Beam hits O2 → calm blue calendar with tick | C14 `AUTOPAY: ON` | beam + stamp | clear 2 |
| F12 | 19.6–21.4 | 1.8 | Beam hits O3 → ghost outlined and pinned with a visible price-tag; it drifts on, tagged | C15 `DUES VISIBLE` | beam + stamp | clear 3 (knowledge, not recovery) |
| F13 | 21.4–23.2 | 1.8 | Beam hits O4 → tangle snaps into a stacked report with tick | C16 `REPORTS: DONE` | beam + stamp | clear 4 |
| F14 | 23.2–25.0 | 1.8 | Beam hits O5 → three ticket cards with ticks | C17 `TICKETS RESOLVED` | beam + stamp ×3 | clear 5 |
| F15 | 25.0–26.6 | 1.6 | Flagpole; he leaps, grabs the blue RentOk flag, slides it down; pixel fireworks | — (the wordmark on the flag is the image asset) | flag zip; fanfare | the flag (M6) |
| F16 | 26.6–27.8 | 1.2 | Banner over the scene; score ticks up; hearts full | C18 `LEVEL COMPLETE` | fanfare tail; V3 begins | level complete |
| F17 | 27.8–30.0 | 2.2 | End card: brand-blue panel; closing line; wordmark; CTA button | C19 `PG OWNER? LEVEL UP.` · C21 wordmark · C20 `Get the app` | V3 ends by 29.2; music resolves; silence 29.8–30.0 | the product and the ask |

Sum: 1.2+2.0+2.0+2.0+2.0+2.0+1.4+1.8+1.6+1.8+1.8+1.8+1.8+1.8+1.6+1.2+2.2 = **30.0 s**.

Muted test: with the sound off the sequence still reads game → five named obstacles → out of hearts → cheat code text → phone/app → five clears with cards → flag → `LEVEL COMPLETE` → wordmark + `Get the app`. Every mandatory event is visual. **Pass (by design; the checker confirms on the assembly).**

## COPY DECK (exact strings; all Latin; overlay; code-set; `may_reflow` false unless stated)

| id | string | role | frame | size (cap px) | may_reflow | claim basis |
|---|---|---|---|---|---|---|
| C01 | `PG OWNER` | player tag | F1–F16 | 44 | no | customer words |
| C02 | `LEVEL 1` | HUD | F1–F16 | 44 | no | — |
| C03 | `RENTOK MODE: OFF` | HUD slot | F1–F8 | 40 | no | brand name (Stage 2 D1) |
| C04 | `UNVERIFIED TENANT` | obstacle label | F2 | 60 | yes (2 lines) | problem, customer words |
| C05 | `RENT NOT PAID` | obstacle label | F3 | 60 | yes | problem |
| C06 | `LEFT WITHOUT PAYING` | obstacle label | F4 | 60 | yes | problem, customer words |
| C07 | `ACCOUNTS MESS` | obstacle label | F5 | 60 | yes | problem ("no place to do reconciliation") |
| C08 | `COMPLAINT CALLS` | obstacle label | F6 | 60 | yes | problem; cm L15 "Complaints on calls, WhatsApp" |
| C09 | `CONTINUE?` | freeze | F7 | 84 | no | game convention |
| C10 | `CHEAT CODE: INSTALL RENTOK` | cheat bar (may break after the colon) | F8 | 72 | yes (2 lines at the colon) | customer words (PC7) |
| C11 | `INSTALLING...` | phone screen | F9 | 48 | no | — |
| C12 | `RENTOK MODE: ON` | HUD slot | F9–F16 | 40 | no | brand |
| C13 | `TENANT: VERIFIED` | card | F10 | 72 | no | PC1d (tv L66–70) |
| C14 | `AUTOPAY: ON` | card | F11 | 72 | no | PC2a (home L19–20; autopay L4–5) |
| C15 | `DUES VISIBLE` | card | F12 | 72 | no | PC3a (autopay L117, L136; home L92) |
| C16 | `REPORTS: DONE` | card | F13 | 72 | no | PC4a (home L90) |
| C17 | `TICKETS RESOLVED` | card | F14 | 72 | no | PC5a+PC5c (cm L61, L75–76, L83; L24 "Complaints Resolved") |
| C18 | `LEVEL COMPLETE` | banner | F16 | 96 | no | game convention |
| C19 | `PG OWNER? LEVEL UP.` | closing line | F17 | 84 | no | names the audience; game idiom tied to the story |
| C20 | `Get the app` | CTA | F17 | 64 | no | PC6a (home L140) |
| C21 | wordmark image (`RentOk` + "India's renting superapp") | mark | F15 flag, F17 | image | — | S-LOGO |
| C22 | score digits (e.g. `000120`) | HUD, decorative | F1–F16 | 40 | — | not a claim; excluded from the exact-copy check |

Forbidden-list scan (Stage 2) over C01–C20: no `guarantee`, `never`, `always`, `100%`, `%`, `no more`, `prevent`, `recover`, `claim`, `insur`, `Eqaro`, `Mario`, `Nintendo`, tool names — **clean** (to be re-run by code at Stage 5, `scan_copy_deck.py`).

Phone-size readability: at 1080 px wide on a ~65 mm-wide phone screen, 60 px cap height ≈ 3.6 mm, 40 px ≈ 2.4 mm (HUD, secondary), 72–96 px ≈ 4.3–5.8 mm. The longest label `LEFT WITHOUT PAYING` wraps to two lines within 950 px. Contrast is measured on the rendered pixels by the compositor gate (≥ 4.5:1 or an opaque plate is added). Every label is a shape + colour + text, never colour alone.

---

## CHANGES-FROM-SUPPLIED-DIRECTION (ChatGPT direction, element by element)

| # | Supplied element | Verdict | Reason (customer words / verified facts / Canon / constraints) |
|---|---|---|---|
| 1 | Working title "PG OWNER — LEVEL UP!" and on-screen title "PG OWNER — LEVEL 01" | CHANGE | "PG OWNER" is kept as the player tag (names the audience, sk_ogx_0007); the exclamation mark is dropped (sk_whip_0033); "LEVEL 01" becomes `LEVEL 1` in the HUD; there is no title card (see 4) |
| 2 | Character "identifiable through a key ring and simple property-manager styling" | KEEP + IMPROVE | keys kept; added a rent register, reading glasses on the head, an ochre checked shirt for colour identification (sk_ms_c003_0016) and everyday Indian dress (sk_dpci_0070); explicit no-cap/no-moustache/no-overalls rule (A9) |
| 3 | Obstacle list (unverified document, overdue rent, unpaid exit, reconciliation monster, complaint) | KEEP mapping, CHANGE designs | the five map one-to-one onto the customer's five; designs replaced by five original creatures with distinct silhouettes and code-set labels (in-model text is out; RR-1) |
| 4 | 00:00–00:03 "A retro-platformer start screen appears … start-game chime" | DROP | the first frame is the gate (sk_ogx_0040); open mid-action (sk_abcd_0007); 3 s of start screen is 10 % of the film with no story |
| 5 | Three hearts; loses health; "cornered with one heart remaining"; "The game freezes" | KEEP | the stakes are dosed (sk_sb_c003_0012) and legible with sound off; hearts are generic HUD, not Nintendo |
| 6 | "CHEAT CODE UNLOCKED: INSTALL RentOK" | CHANGE | shortened to `CHEAT CODE: INSTALL RENTOK` — fits one bar at 72 px in the safe box; caps resolves the RentOK/RentOk casing (Stage 2 D1); "UNLOCKED" is redundant with the typing animation |
| 7 | "RentOK Control Blaster" | CHANGE | the power-up is the RentOk phone itself firing an OK beam, with a shield glow for the immunity half. Reasons: the product in use (sk_ogx_0041); the brand becomes load-bearing (sk_ctg_0053); "Blaster" reads as a generic gun and a realistic firearm is avoided (Stage 1 D6/FL3); the customer's "gun sort of power/immunity" mechanic is preserved (projectile + immunity) |
| 8 | Transformation list (verification record, reminder/tracked due, visible dues, organised report, service ticket) | KEEP, wording CHANGED to cited strings | all five verified at Stage 2; strings replaced by the permitted-claims list (C13–C17); for the unpaid-exit obstacle the depiction stops at "dues visible / tagged" so nothing implies recovery or prevention (M11) |
| 9 | Timings 0–3 / 3–9 / 9–13 / 13–17 / 17–25 / 25–30 | CHANGE | start screen removed; every obstacle gets a 2.0-s introduction (five, not 3+2) so A3 can be checked on the first pass; install compressed to 3.4 s (F8–F9) — enough for the typing and the phone, not a demo; power run 9.0 s for five clears at 1.8 s each (label read time ≥ 1.2 s, sk_gote_c003_0053); flag + banner 2.8 s; end card 2.2 s |
| 10 | "LEVEL COMPLETE!" | CHANGE | `LEVEL COMPLETE` — no exclamation mark (sk_whip_0033) |
| 11 | Closing "PG MANAGEMENT? LEVEL UP WITH RentOK." | CHANGE | `PG OWNER? LEVEL UP.` + `Get the app` + wordmark: names the reader rather than the category (sk_ogx_0007), keeps the game idiom that the story earned, adds the site's own CTA (PC6a) and the package close (sk_ogx_0039); "with RentOK" is carried by the wordmark |
| 12 | "Arcade music" / "start-game chime" | KEEP music, DROP the chime | original chiptune bed (Lyria first, code fallback — no Nintendo melody); no start chime because there is no start screen; SFX synthesised by code |
| 13 | "An in-game smartphone appears … installed and activated … health counter is restored … world transitions from chaotic to controlled" | KEEP | all four are the turning point's visible evidence (M4/M5) and the muted test depends on them |
| 14 | "The character should physically interact with the game obstacles, rather than merely running past labels that disappear automatically" | KEEP | adopted as a hard rule of the animation: contact (hit/knock-back) in F2–F6, beam contact + transformation in F10–F14 |
| 15 | "Assess whether the gameplay is intelligible within a vertical 9:16 frame" | KEEP as a requirement, RESOLVED | action band inside the Meta safe box; character ≈ 1/7 frame height; one obstacle on screen at a time; labels ≥ 60 px; end card inside the box |
| 16 | "may combine original AI-generated visual assets with deterministic animation" | NOT ADOPTED HERE | the production method is decided at Stage 4 on the plan's requirements (identity over 30 s, exact text, contact, timing, budget), not because it was suggested |
| 17 | "original 2D or 2.5D platform-game aesthetic" | KEEP 2-D, DROP 2.5-D | 2-D flat cel-shade + a code pixelation pass unifies assets from separate draws; 2.5-D would expose per-asset lighting mismatches (PA-D4) |
| 18 | Added elements not in the direction | ADD | the greyed HUD slot `RENTOK MODE: OFF` from 0.0 s (brand-early, sk_abcd_0011, and the set-up for the turning point); the arcade announcer (three lines = on-screen twins; audio brand mention, sk_abcd_0012/0021); `CONTINUE?` on the freeze (a game convention that makes the cheat code the answer to a question) |

Nothing was rejected for being supplied; nothing was kept for being supplied.

---

## Audio direction (Canon gap — evidence and reasoning only)

- Music: one original chiptune-style bed, upbeat, ~140 bpm, no vocals, 30 s (Lyria route MUS/lyria+native, clean 4/4, USD 0.06; tracks run ~32.8 s, trimmed by code, RR-13). Prompt wording neutral (RO-09: Lyria refused advertising-flavoured wording once). Chiptune quality on Lyria is untested (n=0): if the draw does not read as arcade, the fallback is a code-synthesised square-wave loop (USD 0, deterministic, unarguably original). Music drops out on the freeze (F7) and returns brighter at F9 (a second Lyria draw is NOT planned; the "brighter" return is a code-side filter/level change on the same track).
- SFX: all synthesised by code (numpy): step loop, hurt blip, thud, ring-buzz, key blips, power-up chime, beam, stamp, flag zip, fanfare. No sampled or Nintendo sounds.
- Voice: three announcer lines (3.8), one source (3.10 audition).
- Mix: music −16 LUFS under voice, ducked −6 dB during V1–V3; SFX peaks below voice; master integrated −14 LUFS ±1, TP ≤ −1 dBTP (Stage 2 §2.6).

---

## Stage 3 exit criteria — self-assessment (the checker issues the verdict)

| Criterion | Self-assessment | Evidence |
|---|---|---|
| A board exists with numbered frames and timecodes summing to 30.0 s | met | F1–F17, sum shown |
| Numbered hero frame, not a claim | met | F10 with the PA-D7 line |
| Every mandatory event on a numbered frame | met | 3.7 table |
| Copy deck with exact strings; forbidden scan clean | met | C01–C22; scan result recorded, to be re-run by code |
| Canon retrieved by id with claim text, gaps named | met | 3.0b; evidence files |
| ChatGPT direction interrogated element by element with reasons | met | 18-row table |
| On-screen = spoken | met | 3.8 |
| Voice audition format | met | 3.10 (executed at Stage 5) |
| Pack check lines rendered by id | met | 21 lines in 3.11 |
| 3.13 non-author checker | not mine to answer | reserved for the checker session |
