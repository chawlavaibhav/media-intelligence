# 06 — Evaluation protocol: four clips, one event, blind

Experiment `RENTOK-CREATIVE-QUALITY-001`. Written 2026-09-21. Status: PROPOSED (nothing has been evaluated; Treatments B, C, D do not yet exist).

## 1. What is judged, by whom, on what

- **Objects:** four short clips (≈ 5–8 s, 9:16, 1080×1920, H.264/AAC MP4) that each cover the same event: *the PG owner faces the complaints obstacle → is hit and reaches GAME OVER? → the cheat code is entered and RentOk is installed → he gains a visible power → he uses it on the first obstacle (the document wall) and clears it, and the first product chip lands.* Treatment A is the frozen baseline (04); B, C and D are built as planned in 05.
- **Evaluator:** one **independent evaluator** who did not write, direct, prompt, render or check any of the four clips — a non-author session, or the customer, or both (recorded separately). The evaluator receives the clips, this rubric and the scoring sheet — **no plan, no prompt, no code, no treatment description, no cost.** The evaluator judges media, not documents.
- **Blindness:** the clips are named `CLIP-K.mp4`, `CLIP-L.mp4`, `CLIP-M.mp4`, `CLIP-N.mp4`. The mapping treatment→label is drawn by a seeded random permutation, written to `eval-packet/MAPPING.json`, hashed, and the hash committed *before* the packet is delivered; the mapping file itself is committed only after the scoring sheet is committed. The presentation order in the packet README is a second seeded permutation (so the label order and the treatment order are independent). Seeds and hashes are recorded in `eval-packet/SEAL.txt`.
- **Playback:** the evaluator watches each clip at least twice — once at phone width (≤ 400 px wide, sound on) and once at full size (sound on) — before scoring; a 10-fps contact sheet of each clip is supplied for reference but scores are given on the moving picture.
- **Time of judgement:** all four in one sitting; a single pass of scores, then one optional revision pass; no discussion with anyone during scoring.
- **Same-event check first:** before any quality scoring, the evaluator confirms for each clip that the event list above is present in that order; a clip that is missing an event is scored, but the miss is recorded under §2 and disqualifies it from "preferred".

## 2. Part (i) — mandatory customer requirements (PASS / FAIL per item, per clip)

Derived from the frozen brief and the acceptance contract (A1–A6, A9, A11); a FAIL on any item means the clip cannot be preferred whatever its quality scores.

| # | Requirement (customer words) | PASS means |
|---|---|---|
| R1 | "The player is basically a PG owner" | the character is recognisable as the same PG owner (a man with spectacles, checked shirt, keys, a red register) — by picture, with or without the HUD label |
| R2 | obstacle recognisable ("solving complaints" then "tenant verification") | the first obstacle reads as complaints/tickets and the second as unverified paperwork, from the picture before the label |
| R3 | "a cheat code — install RentOK app" | the install/activation is a distinct, visible event that changes the state of the scene |
| R4 | "visibly enhanced ability" | a change *on the character* (not only a HUD colour) is visible after the install |
| R5 | powered action | he *does* something with the power (fires, strikes, projects) — an action, not a decoration |
| R6 | physical interaction | the power *contacts* the obstacle and the obstacle *responds* (bursts, breaks, transforms); nothing "disappears automatically" |
| R7 | clear payoff | the clear produces a visible reward (the chip / a status) |
| R8 | "feel like an actual platform game, not a conventional promotional video with gaming graphics placed over it" | side-on game world, HUD, and character that read as one game — not a film with a HUD on top |

## 3. Part (ii) — creative-quality target (1–5 per criterion, anchors written out)

Score each criterion for each clip. Use the anchor text; half points are not allowed. The anchors describe *what is on screen*, not intentions.

