# Stage 3 — Creative (a numbered board exists; feeling / framing / impact per beat)

Job `AGY-2026-09-21-MOKOBARA-ODYSSEY-001`. Companion files: `board.json` (the board, the identity anchors), `copy-deck.json` (every exact string), `stages/evidence/canon-lookup.txt`.

## A. Canon, consulted honestly

**A1. Deterministic pack lookup** (USD 0; `stages/evidence/canon-lookup.txt`): 10 packs selected, **2 injected** (compiled + accepted): `composition_and_attention`, `product_appearance`; prefix sha256 `4d7a5b27…`, 5,298 tokens, 21 check ids. 8 packs fired but are uncompiled (recorded as gaps, never invented). Note: `runtime.cli` refuses kind `multi_shot_story` under policy profile `dry`; the lookup was run by the direct call Lane A used.

**A2. Accepted claims retrieved by id from `canon/knowledge/current/**`** (text quoted from the source-knowledge files; used for the decisions named):

| Decision | Claim (id) | Quoted text | How it is used |
|---|---|---|---|
| Open | `sk_abcd_0007` | "beginning in the middle of the action, and opening on a close-up" | Beat 1 opens on the hand scratching the tally mark |
| | `sk_ogx_0040` | "Open with the fire. You have only 30 seconds. If you grab attention in the first frame with a visual surprise…" | first frame = hundreds of tally marks in rock (years, in one image) |
| Brand early / often / richly | `sk_abcd_0010`, `sk_abcd_0011`, `sk_ogx_0039` | "Brand early, often, and richly" · "an early appearance that then lapses does not satisfy it" · "Use the name within the first ten seconds" · "Commercials which end by showing the package are more effective" | the bag (product in-situ) is on screen from 3.5 s to 28 s; a code wordmark super at 5.0–7.5 s; end card = the package |
| Product as hero | `sk_ogl_c003_0014` | "Whenever you can, make the product itself the hero" | the bag is the object every beat turns on |
| Story | `sk_sb_c003_0014` | "What does the hero want? Who or what is opposing…? What will the hero's life look like…?" | answerable at any frame: home / the sea and the years / her |
| | `sk_whip_0011` | "if you don't have conflict, you don't have a story" | the first 12 s are the years and the grey, unsoftened |
| Humour | `sk_whip_0058` | "don't set out to be funny; set out to be interesting … funny isn't a language, funny is an accent" | the gag is played dry inside a real survival story, not as a sketch |
| | `sk_whip_0031` | "an exaggeration must be based on a truth, or what remains is a silly contrivance" | the truth: "Capacity: 30L", "a change of clothes for an overnight trip, and all your daily essentials", hidden compartments (Stage 2 (b)); the paddle is the exaggeration of it |
| | `sk_ogx_0032` vs `sk_mla_0064` | Ogilvy: "humor can now sell … very few writers can write funny commercials which are funny" · Hopkins: "Frivolity has no place in advertising. Nor has humor." | a real tension in Canon, uncompiled; resolved by the brief clause "would be funny…" (the customer forces humour) and Ogilvy's later reversal; the risk Ogilvy names is carried as LJ "does the gag read?" |
| | `sk_fre_c003_0025` | "The reveal is a cinematic device … effective through surprise" | beat 4 is a reveal held in one locked shot |
| | `sk_hea_mts_0011` | "surprise doesn't last … systematically 'opening gaps'" | beat 5 keeps asking "what else is in there?" after the surprise of beat 4 |
| Cuts | `sk_gote_c003_0004`, `sk_gote_c003_0006`, `sk_murch_c003_0020` | new information per shot; a motivation to leave; "Emotion … preserve at all costs" | 6 cuts, each on a new object or state; her photo held before the gag |
| Screen direction | `sk_gos_c003_0007` | "screen direction … must be maintained from one shot to the next" | he faces/travels left→right in beats 1, 2, 6 |
| Key of the picture | `sk_alt_c003_0018` | comedy "lit high and brilliant"; drama otherwise | **deviation, recorded:** the film is a drama with a comic turn, so the key stays low grey; the only "high" light is inside the bag (yellow) and the dawn. Forcing clause: the brief's survival story |
| Audio brand mention | `sk_abcd_0012` | "an audio mention of the brand raises the performance of the on-screen brand visual" | **deviation, recorded:** no voice-over (Stage 1 §2 language decision); cost = weaker brand recall per this source; can be added as one VO track later |
| Wordmark | `sk_vig_c003_0013` | a logo "should not be discarded"; identity is a system | the site's own SVG, never redrawn |

