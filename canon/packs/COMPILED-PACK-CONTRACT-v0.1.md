# Compiled-Pack Contract v0.1 — runtime contract and module-by-module runtime disposition

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

**Reconciles:** `canon/context/CANON-CONTEXT-SPEC-v0.1.md` (PR #83, this branch, PROPOSED) and
`canon/retrieval/RETRIEVAL-CONTRACT-v0.1.md` at commit `8115400` (PR #84, reachable only via
`git show 8115400:<path>`; never checked out or copied by this document's authoring).
**Authority claimed:** none. Neither PR is adopted; this document proposes the merge disposition a
Controller decision would have to rule on. It admits no source, executes nothing, and spends USD 0.
**Companion (proposed, not yet written):** `canon/packs/pack-triggers-v0.yaml` (trigger table),
`canon/validation/validate_compiled_pack.py` (extended validator). Referencing them here creates
neither.

---

## 1. Settled direction this contract serves

EVAL-037 established that the model-triggered consumption path is dead for weak models: Gemma
FULL_CANON used Canon 0/18 times; Sonnet's surviving searches returned envelopes where HOLD
outnumbered accepted ~2.3:1 (`eval/experiments/EVAL-037/CONCLUSION.md`;
`canon/context/CANON-CONTEXT-SPEC-v0.1.md` §1 tabulates the failures with recompute command
`python3 canon/validation/recount_eval037_retrieval.py`). The direction this contract binds:
**Canon ships as a small set of pre-compiled, per-pack doctrine artifacts, injected
unconditionally** — the runtime performs no retrieval, no ranking, no tool call, no model-triggered
read. Runtime is: Normalized Request (NR) → pack ids (a table lookup) → concatenate pre-compiled
byte-stable text. Everything selective, epistemic, and budgetary happens offline in the compiler.

The 10 pack ids are fixed by `canon/planning/CANON-V1-LIVE19-COVERAGE.yaml` (`packs:` block):
`composition_and_attention`, `typography_and_copy`, `product_appearance`,
`colour_and_visual_register`, `camera_and_spatial_grammar`, `editing_pacing_and_short_form`,
`commercial_communication`, `concept_and_distinctiveness`, `indian_indic_context`,
`critique_and_effectiveness`. Three compile thin (`typography_and_copy` and
`editing_pacing_and_short_form` = `critical_hole`, `indian_indic_context` = absent per that file);
a thin pack compiles an explicit coverage statement — it never borrows HOLD candidate material.

## 2. Pack format

One artifact per pack: `canon/packs/<pack_id>.compiled.yaml`. The format is the PR #83
`CANON_CONTEXT` object shape re-targeted from per-request to per-pack — same five sections, same
six mandatory `key_guidance` fields, same fail-closed validator core
(`canon/validation/validate_canon_context.py`), with compilation-specific additions:

| Block | Content | Origin |
|---|---|---|
| `pack_id`, `pack_version` | closed id from the 10 above; version bumps only on recompile | new |
| `applicability` | modality set from the closed enum `{static_image, video, audio, image_sequence, any}` | new (gap: no pack today declares a modality axis) |
| `corpus_fingerprint` | recomputes to `CANON-CORPUS-INDEX.yaml` accepted `combined_digest`; algorithm from `8115400:canon/retrieval/corpus.py` | PR #84 G7 |
| `budget` | declared and validator-enforced per pack (see §5) | PR #83 R1, re-targeted |
| `production_questions` | questions-with-defaults skeleton seeded from the 9-question catalogue at `8115400:canon/retrieval/questions.py` | PR #84 |
| `key_guidance[]` | six fields per entry (`principle` verbatim, `applicability`, `concrete_implication`, `failure_mode`, `evidence`, `uncertainty`) **plus `confidence_marker`**, a derived label recomputable by pure function from `claim_type` × `evidence.characteristics` × caveat origins (proposed decision table `canon/context/confidence-marker-v0.yaml`) | PR #83 §2.1 + new |
| `conflicts` | every one-hop relation partner over `{contradicts (sym), qualified_by/qualifies (inverse pair), trades_off_with (sym), depends_on (directed)}` is compiled into the same decision entry, named here with a `resolution_rule` (PR #83 R7), or the citing object is dropped — closure is compile-time, never runtime | PR #83 R7 + closure |
| `do_not_overgeneralize` | mandatory, non-empty | PR #83 R8 |
| `source_trace` | every cited id resolves in `canon/knowledge/current/` with Audit-Gate-complete status; HOLD/QA ids fail validation | PR #83 R4 |

Closure is cheap by census: 225/677 accepted objects carry a closure-relevant relation, partner
fan-out mean 1.22, max 4 (recompute: loop over
`canon/knowledge/current/*/source-knowledge.yaml` counting `intra_source_relations` by type).
Regression case: `sk_gos_c003_0012` must never ship without `sk_gos_c003_0010`,
`sk_gos_c003_0007`, `sk_gos_c003_0013`.

**Serialization is byte-stable**: sorted keys, no timestamps, no environment-dependent content,
LF line endings, UTF-8. The only bytes that change between compiles of unchanged doctrine are
none; `corpus_fingerprint` changes only when the accepted corpus changes. This is a cache
requirement (§6), not a style preference.

## 3. NR → pack trigger rule

The single medium authority is the frozen CANON-010 grammar
(`canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml`): `modality` (field R05,
required, enum of 4) and `requested_operation` (field R01, required, enum of 7, provenance
`customer_stated`|`customer_implied`, never `system_derived`). Raw-text media detection
(`detect_media` at `8115400:canon/retrieval/questions.py`) is retired from the runtime path: it
re-derives a field the contract already requires and cannot emit `audio` or `image_sequence`.

**Trigger rule.** A total table (proposed `canon/packs/pack-triggers-v0.yaml`) over all
4 × 7 = 28 `(modality, requested_operation)` cells. Each cell names:

- `base_packs` — always injected for that cell (universal packs are in every cell);
- `conditional_packs` — each keyed to a specific NR field: `text_requirements` non-empty →
  `typography_and_copy`; product/packshot entity in `entities[]` → `product_appearance`;
  `language_topology` or cultural-marker entities → `indian_indic_context`; advertising
  acceptance intent → `commercial_communication`.

Totality (all 28 cells defined, every named pack id in the closed set of 10) is a validator
check, not a convention.

**Uncertain-classification fallback (binding).** When classification is uncertain — `modality`
provenance `customer_implied` combined with non-empty `ambiguity_markers[]`, or contradictory
cues across NR fields — inject the **union** of the `static_image` and `video` branch base sets
plus the universal packs. A bounded superset, never guess-and-drop: the Gemma 0/18 lesson is that
under uncertainty the system defaults to inclusion, because the model will not fetch what was
omitted. The union is still bounded by §5's per-request budget, and the trigger table must prove
its largest legal combination fits.

**Audio cell.** `modality=audio` is admissible in the grammar but zero packs and zero accepted
sources cover audio. The cell maps to the universal packs plus a **mandatory compiled
coverage-gap notice** — an explicit statement of what Canon does not know, injected instead of
silence. Closing the gap needs new source ingestion only the Controller can authorise.

## 4. Injection placement — schema fields vs system prompt

- **Pack text goes in the system prompt**, concatenated in canonical order (§6), as the stable
  prefix. It is not delivered as tool results (no tool surface survives at runtime), not as
  API-level schema/metadata fields, and not interleaved with the request. Rationale: the system
  prompt is the only position that is (a) unconditional — the model cannot decline to fetch it,
  (b) cacheable as a shared prefix across requests, (c) uniform across weak providers that lack
  bespoke schema fields.
- **The NR is data, not doctrine**: it enters as the first user-turn content, in its frozen
  grammar serialization, *after* the pack prefix and after the cache breakpoint. The volatile
  bytes never sit upstream of the stable bytes.
- **Per-entry epistemic fields stay inside the pack's own YAML** (schema fields *of the pack
  object*, per §2), not as separate prompt apparatus. The pack is self-contained: a model that
  reads only the system prompt has the claim, its scope, its failure mode, its evidence character,
  and its confidence marker in one place.

## 5. Budget arithmetic

**UNCOMMITTED — session arithmetic pending a Controller note.** All prices are Anthropic's
(session numbers: Sonnet 2.00/10.00, Haiku 1.00/5.00 USD per MTok; cache read 0.1×, cache write
1.25× at 5-min TTL / 2× at 1-hour, reads refresh TTL free). If the Controller intends a
non-Anthropic weak model, every coefficient below must be recomputed against that provider's
price sheet before any figure is relied on. Budgets are additionally uncalibrated against
accepted outcomes (CANON-CONTEXT-SPEC R1 note; `8115400:canon/retrieval/budgets.py` docstring);
calibration is a model experiment requiring Controller-authorised spend.

Let B = base prompt tokens (~2K), O = output tokens (9–13K observed), C = injected Canon tokens.

- **Uncached parity** (Haiku+Canon vs Sonnet alone): `2B + 10O = 1*(B + C) + 5O` ⟹
  **`C = B + 5*O`** ≈ **47K–67K tokens** at O = 9–13K, B ≈ 2K.
- **Cached variant** (pack prefix read at 0.1×): `2B + 10O = B + 0.1C + 5O` ⟹
  **`C = 10*(B + 5*O)`** ≈ **470K–670K tokens** — pack size stops being the binding economic
  constraint; context window and attention dilution remain.
- **Binding cold-case rule:** per-request injected total (all packs + notices) **≤ ~45K tokens**,
  so the uncached break-even holds even when the cache is cold or traffic is below the warmth
  threshold (§6). At default per-pack envelopes (≤ 8 entries / ≤ 16 KiB ≈ 4K tokens, inherited
  from PR #83's oracle-derived budget and equally uncommitted), even the full 10-pack union is
  ~40K tokens and fits.
- **Growth is absorbed offline.** Raw claims-only injection is already ~80K tokens
  (319,104 claim chars over 677 objects at ~4 chars/token; recompute: sum `len(claim)` over
  `canon/knowledge/current/*/source-knowledge.yaml`) — past the low-end break-even today, and
  ~160K tokens once HOLD admission roughly doubles the corpus. Compiled packs stay O(1) per
  request: growth goes into offline recompilation against fixed per-pack budgets.

Recompute the algebra from this section's two displayed equations; recompute the corpus figures
with the one-line loop above; every other number cites its committed file.

## 6. Cache strategy (mandated, not advisory)

1. **Canonical fixed pack order** — universal packs first, then modality-branch packs, then
   conditional packs — so image and video requests share the universal prefix bytes.
2. **Minimal combination set** — a handful of standard pack sets from the trigger table, never
   per-request composition. Every distinct byte sequence is a separate cache entry; bespoke
   assembly is 0% cache reads by construction, forever (the PR #84 economics failure).
3. **Packs precede the volatile NR**, with an explicit `cache_control` breakpoint at the end of
   the shared prefix. Nothing request-specific upstream of the breakpoint.
4. **Byte-stable serialization** (§2) — recompilation of unchanged doctrine must not invalidate
   warm caches; `corpus_fingerprint` changes only on real corpus change.
5. **Warmth threshold**: below ~1 request per 5 minutes per pack combination (5-min TTL; a read
   refreshes the TTL free) the cache never warms, and the **uncached** break-even `C = B + 5*O`
   governs — which is why §5's ≤ ~45K rule is stated for the cold case and is not relaxed by
   this section.

## 7. Guarantees, restated from RETRIEVAL-CONTRACT v0.1 for the compiled setting

`8115400:canon/retrieval/RETRIEVAL-CONTRACT-v0.1.md` G1–G9 carry forward as follows. G2 and G3
are re-targeted from per-request to per-pack; the rest restate with the enforcement point moved
from runtime to compiler+validator.

| # | Compiled-setting guarantee |
|---|---|
| G1 | Accepted-only, structurally: the compiler reads `canon/knowledge/current/**` through the fail-closed loader (algorithm at `8115400:canon/retrieval/corpus.py`); HOLD (`canon/candidates/`) and QA (`canon/qa/`) are unreachable by construction — there is no diagnostic flag on the production path. The EVAL-037 53.5%-HOLD contamination class is eliminated, not filtered. |
| G2 | Nothing unbounded, **per pack**: every pack declares a required positive budget in entries and serialized bytes; `None` rejected at construction (pattern from `8115400:canon/retrieval/budgets.py`); additionally the largest legal pack combination in the trigger table must fit the §5 per-request injection budget. |
| G3 | Size reported = size delivered, **per pack**: the stamped serialized byte length is the exact length of the committed pack file; token figures divide by 4 and are labelled estimates; the enforced quantity is bytes. |
| G4 | Status and uncertainty survive **compilation**: every `key_guidance` entry carries evidence characteristics, both uncertainty fields, and caveats with `origin` preserved (`source_stated` vs `extractor_observed` never collapse); the per-kind field projections at `8115400:canon/retrieval/bundle.py` (`_content_for` / `_epistemics_for` / `STATUS_LEGEND`) are the projection basis. |
| G5 | Nothing paraphrased: `principle` is a verbatim slice of a committed corpus field; truncation marked, never applied to caveats/evidence/uncertainty. Compilation composes and selects; it does not rewrite claims. |
| G6 | No quality ranking: `confidence_marker` labels evidence character by committed pure function; it never scores, rates, or ranks sources, and binding count is never a proxy for anything. |
| G7 | Determinism: same accepted-corpus fingerprint + same compiler version ⟹ byte-identical packs. No model call, no randomness, no wall-clock. The fingerprint recomputes to `CANON-CORPUS-INDEX.yaml`'s accepted `combined_digest`; a stale stamp is a validator FAIL. |
| G8 | Fail closed: unknown ids, HOLD ids, un-auditable sources, missing index, budget breach, closure breach, marker mismatch, trigger-table hole — each is a hard FAIL, never a warning. Presence on disk is not admission. |
| G9 | Read-only at runtime: the runtime path writes nothing anywhere under `canon/`; the compiler writes only under `canon/packs/`. |

Re-targeted G2/G3 supersede PR #84's per-request 30K-chars/12-items budget and PR #83's
per-request framing of the 16 KiB/8-entry envelope; the envelope values themselves carry forward
per pack as uncommitted defaults (§5).

## 8. What a validator PASS establishes — and what it does not

A PASS from the compiled-pack validator (proposed extension of
`canon/validation/validate_canon_context.py`) **establishes, mechanically**:

- every cited id resolves in `canon/knowledge/current/` with Audit-Gate-complete status, and no
  HOLD/QA id appears anywhere in the pack;
- every `principle` is verbatim against its committed corpus field (digest-checked when condensed);
- declared budgets hold in every dimension, and the largest legal trigger-table combination fits
  the per-request injection budget;
- one-hop relation closure holds: every partner is compiled into the same entry, named in
  `conflicts` with a `resolution_rule`, or the citing object is absent;
- every `confidence_marker` recomputes exactly from the committed decision table;
- the stamped `corpus_fingerprint` equals the recomputed accepted-corpus digest;
- the trigger table is total over all 28 cells with pack ids from the closed set.

A PASS **does not establish**:

- **relevance** — no artifact labels a Canon object relevant to a brief; fit is unmeasured;
- **doctrine quality or medium fit** — a structurally valid pack can still carry film-editing
  knowledge into a still-image request; applicability declarations make this visible, not correct;
- **outcome improvement** — no claim that packs raise accepted-outcome rate or lower Cost per
  Accepted Outcome; that requires a controlled model experiment (proposed as EVAL-038) which no
  validator can substitute for;
- **budget adequacy** — the envelopes are uncalibrated (§5);
- **admission or adoption** — a PASS admits no source, adopts no proposal, and asserts no
  Controller decision. Exit status is a structural fact about committed bytes, nothing more.

## 9. Runtime disposition — module by module

Disposition vocabulary (exactly one per file): **KEEP** (+ADAPT: stays on this branch as the
substrate, amended per-request→per-pack), **SALVAGE** (-OFFLINE: algorithm/content re-homed into
the offline compiler; the module's runtime role ends), **SUPERSEDE** (retired by the compiled
runtime; noted parts may be reused as compiler heuristics), **FREEZE** (evidence; never edited,
never load-bearing at runtime), **RESTATE** (its guarantees carry forward via §7 of this
document). No file is physically moved or edited by this proposal: PR #84 modules exist only at
commit `8115400`, and copying any of them into the working tree is a cross-branch integration
only a Controller-authorised task can perform.

### 9.1 `canon/context/` on this branch (PR #83)

| File | Disposition | Rationale |
|---|---|---|
| `canon/context/CANON-CONTEXT-SPEC-v0.1.md` | KEEP+ADAPT | the six-field object shape becomes the pack format; per-request framing amended to per-pack (§2, §7 G2/G3) |
| `canon/context/canon-context-schema-v0.1.yaml` | KEEP+ADAPT | schema substrate for `<pack_id>.compiled.yaml`; gains pack_id/applicability/fingerprint/marker blocks |
| `canon/context/build_example_context.py` | KEEP+ADAPT | render-by-id generalizes into the compiler's projection step |
| `canon/context/examples/B06-watch-hero.canon-context.yaml` | KEEP | worked example and regression fixture for the validator core |
| `canon/validation/validate_canon_context.py` | KEEP+ADAPT | (not under `canon/context/`, listed for completeness) validator core; extended with closure, marker recomputation, fingerprint staleness, trigger totality |

### 9.2 `canon/retrieval/` and companions at commit `8115400` (PR #84) — read via `git show 8115400:<path>`

| File | Disposition | Rationale |
|---|---|---|
| `canon/findings/CANON-015-CONTROLLER-BRIEF.md` | FREEZE | historical brief; evidence of the proposal's framing |
| `canon/retrieval/README.md` | FREEZE | describes the retired per-request runtime; evidence only |
| `canon/retrieval/RETRIEVAL-CONTRACT-v0.1.md` | RESTATE | G1/G4/G5/G6/G7/G8/G9 carried into §7; G2/G3 re-targeted per-pack |
| `canon/retrieval/__init__.py` | SUPERSEDE | package wiring for the per-request runtime; nothing to carry |
| `canon/retrieval/budgets.py` | SALVAGE-OFFLINE | no-None fail-at-construction budget pattern, re-targeted per-pack (§7 G2) |
| `canon/retrieval/bundle.py` | SALVAGE-OFFLINE | `_content_for` / `_epistemics_for` / `STATUS_LEGEND` per-kind projections become the compiler's projection layer (§7 G4/G5); its bundle assembly and its dropping of `intra_source_relations` do not survive |
| `canon/retrieval/cli.py` | SUPERSEDE | per-request CLI entry point; no runtime assembly exists to invoke |
| `canon/retrieval/corpus.py` | SALVAGE-OFFLINE | accepted-only fail-closed loader, lineage groups, corpus fingerprint — the compiler's input layer (§7 G1/G7) |
| `canon/retrieval/evaluation/EVAL-SET-v0.1.yaml` | FREEZE | evidence of the bounded-retrieval evaluation |
| `canon/retrieval/evaluation/HUMAN-REVIEW-RUBRIC.md` | FREEZE | evidence |
| `canon/retrieval/evaluation/RESULTS-v0.1.md` | FREEZE | evidence |
| `canon/retrieval/evaluation/build_eval_set.py` | FREEZE | evidence tooling; not a production path |
| `canon/retrieval/evaluation/bundles/B01-canon-context.json` | FREEZE | evidence bundle |
| `canon/retrieval/evaluation/bundles/B02-canon-context.json` | FREEZE | evidence bundle |
| `canon/retrieval/evaluation/bundles/B03-canon-context.json` | FREEZE | evidence bundle |
| `canon/retrieval/evaluation/bundles/B04-canon-context.json` | FREEZE | evidence bundle |
| `canon/retrieval/evaluation/bundles/B05-canon-context.json` | FREEZE | evidence bundle |
| `canon/retrieval/evaluation/bundles/B06-canon-context.json` | FREEZE | evidence bundle |
| `canon/retrieval/evaluation/results-v0.1.json` | FREEZE | evidence |
| `canon/retrieval/evaluation/run_offline_eval.py` | FREEZE | evidence tooling |
| `canon/retrieval/plan.py` | SUPERSEDE | `build_plan(request_text)` keys off raw text; the frozen NR replaces it as the single request authority |
| `canon/retrieval/questions.py` | SALVAGE-OFFLINE | the 9-question catalogue seeds each pack's questions-with-defaults skeleton and its capability-routing boundary test survives verbatim; the cue-matching and `detect_media` halves are retired (they re-derive NR field R05 and cannot emit `audio`/`image_sequence`) |
| `canon/retrieval/rank.py` | SUPERSEDE | no per-request ranking exists under unconditional injection; the Jaccard near-dup filter and source/lineage spread caps are reused as compiler selection heuristics |
| `canon/retrieval/tools.py` | SUPERSEDE | `canon_context` tool call disappears (Gemma 0/18: optional Canon is unused Canon); `canon_detail` at most diagnostic |
| `tests/test_canon_retrieval.py` | SALVAGE-OFFLINE | the capability-routing boundary test (`test_catalogue_never_asks_a_capability_routing_question`) survives verbatim against the pack question skeletons; per-request runtime tests retire with their modules |

Completeness of these two tables — every file in `git show 8115400 --stat` (25 files) plus every
file under `canon/context/`, each with exactly one disposition token — is checked mechanically by
`tests/check_rep06_runtime_sections.py`.

## 10. Recompute index

| Claim | Command |
|---|---|
| 25 files at 8115400 | `git diff-tree --no-commit-id --name-only -r 8115400 \| wc -l` |
| Gemma 0/18, overflow 16/18, HOLD-majority envelopes | `python3 canon/validation/recount_eval037_retrieval.py` |
| 677 objects / 319,104 claim chars ≈ 80K tokens | PyYAML loop summing `len(claim)` over `canon/knowledge/current/*/source-knowledge.yaml` |
| closure census 225/677, fan-out mean 1.22 max 4 | PyYAML loop over the same files counting `intra_source_relations` in `{contradicts, qualified_by, trades_off_with, depends_on}` |
| grammar enums (7 operations × 4 modalities) | PyYAML dump of fields R01/R05 in `canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml` |
| 10 pack ids, 3 thin | PyYAML dump of `packs:` in `canon/planning/CANON-V1-LIVE19-COVERAGE.yaml` |
| break-even `C = B + 5*O` and `C = 10*(B + 5*O)` | algebra in §5 from the two displayed parity equations; prices UNCOMMITTED session numbers, Anthropic-only |

Nothing in this document is self-authorising. Adoption of any disposition above, integration of
any 8115400 module, calibration spend, and EVAL-038 execution each require a Controller decision
recorded under `coordination/decisions/`; coordination/CONTROL-STATE.md governs.
