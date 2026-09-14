# Handoff — the USD-0 tranche of 14 September 2026

**Written by the lead implementation agent at the end of the tranche. Nothing here spent money, called
a provider, or merged anything. Two PRs are open for the Controller; the Controller merges.**

## A. Refs

| What | Ref |
|---|---|
| `main` (unchanged) | `dcfa6af1064b55761b89be29ef5ae22710fdd4cf` |
| Closeout branch start | `work/audit-closeout-and-runtime-v0` @ `e57bb36ef66edb5e918231afaf03c9c23f17b188` |
| Closeout branch final | `work/audit-closeout-and-runtime-v0` @ `c771fef` — **PR #95** → `main`, https://github.com/chawlavaibhav/media-intelligence/pull/95 |
| Runtime child branch | `work/runtime-alpha-vertical-slice-v0` (from `c771fef`) — stacked PR → the closeout branch (link in the PR list) |
| PR #94 (the audit brief) | untouched, still open |

## B. What happened, in one paragraph each

**Closeout.** Four lanes in isolated worktrees: (A) six Controller records materialising rulings
C-1…C-11 verbatim with provenance, every open item on the 10-Sep decision sheet dispositioned, the
handoff's "four branches / none pushed" corrected; (B) the routing map and taint register regenerated
under C-3/C-4/C-6b/C-6c/C-6d from the sealed run directories through one arithmetic (36 clean / 25
directional / 0 awaiting; RR-16 withdrawn; RR-1 rewritten; the two exact-text cells re-keyed with
`text_mechanism` on every cell); (C) cumulative budget lineage in the ledger (`budget_id` / `amends`),
replayed against the sealed Wan 2 ledgers, plus a vendor-billed reconciliation field that blocks
nothing; (D) Alpha-1 policy as data with `adopted: true` and `spend_authority: none` everywhere. The
lead adapted the router to the re-keyed evidence (26 of 61 cells auto-route under the alpha profile,
was 16), refreshed `PROJECT-MEMORY.md` and `CONTROL-STATE.md` (C-6) with byte-for-byte snapshots, and
added a re-runnable sealed-evidence verifier.

**Vertical slice.** Four more lanes: (E) intake and compiler bridged to the v1 contracts — the two
runtime lanes had never actually connected — with a Stage-A blueprint planner at USD 0 and briefs
derived mechanically from frozen cases; (F) the dry-twin profile, scoped route exclusions, the
execution bridge through the harness adapters, `execute()` failing closed on spend authority; (G) the
package renderer, pre/post gates over `canon.gate`, bounded repair, human-acceptance states, the
OUTCOME-EVENT-v1 store and a loop driver; (H) Canon Injection v1 (receipt-free 328-token prefix) and
the template library. The lead wired the one-command chain (`runtime/alpha/`), ran a 14-run dry
battery over existing briefs and committed the results, and repaired four seam defects the battery
exposed.

## C. Controller decisions materialised

`coordination/decisions/` — six records dated 2026-09-14: `CONTROLLER-AUDIT-CLOSEOUT-CAP-CROSSINGS-AND-CALL-LIMIT`
(C-1, C-5b, C-2); `CONTROLLER-AUDIT-CLOSEOUT-EVIDENCE-RULINGS` (C-3, C-4, C-6b, C-6c, C-6d);
`CONTROLLER-AUTHORISATION-LINEAGE-CUMULATIVE-BUDGET` (C-6a); `CONTROLLER-GOVERNOR-REFRESH-ORDER` (C-6);
`CONTROLLER-ALPHA-1-PRODUCT-FAMILY-AND-RELEASE-POLICY` (C-7, C-8, C-11 — twelve conditions verbatim);
`CONTROLLER-CAPABILITY-LAB-STOP-WIDENING-AND-CANON-INJECTION-V1` (C-9, C-10). Each carries the rider:
adopting the Alpha policy is not spend authorisation. C-5 recorded as withdrawn (context only).

## D. Product chain — before / now / still missing

