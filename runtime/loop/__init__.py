"""PC-03D product loop (lane G): the runtime's gate, repair, acceptance and memory chain.

What this package does, in order, for one job:

1. `package.render_package`   — turns a PRODUCTION-SPEC-v1 plus the planner's blueprint into the
                                 FINAL_PRODUCTION_PACKAGE text the Canon gate parses (v2 schema).
2. `predispatch.run`          — runs the gate's pre-dispatch checks over that text and the dispatch
                                 descriptor BEFORE anything would be sent; a FAIL blocks the job.
3. `postdraw.run`             — runs the gate's post-draw checks over the returned artifact (in this
                                 USD-0 tranche a synthetic PNG/MP4 stub from `synthetic`, or None).
4. `repair.propose`           — a bounded repair: what failed, what changes, what stays the same;
                                 never "try again"; refuses past the profile's repair_allowance.
5. `acceptance.Acceptance`    — the human decision (C-8): pending_human -> accepted | rejected |
                                 repair_requested; delivery only by an explicit human release.
6. `memory.OutcomeStore`      — one immutable OUTCOME-EVENT-v1 per job, the project's empirical
                                 memory. In this tranche every event is `dry_run: true`: memory of
                                 the CHAIN having run, never of a real outcome.
7. `driver.run_loop`          — sequences 1-6.

Doctrine rows always come from `canon.gate`; nothing here restates a pack rule in prose. Every
operating limit is read from the policy profile row (`profile.limit(...)`); none is a constant.
No network, no model call, no provider call: the only bytes "drawn" are synthetic.
"""
