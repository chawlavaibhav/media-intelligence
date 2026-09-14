# Alpha 1 — what it is, what it is not, and where its limits live

For a new engineer. Written 14 Sep 2026 against the Controller's rulings of that day. Every claim
below points at a file; nothing here is a chat recollection.

## What Alpha 1 is (Controller ruling C-7, verbatim)

> "Freeze Alpha 1 to: one STATIC COMMERCIAL AD WITH EXACT OVERLAY COPY, optionally followed by: one
> SHORT MOTION VERSION DERIVED ONLY FROM THE ACCEPTED STILL. Supplied-photo work is conditional
> behind the identifiable-person / consent gate. Exclude from Alpha 1: talking heads; lip-sync;
> native speech; multi-shot stories; generated in-scene exact text."

In plain terms: a customer gets one still advertisement whose price, offer, legal line or brand name
is set onto the picture **by code**, exactly as supplied. If they want it, that accepted still can
then be animated into one short silent clip. If they supply their own photograph, it can be edited,
but only once the consent gate is satisfied for anyone identifiable in it.

Record: `coordination/decisions/CONTROLLER-ALPHA-1-PRODUCT-FAMILY-AND-RELEASE-POLICY-2026-09-14.md`
(being written by Agent A; cited as the basis in the profile row).

## What Alpha 1 is not

Out by C-7's words, and recorded as data in the profile row (`excluded_by_ruling`):

| C-7 phrase | Registry kind it excludes (`runtime/contracts/DELIVERABLE-KINDS.yaml`) |
|---|---|
| "talking heads" | no registry kind of that name exists today; recorded against the phrase |
| "lip-sync" | `lipsync_to_supplied_audio` |
| "native speech" | `two_speaker_dialogue`; and `spoken_voiceover` on the most restrictive reading (narration is generated speech) |
| "multi-shot stories" | `multi_shot_story` |
| "generated in-scene exact text" | not a kind but a strategy: `generated_in_scene` is outside `exact_text_strategies_allowed` |

Also outside Alpha 1, not because C-7 names them but because C-7 *freezes* the family to the kinds it
lists: `text_in_motion`, `music_bed` (`outside_alpha_1_by_omission`).

Note the in-scene exclusion carefully. The Lab has evidence that two image models can draw exact
Devanagari text inside a scene (RR-2 in `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml`). That
capability is out of Alpha 1 **by ruling, not by capability**. Do not read the profile as saying it
does not work.

## The release policy (C-8, verbatim)

> "Every Alpha-1 output requires human approval before external delivery. No autonomous external
> delivery."

In the profile: `acceptance_authority: human`, `automated_judge_in_release_path: false`,
`autonomous_external_delivery: false`, `human_approval_required_before_external_delivery: true`.

Why a person and not the automatic judge: the judge qualification run
(`eval/experiments/EVAL-040/QUALIFICATION-REPORT-2026-09-09.yaml`, summarised in the profile note)
found the automated judge agrees with the human judge only about two thirds of the time (66 %) and
wrongly accepts 22 % of what the human rejects. A judge that passes one in five bad outputs cannot be
the thing that releases work to a customer. That is a fact about today's judge, not a permanent
property of the product; the profile invariant says an automated judge may enter the release path
only after passing qualification against frozen criteria.

## The public-release gate (C-11)

> "Adopt Auditor A's twelve-condition T8 public-release gate."

The twelve conditions are copied verbatim from `coordination/audits/AUDIT-2026-09-10-REPORT-A.md`
§7 T8 into the profile row (`public_release_gate.conditions`), and a test checks the copy against the
report line by line. **None of the twelve is met today.** Alpha 1 is a *private*, human-supervised
alpha. The gate is what would have to be true before anything is delivered automatically to the
public, and it is held as data so a later check can read it rather than re-type it.

## Where the limits live

All of them in one row: `runtime/contracts/POLICY-PROFILES.yaml`, profile `alpha_human_release`.
The runtime reads limits from that row and refuses if a limit it needs is missing
(`runtime/policy/REQUIRED-LIMITS-v0.yaml` lists which limits each lane needs; intake checks the
`required_at_intake` list before anything else runs). No limit is a constant in code; a test in
`runtime/tests/test_policy_alpha1.py` checks the two profile-reading modules for numeric literals,
and `runtime/tests/test_spec_compile.py` greps the consumers for the profile's numbers.

