# Acceptance contract — Upwork introduction film (frozen before first paid dispatch)

The film is judged as ONE film against this list. Deterministic checks are run by code; the rest are
Controller (Vaibhav) judgments. A first pass may fail; one bounded repair cycle is authorised; then the
film returns for ACCEPT / SPECIFIC REPAIR / REJECT.

## A. Commercial
- A1 By 0:05 a muted viewer can read what is sold ("Meta ads … twenty-four hours" on screen as supers).
- A2 Standard 24 h stated before Express 4 h; "4 h" never appears on a frame without "09:00–19:00 IST".
- A3 No internal-technology word anywhere (model names, routing, pipeline, Canon, registry, LLM).
- A4 Deliverables shown are exactly the menu: statics in four sizes, 10–15 s vertical video ads, English + Hindi, variants of an approved concept. Nothing longer than 15 s is presented as a deliverable.
- A5 CTA spoken and on screen: send your product link → straight price for a first test pack.
- A6 "AI-generated. Human-directed. Custom per order." on the end card; "Adwisely" exactly once; the owner named once as the human who checks.
- A7 No price, no metric, no client name, no banned word (UGC, spokesperson, talking head, avatar, consistent character), no other company name.

## B. Creative
- B1 One film: one light direction (window left) across presenter and product plates; one type system in the cards; cuts only, one fade at the end.
- B2 Presenter takes read as the same person (see C1) and as deliberate: still frame, eyes to lens, no drift of room or wardrobe.
- B3 Each frame has one boss element; supers are never over busy picture; cards are left-aligned on solid ground.
- B4 The work section proves rather than lists: the build is legible as a real ad being finished; four sizes, six hooks and the Hindi flip are the same ad, not new pictures.
- B5 The film would not be mistaken for a generic AI showreel: no thumbnail wall, no drone shot, no neon, no exclamation mark, no caps headline.
- B6 The three phone clips each pass the producer test alone (would a buyer pay for this ad?).

## C. AI-failure control (each is a REJECT trigger on its own)
- C1 Identity: face, hair, wardrobe, room match across T1/T2/T3 at a glance; no change of skin tone, earrings, neckline or wall.
- C2 Speech: words in each take match the script verbatim (Controller listens; transcript check by ear), lips move with the words, no doubled syllables, no accent switch mid-take, no robotic cadence.
- C3 No malformed hands/teeth/eyes on the presenter; no warped bottle on the plate.
- C4 No stray generated lettering anywhere in any generated frame (plate, presenter room, library clips as cropped).
- C5 No continuity defect that breaks comprehension (the ad shown in the insert at 0:02.5 is the same ad the build finishes at 0:17).
- C6 No filler shot: every shot is nameable by purpose in the shot map.

## D. Technical
- D1 1920x1080, H.264, AAC, ≤ 58.0 s, ≤ 200 MB; also a YouTube-ready copy. Loudness −16 LUFS integrated ±1, true peak ≤ −1 dBTP.
- D2 Speech intelligible with music ducked ≥ 12 dB under dialogue; no music under the last 0.5 s.
- D3 Every critical text string is composed by code from `plan/COPY-DECK.yaml`; a script asserts the rendered frames' text sources equal the deck (no hand-typed text in the timeline).
- D4 Contrast of every super and card text ≥ 4.5:1 (≥ 3:1 for ≥ 24 px bold) against its ground — measured by code on the rendered frame.
- D5 No watermark, no provider badge, no metadata credit visible.
- D6 Vertical ads inside phone frames keep their full 9:16/4:5 area; no crop of ad text.

## E. Truth
- E1 Every ad or clip shown was produced by the pipeline (new for this film, or a sealed EVAL-040 accepted artifact, path recorded in the production map). Invented brands only; presented as demonstrations.
- E2 No claim on screen or in speech exceeds the live profile (COMMERCIAL-BRIEF §9).
- E3 The presenter never claims to be the owner; the disclosure is literal.

## Bounded repair rule
If the first pass fails, repair the smallest failing unit (one take, one plate, one card) within the remaining cap. No second repair without the Controller.
