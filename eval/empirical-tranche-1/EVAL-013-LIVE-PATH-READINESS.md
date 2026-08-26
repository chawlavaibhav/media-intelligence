# EVAL-013 — EMP-001 live-path readiness

**Verdict:** `READY_FOR_SPEND_APPROVAL`

**Branch:** `work/eval-013-emp-001-live-path-correction` · **not merged**
**External provider/model/evaluator calls made by EVAL-013: 0**
**External spend: USD 0 / INR 0**

Evidence: [`VERIFICATION-PRE-SPEND.md`](VERIFICATION-PRE-SPEND.md), copied from fresh runs.
Supersedes [`EVAL-012-ZERO-SPEND-READINESS.md`](EVAL-012-ZERO-SPEND-READINESS.md), whose verdict
the Controller correctly rejected.

---

## The five blockers, closed

| | Blocker | Correction | Proof |
|---|---|---|---|
| **B1** | live qualification orchestration absent — `--live` opened a valid guard then raised unconditionally | `ImageResolver`, `LiveCandidate`, `run_live`, `--fake-live` | 2,304 dispatches through the real judges, transports and scorer |
| **B2** | no fal generation adapters for the frozen routes | `FalImageRoute` for IMG-01 and IMG-02, frozen bodies | 16 dispatches, correct URLs, frozen config asserted |
| **B3** | A-TEXT measured by `_fake_transcribe` and hard-coded `synthetic: true` | real path fetches the artifact and calls the qualified judge's blind `transcribe`; `synthetic` derives from the execution mode | `synthetic: False` on a fake-live run; judge dispatched 16 times |
| **B4** | no positive controls | positive fake-live controls for both paths, each with a negative twin | 65 new tests; every one fails if the live branch refuses |
| **B5** | `Authorization: Bearer` sent to every provider | per-provider transports; Gemini uses `x-goog-api-key` with the version in the URL | emitted headers and URLs asserted through an HTTP recorder |

**B3 was a correctness defect, not a gap.** A paid run would have been scored by a stub reading its
own generator's payload, then filed as synthetic — spend with no measurement, mislabelled so
nobody could tell from the record.

## Three defects this correction found in its own predecessor

Writing the positive controls surfaced three more, all now fixed:

1. **The blind check never ran on the live path.** The checker contract requires it before any
   call; EVAL-012 enforced it only in tests. A leak would have reached the wire. Now a
   pre-dispatch refusal that costs nothing, because nothing is reserved or sent.
2. **The blindness scan was itself blind.** The transport serialised with `ensure_ascii=True`, so
   a Devanagari target would travel as `\uXXXX` and every scan looking for Devanagari characters
   passed while seeing nothing — blind in exactly the place it was watching. The wire now carries
   UTF-8 and the scan parses first.
3. **The verdict blind rule cried wolf.** It demanded the target appear exactly once across the
   whole serialised body, which is not an invariant: short targets occur incidentally in prompt
   prose, in enum values like `input_text` and inside base64. It fired on the preflight's own
   probe. Replaced with the rule the Devanagari checker contract already settled on.

## Positive fake-live paths proved

Both run the **same** orchestration, request builders, auth headers, parsers and scorer as a paid
run. Only the socket is replaced, by an injected recorder. Both walk the real authorisation gate.

**Qualification** — 2,304 recorded dispatches, 0 network calls, `synthetic: false`, every call
record pinning alias and resolved version with `retries: 0`. The progressive stop holds on the
live path: a live candidate that false-passes on Devanagari receives 576 Devanagari dispatches and
**0** Latin dispatches.

**A-TEXT** — 16 generations (8 + 8), 16 evaluator dispatches, 0 network calls, `synthetic: false`,
0 Registry rows. Generation and evaluator trials stay separate: a refused generation persists with
no evaluator call; an artifact whose judge refused persists **both** trials, both costs and an
absence reason.

### What fake-live does NOT establish

The fake readers are **perfect**. A perfect reader is not a real one. `16/16 exact matches` is a
property of the fake and says nothing whatever about IMG-01, IMG-02 or either judge candidate. The
empirical floor is unchanged: 0 qualified models, 0 qualified evaluators, 0 Registry rows, and no
accepted evidence that Canon improves model outcomes.

## Remaining prerequisites before the first real call

### 1. Explicit user approval — **BLOCKING**

> EMP-001: maximum **USD 10.00** / approximately **₹954** consumed API spend, excluding taxes,
> **no retries**, **no account pre-funding above that ceiling**.

### 2. Runtime secrets — **BLOCKING**

`OPENAI_API_KEY`, `GOOGLE_API_KEY`, `FAL_KEY`, plus a funded fal surface. If a provider demands a
minimum deposit above the approved ceiling, **stop and return** rather than funding it.

### 3. Exact version pinning at execution — **BLOCKING, and now enforced**

`--live` refuses without `--openai-version` and `--gemini-version`. A judge refuses to exist
without a `resolved_version`, and the Gemini transport refuses a body naming a different model
than its URL. This branch makes **no claim** about current provider availability or pricing.

### 4. Human perceptibility review of the Latin pack — **zero-spend, outstanding**

`text_qualification/perceptibility-review.csv` is emitted **unfilled** — 96 rows, all verdict
columns blank. Not performed, deliberately not fabricated. The mechanical half is done: all 48
mismatches differ after NFC *and* in decoded pixels. That proves a difference is on the page; it
does not prove a person would notice it.

**Latin paid qualification remains gated on this review.** The Devanagari leg already carries a
completed human validation, so Q2a could proceed without it if the Controller so decides; the code
assumes neither.

### 5. Materialising the derived material — **zero-spend, mechanical**

Both image sets are gitignored build products and a fresh checkout must rebuild them before the
suite runs (~30s, free). Commands are in the README and the verification record. The rebuilt
Devanagari `items.jsonl` must hash to `9c69cac2…` or the runner fails closed.

## The live path remains unproven against a real provider

`OpenAIHttpTransport`, `GeminiHttpTransport` and `FalImageRoute` have never been run against a
provider. Their URLs, headers and bodies are asserted against documented contracts, not against
observed responses. The first authorised call is also the first test of them, and it should be
treated as such — expect to spend a trial discovering a real response shape.

## Confirmation

- External provider/model/evaluator calls made by EVAL-013: **0**
- External spend: **USD 0 / INR 0**
- No terms accepted, no account funded, no API credit consumed
- Capability Registry empirical rows: **0**, unchanged and byte-identical
- 13/13 protected baselines byte-identical; Devanagari battery read, never written
- Scope, roster, thresholds, ceiling, retries, four A-TEXT strings, 16-generation cap: **unchanged**
- All valid EVAL-012 work preserved
- Branch pushed, **not merged**

## Would approval + secrets + version pins now be enough to start, with no further code change?

**Yes — for the Devanagari leg, which is the first thing EMP-001 runs.**

With a valid authorisation file, the three keys and two pinned versions, `qualify_text.py --live`
executes the real protocol with no code change. The A-TEXT runner then consumes a qualified judge
and the frozen fal routes the same way.

Two honest qualifications on that "yes":

- **Latin qualification still needs the human perceptibility review** — a zero-spend prerequisite,
  not a code change.
- **The transports are unproven against live providers.** No code change is *known* to be needed;
  whether one *turns out* to be needed is exactly what the first authorised call will reveal.
