# ADDENDUM A — Canon interrogation: assessment of the "wrong-question" hypothesis

Date: 2026-09-20. Source of the hypothesis: the ChatGPT/Vaibhav handoff ("we are asking the wrong questions to Canon"). Evidence: the audit's council reports (06, 09, 12, 14, 15) and the repository at `main @ 3bb9a3c`, Cumin job `de1f978` / `86ec183`. Labels: OBSERVED / INFERENCE / HYPOTHESIS / UNKNOWN. Read-only; no provider called; no spend.

## 1. How Canon interrogation actually works (OBSERVED)

There is no interrogation step. `runtime/canon/normalize.py` maps the deliverable kind to modality / operation / advertising flag and reads only `language` and `market` from the brief. `runtime/canon/packs.py` selects pack ids from `canon/packs/pack-triggers-v0.yaml` by those fields and injects, verbatim, the pre-compiled text of any selected pack that exists (2 of 10). No query is formed, nothing is ranked, no source is read, and Canon is not consulted again after a failure. The only model-generated Canon queries ever run were inside the sealed EVAL-037 BM25 tool (controlled lane: 53 searches, 1 full read; unbounded lane: 16/18 context overflows). CANON-015's retriever is unmerged.

The two compiled packs are themselves question-shaped: 21 decisions, each `question / DEFAULT / CHECK` (e.g. PA-D7 "Does the imagery earn its space commercially? … State in one line what the hero image sells at a glance; if that line needs the body copy, the image fails"). These are static per pack, cover lighting and composition only, and are answered by the author with a verdict token. Cumin rendered 20 "pass", 1 "n-a".

## 2. What the real questions and retrieval outputs looked like on Cumin (OBSERVED)

`JOB.yaml @ de1f978` L112–117: ten packs selected, two injected, eight `missing_domains` (`commercial_communication`, `critique_and_effectiveness`, `camera_and_spatial_grammar`, `editing_pacing_and_short_form`, `concept_and_distinctiveness`, `colour_and_visual_register`, `typography_and_copy`, `indian_indic_context`). Prefix 5,298 tokens, sha recomputed identical. By the documented BOOTSTRAP command the operator saw decision id + question + CHECK (4,520 chars); DEFAULT text and the 28 conflict rules were not printed. The plan carried the two packs' typed fields (finish per object, one window source, placement zone, attention order) and those held on the plates. No question about product role, opening, close, direction, voice register or VO-first timing was posed by anything.

## 3. Where important creative decisions remained unresolved (OBSERVED on the media, council 12)

The plan text said "product-led", "bowls in every beat", "never obstructed by text", "a noodle slips back into the bowl in the first second". The accepted plates and finals show: beat 1 = she eats, he is passive (no event); the rim-notch product argument is in no frame; beat 2 = 5.5 s of a static hand; beat 5 cuts in on an open mouth under the VO; end card from a borrowed photo of a different bowl finish and kitchen; 4:5 and 1:1 carry cards over the chopsticks; VO overlap 0.92 s and overrun 0.94 s. Eight of twelve defects were visible on plates, a contact sheet, a prompt string or by arithmetic before any clip was bought. The gap is between the plan and the accepted plates: acceptance was per asset, never on a board or a timeline.

Ranked by what the human rejected on: (1) proposition / product role / close / direction; (2) opening event; (3) voice register and casting; (4) timing derived from measured VO; (5) per-format composition and obstruction; (6) cinematography specifics. The handoff's §8 list (frame composition, subject scale, environment, lighting, attention hierarchy, camera, references) is mostly (1)–(2) and (6); lighting and composition were the parts that held.

## 4. Whether current Canon can resolve those decisions (OBSERVED)

