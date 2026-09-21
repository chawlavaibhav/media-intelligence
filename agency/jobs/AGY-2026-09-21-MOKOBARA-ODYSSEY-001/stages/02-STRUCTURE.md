# Stage 2 — Structure and facts (every fact has a source; nothing asserted from memory)

Job `AGY-2026-09-21-MOKOBARA-ODYSSEY-001`. Fetched sources live in `source/mokobara/` with `SHA256SUMS.txt` and `FETCH-LOG.txt` (UTC per URL).

## (a) Publishing specification — reused from Lane A, not re-derived

Source: `agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-A-001/stages/02-STRUCTURE.md` @ `0405feb0` (its §2.1–2.2 quote the Meta Reels ads guide and YouTube's Shorts/encoding/safe-zone pages, fetched 2026-09-20 with sha256 in its `source/platform/`). The numbers carried:

| Item | Value | Where it came from |
|---|---|---|
| Geometry | 9:16, **1080×1920**, H.264 High, yuv420p, progressive, 24 fps (the clips' native rate; resampling to 30 would duplicate frames — YouTube lists 24 among common rates), MP4 | YouTube "maximum resolution of 1080p"; Meta H.264/AAC; Lane A A8 |
| Audio | AAC-LC 48 kHz stereo ≥128 kbps; **−14 LUFS integrated, true peak ≤ −1 dBTP** (recorded default) | YouTube encoding page; Lane A 2.4 |
| Container | **no edit lists** (walk the `moov/trak/edts` boxes), `moov` first (faststart) | YouTube "No Edit Lists"; Meta "edit lists or special boxes" |
| Duration | 29.5–30.5 s | Stage 1 decision |
| **Critical-element safe box** | **(65,288)–(888,1248)** = 823×960 px — the intersection of the Reels (14 % top / 35 % bottom / 6 % sides) and YouTube (288/672/48/192) safe zones | Lane A §2.2 |
| Muted-first | yes — every beat carries its meaning in picture; no information exists only in sound | Lane A 2.4 |

All exact text (wordmark, tagline, CTA, product name) is composed by code inside the safe box. The generated picture fills the full frame and may be cropped by a platform.

## (b) Brand and product facts (OBSERVED from fetched files; quote-exact)

Fetched 2026-09-21 (UTC in `FETCH-LOG.txt`): `transit-backpack.json` (sha256 `df3e1fda…`), `transit-backpack.html` (`136c484e…`), `home.html` (`598752bd…`), seven "Private Island" product photos + one "Crypto Sunray" photo (`SHA256SUMS.txt`), `wordmark-white.svg` (`c443658f…`, the site's own header `<img>` asset `Mokobara_SVG_White_Logo.svg`), `logo-png.png` (`b3aefbd5…`).

| Fact | Exact value | Source line |
|---|---|---|
| Brand name spelling | **mokobara** (lowercase wordmark; the site's copy uses it as a common noun: "Every mokobara goes through…"); "Mokobara" capitalised as `vendor` | `wordmark-white.svg`; `home.html`; `transit-backpack.json` `vendor` |
| Product name | **Transit Backpack** — page title "Transit Backpack"; the product-information image says "Transit Backpack - 30L" | `transit-backpack.json` `title`; `…Private_Island_1.jpg` |
| Colourway | **Private Island** (option `Color`, 5 values: Money Moves Sunray · Seize The Gray · Home Grown Sunray · Money Moves · Private Island) | `transit-backpack.json` `options[0].values` |
| Appearance (for the likeness) | deep navy body, smooth matte "reverse-coated polyester", "vegan leather trims", **bright yellow lining**, one vertical front zip + a front bucket pocket with two black zip pulls, black padded straps, a small top grab handle, a small rectangular tonal patch and a tiny wordmark on the lower front (the wordmark is NOT reproduced in the generated bag) | the seven Private Island photos; `body_html` "Crafted with reverse-coated polyester, and vegan leather trims." |
| Capacity | **"Capacity: 30L"**; "Splendidly sized: 48 x 31 x 16 cms" | `body_html` |
| Use | "Designed for everyday use and 1-2 day trips." · image copy "Can easily hold a change of clothes for an overnight trip, and all your daily essentials." · "Our most functional backpack ever" | `body_html`; `…Private_Island_2.jpg` (text inside the brand's own image) |
| Compartments | "Front compartment houses a retractable key holder, cardholder, pen pockets, slip pockets and a zipper pocket." · "two hidden water bottle/umbrella compartments. Can fit up-to 1L water bottle easily." · "Body blended magnetic pocket for passport, boarding pass and cellphone." | `body_html` |
| Price | `price` 5999.00, `compare_at_price` 9999.00 (recorded; **not used on screen**, Stage 1 §2) | `transit-backpack.json` `variants[]` |
| Hero line | "The Joy Is in the Details" · "Every street, every airport, every work desk." | `home.html` |
| Tone | plain, confident, slightly dry (dossier §7, OBSERVED from site copy) | dossier |

**Permitted on screen** (byte-exact, any subset): `mokobara` (wordmark asset) · `Transit Backpack` · `30L` · `mokobara.com` · one original tagline (Stage 3) that makes no capability claim beyond "it carries a lot / it comes home". The film's exaggeration (arms vanish inside; a paddle comes out) is obvious comic hyperbole in picture, never stated as text.

**Forbidden:** anything not on the page — "indestructible", "waterproof", "lifetime", "survives years", "airline-approved", "TSA", any warranty/material spec beyond the quoted line, any scarcity or ranking claim, any price framing (dossier §10). Prompt guard word list: `indestructible|waterproof|lifetime|guarantee|best-selling|#1`.

## (c) IP rules resolved into do / don't

- **Do:** the myth's shape (a man kept on an island for years; a photograph of the wife he is going back to; the journey home by sea); a nameless protagonist; a generic grey volcanic/rocky island; an improvised raft; dawn.
- **Don't (prompt guard refuses these words):** `odyssey|odysseus|penelope|telemachus|ithaca|calypso|homer|nolan|universal|cast away|castaway|wilson|hanks|fedex|robinson crusoe|tom hanks|matt damon|zendaya|lupita|holland` — no film title, actor, character, prop (no volleyball with a face), footage, score or artwork; no imitation of a specific film's poster or grading; no identifiable real person (the wife's photo is a generated, unnamed woman).
- The word "odyssey" therefore appears nowhere in prompts, on screen or in the tagline.

## (d) Assets: have vs originate

| Asset | Status |
|---|---|
| Product reference photos (7 × Private Island) | HAVE — `source/mokobara/`, hashed; used ONLY as reference images for the generator and for the checker's likeness comparison; never placed in the film (Stage 1 M1; the decision is recorded here: **no Mokobara photograph appears in the film**) |
| Wordmark | HAVE — `wordmark-white.svg` from the site header, rasterised by `rsvg-convert` for the code end card |
| Protagonist | ORIGINATE — one hero still (nano-banana-2), then reused as the identity reference in every beat still |
| Wife's photo | ORIGINATE — inside beat-3 still/clip, a generated unnamed woman |
| Island, raft, props | ORIGINATE — in the beat prompts |
| Music | ORIGINATE — Lyria instrumental (MUS/lyria+native, clean 4/4, USD 0.06) if the audio decision (Stage 3) calls for a bed |
| Fonts for tagline/CTA | system Avenir Next (geometric sans; the brand's typeface is not verified from page source — dossier §7) |
