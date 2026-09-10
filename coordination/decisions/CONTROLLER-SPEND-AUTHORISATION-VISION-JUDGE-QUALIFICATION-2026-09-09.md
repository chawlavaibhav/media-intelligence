# Controller — Spend Authorisation: vision-model judge qualification run — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION. **Role:** Writer Controller, recording the human Controller's words.

## 1. Authority — the Controller's words

Put to the Controller: the vision-model judge is built and tested offline; on the 210 verdicts on disk it would make 192
calls on the Gemini key; it cannot run until a Gemini API price page is pinned and a small cap is signed.

> **"allow vision model to judge. approved."**

## 2. Scope

One qualification run of `instruments/vlm_screen.py` via `qualify_screen.py` over every sealed, Controller-judged
artifact (14 runs, 209 judged trials; 192 model calls: 117 images, 75 videos × 3 frames = 225 frames; 16 audio files are
`cannot_judge` and cost nothing). Judge model `gemini-3.5-flash` on the Gemini Developer API with the key named
`GOOGLE_API_KEY` (Controller decisions: Gemini-named models on the Gemini key; GCP over fal). Price pinned:
`price-pins-2026-09/gemini-api-judge/PIN-INDEX.yaml` (USD 1.50 / 1M input tokens, USD 9.00 / 1M output, 1,548 tokens
per image allowance). **Dry-run estimate USD 1.83.**

Outputs: `SCREEN-RESULTS.yaml` beside each run's RESULTS.yaml and `QUALIFICATION-REPORT.yaml` (agreement, Cohen's
kappa, per-question/per-route confusion, every disagreement with the Controller's note). The instrument stays
`screened_not_qualified` until the Controller freezes `SCREEN-QUALIFICATION-CRITERIA-v0.yaml` and the report meets it;
no Registry row comes from it either way.

## 3. Cap and hard limits

Cap **₹480 = USD 5.00** (`screen_cap_usd`), max 200 calls; reservation-first (the runner stops before any call whose
reservation would cross the cap); 0 retries; key by name only; the judge never sees the Controller's verdicts.

## 4. Not authorised

Any second pass, another judge model, or screening of unjudged artifacts (the text-to-video lane's clips are screened
only after the Controller has judged them).
