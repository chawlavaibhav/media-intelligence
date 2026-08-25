# Missing-pack supply routes — research only, zero acquisition

**Task:** R4 of `resources/tasks/RESOURCES-V1-OVERNIGHT-PROGRAM.md`
**Date:** 26 Aug 2026 · **Branch:** `work/resources-v1-overnight`
**Hard rule observed:** **0 new source-family acquisition. 0 downloads. 0 logins, accounts, forms,
terms acceptances or purchases. ₹0 / $0 spent.** Nothing below was obtained; everything below is a
route for the Controller to approve, modify or reject.

---

## How to read the rights statements here

Two of this project's most expensive lessons are about rights research: **a code licence is not a
media licence**, and **a description can be wrong for months while every integrity check passes**. So
every external claim below carries one of two labels:

- **`checked_tonight`** — I confirmed it from a search result in this session, and the confirmation
  is quoted or cited.
- **`NOT VERIFIED tonight`** — plausible, from my own knowledge or a secondary source. **It must be
  confirmed against the official distribution page by a human before any acquisition decision.**

I did not verify anything by visiting an official page directly: **the network egress proxy in this
session blocks direct fetches** (confirmed — `people.cs.pitt.edu` returned `EGRESS_BLOCKED`). Search
worked; direct official-document retrieval did not. That limitation is itself a finding: **official
rights verification cannot be completed from this cloud session** and must happen where the official
pages are reachable.

---

## A. Product reference pack — target ≥48 images = 12 products × ≥4 views

Serves 11 requirement rows. The highest-leverage pack in the matrix.

### A1 — Controlled first-party capture · **RECOMMENDED**

Photograph 12 physical products the project or the operator owns, ≥4 controlled views each: fixed
lighting, colour reference card in frame, recorded camera and lens, turntable or marked angles.

| | |
|---|---|
| Rights | **Cleanest possible.** First-party ownership; no third-party licence, no consent question. |
| Scale | 48 images is roughly one afternoon with a phone, a lamp and a colour card. |
| Cost | Effectively zero beyond time. |
| Fit | **Total.** It is the only route that guarantees the *same* product across ≥4 *controlled* views with a *known* brand colour — which is what `packaging_brand_colour_fidelity` actually needs. |
| Independence | Perfect: the pack cannot leak into any public training corpus we later test against. |
| Limitation | Products are whatever is to hand. Achieving ≥6 commercial categories and ≥50% Indian-market needs deliberate selection. |

**Why this ranks first.** Every public alternative fails on the same axis: it gives you *images of
products*, not *controlled views of a known product with a measured colour*. Reference conditioning
and edit preservation both need the reference to be something we control.

### A2 — Google Scanned Objects · **RESERVE**

~1,030 3D-scanned household items, scanned on a controlled rig with calibrated lighting; renderable
to arbitrary controlled views. Licence reported as **CC BY 4.0** — `checked_tonight` via search of
Google Research's own announcement, **not** confirmed against the distribution page.

| | |
|---|---|
| Strength | Genuinely controlled multi-view by construction, permissive licence, no people in it. |
| **Disqualifying limitation** | These are **generic household objects, not branded packaged goods**. They carry no wordmark and no brand colour spec, so they cannot serve `logo_wordmark_fidelity` or `packaging_brand_colour_fidelity` at all. |
| Verdict | Useful for `product_identity` and `reference_conditioning` only. A supplement to A1, never a replacement. |

### A3 — Amazon Berkeley Objects · **BLOCKED pending rights resolution**

~147k product listings, ~398k catalog images, and **8,222 listings with turntable sequences of 24 or
72 views** — structurally almost exactly what the pack wants.

**The blocker is a licence contradiction, found tonight.** `checked_tonight`: the AWS Open Data
registry reports **CC BY-NC 4.0** while the dataset's own documentation is reported as **CC BY 4.0**.
Those differ on the one axis that matters for a commercial product: **NC forbids commercial use.**

**This is exactly the trap that caught PVP** — where a search asserted the dataset was MIT and that
turned out to be the repository's *code* licence. I am not resolving it, and I am not guessing which
statement governs. A human must read the actual licence file in the actual distribution before this
route is opened. Until then: **blocked, not rejected** — if it resolves to CC BY 4.0 it becomes the
strongest public product route available.

**Do not assume e-commerce catalog photography is usable simply because it is public.** ABO is a
deliberate research release; ordinary retail catalogue imagery is not, and scraping it is not a route.

---

## B. Person reference pack — target ≥32 images = 8 identities × ≥4 views

**The highest-risk pack in the project.** Flagging privacy and biometric implications explicitly, as
the runbook requires.

### B1 — Consented internal capture · **RECOMMENDED**

8 consenting colleagues or contacts, ≥4 controlled views each, with **written consent naming internal
model-evaluation use, retention period and withdrawal process**.