| Component | Before (10 Sep) | Now (child branch, dry) | Still missing |
|---|---|---|---|
| Customer intake | fixture briefs → v0 contract; consent keyed on role | PRODUCTION-JOB-v1; consent on `depicts_identifiable_person`; C-7 limits enforced from the profile; briefs derived from frozen cases | live customer API |
| Production Specification | v0 spec, not loadable by the router | v1 spec the router loads; scoped `route_exclusions`; `text_mechanism`; `waived_capabilities` | contract version declaring the interface keys (`schema`, `blueprint`, `text_mechanism`) |
| Reasoning pass | recorded fixture only | Stage-A blueprint fixture, recorded fixture, or template (no model call) | a live planner that writes gate-conformant prompts |
| Canon injection | v0 block with receipt instructions | v1 receipt-free prefix, `prefix_sha256`, accepted packs only, missing domains named | cache pricing pin; packs' own terse text still carries receipt vocabulary |
| Route decision | evidence-aware, 16/61 auto-routable; exact-text cells collided | mechanism-keyed cells; eliminated routes refused by name; 26/61 auto-routable | a second usable route for photo edits / person references |
| Execution | `execute()` refused ("no client") | EXECUTION-MANIFEST-v0 through harness `dry_run()`; ceilings per attempt; fallback conditional; `execute()` checks spend authority first | live transport (deliberately absent); signed runtime spend record |
| Pre-dispatch gate | gate exists (canon/gate), never fed by the runtime | fed by the package renderer; blocks on LIMIT-TEXT / DISPATCH-* | gate-conformant frozen blueprints |
| Post-draw check | interface only in prose | over synthetic PNG/MP4 + scripted detector; NOT_RUN when no artifact | a real artifact; a paid detector under its own authorisation |
| Bounded repair | none | explicit repair request with provenance; allowance from the profile; exhaustion refuses | — |
| Human acceptance | none | pending_human → accepted / rejected / repair_requested; release by a person only | — |
| Empirical memory | OUTCOME-EVENT-v0 contract, nothing wrote one | OUTCOME-EVENT-v1 written, immutable, `dry_run: true` | a real (non-dry) event |
| Template library | none | TEMPLATE-v0; promote from a human-accepted event; repeat job served without a reasoning pass | a template from a real outcome (dry-only today) |

## E. Parallel-agent report

| Lane | Branch / worktree | Owned files | Commits | Verification | How the lead reviewed |
|---|---|---|---|---|---|
| A governance | `work/closeout-a-governance` | `coordination/decisions/*-2026-09-14.md`, decision sheet, handoff, audits README, DECISION-LOG | `ae5ba7d` | 15 verbatim quotes checked programmatically; runtime 127 OK | read all six records against the ruling text; fixed its one inference in the handoff after B's counts landed |
| B evidence | `work/closeout-b-evidence` | `evidence_map.py`, recompute + taint tools, regenerated map/register, audit addendum | `16858b5` `47418d7` `57bba0d` `603c6e4` | harness 374 OK; Registry PASS 575; `--check` UNCHANGED; sealed trees untouched | re-ran `--check`, validator, sealed diff; inspected the re-keyed cells and RR-1/RR-16 text |
| C spend | `work/closeout-c-spend` | `ledger.py`, lineage tests, example auth, README, `reconcile_spend.py`, spend addendum | `1c4169b` | harness 378 OK; replay shows 8.480/8.39 and 11.840/11.53 refused | read the pooling rule and `_matches`; re-ran the 16 lineage + 23 ledger tests |
| D alpha policy | `work/closeout-d-alpha` | `POLICY-PROFILES.yaml`, REQUIRED-LIMITS, profile accessors, `ALPHA-1.md`, tests | `5ee4cc8` `237046b` | runtime 161 OK, 2 expected failures | read the profile diff line by line; re-ran the suite |
| E contracts | `work/vs-e-contracts` | intake, spec, normalize, paths, cli, fixtures, brief tools | `a8754fe` `efc637d` | runtime 222 OK | re-ran the merged suite; repointed 6 tests written against the old `dry` row |
| F execution | `work/vs-f-execute` | `runtime/execute/**`, EXECUTION-MANIFEST-v0, dry-twin profile, exclusion scope, `execute()` | `3f8e564` `afca541` | runtime 218 OK, exploding-socket test | read the bridge's build/run; verified manifests on the fixtures and in the battery |
| G loop | `work/vs-g-loop` | `runtime/loop/**`, OUTCOME-EVENT-v1, synthetic fixtures | `d8cb9c9` `488baaf` `9bb959e` `6871d8a` | runtime 249 OK | re-ran its tests; drove all four loop paths through the CLI |
| H canon | `work/vs-h-canon` | `packs.py`, INJECTION-PREFIX-v1, `templates.py`, TEMPLATE-v0 | `76c3059` `6900464` `6c97583` | runtime 194 OK | re-ran its tests; corrected TEMPLATE-v0's `main` requirement after the battery |

