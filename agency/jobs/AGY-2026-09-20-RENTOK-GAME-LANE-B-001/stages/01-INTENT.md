# Stage 1 — Intent · AGY-2026-09-20-RENTOK-GAME-LANE-B-001 (lane B)

Author: lane-B producer session. Date: 2026-09-20. Cost: USD 0.
Inputs: `input/01-CUSTOMER-BRIEF-FROZEN.md` (the only customer words), `input/03-ACCEPTANCE-CONTRACT.md`, `input/04-QUESTION-TEMPLATE-v0.1-FROZEN.md` (Stage 1 lines 1.0–1.12), Controller constraints from the task brief.
`input/02-CHATGPT-DIRECTION-LANE-B-ONLY.md` is **not** an input to this stage: it is a PROPOSED creative direction, and nothing from it enters the intent contract (it is interrogated at Stage 3).

Vocabulary: **preserve** = the customer said it (quoted) · **decide** = we chose, shown for veto, with the cost of being wrong · **lookup-fact** = to be fetched and dated · **derive** = follows from other answers. Class: DET (code can check it) · LJ (named independent visual inspection) · HJ (human/customer judgment) · RSR / EMC as in the template. Priority: **blocks** (the stage cannot close without it) · **default-recorded** (a default is recorded; proceeding is permitted).

The customer will not be asked anything further (Controller note in the frozen brief); every residual `ask` below has become `decide` with an assumption and the cost of being wrong.

---

## 1.0 — Production means (template correction 2)

| | |
|---|---|
| Question | Is the deliverable produced by generative models and/or code, with nothing solved by live filming? |
| Why it matters | Rules out filming, stock, actors and earlier RentOK material before any creative decision; every element must be solved by references, composition, code or a test. |
| Class / priority | DET / blocks |
| Source | Controller constraint (task brief) + the frozen brief's confirmed answer "Game identity: An original Mario-inspired game" |
| Evidence | Task brief: "The deliverable is produced by generative models and/or code — no live filming, no stock footage, no human actors, no reuse of any earlier RentOK material." |
| Answer | Yes. Generative models (credit pools only) and code (Pillow / ffmpeg / hb-view). |
| Decision | Every visual element is either generated under a route in the routing table or drawn/composed by code. No exceptions. |
| Assumption | none |

## 1.1 — Deliverable

| | |
|---|---|
| Question | What is the deliverable (type, count, formats, duration band)? |
| Why it matters | Fixes the container the whole plan is built for (one file, one geometry, one duration); A7/A8 are checked against it. |
| Class / priority | DET / blocks |
| Source | preserve |
| Evidence | Customer: "I want to make a video for RentOK." · "Platforms: Instagram Reels / Facebook and YouTube Shorts." · "Duration: 30 seconds." |
| Answer | One video, 30 s, for Instagram Reels / Facebook and YouTube Shorts. Pixel geometry, codec and container are Stage 2 lookup-facts (A8 names 9:16 1080×1920 H.264/AAC MP4 as the expected result of that lookup; I do not assert it from memory here). |
| Decision | `contract.deliverable`: 1 × vertical short video, 30.0 s target (A7 tolerance 29.5–30.5 s by ffprobe), one master file; per-platform variants only if Stage 2 shows the platforms need different files. |
| Assumption | "30 seconds" means the whole file is 30 s including the end card (not 30 s of game plus a card). Cost of being wrong: low — a 30-s file is what both platforms accept; a longer file would breach A7. |

## 1.2 — Purpose and the viewer's action

| | |
|---|---|
| Question | What is the video for, and what does the customer want the viewer to do or feel? |
| Why it matters | Sets the ask (Stage 3 CTA copy) and the acceptance item A10 ("communicates why RentOK is relevant to a PG owner"). |
| Class / priority | HJ / blocks |
| Source | preserve (purpose) + decide (viewer action) |
| Evidence | Customer: "The video must communicate why RentOK is relevant to a PG owner." · "The game also introduces a cheat code — install RentOK app." · Site (home.txt line 140): "Get the app"; line 49: "Get free demo". |
| Answer | Purpose: make a PG owner recognise their own daily problems and see RentOK as the thing that changes the game. Viewer action: **install the RentOK app** — decided, because the customer's own turning point is "install RentOK app" and the site's primary CTA is "Get the app". |
| Decision | `contract.objective`: awareness + app-install intent among PG/hostel owners in India. The ask on the end card is an install/get-the-app line (exact words at Stage 3). |
| Assumption | The customer wants app installs rather than "book a demo". Cost of being wrong: low — the cheat code is literally "install RentOK app", and an install line does not contradict a demo funnel. |