| Decision class | Canon | Where |
|---|---|---|
| Structure: brand early/often/richly; open in action or close-up; ask after context; finish with the product; see-and-say | **yes** | `google-abcd-video-ads` sk_abcd_0005/0006/0007/0010/0011/0012/0013/0019/0020/0021/0026; `ogilvy-beyond-ch2` sk_ogx_0039; `hopkins` sk_hop_sa_0026; `miller-storybrand` sk_sb_c003_0011 — all accepted, all in the **uncompiled** `commercial_communication` pack |
| Composition / lighting / product finish | yes, compiled | PA-D1–D10, CA-D1–D11 |
| Camera, editing, holds, cuts | yes, partly compiled (CA-D7–D11); more in Grammar of the Shot/Edit, Murch, Ondaatje (uncompiled) | |
| Packshot on light ground | yes | `qa_lsmx_0039` (Q&A, excluded from production by four contracts) |
| Supers = VO wording | yes | `qa_ogx_0073` |
| Voice casting / register / naturalness | **no** — zero audio sources | coverage map `modality_base_packs.audio: []` |
| Text over a subject | **no** — 0 matching claims in 1,300 SK | council 06 §4 |
| VO-first timing | no (universal craft; MF `assemble.py` had it as code) | |
| Hands / chopstick grip / embossed mark fidelity | not a knowledge question — empirical model capability | micro-qualification |

## 5. Verdict on the hypothesis (INFERENCE)

Partly right, and the right part is stronger than stated. The system does not ask the wrong questions; it asks none, by design. The one question-shaped mechanism it has is answered by its author. The handoff's proposed sequence (decompose the communication problem → identify unresolved decisions → targeted questions → retrieve/interpret → resolve → translate into production fields → re-ask after failure) is the correct shape and can be built from parts already in the repository (Creative IR's `preserve/derive/decide/delegate/ask/flag` field model; the compiled packs' typed fields; the ~30 structure claims by id; CANON-015's retriever if a lookup is shown to lose value).

Where the handoff is weaker: it locates the quality loss in unresolved *visual* choices. The observed rejections were structure, voice, timing, obstruction and assembly first; lighting and composition held. The second audit's nine reference films do show a real cinematography gap (slideshow vs directed film), so the visual questions belong in the protocol, after the structural and timing ones. And no question protocol changes a decision unless a session other than the author answers it and a "no" gates spend: PA-D7 is the existing proof.

## 6. The alternative protocol on the existing architecture (RECOMMENDATION)

1. Completed brief with field operations (SPEC-01): every `decide` / `flag` field is an unresolved decision.
2. One targeted question per unresolved decision, in inverse form (viewer response → perceptual property → observable characteristic → controllable parameter).
3. Answer from: the ~30 structure claims by id (fit in context; no retriever); the compiled packs' typed fields; CANON-015 BM25 over accepted SK for camera/editing only if NODE 3 says the lookup loses value; MF priors and case notes for voice/timing; "not a knowledge question → micro-qualify" for hands, marks, mouths.
4. Write each resolved decision into the typed production fields the job record already has; build the six-frame board from accepted plates before any clip; derive beat durations from measured VO.
5. A fresh-context checker answers the ≤12-line structure checklist against the brief and the board; a "no" returns to P1.
6. After a failure, the failed check or frame becomes the next question.

Addendum B runs step 1–4 on paper for the Cumin brief and step 5 with a separate session.

## 7. How to test without ingestion or media spend (RECOMMENDATION)

- Paper experiment (Addendum B): existing pathway (the `86ec183` blueprint) vs decision-driven pathway on the same brief with Canon frozen at `3bb9a3c`; compare retrieved ids, decisions, specificity/feasibility, unresolved ambiguities, unsupported assumptions, route-infeasible requirements; two reviewers blind to pathway. Extend to the Nivaas and Upwork briefs before drawing a conclusion (n = 1 otherwise).
- Only if the plans differ materially on the dimensions the human rejected on: generate both through the same routes, cap ≈ USD 10, and judge the *media* blind with two non-author reviewers on first-pass acceptance, the known-rejection checklist, and the reference-film craft dimensions. Plan quality has already fooled this project once (EVAL-037 judged packages).
- Prerequisite: the judge-reliability packet (Addendum C).