Integration commits by the lead: `f1007a7` verifier, `db3f533` snapshots, `1113e40` router adaptation,
`c771fef` Governor refresh, `77bdca4` Wave-2 test repointing, `0a40542` alpha slice + battery, plus
the eight `Integrate lane …` merge commits.

## F. Verification (child branch head; closeout head where noted)

```
python3 -m unittest discover -s runtime/tests -p 'test_*.py'                    # 403 OK (baseline 127)
cd eval/harness-v2 && python3 -m unittest discover -s tests -p 'test_*.py'      # 390 OK at c771fef (baseline 362); child branch does not touch eval/
python3 eval/registry/validate_registry.py                                      # PASS, 575 rows
python3 coordination/audits/tools/verify_price_pins.py                          # 81/81, 2 warnings (pre-existing ellipsis quotes)
python3 coordination/audits/tools/build_taint_register.py --check               # UNCHANGED
python3 coordination/audits/tools/recompute_elimination.py                      # exit 0 (63 groups, 12 disagreements recorded)
python3 coordination/audits/tools/reconcile_spend.py                            # USD 122.241262 against caps; vendor billed: not reconciled
python3 coordination/audits/tools/verify_sealed_evidence.py --against origin/main  # 311/311 re-hash; sealed trees UNCHANGED
python3 -m unittest tests.test_gate_artifact tests.test_gate_predispatch tests.test_gate_postdraw \
   tests.test_gate_package tests.test_gate_doctrine tests.test_gate_cli tests.test_gate_textscan \
   tests.test_gate_regression_battery                                           # 274 OK, 1 expected failure
python3 -m tests.test_gate_regression_battery --table                           # 172 rows, 0 mismatches
python3 -m runtime.alpha.battery                                                # 14 runs, 14 intended states or precise refusals, 0 crashes, USD 0
```

## G. Dry Alpha battery (`runtime/battery/results/2026-09-14/SUMMARY.yaml`)

