# Runtime contracts — what the first lane found, and what changed

The four contracts were frozen so that parallel workers would agree on the objects they hand each
other. Then one lane actually built against them. It found **nine defects**, and it found them by
trying to compile a real Indian commercial brief rather than by reading the file.

That is the point of a vertical slice, and it is worth saying plainly: the contracts were wrong in
nine places after an hour of careful design, and one hour of use exposed all nine. No amount of
further design would have found them.

`PRODUCTION-JOB-v0.yaml` and `PRODUCTION-SPEC-v0.yaml` are kept unedited beside their v1 files, as the
record of what was frozen. The two registries and `ROUTE-DECISION-v0` were corrected in place, because
their defects were plain errors of fact rather than changes of meaning; each correction says so in the
file.

## The one that matters most: a consent hole

**v0 required a consent reference only when a reference asset's declared `role` was `person`.**

One of the fixture briefs is a Rajkot furniture showroom asking for a member of staff to be removed
from a photograph. That photograph depicts a real, identifiable person. Its role is `scene`. It passed
the consent gate untouched.

A gate that keys on how the customer labelled the file is not a gate. **v1 requires every asset to
answer `depicts_identifiable_person`, and the consent requirement keys on that answer, whatever the
role.** The field is required rather than defaulted, so a person cannot be passed through by omission.

This is the kind of defect that stays invisible until the first real customer photograph, and then
stops being a software problem.

## The other eight

| # | v0 said | Why it was wrong | v1 |
|---|---|---|---|
| 1 | A job carries a deliverable `kind` and nothing about the operation or modality | Canon's pack lookup runs before any model sees the job, so both must be readable from the job. The lane had to invent a side table. | `operation` and `modality` are job fields |
| 2 | The subject can be inferred from a supplied reference asset | A product advertisement with no customer photograph never fires the product-appearance doctrine | optional `subject` block |
| 3 | Exact text is a string, a script and a reflow flag | No way to say the text must sit *inside* the scene, so the entire in-scene branch of the evidence (RR-2, 4/4 on two routes) was unreachable from a real job | `placement: overlay \| in_scene` |
| 4 | Consent keys on `role == person` | see above | keys on depiction |
| 5 | `cost_ceiling_usd` is required, and the profile also carries a default | The profile default was unreachable, i.e. dead configuration | the job field is optional; intake fills it from the profile row before validating, so the value still always comes from data |
| 6 | `canon.missing_domain` is one string | Several triggers routinely fire with no compiled pack — six on the first brief — and one string loses which doctrine is absent | `missing_domains`, a list |
| 7 | Nothing carries an evidence-derived route prohibition | RR-3's "do not use these routes for Devanagari" survived only as prose, and the routing lane would have had to re-derive it. A prohibition that must be re-derived is one that will eventually be forgotten. | `route_exclusions` on the spec, `exclusions_applied` on the route decision |
| 8 | Nothing checks whether an input is adopted | The first alpha profile is `proposed_awaiting_controller` and all three Canon inputs are `PROPOSED`, yet nothing stopped a paid run under them | `adopted:` on every profile, and an invariant: a non-adopted input may plan and price, never spend |
| 9 | `motion.from: accepted_still` | No way to order the two deliverables, so a job could animate a still nobody had accepted — the exact input bias the evidence already carries | `motion.depends_on` |

## One thing deliberately not changed

The lane observed that `strategy_basis` inevitably names routes, which sits oddly beside the rule that
nothing in a spec may name a route. It does, and the rule stands, with `route_exclusions` as its
single declared exception. A rule that forbids routes is useless if it cannot say which ones. Both
are now written down rather than left as an inconsistency for someone to discover later.

---

# Second round — what the router lane found

The router lane was built against v1 and found four more defects. Three of them were mine, introduced
while writing the contracts; one is a standing Controller decision that nothing implemented.

**1. A status that does not exist, named in the profile that matters.** `alpha_human_release` said it
would auto-route cells whose evidence status was `launch_eligible`. The taint register has no such
status and says in writing that it never will — whether a cell may carry customer traffic is a
Controller ruling plus a policy profile, not a label an auditor stamps on evidence. The effect was
total: under the shipped alpha profile the router could auto-route **0 of 61 cells**. Corrected to
`clean_observed`.

