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
