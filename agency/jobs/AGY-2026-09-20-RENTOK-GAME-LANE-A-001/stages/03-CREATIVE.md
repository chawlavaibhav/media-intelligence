# Stage 3 — Creative (gate: a board exists; a non-author answers the structure checklist against it)

Job `AGY-2026-09-20-RENTOK-GAME-LANE-A-001`. Template lines 3.1–3.13. Companion files written by this stage: `copy-deck.json` (every exact string), `board.json` (numbered frames with timecodes), `stages/evidence/canon-lookup.txt`, `stages/evidence/typo-audition-9x16.png`, `tools/pixfont.py`.

---

## Part A — Canon, interrogated honestly

### A1. Deterministic pack lookup (USD 0, `stages/evidence/canon-lookup.txt`)

Input `brief.job.json` (PRODUCTION-JOB-v1; kind `multi_shot_story` = nearest registered kind, ambiguity recorded). Output:

- `packs_selected` (10): concept_and_distinctiveness, critique_and_effectiveness, composition_and_attention, colour_and_visual_register, camera_and_spatial_grammar, editing_pacing_and_short_form, typography_and_copy, product_appearance, indian_indic_context, commercial_communication.
- `packs_injected` (2, compiled + accepted): **composition_and_attention**, **product_appearance**. Prefix sha256 `4d7a5b27e17c5ff3b0561521b0b1b540b995562bb0dc94b6f188a5ebcec1c8fe`, 5,298 tokens, 21 check ids.
- `missing_domains` (8): the other eight — recorded, never invented. Both compiled packs carry `status: PROPOSED — … CONTROL-STATE.md governs`.

### A2. Accepted claims retrieved by id from `canon/knowledge/current/**` (claim text quoted; nothing listed here was not read)