## 1.3 — Product, brand, exact features

| | |
|---|---|
| Question | Is there a product, brand or person that must appear, and which features must be exact (marks, colours, label text)? |
| Why it matters | Exact strings are composed by code (mechanism B); anything exact that a model draws must be text-scanned. Decides what Stage 2 must source. |
| Class / priority | DET / blocks |
| Source | preserve + lookup-fact (Stage 2) |
| Evidence | Customer: "a video for RentOK", "install RentOK app", "Brand and product source: Official RentOK website, https://rentok.com". Site titles in the snapshot spell "RentOk" (home.txt line 1 "RentOk \| PG/Hostel/Flat Management App"; line 63 "RentOk"). Snapshot html references a wordmark file `rentok-new-logo.webp` and `theme-color #0038FF` (OBSERVED in `home.html`; the file itself is not in the snapshot — Stage 2 fetches and hashes it). |
| Answer | Brand: RentOK/RentOk — the name must appear exactly; spelling is a Stage 2 fact question (D1 below). The app must appear as an installable thing inside the game (the cheat code). No person must appear. No product photograph exists; the "product" is an app — the site's dashboard/app screens are the only visual product reference and are not to be reproduced pixel-for-pixel (they are claims evidence, not assets). |
| Decision | `contract.distinctive_assets`: (a) brand name string, exact, code-set; (b) brand colour(s) as observed on the site (Stage 2); (c) an original in-game app icon/phone representation carrying the brand name; (d) the site wordmark on the end card if Stage 2 obtains a usable file — otherwise the name set in type by code. All product-capability depictions must cite a snapshot line (Stage 2). |
| Assumption | The site's wordmark is a brand asset, not "earlier RentOK material" (the exclusion targets prior creative). Cost of being wrong: low — the fallback (name set by code in brand colour) needs no asset. |

## 1.4 — Mandatory events and facts (customer's own words) — each with a verification method

| id | Customer words (verbatim) | What must be in the file | Verification method (mandatory) | Class |
|---|---|---|---|---|
| M1 | "The video has a Mario game." + "The video should feel like an actual platform game, not a conventional promotional video with gaming graphics placed over it." | A side-scrolling platform level with a player character, obstacles, HUD elements (score/hearts/level), and a finishing flag; the game frame runs for most of the 30 s, not as a decoration | LJ: named independent inspection (the checker session) on the assembled film with a five-item checklist: side-scroll level · player character · obstacles · HUD · flag. DET support: the storyboard assigns the game frame ≥ 24 of 30 s; assembly log proves the timeline. HJ: the customer's blind verdict (A1) | LJ+HJ |
| M2 | "The player is basically a PG owner." + "The PG owner must be recognizable as the player." | The player character carries PG-owner identifiers readable at phone size (costume/props/label/context) | LJ: checker names the identifier(s) seen at phone size on frames 1–3 without being told; DET support: the copy deck's player label string (if used) rendered byte-exact | LJ+HJ |
| M3 | "The obstacles in the game are basically the problems that owner faces — tenant verification, collecting rent, tenants leaving without paying rent, no place to do reconciliation, solving complaints and so on." + "The obstacles must represent genuine PG-management problems." | Five obstacles, each identifiable as one named problem | DET: the five obstacle label strings exist in the copy deck and are rendered byte-exact (code-set text, exact-copy byte-check C6) and each sits on a numbered storyboard frame. LJ: per-obstacle checklist (A3) — the checker maps each obstacle to a named problem | DET+LJ |
| M4 | "The game also introduces a cheat code — install RentOK app." + "The RentOK installation must be the central turning point." | An in-game cheat-code event whose content is installing the RentOK app, placed at the structural midpoint / turning point | DET: the cheat-code string is in the copy deck and rendered byte-exact at the planned frame; the storyboard shows the before/after split around it. LJ+HJ: reads as the turning point (A4) | DET+LJ+HJ |
| M5 | "Once it is done, Mario gets a gun sort of power/immunity." + "The character must acquire a visibly enhanced ability" + "Power-up design: Delegated to the creative system, while preserving the requested game-style power/immunity mechanic." | After install, the character visibly gains a power-up (a game-style projectile/immunity ability) and it is used | LJ: checker confirms a visible acquisition event and a visible change of the character's state (A5); HJ: customer | LJ+HJ |
| M6 | "It runs and kills all the obstacles and gets the flag." + "use it to overcome the obstacles, and reach the finishing flag." | The character, with the power-up, overcomes each of the five obstacles and reaches the flag | LJ: checker ticks all five overcome + flag reached (A6); DET support: storyboard has five clear-beats and one flag beat, each numbered | LJ+HJ |
| M7 | "Duration: 30 seconds." | 29.5–30.5 s | DET: `ffprobe` duration on the delivered file (A7) | DET |
| M8 | "Platforms: Instagram Reels / Facebook and YouTube Shorts." | Meets the platforms' current published specs; critical text inside the safe zones documented at Stage 2 | DET: ffprobe geometry/codec/duration/size vs the Stage 2 spec; LJ: safe-zone visual on the final file (A8) | DET+LJ |
| M9 | "Game identity: An original Mario-inspired game, rather than an exact reproduction of Nintendo's character, artwork, music or game assets." | No Nintendo character, artwork, level design, melody or asset | LJ: checker checks against the Stage 2 IP do/don't list (A9); DET support: no prompt contains a Nintendo name/asset word (grep over all generation prompts) | LJ |
| M10 | "The video must communicate why RentOK is relevant to a PG owner." | The film makes the relevance evident | HJ: customer verdict (A10); LJ proxy: the muted test — the checker states the relevance in one sentence after a sound-off viewing | HJ |
| M11 | "Do not add unverified claims that RentOK guarantees rent recovery, prevents tenants from leaving, or automatically eliminates all operational problems." | No on-screen or spoken line states or implies those | DET: string scan of the full copy deck + any VO transcript against the Stage 2 forbidden-claims list and permitted-claims list (A11); LJ: implied-claim check by the checker | DET+LJ |

