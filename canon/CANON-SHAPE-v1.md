# Canon — shape and consumption contract v1 ("final shape for now")

**STATUS: Controller-directed direction, recorded 2026-09-01 in session
`session_01MTzh8gGKkyN31UruDXHcZo` ("Let's stick with that… final shape of Canon for now").
It becomes the governing shape when the Controller merges the branch carrying it. Until then
`coordination/CONTROL-STATE.md` governs.** This document states what Canon *is*, what it is
*for* on the evidence so far, and how it is *consumed* — and it deliberately stops short of any
verdict on whether Canon works: **that judgment is reserved to the Controller** (DN-07 series;
EVAL-038 conclusion is a proposal, not a finding of adequacy).

It supersedes, in part, `canon/compilation/INJECTION-CONTRACT-v0.md`: the forced-consumption
"receipt" schema in that contract is retired as a production mechanism (see §5). Everything else in
the tranche-A artifacts stands as PROPOSED.

---

## 1. What Canon is

A durable library of media-production expertise — photography, lighting, composition, editing,
advertising, and the Indian market — extracted from admitted sources with page-level provenance,
graded evidence, and a formal admission gate. It is book knowledge. It is **never** evidence
about model capability, never a Capability Registry input, never benchmark ground truth
(`PROJECT-MEMORY.md` §4.2).

## 2. What it contains today (recomputable)

| Layer | State | Recompute |
|---|---|---|
| Accepted sources | **37** (24 → 37 under DN-06) | `python3 canon/validation/validate_audit_gate_v02.py` |
| Knowledge objects | **1,300** SourceKnowledge · 132 concept systems · 291 bindings | `python3 canon/knowledge/build_corpus_index.py` |
| HOLD candidates | 5 (desai — clean-copy diff; airey/freeman-beyond/samara-ch2 — replacement copies; ries — retired DN-05) | `canon/knowledge/CANON-CORPUS-INDEX.yaml` |
| Coverage layer | live-37 map: 10 packs × 56 domains, every source packed; ruling-(c) markers on google-abcd (`platform_contingent`) and sontag (`critique_context`) | `python3 canon/validation/validate_live37_coverage.py` |
| Join layer | 60 cross-source candidate records incl. 13 adjudicated duplicate terms (2 genuine homonyms) — all `status: proposed` | `python3 canon/validation/validate_cross_source_candidates.py` |
| Vocabulary | 583 domain labels mapped (96.0% of mentions), 53 queued | `python3 canon/validation/validate_domain_vocabulary.py` |
| Confidence markers | deterministic marker for all 1,300 objects (MEASURED/REASONED/ASSERTED + flags) | `python3 canon/compilation/assign_markers.py --check` |
| Compiled packs | **2 of 10**: `product_appearance` (10 decisions), `composition_and_attention` (11 decisions), guard-closure enforced | `python3 canon/validation/validate_compiled_pack.py` |

## 3. What it is for — on the evidence, stated without verdict

EVAL-037 established that Canon can improve a strong model's production reasoning. EVAL-038
(committed, blinded, commitments verified) established, for the two-pack configuration tested:

- **Not a substitute for model capability.** Weak model + packs did not match a strong model
  alone on any of six briefs (0/6, 18/18 top-3 slots to the baseline), and cost more per
  delivered plan all-in. The substitution rationale is closed for that configuration.
- **A candidate acceptance gate.** The compiled doctrine forbids both human-rejected PILOT-001
  candidates on the human's own grounds (retro-test); the pack-guided image won the B06 media
  pair; both videos failed on the exact defect the packs' overlay rule guards against; the
  replay demonstration showed draw-to-draw variance flips acceptability.

These are recorded observations. **Whether the gate "works" — moves the accepted-outcome rate
enough to matter — is the Controller's call, to be measured, not concluded here.**

## 4. The consumption architecture ("inject it properly")