**2. I planted it in the contract too.** `ROUTE-DECISION-v0`'s note offered `launch_eligible` as its
first example of a status, which is where the profile copied it from. Corrected, and the note now
names the register as the single source of the vocabulary.

**3. A manual decision could not be represented.** `primary` was marked required, but a decision to
hand the route choice to a person has no primary by definition. Now optional, absent exactly when
`manual_route_required` is true.

**4. An unscoped prohibition is too blunt.** RR-3 forbids certain routes from *drawing* Devanagari
text. Excluding those routes outright also deleted the RR-1 evidence, in which the same route makes a
textless plate and code sets the text — where nothing is drawn at all, and which is the cheapest exact
-text path the project has. `route_exclusions` now carries a `scope`.

**5. A Controller decision nothing implemented.** `CONTROLLER-FAL-LAST-CHOICE-CREDITS-FIRST-2026-09-09`
says that when one model is offered on both fal and a GCP surface, it is called on GCP. Nothing in the
runtime knew that. It is now `surface_preference` on the profile, with the decision cited.

The same record also warns against the misreading it invites: it is a rule about *where a given model
is called*, not a preference for credit-funded models over cash-funded ones. That decision says
plainly that preference between different models stays what the blind verdicts say, with cost as a
tie-break only. A router that quietly preferred cheaper credit routes over better cash routes would be
breaking the decision it believed it was obeying — so the profile field says so in words.

## The pattern worth noticing

Across two rounds, thirteen defects. Not one was found by reading a contract; every one was found by
building something that had to use it. Three of the four in this round were introduced by the same
hand that wrote the rule they broke.

---

# Third round — lane H (Canon Injection v1 + template library, ruling C-10)

Built at USD 0 against CANON-SHAPE-v1 §4–§6. Nothing under `canon/`, `eval/` or `coordination/`
was edited; no pack was compiled; no model was called. Four things were found by building.

**1. The v0 system block asked the model for receipts, and so do the packs.** The v0 block
(`canon/compilation/INJECTION-CONTRACT-v0.md` §2) carries three receipt instructions: "record it in
DOCTRINE_DEVIATIONS with that clause", "a DOCTRINE_DEVIATIONS entry on that decision id covers its
conflict rules", and "Answer every CHECK by decision id in FAILURE_PREVENTION as pass or fix".
CANON-SHAPE-v1 §5 retired all of them (the receipts cost about five times the rules they proved).
The runtime now injects its own receipt-free block (`runtime/canon/INJECTION-PREFIX-v1.md`, 328 of
the budgeted 340 tokens) and leaves the v0 file untouched. But the block is only the first 1.3K of
the prefix. **The two compiled packs' `terse_injection_text` (about 20K chars) open with the same
receipt sentence** — "override it in DOCTRINE_DEVIATIONS … Answer every CHECK in FAILURE_PREVENTION
as pass or fix" — and PA-D10's DEFAULT and CHECK, CA-D9's CHECK and CF-06 name DOCTRINE_DEVIATIONS
in their own text. Those bytes are canon-owned, byte-stable and validated as such, and the runtime
must not paraphrase a pack ("render by id, never paraphrase"). So under Injection v1 the model still
reads the retired instruction, from the packs. The lookup records this honestly as a notice naming the
packs, and `receipts_required` is `False` — the gate never reads receipts and nothing downstream asks
for them — but the words themselves can only go when the packs are recompiled, which is a Canon-stream
decision, not a runtime one, and is not authorised by C-10. Where the words come from:
`canon/compilation/compile_pilot_packs.py` (the terse header sentence, and the PA-D10 default at
line 211). OBSERVED; the wasted tokens per request are the receipt sentence's length, not the
receipts' — the model is not asked to write anything back.