**Q1 · Prompt adherence (does the clip do what the event list says, with nothing extra or missing?)**
1 — one or more events missing, out of order, or an unrequested element (extra character, invented text, a different world) is present.
2 — all events present but one is barely legible (you have to know it is there) or a small unrequested element intrudes.
3 — all events present and legible in order; minor liberties that do not change the story.
4 — all events present, legible, in order, and each is given its own clear moment.
5 — as 4, and the clip adds nothing and loses nothing: every second serves an event on the list.

**Q2 · Visual quality (craft of the picture itself)**
1 — broken drawing or rendering: garbled shapes, smearing, keying fringes, artefacts a viewer notices at phone size.
2 — clean but crude: flat, repetitive, or visibly assembled from parts (a sprite sliding over a background).
3 — competent: consistent style, clean edges, nothing distracts; nothing delights.
4 — attractive: considered palette and light, depth in the scene, details that reward a second look.
5 — striking: a frame you would pause on; style, light and composition all working; nothing looks like a placeholder.

**Q3 · Character expressiveness (can you read what the owner feels?)**
1 — the character has one face and one attitude throughout; you infer feeling only from the HUD or text.
2 — one visible change of pose or face across the clip (e.g. standing → knocked), no expression.
3 — the face or body shows at least two distinct states (e.g. alarmed, then determined) at the right moments.
4 — feelings read at every beat — dread, pain, defeat, awe, confidence, release — through pose *and* face.
5 — as 4, and the transitions between states are performed (anticipation, reaction, follow-through), so the character seems to *decide*, not switch.

**Q4 · Motion quality (weight, timing, impact)**
1 — objects slide at constant speed; contacts do not register; nothing accelerates, decelerates, or reacts.
2 — a few timed effects (a flash, a knock-back) mark events, but bodies are rigid and motion is linear.
3 — actions have a beginning and an end; the hit and the burst land with a visible reaction (shake, stop, recoil, debris).
4 — as 3, with anticipation before actions and follow-through after them; weight is believable; effects are proportionate to the event.
5 — every action is staged: the eye is led to it, it lands, and it settles; the clip would be used as a reference for "game feel".

**Q5 · Environmental richness (the world)**
1 — a flat backdrop; no depth; the world is indifferent to the story.
2 — a backdrop with some parallax or props; still the same world before and after the turning point.
3 — depth (layers, foreground/background) and some detail; the world changes at the turning point (light, colour).
4 — a place with life and depth; the world reacts to events (darkens with the defeat, brightens with the power).
5 — the world is a character: its light, colour and detail carry the story as much as the hero does.

**Q6 · Gameplay readability (does it read as a game you could play?)**
1 — a slideshow of labelled pictures; no sense of control, space or rules.
2 — game furniture (HUD, scrolling) is present, but the character does not seem to *play* — things happen to him on cue.
3 — obstacles, hits, a power and a clear read as rules; you understand what would happen next.
4 — as 3, and the level has space (ground, jumps, distance) and the actions have cause and effect that a player would feel.
5 — it looks like captured gameplay of a good game; the HUD and the action agree at every frame.

**Q7 · Audiovisual impact (sound and picture together)**
1 — sound absent, wrong, or out of sync; or the picture ignores the sound.
2 — cues on the events, but thin; music indifferent to the beats.
3 — every event has a sound that fits it; the music supports the tone.
4 — as 3, with dynamics: the mix drops, holds or rises with the story (dread, silence, release); impacts have weight.
5 — sound and picture are one performance; the power-up moment is *felt* through the speakers.

**Q8 · Commercial suitability (would this sell the install to a PG owner?)**
1 — the product moment is unreadable or off-putting; a viewer would not know what was installed or why.
2 — the product moment is present but generic; the install reads as a label, not a change.
3 — the install is the clear turning point and its benefit (the chip) is legible; brand-safe.
4 — as 3, and the sequence makes the viewer *want* the power: the problem hurt, the fix relieved.
5 — a sequence you would put in a paid Reel as-is; brand, story and feel aligned; nothing to fix.

