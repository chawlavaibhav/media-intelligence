# Image half two — edit, extend, compose, reference — summary (judged 2026-09-09)

**Run** `half2` (36 trials: 6 cases × 3 edit routes × 2 repeats), on the constructed stand-ins of run `half2-fixtures`
(`eval/experiments/EVAL-040/fixtures/STAND-IN-SPEC.yaml`; no customer photos existed, the Controller chose stand-ins:
"freeze as proposed, constructed stand in, go ahead"). Spend USD 3.30 lane + USD 0.15 smoke + USD 1.61 stand-ins of the
₹700 cap (`CONTROLLER-SPEND-AUTHORISATION-IMAGE-HALF-TWO-AND-VIDEO-PIECE-1-2026-09-09.md`). Every call returned an
artifact; no refusal, no error. `gpt-image-2-edit` was excluded (price unpinned on the roster).

**Judge** the Controller, blind (J01–J36, judge copies re-encoded to metadata-free PNG, reference photos and decoy
line-ups on the page; reveal key `~/.eval040-keys/REVEAL-half2.json`, commitment verified at reveal). Verdicts in
`judging/VERDICTS.yaml`, reveal in `RESULTS.yaml`.

## Result by route (all four skills pooled, 12 trials each)

| Route | Accepted | Price per call | Price per accepted | Read |
|---|---|---|---|---|
| Seedream 5 Pro edit | 10 / 12 | USD 0.0675 | USD 0.081 | the default for work on a supplied photo |
| FLUX.2 Pro edit | 4 / 12 | USD 0.0575 | USD 0.173 | clean sofa removal; fails extension, reference and text hygiene |
| Nano Banana Pro edit | 3 / 12 | USD 0.15 | USD 0.60 | most expensive, weakest; drifts colour, skin tone, clothes |

## Result by question

| Question | Seedream 5 Pro | FLUX.2 Pro | Nano Banana Pro | Controller's reject notes |
|---|---|---|---|---|
| IMG-EDIT (remove sofa-sitter; clean masala pack to white) | 2 / 4 | 3 / 4 | 1 / 4 | Seedream: pack "size increased", sofa colour changed; FLUX: "new text appeared" on the pack; NB Pro: sofa colour changed ×2, "background came in" |
| IMG-EXT (extend 16:9 banner to 9:16) | 2 / 2 | 0 / 2 | 0 / 2 | FLUX "changed size" ×2; NB Pro "slight cutoff, not consistent" ×2 |
| IMG-COMP (supplied face + supplied pack + Hindi headline) | 2 / 2 | 1 / 2 | 1 / 2 | FLUX "face seems a little changed, unsure"; NB Pro "face looks fairer" |
| IMG-REF (referenced tin; referenced person at a cafe) | 4 / 4 | 0 / 4 | 1 / 4 | FLUX "tin looks bruised" ×2, "not a cafe setup" ×2; NB Pro "tin looks bruised", "clothes changed" ×2 |

Elimination (E2, accepts ≤ 25 % of n): Nano Banana Pro edit eliminated on IMG-EDIT, IMG-EXT and IMG-REF; FLUX.2 Pro
edit eliminated on IMG-EXT and IMG-REF; Seedream 5 Pro edit survives every question.

## What this says

1. **Seedream 5 Pro edit is the default for anything done to a supplied photo** — object removal, banner extension,
   composing a supplied face with a supplied product, reproducing a referenced product or person. It was the only route
   that survived all four questions, at the second-cheapest price. Its two misses were on the masala-pack clean-up
   (pack grew; colour drift on one sofa draw).
2. **Extension is a one-route skill today.** Only Seedream kept the banner's size and edges; FLUX resized it, Nano
   Banana Pro cut it off.
3. **Nano Banana Pro edit is not worth its price for photo work** — consistent with round one, where it was the worst
   value on core stills. Its failures are drift: colour, skin tone, clothing, background.
4. **Reference fidelity (tin, person) is where FLUX.2 Pro edit fails hardest** (0/4): "bruised" tins and a missing cafe.
5. **Round-one text rule holds here**: FLUX added stray text to a pack it was asked only to clean.

Caveats: n = 2 per (case, route); stand-ins are model-generated pictures, not customer photos (identity/colour drift
on real photos may differ); two Controller rejects on the referenced person ("clothes changed") read the contract more
strictly than written (the contract asked for the same face, hair and build) — kept as given, noted here. No Registry
row carries any of the acceptance numbers above; the Registry holds only the deterministic rows (format, cost,
latency/errors, reliability, repeat consistency) re-evaluated under the frozen criteria (`registry_rows.py`, 90 rows).

## Routing consequence (recorded in ROUTING-EVIDENCE-MAP-v0 as RR-4, RR-5)

- Supplied-photo work → Seedream 5 Pro edit first; FLUX.2 Pro edit only as the object-removal fallback.
- Banner extension → Seedream 5 Pro edit only.