**2. The planner fixture key includes the system block.** `FixturePlanner` keys a recorded plan by
the sha of the whole payload (system + user), so changing one word of the system block orphans every
recorded plan. The v1 default would have refused all three fixture briefs with
`PLANNER_FIXTURE_MISSING`. The index (`runtime/fixtures/planner/INDEX.yaml`) now carries the v1 keys
beside the v0 keys, pointing at the same recorded plans — legitimate because the recorded plans never
carried receipts (RESPONSE_FIELDS has no room for them), so the retired sentences change nothing a plan
contains. Worth knowing for lane E and the lead: a fixture keyed on the prefix bytes is re-keyed every
time the prefix changes, by design; that is the price of proving the prompt bytes are what we think.

**3. The spec alone cannot say what job it is.** The template identity (what makes two jobs "the same
shape") needs market, language and the supplied assets' roles. PRODUCTION-SPEC carries none of them —
`identity_requirements.preserve` holds only identity roles (a `scene` photograph is invisible), and
market/language survive only inside the brief prose. So `TemplateLibrary.promote(spec, event)` takes
the Normalized Request (`nr=`) or the job (`job=`) as well, and refuses without one rather than
guessing. The interface note said `promote(spec, outcome_event)`; the two extra keyword arguments are
the smallest honest change. If a later spec version carries the NR (or its identity facts), the
keyword becomes optional.

**4. The NR does not carry `placement` yet.** `identity_version` 1 includes each exact string's
placement (overlay vs in-scene), because those are different products. `runtime/canon/normalize.py`
(v0, read-only for this lane) does not put placement on a text requirement, so today the identity
records `placement: null` while a v1 spec's strings say `overlay`. When lane E's normaliser carries
placement, every identity sha changes. No template exists yet (the store is empty; nothing has been
accepted), so nothing is orphaned; but a template promoted under a v0 NR would not match a v1 NR, and
that is correct behaviour, not a bug — the identity says what it saw.

## Design choices the interfaces did not dictate

- **Exact-text CONTENT is in the identity.** A template's objective and prompts describe one
  customer's product ("Gupta Oil Mills' one-litre tin…"), so "the same job shape" for Alpha 1 means the
  same copy for the same product — a genuine repeat — never any Devanagari overlay ad. The slot-fill
  is still performed on every use, so the invariant "a template never carries another customer's
  strings" holds in code as well as by construction. Widening this is a new `identity_version`.
- **A dry-only template matches only under `dispatch_mode: dry`.** The dry twin profile can reuse it;
  a live job cannot. `match(nr, dispatch_mode=...)` defaults to `live`.
- **`prefix_sha256 == injected_context_sha256` in v1.** The whole payload is upstream of the cache
  breakpoint (COMPILED-PACK-CONTRACT-v0.1 §4), so both names cover the same bytes. Both are kept:
  one is PRODUCTION-SPEC's field, the other CANON-SHAPE's cache vocabulary. `cache_boundary_marker`
  is metadata about where the volatile turn begins and is never injected.
- **Refusal codes local to `templates.py`** (`TEMPLATE_PROMOTION_REFUSED`, `TEMPLATE_SLOT_MISMATCH`,
  `TEMPLATE_IMMUTABLE`, `TEMPLATE_INVALID`) rather than on `runtime.errors.Refusal`, which every lane
  edits this round. Moving them onto the class after the merge is a one-line change per code.
- **`packs_injected` beside `packs_selected`** on the template's canon block, so a reader can tell the
  doctrine that was actually in the prefix from the triggers that fired without a compiled answer.
- **No index file for the store.** `match` is an exact comparison over a directory listing; an index
  would be a second copy of the truth that can drift from the files.

## Contract added

`runtime/contracts/TEMPLATE-v0.yaml` (new, frozen). Invariants: promotion only from a human-accepted
outcome event; a dry event yields a dry-only template; exact strings are slots and are always re-filled
from the job; a template is a plan asset, never a route decision and never Registry evidence; templates
live under `runtime/store/templates`, never under `eval/`; written once; no HOLD id and no receipt
vocabulary; match is exact, newest wins.

---

# Third round — lane G (PC-03D product loop, 14 Sep 2026)

Lane G built the chain that runs AFTER a route is chosen: the package the Canon gate reads, the two
gate passes, bounded repair, the human decision, and the one immutable record of what happened. It
built against OUTCOME-EVENT-v0 and found that v0 could not hold what the chain produces. v0 is not
edited; `OUTCOME-EVENT-v1.yaml` sits beside it. What changed and why, in plain terms:

| # | v0 said | What building the loop showed | v1 |
|---|---|---|---|
| 1 | Nothing says whether the event is real | Every event this tranche writes comes from a dry run over a synthetic artifact. Without a flag, a later count of "accepted outcomes" or "cost per accepted outcome" would include rehearsals as if they were deliveries. | `dry_run: bool`, required, with the contract header saying what a dry event is memory OF (the chain) and is not (an outcome) |
| 2 | `canon.missing_domain` one string | Same defect the spec fixed in round one | `missing_domains`, a list; plus `packs_selected` as ids, and optional `corpus_digest` / `injection_prefix_sha256` for Canon injection v1 |
| 3 | No route identity on the event | C-6c makes the exact-text mechanism part of the route identity; an event that names only `route_key` cannot answer "how did code-composed plates fare on this route?" | `route {route_key, cell_key, cells, text_mechanism, surface, surface_model_id, evidence_status, price_pin_ref}` |
| 4 | No planner identity | The template library (lane H) promotes from accepted events and needs to know whether the plan came from a frozen blueprint, a recorded fixture or an existing template | `blueprint {planner, source_ref, template_id}` |
| 5 | One optional `repair` object | A job may carry more than one repair (a gate repair then a human one) and each attempt must say which repair it executes; a single object loses the chain | `repairs[]` with `repair_id`, `attempt_index`, `source`; `attempts[].is_repair_of` and `attempts[].repair_id` |
| 6 | Attempt status vocabulary has no dry value; billing_state has no "never sent" value | A dry attempt is neither ok nor an error, and its money was never reserved | `status` admits `dry_not_sent`; `billing_state` admits `not_dispatched`; `artifact_origin` says provider / synthetic / none so a synthetic PNG is never mistaken for a draw |
| 7 | Gate rows had nowhere to be linked to an attempt | The post-draw gate runs once per attempt; one `post_draw` list cannot say which attempt failed | `attempts[].gate_pre_report_sha256`, `gate_post_report_sha256`, `gate_post_verdict`; `gate.post_draw_by_attempt` |
| 8 | `acceptance` records authority and decision but not WHO | The store must refuse an "accepted" that no person recorded, and nothing in v0 carried the person or proved the transitions | `acceptance.decided_by`, `acceptance.transcript_sha256`, `acceptance.state`; the store refuses accepted without a human |
| 9 | No manifest or decision fingerprint | The attempts come from an EXECUTION-MANIFEST; an event that cannot name it cannot be audited against it | `fingerprints.decision_sha256`, `fingerprints.manifest_sha256`, optional `package_sha256` |
| 10 | `template_candidate` optional | Every terminal event answers the question (eligible or not, and why) | required, with `resulting_template_ref` for the superseding event a promotion writes |

## Things the gate or the contracts could not express (reported, not patched)

1. **The frozen IMG-TEXT-01 textless-plate prompt fails the gate.** Copied verbatim from
   `eval/empirical-planning/STAGE-A-FREEZE-2026-09/BLUEPRINTS/IMG-TEXT-01.blueprint.md` § textless plate,
   LIMIT-TEXT reports FAIL: sub-check T3, the word "poster" is in `TEXT_SURFACE_TERMS`
   (canon/gate/vocab.py) and the sentence "Diwali festive poster background, square." carries no
   illegibility or deferral term. The blueprint's own header records that the gate had not been run on
   it. The renderer does not touch prompts, so the loop's pre-dispatch blocks on this blueprint; the
   passing paths use a runtime-authored fixture (`runtime/fixtures/synthetic/blueprint-plate-clean.json`)
   that says so in its `_note`. Whether "poster" should count as a text-bearing surface in a
   background-plate prompt is a Canon-stream question, not the runtime's.
2. **The gate's LIMIT-TEXT does not fail a plate prompt that lacks a no-lettering instruction** — it
   reports the clause's presence in its PASS detail only. The loop adds its own blocking row,
   `RUNTIME-PLATE-NO-LETTERING-INSTRUCTION`, using the gate's `NO_TEXT_CLAUSE` vocabulary over the same
   extracted prompt (runtime/loop/predispatch.py).
3. **An empty pack override switches the limit off.** `run_predispatch(..., packs=[])` makes LIMIT-TEXT
   NOT-APPLICABLE. The committed spec fixtures carry `canon.packs_selected: []`, so a literal reading of
   "pass the compiled packs" would have silenced the baked-text limit on exactly the job it exists for.
   The loop passes `packs=None` (trigger table) when the spec names no compiled pack.
4. **PRODUCTION-SPEC-v1 carries no pixel minimum**, only `resolution_class`, so DISPATCH-DIMENSIONS is
   NOT-RUN on every runtime package. Not invented.
5. **The spec fixtures' `job_sha256` is an unquoted run of zeros**, which YAML reads as the integer 0.
   The event refuses a fingerprint that is not 64 hex characters (`FINGERPRINT_INVALID`); the lane-G
   tests restore the intended placeholder when loading. Lane F/E own the fixtures.
6. **The `dry` profile row has `acceptance_authority: none` and `repair_allowance: 0`** at this commit,
   so the loop's acceptance cannot record under it (refused by name). The lead's decision makes `dry`
   the twin of `alpha_human_release`; lane F owns that change. Lane G's tests run under
   `alpha_human_release`, whose `spend_authority.status` is `none` — nothing can dispatch under it.
7. **Video text scan.** stdlib cannot decode frames from an MP4, so LIMIT-TEXT post-draw is NOT-RUN on
   every motion attempt and the verdict rests on geometry, duration and track rows. The synthetic MP4 is
   header-only (ftyp + moov), enough for the probe, and is labelled as such.

---

# Third round — lane F (execution bridge, 14 Sep 2026)

Lane F built the bridge from a route decision to rendered provider attempts, under the lead's rule that
`dry` is the dry twin of `alpha_human_release`. It found three things worth recording and changed one
frozen-adjacent file by addition only.

**1. The router ignored the scope the spec contract already required.** `PRODUCTION-SPEC-v1` made
`route_exclusions.scope` a required field in round one, precisely so that RR-3's "do not let these
routes *draw* Devanagari" would not also delete RR-1's textless plate. The router's `Exclusion` had no
scope and stage 1 dropped the whole route. The effect on the most ordinary alpha job (a static ad with
code-set overlay copy): flux-2-pro, the cheapest plate at USD 0.03, was gone and qwen-image-3 (0.04)
became primary. Fixed in `runtime/route/spec.py` (`Exclusion.scope`, default `whole_route`) and
`decision.py` stage 1: a `generated_text_only` exclusion bites only when the spec's
`exact_text.text_mechanism` is `model_draws_text`, or — fail closed — when the spec carries exact text
but no mechanism. Every exclusion row on the decision now says whether it bit or was `scoped_out`, and
why. The router's own fixtures were the ones missing `scope` and `text_mechanism`; they carry both now.

**2. `execute()` checked adoption, not money.** Recorded in round two as an expected-failure test; closed.
For a live-mode profile `execute()` refuses before it plans when `may_spend()` is false, naming the
missing spend authorisation. A dry-mode profile needs no spend authority, because nothing is sent and
reservations are 0; that is the point of the twin.

**3. A dry profile with zero draws is not evidence about the alpha.** The old `dry` row auto-routed every
evidence status and allowed no draws, so a dry run under it took none of the alpha's decisions. It is
now `dry_permissive` (kept for lane development and cell audits), and `dry` copies
`alpha_human_release` verbatim with `dispatch_mode: dry`. A data test pins the twin to the alpha on every
key outside `{profile, purpose, status, adoption_basis, dispatch_mode, spend_authority, note}`.

**What changed in shared files, by addition only.** `POLICY-PROFILES.yaml`: `dispatch_mode` on every row
(`live` on the two alpha rows, `dry` on the two dry rows). `REQUIRED-LIMITS-v0.yaml`: `dispatch_mode`
required at intake and read by the bridge. `ROUTE-DECISION` (shape, not the frozen file): the `fallback`
slot now also carries `unit_price`, `unit`, `quantity`, `quantity_unit`, `price_pin_indexes`,
`surface_model_id`, `arm`, `adapter_family`, `credential_name`, so a fallback attempt is priced from the
same fields as a primary one; `exclusions_applied` rows carry `scope`, `scope_declared`, `scope_reason`
and `effect` may now read `scoped_out`. `EXECUTION-MANIFEST-v0.yaml` is new.

**What the harness said when asked to render real attempts** (observed, not inferred): the fal text-to-
image routes (flux-2-pro, qwen-image-3, gpt-image-2) and the Gemini API image route (nano-banana-2)
render a verified body from the spec alone. Every image-to-video route (minimax-h3-max-i2v,
kling-v3-pro-i2v) and every edit route (seedream-5-pro-edit) refuses with the harness's own
`input_unresolved:<role>` until the accepted still / supplied photograph is handed over as a sealed
input — which is correct, and is now visible on the manifest rather than discovered at dispatch. The
harness also refuses any caller parameter that is not an input role (a `seed`, for instance), and the
bridge keeps that refusal verbatim.

**Not changed, reported.** The router still does not read `exact_text_strategies_allowed` or
`motion_requires_accepted_still` (ALPHA-1.md already says so): under `dry`, the in-scene fixture still
routes although the twin forbids `generated_in_scene`. That enforcement belongs to the compiler / gate
lanes, not to the bridge. `surface_preference` is recorded on every manifest but applied nowhere,
because the roster offers no model on both fal and a GCP surface today; the bridge says so rather than
inventing a surface.

---

# Third round — lane E (14 Sep 2026)

The first lane wrote v1 and the router lane built against it. Neither ran a brief through both. When
the lead and lane D connected them, intake was still validating against the **v0** file
(`runtime/paths.py` bound both contracts to v0), so the consent gate still keyed on `role == person`
— the hole this document's first section says v1 closed — and the compiler emitted a spec with no
`schema` key, which `runtime/route/spec.py` refuses on its first line. Lane E bound both to v1 and
found the following while making the two ends meet. None was found by reading.

**1. v1 does not declare the keys the router requires.** `PRODUCTION-SPEC-v1.yaml` has no `schema`
field, yet `runtime/route/spec.py` refuses a spec whose `schema` is not `PRODUCTION-SPEC-v1`; the
router's own fixture specs carry it. WAVE2-INTERFACES §1 further requires `blueprint` and
`exact_text.text_mechanism` (C-6c), and v1 declares neither. A contract is never edited in place,
and a v2 file would carry a schema name the router does not accept — so the compiler validates the
contract-declared part against v1 and attaches those three keys as interface extensions
(`runtime/spec/compile.py` `INTERFACE_KEYS`, `contract_view()`). The next contract version should
declare all three. Recorded, not hidden.

**2. `character_exact` was a level nobody answered.** The compiler's facet table gave
`exact_text_composition` the level `character_exact`; the router's binding answers that capability at
`code_set_on_textless_plate` or `generated_in_scene` and refuses to choose a level on the spec's
behalf. So every exact-text spec went to a person, silently. The level is now the chosen strategy
(`FACET-CAPABILITIES-v0.yaml`, marker `exact_text_strategy`).

**3. A provenance block outside the contract.** A brief derived from a frozen Stage-A case must say
which case and which blueprint bytes it came from, so the reasoning pass can be served from that
blueprint instead of a model. v1 has no such field. Rather than a v2 for one optional key, the brief
JSON may carry a top-level `_provenance` block that intake strips before validation and stores beside
the job (`<store>/jobs/<job_id>.provenance.json`, returned as `IntakeResult.provenance`). It is never
part of the job's fingerprint. If a later contract wants it inside, it is one field.

**4. The derived acceptance line held approximate strings exact.** `exact_strings_read_exactly` fired
on every string; the first Stage-A case with an approximate string (IMG-TEXT-02, "Offer ends 15
January", may_reflow) would have been held character-exact by the runtime while the case's own line
says "readable in some wording". Now contractual strings only.

**5. Two frozen acceptance lines fail the runtime's own guard.** IMG-REF-02 and VID-TOPO3-01 open a
line `ACCEPT only if, …` (comma). `ACCEPTANCE-STYLE-v0` requires the opening `ACCEPT only if ` (space);
the Stage-A build guard (`tools/build.py` LEAK) never checked openings. Per the lane brief the line is
refused, not edited (`ACCEPTANCE_STYLE_VIOLATION` naming it). Whether the runtime's opening rule
should admit a comma clause is a question for whoever owns the style file next; the Lab file is
read-only and untouched.

**6. The router ignores `route_exclusions[].scope`** — the very field the second round added.
`runtime/route/spec.py:40-44` has no scope on `Exclusion`, `:115-120` never reads it, and
`runtime/route/decision.py:243-249` drops the whole candidate at `hard_requirements`. For a
Devanagari overlay job (IMG-TEXT-01) the compiler writes RR-3's three routes with scope
`generated_text_only` and `text_mechanism: deterministic_text_composition`, and the router still
drops `IMG-CORE/flux-2-pro` and `IMG-CORE/seedream-5-pro` as plate routes although nothing is drawn.
Lane F owns the router; the defect is pinned as an expected-failure test in
`runtime/tests/test_e_alpha_briefs.py::RouterScopeDefectTracker`.

**7. A supplied product photograph makes a from-scratch static ad unroutable.** The mustard-oil brief
(static_ad + a product photo whose label must match) compiles to `image_generation` (IMG-CORE) plus
`reference_fidelity` (IMG-REF), both mandatory and dispatching; the router requires ONE route with a
cell in both questions and no route has one, so it goes manual under every profile — including dry.
Either the binding should let an IMG-REF route answer `image_generation` when a reference is
supplied, or the compiler should express "generate with reference" as one capability. Reported for
lanes F and E to settle together; nothing changed in this round.

What was NOT changed: no `*-v0.yaml` or `*-v1.yaml` file, no file under `eval/`, `canon/` or
`coordination/`, `POLICY-PROFILES.yaml` (both limits the compiler needed were already on every row),
`runtime/canon/packs.py` (lane H), `runtime/route/**` (lane F).


---

# Third round — lead integration (14 Sep 2026)

Found by running the whole chain over the committed briefs (`python3 -m runtime.alpha.battery`), after
the four lanes were merged. Each is recorded in `coordination/audits/HANDOFF-USD0-TRANCHE-2026-09-14.md`
§H with its defect number.

1. **A kind's unconditional capability blocks the job it exists for** (DEF-7). `DELIVERABLE-KINDS`
   `static_ad` demands `exact_text_composition`; a static ad with no exact strings has no strategy
   level, so the router refused to choose and sent a routable job to a person. Now a row in
   `FACET-CAPABILITIES-v0.yaml` (`kind_capability_conditions`) waives the capability when its fact is
   absent, and the spec records `waived_capabilities`.
2. **`reference_fidelity` is an image question** (DEF-8). The `supplied_asset_present` facet demanded
   it of a motion-from-still job, which no image-to-video route answers. The facet now applies to
   `static_image` only.
3. **A video blueprint's single generation prompt is its motion prompt** (DEF-9). The blueprint planner
   now sets `generation_prompts.motion` from §6 when no `i2v_motion_prompt` block exists.
4. **TEMPLATE-v0 required `generation_prompts.main`** (DEF-10), which code-composed text never
   dispatches; corrected in the file the day it was written, before any template existed.
5. **The frozen Stage-A plate prompts fail the gate** (DEF-1) — not a contract defect but the most
   consequential finding: the gate's LIMIT-TEXT rule is sentence-local and the blueprints predate it.
   Nothing frozen was edited; one labelled runtime-authored recorded plan proves the chain instead.
