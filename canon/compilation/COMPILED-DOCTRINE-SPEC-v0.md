# COMPILED-DOCTRINE-SPEC v0 — the shape of a compiled doctrine pack

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

**Task:** REP-05. **Addresses:** GAP-04, GAP-05, GAP-09, GAP-11, GAP-14, GAP-16.
**Instantiates:** `canon/packs/COMPILED-PACK-CONTRACT-v0.1.md` §2 for the two pilot packs.
**Compiler:** `canon/compilation/compile_pilot_packs.py` (fresh code; renders by id,
fail-closed; nothing copied from commit 8115400).
**Validator:** `canon/validation/validate_compiled_pack.py` (extends the
`canon/validation/validate_canon_context.py` check family).
**Outputs:** `canon/compilation/PACK-product_appearance-v0.yaml`,
`canon/compilation/PACK-composition_and_attention-v0.yaml`.

## 1. What a decision entry is

Doctrine compiles to **decisions in questions-with-defaults form**, not to claim dumps. Each
entry carries exactly:

| Field | Origin | Rule |
|---|---|---|
| `decision_id` | authored | `PA-Dn` / `CA-Dn`; its check id is `<decision_id>-check` |
| `question` | authored | the production question the decision settles |
| `default` | authored | a decision already made, imperative, answer-shaped — the model edits it, it never composes from principle |
| `check` | authored | an inspectable yes/no over the model's OWN output, answered per check id in FAILURE_PREVENTION (schema v2, `canon/compilation/INJECTION-CONTRACT-v0.md` §3.2) |
| `confidence_marker` | computed | the decision-level aggregate of §4, recomputed by the validator |
| `compiled_from[]` | rendered by id | every cited `sk_`/`scs_` id with kind, owning dir, verbatim `concept_label`, and its claim-level marker from `canon/compilation/marker-map-v0.yaml` |
| `feeds_sections` | authored | which FINAL_PRODUCTION_PACKAGE v2 sections the decision fills |
| `limits` | authored | do-not-overgeneralize lines (R8), including the mandatory verbatim lines of §5 |

Pack level adds `conflicts[]` (pre-arbitrated, §3), `closure_waivers[]` (§2),
`pack_limits[]` (§5), `corpus_digest` (§6), `terse_injection_text` (§7), and `counts` whose
every number recomputes from the pack's own body.