| Run | Route (primary / fallback) | Policy outcome | Gate | Repair | Final dry state | Reason where refused |
|---|---|---|---|---|---|---|
| B02 static ad, frozen blueprint plan | flux-2-pro / qwen-image-3; text composed from `IMG-TEXT/flux-2-pro+code_overlay` | routed | pre **FAIL** LIMIT-TEXT | — | abandoned (nothing dispatched) | frozen plate prompt: "poster" in sentence 1, no deferral term (DEF-1) |
| B03 Devanagari overlay, RR-3 exclusions | same; exclusions `scoped_out` (plate route kept) | routed | pre **FAIL** LIMIT-TEXT | — | abandoned | same defect |
| B01 static ad, exact overlay copy (recorded plan) | flux-2-pro / qwen-image-3 | routed, 4 attempts rendered, 2 would dispatch | PASS | 0 | **accepted**; event written; template `reusable_dry_only` | — |
| B04 static ad, no text, product hero | flux-2-pro / qwen-image-3 | routed (exact-text requirement waived, on record) | PASS | 0 | **accepted** | — |
| B05 short motion from the accepted still | minimax-h3-max-i2v / veo-3.1-fast-i2v | routed; accepted still handed over as `image_url`; **fallback not executable at 4:5** (Veo enum 16:9/9:16) | PASS | 0 | **accepted** | — (fallback gap recorded on the manifest) |
| B06 supplied photo, identifiable staff member, no consent | — | **refused at intake** | — | — | refused | `CONSENT_MISSING` |
| B07 same, with consent | seedream-5-pro-edit / none | **manual_route_required** | — | — | manual | `fallback_required` and no second eligible route (IMG-EDIT directional) |
| B08 person references with consent | — | **refused at spec** | — | — | refused | `ACCEPTANCE_STYLE_VIOLATION`: frozen contract line opens "ACCEPT only if," (DEF-4) |
| B09 text in motion | — | refused at intake | — | — | refused | `KIND_NOT_IN_PROFILE` (C-7) |
| B10 marketplace talking-head ad (UW-008) | — | refused at intake | — | — | refused | `KIND_NOT_IN_PROFILE` (C-7) |
| B11 customer ceiling USD 0.02 | flux-2-pro / qwen-image-3 | **manual_route_required** before dispatch | — | — | manual | `cost_envelope_exceeded` 0.08 > 0.02 |
| B12 baked lettering on draw 1 | flux-2-pro / qwen-image-3 | routed | PASS; post-draw FAIL then PASS | 1 | **accepted** (attempt 2 `is_repair_of` attempt 1) | — |
| B13 lettering on every draw | same | routed | post FAIL ×2 | 1 (allowance) | abandoned | `REPAIR_ALLOWANCE_EXHAUSTED`; no hidden retry |
| B14 identical repeat job | same | routed | PASS | 0 | **accepted**, planner `template:<B01>` | — |

No crash, no hidden default, no arbitrary route, no silent downgrade. Every synthetic input is labelled
as such in the objects written; a dry event is memory of the chain, never of a real outcome.

## H. Contract defects found by building (none hidden)

1. **DEF-1 — the frozen Stage-A plate prompts fail the gate they predate.** `LIMIT-TEXT` scans sentence
   by sentence; IMG-TEXT-01/-02's textless plate prompts say "poster" in sentence 1 with the no-text
   clause only in the last sentence. The blueprints are sealed; the runtime records the refusal.
   Prospective fix: prompts written to the gate's rule (the recorded plan in B01 shows the shape).
2. **DEF-2 — the two runtime lanes never connected.** PC-03A compiled v0 objects the PC-03B router
   refused (`paths.py` bound v0; no `schema`/`policy_profile`; consent keyed on role). Closed (lane E).
3. **DEF-3 — PRODUCTION-SPEC-v1 declares neither `schema`, `blueprint` nor `exact_text.text_mechanism`**,
   yet the router requires `schema`. Carried as interface keys beside the contract; the next contract
   version should declare them.
4. **DEF-4 — two frozen acceptance-contract lines fail the runtime style guard** (IMG-REF-02,
   VID-TOPO3-01 open "ACCEPT only if," with a comma). Refused, not edited; a style-file decision.
5. **DEF-5 — `route_exclusions.scope` was ignored by the router**, dropping the cheapest plate route for
   overlay jobs. Closed (lane F).
6. **DEF-6 — `execute()` checked `adopted` only, not spend authority.** Closed (lane F).
7. **DEF-7 — a kind's unconditional `exact_text_composition` sent text-free static ads to a person.**
   Closed as data (`kind_capability_conditions`) with the waiver recorded on the spec.
8. **DEF-8 — `reference_fidelity` demanded of a motion-from-still job** (no route answers VID-I2V and
   IMG-REF at once). Closed as data (facet applies to still images). A static ad with a supplied
   product photo still demands two questions from one call (lane E's finding) — open.
9. **DEF-9 — a video blueprint's single §6 prompt was not recognised as the motion prompt.** Closed.
10. **DEF-10 — TEMPLATE-v0 required `generation_prompts.main`**, which code-composed text never
    dispatches. Corrected the same day it was written.
11. **DEF-11 — the compiled packs' terse text carries the retired receipt vocabulary** (the terse header
    sentence and PA-D10/CA-D9 name DOCTRINE_DEVIATIONS). Canon-stream; not edited; the lookup records a
    notice. Removing it is a pack recompilation, not authorised by C-10.
