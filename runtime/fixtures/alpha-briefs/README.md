# alpha-briefs — customer requests derived from frozen Lab cases, USD 0

Every JSON file here was **generated**, not written, and regenerates byte for byte
(`runtime/tests/test_e_alpha_briefs.py::ToolDeterminismTest`). Do not hand-edit one; re-run the tool.

| file | tool and arguments | source (read-only) |
|---|---|---|
| `img-text-02.json` | `python3 -m runtime.tools.brief_from_stage_a_case IMG-TEXT-02` | Stage-A case IMG-TEXT-02 |
| `img-text-01.json` | `… IMG-TEXT-01` | Stage-A case IMG-TEXT-01 |
| `img-core-01.json` | `… IMG-CORE-01` | Stage-A case IMG-CORE-01 |
| `vid-i2v-01.json` | `… VID-I2V-01 --depends-on alpha-dry-img-core-01` | Stage-A case VID-I2V-01 |
| `img-edit-01.json` | `… IMG-EDIT-01` | Stage-A case IMG-EDIT-01 |
| `img-ref-02.json` | `… IMG-REF-02` | Stage-A case IMG-REF-02 |
| `vid-topo3-01.json` | `… VID-TOPO3-01 --depends-on alpha-dry-img-text-01` | Stage-A case VID-TOPO3-01 |
| `mkt-001.json` | `python3 -m runtime.tools.brief_from_marketplace_case MKT-001` | marketplace brief bank, MKT-001 (Upwork UW-008) |

Frozen package: `eval/empirical-planning/STAGE-A-FREEZE-2026-09` (package `STAGE-A-FREEZE-2026-09`,
base `cb92f1e`). Each brief's `_provenance` block records the sha256 of the blueprint it came from, of
`TEST-CASES.yaml` (`8c2430e760279bb60a0ce429b933c64bb85340e2089be9ebad3f28d49e7cdb9c` at generation), of
the tool, and of the kind map `runtime/tools/STAGE-A-CASE-KIND-MAP-v0.yaml`. The marketplace brief
records the sha256 of `canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml`.

## What the tool does, and refuses to do

`brief.text` is the case's `customer_request.text` verbatim. Strings, scripts, exactness, entities,
duration and aspect come from the case's frozen Normalized Request. The deliverable kind comes from the
case family through the kind map; `operation`/`modality` come from `runtime/canon/KIND-NR-BINDING-v0.yaml`
for that kind. Nothing is inferred:

- **placement** is `overlay` for every string and `_provenance.placement_default: true` says so; the
  tool never decides that copy sits on a pack or a sign.
- **consent_ref** is absent unless `--consent-ref` is given, so the consent gate fires exactly as it
  would for a real submission. `depicts_identifiable_person` is true only where the case's own
  entities put a person in the asset (`_provenance.depicts_basis` says which).
- **policy_profile** is `dry` (the dry twin of `alpha_human_release`), `retention.delete_after_days`
  is left for intake to fill from the profile, and `cost_ceiling_usd` likewise.

## Expected intake / compile outcome today (dry profile)

| brief | outcome | why |
|---|---|---|
| img-text-02 | compiles; the router plans it (primary present, self-composed cell `IMG-TEXT/flux-2-pro+code_overlay`) | Latin overlay copy, code-set |
| img-text-01 | compiles; routes with RR-3's three routes carried as `generated_text_only` exclusions | Devanagari overlay copy, code-set |
| img-core-01 | compiles | no text; product subject fires `product_appearance` |
| vid-i2v-01 | compiles | motion from the accepted still, `depends_on` the IMG-CORE-01 job |
| img-edit-01 | **CONSENT_MISSING** at intake | the showroom photo depicts the staff member to be removed; add `--consent-ref` to pass |
| img-ref-02 | **CONSENT_MISSING** at intake | three identity references of a real person |
| vid-topo3-01 | **ACCEPTANCE_STYLE_VIOLATION** at compile (with consent irrelevant) | the case's first acceptance line opens `ACCEPT only if,` (comma); the runtime guard requires `ACCEPT only if ` and the line is not edited |
| mkt-001 | **KIND_NOT_IN_REGISTRY** at intake (`KIND_NOT_IN_PROFILE` under `alpha_human_release`) | the buyer asked for a talking-head avatar; no such kind exists and C-7 excludes it |

The `_provenance` block is not a PRODUCTION-JOB-v1 field. Intake strips it before validation and
stores it beside the job (`<store>/jobs/<job_id>.provenance.json`); the compiler reads it to serve the
reasoning pass from the case's frozen blueprint (`runtime/spec/blueprint_planner.py`).