The values the rulings did not reopen stay as they were: two provider draws per deliverable, one
repair, a declared fallback required, USD 5.00 default job ceiling, 30 days retention, GCP preferred
when the same model is on fal and GCP.

## Adopted is not the same as allowed to spend

Two different things, deliberately kept apart in the row:

- `adopted: true` — the Controller has agreed the profile's **limits**. It is a policy.
- `spend_authority: {status: none, record: null}` — nobody has signed a spend authorisation for
  runtime dispatch under it. It is **money**, and it is absent.

The Controller's rider, 14 Sep 2026: "Adopting the Alpha policy is NOT spend authorisation. No paid
dispatch is authorised by any decision above." A dispatch needs both: adopted, and a signed record
named in `spend_authority.record`. Both profile readers expose `may_spend()`, which returns `False`
and says exactly which of the two is missing (`runtime/route/profile.py`,
`runtime/policy/profiles.py`).

**Known gap, recorded as an expected-failure test:** `Router.execute()` in
`runtime/route/decision.py` checks only `adopted`. With the profile now adopted, the only thing
between the alpha profile and a dispatch of a fully-routable spec is that no provider client exists
on this branch. The execution bridge (Wave 2) must check `spend_authority` before planning. See
`test_execute_must_refuse_on_spend_authority_none_before_planning` in
`runtime/tests/test_route_limits.py`.

## The evidence the wedge rests on

- **Exact overlay copy — RR-1** (`eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml`): code-set text
  on a cheap textless plate, 4/4 accepted at about USD 0.03 per accepted picture. Read "4/4"
  correctly: **the image model did not draw the accepted copy; code did.** The plate is generated,
  the text is composited by the runtime, so it is exact by construction. The two map cells behind
  this rule share one route key and one arm and are being re-keyed under Controller item C-6c
  (`coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`); until that lands the taint
  register marks them blocked, and the router hands a static-ad job to a person rather than
  auto-routing it. The mechanism is sound; the bookkeeping is being fixed.
- **Short motion from the accepted still — RR-8**: image-to-video on Kling v3 Pro 8/8, Wan 3.0
  Prime 8/8, MiniMax H3 Max 7/8 (cheapest), Veo 3.1 fast 5/8. The input bias is real and is why
  `motion_requires_accepted_still: true`: the 8/8 was measured on stills a person had already
  accepted, so the product only animates stills a person has accepted.
- **Supplied photo — RR-4/RR-5**: Seedream 5 Pro edit 10/12, every draw on a constructed stand-in,
  never a real customer photograph. Conditional in Alpha 1 for that reason as well as consent.

## What does not exist yet (do not claim it does)

Verified against this branch and `coordination/audits/HANDOFF-TO-CONTROLLER-2026-09-10.md` §6:

- **Execution bridge** — nothing dispatches. `Router.execute()` refuses by design
  ("no provider client is wired"). Wave 2.
- **Post-draw deterministic checks** — the spec names them (`deterministic_checks`); nothing runs them.
- **Repair loop** — `repair_allowance: 1` is read into the spec; no code performs a repair.
- **Acceptance states** — no accepted / rejected / released state exists on a job; human approval
  (C-8) is policy in the row, not a workflow in code.
- **Empirical memory event** — `OUTCOME-EVENT-v0.yaml` is a contract; nothing writes one.
- **Customer-facing intake** — `runtime/cli.py` turns a fixture brief into a spec with the planner
  answered from a recorded fixture; there is no command that accepts a live customer request.
- **Enforcement of the two new C-7 limits** — `exact_text_strategies_allowed` and
  `motion_requires_accepted_still` are data today; neither `runtime/spec/compile.py` nor
  `runtime/route/decision.py` reads them yet.
- **A second usable route for static ads and photo edits** — the handoff's most useful sentence:
  the alpha profile requires a fallback, and today those two kinds have one usable route each, so
  they go to manual routing.

What does exist on this branch: intake against the frozen job contract, brief-to-spec compilation
with deterministic Canon lookup (PC-03A), and an evidence-aware, offline router that plans, prices
and refuses (PC-03B). All of it runs at USD 0 with no network.
