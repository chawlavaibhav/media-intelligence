# Stage 1 — Intent (gate: nothing invented; every mandatory item has a verification method)

Job `AGY-2026-09-20-RENTOK-GAME-LANE-A-001` · applied by hand from `input/04-QUESTION-TEMPLATE-v0.1-FROZEN.md` §Stage 1.
Inputs: `input/01-CUSTOMER-BRIEF-FROZEN.md` (the only customer words), `input/03-ACCEPTANCE-CONTRACT.md` (A1–A11).
Rule kept throughout: customer words are quoted; anything else is marked **decide** with the cost of being wrong. The customer is not asked anything further (Controller note).

Vocabulary: **class** DET = deterministic code check on the delivered file · LJ = independent visual inspection by a non-author session · HJ = human (customer, blind) · RSR = a structure/retrieval question answered from Canon or platform documents · EMC = evidence-from-cases question. **priority** `blocks` = the stage cannot close without an answer · `default-recorded` = a recorded default lets work proceed.

---

## 1.1 What is the deliverable?

- Why it matters: fixes the container, geometry, count and duration every later check measures against (A7, A8).
- Class/priority: DET · blocks. Source: **preserve**.
- Evidence (customer, verbatim): "I want to make a video for RentOK." · "Platforms: Instagram Reels / Facebook and YouTube Shorts." · "Duration: 30 seconds."
- Answer: one finished video, 30 s, vertical 9:16, delivered as one MP4 suitable for Instagram Reels / Facebook Reels and YouTube Shorts.
- Decision: `contract.deliverable = {count: 1, kind: game-style advertising film, duration_s: 30.0 (A7 tolerance 29.5–30.5), aspect: 9:16, pixels: 1080×1920, container: MP4 H.264/AAC}`. Pixel/codec values are the acceptance contract's (A8); Stage 2 re-verifies them against the platform pages.
- Assumption: one master file serves both platform families (both accept 9:16 1080×1920 MP4 — to be confirmed at 2.1). Cost if wrong: one extra encode, USD 0.

## 1.2 What is it for, and what should the viewer do or feel?