## 1.5 — Forbidden

| | |
|---|---|
| Question | What is forbidden (claims, tone, content, competitors)? |
| Why it matters | Becomes the DET scan list (A11) and the creative no-go list. |
| Class / priority | DET / blocks |
| Source | preserve + derive (Controller constraints) |
| Evidence | Customer: "Do not replace the game concept with a conventional testimonial, generic SaaS advertisement, or unrelated lifestyle film." · "Do not add unverified claims that RentOK guarantees rent recovery, prevents tenants from leaving, or automatically eliminates all operational problems." · "not an exact reproduction of Nintendo's character, artwork, music or game assets." Controller: no filming/stock/actors/prior RentOK material; no fal, no new paid services; product claims only with a snapshot line. |
| Answer | `contract.forbidden[]`: F1 testimonial / generic SaaS ad / lifestyle film structure · F2 claims of guaranteed rent recovery, of preventing tenants leaving, of eliminating all problems (word-level list built at Stage 2: "guarantee(d)", "never", "100%", "zero problems", "no more problems", "all problems", "always paid", "can't leave", etc.) · F3 any Nintendo character/asset/melody/level · F4 any product capability not cited to a snapshot line · F5 competitor names (none named by the customer; none will appear — decided) · F6 any tool/model name on screen (QA E3). |
| Decision | F2's word list is a DET check over the copy deck and any VO transcript; F1/F3 are LJ; F4 is a Stage 2 citation table. |
| Assumption | none material. |

## 1.6 — Tone / register

| | |
|---|---|
| Question | Tone/register, with one example the customer accepts? |
| Why it matters | Drives the visual system, music and copy voice; a mismatch is the most likely SPECIFIC REPAIR. |
| Class / priority | HJ / default-recorded |
| Source | decide (customer: "Visual treatment: Delegated to the creative system.") |
| Evidence | Customer's own framing is playful ("Mario game", "cheat code", "gun sort of power"); the site's voice is informal Indian-English with humour ("No more calls. No more running after tenants. No more jhikjhik", home.txt line 84). The only example the customer "accepts" is their own brief. |
| Answer | Retro-arcade, energetic, affectionate towards the PG owner (the owner is the hero, never the joke), confident about RentOK without hype. |
| Decision | `contract.tone`: "arcade, warm, quick". Copy voice: short game-style captions in caps; no corporate sentences inside the game frame. |
| Assumption | The customer will accept a humorous register. Cost of being wrong: medium (a taste rejection means a creative-direction repair, not a re-shoot); mitigated because the customer chose a game premise. |

