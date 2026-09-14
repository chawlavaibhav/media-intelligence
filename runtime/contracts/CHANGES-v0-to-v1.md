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
