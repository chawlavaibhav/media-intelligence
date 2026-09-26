# E8-B — Model roster, decided before sourcing

**Task:** EVAL-008 · **Date:** 26 Aug 2026
**Status: FROZEN for this task.** Written and committed **before** any sourcing analysis existed.
**0 API calls · ₹0 spent · no account created · no Registry row.**

---

## The one rule this document obeys

**Nothing here was decided because a model is easy or cheap for us to reach.**

The user has credits on a service they call *Frontier Clouds* and access to *fal*. Those
are routes to models. They are not reasons to test a model, and they are not reasons to
skip one. This document was completed and committed to git before the sourcing documents
were written, so the ordering is checkable rather than merely asserted — see
`EVAL-008-CONTROLLER-BRIEF.md` for the commit evidence.

Where sourcing facts were unavoidably encountered while researching capability, they were
recorded in `MODEL-UNIVERSE.md` and **not used** as selection reasons. Two entries below
are on the list despite a known access problem, and one is excluded despite being easy to
reach — both are called out explicitly, because that is what makes the rule real.

---

## What the three levels mean

| Level | Test says |
|---|---|
| **Must test** | Leaving it out leaves a hole. Either a frontier we cannot see, or a way of producing work we would have no evidence about at all. |
| **Should test** | A differentiated challenger, a specialist, a cost frontier, or a control arm that makes another model's result interpretable. |
| **Reserve** | Genuinely relevant, but currently answers a question another selected model already answers. Listed in `MODEL-UNIVERSE.md` with the promotion condition. |

There is deliberately **no target count**. The list got short by removing models that
answer the same question, not by hitting a quota.

---

## Must test — 15 entries

Each row answers the required question in plain English: *what different thing will we
learn by testing this?*

### Image

**1. GPT Image 2 — OpenAI**
We learn whether a specific, falsifiable vendor claim survives our own battery. OpenAI's
material claims roughly 99% character accuracy including **Hindi and Bengali**. This
project already owns a 96-item Devanagari exactness battery whose right answers are known
by construction, built precisely because a model can produce text that is *subtly* wrong
and a checker can wave it through. This is the highest-value single measurement available
to us: it is cheap, the claim is specific, and either answer changes what we build.

**2. Gemini 3.1 Flash Image (Nano Banana 2) — Google**
We learn whether the cheap tier of a frontier family is good enough to be the production
default. This is a Cost-per-Accepted-Outcome question, not a quality-ranking question. It
is also reported to be built for identity preservation across edits, which is the thing
commercial product work actually needs.

**3. Seedream 5.0 Pro — ByteDance**
We learn whether a different training lineage produces different *acceptance* on
Indian-market commercial creative. Every other frontier image pick is US or European.
Aesthetic priors are not universal, and "accepted by the customer" is a human judgement,
not a benchmark. If lineage turns out not to matter, that is a genuinely useful negative
result and we can drop a vendor.

**4. Reve 2.1 — Reve AI**
We learn whether **editing a structure beats re-rolling a picture**. Reve plans an image
as addressable regions and edits one element without regenerating the rest. Every retry
we avoid is money saved, and this is the only commercial model whose API appears to expose
the structure/render separation that this project's own architecture assumes. If it works,
it is evidence about our design, not just about a vendor.

**5. FLUX.2 [pro] — Black Forest Labs**
We learn whether a model built specifically for instruction editing beats a general
frontier model doing editing as a side capability. Editing is the majority of real
commercial production work — the first image is rarely the delivered image.

**6. Qwen-Image-2512 / Qwen-Image-Edit — Alibaba (Apache 2.0, open weights)**
We learn what our marginal cost could be if we owned the image step, and whether an open
model can carry **multilingual in-image text** — reportedly its strongest capability and
exactly our hardest problem. If the answer is yes even at a lower quality ceiling, our
unit economics stop scaling with volume, which is a strategic change, not an optimisation.

### Video

