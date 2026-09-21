# Controller comparison — RentOK game video, two lanes (written after the customer's blind verdicts, 2026-09-21 IST)

**Verdict of record (verbatim, chat, 2026-09-20T20:06Z):** "both accepted. vidoe one has robotic voice over althouh. video 2 is better" — Video X (= Lane B, ChatGPT-directed) ACCEPT with a noted robotic voice-over; Video Y (= Lane A, autonomous) ACCEPT and preferred. Mapping opened only after the verdict was written (`05-BLIND-PACKET/VERDICTS.md`, `05-BLIND-PACKET-SEALED/MAPPING.json`, seal sha256 `39365d62…`). Blindness limitation: §8 of the experiment contract (the human had seen per-lane progress facts in chat).

Labels: OBSERVED (from committed records, re-measured where stated) · INFERRED · UNKNOWN. **One customer, one job: nothing below establishes a general winner.**

## 1. Cost, attempts, time — reported apart from quality (OBSERVED)

| | Lane A — autonomous | Lane B — ChatGPT-directed |
|---|---|---|
| Paid attempts | 8 (7 Nano Banana 2 stills + 1 Lyria) | 25 (7 NB2 stills + 1 Lyria + 9 voice auditions across Sarvam/ElevenLabs/Gemini TTS + 8 Gemini transcription checks) |
| Failed / refused / local-fault calls | 0 | 3 (ElevenLabs HTTP 401 quota; Gemini TTS refusal; one local fault, nothing sent) |
| Reserved spend (upper bound; vendor statements unreconciled) | **USD 0.529** | **USD 0.58675** |
| Cap | USD 10.00 | USD 10.00 |
| Cost per accepted outcome (this job) | USD 0.529 | USD 0.587 |
| TTAO (job clock → human ACCEPT) | **1 h 54 m 18 s** | **1 h 53 m 07 s** |
| Presentations / versions to acceptance | 1 / 1 (after 1 checker repair round + 1 regression fix) | 1 / 1 (after 1 checker repair round) |
| Baseline (case UPWORK-INTRO-001, 57-s film) | 7 h 54 m / USD 15.39 / 5 versions | same |
| Session tokens (Controller-side accounting, not a ledger figure) | producer ≈ 588 k, checkers ≈ 272 k + 202 k | producer ≈ 578 k, checkers ≈ 266 k + 220 k |

INFERRED: the USD 0.06 difference is entirely Lane B's voice auditions and transcription checks; picture assets cost the same in both lanes (7 × 0.067 + 0.06).

## 2. What each pathway produced (OBSERVED from the stage records and the films)

Both lanes, independently and without seeing each other, chose the same production method: a 2-D side-scroller rendered by code (Pillow → ffmpeg) with a handful of textless AI stills for the character sheet, five obstacles and a world plate, every string composed by code, music from Lyria, and **no generative video**. Both reasoned from the same evidence (route observations on identity drift and in-model lettering; no timing control in generative video) — so the convergence is a property of the shared evidence base, not of either creative input.

Where they differ:

| Dimension | Lane A | Lane B |
|---|---|---|
| Creative starting point | brief only | brief + ChatGPT direction, interrogated element by element |
| Player identity | keys + red register + HUD tag | keys + register + HUD tag (a "PG" nameplate proposed by the direction was dropped at the gate: it would have been model-drawn text) |
| Power-up | phone item + cyan aura + tick projectiles + immunity | RentOk phone firing an "OK beam" + shield glow (the direction's "Control Blaster" replaced — no firearm, product in use) |
| Obstacle clearing | per-obstacle transformations (debris / dashboard card / red→green tickets) after the repair round | obstacles converted to cited status cards |
| Voice | none (recorded deviation; muted-first) | three-line arcade announcer, Sarvam bulbul:v3 after a 3-candidate audition — the element the customer called "robotic" |
| Changes from supplied direction | n/a | 10 material changes, each logged with a reason (`03-CREATIVE.md` CHANGES-FROM-SUPPLIED-DIRECTION) |

## 3. Where the difference came from — by mechanism, as far as the evidence allows

**Creative direction (the variable under test).** The supplied direction gave Lane B a complete structure at minute zero; Lane B spent its Stage 3 verifying and improving it rather than inventing. Lane A invented its own and arrived at a comparable structure. Both passed every mandatory customer item at the independent check. The customer preferred Lane A's film and named one concrete difference — the voice — which was a Lane B *addition* to the supplied direction (the direction asked for "arcade music and a start-game chime", not an announcer). INFERRED: on this job the ChatGPT direction neither helped nor hurt the structure; the preference tracked an execution choice, not the direction. UNKNOWN: whether a voiceless Lane B would have been preferred.

**Canon interrogation.** Lane A cited 33 accepted claim ids + the 21 compiled decisions; Lane B cited 62 + 21 (the Lane B checker found audio/colour claims Lane B had first declared gaps, and Lane B then used them). Both lanes' checkers verified the cited ids exist and were quoted faithfully. Both lanes recorded the same real gap: no accepted Canon on games, arcade readability, pixel art or chiptune. OBSERVED: the two films are structurally similar in the dimensions Canon covers (open in action, brand early, ask on a card, close on the brand). INFERRED: Canon shaped the ad-structure layer in both lanes equally; it did not differentiate them. The experiment does not isolate Canon as a variable (contract §2).

**Production selection.** Identical method, identical picture cost. Lane B's only extra selection — a voice route — produced the one customer-named defect. OBSERVED: no route used was outside `production_use_allowed: true`; no fal; no cap crossing.

**Execution.** Both lanes' first renders had defects their own DET suites did not test for (Lane A: MP4 edit lists, flag hidden behind the checklist, board fidelity; Lane B: graphic-over-text, pole through the character, VO 1.2 s ahead of its words, register missing in 3 sprite cells). Both fixed everything at USD 0 in one round. Lane A's repair introduced a regression (black end card) that the checker's re-verification caught and a one-line fix removed. INFERRED: rendering by code made repairs free, and made the repair loop the place where quality was actually won.

**Independent checking.** OBSERVED: 4 gate reviews + 2 stage-5 verifications + 2 re-verifications, all by sessions that wrote none of the work; they reopened 2 items in Lane A (one of them a forbidden-claim depiction — a tenant "frozen" by the power-up — caught before any spend) and 2 in Lane B (a would-be model-drawn nameplate; a pool-labelling question), then found 10 + 7 defects on the finished files, one regression, and passed both for presentation. The customer accepted both. INFERRED: the checker layer is where the forbidden-claim risk and the file-spec misses were caught; the producers' self-checks caught layout collisions (via the runtime gates) but not these.

## 4. What the customer's words support and do not support

- Supported: both films are commercially acceptable to this customer for this brief at a cost of ≈ USD 0.55 each and under two hours each.
- Supported: the generated voice (Sarvam bulbul:v3, one of three candidates auditioned) was heard as robotic by the customer — a directional route observation (n = 1, `routing_authority: none`).
- Not supported: that the autonomous pathway is generally better, that Canon caused either result, that a code-rendered game is the right production method for other game-style briefs, or that the voice was the *only* reason for the preference (the customer gave one reason; the checkers named others — tone, sparse lower band — that were never adjudicated).

## 5. Learning candidates (for `/media-agency-sync`, not applied here)

1. Two production-learning cases to distil (`AGY-2026-09-20-RENTOK-GAME-LANE-A-001`, `…-LANE-B-001`), both ACCEPTED, learning packets `pending_sync`.
2. Deterministic checks promoted from this job (candidates): MP4 box-tree edit-list check; graphic-vs-text disjointness (not only text-vs-text); brand-colour pixel sample on rendered frames; a repair statement must quote a measured pixel/value. All found by independent checkers, all USD 0.
3. Route observations (directional): Nano Banana 2 sprite sheets — 2/2 first draws passed a multi-pose consistency card with no stray lettering; Sarvam bulbul:v3 announcer heard as robotic by the customer; Gemini TTS refused one arcade line as prohibited content; ElevenLabs per-key quota invisible to the balance read.
4. Process: the five-stage protocol with a non-author checker ran end-to-end twice with zero cap pressure; the expensive part was wall-clock reading and record-writing (≈ 30 min per lane for Stages 1–4), not media.

## 6. Housekeeping still open (Controller decisions, not done by this file)

Push the three branches (lane A's evidence commit is ≈ 550 MB of sampled frames; slimming is possible from committed code); run `/media-agency-sync` for the two cases; decide whether the RentOK films go anywhere (human release, C-8 — nothing has been delivered externally); reconcile vendor statements against the two ledgers.