| | |
|---|---|
| Rights | The only route where consent is unambiguous, because we obtain it directly. |
| Privacy/biometric | Real, and handled properly: facial images are biometric data in several regimes. Consent must be specific, recorded next to the media (storage class B), and revocable. **Losing the consent record makes the media unusable even if the media survives.** |
| Cost | Time and goodwill. |
| Limitation | Requires a human. **I cannot obtain consent and must not try.** |
| Blocker | `ACCESS / LEGAL` — a human permission decision under `shared/AUTONOMY-POLICY.md`. |

### B2 — Purpose-created synthetic identity references · **RESERVE, and there is precedent**

Generate a small set of consistent fictional identities and use them as references.

**The precedent is in our own history.** The legacy `media-factory` spike did exactly this: its
`brand.json` defines the recurring character as a *"Pixar-style 3D animated character"* described
entirely in prose. **It used a described fictional identity, not a real person** — and its 64 scored
generations still surfaced real identity failures ("face drift — younger, streak moved").

| | |
|---|---|
| Rights/consent | No real person, so no consent and no biometric exposure. |
| **Scientific caveat** | A generated face is not a photographed face. Whether identity-preservation results on synthetic references transfer to real people is **an open question, not an assumption.** It must be stated in any Registry entry derived from it. |
| Circularity risk | If the references come from the same generator family being tested, the test is rigged. References must come from outside the tested roster, and that constraint must be recorded. |
| Verdict | A legitimate fallback that de-risks consent entirely, at a stated cost in external validity. **Eval decides whether that trade is acceptable — not Resources.** |

### B3 — Public face datasets · **REJECT**

| | |
|---|---|
| Verdict | **Reject, not defer.** |
| Why | Consent for research collection is not consent for evaluating commercial generative systems. Facial data is biometric under several regimes; most such datasets carry redistribution and use restrictions; several well-known ones have been withdrawn by their creators over exactly these concerns. |
| Runbook rule | *"Do not acquire random public people's faces tonight."* I did not, and I am recommending it stays that way. |

**Explicitly recorded:** the 19 committed `spike/guddu/` images were the most plausible existing
candidate for this pack. **They are not one** — I opened them; they are AI-generated illustrated
story frames with no identifiable person. See the legacy reconciliation.

---

## C. Clean AV pack — target 36 clips = 24 single-speaker + 12 two-speaker

**The most blocked pack, and tonight's research made it look worse, not better.**

### The finding: the AV gap is harder than the audio gap

Public **audio** corpora for Hindi/English/Hinglish do exist — `checked_tonight`, search surfaced
HiACC (Hinglish adult and children code-switched, ~5.24 hours) and the Multilingual & Code-Switching
ASR Challenge set. But our requirement is **audio-visual**: lip-sync and two-speaker turn assignment
need to *see the speaker's face*.

Three problems compound:

1. **Audio-only does not serve the lane.** Four of five speech capabilities need video of a speaking
   face. An audio corpus serves `spoken_language_correctness` and nothing else.
2. **Licence.** HiACC is reported as **CC BY-NC 4.0** (`checked_tonight`). NC is a live problem for a
   commercial product, exactly as with ABO.
3. **Faces bring B's problems back.** Any AV corpus showing identifiable speakers carries the same
   biometric and consent exposure as the person pack, plus voice, which is separately protected in
   several regimes. **Audio rights and voice/identity permission must be recorded as separate facts**
   — the registry's six-fact rights model already supports this.

And nothing public reliably ships **turn boundaries with speaker attribution**, which the 12
two-speaker clips explicitly require.

### C1 — Controlled recording with consent · **RECOMMENDED**

Record 36 clips with consenting speakers: 24 single (8 English / 8 Hindi / 8 Hinglish) and 12
two-speaker (4 / 4 / 4). Transcribe them, mark turn boundaries, record consent for **both** the
speaker's likeness and their voice.

| | |
|---|---|
| Rights | Clean by construction, including the voice permission that public sources rarely give. |
| Fit | **Total**, and the only route that reliably yields verified transcripts *and* turn boundaries. |
| Cost | The largest manual effort of any pack: recording plus transcription plus turn annotation, in three language conditions. |
| Bonus | Deterministic perturbations — a known 120 ms audio shift, a swapped speaker channel — are trivial once clean originals exist, and they are the only *exactly-known* ground truth in the whole speech family. |
| Blocker | `ACCESS / LEGAL` — human consent decision. |

### C2 — Creator-permissioned AV · **RESERVE**

Approach specific creators whose material fits and obtain written permission covering media, audio
and voice.

Realistic and slow: it is per-creator negotiation, transcripts and turn boundaries still have to be
produced by us, and the Hinglish balance is unlikely to fall out naturally. Worth pursuing only if
C1 is impossible.

### C3 — Public AV corpora · **BLOCKED**

