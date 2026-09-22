# PART 15 — RECOMMENDED ARCHITECTURE

RECOMMENDATION throughout, argued from Parts 6–14. It neither preserves the existing architecture nor replaces it: it keeps the sub-3 % of the repository that produced every accepted asset, removes the policy and the ritual that blocked and faked knowledge use, and inserts the one mechanism that has evidence from both human-factors and LLM research — a short, binary, instance-level confirmation at a defined pause point, answered by something other than the author, gating spend. Two of its elements are conditional on Part 16 results and are marked so.

## 1. The shape in one paragraph

A **single-threaded producing session** (the current `/media-agency` operator, lighter) does intake, creative direction, planning, dispatch and assembly — writes stay single-threaded (Part 8 E8). Before any paid draw it must produce a **one-page completed brief** (the twelve decisions of Part 9 §1.1, each marked asked / decided / derived) and, for video, a **six-frame board with measured scratch VO**. A **fresh-context checker** — a separate session given only the brief, the board and a ≤12-line binary structure checklist, never the job transcript or the skill — answers the checklist; disagreements and every "no" go to the **human at P1/P2** together with the spend request. Voice for VO jobs is cast by ear at **P3 before plates**. Every asset then passes through **one shared compositor/assembler** that calls the existing gates plus the missing deterministic ones, and a CF-flagged file cannot be a deliverable. The human releases (C-8). Learning enters as **code with a mandatory caller** or as a **directional note keyed by defect class** that the checker reads; nothing else counts as promoted. Canon stays as a **provenance library**; the ~30 advertising claims that matter are the cited sources behind the checklist lines; the Lab is frozen; the runtime loop is frozen until Part 14 NODE 5.

## 2. Components

| # | Component | Form | From the current system | New |
|---|---|---|---|---|
| 1 | **Intake → completed brief** | JOB.yaml `intake` extended with the twelve decisions; `proposition`, `product_role`, `cta`, `end_card`, `distinctive_assets`, `objective_clock`, `acceptance_basis` **non-null** (a "none" value requires a quoted brief clause, like `deviations`) | NR (Truth layer), brief.job.json, intake questions | MF's Truth / Craft / Spec split (council 02 §7): ask ≤ 8 things, decide and show the rest, derive specs |
| 2 | **Structure checklist (≤ 12 lines, binary, positive phrasing)** | e.g. "Product named as hero in the first and last frame? y/n"; "Brand mark or spoken brand by t ≤ 3 s? y/n" (platform default, editable); "A direction line exists (URL / verb)? y/n"; "The end card shows the product from the brand's own photography or an accepted plate? y/n"; "Supers never cross the subject in any delivered geometry? y/n"; "VO measured before shot durations were fixed? y/n"; "Voice cast by ear on the longest line at final pace? y/n"; "Muted test passes on the board? y/n"; "The story event the brief asked for is on a board frame? y/n"; "Every mandatory string is in the frozen deck? y/n" | AD_STRUCTURE_MINIMUM candidate; CA-D1/D2 attention-order questions; the 42 human rejection items | each line cites its source ids (sk_abcd_0010/0007/0019–0021, sk_ogx_0039, sk_hop_sa_0026, case ids) so provenance survives; re-recited late in the transcript (Part 8 A12) |
| 3 | **Fresh-context checker** | a separate model session; inputs: brief, board, checklist, the 3–5 negative examples (`qa_abcd_0010` etc.); outputs: y/n per line + one sentence each; recorded in `blueprint.reviews[]` | the empty `reviews: []` field; the non-existent Karl/Ezra personas | the only role separation the literature supports: different information, a checklist, no author rationale (CoVe factored form) |
| 4 | **Pause points P1 / P2 / P3** | P1 brief + checklist answers + spend cap in one screen; P2 six-frame board from accepted plates with safe-zone overlay and measured VO timeline; P3 voice shortlist (2–3 takes, longest line, final pace) — before plates | the 13:28Z start-of-job summary (already a pause point); micro-qualification | replaces plate-by-plate, clip-by-clip and take-by-take approvals; a REJECT at P1/P2 re-briefs, it does not "repair that layer" |
| 5 | **Shared dispatcher + compositor/assembler** | one module every job imports; calls `check_text_bounds`, `check_contrast`, `check_fit`, `check_geometry`, `check_disjoint`, `check_vo_schedule`, frame hygiene; adds subject-box obstruction, loudness/true-peak, narration-hole, safe-zone-per-template, per-geometry composition, all-pool balance reads, attempt-id lock; rule: CF-flagged ⇒ not a deliverable | per-job `dispatch.py` / `compose.py`, `runtime/compositor/*`, `pools.py`, `provider_errors.py`, `price.py` + pins, ledger | the running code becomes the tested code; the gates gain a mandatory caller |
| 6 | **Release** | human ACCEPT only (C-8); verbatim verdict capture; two-clock timing; human-minutes recorded | as today | add the blinded second reviewer when E6 requires |
| 7 | **Learning** | `check_case.py` gains substance: every `promoted_now` id must resolve to a caller on the mandatory path; every candidate re-derived must reference the prior id; a cross-case index keyed by defect class; K7/K13/K14 in the vocabulary; MF priors ported as directional notes with `checked:` fields | production-learning cases, sync skill | the checker reads directional notes by defect class at P1 |
| 8 | **Canon** | provenance library; the checklist's cited ids; PA-D1/D2/D4/D5 as typed prompt fields; LIMIT-TEXT clause unconditional; the two packs' Q + self-CHECK ritual retired; no new pack in that form; `commercial_communication` compiled **only in checklist form and only if NODE 2 says g > f** | corpus, packs, trigger table, gate | delete WORKFLOW L118-119; C-10 reworded: "no *pack* without a decision; reading is never forbidden" |
| 9 | **Registry / routing** | price, format, latency, reliability table; `directional_notes` per cell quoted at route time (cases + MF); Gemini TTS rostered; RR-12 demoted; liquidity read, not attested | as today | claims relabelled to what the rows measure |
| 10 | **Operator skill** | progressive disclosure: name/description → stage on demand; creative stage first; PROFILE.md replaced by a one-page "what we sell / what is proven"; four instruction conflicts fixed; red-flag table gains creative rows; expert content ≥ 30 % of what is loaded at the creative stage | the five skill files | target ≤ 15 k tokens before the brief (from 60–80 k) |
| 11 | **Runtime loop, Lab, Q&A corpus, bindings, ontology, governance prose** | frozen / archived per Part 10 | — | — |

