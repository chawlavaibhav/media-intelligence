# Stage 1 — Intent (what the customer asked for, and the decisions taken to make it producible)

Job `AGY-2026-09-21-MOKOBARA-ODYSSEY-001`. Source of truth: `input/00-CUSTOMER-BRIEF-FROZEN.md` (verbatim). TTAO clock started `2026-09-21T17:22:48Z` (`TTAO-START.yaml`).

## 1. Mandatory items — from the customer's own words, each with the way it will be verified

| # | Customer's words | Requirement as produced | Verification |
|---|---|---|---|
| M1 | "the proatagonist had mokbara bags" | The bag in the film is a generated likeness of one real Mokobara product, anchored on the product photos fetched from mokobara.com | LJ (human eye): bag likeness vs `source/mokobara/…Private_Island_1.jpg`; DET: reference photo sha256 recorded on every generation attempt |
| M2 | "found his mokobara bag, while he was on the island where he was kept for years" | Beat 2: the bag is discovered on the island; the man visibly bears years (long hair, beard, ragged clothes) | LJ: keyframe of beat 2 shows the bag on the island + the years-worn man; keyframe of beat 1 shows the island |
| M3 | "in that bag he founds her wives photo" | Beat 3: a photograph of a woman is taken from the bag and held | LJ: keyframe of beat 3 shows a photo of a woman in his hands (no identifiable real person: generated) |
| M4 | "a lot of stuff that he could use to go back" · "he packs food and stuff and goes back" | Beats 4–5: useful things come out of / go into the bag (food, rope, flare, paddle …); Beat 6: he leaves the island by sea with the bag on his back | LJ: keyframes of beats 4–6; DET: beat list in `board.json` covers find → pack → leave |
| M5 | "would be funny that he could keep his arms in the bag and food and so much stuff" | The comic reveal: his hand goes in, then the whole arm, then both arms to the shoulder, and things keep coming out — the bag holds an absurd amount | LJ: "does the gag read?" on the beat-4 clip (this is the riskiest generated moment — micro-qualified first, Stage 4) |
| M6 | "the odysey movie angel" + "Avoid getting copyright violoations from odysssey" | Odyssey-shaped story only: a man stranded for years, a wife waiting, the journey home. No names from Homer, no film title, actors, characters, footage, score or artwork; no imitation of any specific film's look | DET: prompt guard refuses a fixed word list (Stage 2 §3); LJ: "does any frame resemble a specific film?" |
| M7 | "lets make an ad with mokobara" | It is an advertisement: the brand appears early (the bag's identity) and the film closes on the brand: wordmark + tagline + CTA composed by code | DET: end-card strings byte-exact vs `copy-deck.json`; wordmark = the site's own SVG (hashed); no in-model lettering (frame text scan) |

Controller reading kept: "arms" = the protagonist's own arms disappearing into the bag (a "bag holds everything" gag). Cost of being wrong: if the customer meant something else (e.g. prosthetic arms stored in the bag), only beat 4 changes — one 8-s clip ≈ USD 0.80 to redo.

## 2. Decisions taken without asking (each with the cost of being wrong)

| Decision | Choice | Why | Cost if wrong |
|---|---|---|---|
| Platform / geometry | **9:16, 1080×1920, one file for Instagram Reels + Facebook + YouTube Shorts.** No 16:9 in the first pass. | The dossier (`coordination/commercial/d2c-prospecting/dossiers/mokobara.md` §1) OBSERVED a Meta Pixel with CAPI and a Google Ads tag = paid acquisition on Meta + Google; its YouTube channel has zero uploads, so vertical short-form is the natural first placement. A 16:9 version would be a second full generation pass (≈ USD 3.4) — not "cheap", so not in the first pass. | A 16:9 cut later costs one more generation pass (Veo clips are generated per aspect; a crop of 9:16 loses the sides). |
| Duration | **≈ 30 s** (29.5–30.5 s) | The brief carries no duration; the shape has seven beats and a brand close; the earlier RentOK jobs used 30 s and the spec is already established for it. | Trimming to 15 s later is an edit, ≈ USD 0. |
| Language | **English on screen; no dialogue in the film.** | The dossier §7 quotes Mokobara's copy as plain English, dry, not exclamatory ("Out doing what it does best."); nothing shows Hinglish. No speech also keeps the job out of the manual-only two-speaker/lip-sync cells and out of "voice by ear" review. Comedy is visual (the gag). | If the customer wants a spoken line, it is one added VO track (Gemini TTS is unpriced in the PriceBook; ElevenLabs credits are authorised) — an add-on, not a re-shoot. |
| Hero product | **Transit Backpack 30L, colourway "Private Island"** (navy outside, sunshine-yellow lining) — `https://mokobara.com/products/the-transit-backpack` | (a) the dossier's selected product with 35 public reference photos; (b) a backpack is worn on the back — it reads on a castaway walking, packing and pushing off, where a suitcase would not; (c) the colourway is literally called *Private Island* — the customer's own product wink at the story; (d) the yellow lining gives the "brand-colour flash in a grey world" when the bag opens; (e) the page says "Designed for everyday use and 1-2 day trips", "Capacity: 30L" and the image copy says "Can easily hold a change of clothes for an overnight trip, and all your daily essentials" — a real "holds a lot" fact under the comic exaggeration. | If Mokobara wants the Cabin Luggage instead, the bag likeness changes in every beat = a full re-shoot (≈ USD 3.4 + stills). |
| Tone | **Cinematic survival, dry comic turn at the reveal, ending on the brand.** Grey, wind, salt; then the bag; then the joke; then dawn. | The brief's own arc; the brand's register is dry, not exclamatory (dossier §7). | Tone is a prompt-level property; a re-take of one beat is ≈ USD 0.4–0.8. |
| Price on screen | **No price** on the end card. | The brief is a brand story, not an offer; the dossier §10 warns that the ₹9,999 compare-at framing is unknown. Brand + product name + CTA only. | Adding a price line later is a code change on the end card, USD 0. |

## 3. Questions that would have changed a decision (none blocking)

- None blocking. Open for the customer's review at release: the choice of the backpack over the Cabin Luggage (above), and whether a spoken line is wanted.
