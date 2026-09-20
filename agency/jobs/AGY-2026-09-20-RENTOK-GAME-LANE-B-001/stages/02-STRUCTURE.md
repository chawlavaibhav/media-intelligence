# Stage 2 — Structure and facts · AGY-2026-09-20-RENTOK-GAME-LANE-B-001 (lane B)

Author: lane-B producer session. Date: 2026-09-20. Cost: USD 0.
Gate rule for this stage: every fact has a source; nothing platform-specific is asserted from memory.

Sources fetched by this lane (all under `source/`, hashes in each folder's `SHA256SUMS.txt`, fetch times in `fetched_utc.txt`):

| id | URL | fetched UTC | sha256 (html) | note |
|---|---|---|---|---|
| S-IGR | https://www.facebook.com/business/ads-guide/update/video/instagram-reels (en_US) | 2026-09-20T18:18:49Z | 410aac1d…6084 | Meta "Awareness Video Ad Specs on Instagram Reels"; text extract `.txt` beside it |
| S-FBR | https://www.facebook.com/business/ads-guide/update/video/facebook-facebook-reels (en_US) | 2026-09-20T18:18:49Z | 3d739711…1860 | Meta "Ads on Facebook Reels" video specs |
| S-SZ | https://www.facebook.com/business/help/980593475366490/ (en_US) | 2026-09-20T18:18:49Z | 8c0dd9f4…9b33 | Meta "About text overlays and the safe zone for ads in Stories and Reels" (body is script-rendered; the sentences quoted below were pulled from the raw html) |
| S-YTS | https://support.google.com/youtube/answer/10059070 | 2026-09-20T18:16:56Z | d21bf111…6779 | "Get started creating YouTube Shorts" |
| S-YTE | https://support.google.com/youtube/answer/1722171 | 2026-09-20T18:16:56Z | e20542aa…171d | "YouTube recommended upload encoding settings" |
| S-YTF | https://support.google.com/youtube/answer/71673 | 2026-09-20T18:16:56Z | e385c3cd…8197 | YouTube maximum upload size |
| S-YTA | https://support.google.com/google-ads/answer/16041697 | 2026-09-20T18:19:23Z | 1ae5ecbb…c702 | "YouTube Shorts ads: Asset specs and best practices" (Google Ads Help) |
| S-YTX | https://support.google.com/youtube/answer/16215842 (Android) | 2026-09-20T18:19:23Z | 77254acc…e982 | "Enhance your Shorts" — the Shorts editor's non-safe-area guides |
| S-LOGO | https://rentok-storage-cdn.azureedge.net/rentok-marketplace/marketplace-dump/landing-page-vectors/rentok-new-logo.webp | 2026-09-20T18:19:42Z | 1ff7dcf5…6f80 (webp) | the wordmark referenced by `home.html` and `autopay.html` |
| SNAP | `source/rentok-snapshot/` (Controller-fetched 2026-09-20T18:00:45Z) | — | see its SHA256SUMS.txt | product-fact source of record; cited as `<page>.txt L<n>` |

Meta pages refused the browser user-agent (HTTP 400) and served the plain `curl/8.4.0` agent; the first fetch without `locale=en_US` came back in Hindi, so the English pages were re-fetched and the Hindi copies discarded. OBSERVED.

---

## 2.1 — Exact pixel dimensions, duration limits, file specs per placement

| | |
|---|---|
| Why it matters | A7/A8 are DET checks against these numbers; the master file is encoded to them. |
| Class / priority | DET / blocks |
| Source | lookup-fact (S-IGR, S-FBR, S-YTS, S-YTE, S-YTF, S-YTA) |

Retrieved evidence (verbatim lines):

- S-IGR: "File Type: MP4, MOV" · "Ratio: 9:16" · "Video Settings: H.264 compression, square pixels, fixed frame rate, progressive scan and stereo AAC audio compression at 128kbps+" · "Resolution: 1440 x 2560 pixels" · "Video Duration: 0 seconds to 15 minutes" · "Maximum File Size: 4GB" · "Minimum Width: 250 pixels for ads less than 30 seconds; 500 pixels for ads 30 seconds or longer" · "Reels ads should not contain: … Videos that contain edit lists or special boxes in file containers."
- S-FBR: "File Type: MP4, MOV, GIF" · "Recommended Ratio: 9:16" · "Resolution: 1440 x 2560 pixels" · "Video Duration: No maximum limit." · "Maximum File Size: 4GB" · same video settings line.
- S-YTS: "short-form videos that are up to 3 minutes long" · "You can upload vertical videos saved to your computer or smartphone as Shorts." · "Note: You can upload Short videos with a maximum resolution of 1080p."
- S-YTA: "Vertical videos, with a 9:16 aspect ratio, are best suited for the Shorts format" · "Video ads can be up to 3 minutes long, though only the first 60 seconds will play on the Shorts feed" · "For action-oriented ads, use 10-30 second vertical videos."
- S-YTE: "Container: MP4 · No Edit Lists · moov atom at the front of the file (Fast Start) · Audio codec: AAC-LC … · Sample rate: 48kHz · Video codec: H.264 · Progressive scan · High Profile · Closed GOP. GOP of half the frame rate · Chroma subsampling: 4:2:0" · "1080p 8 Mbps (standard frame rate)" · "Common frame rates include: 24, 25, 30, 48, 50, 60".
- S-YTF: "The maximum file size you can upload is 256 GB or 12 hours, whichever is less."

Answer → `spec.formats[]` (one master satisfies all three placements):

| field | value | why |
|---|---|---|
| aspect | 9:16 | S-IGR "Ratio: 9:16"; S-FBR; S-YTA |
| pixels | **1080×1920** master | Meta lists 1440×2560 as the spec page's resolution line and a 500-px minimum width for ≥ 30-s ads; YouTube caps Shorts uploads at 1080p (S-YTS). 1080×1920 satisfies every stated minimum and the YouTube maximum; it is the acceptance contract's expected geometry (A8). DECIDED: one 1080×1920 master; a 1440×2560 upscale is not made (it would be a silent upscale of 1080-class generated material, QA B5). |
| container / codecs | MP4, H.264 High profile, progressive, 4:2:0, moov atom first (faststart), no edit lists; AAC-LC stereo ≥ 128 kbps at 48 kHz | S-YTE + S-IGR ("H.264 … stereo AAC … 128kbps+"; "no edit lists") |
| frame rate | 30 fps constant (fixed) | S-IGR "fixed frame rate"; S-YTE lists 30 among common rates; every generated clip is conformed to 30 fps by code |
| duration | 30.0 s (A7: 29.5–30.5) | customer; inside Meta 0 s–15 min and YouTube ≤ 3 min |
| bitrate | ≈ 8–10 Mbps video | S-YTE 1080p standard-rate recommendation 8 Mbps |
| file size | ≪ 4 GB | S-IGR/S-FBR 4 GB cap |
| DET check | `ffprobe -show_streams -show_format`: width 1080, height 1920, codec h264, profile High, pix_fmt yuv420p, r_frame_rate 30/1, audio aac 48000 Hz 2 ch, duration 29.5–30.5 s; `moov` before `mdat` (check with `ffprobe -v trace` or a byte scan) | Stage 4 QA plan item Q-A7/Q-A8 |

## 2.2 — Safe zones / UI-occluded bands

| | |
|---|---|
| Why it matters | Every critical text (labels, cheat code, brand, CTA) and the hero action must sit inside the zone or the film fails A8's LJ half. It also shapes the level layout (where the ground line goes). |
| Class / priority | DET / blocks |
| Source | lookup-fact (S-IGR, S-SZ) + decide (YouTube has no published percentage) |

Retrieved evidence:
- S-IGR (verbatim): "Consider leaving at least 14% of the top, 35% of the bottom, and 6% on each side of your asset free from text, logos, or other important creative elements. This will help ensure that key parts of your design are not cropped, covered by the profile icon or call-to-action, or placed too close to the edges of devices with screens taller than a 9:16 aspect ratio."
- S-SZ (verbatim): "The safe zone refers to the area within your ad where important elements — like text overlays and logos — will not be cropped out or covered by the user interface." · "9:16 video ads in Instagram Feed use the same safe zone guidance as Reels and Stories." · "On devices with screens that are taller than the 9:16 aspect ratio, we may either zoom the creative to better fill the whole screen (which can crop areas outside the safe zone), or show the creative in its original 9:16 aspect ratio and use a black background to fill any extra space."
- S-YTX (verbatim): "If you drag an overlay too close to the edge of the screen, animated white lines will appear, signaling a 'non-safe' area where your content might be partially hidden on some devices. Icons will also display if you place an overlay where viewer elements like the like button might appear." — YouTube publishes the guides inside its editor, not as numbers. No numeric YouTube Shorts safe zone was found in official documentation (searched support.google.com; UNKNOWN whether one exists elsewhere).

Answer → `spec.safe_zones[]` on the 1080×1920 master:

| zone | pixels | status |
|---|---|---|
| Meta critical-content safe box | x 65–1015, y 269–1248 (top 14% = 269 px; bottom 35% = 672 px; sides 6% = 65 px) → **950 × 979 px** | SOURCE-SUPPORTED (S-IGR) |
| YouTube Shorts | no published numbers; the Meta box is adopted as the stricter documented rule. On top of it, DECIDED: no critical text in the right-hand 12% of width (x > 950) within the lower half (y > 960), where the Shorts editor's own guides flag viewer-element positions (S-YTX names the like button; positions are not documented numerically) | INFERRED + decided (cost of being wrong: a label re-position by code, USD 0) |
| Design consequence | The game's action band (ground line, character, obstacles, labels, HUD) lives inside y 269–1248. Below y ≈ 1250 only non-critical ground/soil/foreground texture; above y ≈ 269 only sky/parallax. The end card's wordmark and CTA sit inside the box. | decided |
| DET check | `check_text_bounds`-style code check of every code-set text box against the safe box (Stage 4 tool `safe_zone_check.py` over the copy-deck layout table); LJ: checker views the final file with a 14/35/6 overlay (contact sheet with the box drawn) | Stage 4 |

## 2.3 — Ad structure for this placement (hook window, brand-early, ask placement, close-on-product)

| | |
|---|---|
| Why it matters | Sets where the brand first appears, how the ask is carried, and what the last frame is; Stage 3's brand timeline and CTA follow it. |
| Class / priority | RSR / default-recorded |
| Source | lookup-canon (retrieved claim text saved to `stages/evidence/canon-claims-named-by-template.txt`) + lookup-fact (S-YTA) |

Retrieved evidence (claim text, by id, from `canon/knowledge/current/**/source-knowledge.yaml`):
- sk_abcd_0006 (Jump in): "reach the heart of its story sooner … pacing that keeps the viewer engaged, and tight framing." Caveat: no target time is given.
- sk_abcd_0007: "beginning in the middle of the action, and opening on a close-up … not a required opening."
- sk_abcd_0010 / 0011: brand "early, often, richly"; "an early appearance that then lapses does not satisfy it." Caveat: unquantified; platform-contingent (YouTube).
- sk_abcd_0012 / 0013: audio brand mention reinforces the on-screen mark; the list of branding assets includes "graphic elements, voice-overs and musical treatments".
- sk_abcd_0019 / 0020 / 0021: ask for action with a clear, simple instruction; the CTA tied to a specific objective; on-screen CTA paired with a voice-over saying the same thing (premise: audio heard).
- sk_abcd_0026 (full-funnel): "Branding is to start with a mix of branding elements and finish with the product. Direction is to use calls to action throughout the ad and to become more direct as it proceeds."
- sk_ogx_0039 (Ogilvy): "use the name within the first ten seconds … Commercials that end by showing the package are reported more effective." Scope: television commercials of the period.
- S-YTA (platform fact): "only the first 60 seconds will play on the Shorts feed"; "For action-oriented ads, use 10-30 second vertical videos."

Answer → `spec.ad_structure`:
- Hook: open inside the action (the game already running, close on the player) — sk_abcd_0007; no title-card preamble longer than ~1 s.
- Brand-early: the brand name is on screen within the first 5 s as a game element (HUD label / level sign) and recurs — sk_abcd_0010/0011, sk_ogx_0039 (name inside 10 s). The install event at the midpoint is the richest branding beat; the end card is the product close (sk_abcd_0026, sk_ogx_0039 "end by showing the package" → the wordmark + app icon).
- Ask: carried by the story itself first (the cheat code IS the ask: install the app — sk_abcd_0019 "a scene from the story itself"), then explicit and more direct on the end card (sk_abcd_0026 escalation). If a voice exists it says the CTA words (sk_abcd_0021); if not, the muted structure must carry it alone (the source's premise of heard audio does not hold on Reels, where sound is optional — S-IGR "Video Sound: Optional").
- Last frame: wordmark + CTA + app icon, held ≥ 2 s.

## 2.4 — Permitted claims, verified against the frozen snapshot

| | |
|---|---|
| Why it matters | A11 (DET string scan + LJ) and D (factual accuracy) are checked against exactly this table. Every product capability shown after an obstacle is cleared must be a row here. |
| Class / priority | DET / blocks |
| Source | lookup-fact (SNAP) |

### (b) The five customer-named problems — what the site demonstrably offers

| # | Customer's problem (verbatim) | What the site demonstrably offers (quoted line + citation) | Claims that would be UNSUPPORTED or FORBIDDEN |
|---|---|---|---|
| P1 | "tenant verification" | "Tenant Verification / Verify tenants quickly and securely" (home.txt L17–18) · "Digital KYC & Verify or Reject Tenant's Documents & Govt. IDs" (home L99) · "Tenant gets WhatsApp link. Uploads Aadhaar, photo, signs digital agreement on their phone." (tenant-verification.txt L49) · "We Handle Police Verification / 48-72 hours / We submit to local police station. No follow-ups needed from you. Status updates automatically." (tv L51–53) · "Tenant Verification Status / Real-time verification tracking for all tenants" (tv L59–60) · status columns "KYC / Agreement / Police Verification / Overall Status" with values "Completed / Verified / Pending" (tv L63–75) | "instant verification" (police step is 48–72 h, tv L52); "RentOk makes tenants trustworthy/safe"; "no bad tenants"; any guarantee wording |
| P2 | "collecting rent" | "Autopay / Collect rent automatically every month" (home L19–20) · "Rent Collection. Now Fully Automatic." (autopay.txt L4–5) · "Autopay works like SIP/EMI-money moves to your account automatically." (autopay L9) · "Set the date (1st, 5th, 10th, etc). Money moves to your account. You get instant notification." (autopay L59) · "Automatic payment reminders on WhatsApp, SMS & Notification" (home L86) · "One-click Bulk WhatsApp reminder with Payment Link" (home L87) · "Automatic Late Fine addition after the grace period" (home L88) | "rent is guaranteed"; "100% collection" (the site's own "100% Automatic Rent & Due Collection. 5 days max!" home L83 and "95%+ success rate" autopay L39 are the site's marketing statistics — DECIDED not to use any percentage/statistic in the film, because a number on screen becomes a claim the customer forbade in spirit and A11 scans for); "always paid on time" |
| P3 | "tenants leaving without paying rent" | Dues are visible per tenant: columns "Rent Amount / Dues" and "Pending Dues" (autopay L116–117, L136) · "Excel Reports of Dues, Income, Expense, Lead, Tenant, Profit-Loss" (home L92) · "Payment History to Tenant Ledger" (home L96) · "Real-time update of filled, vacant, under notice rooms & beds" (home L104) · "Autopay automatically retries for 3 consecutive days. You get instant notifications for failures, so you only follow up with specific tenants." (autopay L232) · "Tenants with Autopay enabled show ₹0 dues." (autopay L149, a site statement about enabled tenants) | **Forbidden by the customer**: anything implying RentOk "prevents tenants from leaving" or "guarantees rent recovery". The Zero-Deposit/Eqaro insurance block ("Get 100% Claim whenever a tenant breaks your rent agreement / Powered by Eqaro Guarantees", home L109–115) is a third-party product with conditions and is **not depicted** (it is exactly a recovery-guarantee claim). The site's own "Timely issue resolution prevents tenants from leaving" (complaint-management.txt L177) is likewise not used. Permitted depiction: the owner can SEE who owes what, and is notified of failed collections — knowledge, not recovery |
| P4 | "no place to do reconciliation" | "24/7 Digital Accountant at your fingertips" (home L89) · "✅ Accounting Done ✅ Reports Done +7 more reports" (home L90) · "Real-time transaction updates on App & WhatsApp" (home L91) · "Excel Reports of Dues, Income, Expense, Lead, Tenant, Profit-Loss" (home L92) · "UTR no. directly in the app. No need to check the bank account" (home L94) · "One page shows who paid" (autopay L36) · "Rent Collection Summary" (autopay L110) | "your accounts are always correct"; "no accountant needed" (the site says "Digital Accountant", not "replaces your CA" — it also sells "CA & Accounting Services", home L29–30) |
| P5 | "solving complaints" | "Complaint Management / Track and resolve tenant complaints efficiently" (home L15–16) · "Tenants raise tickets from their app. Complaints auto-appear on your dashboard. Track, assign, and resolve - without a single phone call." (complaint-management.txt L10) · "Ticket auto-appears on dashboard / Auto-assigned to team member / Priority & urgency flagged" (cm L71–73) · "Resolve & Mark Complete … marks the ticket as resolved" (cm L75–76) · "Resolved status shown in Tenant App" (cm L83) | "no complaints"; "complaints solved instantly"; "1 day avg resolution" (site statistic, cm L204 — not used, same rule as P2); "happier tenants, longer stays" implies retention → not used |

### `spec.permitted_claims[]` — the only product strings allowed on screen or in voice (each a short game-style label; Stage 3 picks from these; anything else is a Stage 2 re-open)

| id | on-screen string (exact, caps) | plain meaning | citation |
|---|---|---|---|
| PC1a | `VERIFICATION TRACKED` | the app tracks each tenant's verification status | tv L59–60 |
| PC1b | `KYC: DONE` | digital KYC of documents/IDs | home L99; tv L63 |
| PC1c | `POLICE VERIFICATION: SUBMITTED` | RentOk submits to the police station and shows status | tv L51–53, L65 |
| PC1d | `TENANT: VERIFIED` | overall status value shown on the site's status table | tv L66–70 |
| PC2a | `AUTOPAY: ON` | automatic rent collection enabled | home L19–20; autopay L4–5 |
| PC2b | `RENT COLLECTED AUTOMATICALLY` | money moves on the set date | autopay L9, L59 |
| PC2c | `REMINDER SENT ON WHATSAPP` | automatic payment reminders | home L86–87 |
| PC3a | `DUES VISIBLE` | per-tenant dues shown | autopay L117, L136; home L92 |
| PC3b | `TENANT LEDGER` | payment history per tenant | home L96 |
| PC3c | `PENDING DUES: FLAGGED` | failures/dues notified so the owner follows up with specific tenants | autopay L232, L136 |
| PC3d | `UNDER NOTICE: TRACKED` | notice status of rooms/beds tracked | home L104 |
| PC4a | `REPORTS: DONE` | accounting and reports done in the app | home L90 |
| PC4b | `ONE PAGE: WHO PAID` | collection summary on one page | autopay L36, L110 |
| PC4c | `UTR IN APP` | bank transaction reference visible in the app | home L94 |
| PC4d | `INCOME · EXPENSE · P&L` | report types | home L92 |
| PC5a | `TICKET RAISED` | tenant raises a complaint ticket in their app | cm L61–62, L71 |
| PC5b | `ASSIGNED TO TEAM` | auto-assigned to a team member | cm L72, L49 |
| PC5c | `RESOLVED` | marked resolved; status shown to the tenant | cm L75–76, L83 |
| PC6a | `Get the app` (end-card CTA, sentence case allowed) | the site's own CTA | home L140 |
| PC6b | `India's renting superapp` | the wordmark tagline | S-LOGO; tv L154 |
| PC6c | `PG / Hostel / Flat Management App` | the site's own descriptor | home L1 |
| PC7 | `INSTALL RENTOK` / `INSTALL RENTOK APP` (the cheat code; not a product claim) | customer's words | brief |

### Forbidden-claims list (A11 DET scan over the copy deck + any VO transcript; case-insensitive; substring)

`guarantee`, `guaranteed`, `never`, `always`, `100%`, `zero dues`, `zero problems`, `no problems`, `all problems`, `every problem`, `no more`, `can't leave`, `cannot leave`, `won't leave`, `stop(s) tenants`, `prevent(s)`, `recover`, `recovery`, `insured`, `insurance`, `claim`, `instantly verified`, `instant verification`, `safe tenants`, `trusted tenants`, any `%`, any `X faster`, any rupee amount presented as a saving, and the word `Eqaro`.
Also forbidden by governance: any tool or model name (QA E3); the word `Mario` or any Nintendo name on screen or in prompts (2.5 below).

### Check of the ChatGPT direction's five capability depictions (task requirement)

| ChatGPT depiction | Verdict | Basis |
|---|---|---|
| "completed verification record" | SUPPORTED | tv L59–60 status tracking; L69–70 "Completed / Verified"; L141–142 "Lifetime Dashboard Access / Show verification status anytime" |
| "payment reminder or tracked due" | SUPPORTED | home L86–87 reminders; autopay L117/L136 dues |
| "visible outstanding dues" | SUPPORTED | autopay L117, L136; home L92, L96 |
| "organized report" | SUPPORTED | home L90, L92; autopay L110 |
| "tracked service ticket" | SUPPORTED | cm L10, L61, L71–73 |

All five hold as capabilities. What the direction does NOT say, and the film must also not say, is any recovery/retention outcome for the unpaid-exit obstacle — the transformation must stop at "dues visible / flagged".

## 2.5 — IP: original Mario-inspired, made concrete

| | |
|---|---|
| Why it matters | A9 (LJ) + a DET grep over prompts; a Nintendo look-alike is a rejection and a legal exposure for the customer. |
| Class / priority | DET+LJ / blocks |
| Source | derive (customer's confirmed answer: "An original Mario-inspired game, rather than an exact reproduction of Nintendo's character, artwork, music or game assets.") |

What "Mario-inspired" may keep (the genre, which is not owned): a 2-D side-scrolling platform level; a small player sprite who runs and jumps; ground tiles, floating platforms, a distant sky/hill parallax; enemies/obstacles that are hit or jumped; a heart/lives HUD, a score counter, a level label; a power-up pickup that changes the character; a flag on a pole at the level's end; chiptune-style music.

DO NOT (character): no red cap with a letter, no blue overalls with buttons, no moustache-plumber, no "M"/"L" initials, no white gloves on a small figure, no overall-and-cap silhouette in any colour. The player is a PG owner in Indian everyday dress (design at Stage 3).
DO NOT (world): no question-mark blocks, no brick-block rows, no green warp pipes, no mushrooms of any kind, no turtle/koopa or brown mushroom-goomba shapes, no piranha plants, no coins with a "?" or the Mario coin sound, no castle-at-the-end, no Nintendo-style striped flagpole ball; no title in a Nintendo typeface.
DO NOT (sound): no Nintendo melody, jingle, coin/jump/1-up sound; music is an original chiptune bed generated for this job; SFX are synthesised by code (Stage 4).
DO NOT (words): the word "Mario", "Nintendo", "Super", "Luigi", "Bowser", "Peach", "Koopa", "Goomba", "Mushroom Kingdom" never appear in any generation prompt, on screen, in filenames or in the music brief. DET: grep over all prompts and the copy deck before dispatch.
DO (originality anchors): the world is a PG street (Indian low-rise buildings, a "PG" nameplate, a scooter, a water tank), the obstacles are PG problems drawn as original creatures/objects, the flag carries the RentOk mark, the character's identifiers are keys + a rent register.

Cost of being wrong: a generated still that drifts towards Nintendo tropes is rejected at the micro-qualification (Stage 4) before dependents are built.

## 2.6 — Sound: muted-first? captions? loudness

| | |
|---|---|
| Why it matters | Decides whether the story must work silent (it must), whether VO is worth its cost, and the loudness target for QA D11. |
| Class / priority | DET / default-recorded |
| Source | lookup-fact (S-IGR, S-YTA) + decide |

Evidence: S-IGR "Video Captions: Optional, but recommended" · "Video Sound: Optional, but strongly recommended" · "Reels ads should not contain: … Licensed music. We recommend using original audio or royalty-free music". S-YTA: "Use sound (music, voiceover, or both) in your Shorts ads, which has been shown to increase conversions by over 20%. Also, consider using text overlays." (a platform performance claim; not verified here). Neither page states a loudness target (UNKNOWN from official docs).

Answer → `spec.audio`: muted-first structure (every mandatory event readable with sound off — Stage 3 muted test); sound present (original music bed + synthesised SFX; VO decided at Stage 3 on cost/benefit); no licensed music (Lyria output is original, RR-13); loudness target DECIDED as integrated −14 LUFS ±1, true peak ≤ −1 dBTP (a common streaming delivery level; not a platform rule — recorded as our own target for QA D11, cost of being wrong: a re-normalise by ffmpeg `loudnorm`, USD 0).

## 2.7 — Per-format composition

| | |
|---|---|
| Why it matters | FORMAT_SPECIFIC_REVALIDATION: each delivered geometry needs its own QA row. |
| Class / priority | DET / default-recorded |
| Source | derive from 2.1/2.2 |
| Answer | One geometry (9:16, 1080×1920) serves all three placements, so `spec.per_format_composition = false` for geometry — proven by 2.1 (all three accept 9:16 MP4 H.264/AAC). One delivered file → one `qa.final_geometry` row. If the customer later wants a 1:1 or 16:9 cut, that is a new composition with its own QA, not a crop. |

## 2.8 — Sufficient to proceed?

Yes. Every fact above has a source; the one dependency that blocks spend (the confirmed cap) does not block Stage 3.

## (d) Brand assets — what we have, what we originate

| asset | status | detail |
|---|---|---|
| Wordmark `RentOk` | HAVE (S-LOGO, 5988×3072 webp, RGBA; preview `source/brand/rentok-new-logo.preview.png`) | "Rent" in white on a blue rounded panel, "Ok" in cyan, tagline "India's renting superapp" in yellow. Sampled colours (OBSERVED from the file): panel blue `#0239FF`–`#012BEA` (site `theme-color` `#0038FF`, home.html), white `#FFFFFF`, cyan `#03FFF1`, yellow `#FCF000`. Secondary site colour: green `#30B502` (22 occurrences in home.html). |
| Brand spelling on screen | **DECIDED: `RentOk`** in mixed case wherever the wordmark or a mixed-case string appears; in all-caps game text the string is `RENTOK` (case-neutral, so the customer's "RentOK" and the site's "RentOk" agree). Reason: every page title and the wordmark spell it "RentOk" (home L1, L63; tv L152; cm L102; S-LOGO); the customer's "RentOK" is a casing variant of the same name, and the on-screen mark must match the brand's own asset. Cost of being wrong: a code re-render of the end card, USD 0. |
| App icon | ORIGINATE | no icon file in the snapshot; an original in-game icon (blue rounded square, white "R"-free — a simple key+house pictogram with the RENTOK label set by code) is drawn by code at Stage 4. Not a claim. |
| App / dashboard screens | NOT USED as visuals | the snapshot's dashboard text is claims evidence only; the film shows game-world "transformation cards", not UI reproductions. |
| Character, world, obstacles, power-up, flag | ORIGINATE | Stage 3 design, Stage 4 generation. |
| Fonts | code-set: a pixel/arcade-style Latin face for in-game text is needed. OBSERVED on this Mac (reference kit): Helvetica Neue, Avenir, Futura, Gill Sans, D-DIN; no pixel font listed. Stage 4 either uses a bold condensed system face rendered at low resolution and nearest-neighbour upscaled (a deterministic pixel look, USD 0) or records a font fetch (open-licence) with URL/sha. Decided at Stage 4. |

## Stage 2 exit criteria — self-assessment (the checker issues the verdict)

| Criterion | Self-assessment | Evidence |
|---|---|---|
| Every fact has a source | met | every platform number quotes S-* with sha256; every product line cites `<page>.txt L<n>` |
| Nothing platform-specific asserted from memory | met, with two declared decisions | YouTube safe-zone percentage (none published — decided to adopt Meta's + a right-edge margin) and the loudness target (no official figure — decided) are labelled INFERRED/decided, not fact |
| Permitted / forbidden claims built | met | PC1a–PC7; forbidden list; the five ChatGPT depictions verified |
| IP resolved into do/don't | met | 2.5 |
| Brand assets: have / originate | met | (d) |
