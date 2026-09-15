"""The loop driver: package -> pre-dispatch gate -> (dry) attempts -> post-draw gate -> bounded
repair -> human acceptance -> OUTCOME-EVENT-v1.

    run_loop(spec, blueprint, manifest, profile, *, artifact_provider, detector, human_verdicts)

- `artifact_provider(attempt) -> bytes | None` is what "drawing" is in this tranche: synthetic bytes
  (runtime.loop.synthetic) or None. It is called at most once per manifest attempt and never after
  a block, an exhaustion or a terminal decision — there is no hidden retry anywhere in this file.
- `detector` is the text detector for the post-draw scan (a ScriptedDetector fixture here).
- `human_verdicts` is the ordered list of decisions a person would record, as dicts
  {decision, by, note, utc, contract_lines_failed}; each PASS consumes the next one. With none
  left the loop stops at pending_human and writes no event (a pending job is not an outcome).

SEQUENCE. A pre-dispatch FAIL blocks: no attempt is drawn, the acceptance is abandoned with the
failing ids, the event records zero attempts. Otherwise each manifest attempt is drawn and gated;
a post-draw FAIL asks repair.propose for a bounded repair and the NEXT manifest attempt runs as
`is_repair_of` the failed one; RepairAllowanceExhausted (or no attempt left) abandons. A post-draw
PASS goes to the person; accepted/rejected end the loop; repair_requested seeds a repair the same
way a gate FAIL does. A NOT_RUN (no artifact) attempt is recorded and the loop moves on; if nothing
ever reached a person the acceptance is abandoned as "nothing to accept".

Every limit comes from the profile row via profile.limit; the manifest's own dispatch_mode says
whether the attempts were dry. Nothing here computes a price: incremental_cost_usd for a repair is
the next manifest attempt's expected_cost_usd, as lane F priced it.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from runtime.errors import Refusal
from runtime.loop import memory, package, postdraw, predispatch, repair
from runtime.loop.acceptance import Acceptance
from runtime.loop.refusals import RepairAllowanceExhausted

BLOCKED_PRE, PENDING, TERMINAL = "blocked_pre_dispatch", "pending_human", "terminal"


@dataclass
class LoopResult:
    state: str                      # blocked_pre_dispatch | pending_human | terminal
    acceptance_state: str
    package_text: str
    pre: dict
    attempts: list = field(default_factory=list)
    repairs: list = field(default_factory=list)
    acceptance: Acceptance | None = None
    event: dict | None = None
    written_path: str | None = None
    refusal: str | None = None      # code of the refusal that ended the loop, if one did
    reason: str = ""


def descriptor_for(spec: dict, attempt: dict) -> dict:
    """The dispatch descriptor the gate compares against: the attempt's rendered request body when
    it carries one of the two shapes the gate reads, else the descriptor derived from the spec."""
    body = ((attempt.get("request") or {}).get("body")) if isinstance(attempt, dict) else None
    if isinstance(body, dict) and ("parameters" in body or "generationConfig" in body):
        return body
    return predispatch.dispatch_descriptor(spec)


def _attempt_record(attempt: dict, manifest: dict, *, now_utc: str, artifact, pre_sha: str,
                    post: dict, is_repair_of=None, repair_id=None) -> dict:
    price = attempt.get("price") or {}
    dry = manifest.get("dispatch_mode", "dry") == "dry"
    rec = {
        "attempt_id": str(attempt["attempt_id"]),
        "slot": str(attempt.get("slot") or "primary"),
        "draw_index": int(attempt.get("draw_index", 1)),
        "route_decision_id": str(manifest.get("decision_id") or "not stated"),
        "route_key": str(attempt["route_key"]),
        "surface": str(attempt.get("surface") or "not stated"),
        "surface_model_id": attempt.get("surface_model_id"),
        "requested_utc": now_utc,
        "latency_s": None,
        "status": "dry_not_sent" if dry else "ok",
        "artifact_sha256": hashlib.sha256(artifact).hexdigest() if artifact is not None else None,
        "artifact_origin": "none" if artifact is None else ("synthetic" if dry else "provider"),
        "reserved_usd": "0" if dry else str(price.get("expected_cost_usd", "0")),
        "settled_usd": "0",
        "billing_state": "not_dispatched" if dry else "unknown_provisional",
        "billing_pool": str(price.get("billing_pool") or "not stated"),
        "is_repair_of": is_repair_of,
        "repair_id": repair_id,
        "gate_pre_report_sha256": pre_sha,
        "gate_post_report_sha256": post["report_sha256"],
        "gate_post_verdict": post["verdict"],
        "_post": post,
    }
    return rec


def run_loop(spec: dict, blueprint: dict, manifest: dict, profile, *, artifact_provider, detector,
             human_verdicts: list, product_entity: bool = False, write: bool = False, store=None,
             now_utc: str = "2026-09-14T00:00:00Z", canon_lookup: dict | None = None,
             frame_sampler=None, source_still_clean=None) -> LoopResult:
    """`frame_sampler(attempt, artifact_bytes) -> list[bytes] | None` samples frames from a returned video
    for the post-draw text scan (runtime/loop/frame_hygiene). Without one, a video attempt's post-draw
    verdict is NOT_RUN and nothing can be accepted — the rule promoted from UPWORK-INTRO-001."""
    verdicts = list(human_verdicts or [])
    dry = manifest.get("dispatch_mode", "dry") == "dry"
    acceptance = Acceptance(profile)
    package_text = package.render_package(spec, blueprint)
    pre = predispatch.run(spec, package_text, predispatch.dispatch_descriptor(spec),
                          product_entity=product_entity)
    result = LoopResult(state=PENDING, acceptance_state=acceptance.state, package_text=package_text,
                        pre=pre, acceptance=acceptance)

    if pre["verdict"] != "PASS":
        acceptance.abandon(now_utc, f"pre-dispatch gate {pre['verdict']}: {', '.join(pre['blocking_failures'])}"
                                    " — nothing dispatched")
        result.state, result.reason = BLOCKED_PRE, "pre-dispatch gate blocked the job"
        return _finish(result, spec, manifest, profile, blueprint, dry, write, store, now_utc, canon_lookup)

    attempts_in = list(manifest.get("attempts") or [])
    pending_repair = None          # (repair dict, failed attempt_id) to attach to the next attempt
    reached_human = False
    for i, attempt in enumerate(attempts_in):
        artifact = artifact_provider(attempt)
        frames = frame_sampler(attempt, artifact) if (frame_sampler is not None and artifact is not None) else None
        post = postdraw.run(spec, artifact, descriptor_for(spec, attempt), package_text,
                            product_entity=product_entity, detector=detector, frames=frames,
                            source_still_clean=source_still_clean)
        rec = _attempt_record(attempt, manifest, now_utc=now_utc, artifact=artifact,
                              pre_sha=pre["report_sha256"], post=post,
                              is_repair_of=pending_repair[1] if pending_repair else None,
                              repair_id=pending_repair[0]["repair_id"] if pending_repair else None)
        result.attempts.append(rec)
        if pending_repair and acceptance.state == "repair_requested":
            acceptance.reopen(now_utc, f"repair draw {rec['attempt_id']} in front of the person")
        pending_repair = None

        failure = None
        if post["verdict"] == "FAIL":
            failure = post
        elif post["verdict"] == "PASS":
            reached_human = True
            if not verdicts:
                result.state, result.reason = PENDING, "post-draw PASS; awaiting a human decision"
                return result
            v = verdicts.pop(0)
            acceptance.record(v["decision"], v.get("by"), v.get("note", ""), v.get("utc", now_utc),
                              contract_lines_failed=v.get("contract_lines_failed"))
            if acceptance.state in ("accepted", "rejected"):
                break
            failure = v          # repair_requested
        else:
            continue             # NOT_RUN: nothing drawn, nothing to repair or accept

        nxt = attempts_in[i + 1] if i + 1 < len(attempts_in) else None
        cost = ((nxt or attempt).get("price") or {}).get("expected_cost_usd", "0")
        try:
            req = repair.propose(failure, spec, profile, len(result.attempts), incremental_cost_usd=cost,
                                 fallback_triggers=manifest.get("fallback_triggers"),
                                 fallback_route=nxt.get("route_key") if nxt and nxt.get("slot") == "fallback" else None)
        except RepairAllowanceExhausted as exc:
            result.refusal = exc.code
            acceptance.abandon(now_utc, f"{exc.code}: {exc.message}")
            break
        except Refusal as exc:
            result.refusal = exc.code
            acceptance.abandon(now_utc, f"{exc.code}: {exc.message}")
            break
        result.repairs.append(req)
        if nxt is None:
            acceptance.abandon(now_utc, f"repair {req['repair_id'][:12]} proposed but the manifest has no "
                                        f"further attempt (max_provider_draws reached)")
            break
        pending_repair = (req, rec["attempt_id"])

    if acceptance.state in ("pending_human", "repair_requested"):
        acceptance.abandon(now_utc, "no artifact reached a passing post-draw gate; nothing to accept"
                           if not reached_human else "attempts exhausted before a decision")
    result.state = TERMINAL
    return _finish(result, spec, manifest, profile, blueprint, dry, write, store, now_utc, canon_lookup)


def _finish(result, spec, manifest, profile, blueprint, dry, write, store, now_utc, canon_lookup):
    result.acceptance_state = result.acceptance.state
    post_by_attempt = [{"attempt_id": a["attempt_id"], "verdict": a["gate_post_verdict"],
                        "report_sha256": a["gate_post_report_sha256"],
                        "blocking_failures": list(a["_post"]["blocking_failures"])} for a in result.attempts]
    event = memory.assemble(spec, manifest, profile, package_text=result.package_text, pre=result.pre,
                            attempts=result.attempts, repairs=result.repairs, acceptance=result.acceptance,
                            blueprint=blueprint, dry_run=dry, canon_lookup=canon_lookup,
                            post_by_attempt=post_by_attempt)
    result.event = memory.finalize(event, now_utc)
    if write:
        result.written_path = str((store or memory.OutcomeStore(memory.paths.DEFAULT_STORE)).write(result.event))
    return result
