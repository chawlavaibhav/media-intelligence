# Five-stage question template v0.1 (reusable layer)

Status: PROPOSED, 2026-09-20, authorised by the Controller ("make the reusable questions a fixed list the system enforces"). Not yet wired into `/media-agency`; this file is the specification. The reusable questions below apply to every job; the producer adds job-specific questions under each stage. The Stage Controller does not let a stage close while a reusable question is unanswered or answered "unknown" without a recorded reason.

**v0.1 corrections (from Addendum D §7, the no-hindsight producer run):**
1. Line 1.4: the verification-method column is **mandatory per mandatory item**; a row without one blocks Gate 1.
2. New line 1.0: **the deliverable is produced by generative models**; any element a producer would solve by live filming must instead be solved by references, composition or a test. (A producer without this line correctly chose to film the presenter.)
3. Line 1.9/1.12: every `ask` is tagged **blocks** or **default-recorded, proceed permitted at this cost tier**; a checker scores "resolved before spend" on the blocking asks only.
4. Line 3.2: **Gate 3 refuses to close without a numbered hero frame**; a sentence such as "sells at a glance" is not an answer.
5. Line 3.10: the audition (≥ 2 candidates, the longest line, final pace, before plates) is the **answer format**, not a suggestion.
6. Line 2.6 and every "known risk" statement (4.1, 4.3): must carry a source id, a case id, or `fetch`; the producer input must supply ids for the risk list.
7. Checker rubric: lines 13 (verification method per requirement) and 14 (every fact sourced) are permanent; the checker receives the risk-evidence list for line 12 rather than trusting the plan's own label.

Answer sources: **preserve** (customer said it) · **ask** (customer must say) · **decide** (we choose, shown for veto) · **lookup-fact** (platform page, product page, customer assets — fetched, dated) · **lookup-canon** (accepted claim by id) · **evidence** (Registry cell, case note, MF prior) · **test** (a micro-qualification draw). Class: DET / RSR / LJ / HJ / EMC (Part 9 §3). Every answer records: value, source, who answered, verification method. A stage gate is evaluated by a session other than the one that answered.

## Stage 1 — Intent (gate: nothing invented, every mandatory item has a verification method)