## 1.7 — Language per surface

| | |
|---|---|
| Question | Language(s) per surface (spoken, on-screen)? |
| Why it matters | Decides fonts, TTS route and the exact-copy script; changes the whole copy deck. |
| Class / priority | DET / default-recorded |
| Source | decide (not stated by the customer) |
| Evidence | Site copy is English with Hinglish flavour (home.txt 84 "jhikjhik"); the customer wrote in English; the platforms are Indian-audience. |
| Answer | On-screen: English (short caps labels, the arcade convention; every label ≤ 3 words so it survives phone size). Spoken: decided at Stage 3 (VO or none); if VO exists it is English or Hinglish and its lines equal the on-screen lines where both exist (template 3.8). |
| Decision | `contract.language`: on-screen `en`; spoken `en`/`hi-en` or none (Stage 3). |
| Assumption | English labels are acceptable to the customer. Cost of being wrong: medium — a Hindi version would be a copy re-render by code (labels are code-set), not a regeneration of visuals; VO would be a new TTS take. |

## 1.8 — Channel

| | |
|---|---|
| Question | Where will it run (platform, placement)? |
| Why it matters | Stage 2 spec and safe zones. |
| Class / priority | DET / blocks |
| Source | preserve |
| Evidence | Customer: "Platforms: Instagram Reels / Facebook and YouTube Shorts." |
| Answer | Instagram Reels, Facebook (Reels), YouTube Shorts. Organic or paid placement is not stated. |
| Decision | `contract.channel` as above. Plan to the stricter of the specs; treat as organic short-form (no paid-ad policy review beyond a sanity check at Stage 2 on cartoon-weapon depiction). |
| Assumption | Organic placement. Cost of being wrong: low for specs (paid Reels/Shorts share the same 9:16 file specs — to be confirmed at Stage 2), medium for policy (a paid ad with a "gun" could face ad-policy review; the power-up design at Stage 3 avoids a realistic firearm). |

## 1.9 — Spend cap, deadline, approver

