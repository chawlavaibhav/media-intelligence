# QA CHECKLIST — run in full, record every row in `JOB.yaml` `qa.*`

Vocabulary per row: `PASS | FAIL | NOT_RUN | N/A` + one-line evidence. `NOT_RUN` is never `PASS`.
A FAIL blocks release until repaired (workflow §12) or the human explicitly accepts the deviation
(recorded verbatim). Use the repo's implementations; do not write a weaker one-off check.

## A. Pre-dispatch (USD 0) — `qa.pre_dispatch`

| # | Check | How |
|---|---|---|
| A1 | Canon gate over package + prompts | `python3 canon/gate/run_gate.py pre --package <pkg.md> --prompt-file <prompt.txt> --modality static_image [--product] [--dispatch request.json]` — LIMIT-TEXT (no text-surface word — poster, label, sign, banner… — in a plate or edit prompt without a deferral term; describe a supplied pack's printed face without those words), delivered-vs-declared, named-ratio; all 21 lines printed. The gate cannot express "label preserved from the reference"; that is a recorded gate limitation, not a prompt problem to work around silently |
| A2 | Pack check lines rendered by id | `PA-D1..D10`, `CA-D1..D11` each `pass / n-a / deviation:<brief clause>` in `blueprint.check_lines` |
| A3 | No critical string in a generation prompt | grep every prompt for every `intake.mandatory_text` value; in-scene text only if the job requires it and RR-2 evidence covers it |
| A4 | Route evidence status | every route `clean_observed` + `production_use_allowed: true`, or `manual_only` with the user's OK recorded, never `false` |
| A5 | Price pinned live | roster + pin present for every route (`python3 -m runtime.route.cli --plan …` succeeds without `no live pin`) |
| A6 | Spend cap | `spend.cap` stated by the user this session; Σ planned attempts × price ≤ cap |
| A7 | Pool liquidity read | a balance reading (value, read_utc, source) for every pool the plan touches; positive |
| A8 | Consent | any identifiable person in a supplied asset has a consent ref |
| A9 | Micro-qualification done | every `plan.micro_qualifications[]` item has a human gate verdict before its dependents are dispatched |
| A10 | TTAO clock | `ttao.job_start_utc` and `ttao.planning_complete_utc` stamped |

## B. Post-draw, every still — `qa.post_draw[]`

| # | Check | How |
|---|---|---|
| B1 | Stray lettering | frame scan: no unrequested letters anywhere — edges, reflections, background signage, labels. Nano Banana 2 drew paper-like text once; FLUX added an extra object once (RO-04, RO-08) |
| B2 | Product fidelity (supplied product) | side-by-side at equal width vs the customer photo: proportions within ~5 %, hue family unchanged, every label word readable and correct, no invented marks (PROFILE.md delivery checklist 1–3). FAIL twice → clean cut-out composite, tell the client early |
| B3 | Pack check lines on the artifact | PA-D1 finish declared / PA-D4 one source / PA-D5 grayscale separation / CA-D1 first-read / CA-D3 no accidental tangency / CA-D6 aspect justified |
| B4 | Hands / objects / faces where present | count fingers, count objects vs brief, face symmetry and eyes |
| B5 | Delivered vs declared | aspect, pixel dimensions, no silent upscale |
| B6 | Negative space where copy will sit | the plate leaves the declared copy zone clean |

## C. Composition (every rendered file) — `qa.composition[]`

Run `runtime/compositor/gates.py` in order; each call's result is a row:

| # | Gate | Rule |
|---|---|---|
| C1 | `check_text_bounds` | measured ink box inside canvas and container / token safe area; overflow fails closed — never clipped |
| C2 | `check_contrast` | minimum ratio over every sample behind the box meets the role threshold, or an opaque backing is added and re-measured |
| C3 | `check_fit` | creative proof `contain` by default; `cover` only with `declared_crop` + reason (reported) |
| C4 | `check_geometry` | radius / border / shadow / spacing from one `DesignTokens` source |
| C5 | `check_disjoint` | `headline, offer, code, cta, legal` regions do not overlap (min gap per tokens) |
| C6 | Exact copy byte-check | every rendered critical string == copy deck value, both scripts; `₹`, `%`, `&`, dates and codes included |
| C7 | Brand colours | background/accents == the brand hex values given |
| C8 | Export specs | every size present at exact pixels (1080×1080, 1080×1350, 1080×1920, WhatsApp 800×800 unless the brief says otherwise); Meta safe margins clear |

## C-final. Every delivered geometry, on the final rendered file — `qa.final_geometry[]`

FORMAT_SPECIFIC_REVALIDATION (case 002, HD-03/06/07/08): acceptance at one aspect does not transfer.
One row per delivered file — `{file, geometry: 1:1|4:5|9:16|WA|16:9|…, sha256, rows}` — and the rows
are run on that file, not inherited from the master:

| # | Check on the final file |
|---|---|
| CF1 | C1–C8 (bounds, contrast, fit/declared crop, tokens, disjointness, exact copy, brand colours, export specs) re-run on this geometry |
| CF2 | Subject / critical-object obstruction: no text or UI element sits over the product, face or hero object; contain-by-default for product proof |
| CF3 | Stray lettering and edge artefacts introduced by the adaptation (re-crop, re-scale, re-fill) |
| CF4 | Platform safe zones for this geometry (Reels UI band on 9:16; WhatsApp 800×800 preview crop) |
| CF5 | Hierarchy survives the fit: headline, offer, CTA still read in that order at this size (stack-level fit, not headline-only shrink) |

A geometry without its own row is not deliverable. The master's rows belong to the master.

## D. Video — `qa.video_frames`

Sample frames across the whole clip (first, last, and at least every 1 s; more around cuts).
List the sampled timestamps. The still's verdict transfers nothing.

| # | Check | On sampled frames |
|---|---|---|
| D1 | Frame text hygiene | no lettering in any frame: `python3 canon/gate/run_gate.py post --artifact <clip.mp4> --dispatch <request.json> --frames <dir of sampled frames> --modality video` plus `runtime/loop/frame_hygiene.assess` (any frame `text` → FAIL; no frames → NOT_RUN). The Cloud Vision detector is a paid call and is not authorised by default — the human-eye frame pass is the release check today. Kling sharpened blurred signage into letters once (RO-06) |
| D2 | Product drift | shape, colour, label across frames vs the accepted still |
| D3 | Identity drift | face / hair / clothing / room held across frames and across takes |
| D4 | Hands / objects | as B4, on frames where present |
| D5 | Face quality | eyes, teeth, symmetry at the largest face frame |
| D6 | Camera motion | matches the motivation declared (CA-D11); none where the brief forbids |
| D7 | Continuity / screen direction | CA-D9 across cuts |
| D8 | Crop / framing | subject not cut by the frame; 9:16 safe zones clear of platform UI |
| D9 | Physics | liquids, cloth, shadows plausible; no morphing |
| D10 | Speech | verbatim transcript vs the line (triage transcript), then a human ear: naturalness, cadence, accent, no inserted words (Omni inserted a word once, RO-03); long narration is not accepted on transcript alone (RO-05) |
| D11 | Audio sync / mix | lips vs audio; music ducked under speech; loudness within the delivery target |
| D12 | Delivered vs declared | duration, fps, resolution, codec |
| D13 | Contact sheet | `agency/jobs/<id>/qa/<asset>-contact.png` produced for every assembly |
| D14 | **Cross-clip voice continuity** (CROSS_CLIP_VOICE_CONTINUITY, case 002 HD-13) — required whenever 2+ clips represent one narrator/speaker; recorded in `qa.voice_continuity` | On the ASSEMBLY, by a human ear: (a) same perceived narrator identity across clips; (b) compatible accent and timbre; (c) delivery / cadence continuity; (d) no narration hole, restart or clipped word at any clip boundary. Per-clip transcript match (D10) is presence, not delivery, and does not satisfy this row. FAIL → repair at the audio/assembly layer (single voice source is a candidate pattern, not mandatory) |

## E. Delivery — `qa.delivery`

| # | Check |
|---|---|
| E1 | Every file in `outcome.assets[]` has path + sha256 + producing attempt id |
| E2 | Delivery note (customer work): "AI-generated, human-directed, made fresh for this order", models used, no US copyright on pure AI images, usage rights granted, brief-complete and files-sent times (PROFILE.md delivery checklist 8) |
| E3 | No tool or model name in any customer-visible or portfolio-visible text |
| E4 | Human verdict recorded verbatim; `outcome.status` set only from ACCEPT |

## G. Design reuse provenance — `plan.assets[].reuse` (DESIGN_REUSE_PROVENANCE, case 002)

| # | Check |
|---|---|
| G1 | Every reused treatment / component / asset has `source_asset`, `source_verdict`, `reuse_status ∈ {rejected, accepted_in_context, reusable_candidate}` recorded before use |
| G2 | `rejected` material is used only with `human_reapproval` recorded verbatim for this job |
| G3 | `accepted_in_context` material reused in a different aspect, plate, subject or context has `fresh_qa_required: true` and its new file carries full QA rows (C, C-final, B as applicable) |
| G4 | No reuse is described as "approved" on the strength of an earlier film or tile alone |

## F. Defect classes (for `qa.defects[]` and workflow §12)

`creative_direction` · `generation` · `audio` · `route` · `compositor` · `crop` · `text` ·
`product_fidelity` · `pacing` · `infrastructure`. An outage / 5xx / UNAVAILABLE / timeout is
`infrastructure` (`runtime/execute/provider_errors.classify`), never a model-quality failure.