**Overall:** after the eight scores, the evaluator ranks the four clips 1–4 by preference and writes **one sentence per clip** on the single thing that most helped or hurt it. The rank is recorded separately from the scores and is not derived from their sum.

## 4. Part (iii) — technical constraints (PASS / FAIL, measured by code before the evaluator sees the packet)

| # | Constraint | Check |
|---|---|---|
| T1 | 9:16, 1080×1920, H.264/AAC MP4, 30 fps, no edit lists, moov first | `ffprobe` + the box walk (`runtime/loop/container.py assess_edit_lists`, promoted from case A-004) |
| T2 | critical text inside the platform safe box (65,288)–(888,1248) | `runtime.compositor.gates.check_text_bounds` over the clip's layout log (A, B, C) or over frame-measured boxes (D) |
| T3 | no Nintendo character, artwork or asset | human-eye inspection of the 10-fps contact sheet by the checker (not the evaluator) against the Lane A Stage-2c do/don't list |
| T4 | no forbidden claim; every on-screen string on the permitted list | string scan over the layout log; frame text-hygiene pass (D: every sampled frame, because the model could invent lettering) |
| T5 | duration 5.0–8.0 s; audio present, level-safe (−16 to −12 LUFS integrated, TP ≤ −1 dBTP) | `ffprobe`, `ebur128` |

A clip failing T1–T5 is repaired at the compositor layer if the repair is USD 0 and does not change the generated picture; otherwise it is evaluated with the failure declared on the scoring sheet.

## 5. Packet layout and record

```
experiments/RENTOK-CREATIVE-QUALITY-001/eval-packet/
  README-FOR-EVALUATOR.md      # §1 instructions, the event list, the rubric (§2–§3), the sheet
  CLIP-K.mp4 … CLIP-N.mp4      # the four clips, neutral names
  CLIP-K-10fps.png … CLIP-N-10fps.png
  SCORING-SHEET.md             # one table: clip × (R1–R8, Q1–Q8, rank, one sentence)
  SEAL.txt                     # sha256 of MAPPING.json + of each clip; the two seeds
  MAPPING.json                 # committed AFTER the scoring sheet; treatment → label
  TECH-CHECKS.json             # T1–T5 results per clip, run before delivery
```

The scoring sheet is committed verbatim, in the evaluator's own words, with the evaluator identified (session id or "customer"). No diagnosis is offered to the evaluator and no treatment is revealed until the sheet is committed. If the customer also scores, the two sheets are committed separately and never merged.

## 6. How the result is read (PROPOSED, decided before the data exists)

- **Primary reading:** the *rank*, and R1–R8 — a clip that fails a mandatory item is out regardless of Q scores.
- **Secondary reading:** per-criterion Q scores by treatment, read against the hypothesis:
  - if **B ≈ A** on Q3/Q4/Q6 (prompts changed, renderer fixed) → the prompt step was not where the intent was lost (consistent with 02);
  - if **C > A** on Q3/Q4/Q6/Q7 with the same renderer → direction + renderer primitives are where quality lives (cause A + the animation hand-off);
  - if **D > C** on Q2/Q4/Q5 but **D < C** on Q6/R8 → the method buys picture quality at the cost of "actual game"; the customer's requirement decides;
  - if **D fails R1 or R8** → the method is limited for this look (02's METHOD-LIMITED count changes from 0 to ≥ 1, honestly).
- **What one evaluator cannot establish:** a general winner. n = 1 evaluator × 1 unit; the reading above is directional and is written as such into the production-learning record.

## 7. Bias controls, stated

- Neutral labels, two independent seeded permutations, sealed mapping.
- The evaluator sees no cost, method or authorship, and no document from 01–05.
- The rubric anchors describe on-screen facts, not adjectives, to limit halo from picture quality onto "readability" and "commercial" scores.
- The rank is asked *after* the scores and recorded separately, so a high total cannot silently become "preferred".
- Clip length differences (5–8 s) are declared; if the Controller prefers equal lengths, all four are trimmed to the same event span before sealing.
