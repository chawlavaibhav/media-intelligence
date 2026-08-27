# Controller EMP-001 Pre-Spend Verification — 27 Aug 2026

**Status:** ZERO-SPEND PUBLIC-METADATA VERIFICATION COMPLETE.  
**External provider/model/evaluator calls:** 0.  
**API spend:** USD 0 / INR 0.

This record verifies current public model/route availability and published planning prices. It does not authorise EMP-001 and it does not substitute a model, route, prompt, threshold, repeat count or scientific question.

## OpenAI text-judge candidate

Frozen candidate alias:
- `gpt-5.4-mini`

Current official OpenAI model documentation:
- https://developers.openai.com/api/docs/models/gpt-5.4-mini

Verified:
- model remains available;
- current published token prices are USD 0.75 / 1M input tokens and USD 4.50 / 1M output tokens;
- OpenAI currently publishes the immutable snapshot `gpt-5.4-mini-2026-03-17`.

Execution disposition:
- use `gpt-5.4-mini-2026-03-17` as the OpenAI resolved version for EMP-001 unless a later same-day pre-dispatch check shows it unavailable;
- do not silently substitute a sibling model.

## Google text-judge candidate

Frozen candidate:
- `gemini-3.5-flash-lite`

Current official Google model documentation:
- https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite
- https://ai.google.dev/gemini-api/docs/models
- https://ai.google.dev/gemini-api/docs/pricing

Verified:
- Gemini 3.5 Flash-Lite remains available and GA/stable;
- current documented stable model ID is exactly `gemini-3.5-flash-lite`;
- Google’s current model-version guidance says a **stable** model ID points to a specific stable model and usually does not change, while `latest` aliases are the hot-swapped form;
- current paid-tier prices are USD 0.30 / 1M input tokens for text/image/video/audio and USD 2.50 / 1M output tokens.

Execution disposition:
- treat the documented stable ID `gemini-3.5-flash-lite` as the exact stable version identifier under the frozen `snapshot_or_exact_version_required` rule;
- do **not** invent or use `gemini-3.5-flash-lite-001` merely because synthetic tests use that string as a fixture;
- if the provider exposes a more specific immutable resource identifier at execution without changing the scientific model, persist that identifier too;
- do not use a `*-latest` alias and do not silently substitute another Gemini model.

## fal image route IMG-01

Frozen route:
- `openai/gpt-image-2`
- 1024×1024
- medium quality
- 8 unseeded generations maximum

Current official fal route:
- https://fal.ai/models/openai/gpt-image-2

Verified:
- route remains live;
- the API supports `quality=medium`;
- 1024×1024 is supported;
- current published price for 1024×1024 medium is USD 0.053/image.

This exactly matches `NOMINAL_FAL_PRICE_USD["IMG-01"] = 0.053`.

## fal image route IMG-02

Frozen route:
- `fal-ai/ideogram/v3`
- BALANCED
- 8 unseeded generations maximum

Current official fal route:
- https://fal.ai/models/fal-ai/ideogram/v3

Verified:
- route remains live;
- BALANCED remains a supported rendering speed;
- current published BALANCED price is USD 0.06/image.

This exactly matches `NOMINAL_FAL_PRICE_USD["IMG-02"] = 0.060`.

## Price-book reconciliation

The committed EMP-001 planning rates in `eval/empirical-tranche-1/providers.py` match the current public prices checked above:

- OpenAI: 0.75 input / 4.50 output per 1M tokens;
- Google: 0.30 input / 2.50 output per 1M tokens;
- IMG-01: 0.053/generation;
- IMG-02: 0.060/generation.

No price-book correction is required before the spend decision.

Under the harness's current conservative per-call reservation assumptions:
- one OpenAI judge call reserves USD 0.001788;
- one Google judge call reserves USD 0.000760;
- if both candidates survive all 1,152 calls each, qualification reserves approximately USD 2.935296 total;
- the full 16-generation A-TEXT image component is USD 0.904 at current route prices.

These are planning calculations, not measured invoice economics. The frozen USD 6 qualification sub-cap and USD 10 total ceiling remain ceilings, not spending targets.

## Remaining pre-spend blockers

Still outstanding:
1. the 96-row Latin human perceptibility review;
2. rebuilding the gitignored generated image sets before execution;
3. runtime secrets supplied only at dispatch time;
4. explicit user approval of the bounded EMP-001 spend ceiling.

No paid execution may begin before those gates are satisfied.