**7. Seedance 2.0 Pro — ByteDance** and **8. Seedance 2.0 Fast — ByteDance**
Two rows, because one model at two price tiers is two workflows, and the gap between them
is the measurement. We learn **where the cost/quality knee is**: the point at which paying
more stops buying accepted outcomes. No other pair on the roster gives us that reading as
cleanly, because everything else about the two tiers is held constant.

**9. HappyHorse 1.1 — Alibaba**
We learn whether **one-pass multilingual dialogue video** can replace our compose-from-parts
route. It claims lip-synced dialogue in seven languages generated in a single forward pass.
If it works for our languages, a whole pipeline stage disappears. If Hindi is not among the
seven, that is the finding that justifies the voice + lip-sync route below. Its arena debut
was anonymous, which is unusually clean evidence — people preferred it before they knew
whose it was.

**10. Veo 3.1 — Google**
We learn the accepted-outcome rate of the market's default choice, and how far down its own
published cost ladder (full → Fast → Lite) acceptance survives. It is also our best-evidenced
model overall, so it makes a good reference point for interpreting everything else.

**11. Kling 3.0 — Kuaishou**
We learn whether a model can hold a person or a product **identical across several shots**.
An advert is not one clip. A model can be excellent per clip and useless across a 20-second
spot, and no per-clip benchmark will ever tell us that.

**12. MiniMax H3 (Hailuo 03) — MiniMax**
We learn whether **more references actually buy more consistency**. It accepts up to nine
reference images plus video and audio clips as conditioning, which makes reference count an
experimental variable we can turn. Nobody else lets us do that. This is the instrument for
the identity question, not merely another competitor in it.

**13. Runway Aleph 2.0 — Runway**
We learn whether **fixing footage is cheaper per accepted outcome than generating it**. Every
other video model on this list starts from nothing. Aleph edits a real take — relight, change
angle, swap an object — while preserving the original motion. For a client who already has a
shoot, that is a different business, not a better model.
*Known access problem, recorded and deliberately ignored for selection: a third-party source
says Runway API access moved to Enterprise-only in January 2026. That is a sourcing fact. It
does not change what we would learn, so it does not change this row. It is handled in
`ACCOUNT-ACTIONS.md`.*

### Supporting media — voice and lip-sync

The single most consequential capability observation in this whole task: **the video models
that generate speech natively document five or seven languages, and Hindi is generally not
among them.** The three rows below exist because of that, not out of completeness.

**14. Sarvam Bulbul v3 — Sarvam AI**
We learn whether an India-first voice model gets Hindi, Hinglish and Indian brand names right
where a global model does not. This is the same class of failure as the Devanagari image
problem, moved into audio, and our first product is Indian-market media in exactly these
languages. It is also the only candidate that documents **Hinglish code-switching**, which is
how Indian ad copy is actually written.

**15. ElevenLabs v3 — ElevenLabs**
We learn what "good" means for row 14. Without a strong global control arm, a Bulbul score is
a number with nothing to compare it against, and we would not know whether a failure is Hindi
being hard or that model being weak. **This row is a control, and saying so plainly is the
honest justification for keeping it.**

**16. Sync-3 — sync.so**
We learn whether **TTS plus lip-sync is the working route to Hindi dialogue video** — quite
possibly the *only* route, given the language gap above. It is also methodologically valuable:
because both the video and the audio going in are ours, we know exactly what was said, so some
correctness checks become deterministic instead of requiring a judgement model we have not yet
qualified.

> Counting note: 16 numbered entries, 15 distinct models — Seedance 2.0 appears twice as two
> workflow rows, following the existing rule that one Registry entry is one vendor + model +
> version + workflow.

---

## Should test — 10 entries

**17. Gemini 3 Pro Image (Nano Banana Pro) — Google**
Learns what the extra money buys, measured against row 2 on identical items. On its own it is
redundant; as a pair with row 2 it is one of the cleanest cost/quality readings on the roster.