**A3. The 21 compiled checks** (composition_and_attention CA-D1..11, product_appearance PA-D1..10) applied to the board: CA-D1 one dominant cue per beat (the marks / the colour / the photo / the arms / the zip / the raft / the wordmark); CA-D2 subject off-centre in beats 1, 2, 6 and centred in beat 4 because the scene points inward (CF-08); CA-D7 one device per beat (pull-back / blocking / cut-in / locked hold / hands montage / wide); CA-D9 direction persists; CA-D11 the two camera moves are motivated (beat 1 the reveal of scale, beat 6 following the raft). PA-D1 finishes declared: bag = matte diffuse (coated fabric), zip pulls = small glossy, rock = wet direct; PA-D4 one fictional source: overcast skylight from upper left in beats 1–5, low sun from frame right in beat 6; PA-D5 separation: navy against grey pebbles survives grayscale by tone (dark on mid-grey); PA-D7 "what the hero image sells at a glance": *this bag holds more than seems possible* (beat 4); PA-D9 hero angle: three-quarter front showing front, side and top (beats 2, 4). No PA-D8 glass.

**GAPs (honest):** no accepted Canon on comedy timing, survival cinematography, or short-form pacing (`editing_pacing_and_short_form` uncompiled); audio has no Canon; those decisions are the producer's and are attributed to nobody. Camera and light language for the beats is taken from the Media Factory practice (`03-MEDIA-FACTORY-EVIDENCE.md` §2.2–2.3: shot → fixed identity anchors → action → camera with cause → light/sound; hero still before video; one change-set per re-take).

## B. The film

**Proposition (one line):** *After years alone, the thing that gets him home is the bag that was there all along — and it holds more than seems possible.*

**Protagonist / bag / island / grade** — the four verbatim anchor blocks are in `board.json` `identity_anchors`; they are pasted unchanged into every prompt.

**Board** (`board.json`, 7 beats, 30.0 s; purchase 30 s of Veo = USD 3.00):

| # | t | Beat | Feeling | Framing | Impact |
|---|---|---|---|---|---|
| 1 | 0–3.5 | Years | endurance | ECU hand scratching a tally mark into rock covered in marks → pull back to the small man on the grey shore | the pull-back reveals the scale; wind + scrape; no music |
| 2 | 3.5–7.5 | The bag | recognition | low at the tideline, the navy bag half-buried in grey pebbles, a wave over it; he crouches, brushes sand | colour is the hit; wordmark super 5.0–7.5 s |
| 3 | 7.5–12.5 | Her | the reason | over-shoulder unzip → yellow lining → a photo of a smiling woman; cut in on his face | first warmth; music enters under her |
| 4 | 12.5–20.5 | The reveal | disbelief → laugh | locked medium, bag centre: hand, arm, shoulder; other arm; both to the shoulders; out come rope, coconut, a paddle longer than the bag | deadpan hold; no sting; **HERO FRAME** = both arms in |
| 5 | 20.5–24.5 | Packing | momentum | close on hands: coconuts, dried fish, gourd, rope, flare go in; the zip closes | pace; music lifts; each item a gap, the zip closes it |
| 6 | 24.5–28 | Home | hope | wide dawn: raft into the sea, bag on his back, paddling to a gold horizon | widest frame; first warm light; music opens |
| 7 | 28–30 | Brand close | home | code end card: wordmark · Transit Backpack · 30L · tagline · mokobara.com | the package; music resolves |

**Copy deck** (`copy-deck.json`, byte-exact, code-set): wordmark (SVG asset) · `Transit Backpack · 30L` · `Room for the long way home.` · `mokobara.com`. Tagline check against the brand's register (dry, confident, no exclamation — "Out doing what it does best."): passes; it claims only room (30L is on the page) and the story.

**Audio direction (decided by the beat table):** Veo native audio ON for ambience and Foley (wind, surf, zip, rope, paddle — the sounds code cannot fake convincingly), with "no dialogue, no speech, no music" in every prompt; one Lyria instrumental bed (USD 0.06) entering at 7.5 s; no voice-over. Any generated speech that slips in is a defect (flag for the human ear).

**Muted test:** yes — every beat's meaning is in picture; the wordmark super and end card carry the brand without sound.

**Prompt shape per beat (five parts, Media Factory):** [shot + lens + camera] · [protagonist anchors verbatim] · [action with the emotional state] · [camera move with its cause] · [light source, tonal separation, colour, audio, then the no-text/no-logo clause].