Every candidate reviewed fails on at least one of: research-only or NC terms, no turn boundaries, no
Hinglish, or unresolved biometric/voice exposure. **No specific public AV corpus is recommended, and
none should be acquired on the strength of tonight's research** — all licence positions here are
`NOT VERIFIED tonight` and the egress block prevented official confirmation.

---

## D. Commercial creative bank — target 80 = 40 static + 40 video; 60 active + 20 reserve

Shared by Eval's creative evaluator family and Canon's Experiment B. **One bank, not two.**

### D1 — First-party and permissioned creative · **RECOMMENDED**

Commercial creative the operator produced, commissioned or can obtain written permission to use
internally — including the operator's own client work if those clients permit it.

| | |
|---|---|
| Rights | The only route with a clean answer. Ad creative is dense third-party IP: brand marks, licensed music, talent likeness and stock imagery are often *separately* licensed inside one asset. |
| Fit for the Indian-market target | Strong — a route through Indian businesses naturally produces Indian-market assets. |
| Limitation | Reaching 80 assets across ≥6 categories with a 40/40 static-video split takes real relationship effort. |
| **Selection rule Resources will enforce** | Assets are selected on **category, media type, market/language, duration, platform** — never on whether Canon predicts they are good or bad. Selecting by the theory under test is the circularity this stream exists to prevent. |

### D2 — Pitt Image and Video Ads · **BLOCKED — human decision, and the closest public fit**

64,832 image ads and 3,477 video ads with rich annotation. `checked_tonight`: the official readme
says **"To obtain the dataset for research purposes, please email us."**

| | |
|---|---|
| Blocker | An **email request gate** — a human permission decision. I may not send it, and the Autonomy Policy is explicit that a worker may not accept terms or seek permission on the user's behalf. |
| Why it is still worth a decision | It is the only public candidate that addresses this pack at all, and its **annotation zips are separately downloadable** if metadata-only use is ever wanted. |
| Caveats if it is opened | Research-purpose framing may not cover commercial-product evaluation; the ads themselves carry third-party brand copyright; and it is US-weighted, so it does not serve the ≥50% Indian-market target. |
| Verdict | **Worth putting to the Controller as a yes/no.** It is the single blocked source where reopening has a real argument behind it. |

### D3 — AVA · **REJECT**

Explicit site terms prohibit robots, reproduction and aggregation, and photographers' copyright is
expressly reserved. This is an explicit prohibition — the category current policy treats as a hard
limit, and one that no worker may waive. Not close, and it was never an advertising source anyway.

---

## Summary

| Pack | Recommended route | Reserve | Blocked / rejected |
|---|---|---|---|
| Product ≥48 | **A1 controlled first-party capture** | A2 Google Scanned Objects (no brands) | A3 ABO — licence contradiction unresolved |
| Person ≥32 | **B1 consented internal capture** | B2 synthetic identities (external-validity cost) | B3 public face datasets — reject |
| AV 36 clips | **C1 controlled recording with consent** | C2 creator permission | C3 public AV corpora — none recommended |
| Commercial 80 | **D1 first-party / permissioned** | — | D2 Pitt Ads — email gate, worth a decision; D3 AVA — reject |

**The pattern is not an accident.** In all four packs the recommended route is *controlled or
permissioned first-party material*, because all four requirements demand something public datasets
structurally do not provide: **the same subject, under conditions we control, with rights we can
state.** A public dataset gives you pictures. These capabilities need references.

**All four recommended routes are blocked on the same thing: a human decision.** Consent, permission
and capture are not worker-autonomous actions, and none of them was attempted tonight.

## What I did not do

No download, no login, no account, no form, no terms acceptance, no purchase, no email, no scraping,
no collection of any person's face or voice. No route above was exercised. Every external rights
statement is labelled `checked_tonight` or `NOT VERIFIED tonight`, and **no `NOT VERIFIED` claim may
be relied on for an acquisition decision** until someone confirms it against the official
distribution — which this session's network policy prevented.

## Sources consulted tonight

- [Pitt Image and Video Ads — official readme text, via search](https://people.cs.pitt.edu/~kovashka/ads/readme_images.txt)
- [Scanned Objects by Google Research](https://research.google/blog/scanned-objects-by-google-research-a-dataset-of-3d-scanned-common-household-items/)
- [Amazon Berkeley Objects — AWS Registry of Open Data](https://registry.opendata.aws/amazon-berkeley-objects/)
- [ABO: Dataset and Benchmarks for Real-World 3D Object Understanding (CVPR 2022)](https://openaccess.thecvf.com/content/CVPR2022/papers/Collins_ABO_Dataset_and_Benchmarks_for_Real-World_3D_Object_Understanding_CVPR_2022_paper.pdf)
- [HiACC: Hinglish adult & children code-switched corpus](https://www.sciencedirect.com/science/article/pii/S2352340925006109)
- [Multilingual and code-switching ASR Challenge Dataset (OpenSLR 104)](https://www.openslr.org/104/)