| | |
|---|---|
| Question | Spend cap, deadline, approver? |
| Why it matters | No paid call without a cap; the approver defines who says ACCEPT. |
| Class / priority | DET / **blocks** (cap) |
| Source | Controller in writing (cap) · decide (deadline) · preserve (approver from the acceptance contract §E) |
| Evidence | Task brief: "Plan to a PROVISIONAL ceiling of USD 10.00 for this lane (credits only, 0 hidden retries, hard stop). Treat it as unconfirmed." Acceptance contract §E: "the customer, blind … ACCEPT / SPECIFIC REPAIR / REJECT". |
| Answer | Cap: **unresolved** (provisional USD 10.00; `CAP_USD = 0.0` until the Controller's written confirmation). Deadline: none stated. Approver: the customer (blind, via the Controller). |
| Decision | Stage 4 plans to USD 10.00 and names what is cut if the confirmed cap is lower. |
| Assumption | none — the cap is the one item the Controller supplies. |

## 1.10 — Acceptance basis

| | |
|---|---|
| Question | On what basis will the customer accept (3–6 statements decidable from the file)? |
| Why it matters | The QA plan (Stage 4) maps every item to a named check. |
| Class / priority | DET+HJ / blocks |
| Source | preserve (the common acceptance contract was established before execution) |
| Evidence | `input/03-ACCEPTANCE-CONTRACT.md` A1–A11 (mandatory), B (creative quality), C (production quality), D (factual accuracy), E (commercial acceptance). |
| Answer | A1–A11 as written, each with its named check class; B–E as written. |
| Decision | `contract.acceptance[]` = A1–A11 + D. Nothing added, nothing removed. |
| Assumption | none. |

## 1.11 — Contradictions / flags

| id | Tension | Resolution | Blocks Stage 3? |
|---|---|---|---|
| FL1 | "a Mario game" vs "original Mario-inspired … not an exact reproduction" | Resolved by the customer's own confirmed answer: original. Stage 2 writes the concrete do/don't list. | no |
| FL2 | "kills all the obstacles" vs "Do not add unverified claims that RentOK … automatically eliminates all operational problems" | Inside the game frame, clearing five specific obstacles is the mechanic the customer asked for. The film must not generalise it: (a) each cleared obstacle turns into a specific, verified product outcome (Stage 2 permitted claims), never "all problems solved"; (b) no copy uses totalising words (F2 list); (c) the closing line is about relevance/next step, not elimination. Verified by DET scan (M11) + LJ implied-claim check. | no (rule recorded) |
| FL3 | "gun sort of power/immunity" vs platform tolerance of weapons and the customer's delegation of power-up design | The mechanic (projectile/immunity) is preserved; the object is designed as a non-realistic, clearly arcade device (Stage 3). Stage 2 does a sanity check of platform rules on weapon depiction in organic content. | no |
| FL4 | 30 s vs platform duration limits | Stage 2 lookup; expected within limits on both platforms (not asserted here). | no |
| FL5 | "install RentOK app" as a cheat code vs the site's wording "Get the app" | Both are the same action; the on-screen cheat-code string is decided at Stage 3 and is not a product claim. | no |

No flag blocks Stage 3.

## 1.12 — What we decided rather than the customer, and the cost of being wrong

| id | Decision (ours) | Cost of being wrong | Tier |
|---|---|---|---|
| D1 | Brand spelling on screen (RentOK vs RentOk) — Stage 2 fact question | low: a code-set string re-render, USD 0 | default-recorded |
| D2 | On-screen language English | medium: copy re-render by code; VO re-take if VO exists | default-recorded |
| D3 | The ask = install/get the app | low | default-recorded |
| D4 | Tone: arcade, warm, quick | medium: creative-direction repair | default-recorded |
| D5 | Audio design (music/SFX/VO or none) | medium: audio-layer repair only (audio is a separate layer in the assembly) | default-recorded (Stage 3) |
| D6 | The power-up is an arcade device, not a realistic firearm | medium: the customer said "gun sort of"; if they wanted a literal gun, a power-up redesign is a partial re-generation | default-recorded (Stage 3) |
| D7 | Exactly the five named obstacles; "and so on" is not expanded | low: 30 s cannot carry more than five clearly; the customer listed five | default-recorded |
| D8 | Which capability each obstacle maps to | low–medium: a wrong mapping is a label/transformation re-render (code-set) | default-recorded (Stage 2) |
| D9 | One master file serves all three platforms unless Stage 2 proves otherwise | low | default-recorded |
| D10 | Organic placement assumed | low (specs) / medium (policy) | default-recorded |

No decision is high-cost enough to require an ask, and asks are not available in this experiment.

---

## Generated job-specific questions (inverse form)

For each mandatory event and distinctive asset: what must the viewer perceive → observable property → controllable parameter → route → what breaks it → destination.

| id | Perceive | Observable property | Controllable parameter | Route | What breaks it | Destination |
|---|---|---|---|---|---|---|
| G1 (M1) | "This is a platform game" within 1 s | Side-scrolling ground line, tiled platforms, a HUD strip, a small sprite-scale character | World drawn as a parallax level; HUD composed by code; sprite scale ≤ 1/6 of frame height | code (level + HUD) + generated character/world art | A cinematic wide shot or a 3-D camera move; character too big (reads as a mascot ad) | frames 1–3; Stage 3 world design; Stage 4 method |
| G2 (M2) | "The player is a PG owner" | Identifiers legible at phone size: a bunch of keys, a rent register/ledger book, a "PG" nameplate on the level's first building, a HUD label | Character design brief with 2–3 fixed identifiers; a HUD name label by code | generated character still (identity anchor) + code label | A generic hero; identifiers too small at 9:16 phone size | frame 1–2; Stage 3 player identity; QA LJ M2 |
| G3 (M3) | Five obstacles = five named problems | Each obstacle has a distinct silhouette AND a code-set label ≤ 3 words | Obstacle designs (5 stills) + label strings in the copy deck | generated obstacle stills + code labels | Labels rendered by a model (misspelling); silhouettes too alike; more than one obstacle on screen without labels | frames 4–9; copy deck; QA DET C6 + LJ A3 |
| G4 (M4) | "Installing RentOK is the turning point" | A freeze/interrupt, a cheat-code card with the install string, a phone/app icon, a visible world change after it | Card composed by code at the midpoint; before/after palette shift; HUD state change | code + one generated "world after" plate | Placing the install too late (no time to clear five obstacles) or too early (no struggle) | frame ~10–12; brand timeline |
| G5 (M5) | "The character got a power" | A pickup event, a costume/aura change, a visible projectile | Power-up object design; character variant B (powered) as a second anchor still | generated character variant + code-drawn projectile | Character identity drift between variant A and B | frame ~12–13; Stage 4 risk order |
| G6 (M6) | "All five overcome, flag reached" | Each obstacle hit → transforms into a verified product outcome card; flag pole with brand flag | Transformation cards by code; obstacle "hit" states as stills | code (cards, projectile, hit flash) + generated stills | Running past labels that vanish (ChatGPT's own warning); a transformation that overclaims (FL2) | frames 13–24; Stage 2 claims table |
| G7 (M9) | "Original, not Nintendo" | No red cap/moustache plumber, no question blocks, pipes, mushrooms, koopa/goomba shapes, no Nintendo melody | Character/world design rules; prompt negative list; music brief | all generation prompts + Lyria brief | A model defaulting to Mario tropes when told "Mario-inspired" — the word "Mario" never enters a prompt | Stage 2 IP rules; prompt grep DET |
| G8 (brand) | "RentOK" exact | Byte-exact string in brand colour; wordmark on the end card | Copy deck string; hb-view render; end-card layout | code | A model drawing the name (misspelling); low-contrast colour on the game palette | copy deck; C2/C6 |
| G9 (M11) | Nothing overclaims | Copy deck strings only from the permitted list | Forbidden-word scan | code | A VO line or a card that says "never"/"100%" | A11 DET |

Deleted generated questions (informed no decision): "what score value the HUD shows" (any value works; cosmetic) · "how many lives at start" (the mechanic's count is a Stage 3 detail with no acceptance consequence; kept inside the storyboard, not as a question).

---

## Intent contract (v1)

**Explicit customer requirements (customer words quoted):** M1–M11 above, verbatim in column 2.

**Derived requirements (not customer words; follow from them):**
- R1 One 30.0-s vertical short-form file meeting current Reels/Shorts specs (from 1.1/1.8; specs at Stage 2).
- R2 Five obstacles, exactly the five named problems, each labelled (from M3 + D7).
- R3 The install event sits at the structural midpoint with a visible before/after (from M4).
- R4 Every product outcome shown after an obstacle is cleared is a permitted claim with a snapshot citation (from M11 + F4).
- R5 Exact strings (brand, cheat code, labels, CTA) composed by code (Controller RR-1 rule); any model-drawn text needs recorded justification + evidence + a post-draw text scan.
- R6 No Nintendo asset; the word "Mario" and Nintendo asset names never appear in any generation prompt (from M9).
- R7 The power-up is arcade-styled, not a realistic firearm (D6, FL3).

**Delegated decisions (customer: "Delegated to the creative system"):** visual treatment; power-up design (mechanic preserved); everything in 1.12.

**Unresolved information:** the confirmed spend cap (Controller, in writing). Nothing else blocks.

**Acceptance-critical ambiguities and how they are handled:** FL2 (clearing obstacles vs overclaiming) — handled by R4 + the F2 word scan + the closing line's wording. FL3 (gun) — handled by R7.

**Final deliverables:** `deliverables/rentok-lane-b-30s-9x16.mp4` (master, 1080×1920 expected from Stage 2, H.264/AAC, 30.0 s) + QA contact sheet + copy deck + claims citation table. Per-platform re-encodes only if Stage 2 demands.

**Verification method per mandatory item:** the table in 1.4 (every M-row carries one).

---

## Stage 1 exit criteria — self-assessment (the checker issues the gate verdict, not this session)

| Criterion | Self-assessment | Evidence |
|---|---|---|
| Nothing invented | met, to my knowledge | every customer requirement quotes the frozen brief; every fact about the site cites a snapshot line; platform specs are deferred to Stage 2 rather than asserted |
| Every mandatory item has a verification method | met | 1.4 table, 11 rows, each with a DET/LJ/HJ method and the acceptance item it serves |
| Every `ask` converted to `decide` with cost of being wrong | met | 1.12 D1–D10; the cap is the sole Controller-supplied item |
| The ChatGPT direction did not enter the contract | met | not cited anywhere above; Stage 3 interrogates it |
| Flags resolved or recorded | met | FL1–FL5; none blocks |