| Domain | Retrieved | Claim text used (abridged only by cutting sentences, never reworded) | Used for |
|---|---|---|---|
| Advertising structure — opening | `sk_abcd_0006` (google-abcd) | "asks the ad to reach the heart of its story sooner … pacing that keeps the viewer engaged, and tight framing" | F1 opens mid-run, no title card |
| | `sk_abcd_0007` | "beginning in the middle of the action, and opening on a close-up … not as a required opening" | F1 |
| Advertising structure — brand | `sk_abcd_0010` | "when the brand first appears (early), how often it recurs (often), and how many different kinds of branding element carry it (richly)" | brand timeline: HUD chip, typed name, phone item, end card |
| | `sk_abcd_0011` | "introduced from the start of the ad and its presence maintained across the ad's whole length … an early appearance that then lapses does not satisfy it" | wordmark chip persistent 0–27.6 s |
| | `sk_abcd_0013` | "product shots, pack shots, in-situ branding, graphic elements, voice-overs and musical treatments — … worked into the story through a variety of them" | the app is a game item (in-situ), the HUD chip (graphic), the end card |
| | `sk_ogx_0039` (ogilvy-beyond) | "Use the name within the first ten seconds." · "Commercials which end by showing the package are more effective in changing brand preference" | chip at 0 s; end card = the "package" (wordmark + app) |
| Advertising structure — ask | `sk_abcd_0019` | "ask the viewer to act … a written call to action, graphics, audio, or a scene from the story itself" | the cheat code IS the ask, inside the story (F7); repeated as the end-card CTA |
| | `sk_abcd_0020` | "chosen intentionally against a specific marketing objective … state plainly what the advertiser wants the viewer to do" | CTA = "INSTALL / RENTOK APP", the customer's own action |
| | `sk_abcd_0026` | "Use CTAs throughout your ad, and be more direct as you go" | F7 (in-story) → F11 (direct card) |
| | `qa_abcd_0011` (Q&A bank, ungraded) | action objective: "Present the ask after the context is set" | the ask lands at 15 s after the five problems, not in the hook |
| Advertising structure — audio | `sk_abcd_0012`, `sk_abcd_0021` | "an audio mention of the brand raises the performance of the on-screen brand visual" · "on-screen call to action is to be paired with a voice-over saying the same thing" | **deviation** recorded at 3.10: no voice-over (reason and cost there) |
| Narrative progression | `sk_whip_0011` (sullivan) | "a brand story requires an opposing force … a brief phrased as a solution gives the maker nothing to respond to" | the first half is the five problems, unsoftened; the solution enters only at F7 |
| | `sk_sb_c003_0008` (storybrand) · `sk_whip_0015` | "THE CUSTOMER IS THE HERO, NOT YOUR BRAND" · "the brand is the archetype the hero meets — the figure who … grants a power before the hero returns transformed" | the PG owner is the player; RentOk is the power granted, never the character |
| | `sk_sb_c003_0014` | "What does the hero want? Who or what is opposing the hero …? What will the hero's life look like if she does (or does not) get what she wants?" | answerable at any frame: wants the flag; opposed by the five problems; GAME OVER? vs LEVEL CLEAR! |
| | `sk_hea_mts_0018` | "hearing stories acts as a kind of mental flight simulator" | the clearing run rehearses "problem → app → cleared" five times |
| | `sk_hea_mts_0009` | "To strip an idea down to its core, we must be masters of exclusion" | one mechanic, one power, no second idea |
| | `sk_whip_0005` | "the overlap of clear and clever … 'I don't get it' (too weird) and 'I've seen that before' (too obvious)" | test applied to the proposition (Part B) |
| Hierarchy / attention | `sk_ms_c003_0019` (kenworthy) | "repeatedly shifting focus … doesn't guide attention so much as confuse" | one moving cue per beat (CA-D1) |
| | `sk_hop_sa_0026` (hopkins) | "A picture in an advertisement must be a salesman in itself and earn the space it occupies" | the hero-frame line (3.2) |
| | `sk_hop_sa_0014` | "Think of a typical individual … who is likely to want what you sell" | the owner is a specific person (Part B) |
| Editing / pacing | `sk_gote_c003_0004` (grammar of the edit) | "A new shot should always present some new information to the viewer." | each beat introduces one new obstacle or state |
| | `sk_gote_c003_0006` | "There should always be a motivation for making a transition away from a shot." | the only cut (F10→F11) is motivated by the flag reached |
| | `sk_murch_c003_0013` (murch) | "when and in what order to release those various pieces of information" | order: problems → code → power → clearing → flag → brand |
| | `sk_murch_c003_0019/0020` | six ranked criteria; "Emotion … preserve at all costs" | the GAME OVER? low point is held 0.8 s before the panel |
| Shot design / motion | `sk_gos_c003_0007`, `sk_gote_c003_0017` | "screen direction … must be maintained from one shot to the next" | everything travels left→right; the fleeing tenant too |
| Typography / readability | `sk_wcag_0001`, `sk_wcag_0002` | "contrast ratio of at least 4.5:1" · large-scale text "need only reach 3:1" | contrast gate thresholds (labels ≥ 4.5:1 measured over real pixels) |
| | `sk_sam_c003_0021` (samara) | "Text … can be set on top of an image (so long as there's enough contrast between their relative values …)" | labels get a dark backing band where the measured ratio fails |
| Brand mark | `sk_vig_c003_0013` (vignelli) | "A real Corporate Identity is based on an overall system approach, not just a logo" · a logo "should not be discarded for a new one" | the wordmark is placed as-is, never redrawn |
| Product as hero | `sk_ogl_c003_0014` (ogilvy) | "Whenever you can, make the product itself the hero of your advertising." | tension with `sk_sb_c003_0008`; resolved: the product is the power-up (the hero's instrument), and the "package" closes the film |

GAPs (honest): **no accepted Canon on** game/arcade grammar, pixel-art readability, or chiptune sound (alternative source: explicit reasoning below + the USD-0 typography audition); **typography_and_copy**, **editing_pacing_and_short_form**, **colour_and_visual_register**, **camera_and_spatial_grammar**, **commercial_communication**, **indian_indic_context** packs are uncompiled — the claims above are individual accepted sources retrieved by id, not a pack; **audio** has zero accepted Canon (trigger table coverage_gap_notice) — audio decisions are the producer's, attributed to nobody.

### A3. The 21 compiled check lines rendered against the blueprint (`blueprint.check_lines`)

| id | Verdict | Basis |
|---|---|---|
| PA-D1 | pass | every sprite declared **matte/flat pixel art**, no specular anywhere; the phone screen is the one "glossy" object and is declared flat too (a flat cyan rectangle) |
| PA-D2 | n-a | no glossy surface |
| PA-D3 | pass | hard source implied (crisp 1-px pixel shadows on sprites; no soft shadow anywhere) — consistent |
| PA-D4 | pass | one fictional source: daylight from upper-left; every generated sprite prompt states it; code drop-shadows fall lower-right |
| PA-D5 | pass | every sprite carries a 2-px dark outline; grayscale separation checked by code on each cut-out (B3) |
| PA-D6 | pass | key level declared bright daytime, constant until F6 (desaturate) and F11 (brand blue) — both changes are story events |
| PA-D7 | pass | hero frame F9.2 sells "the owner, powered by the app, blasts the rent problem" with no copy (3.2) |
| PA-D8 | n-a | no glass/dark/mirror object |
| PA-D9 | n-a | no 3-D product; the wordmark is shown face-on |
| PA-D10 | pass | deviations listed in Part C (D-1 no VO; D-2 raster wordmark not code-typed) |
| CA-D1 | pass | per beat: 1st read = the moving sprite entering from the right; 2nd = its label; 3rd = the HUD change — one cue each, no competing motion |
| CA-D2 | pass | the owner sits in the left third of the play window because he runs right and needs room ahead (a reason, not a ratio) |
| CA-D3 | pass | edge treatment "cut by the frame": obstacles enter/exit through the right edge; the owner never touches an edge; labels centred with ≥ 65 px clearance |
| CA-D4 | pass | the cheat-code panel is darker than the sprites it frames (F7) |
| CA-D5 | pass | deliberately restless during the run (weight arriving from the right); balanced at F11 (centred stack) |
| CA-D6 | pass | 9:16 justified by a named vertical shape in the scene — the PG building facade with stacked floors behind the level, and the HUD / checklist / play band / ground stack — not by the platform alone |
| CA-D7 | pass | per beat the device is **blocking** (a sprite enters); the one cut is at the flag with new information (the brand card) |
| CA-D8 | pass | with one cut nothing is sacrificed; if the flag beat runs long, planarity is given up first, never emotion |
| CA-D9 | pass | screen direction left→right throughout; the end card is a new scene, not a continuation |
| CA-D10 | pass | holds 1.2–3.0 s, each ending when its label has been readable ≥ 1.0 s and its action resolved; the prevailing norm assumed is arcade tempo (stated, not Canon) |
| CA-D11 | pass | the only camera move is the side-scroll follow at the player's run speed; it stops when the game "pauses" (F7) — both motivated |

---

## Part B — The creative package

### 3.1 Proposition (one sentence)

**Running a PG is a platform game where every level is the same five problems — and installing the RentOk app is the cheat code that turns the owner into the one who clears them.**

Clear-and-clever test (`sk_whip_0005`): clear — the five problems are named in the customer's words; clever — the cheat code is the install. Not "seen before" in this category (the site's own register is dashboards and numbers); not "don't get it" (a 30-year-old convention everyone under 50 reads instantly).