```
customer request
  → Normalized Request (CANON-010 grammar)
  → pack lookup (deterministic: NR → 2–4 pack ids; canon/packs/pack-triggers-v0.yaml)
  → blueprint: a reasoning model writes ONE production plan
        · packs injected UNCONDITIONALLY as a stable, byte-identical, cache-served prefix
        · no forced compliance receipts (the model does not write back proof — see §5)
        · model choice is free: strong (≈USD 0.06/plan), batched (≈½), or free-tier;
          the shape does not depend on which
  → PRE-DISPATCH GATE  (code, zero tokens): the packs' check lines run over the generation
        prompt — declared finish per object, one light source, no in-image text, attention
        order named, brief-fixed parameters honoured…
  → cheapest verified generation route (price pinned at execution time, 0 retries)
  → POST-DRAW GATE     (code, ≈zero): baked-text scan first, then the artifact checks
  → redraw loop until the gate passes (draws are variance; the blueprint amortises)
  → human acceptance (the Controller / customer — the only quality authority)
  → EMPIRICAL MEMORY: the accepted blueprint becomes a template asset; later similar
        requests match it and fill slots in code — no reasoning tokens for routine volume
```

Canon touches this pipeline in exactly three places: the injected packs (the blueprint's
doctrine), the two gates (the packs' check lines as code), and the template library (accepted
blueprints carrying the doctrine forward). Nowhere does the consuming model decide whether to
consult Canon, search it, or read it — the self-diagnosis trap that produced Gemma's 0/18 in
EVAL-037 is designed out.

## 5. Rules that survive, rules that changed

**Survive from CANON_CONTEXT v0.1 / compiled-pack contract:** accepted Canon only, fail-closed on
HOLD; render by id, never paraphrase; guard closure (a rule travels with its exceptions);
computed confidence markers; conflicts stated with a resolution rule or marked unresolved;
mandatory limit lines; O(1) per-request cost in corpus size; a validator PASS establishes
structure, never quality.

**Changed by EVAL-038's accounting:**

| v0 mechanism | Why it changed | v1 mechanism |
|---|---|---|
| Forced-consumption schema: the model writes a filled field per decision + a line per check (`FAILURE_PREVENTION`, `DOCTRINE_DEVIATIONS`) | The receipts cost ~5× the rules (10.2K vs 5.8K output tokens; output priced 5× input). Compliance verified by prose is compliance paid for twice | The gate verifies mechanically; the model writes the plan only |
| Cold per-request injection | Never cached in EVAL-038; cache pricing not pinned | Packs are a stable prefix served from cache (~0.1× input price); cache pricing pinned before any cost claim |
| One bespoke blueprint per draw | Blueprints re-execute for pennies; variance lives in draws | One blueprint → N draws → template asset; reasoning cost falls with volume |
| Budget calibrated to "beat the corpus dump" | The real baseline was a USD 0.063 bare plan, not a USD 0.18 dump | Budget calibrated to the gate's savings on media draws, not to reasoning-token thrift |

## 6. Cost model at production scale (per image, against a ≈USD 0.05 generation route)

| Component | Marginal cost | Basis |
|---|---|---|
| Canon knowledge | 0 | compiled offline, amortised |
| Pack injection (~4.6K tokens, cached) | ≈0.0005 | cache-read pricing, to be pinned |
| Compliance receipts | 0 | retired (§5) |
| Blueprint | 0.00–0.02, falling with template reuse | one plan per many draws; routine volume templated |
| Gates | ≈0 (+≈0.0015 if OCR text scan per draw) | deterministic code |
| **True unit cost** | **generation price × draws-per-accepted-output** | the only number that matters (CpAO) |

The Canon layer exists to shrink the multiplier, not the generation price. Whether it does is
measured per §3.

## 7. Open work, in order (none authorised by this document)

1. **Build the gate** — derive pre-dispatch and post-draw checks as code from PA-D1..D10 and
   CA-D1..D11; baked-text scan first. This is the next build.
2. **Injection v1** — cached stable prefix, no receipts; pin cache pricing; retire the v0
   receipt schema in the runner.
3. **Template library / empirical memory** — accepted blueprints as reusable assets.
4. **Remaining packs only as the gate needs them** (colour/register, commercial-communication
   check lines first) — REP-11 is no longer driven by injection coverage.
5. **Controller items:** promote DN-06/DN-07 to `coordination/decisions/`; Governor refresh of
   `PROJECT-MEMORY.md` / `CONTROL-STATE.md` (both still describe the pre-EVAL-038 programme);
   the four HOLD copies; EVAL-037 judging attestation.
6. **Measurement the Controller may commission:** acceptance-rate runs (many draws per arm,
   blind accept/reject) — the cheapest decisive measurement in the programme.