## 3. Why this and not the alternatives (Part 11)

- Not **A** (human CD) as the product: it is the observed ceiling on quality and the observed floor on human attention (1–8 h/job; break-even ≤ 1.7 h). A remains the fallback for taste the checklist cannot carry.
- Not **B** bare: a strong model under a tutorial brief and "proceed on the brief" produced a tutorial; a checklist the author answers is PA-D7 again. B + a non-author checker + gates on the path *is* this architecture.
- Not **C** as is: Parts 5, 6, 12.
- Not **D**: the ~30 claims fit in context; retrieval over 7 MB adds near-miss crowding and costs 2.5× for a tie; nothing to rank.
- Not **E** as a five-agent pipeline: MAST; ≈ 15× tokens; only the checker role has evidence; writes stay single-threaded.
- Not **F**: no labels, no qualified judge. NODE 7 later for one or two narrow judgments.

## 4. What it does to the observed failures (INFERENCE; the test is Part 16)

| Observed failure | Where it is caught in this architecture |
|---|---|
| Cumin tutorial / no CTA / no end card / brand late (DF-07) | intake non-null fields + checklist lines 1–4 answered by the checker; human sees "no" at P1 before USD 0 |
| No hook event; product argument in no frame; she eats in beat 1 | P2 board from accepted plates (visible on `plate-A` / `plate-B` — Part 6 §3.5) |
| Voice register wrong; 26 takes | P3 before plates; 2–3 candidates on the longest line; house default recorded after the first accepted job |
| VO overlap / overrun; timeline before VO | measured VO at P2; `check_vo_schedule` on the mandatory path |
| Text over subject; flagged files shipped | obstruction gate with a subject box; CF-flagged ⇒ not a deliverable |
| 002's 13 single-frame defects | shared compositor; no job can import a gateless rasteriser |
| Robotic long-form TTS chosen on a short-line cell | `directional_notes` (MF P8, RO-05) quoted at route time; P3 on the *longest* line |
| Learning re-derived under new names | `check_case.py` substance checks; class-keyed index |
| 60–80 k tokens before the brief | ≤ 15 k; creative stage first |
| Approvals at string/plate/take level | three pause points; component approvals removed |

## 5. What it does not fix (stated plainly)

- Taste the human articulates only after seeing a film ("competent, not extraordinary") — P2 shortens the loop; it does not remove it.
- Model behaviour: embossed marks, hands, mouths, extend decay — micro-qualification and references reduce, do not eliminate.
- Voice naturalness without a human ear — until NODE 7.
- The commercial promise: 24 h / 4 h, VO standard, product-photo-in-scene — this architecture makes the clock *measurable* and the VO *castable*; it does not make the promises true. The first paid order does.
- Owner economics: human minutes per job fall (INFERENCE: from 39 decision points / 3 jobs to ≈ 3 pause points + release), but revenue is USD 0.

## 6. Conditional elements

| Element | Adopt if | Otherwise |
|---|---|---|
| Compile `commercial_communication` in checklist form | NODE 2: g > f by unanimity | checklist lines cite Canon ids; no pack |
| Job-time assembly of ~2.5 k tokens of doctrine from NR + objective | NODE 3: e < b | keep the trigger-table lookup for the typed lighting fields only |
| Cheaper model for first drafts | NODE 4: weak+b ≈ strong+b | strong model throughout |
| Second reviewer on every release | NODE 0: κ < 0.6 | author-judge + checker |
| Narrow trained judges (tutorial-vs-ad; naturalness) | NODE 7 labels exist | human at P1/P3 |
