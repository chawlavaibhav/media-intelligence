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