**18. MAI-Image-2.5-Pro — Microsoft**
Currently reported #1 on blind-preference image *editing*. Learns whether "preferred" and
"usable in commercial production" are the same thing — they often are not. Kept despite
overlapping Reve and FLUX.2 because it comes from a lineage nothing else here shares. **If
its results track Reve 2.1's closely, move it to reserve** rather than keeping both.

**19. Ideogram V3 — Ideogram**
The typography specialist. Learns whether the specialist succeeds where the frontier
generalist fails. Its value is as **a fallback that is already measured** on the day GPT Image 2
disappoints on Devanagari — discovering we need it and then starting to evaluate it costs a
release cycle. **Justification for keeping it alongside row 1:** they share the hypothesis but
not the failure mode. One is a reasoning model checking its own output; the other is a model
trained specifically on text-bearing images. A shared hypothesis is only a reason to cut when
the *evidence* would be the same, and here it would not be.

**20. Recraft V3 — Recraft**
The only candidate emitting **native vector output**. Learns whether we can take type out of
the raster generator entirely for the design parts of a creative — a logo or a price flash
rendered as vector cannot misspell Hindi the way a diffusion model can. **Its risk is scope,
not redundancy:** if the product never takes on design deliverables, this row is wasted. That
is a Controller call, and it is the reason this sits at Should rather than Must.

**21. FLUX.2 [klein] — Black Forest Labs (open weights, Apache 2.0)**
Learns the small end of self-hosting: what quality fits on a consumer-class GPU. Different
economic question from row 6, which is about the capable end.

**22. Gemini Omni Flash — Google**
Learns whether a **conversational** iteration loop converges on an accepted outcome faster
than re-prompting. That is a question about the interaction pattern, not the pixels, and it is
the only row that asks it. Kept despite sharing Google's lineage with row 10.

**23. Wan 2.7 — Alibaba (open weights)**
Learns the true cost of owning the video step — honestly counted, including GPU hours and
engineering, not "free because the weights are free". No native audio.

**24. LTX-2 — Lightricks (open weights)**
Learns whether we can own the **native audio-video** step, not just the silent one. That is
what separates it from row 23; otherwise they would be one entry.

**25. Marey Realism V1.5 — Moonvalley**
Learns **what commercial safety costs in quality**. Trained only on licensed data. The
project's stated posture is internal-research-only and says the rights question must be
reopened before anything reaches a customer. On that day we will need this number and will
not have time to measure it. **Promote to Must the moment any output is intended to leave
internal research.**

**26. OmniHuman v1.5 — ByteDance**
Learns whether a spokesperson can be produced from **a single photograph plus audio**, with no
source video at all. Different input contract from row 16, therefore a different cost structure
and different failure modes.

---

## Redundancy pairs — kept, and why

The task requires that where two models answer effectively the same hypothesis, we either
justify both or demote one. These are the pairs, decided on evidence value alone.

| Pair | Shared hypothesis | Verdict |
|---|---|---|
| GPT Image 2 · Ideogram V3 | Text exactness in images | **Keep both.** Different mechanisms, so different failure modes; and one is the pre-measured fallback for the other. |
| Nano Banana 2 · Nano Banana Pro | Frontier image quality | **Keep both.** The pair *is* the cost/quality experiment. Neither is informative alone. |
| Seedance 2.0 Pro · Fast | Video quality | **Keep both**, same reason, and cleaner because everything else is held constant. |
| Reve 2.1 · FLUX.2 [pro] · MAI-Image-2.5-Pro | Instruction editing | **Keep Reve and FLUX.2; MAI at Should with an explicit demotion condition.** Reve's mechanism is structurally different; FLUX.2 is the dedicated editing family; MAI is the current preference leader from a third lineage. Three is one too many if two of them agree. |
| Veo 3.1 · Gemini Omni Flash | Google video | **Keep both.** Same vendor, different interaction model, and the interaction model is the measurement. |
| Wan 2.7 · LTX-2 | Open video economics | **Keep both.** LTX does native audio; Wan does not. Without LTX the open lane cannot answer the audio question at all. |
| Sync-3 · OmniHuman v1.5 | Getting a mouth to match audio | **Keep both.** Different inputs — existing video versus a single still — so different production routes and different costs. |
| Sarvam Bulbul v3 · ElevenLabs v3 | Hindi/Hinglish voice | **Keep both.** One is the subject, one is the control. |
| Vidu Q3 · PixVerse V6 vs Seedance Fast / Veo Lite | Cheap video | **Demote Vidu and PixVerse to reserve.** The cost frontier is already readable from cheap tiers of models we test anyway, without adding two vendors. |
| Cosmos 3 Super vs Qwen-Image / FLUX.2 [klein] | Open image economics | **Demote Cosmos to reserve.** Two open image rows already cover the large and small ends. |

