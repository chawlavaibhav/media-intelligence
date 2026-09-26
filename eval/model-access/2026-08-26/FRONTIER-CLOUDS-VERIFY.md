# Frontier Clouds — residual verification checklist

**Task:** EVAL-008 · **Date:** 26 Aug 2026 · **Status: SUPERSEDED IN PART.**

**Read `FRONTIER-CLOUDS-AVAILABILITY.md` first.** That is now the E8-C deliverable.

This file was originally the whole E8-C output, written when the service named "Frontier
Clouds" could not be identified from public evidence. **The Controller has since resolved the
identity: Frontier Clouds means the three hyperscalers — GCP, AWS and Azure.** The availability
pass has been done against all three.

What survives here is only the part that could not be closed from this session: **this
environment cannot reach AWS or Azure documentation.** Both were re-probed after the identity
was resolved and both answered `403`, along with `docs.aws.amazon.com`, `learn.microsoft.com`
and `ai.azure.com`. Only `cloud.google.com` was reachable, which is why the Google rows are
verified and the rest are not.

So the checks below need someone who can open a console. You can. This session could not.

---

## 1. Confirm the three Azure rows — the highest-value check

Each is currently **T2/T3**: a search tool read a Microsoft-owned page and summarised it. Open
your Microsoft Foundry catalogue and confirm, recording the **exact deployed version string**
for each.

| # | Model | What to confirm | Why it matters |
|---:|---|---|---|
| 1 | **GPT Image 2** (Must) | that `gpt-image-2` is deployable, not just `gpt-image-1.5` | It carries our single highest-value hypothesis — the Devanagari typography claim |
| 5 | **FLUX.2 [pro]** (Must) | that **FLUX 2 Pro** is deployable, and whether `[flex]` or `[klein]` are too | We selected `[pro]` specifically; a different variant is a different model |
| 18 | **MAI-Image-2.5-Pro** (Should) | deployable at **model version 2026-06-02 or later**, and that a region near you is enabled (**South India** is reported available) | This row went from "no route evidenced" to "available" purely on this finding. Confirm before relying on it |

## 2. Confirm what your credits actually cover

**The single most consequential unknown left in this task.** Credit grants routinely cover
language-model inference and exclude image and video generation — which is where essentially
all of this programme's cost sits. If media is excluded, the preferred-route ladder collapses
to fal and direct, and the budget picture changes completely.

Worth answering per cloud, because the answer can differ between them.

## 3. Check how your credits split across the three clouds

**Bedrock carries none of this roster**, and its own media models are being retired — Nova
Canvas has a published end-of-life of 30 September 2026, Nova Reel is Legacy. Credits weighted
toward AWS are therefore worth much less to this programme than a headline total suggests.

If most of the credit sits on AWS, that is worth knowing before a budget is approved, not after.

## 4. Two smaller Google questions

- **Does Veo 3.1 expose the advanced frame/extend/camera controls?** Google's pricing table
  lists them under **Veo 2** only. If 3.1 does not have them, Veo cannot serve the video-edit
  lane, which then rests entirely on Runway Aleph, HappyHorse and MiniMax H3.
- **What does Nano Banana Pro cost per image?** The image-output cell was not populated in the
  pricing table we read.

---

## What is already settled, and needs no further checking

The four Google rows — **Nano Banana 2, Veo 3.1 (and its Fast and Lite tiers), Nano Banana Pro
and Gemini Omni Flash** — have exact identities, GA dates and printed prices read directly from
Google's own pages in this session. They are the one part of the sourcing analysis that would
survive an audit as-is. Details in `FRONTIER-CLOUDS-AVAILABILITY.md`.