### Player identity — how a PG owner is recognisable inside a game

Cues, in order of strength at phone size: (1) the HUD name **PG OWNER** from frame 1 (code, 42 px caps); (2) props on the sprite readable at ≈ 220 px height — a **bunch of keys on a ring at the belt** and a **rent register / ledger book** under the arm; (3) costume — a checked half-sleeve shirt, dark trousers, rectangular spectacles, chappals; an adult Indian man of ~40, slightly stocky, ordinary (a specific person, `sk_hop_sa_0014`); (4) context — the level runs along a PG building facade with stacked floors, water tanks and a lane. None of the four is a Nintendo cue (Stage 2c).

### World / level design (vertical-native, F4 from Stage 1)

- Canvas 1080×1920; critical box (65,288)–(888,1248). Full-bleed background: sky gradient (top), a tall **PG building facade** with stacked floors and small windows filling the upper third (the named vertical shape, CA-D6), rooftops/water tanks in the middle distance, a lane in front. Ground line at y = 1130 (inside the box); ground tiles plain ochre brick.
- Parallax: background plate scrolls at 0.25× the ground speed; foreground props at 1×. Scroll speed 320 px/s (problem half), 480 px/s (clearing run).
- HUD row at y ≈ 300–345: left `PG OWNER ▮▮▮▮▮` (scale 6); right: the wordmark chip 150 × 77 px (raster) at x 738–888.
- Checklist column (F9 onward) at x = 90, y = 400 → 640: five rows of green chips on a dark backing.
- Labels: obstacle labels centred at y ≈ 720 (yellow #FFF100, scale 7, dark backing band); state flashes (`GAME OVER?`, `POWER UP!`, `LEVEL CLEAR!`) centred at y ≈ 560.
- Palette: sky #6FB7FF→#CFEBFF, facade cream #F1E3C6 with terracotta #C8683F, ground ochre #B98A3E/#8C6428, outline #1E1E28; brand blue #0038FF, cyan #03FFF1, yellow #FFF100, green #30B502 reserved for the app/power/labels/chips so the brand colours mean "the solution".

### The five obstacle representations (each mapped to a verified capability for its clearing chip)

| # | Customer problem | Obstacle sprite (what the picture says before the label) | Label (copy deck) | Cleared → chip (Stage 2 permitted claim) |
|---|---|---|---|---|
| 1 | tenant verification | a wall of paper documents with a faceless silhouette peeking out and a big question mark above it | `TENANT VERIFICATION` | `✓ DIGITAL KYC` (home.txt:99) |
| 2 | collecting rent | a heavy cloth money sack with a padlock and chain, hopping away from the owner | `COLLECTING RENT` | `✓ AUTOPAY` (home.txt:19–20; autopay.txt:4–5) |
| 3 | tenants leaving without paying | a tenant sprite with a suitcase and a coin bag sprinting ahead and out of frame right | `LEFT WITHOUT PAYING` | `✓ DUES TRACKED LIVE` (autopay.txt:104–107, 136; home.txt:104) |
| 4 | no place to do reconciliation | a toppling tower of ledgers, loose sheets and a calculator | `NO RECONCILIATION` | `✓ ONE DASHBOARD` (autopay.txt:95) |
| 5 | solving complaints | a swarm of angry red speech-bubble tickets with exclamation marks | `COMPLAINTS` | `✓ COMPLAINT TICKETS` (complaint-management.txt:10) |

### Gameplay mechanics

Side-scroll runner. Problem half: the owner runs and jumps (jump arc 0.5 s, code); each obstacle either blocks (1, 4), hits (2, 5) or escapes (3); each contact costs one health segment (5 → 0) with a white hit-flash and a knock-back of 60 px. Clearing half: the owner runs faster, is immune (contact does nothing — the immunity the customer asked for), and fires cyan tick projectiles (one per 0.4 s, 26 px, 900 px/s) that burst each obstacle into pixel debris; the burst spawns the green chip which flies to the checklist. Flag: a jump at the pole, the flag rises 0.8 s.

### The install-RentOk turning point (F7, 15.0–18.0 s — the middle of the film)

At health 0 the world desaturates and `GAME OVER?` flashes (0.8 s). A dark arcade panel with a cyan border slides up inside the box: header `CHEAT CODE:`, then the two lines type in letter by letter with key-click SFX (1.4 s): `INSTALL` / `RENTOK APP`. On the last letter a RentOk-blue phone item drops into the owner's hand (0.4 s), the screen shows the wordmark, a white flash, colour returns, health refills to five in cyan. The panel slides away. This is the one moment the game "stops", which is what makes it the turning point (M4).

### The power-up (customer's "gun sort of power/immunity", preserved)

Form: the phone. Effect: (a) a pulsing cyan aura (code: 2-px outline + 40 % alpha halo) — the visible change (M5); (b) **projectile** — cyan tick marks fired forward, the "gun sort of" mechanic without a firearm (Stage 1 F3); (c) **immunity** — health no longer drops; contact with an obstacle now bursts the obstacle instead of the owner. Rendered by code from the base sprite (palette shift + aura), so the character cannot drift between "before" and "after".

### The flag / victory (F10)

A tall grey pole at the end of the level; the flag is RentOk blue with a cyan tick. The owner jumps, grabs the pole, the flag rises to the top; `LEVEL CLEAR!` flashes; pixel confetti in brand colours. No castle, no jingle from any existing game.

### Branding timeline (3.4)

| t (s) | Brand element | Kind (`sk_abcd_0013`) |
|---|---|---|
| 0.0–27.6 | wordmark chip in the HUD, top-right, 150 × 77 px | graphic element, persistent (`sk_abcd_0011`); the name is on screen inside 10 s (`sk_ogx_0039`) |
| 15.8–17.4 | `RENTOK APP` typed in the cheat panel (70 px caps) | in-story, the ask itself |
| 17.4– | the phone item with the wordmark on its screen; from 18.0 a phone icon beside the health bar | in-situ product |
| 19.6–25.6 | five green chips naming app capabilities | product proof |
| 27.6–30.0 | end card: wordmark large (≈ 700 px wide) + CTA + URL on brand blue | the "package" close (`sk_ogx_0039`) |

### Closing CTA copy (3.5, 3.6)

Surface: card, code-set. Lines: `INSTALL` / `RENTOK APP` (white, 70 px caps) then `RENTOK.COM` (49 px). The same words as the cheat code — the ask is made twice, more directly the second time (`sk_abcd_0026`). No spoken line exists, so 3.8 (on-screen = spoken) is satisfied trivially and recorded as such. Last frame (3.6): the end card held still for its final 1.0 s — wordmark, CTA, URL, nothing moving.

### Audio direction (2.6, 3.10)

- Music: one original instrumental bed, chiptune character, ≈ 140 bpm, bright, 30 s (Lyria; trimmed from ≈ 32.8 s by code, RR-13). Prompt wording neutral (RO-09 risk). No melody from any existing game (Stage 2c).
- SFX (code-synthesised, ffmpeg): jump blip; hit (short noise burst + pitch drop); key-click ×18 for the typing; power-up (rising 4-note arpeggio, original); projectile "pew"; burst; flag fanfare (original 5-note motif in a major key, written for this job); end-card soft hit.
- Voice: **none**. Reasons: (1) the film must work muted (Stage 2.6) and every word is on screen; (2) no clean single-voice route with Indian English at this length exists in this project's evidence — Sarvam long narration was rejected by ear (case 001 RO-05, SD-05), Omni's voice judged synthetic (RO-03), native per-clip voices vary (case 002 RO-02); (3) a VO would add the audio-schedule and continuity checks (5.4, D14) for little gain on a 30-s arcade piece. Cost of being wrong (`sk_abcd_0012/0021` say audio brand mention helps): weaker brand recall for sound-on viewers; mitigation: the name is on screen from 0 s, typed at 15.8 s, and closes the film; a VO line can be added later at ≈ USD 0.01–0.02 without re-rendering picture. The 3.10 audition (≥ 2 candidates on the longest line) is therefore **n-a for voice** and was applied instead to **typography**: the longest label and the CTA were rendered at final scale inside the safe box (`stages/evidence/typo-audition-9x16.png`; result: labels at scale 7 = 791 × 49 px fit the 823-px box; the cheat code and CTA go on two lines at scale 10; scale 8 single-line labels overflowed and were rejected).
- Loudness: −14 LUFS integrated, TP ≤ −1 dBTP (recorded default).

### Visual system / typography (3.11, 3.9)

- Every exact string: `tools/pixfont.py`, an original 5×7 bitmap capitals font written for this job (no download, no licence, byte-exact by construction; glyph coverage of the whole deck verified: none missing). Scales: HUD 6 (42 px caps), obstacle labels 7 (49 px), state flashes 8 (56 px), cheat code and CTA 10 (70 px), chips 6 (42 px), URL 7.
- Readability at phone size for every label (3.9): all strings sit inside (65,288)–(888,1248); widest string `TENANT VERIFICATION` / `LEFT WITHOUT PAYING` = 791 px at scale 7 (audition, fits); minimum cap height 42 px ≈ 2.7 mm on a 70-mm-wide phone display — above ordinary phone UI caption size. Labels are yellow on a dark backing band (measured contrast ≥ 4.5:1, `sk_wcag_0001`); chips green on dark backing; cheat code cyan on the dark panel; CTA white on brand blue (measured, C2). Copy zones per frame (3.9): labels at y ≈ 720 are above the play band (owner and obstacles occupy y 900–1130) — text never sits on the character, the obstacles or the phone; the HUD row is above the label zone; the checklist column is left of the owner's lane and only appears while he is at x ≥ 300.
- Wordmark: the raster from `source/rentok-brand/` placed by code; minimum size 150 px wide (chip) — at that size the baked-in tagline is ≈ 6 px tall and unreadable; it is treated as part of the mark's texture, not as copy (a deviation recorded in Part C; if the checker judges it as garbled lettering, the chip is replaced by a code-typed `RentOk` in the two brand colours).

### 3.12 Cuts and holds

One cut (F10 → F11). Every other transition is blocking within the continuous scroll. Holds are set by content: 2.8 s per obstacle in the first half (enter 0.6 s, contact 0.4 s, label readable ≥ 1.2 s, exit 0.6 s); 2.4 s for obstacles 4–5 (the tempo tightens toward the low point); 1.2 s per obstacle in the clearing run (the labels are already known; the chip persists, so nothing is lost to speed); 3.0 s for the turning point (the longest hold in the film — the event that matters most gets the most time); 2.4 s end card.

### The muted test

Yes. Every beat carries its meaning in picture plus an on-screen label; the sound adds feel only.

---

## Part C — Deviations from pack defaults (PA-D10) and recorded assumptions

| id | Deviation / assumption | Forcing clause or reason | Cost if wrong |
|---|---|---|---|
| D-1 | No voice-over despite `sk_abcd_0012/0021` | Stage 2.6 muted-first; no clean single-voice route in evidence (cases 001/002) | weaker sound-on recall; add a line later ≈ USD 0.02 |
| D-2 | Wordmark used as a raster (its tiny tagline unreadable at chip size) rather than code-typed | brand fidelity (`sk_vig_c003_0013`); the brand's own file from the customer's named source | checker flags the chip as garbled → swap to the code-typed two-colour `RentOk`, USD 0 |
| D-3 | Product-as-hero (`sk_ogl_c003_0014`) subordinated to customer-as-hero (`sk_sb_c003_0008`) | the customer's own casting: "The player is basically a PG owner" | none — customer-mandated |
| D-4 | `GAME OVER?` shown with a question mark, never a full "GAME OVER" | the film must not say the owner's business fails; the question keeps it a game beat | none |
| D-5 | Numbers excluded from all copy though the site prints them | Stage 2.4 rule (A11) | none |

---

## Part D — NUMBERED STORYBOARD (30.0 s, 30 fps; timecodes from `board.json`; the copy deck strings are byte-exact)

| Frame | t0–t1 (s) | On screen (picture) | Copy on frame (exact) | Sound | Mandatory |
|---|---|---|---|---|---|
| **F1** | 0.00–1.80 | Cold open mid-action: the level is already scrolling; the PG owner (keys at the belt, register under the arm) runs right and jumps a gap between two rooftop blocks; HUD live; wordmark chip top-right | `PG OWNER` `▮▮▮▮▮` · `LEVEL 1` (centre flash 0.0–1.2 s) | bed starts on a downbeat; jump blip at 0.9 s | M1, M2 |
| **F2** | 1.80–4.60 | Obstacle 1 enters from the right: a wall of paper documents with a faceless silhouette and a big `?` above; the owner runs into it, bounces back, white hit-flash | `TENANT VERIFICATION` (label above the wall, 2.2–4.6 s); health → `▮▮▮▮▯` | hit | M3 |
| **F3** | 4.60–7.40 | Obstacle 2: a padlocked money sack hops toward him; he jumps, clips it, knock-back | `COLLECTING RENT`; health → `▮▮▮▯▯` | hop ×3, hit | M3 |
| **F4** | 7.40–10.20 | Obstacle 3: a tenant with a suitcase and a coin bag sprints past him from behind and exits frame right; the owner reaches out, trips | `LEFT WITHOUT PAYING`; health → `▮▮▯▯▯` | run steps, trip | M3 |
| **F5** | 10.20–12.60 | Obstacle 4: a tower of ledgers, sheets and a calculator topples onto him; he is half-buried | `NO RECONCILIATION`; health → `▮▯▯▯▯` | crash | M3 |
| **F6** | 12.60–15.00 | Obstacle 5: a swarm of angry red ticket-bubbles dives at him; he sits down; the world desaturates from 14.2 s | `COMPLAINTS`; health → `▯▯▯▯▯`; `GAME OVER?` centre flash 14.2–15.0 s | swarm buzz, low tone | M3 |
| **F7** | 15.00–18.00 | Turning point: dark panel with cyan border slides up (15.0–15.5); header appears; the two lines type in (15.8–17.2); on the last letter a RentOk-blue phone drops into his hand (17.2–17.6), its screen shows the wordmark; white flash; colour returns; health refills in cyan (17.6–18.0); panel slides away | `CHEAT CODE:` · `INSTALL` · `RENTOK APP` (typed); health → `▮▮▮▮▮` | key-clicks ×18; power-up arpeggio at 17.4 | **M4** (install event at 17.4 s, inside the middle third) |
| **F8** | 18.00–19.60 | The owner stands, cyan aura pulses around him, he fires one test tick upward-right; a phone icon appears beside the health bar | `POWER UP!` centre flash 18.0–19.2 | aura hum, pew | **M5** |
| **F9.1** | 19.60–20.80 | Clearing run begins at higher speed; obstacle 1 re-enters; a tick projectile bursts the document wall into pixels; a green chip flies to the checklist (row 1) | `TENANT VERIFICATION` (0.4 s) → `✓ DIGITAL KYC` (persists) | pew, burst, chip ding | M6, M10 |
| **F9.2 — HERO** | 20.80–22.00 | Obstacle 2 re-enters; the padlocked sack bursts under a tick; the owner mid-run with aura, five cyan health segments, the phone icon in the HUD, first chip already on the checklist. **Hero frame = t 21.40 s**: without any copy it shows the app-powered owner blasting the rent problem | `COLLECTING RENT` → `✓ AUTOPAY` | pew, burst, ding | M6, M10, hero (3.2) |
| **F9.3** | 22.00–23.20 | The fleeing tenant re-enters ahead; a tick tags him; he freezes and turns transparent with a ledger line drawn beside him; chip row 3 | `LEFT WITHOUT PAYING` → `✓ DUES TRACKED LIVE` | pew, ding | M6, M10 |
| **F9.4** | 23.20–24.40 | The ledger tower re-enters and is blasted into one neat stack/screen; chip row 4 | `NO RECONCILIATION` → `✓ ONE DASHBOARD` | pew, burst, ding | M6, M10 |
| **F9.5** | 24.40–25.60 | The ticket swarm re-enters; ticks turn each red bubble green as they hit; chip row 5 — all five chips now visible | `COMPLAINTS` → `✓ COMPLAINT TICKETS` | pew ×3, ding | M6, M10 |
| **F10** | 25.60–27.60 | The flagpole enters; the owner jumps (26.2), grabs the pole at 26.6 (flag reached), the RentOk-blue flag with a cyan tick rises to the top (26.6–27.4); pixel confetti; scroll stops | `LEVEL CLEAR!` centre flash 26.6–27.6 | flag fanfare (original) | **M6** (flag) |
| **F11** | 27.60–30.00 | Cut: the game freezes, dims to brand blue (0.3 s); the wordmark (≈ 700 px wide) centred at y ≈ 700; CTA two lines below; URL below that; last 1.0 s held still | `INSTALL` · `RENTOK APP` · `RENTOK.COM` + WORDMARK raster | soft hit; bed resolves and ends at 29.8 | M10; last frame (3.6) |

Timecode sum: 1.8 + 2.8 + 2.8 + 2.8 + 2.4 + 2.4 + 3.0 + 1.6 + 6.0 + 2.0 + 2.4 = **30.0 s** (`board.json` verified by code).

### 3.7 Every mandatory event on a numbered frame

| M | Frame(s) |
|---|---|
| M1 platform game | F1–F10 (continuous), HUD from F1 |
| M2 PG owner recognisable | F1 (HUD name + props), every gameplay frame |
| M3 five obstacles | F2, F3, F4, F5, F6 (and again F9.1–F9.5) |
| M4 install RentOk = turning point | F7 (event at 17.4 s) |
| M5 visible enhanced ability | F8 (aura, projectile, phone icon) |
| M6 overcome obstacles, reach flag | F9.1–F9.5 (five clears), F10 (flag at 26.6 s) |
| M7 30 s | whole board (30.0 s) |
| M8 platform/safe zones | every string inside (65,288)–(888,1248) — audition + CF4 |
| M9 original Mario-inspired | Stage 2c table applied to every sprite/sound |
| M10 why RentOk is relevant | F9.1–F9.5 chips + F11 |
| M11 no unverified claim | copy deck strings only; `claims_source_map` in `copy-deck.json` |

### 3.13 Author's own list of answers given as a claim rather than a frame or a line (for the checker to reopen if they disagree)

- 3.2 hero frame: given as a numbered frame (F9.2, t 21.40) — not a claim.
- 3.9 readability: given as measured pixel widths/heights from a rendered audition — not a claim; the contrast figures are **not yet measured** (they will be at composition, C2) — that part is a plan, stated as such.
- Player-identity strength of the "keys + register" cue at 220 px sprite height is a **prediction** until the character sheet exists — it is the riskiest generative item and is tested first (Stage 4).

## Stage 3 exit criteria — self-assessment (the checker issues the gate verdict)

| Criterion | Self-assessment |
|---|---|
| A board exists with numbered frames and timecodes summing to 30.0 s | Met — Part D, `board.json` |
| A numbered hero frame, not a sentence | Met — F9.2 at 21.40 s |
| Every mandatory event sits on a numbered frame | Met — 3.7 |
| Copy deck exists with exact strings; on-screen = spoken | Met — `copy-deck.json`; no spoken lines |
| Canon consulted by id with claim text; gaps named | Met — Part A; 8 uncompiled packs + audio named as gaps |
| 21 check lines rendered by id | Met — A3 |
| Readability at phone size shown, not asserted | Met for geometry (audition); contrast pending measurement at composition (stated) |
| Voice audition | n-a (no voice; reason recorded); typography audition done in its place |

Written by the producer session (lane A). Not a verdict.