Authored text is Canon judgment (the REP-05 brief's enumeration); everything mechanical —
labels, markers, closure, origin counts, digests, token counts — is rendered by id from
committed bytes and fails closed on any miss, per the three house rules of
`canon/experiments/v1/value-gate/build_oracle_contexts.py`.

## 2. Closure rule (GAP-11) — mandatory, direction-normalized

Stored relation direction is extractor choice: across the 10 pilot-pack sources the corpus
stores `qualifies` 108 times against `qualified_by` 50. A compiler reading only the stored
direction ships rules without their exceptions. So the compiler builds the **undirected guard
union** before emitting anything:

- `contradicts` — symmetric;
- `qualifies` — reversed into `qualified_by` on the target;
- `trades_off_with` — symmetric;
- `depends_on` — directed (outgoing from the cited object only).

For every cited sk object, **each** guard partner must be (a) cited in the same pack, (b)
named in a `conflicts` entry carrying a `resolution_rule`, or (c) listed in
`closure_waivers` with a stated reason. Anything else is a hard compile failure and a hard
validation failure. `generalises` / `specialises` / `member_of_system` /
`demonstrated_together_with` are navigation, not guards, and are not consumed.

Regression case (frozen): a pack citing `sk_gos_c003_0012` must also carry
`sk_gos_c003_0007`, `sk_gos_c003_0010` and `sk_gos_c003_0013`.

Recompute the pilot closure: `python3 canon/compilation/compile_pilot_packs.py --check`
(the compiler refuses to emit on any closure hole).

## 3. Conflicts are pre-arbitrated (R7), tensions are conditioned

A weak model cannot arbitrate two competing claims (EVAL-037; INJECTION-CONTRACT §1). Every
in-pack `contradicts` or `trades_off_with` pair therefore appears as ONE `conflicts` entry
whose `resolution_rule` is a scoped if/then — almost always a scope rule — and the terse
rendering repeats it under `PRE-ARBITRATED CONFLICTS`. Deleting one side would be
manufacturing agreement (`canon/findings/CANON-014-CROSS-SOURCE-OBSERVATIONS.md` §3.2);
shipping both without the rule would repeat the failure the contract exists to prevent.

Cross-source tensions (kind `cross_source_tension`) carry accepted ontology term ids as
members, rendered by id from `ontology-mappings.yaml`; the pairing is referenced from the
REP-02 candidate ledger (`canon/candidates/ontology-join/cross-source-candidates-v0.yaml`,
status proposed) **about** the tension — no HOLD content is consumed, and promotion of any
ledger row remains a Controller review. Pilots carry T4 (whitespace, conditioned on artifact
class; `xj_0022`) and T5 (speculars, resolved on deliberateness; `xj_0023`).

## 4. Decision-level confidence marker (REP-04 layer, aggregated)

Claim-level markers are the committed pure function of
`canon/context/confidence-marker-v0.yaml`, computed by
`canon/compilation/assign_markers.py`. A decision aggregates the markers of its cited sk ids
under this deterministic rule (the validator recomputes it and fails on mismatch):

1. **Base** = the weakest base among cited sk ids (`ASSERTED < REASONED < MEASURED`). A
   decision citing exactly ONE sk object is demoted one further grade (floor `ASSERTED`):
   adopting a corpus-wide default from a single claim is itself an assertion the corpus does
   not evidence (this is what puts PA-D9 at `ASSERTED`).
2. **Suffixes** = union over cited ids, rendered in the scheme's suffix order.
3. **Flags** = union of claim-level flags, PLUS decision-level `DATED` when any cited id's
   owning source has `technology_contingency.applicable: true` in its audit record and that id
   has no `durable_mechanism` row in
   `canon/planning/PROPOSED-claim-dating-annex-v1.yaml` (the audit gate itself says the
   durability question is live for every claim of such a source), PLUS decision-level
   `MEDIUM-UNTESTED` when any cited id appears in the annex's `medium_transfer_untested`
   rows (GAP-LEDGER G2/G5: flagged untested, presumed neither way). `MEDIUM-UNTESTED`
   renders after the claim-flag order.
4. **Origin** = `SINGLE-ORIGIN` / `MULTI-ORIGIN(n)` where n is the exhaustive maximum
   mutually-independent subset of the decision's cited source ids under
   `canon/validation/validate_audit_gate_v02.independent_origins_ok` — the same pairwise rule
   the coverage builder uses. Companion volumes therefore do not double-count (CA-D9, citing
   Grammar of the Shot and Grammar of the Edit, is `SINGLE-ORIGIN`). Claim-level cross-source
   consensus remains uncomputable (0 cross-source relations committed) and is not claimed.

Rendering: `[BASE{suffixes}|FLAGS...|MEDIUM-UNTESTED?|ORIGIN]`. Markers label evidence
character; they never rank sources.

## 5. Mandatory verbatim limit lines

Exact strings, grep-checked by the validator (constants live in the compiler and validator):

- **Both packs** (GAP-09, A14 absent): "Devanagari correctness criteria do not exist in Canon
  — never generate Devanagari glyphs; composite text deterministically."
- **product_appearance** (GAP-16): the LSM later-chapters coverage caveat — the pack states
  that the source's later chapters are HOLD and are recorded as qualifying and in places
  reversing ch3 guidance, citing the caveat's **existence only**; no HOLD content is consumed.
- **PA-D9** (A13 `application_unbound`): "Packshot convention absent from Canon …" — the
  hero-angle default is one 1949 cinema-era claim and must not be overgeneralized.
- **CA-D6** (A01/G2): no accepted source treats fixed 9:16 feed frames; transfer untested.

## 6. Byte stability and corpus stamping

Serialization: `yaml.safe_dump(sort_keys=True, allow_unicode=True, width=100)`, LF, UTF-8, no
timestamps, no environment-dependent content. Two compiles of unchanged inputs are
byte-identical (`--check` proves it; the validator re-proves it against committed bytes).

Every pack stamps `corpus_digest` = the accepted-corpus `combined_digest` of
`canon/knowledge/CANON-CORPUS-INDEX.yaml` (`fingerprints.accepted_canon`), recomputed two
ways before stamping: each listed file's bytes are re-hashed against its recorded sha256
(stale index = hard fail), and the combined digest is recomputed from the sorted
`path:sha256` rows (algorithm of `canon/knowledge/build_corpus_index.py::fingerprint`). A
stale stamp is a validation FAIL. The digest changes only when the accepted corpus changes —
the cache requirement of COMPILED-PACK-CONTRACT §6.

## 7. Sizing (every figure recomputable)

Terse rendering: header + per-decision `id [marker] / Q / DEFAULT / CHECK (/ LIMIT)` + the
pre-arbitrated conflict rules + pack limits. Budget: **≤ 2,500 tokens per pack at 4
chars/token** (≤ 10,000 chars), enforced at compile time and validation time. Compiled
pilots (recompute: `counts` block of each pack, or rerun the compiler):

| pack | decisions | cited sk objects | cited claim bytes | terse chars | terse tokens |
|---|---|---|---|---|---|
| product_appearance | 10 | 32 | 13,132 | 7,734 | 1,934 |
| composition_and_attention | 11 | 65 | 26,857 | 9,983 | 2,496 |

Union: 21 decisions, 97 distinct cited sk objects, 39,989 distinct-claim bytes (~10.0K tokens
verbatim; recompute: sum `len(claim)` over the union of cited sk ids). Against the injection
budget: the trigger table's largest legal combination — the uncertainty union of 10 packs —
is 38,188 tokens ≤ 45,000 (`canon/packs/pack-triggers-v0.yaml`, recomputed mechanically by
the validator). Terse doctrine is injected; verbatim claim text is reserved for CONTESTED
pairs at a later, Controller-authorised fidelity step.

## 8. What a compile + PASS establishes, and does not

Establishes, mechanically: accepted-audited citations only; zero HOLD/candidate ids; guard
closure; markers that recompute; budgets that hold; a fresh corpus stamp; deterministic
bytes. Does NOT establish: relevance to any brief, doctrine quality, medium fit, outcome
improvement, budget adequacy, or adoption. No artifact of REP-05 admits a source or asserts a
Controller decision; `coordination/CONTROL-STATE.md` governs.
