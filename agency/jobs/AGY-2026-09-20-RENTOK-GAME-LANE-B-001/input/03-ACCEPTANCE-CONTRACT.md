# Common acceptance contract — established before execution (2026-09-20)

Derived from the original customer request and confirmed answers (`01-CUSTOMER-BRIEF-FROZEN.md`). Applies identically to both lanes. Each item names how it is checked; DET = deterministic (code over the delivered file), LJ = independent visual inspection by a non-author session, HJ = human (the customer, blind).

## A. Customer-requirement compliance (mandatory; a miss is a failed deliverable)

| # | Requirement (customer words in quotes) | Check |
|---|---|---|
| A1 | The film is "a Mario game" — reads as an actual platform game (side-scrolling level, player character, obstacles, HUD-style elements, a finishing flag), "not a conventional promotional video with gaming graphics placed over it" | LJ + HJ |
| A2 | "The player is basically a PG owner" — recognisable as a PG owner within the game (costume, props, label or context), not a generic hero | LJ + HJ |
| A3 | The obstacles represent the named problems: "tenant verification, collecting rent, tenants leaving without paying rent, no place to do reconciliation, solving complaints" — each of the five is identifiable in the film | LJ (per-obstacle checklist) |
| A4 | "The game also introduces a cheat code — install RentOK app" — an install-RentOK event is the central turning point | LJ + HJ |
| A5 | "Mario gets a gun sort of power/immunity" — the character visibly acquires an enhanced ability (the requested game-style power/immunity mechanic is preserved) | LJ + HJ |
| A6 | "It runs and kills all the obstacles and gets the flag" — the character overcomes the obstacles with the new ability and reaches the finishing flag | LJ + HJ |
| A7 | Duration 30 s (tolerance: 29.5–30.5 s measured by ffprobe) | DET |
| A8 | Suitable for Instagram Reels / Facebook and YouTube Shorts: 9:16, 1080×1920, H.264/AAC MP4, platform limits met, critical text inside the platform safe zones the lane documented at Stage 2 | DET (container/geometry/duration) + LJ (safe-zone visual) |
| A9 | Original Mario-inspired: no Nintendo character, artwork, music or asset reproduced (no Mario/Luigi likeness, mushroom-kingdom assets, Nintendo melodies) | LJ + the lane's Stage 2 IP record |
| A10 | The film communicates why RentOK is relevant to a PG owner | HJ |
| A11 | No unverified claim: nothing states or implies that RentOK guarantees rent recovery, prevents tenants from leaving, or eliminates all problems | DET (string scan of on-screen copy against the permitted-claims list) + LJ |

## B. Creative quality (independent evaluation; the customer's verdict governs)

Coherent as a platform game · gameplay readable in 9:16 at phone size · the transformation (install → power-up → clearing) is engaging · the commercial message lands.

## C. Production quality

Visuals, animation, timing, sound, text, branding and editing coherent and professionally executed; no stray/garbled generated lettering; brand mark and CTA legible; audio present and level-safe.

## D. Factual accuracy

Every depicted RentOk capability is supported by the frozen website snapshot (`source/rentok-snapshot/`) or a page the lane fetched and hashed; each material claim cites its source line.

## E. Commercial acceptance (the customer, blind)

Presented as Video X / Video Y. Verdict per video: ACCEPT / SPECIFIC REPAIR / REJECT, recorded verbatim, with reasons asked for on a rejection (no diagnosis offered, no pathway revealed). Actual spend, attempts and cost per accepted outcome are reported separately from the quality judgments.