| # | Question | Source | Class | Destination |
|---|---|---|---|---|
| 1.1 | What is the deliverable (type, count, formats, duration band)? | preserve / ask | DET | contract.deliverable |
| 1.2 | What is it for (ad / content / scene / demo), and what does the customer want the viewer to do or feel? | ask (default offered) | HJ | contract.objective |
| 1.3 | Is there a product, brand or person that must appear, and which of its features must be exact (marks, colours, label text)? | ask | DET | contract.distinctive_assets |
| 1.4 | Which events or facts are mandatory (the customer's own words)? | preserve | DET | contract.mandatory[] — each with a verification method |
| 1.5 | What is forbidden (claims, tone, content, competitors)? | ask / derive from sources | DET | contract.forbidden[] |
| 1.6 | Tone/register, with one example the customer accepts? | ask | HJ | contract.tone |
| 1.7 | Language(s) per surface (spoken, on-screen)? | preserve / ask | DET | contract.language |
| 1.8 | Where will it run (platform, placement)? | ask (default offered) | DET | contract.channel |
| 1.9 | Spend cap, deadline, approver? | ask | DET | contract.cap / deadline / approver |
| 1.10 | On what basis will the customer accept (3–6 statements decidable from the file)? | ask (drafted by us) | DET+HJ | contract.acceptance[] |
| 1.11 | Does anything in the request contradict itself, the platform, or the customer's other instructions? | derive | — | contract.flags[] — a flag blocks Stage 3 until resolved |
| 1.12 | Which of the above did we decide rather than the customer, and what is the cost of being wrong? | derive | — | contract.assumptions[] — high-cost assumptions are asked, not assumed |

## Stage 2 — Structure (gate: every fact has a source; nothing platform-specific is asserted from memory)

| # | Question | Source | Class | Destination |
|---|---|---|---|---|
| 2.1 | Exact pixel dimensions, duration limits, file specs per placement? | lookup-fact (platform page, dated) | DET | spec.formats[] |
| 2.2 | Safe zones / UI-occluded bands per placement? | lookup-fact | DET | spec.safe_zones[] |
| 2.3 | If an ad: hook window, brand-early expectation, ask placement, close-on-product — for this placement? | lookup-canon (sk_abcd_0006/0007/0010/0011/0019/0020/0021/0026; sk_ogx_0039) + lookup-fact for platform variants | RSR | spec.ad_structure |
| 2.4 | Which claims may be made, verified against which source (product page, packaging, customer document)? | lookup-fact | DET | spec.permitted_claims[] — every number/feature string-matched at Stage 5 |
| 2.5 | Which assets do we have (photos, logo, screens, references) and which are missing? | lookup-fact (customer assets, hashed) | DET | spec.assets[] / ask |
| 2.6 | Sound: muted-first? captions? loudness target per placement? | lookup-fact + decide | DET | spec.audio |
| 2.7 | Must each delivered format be composed separately (crop survivability)? | derive from 2.1/2.2 | DET | spec.per_format_composition = true unless proven otherwise |
| 2.8 | Is the information sufficient to proceed, or which dependency blocks? | derive | — | gate |

## Stage 3 — Creative (gate: a board exists; a non-author has answered the structure checklist against it)

| # | Question | Source | Class | Destination |
|---|---|---|---|---|
| 3.1 | What is the single proposition (one sentence)? | decide (veto) | HJ | plan.proposition |
| 3.2 | What is the hero, and in which numbered frame does it sell itself without copy? | decide + lookup-canon (sk_hop_sa_0026, PA-D7) | LJ | plan.hero_frame (a numbered frame, never a claim) |
| 3.3 | What is the opening frame (close-up / mid-action), and what event is in it? | decide + lookup-canon (sk_abcd_0007) | LJ | plan.board[1] |
| 3.4 | Where does the brand appear over time (first mark, in-context presence, spoken mention)? | decide + lookup-canon (sk_abcd_0010/0011/0012/0013) | RSR | plan.brand_timeline |
| 3.5 | What is the ask, in what words, on which surface (card / spoken), at what point? | decide + lookup-canon (sk_abcd_0019–0021, qa_abcd_0011) | RSR | plan.ask |
| 3.6 | What is the last frame? | decide + lookup-canon (sk_abcd_0026, sk_ogx_0039) | RSR | plan.board[last] |
| 3.7 | Is every mandatory event from 1.4 on a numbered board frame? | derive | DET | plan.board ↔ contract.mandatory |
| 3.8 | Do on-screen lines equal spoken lines wherever both exist? | decide + lookup-canon (qa_ogx_0073) | DET | plan.copy_deck ↔ plan.vo_lines |
| 3.9 | Copy zone per frame per format: where is text, and is it off hands, faces and product? | decide + spec.safe_zones + lookup-canon (CA-D2, sk_wcag_0001) | DET | plan.copy_zones[] |
| 3.10 | Voice: register, language, who casts it and on which line? | preserve (1.6/1.7) + evidence (MF P8, RO-05) | HJ | plan.voice (cast by ear on the longest line, before plates) |
| 3.11 | Composition, light, finish per key object (the compiled pack fields)? | lookup-canon (PA-D1–D6, PA-D8–D9, CA-D1–D11) | LJ | plan.visual_system |
| 3.12 | Cuts and holds: new information per cut; hold set by content; motion motivated? | lookup-canon (CA-D7/D10/D11) | LJ | plan.board[].hold |
| 3.13 | Which of 3.1–3.12 did the author answer with a claim rather than a frame or a line? | **non-author checker** | — | plan.reviews[] — a "claim" answer reopens the question |

## Stage 4 — Selection (gate: riskiest element tested first; every route has evidence or a test; balances read)

| # | Question | Source | Class | Destination |
|---|---|---|---|---|
| 4.1 | Which element of the board carries the highest generative risk (hands, objects in contact, falling objects, faces speaking, legible screens/text in motion, identity across shots, extend chains, non-English speech)? | evidence (case notes, MF priors) — **not the author's label** | EMC | plan.risk_order[1] — made and judged first |
| 4.2 | For each asset: which route, with what evidence status, at what price, from which pool? | evidence (Registry / routing map) + lookup-fact (price pins) | DET | plan.assets[].route |
| 4.3 | What has failed before on this route for this kind of shot? | evidence (`directional_notes`, cases, MF) | EMC | plan.assets[].known_failures[] |
| 4.4 | Is anything text, logo or UI to be generated? (Answer must be no; composite it.) | rule (LIMIT-TEXT) | DET | plan.composite[] |
| 4.5 | Voice: how many generations produce the voice? (Answer must be one file or one take.) | rule (002 HD-13b) | DET | plan.voice.source_count = 1 |
| 4.6 | Are VO durations measured before any shot duration is fixed? | rule | DET | plan.timeline.derived_from = measured VO |
| 4.7 | References: which identity/product stills anchor every shot (≤ 3–4 per route)? | evidence (vendor limits) | DET | plan.assets[].references[] |
| 4.8 | Pool balances: read (not attested) for every pool the plan touches? | lookup-fact (API) | DET | plan.pools[] |
| 4.9 | Expected spend vs cap, with one repair round? | derive | DET | plan.spend |
| 4.10 | Order of work: voice → riskiest shot → plates per format → board with measured VO → remaining clips → assembly? | rule | DET | plan.order |

## Stage 5 — Execution and verification (gate: every DET check ran and passed; every HJ item has a named judge; a flagged file is not a deliverable)

| # | Question | Source | Class | Destination |
|---|---|---|---|---|
| 5.1 | Do all mandatory strings appear byte-exact where the deck says? | code | DET | qa.exact_text |
| 5.2 | Text bounds, contrast ≥ 4.5:1 on real pixels, disjointness, contain-fit for product proofs? | code (existing gates) | DET | qa.geometry |
| 5.3 | Does any text, card or mark intersect the subject mask (hands, faces, product) in any format? | code (subject box) | DET | qa.obstruction |
| 5.4 | Do any two VO lines overlap; does the last line end before the film; any silence > 0.8 s inside a line? | code (`check_vo_schedule`, `silencedetect`) | DET | qa.audio_schedule |
| 5.5 | Loudness and true peak within the declared target? | code | DET | qa.loudness |
| 5.6 | Duration inside the placement limit; each format its own composition; safe zones respected? | code | DET | qa.formats |
| 5.7 | Any generated lettering, logos or UI in sampled frames? | code (frame hygiene) or named human | DET/HJ | qa.frame_hygiene |
| 5.8 | Every mandatory event visible on a frame; hero in first and last frame; brand timeline as planned? | non-author checker on the assembled film + contact sheet | LJ | qa.structure |
| 5.9 | Identity stable across shots; mouths closed under VO; voice one source by ear? | named human | HJ | qa.continuity |
| 5.10 | Which stage does each failure belong to (1 intent / 2 structure / 3 creative / 4 selection / 5 execution)? | **non-author** | — | qa.failures[].stage — the job re-enters at that stage |
| 5.11 | Release? | human (C-8) | HJ | release |

## Generated questions (job-specific layer)

For each mandatory event (1.4), each distinctive asset (1.3), and each board frame (3.3–3.6), the producer writes one job-specific question in the inverse form: *what must the viewer perceive → what observable property carries it → which controllable parameter produces it → which route can produce it → what would break it*. Each such question records its destination (a frame, a prompt field, a route choice, or a check). A generated question that informs no decision is deleted with a note.

## Learning into the template

A question is added to this file only when a recorded rejection shows the failure was not covered by an existing line, with the case id cited next to it. A question is removed when three consecutive jobs answered it identically with no effect on a decision. Answers, not questions, accumulate per job class as defaults.