- Why it matters: sets the proposition (3.1), the ask (3.5) and the HJ acceptance test A10 ("communicates why RentOK is relevant to a PG owner").
- Class/priority: HJ · blocks. Source: **preserve** for the purpose; **decide** for the viewer action.
- Evidence: "The video should feel like an actual platform game, not a conventional promotional video with gaming graphics placed over it." · "The video must communicate why RentOK is relevant to a PG owner." · "The game also introduces a cheat code — install RentOK app."
- Answer: an advertisement for RentOK aimed at PG owners; the viewer should recognise their own daily problems in the obstacles and understand that installing the RentOK app is what changes the game.
- Decision: `contract.objective = "A PG owner watching on a phone recognises the five problems as their own and understands that installing RentOK is the move that changes them; the film feels like a game first, an ad second."` Viewer action = install/try the app (the customer's own "cheat code — install RentOK app").
- Assumption (decide): the ask is "install the app" rather than "book a demo" (the site offers both: `home.txt` L49 "Get free demo", L140 "Get the app"). Cost if wrong: CTA wording repair, USD 0 (code-set text).

## 1.3 Which brand, product or person must appear, and which features must be exact?

- Why it matters: exact strings are byte-checked at Stage 5 (5.1); brand marks decide what must be originated versus copied.
- Class/priority: DET · blocks. Source: **preserve** (brand must appear) + **lookup-fact** at Stage 2 (spelling, wordmark, colours).
- Evidence: "Brand and product source: Official RentOK website, https://rentok.com." Controller note: the customer writes "RentOK", the site spells "RentOk".
- Answer: the RentOK/RentOk brand name and app must appear; no person, packshot or supplied logo file exists. The wordmark and colours are only observable from the frozen snapshot (Stage 2.5).
- Decision: `contract.distinctive_assets = [brand name (spelling resolved at 2.4/2.5), app depiction (a phone with the app — originated), no supplied logo file]`. Every exact string is code-set (mechanism B, RR-1); none is generated in-scene unless Stage 4 records why with evidence.
- Assumption: none yet; the spelling question is a Stage 2 fact question, not an assumption.

## 1.4 Which events or facts are mandatory (customer's own words) — each with a verification method

Class DET/LJ/HJ as named · priority **blocks** (template correction 1: a row without a verification method blocks Gate 1). "Named independent visual inspection" = the checker session that issues gate verdicts, working from the assembled film plus the contact sheet under `qa/`; it is never the author.

| id | Mandatory event (customer words) | Acceptance ref | Verification method |
|---|---|---|---|
| M1 | "The video has a Mario game." / "should feel like an actual platform game" | A1 | LJ: checker confirms on the contact sheet a side-scrolling level, a player character, obstacles, HUD elements and a finishing flag, and that the game is the film rather than an overlay; HJ: customer blind verdict |
| M2 | "The player is basically a PG owner." / "must be recognizable as the player" | A2 | LJ: checker names the cue(s) that make the character a PG owner (Stage 3 fixes them: a keyring, a "PG" cap/badge, a rent register) at the hero frame and at least one gameplay frame; DET: the PG-owner label string (if used) present in the copy deck and rendered (`check_exact_copy`) |
| M3 | Obstacles = "tenant verification, collecting rent, tenants leaving without paying rent, no place to do reconciliation, solving complaints" | A3 | DET: five obstacle labels present in `copy-deck.json` and byte-rendered on their frames (compositor exact-copy check); LJ per-obstacle checklist: each of the five identifiable by picture + label |
| M4 | "The game also introduces a cheat code — install RentOK app." / "must be the central turning point" | A4 | DET: the install event sits on a numbered frame with a timecode inside the middle third of the film (timeline.json); the string "INSTALL RENTOK" (exact form fixed at Stage 3) byte-present; LJ: checker confirms the film's state changes visibly at that frame |
| M5 | "Mario gets a gun sort of power/immunity" / "visibly enhanced ability … game-style power/immunity mechanic is preserved" | A5 | LJ: checker confirms a visible change of the character (glow/aura/projectile) and that the change is used, not decorative; DET: a `powered` character asset distinct from the `base` asset exists in the asset ledger and appears after the install frame only |
| M6 | "It runs and kills all the obstacles and gets the flag." / "overcome the obstacles … reach the finishing flag" | A6 | LJ: checker counts obstacles cleared after the power-up (target: all five re-appear and are cleared) and sees the flag reached; DET: the flag frame exists in timeline.json and is the last gameplay beat before the end card |
| M7 | "Duration: 30 seconds." | A7 | DET: `ffprobe` duration 29.5–30.5 s |
| M8 | "Platforms: Instagram Reels / Facebook and YouTube Shorts." | A8 | DET: ffprobe 1080×1920, H.264/AAC, MP4, within the size/duration limits recorded at 2.1; LJ: critical text inside the safe zones recorded at 2.2 |
| M9 | "An original Mario-inspired game, rather than an exact reproduction of Nintendo's character, artwork, music or game assets." | A9 | LJ + the Stage 2 IP record (2c): checker applies the do/don't list to the character, world, obstacles, sound |
| M10 | "The video must communicate why RentOK is relevant to a PG owner." | A10 | HJ (customer, blind); proxy before that: LJ checker states in one line what the film says RentOK does, without help from the copy deck |
| M11 | "Do not add unverified claims that RentOK guarantees rent recovery, prevents tenants from leaving, or automatically eliminates all operational problems." | A11 | DET: string scan of every on-screen string in `copy-deck.json` against `spec.permitted_claims[]` and the forbidden list (Stage 2b); LJ: the picture does not imply a guarantee either (e.g. no "100%" badge, no "never again" line) |

## 1.5 What is forbidden?

- Why it matters: drives the forbidden-claims scan (A11), the IP record (A9), and the "not a conventional ad" test (A1).
- Class/priority: DET · blocks. Source: **preserve** (customer) + Controller governance.
- Evidence (customer): "Do not replace the game concept with a conventional testimonial, generic SaaS advertisement, or unrelated lifestyle film." · "Do not add unverified claims that RentOK guarantees rent recovery, prevents tenants from leaving, or automatically eliminates all operational problems." · "An original Mario-inspired game, rather than an exact reproduction of Nintendo's character, artwork, music or game assets."
- Evidence (Controller, governance not creative): no live filming, no stock footage, no human actors, no reuse of earlier RentOK material; no fal, no new paid services; no generated exact text without recorded reason + evidence; no mutation of Canon/Registry/coordination.
- Decision: `contract.forbidden = [testimonial format; generic SaaS ad; lifestyle film; any claim of guaranteed rent recovery; any claim that tenants cannot leave / will not leave; any claim that all problems are eliminated; any Nintendo character, artwork, level design, music or asset; any unverified product capability; live footage / stock / actors / prior RentOK material; in-scene generated exact text without Stage 4 record]`.
- Assumption: "kills all the obstacles" is the customer's game metaphor (Controller note); clearing obstacles in the game frame is allowed, stating elimination in copy is not. Cost if wrong: none — this reading is the customer's own intent block.

## 1.6 Tone / register, with one example the customer accepts

- Why it matters: HJ acceptance (B "creative quality") and the audio direction.
- Class/priority: HJ · default-recorded. Source: **decide** (customer: "Visual treatment: Delegated to the creative system.").
- Evidence: the customer's example is the request itself — "a Mario game", "cheat code", "gets the flag": playful, retro-arcade, knowing.
- Answer: playful 8-bit/16-bit arcade register with a dry, confident commercial close; the PG owner's problems are shown with affection, not mockery.
- Decision: `contract.tone = "retro-arcade playful; the joke is on the problems, never on the owner; the close is calm and clear"`.
- Assumption: the customer will accept an original pixel-art look as "a Mario game" without the Nintendo look. Cost if wrong: creative-direction repair (a new art style) — the most expensive kind of repair (re-draw of the character sheet, ≈ USD 0.07–0.20 per still plus any dependent clips). Mitigation: the character sheet is the first paid asset and is checker-inspected before dependents (Stage 4 order of work).

## 1.7 Language(s) per surface

- Why it matters: every exact string's script and the text-shaping path (Latin only vs Devanagari via HarfBuzz).
- Class/priority: DET · default-recorded. Source: **decide** (customer silent; the request and the site are in English).
- Evidence: `home.txt` L1 "RentOk | PG/Hostel/Flat Management App", L40–43 "The easiest way to manage your PGs … Save time. Work less. Earn more." — the site's own copy is English with occasional Hinglish flavour (L84 "No more jhikjhik").
- Answer: on-screen English (Latin script), short nouns. No spoken narration by default (Stage 3 decides audio; any VO would be English).
- Decision: `contract.language = {on_screen: en (Latin), spoken: none by default}`.
- Assumption: English labels are readable by the audience of a Bangalore/Pune/Hyderabad/Delhi PG owner (the site's own stated audience, `autopay.txt` L267). Cost if wrong: labels are code-set, a Hinglish re-render is USD 0.

## 1.8 Where will it run?

- Class/priority: DET · blocks. Source: **preserve**. Evidence: "Platforms: Instagram Reels / Facebook and YouTube Shorts."
- Decision: `contract.channel = [Instagram Reels, Facebook Reels, YouTube Shorts]`, organic post assumed (paid-ad specs not requested). Assumption cost: if the customer runs it as a paid Reels ad, the same 9:16 file applies; ad-specific text-overlay rules are not asserted here.

## 1.9 Spend cap, deadline, approver

- Class/priority: DET · blocks (spend) / default-recorded (deadline, approver). Source: Controller (spend); **decide** (deadline); **preserve** (approver from the acceptance contract §E).
- Evidence: Controller: "Plan to a PROVISIONAL ceiling of USD 10.00 for this lane (credits only, 0 hidden retries, hard stop). Treat it as unconfirmed." Acceptance contract §E: the customer, blind, issues ACCEPT / SPECIFIC REPAIR / REJECT.
- Answer: cap = **unresolved** (provisional USD 10.00 for planning; `CAP_USD = 0.0` in tools until the written cap arrives). Deadline: not stated — this experiment session. Approver: the customer (blind) via the Controller; the checker session gates stages.
- Decision: `contract.cap = provisional USD 10.00, unconfirmed; contract.deadline = unknown (not stated); contract.approver = customer (blind, §E)`.
- This is the one `ask` that stays open and it is the Controller's, not the customer's.

## 1.10 On what basis will the customer accept?

- Class/priority: DET+HJ · blocks. Source: **preserve** — the acceptance contract A1–A11 is given and identical for both lanes.
- Decision: `contract.acceptance[] = A1..A11` as written in `input/03-ACCEPTANCE-CONTRACT.md`; the mapping to checks is in 1.4 above and expanded in Stage 4's QA plan.

## 1.11 Does anything contradict itself, the platform, or the customer's other instructions? (flags)

| flag | Contradiction | Resolution | Status |
|---|---|---|---|
| F1 | "a Mario game" (request) vs "original Mario-inspired game, rather than an exact reproduction" (confirmed answer) | The confirmed answer governs: original character/world/sound; the platform-game grammar (side-scroll, jump, obstacles, flag, HUD) is genre, not Nintendo property. Concrete do/don't list at Stage 2c. | resolved |
| F2 | "kills all the obstacles" vs "Do not add unverified claims that RentOK … automatically eliminates all operational problems" | Obstacles are cleared inside the game (allowed: the customer's metaphor); no on-screen or spoken copy states or implies elimination, guarantee or prevention; the product-capability copy uses only Stage 2 permitted claims. | resolved (checked by A11 scan + LJ) |
| F3 | "a gun sort of power" vs platform suitability and the brand's register | The customer delegated the power-up design "while preserving the requested game-style power/immunity mechanic". Decide: a projectile/immunity power-up that is not a firearm (Stage 3 designs it, e.g. the app's tick-mark projectile plus a shield aura). The mechanic — the character now fires at/through obstacles and cannot be hurt — is preserved. Cost if wrong: the customer wanted a literal gun; repair = swap the projectile sprite (one still, USD ≤ 0.13, or code). | resolved as a recorded decision |
| F4 | A side-scrolling platform game is a landscape form; the deliverable is 9:16 | Stage 3 designs a vertical-native level: the playfield is the full 9:16 frame, the level scrolls horizontally in the middle band with the ground low in frame, HUD at top inside the safe zone, obstacles taller than wide. Gameplay must still read at phone size (A8/B). | resolved in design; verified at 3.9 / CF4 |
| F5 | "RentOK" (customer) vs "RentOk" (site) | Stage 2.4/2.5 fact question. | open → Stage 2 |
| F6 | The customer says "install RentOK app"; the site's primary calls are "Get free demo" / "Try for free" / "Get the app" (`home.txt` L49, L76, L140) | The CTA copy is chosen at Stage 3 from strings the site itself uses, so the ask is supported; "install" is the customer's word and may be used as the in-game cheat-code label. | resolved |

No flag blocks Stage 3; F5 resolves at Stage 2 before any copy is frozen.

## 1.12 Which of the above did we decide rather than the customer, and what is the cost of being wrong?

| id | Decided by us | Cost of being wrong | Tier |
|---|---|---|---|
| D1 | Viewer action = install/try the app (1.2) | CTA string re-render, USD 0 | low |
| D2 | English on screen, no spoken narration by default (1.7; audio finalised at Stage 3) | label re-render USD 0; adding VO later ≈ USD 0.01–0.02 (TTS) + re-assembly | low |
| D3 | Retro-arcade playful tone; original pixel-art look (1.6) | creative-direction repair: new character sheet ≈ USD 0.07–0.20 + dependent clips | high — mitigated by testing the character first |
| D4 | Non-firearm projectile/immunity power-up (F3) | one sprite swap ≈ USD 0.07–0.13 or code | low-medium |
| D5 | Vertical-native level design (F4) | if gameplay is unreadable at phone size: re-layout by code, USD 0 (code-animated) | low if code-animated; high if generative |
| D6 | One master file for both platform families (1.1) | one extra encode, USD 0 | low |
| D7 | Organic placement assumed (1.8) | none for the file; ad-policy text rules not asserted | low |

High-cost assumption D3 would normally be asked; the Controller has ruled the customer is not asked, so it is mitigated by order of work (character first, checker-inspected, frozen) rather than by a question.

## Generated questions (job-specific layer) — inverse form

Format: what must the viewer perceive → what observable property carries it → which controllable parameter produces it → which route can produce it → what would break it → destination.

| id | Question chain | Destination |
|---|---|---|
| G1 (M1) | Perceive "this is a platform game" → a continuous side-scrolling ground line, a jumping character, a HUD strip, a flag → tile-based level rendered by code, sprite jump arc by code, HUD strings code-set → code/procedural (Pillow + ffmpeg) with generative stills only for sprites/backgrounds → broken by: cutting to non-game footage, camera moves a game would never make, photoreal rendering | Stage 3 board frames 1–N; Stage 4 method = code animation |
| G2 (M2) | Perceive "the player is a PG owner" → a costume/prop cue readable at ≈ 200 px sprite height (keyring, "PG" cap, ledger) plus a HUD label → sprite design prompt + HUD label string → nano-banana-2 character sheet (still) + code overlay → broken by: a generic hero, cue too small at phone size, label in the occluded band | Stage 3 player identity; 3.9 readability; Stage 4 micro-qualification |
| G3 (M3) | Perceive each of the five problems → an obstacle whose picture says the problem before the label does (e.g. a wall of documents, a fleeing tenant with a bag, a spreadsheet mountain) + a 1–3-word label → five obstacle sprites + five code-set labels → nano-banana-2 stills, code labels → broken by: labels that are claims, picture ambiguity, two obstacles that look alike | Stage 2b claims; Stage 3 obstacles; A3 checklist |
| G4 (M4) | Perceive "installing RentOK is the turning point" → the game visibly pauses/changes state at the install event (cheat-code entry, screen flash, phone with the app) in the middle of the film → a dedicated 2–3-s beat with the string "INSTALL RENTOK APP" (form fixed at Stage 3) → code composition on a textless phone plate → broken by: the beat too short, brand mark unreadable, event placed at the end instead of the middle | Stage 3 turning-point beat; M4 DET |
| G5 (M5) | Perceive "the character has a new power/immunity" → sprite change (aura/colour) + projectile + obstacles no longer hurt → a second character sheet (powered) + projectile sprite + hit-flash by code → nano-banana-2 still from the base sheet as reference (identity risk) → broken by: the powered character no longer reading as the same character | Stage 4 riskiest capability (identity across two sheets); micro-qualification |
| G6 (M6) | Perceive "obstacles overcome, flag reached" → each of the five obstacles re-appears and is cleared by the projectile/immunity, then the flag → code choreography → broken by: fewer than five cleared, flag not reached, ending on a card before the flag | Stage 3 frames; A6 |
| G7 (M8) | Perceive nothing hidden by platform UI → all critical text inside the documented safe zones → layout constants from Stage 2.2 → code → broken by: a HUD or label in the bottom ≈ 20 % or right rail | Stage 2.2; CF4 |
| G8 (M11) | Perceive no guarantee → every string on screen in the permitted list; no "100%", "never", "guaranteed" → copy deck scan → broken by: a generated frame that draws text | A11 scan; frame text hygiene D1 |

Deleted generated question: "what font family reads as 'retro'?" — informs no requirement or check beyond 3.9 readability; folded into Stage 3 typography (one line).

## Stage 1 exit criteria — self-assessment (the checker issues the gate verdict)

| Criterion | Self-assessment |
|---|---|
| Nothing invented: every customer requirement is a quotation | Met — 1.1–1.5, 1.8, 1.10 quote the frozen brief; no requirement is paraphrased |
| Every mandatory item (M1–M11) carries a verification method | Met — table 1.4; DET where deterministic, LJ named as the checker session, HJ = customer blind |
| Assumptions separated from requirements with cost of being wrong | Met — 1.12, D1–D7; one high-cost assumption (D3) mitigated by order of work |
| Flags resolved or routed | Met — F1–F4, F6 resolved; F5 routed to Stage 2 (fact) |
| Open asks | One: the written spend cap (Controller's, not the customer's). No customer ask remains |

Written by the producer session (lane A). Not a verdict.
