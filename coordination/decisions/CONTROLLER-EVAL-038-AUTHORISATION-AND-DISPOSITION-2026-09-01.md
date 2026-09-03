# Controller — EVAL-038 Authorisation and Disposition — 2026-09-01

**Status:** APPROVED CONTROLLER DECISION.
**Role:** Writer Controller.
**Target:** `claude/canon-context-guidance-ohi1i9` (PR #83); evidence under
`eval/experiments/EVAL-038/`.

This record promotes decision note **DN-07** from
`canon/candidates/canon-014/REP-07-DECISION-NOTES.md` into `coordination/decisions/`, and records
the disposition the Controller has taken on the result. The worker session that recorded DN-07 was
blocked by its permission policy from writing here. Nothing below extends the ruling.

## 1. Authority — the Controller's words, verbatim

Recorded before any paid call, as instructed:

> I am the Controller. I approve EVAL-038 EXTENDED TO MEDIA GENERATION with a
> HARD max consumed API spend of USD 10.00 total, 0 retries, execution-time
> route/price verification before every paid call, keys from this machine.
> Record this approval verbatim as DN-07 in the REP-07 decision-notes file
> before any paid call. Media generation here is product learning — not
> Capability Registry evidence.

Execution directives, verbatim:

> Execute on a new branch off claude/canon-context-guidance-ohi1i9:
> 1. USD-0 retro-test from the EVAL-038 design (replay my two rejected
>    PILOT-001 candidates against the compiled packs).
> 2. Reasoning arms over ALL SIX EVAL-037 briefs — image and video both:
>    Haiku+packs x2 reps, unconditional injection per the injection contract;
>    then pin Gemma's official price (bytes+date, snapshot pattern — network
>    fetch authorised) and run Gemma+packs with remaining reasoning budget.
>    Baseline = the committed Sonnet NO_CANON packages; never re-run Sonnet.
> 3. Generation: for B06 (image) and B01 (video), execute BOTH the best
>    Haiku+packs package and the committed Sonnet NO_CANON package into real
>    media — 2 images + 2 videos — using the cheapest verified route.
> 4. Seal everything as committed bytes per the repo's sealed-evidence
>    conventions (EVAL-024 pattern), push, and hand me the blinded judging
>    protocol: I judge packages and media; models never judge themselves.
>
> Stop at the cap without exception; if video pricing makes step 3 exceed
> remaining budget, generate the image pair, report the exact video quote,
> and stop for my approval rather than guessing.

```yaml
machine_authorisation:
  tranche_id: EVAL-038-MEDIA-EXT
  authorised: true
  max_consumed_api_spend_usd: "10.00"
  retries_authorised: 0
  execution_time_route_price_verification: required_before_every_paid_call
  approved_by: "Vaibhav Chawla (Controller)"
  approved_at: "2026-09-01"
  media_generation_role: product learning only — NOT Capability Registry evidence
  comparators_reused_usd0: committed Sonnet NO_CANON packages (never re-run)
  stop_rule: hard stop at USD 10.00
```

The authority is spent. EVAL-038 executed within it: **USD 2.260122 consumed of the USD 10.00 cap**,
0 retries, every call price-verified, no cap breach. (The ledger carries a conservative 2.760122
including an annotated phantom 0.50 entry from a duplicate session.) This decision does not renew
the authority; no further paid EVAL-038 execution is authorised.

## 2. Disposition — what is closed

**The tested substitution configuration is closed.** Weak model plus the two compiled packs, with
unconditional injection, did not match a strong model working alone on any of the six briefs — **0
of 6**, with the three Sonnet NO_CANON repetitions taking all 18 top-3 slots under blind judging
against a decision rule fixed before execution. The economics pointed the same way independently:
the "cheap" arm cost more per package (USD 0.072 vs USD 0.063).

Consequences:

1. **Do not rerun this configuration to reconfirm it.** Two packs, Haiku/Gemma-class consumers,
   forced injection: answered.
2. **The negative result stands as committed evidence** and is never rewritten. Programme standard.
3. This closes **that configuration**, not "any compiled Canon." Only 2 of 10 packs existed; the
   evidence limits recorded in `canon/findings/PROPOSED-EVAL-038-CONCLUSION.md` §5 (single-reviewer
   package judging, blinding scrub scars, n=2 media pairs) travel with any citation of this result.
4. Media generated under this authority is **product learning only — never Capability Registry
   evidence**, per the authorisation's own terms.

## 3. Disposition — what is reserved

The Controller has reserved the verdict on whether Canon works. In the Controller's words:

> **"i don't want you to conclude this any further... It's my call eventually to decide whether it
> works or not."**

Therefore:

- `canon/findings/PROPOSED-EVAL-038-CONCLUSION.md` is a **worker proposal, not an adopted finding**.
  Its observations are on the record; its programme disposition is not a Controller decision and
  must not be cited as one.
- **No worker draws a further conclusion** about Canon's adequacy, value or production-readiness
  from this evidence. Recording an observation is permitted; issuing a verdict is not.
- The question "does the compiled-doctrine gate move the accepted-outcome rate?" is **open and
  reserved to the Controller**, to be measured rather than argued. The measurement the Controller
  may commission — acceptance-rate runs, many draws per arm, blind accept/reject — is not authorised
  by this record.

Observations that remain on the record, without verdict: the compiled doctrine forbids both
PILOT-001 candidates the Controller rejected, on the Controller's own grounds; the pack-guided
image won the B06 pair after the Controller's post-reveal revision; both B01 videos failed on
baked-in text, the exact defect the packs' overlay rule guards against; and re-executing frozen
prompts produced worse artifacts, showing draw-to-draw variance flips acceptability.

## 4. Not authorised by this decision

- any further paid execution, under EVAL-038 or otherwise;
- a rerun of the refuted configuration;
- a Capability Registry row from any EVAL-038 artifact;
- adoption of the proposed conclusion's programme disposition;
- Production IR / Planner implementation;
- compilation of the remaining 8 packs (REP-11), which this result does not justify on its own.