---

## Excluded despite being currently prominent

| Model | Reason — and the category of reason |
|---|---|
| **Sora 2 (OpenAI)** | **Model viability.** Reported deprecated 26 April 2026, API shutdown 24 September 2026. A Capability Registry row for it would expire within weeks of being written, and the Registry is meant to be durable evidence. *Verify this date before the exclusion is treated as final.* |
| **Runway Gen-4.5** | **Superseded in-vendor.** Aleph 2.0 covers the capability we actually want from Runway. |
| **Imagen 4 family (Google)** | **Superseded in-vendor**, even though it is the best-priced thing we found today. Cheapness is not a hypothesis. |
| Nano Banana v1, Ideogram V2, Seedream 4.5, FLUX.1 Kontext, Veo 2/3, Kling 2.5, Hailuo 02, Seedance 1.5 | **Superseded in-family** by an entry already selected. |
| Midjourney | **Redundancy**, at reserve. Its aesthetic-ceiling hypothesis is real but weakly separable from the frontier picks. Its unclear production API is recorded separately so it is not mistaken for the reason. |

---

## Two consequences the Controller has to decide, not the Lab

**First — this roster is larger than the previously planned rig.** The earlier inventory
(`eval/v1/MODEL-WORKFLOW-INVENTORY-2026-08-26.md`) reserved a **cap of 19** endpoint/workflow
slots across five lanes, with 0 filled. This roster names **26 Must/Should rows**. Both numbers
are honest: that one was a capacity plan, this one is a measurement plan built from current
capability evidence with no cap imposed. **They must be reconciled before any paid run**, and
the reconciliation is a budget decision. The Lab's view, offered as a recommendation and not a
decision: the 15 Must rows fit inside 19 with room for the four highest-value Should rows
(Nano Banana Pro, Ideogram V3, Gemini Omni Flash, Marey), and the rest can wait for a second
wave.

**Second — this roster licenses nothing.** No model here is qualified, ranked, admitted, or
entered in any Registry. No checker has ever been run in this project, so we currently have no
qualified way to judge a generated image at scale. **Choosing what to measure does not create
the ability to measure it.** That dependency is unchanged by this task.

---

## What we would still not know after testing all of this

Worth stating so it is not discovered later as a surprise.

- **Whether our judge is trustworthy.** Every capability number depends on a checker, and none
  has been qualified. A roster does not fix that.
- **Whether one accepted outcome predicts the next.** These are single-shot capability
  measurements; production is repeated work under varying briefs.
- **Whether any of it is legal to show a customer.** Only Marey and, by claim, Veo address
  provenance and indemnity. That question sits outside the Capability Lab.
- **Exact versions.** Current public sources disagree on version numbers for FLUX.2 [klein]
  (4B or 9B), LTX-2 (2.0 / 2.3 / 2.5), Wan (2.6 or 2.7), Seedream (4.5 or 5.0), and on whether
  MiniMax H3 is open-weights. **Every row must be version-pinned from the provider's own
  catalogue before it is measured**, or the Registry row will not mean anything.
