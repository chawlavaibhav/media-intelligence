# Stage 2 — Structure and facts (gate: every fact has a source; nothing platform-specific asserted from memory)

Job `AGY-2026-09-20-RENTOK-GAME-LANE-A-001`. Template lines 2.1–2.8 plus the four Controller-named sections (a) publishing spec · (b) product facts · (c) IP · (d) brand assets.
Evidence files added by this stage: `source/platform/*` (`SHA256SUMS.txt`, `fetched_utc.txt`) and `source/rentok-brand/*` (`SHA256SUMS.txt`, `fetched_utc.txt`). Line numbers below refer to the `.txt` extracts in `source/rentok-snapshot/` (fetched by the Controller 2026-09-20T18:00:45Z; the `.html` is the evidence, hashes in that folder's `SHA256SUMS.txt`).

---

## (a) Publishing specification

### 2.1 Exact pixel dimensions, duration limits, file specs per placement

- Why it matters: A7/A8 measure the delivered file against these numbers; the encode command is written from them.
- Class/priority: DET · blocks. Source: **lookup-fact** (official pages, fetched today).
- Retrieved evidence (verbatim):
  - Instagram Reels (Meta Ads Guide, `source/platform/ig-reels-ads-guide.txt`, fetched 2026-09-20T18:17Z): "File Type: MP4, MOV" · "Ratio: 9:16" · "Video Settings: H.264 compression, square pixels, fixed frame rate, progressive scan and stereo AAC audio compression at 128kbps+" · "Resolution: 1440 x 2560 pixels" · "Video Duration: 0 seconds to 15 minutes" · "Maximum File Size: 4GB" · "Minimum Width: 250 pixels for ads less than 30 seconds; 500 pixels for ads 30 seconds or longer" · "Videos that contain edit lists or special boxes in file containers" (must not contain).
  - Facebook Reels (Meta Ads Guide, `source/platform/fb-reels-ads-guide.txt`, fetched 2026-09-20T18:19Z): "File Type: MP4, MOV, GIF" · "Recommended Ratio: 9:16" · same video settings line · "Resolution: 1440 x 2560 pixels" · "Video Duration: No maximum limit." · "Maximum File Size: 4GB" · "Videos should not contain edit lists in file containers."
  - YouTube Shorts (`source/platform/yt-shorts-basics.txt`, https://support.google.com/youtube/answer/10059070, fetched 2026-09-20T18:14:55Z, sha256 `aec4c6ae…`): "short-form videos that are up to 3 minutes long" · "upload vertical videos" · "You can upload Short videos with a maximum resolution of 1080p."
  - YouTube encoding (`source/platform/yt-upload-encoding.txt`, https://support.google.com/youtube/answer/1722171, sha256 `8999a32d…`): "Container: MP4" · "No Edit Lists (or the video might not get processed correctly)" · "moov atom at the front of the file (Fast Start)" · "Audio codec: AAC-LC or Opus or Eclipsa Audio" · "Sample rate: 48kHz" · "Video codec: H.264" · "Progressive scan (no interlacing)" · "High Profile" · "Chroma subsampling: 4:2:0" · "Common frame rates include: 24, 25, 30, 48, 50, 60" · 1080p recommended bitrate "8 Mbps" (standard frame rate) · audio "Stereo 384 kbps" (recommended), "Mono 128 kbps".
- Observed limitation: Meta serves the ads-guide only to a browser session (curl → HTTP 400/404); the two Meta extracts are the rendered page text copied verbatim via the browser pane, with URL and UTC recorded; their html could not be saved, so their sha256 is of the text file, not the page. The Meta pages are the *ads* guide; Meta publishes no separate organic-Reels spec page that this session could fetch. YouTube's pages are saved as html with sha256.
- Answer → `spec.formats[]` (one file serves all three placements):

| Field | Value | Basis |
|---|---|---|
| aspect | 9:16 | all three sources |
| pixels | **1080×1920** | YouTube "maximum resolution of 1080p"; Meta's 1440×2560 is a recommendation above YouTube's cap; the acceptance contract A8 fixes 1080×1920; width ≥ 500 px satisfied |
| container | MP4, moov atom first (`-movflags +faststart`), no edit lists | YouTube + Meta |
| video codec | H.264 High profile, progressive, 4:2:0, fixed frame rate **30 fps**, VBR ≈ 8–10 Mbps | YouTube encoding page; Meta "fixed frame rate, progressive scan" |
| audio codec | AAC-LC stereo, **48 kHz**, **192 kbps** (≥ Meta 128 kbps+; ≤ YouTube's 384 recommended) | both |
| duration | 30.0 s (A7 29.5–30.5) — inside IG 0 s–15 min, FB no max, YouTube Shorts ≤ 3 min | all |
| file size | ≪ 4 GB (≈ 35 MB at 9 Mbps × 30 s) | Meta |

- Decision: encode once with ffmpeg to the row above; DET check = ffprobe fields (width, height, codec_name, profile, r_frame_rate, pix_fmt, sample_rate, channels, duration) plus a moov-position check.

### 2.2 Safe zones / UI-occluded bands per placement

- Why it matters: every label, HUD element and the CTA must sit where platform UI cannot cover it (A8 LJ, CF4).
- Class/priority: DET · blocks. Source: **lookup-fact**.
- Retrieved evidence (verbatim):
  - Instagram Reels: "Consider leaving at least 14% of the top, 35% of the bottom, and 6% on each side of your asset free from text, logos, or other important creative elements. This will help ensure that key parts of your design are not cropped, covered by the profile icon or call-to-action, or placed too close to the edges of devices with screens taller than a 9:16 aspect ratio."
  - Facebook Reels: "Consider leaving roughly 14% of the top, 35% of the bottom, and 6% on each side of your asset free from text, logos, or other key creative elements".
  - YouTube (Google Ads help, `source/platform/yt-vertical-safe-area.txt`, https://support.google.com/google-ads/answer/9128498, sha256 in `SHA256SUMS.txt`, fetched 2026-09-20T18:18:16Z): "Safe zones for vertical video ads on YouTube … Use this image as a reference to ensure important elements like your logo, product, supers, and others are within the red safe area". The referenced figure (`yt-vertical-safe-area-figure.svg`, saved and hashed) is labelled "Resolution 1080x1920", "Dimensions in pixels", with margins **288** (top), **672** (bottom), **48** (left), **192** (right) around the red "Safe Zone" rectangle. YouTube publishes no separate organic-Shorts safe-zone page that this session could find on support.google.com; the ads figure is the only official pixel figure and is used as the conservative bound.
- Answer → `spec.safe_zones[]` at 1080×1920:

| Placement | Top | Bottom | Left | Right | Safe box (x0,y0)–(x1,y1) |
|---|---|---|---|---|---|
| Instagram / Facebook Reels (14 % / 35 % / 6 %) | 269 px | 672 px | 65 px | 65 px | (65,269)–(1015,1248) |
| YouTube vertical (figure) | 288 px | 672 px | 48 px | 192 px | (48,288)–(888,1248) |
| **Intersection — the job's critical-element box** | **288** | **672** | **65** | **192** | **(65,288)–(888,1248)** = 823 × 960 px |

- Decision: all exact text, the HUD, the wordmark, the CTA and the player character's resting position sit inside (65,288)–(888,1248). Background world art fills the full 1080×1920 (it may be covered). DET check: every text/logo box from the compositor's layout log is inside that rectangle (`check_safe_zone`, a job tool over `runtime/compositor/gates.check_text_bounds` with the safe box as the container).
- Consequence for design (F4 from Stage 1): the playable band is ≈ 823 px wide by 960 px tall — a near-square window in the middle of the phone. The level scrolls horizontally through this window; the HUD lives at its top edge (y ≈ 300–380), the ground line at y ≈ 1130, the CTA card inside the bottom of the box.

### 2.3 Ad structure for this placement (hook window, brand-early, ask, close-on-brand)

- Why it matters: decides where the brand first appears, when the install ask lands and what the last frame is (3.4–3.6).
- Class/priority: RSR · default-recorded. Source: **lookup-canon** (retrieval done at Stage 3, where the claim texts are quoted by id) + **lookup-fact** for the placement.
- Platform facts: Reels and Shorts are full-screen, vertically scrolled, skippable ("people can comment, like, view, save, share and skip ads" — IG extract); captions and sound are "Optional, but recommended / strongly recommended" — so the film must work muted (2.6).
- Answer: hook inside the first ≈ 2 s (a game already in motion, not a title card); brand present early through the game's own HUD (a small "RentOk"-coloured element is *not* enough — the brand must be nameable by ≈ 8–10 s per the Canon claims retrieved at 3.4); the ask ("INSTALL RENTOK APP") is the mid-film turning point (customer-mandated); the last frame is the wordmark + CTA (close-on-brand). Confirmed or amended by the Canon retrieval at Stage 3.

### 2.6 Sound: muted-first? captions? loudness target?

- Class/priority: DET · default-recorded. Source: **lookup-fact** + **decide**.
- Evidence: Meta "Video Captions: Optional, but recommended", "Video Sound: Optional, but strongly recommended" (both extracts); "Licensed music. We recommend using original audio or royalty-free music" (IG extract, under "should not contain"). YouTube pages fetched state no loudness target. No fetched page states a loudness number.
- Answer → `spec.audio`: muted-first = **yes** (every beat carries its meaning in picture + on-screen label; no information exists only in sound). Music = original generated instrumental (Lyria, MUS/lyria+native clean 4/4, USD 0.06) — satisfies "original audio"; SFX = synthesised by code (ffmpeg tone generators) — no licensed sample. Captions = not applicable (no speech by default; if Stage 3 adds a VO line, its text is on screen byte-identical, 3.8). Loudness target = **decide**: −14 LUFS integrated, true peak ≤ −1 dBTP, measured with `ffmpeg -af ebur128` (no platform number was retrievable; this is the recorded default, class DET at 5.5). Known risk with a source id: Lyria refused a frozen prompt three times on wording (case UPWORK-INTRO-001 RO-09, SD-10, n=4) — prompt wording kept neutral; a refusal is `infrastructure_transient`, counted, never retried silently.

### 2.7 Must each delivered format be composed separately?

- Source: derive from 2.1/2.2. Answer: **one** delivered geometry (9:16, 1080×1920) serves all three placements; the safe-zone intersection is used for composition, so no per-placement composition is needed. `spec.per_format_composition = false` — proven by 2.2's intersection, not assumed. FORMAT_SPECIFIC_REVALIDATION still applies to the one delivered file (its own `qa.final_geometry` row).

---

## (b) Product facts — what the site demonstrably offers for each of the five customer-named problems

### 2.4 Which claims may be made, against which source

- Why it matters: A11 (DET string scan + LJ) and §D factual accuracy; every obstacle's "cleared by" label must be a supported capability.
- Class/priority: DET · blocks. Source: **lookup-fact** (frozen snapshot only; no further page was needed).
- Rule adopted for this job (decide, cost of wrong = a label re-render at USD 0): on-screen copy names **features**, never numbers, percentages, guarantees or outcomes. The site itself prints figures ("100% Automatic Rent & Due Collection", "98% On-time payment rate", "99.2% Stay Enabled") but any number on screen next to a cleared obstacle would read as a promised outcome — exactly what A11 forbids. So numbers are excluded even where the site states them.

| Problem (customer words) | What the site demonstrably offers (quoted line + file:line) | Permitted claim strings (feature, ≤ 3 words) | Unsupported / forbidden for this film |
|---|---|---|---|
| "tenant verification" | "Digital KYC & Verify or Reject Tenant's Documents & Govt. IDs" (home.txt:99); "From Joining Form to Police Verification. Payment History to Tenant Ledger" (home.txt:96); "Tenant gets WhatsApp link. Uploads Aadhaar, photo, signs digital agreement on their phone." (tenant-verification.txt:49); "We submit to local police station. No follow-ups needed from you. Status updates automatically." (tenant-verification.txt:53); "Real-time verification tracking for all tenants" (tenant-verification.txt:60) | `DIGITAL KYC` · `POLICE VERIFICATION` · `VERIFICATION STATUS LIVE` | "verified in seconds"; "no bad tenants"; "guaranteed genuine tenants"; any turnaround number ("48-72 hours" is on the site but is a service promise, excluded by the numbers rule) |
| "collecting rent" | "Autopay / Collect rent automatically every month" (home.txt:19–20); "Rent Collection. Now Fully Automatic." (autopay.txt:4–5); "Rent Collects Automatically … Money moves to your account. You get instant notification." (autopay.txt:58–59); "Automatic payment reminders on WhatsApp, SMS & Notification" (home.txt:86); "One-click Bulk WhatsApp reminder with Payment Link" (home.txt:87); "Automatic Late Fine addition after the grace period" (home.txt:88) | `AUTOPAY` · `RENT ON AUTOPAY` · `AUTO REMINDERS` · `WHATSAPP PAYMENT LINK` · `AUTO LATE FINE` | "rent guaranteed"; "100% collection"; "rent recovery"; "5 days max" (site number, excluded); "never chase rent again" |
| "tenants leaving without paying rent" | The site offers tracking and collection mechanisms, not a guarantee: "Real-time update of filled, vacant, under notice rooms & beds" (home.txt:104); "Rent Not Paid … Tenants Not Paid" dashboard (autopay.txt:104–107) and "Pending Dues" (autopay.txt:136); "Autopay automatically retries for 3 consecutive days. You get instant notifications for failures, so you only follow up with specific tenants." (autopay.txt:232); "Automatic Late Fine addition after the grace period" (home.txt:88); "Payment History to Tenant Ledger" (home.txt:96). The site also advertises a third-party cover: "Get 100% Claim whenever a tenant breaks your rent agreement / Powered by Eqaro Guarantees" (home.txt:110–111) with conditions (home.txt:113–115) — **not used**: a partner insurance product with claim conditions cannot be stated honestly in a 2-word game label | `DUES TRACKED LIVE` · `TENANT LEDGER` · `UNDER-NOTICE TRACKING` · `AUTO REMINDERS` | "prevents tenants from leaving" (the customer forbids it; the site's own line at complaint-management.txt:177 "Timely issue resolution prevents tenants from leaving" is therefore NOT used); "no one leaves unpaid"; "100% claim"; "deposit guaranteed"; "rent recovery" |
| "no place to do reconciliation" | "24/7 Digital Accountant at your fingertips" (home.txt:89); "Real-time transaction updates on App & WhatsApp" (home.txt:91); "Excel Reports of Dues, Income, Expense, Lead, Tenant, Profit-Loss" (home.txt:92); "UTR no. directly in the app. No need to check the bank account" (home.txt:94); "No more Excel sheets. No more payment confusion. Everything in one dashboard." (autopay.txt:95); "Rent Collection Summary" (autopay.txt:110) | `DIGITAL ACCOUNTANT` · `ONE DASHBOARD` · `PROFIT-LOSS REPORTS` · `UTR IN APP` | "accounting done for you" as a service claim (the site offers "CA & Accounting Services" separately at home.txt:29–30 — a paid service, not the app feature; not used); "zero errors" |
| "solving complaints" | "Complaint Management / Track and resolve tenant complaints efficiently" (home.txt:15–16); "Tenants raise tickets from their app. Complaints auto-appear on your dashboard. Track, assign, and resolve - without a single phone call." (complaint-management.txt:10); "Every complaint auto-assigned to a team member" (complaint-management.txt:49); "Flagged instantly with push alerts" (complaint-management.txt:48); "Live status updates in app" (complaint-management.txt:51) | `COMPLAINT TICKETS` · `AUTO-ASSIGNED` · `TRACK & RESOLVE` | "all complaints solved"; "1 day resolution" / "8 days to 2 days" (site figures, excluded); "happier tenants, longer stays" (an outcome claim) |

- `spec.permitted_claims[]` (the only strings allowed to describe RentOk capabilities on screen; the copy deck may use any subset, each byte-exact):
  `DIGITAL KYC`, `POLICE VERIFICATION`, `VERIFICATION STATUS LIVE`, `AUTOPAY`, `RENT ON AUTOPAY`, `AUTO REMINDERS`, `WHATSAPP PAYMENT LINK`, `AUTO LATE FINE`, `DUES TRACKED LIVE`, `TENANT LEDGER`, `UNDER-NOTICE TRACKING`, `DIGITAL ACCOUNTANT`, `ONE DASHBOARD`, `PROFIT-LOSS REPORTS`, `UTR IN APP`, `COMPLAINT TICKETS`, `AUTO-ASSIGNED`, `TRACK & RESOLVE`, plus the generic app descriptions the site uses for itself: `PG/Hostel/Flat Management App` (home.txt:1), `The easiest way to manage your PGs` (home.txt:40–41), `Save time. Work less. Earn more.` (home.txt:43).
- `spec.forbidden_claims[]` (the A11 scan fails on any of these substrings, case-insensitive, in any on-screen string): `guarantee`, `guaranteed`, `100%`, `never`, `no more` (as a promise), `zero` + noun of a problem (e.g. "zero dues", "zero complaints"), `prevent`, `recover`, `recovery`, `eliminate`, `all problems`, `every problem`, `always`, any `%`, any numeral attached to an outcome (days, hours, rupees) — plus `Nintendo`, `Mario`, `Luigi`, `Mushroom Kingdom` (IP). Obstacle labels name **problems** (allowed to be blunt: `RENT DUE`, `COMPLAINT`) — they are not claims.
- Numbers rule exception: `30` in the HUD timer/score is game furniture, not a product claim — the scan whitelists HUD score/timer strings, which are listed separately in the copy deck.

### Spelling of the brand (flag F5)

- Evidence: the site writes "RentOk" everywhere in its own copy — "RentOk | PG/Hostel/Flat Management App" (home.txt:1), "Join 15000+ property owners who trust / RentOk" (home.txt:62–63), "© 2026 RentOk. All rights reserved." (complaint-management.txt:280), and the wordmark file renders "Rent" (white) + "Ok" (cyan). The customer wrote "RentOK" in chat.
- Decision: on screen, the wordmark and any mixed-case mention use **RentOk** (the brand's own spelling from the source the customer named as authoritative). The cheat-code label and other arcade-style strings are set in ALL CAPS — `INSTALL RENTOK APP` — which is spelling-neutral and matches the customer's own words. Cost if wrong (customer insists on "RentOK" in mixed case): a string re-render, USD 0.

---

## (c) IP — "original Mario-inspired" resolved into do/don't rules

- Why it matters: A9 (LJ + this record). Source: **preserve** (customer: "An original Mario-inspired game, rather than an exact reproduction of Nintendo's character, artwork, music or game assets") + reasoning (no Canon covers IP; recorded as explicit reasoning, not a legal opinion).
- Reasoning: genre conventions of a 2-D side-scrolling platformer (a running/jumping player, a ground line, blocks, pits, enemies, a power-up, a level-end flag, a coin/score HUD, a "cheat code" idea) are shared across hundreds of games and are not Nintendo's property. What must not be reproduced are Nintendo's specific expressive choices: the characters (Mario, Luigi, Peach, Bowser, Toad, Yoshi), their costumes and colour schemes, the named enemies (Goomba, Koopa, Piranha Plant), the specific items (Super Mushroom, Fire Flower, Super Star, ? block, brick block in the Nintendo style, green warp pipe), the Mushroom-Kingdom world art, the level layouts, the logos, and the music (the Super Mario Bros. theme, the 1-up/coin/power-up jingles). The word "Mario" never appears on screen or in sound.

| Element | DO (this film) | DON'T |
|---|---|---|
| Character | An original pixel-art PG owner: adult Indian man, short hair, rectangular spectacles, a checked half-sleeve shirt (blue/white), dark trousers, a keyring at the belt, a small register/notebook in hand; no hat; no moustache-as-signature; no overalls | Red cap with an initial, blue overalls, big moustache, white gloves, plumber; any Nintendo silhouette |
| Power-up form | A phone-shaped item with the RentOk blue; the powered state = a cyan aura + cyan tick-mark projectiles; no mushroom, star, flower or fire | Super Mushroom, Fire Flower, Super Star, invincibility rainbow flicker, fireballs |
| Obstacles | Original problem-shaped sprites: a wall of paper documents, a running suitcase, a rent-due sack, a tangle of spreadsheets, an angry ticket | Goombas, Koopas, Piranha Plants, Bullet Bills, Bowser |
| World | Original: a PG street — flat Indian rooftops, water tanks, a lane, terracotta and cream; ground tiles as plain brick/stone in muted ochre; clouds simple | Mushroom-Kingdom hills with eyes, green warp pipes, ? blocks, castle end, the specific sky/hill art |
| Flag | A tall pole with a RentOk-blue flag (a tick mark on it), reached by the player | The goal flag with a castle behind it, the specific flagpole descent animation |
| HUD | Original type (a pixel font with an open licence — see Stage 3), labels SCORE / LEVEL / a timer | Nintendo font, "WORLD 1-1", "MARIO ×3" |
| Music / SFX | Original generated chiptune-style bed (Lyria) + code-synthesised beeps for jump/hit/power-up | The SMB theme, the coin/1-up/power-up jingles, the death jingle |
| Words | "cheat code", "power-up", "level", "flag" (generic) | "Mario", "Nintendo", "Super", "Mushroom Kingdom", "1-UP" |

- Verification: the checker applies this table to the character sheet, the obstacle sheet, the world plate, the audio and the copy deck (A9). Generation prompts never contain "Mario", "Nintendo" or the names above (DET grep at pre-dispatch, like A3).

---

## (d) Brand assets — what exists, what must be originated

### 2.5 Which assets do we have, which are missing?

- Class/priority: DET · blocks. Source: **lookup-fact** (fetched and hashed).
- Have (OBSERVED):
  - The site's wordmark file: `source/rentok-brand/rentok-new-logo.webp` (URL `https://rentok-storage-cdn.azureedge.net/rentok-marketplace/marketplace-dump/landing-page-vectors/rentok-new-logo.webp`, referenced by `home.html` as `<img alt="RentOk Logo" …>`, fetched 2026-09-20T18:19:29Z, sha256 `1ff7dcf58689684d8ddae150d384f4aa30c246c314b0bf4e4a389a06e8f66f80`, 5988×3072 RGBA). It renders "Rent" in white and "Ok" in cyan on a blue rounded rectangle, with the yellow tagline "India's renting superapp".
  - Brand colours measured from that file and the page: blue **#0038FF** (`home.html` `<meta name="theme-color" content="#0038FF">`, the most frequent hex in the page, 38×; logo fill measures #0239FF), cyan **#03FFF1** ("Ok"), yellow **#FFF100** (tagline), white #FFFFFF. Secondary hexes in the page: green #30B502, orange #FF8A2D, dark #2C3032.
  - The five product-page texts (b) and the app's own self-description strings.
- Missing (must be originated): the player character, the five obstacles, the world/level art, the phone/app depiction (the site's dashboard screenshots are not reused — "no reuse of any earlier RentOK material"; the app screen shown in-film is a simplified original mock in brand colours carrying only permitted strings), the flag, the HUD font, music and SFX.
- Decision: the wordmark is composited by code from the fetched file (a raster brand asset placed by code = mechanism B; it is never regenerated); a code-typed fallback ("Rent" white + "Ok" cyan in a geometric sans) exists only if the file's baked-in tagline is judged too small at the end-card size (LJ at Stage 5). No app-store badge is used (no store link was found in the snapshot; `home.txt:140` "Get the app" is the site's own CTA wording).
- Reuse provenance (DESIGN_REUSE_PROVENANCE): no treatment, component or asset from cases 001/002 is carried into this job; `plan.assets[].reuse` = null throughout.

### 2.8 Is the information sufficient to proceed?

- Sufficient. No dependency blocks Stage 3. Open item carried: the written spend cap (Stage 1 §1.9).

---

## Stage 2 exit criteria — self-assessment (the checker issues the gate verdict)

| Criterion | Self-assessment |
|---|---|
| Every platform number has a fetched, dated source | Met — YouTube pages saved with sha256; Meta pages recorded as rendered-text extracts with URL + UTC (html not obtainable — recorded limitation) |
| Safe zones per placement and the intersection used for composition | Met — 2.2 table; DET check named |
| Every product claim quotes file:line from the frozen snapshot | Met — 2.4 table; permitted and forbidden lists written |
| No unsupported claim admitted; the customer's three forbidden claims are on the forbidden list | Met — including the site's own "prevents tenants from leaving" line, deliberately not used |
| IP resolved into concrete do/don't rules | Met — (c) table; DET grep of prompts named |
| Brand assets: have vs originate, with hashes | Met — (d); wordmark file hashed; colours measured |
| Audio and per-format composition decided with basis | Met — 2.6 (loudness target is a recorded default, not a platform fact), 2.7 |

Written by the producer session (lane A). Not a verdict.