12. **DEF-12 — the declared fallback for a 4:5 image-to-video job is not executable** (Veo 3.1 fast
    i2v pins 16:9/9:16 only). The manifest records `if_triggered_would_dispatch: false`; a fallback
    trigger would hand to a person. The router's fallback check is evidence-only.
13. **DEF-13 — the `dry` row was permissive** (all kinds, all statuses, 0 draws), so a dry battery could
    exercise no policy path. Replaced by the dry twin of `alpha_human_release` (lead's choice).
14. **Observation (not fixed):** among evidence-eligible routes the router orders by cost only; RR-2's
    positive preference (Nano Banana 2 / GPT Image 2 for in-scene text) is not encoded, so an in-scene
    job under a wider profile would pick qwen-image-3 (cheapest, 3/4). Out of Alpha 1 by C-7.

## I. Remaining blockers

- **USD-0 engineering:** a contract version declaring the interface keys (DEF-3); a style-file ruling
  on DEF-4; the IMG-CORE+IMG-REF single-call requirement (DEF-8 residue); pack recompilation for
  DEF-11 only if the Controller reopens packs; live transport behind the bridge (deliberately unbuilt
  until a spend record exists); a customer-facing API.
- **New Controller decision:** who reads the four provider statements (C-2 left it open); whether
  Alpha-1 prompts may be written by a live reasoning pass (that is a paid call per plan) or must be
  recorded plans; a signed runtime spend authorisation record (the object `spend_authority.record`
  would name) — shape proposed in `runtime/execute/authorisation.py`.
- **Paid evidence:** the first real Alpha-1 run (see J); C-13 Gemini API smoke for the two still
  routes priced on an untested surface; C-15 clean reruns only for the three `replacement_needed`
  cells if Alpha traffic ever needs them (it does not today).
- **External / commercial:** vendor statements; output-rights, provider commercial-terms review,
  retention policy, refund behaviour — none exists (Report A §6 "Missing operations"; T8 conditions).

## J. First paid tranche recommendation (not executed)

**One static overlay ad, end to end, on the cheapest clean route.** Brief `img-text-02-conformant`
(the AlphaFit offer; exact Latin overlay copy), profile `alpha_human_release`, `dispatch_mode: live`,
job ceiling USD 0.20, 0 retries: two plate draws on **flux-2-pro on fal** (USD 0.03 each, cell
`IMG-CORE/flux-2-pro` clean; text composed by code from cell `IMG-TEXT/flux-2-pro+code_overlay`, 4/4),
fallback **qwen-image-3** (USD 0.04), pre-dispatch gate, post-draw with the scripted detector replaced
by a real inspection by the Controller, human accept/reject, one real OUTCOME-EVENT and, if accepted,
the first non-dry template. Cost ≈ USD 0.06–0.14. It is the smallest experiment the runtime now
justifies because every other box of the chain has been exercised dry; what it measures is whether the
chain produces a customer-acceptable result at all, which no amount of further dry work can.
Prerequisites before the record is signed: the live transport wired behind `ExecutionBridge.run()`,
and a decision on whether the plan comes from a recorded fixture (as in B01) or a paid reasoning pass.

## K. Diff safety

- Sealed experiment evidence unchanged: `verify_sealed_evidence.py --against origin/main` → 311/311,
  UNCHANGED, on both branches.
- No paid authorisation created: every profile `spend_authority.status: none`; no `*.local.yaml` read
  or written; `coordination/audits/vendor-statements/` does not exist.
- No provider call made; the whole chain runs under an exploding socket in a fresh interpreter
  (`runtime/tests/test_alpha_cli.py::NoSocketEver`).
- Spend = USD 0.
