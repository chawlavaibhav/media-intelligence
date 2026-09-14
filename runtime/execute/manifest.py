"""EXECUTION-MANIFEST-v0 shapes: ids, hashes, the blocked form, and a rendering a person can read.

The contract is runtime/contracts/EXECUTION-MANIFEST-v0.yaml. This module holds the small, shared pieces
so bridge.py can stay about the decisions: how a manifest is identified, how an object is fingerprinted,
what a blocked manifest looks like, and how the whole thing prints.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

SCHEMA = "EXECUTION-MANIFEST-v0"
DISPATCH_MODES = ("dry", "live")

# reason_code vocabulary for manifest.blocked. Open: a new reason is a new word here, with a test.
BLOCKED_MANUAL = "manual_route_required"
BLOCKED_NO_PRIMARY = "no_primary"
BLOCKED_NO_FALLBACK = "fallback_required_missing"
BLOCKED_CEILING = "cost_envelope_exceeded"

ATTEMPT_DRY_NOT_SENT = "dry_not_sent"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")


def sha256_of(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj)).hexdigest()


def manifest_id(job_id: str, decision_id: str, profile: str, built_utc: str) -> str:
    return "em-" + hashlib.sha256(f"{job_id}|{decision_id}|{profile}|{built_utc}".encode("utf-8")).hexdigest()[:16]


def blocked(reason_code: str, reason: str) -> dict:
    return {"reason_code": reason_code, "reason": reason}


def render(manifest: dict, run_result: dict | None = None) -> str:
    """The manifest as a person reads it: what would be sent, for how much, and why not."""
    m = manifest
    out = []
    out.append("=" * 100)
    out.append(f"EXECUTION-MANIFEST  {m['manifest_id']}   job {m['job_id']}   spec {m['spec_id']}   "
               f"decision {m['decision_id']}")
    out.append(f"profile {m['policy_profile']}   dispatch_mode {m['dispatch_mode']}   built {m['built_utc']}")
    out.append("=" * 100)
    if m["blocked"]:
        out.append(f"BLOCKED  [{m['blocked']['reason_code']}]  {m['blocked']['reason']}")
        out.append("         a blocked manifest carries no attempts")
    else:
        c = m["ceiling"]
        out.append(f"CEILING  job {c['job_ceiling_usd']} USD"
                   + (f" (request ceiling {c['request_ceiling_usd']}; effective {c['effective_ceiling_usd']})"
                      if c.get("request_ceiling_usd") is not None else "")
                   + f"   reserved if every attempt ran: {c['reserved_total_usd']}   "
                   f"blocked_by_ceiling: {c['attempts_blocked_by_ceiling']}")
        out.append("")
        out.append("ATTEMPTS (in the order they would be reserved)")
        for a in m["attempts"]:
            flag = "WOULD SEND " if a["would_dispatch"] else "WOULD NOT  "
            if a["slot"] == "fallback":
                flag = "CONDITIONAL"
            out.append(f"  [{flag}] {a['attempt_id']}")
            out.append(f"        {a['slot']:<8} draw {a['draw_index']}  {a['route_key']} on {a['surface']} "
                       f"({a['adapter_family']}, {a['surface_model_id']})")
            p = a["price"]
            out.append(f"        price   {p['unit_price']} {p['unit']} x {p['quantity']} = USD {p['expected_cost_usd']}  "
                       f"pool {p['billing_pool']}   pin {p['price_pin_ref']}")
            r = a["request"]
            out.append(f"        request {r['method']} {r['url']}   body sha256 {(r['body_sha256'] or 'none')[:16]}…  "
                       f"({r['rendered_by']})")
            e = a["evidence"]
            out.append(f"        evidence {e['cells']} {e['status']}   text_mechanism {e['text_mechanism']}")
            ce = a["ceiling"]
            out.append(f"        ceiling reserved_before {ce['reserved_before_this_usd']} + this {ce['this_attempt_usd']} "
                       f"vs {ce['job_ceiling_usd']} -> {'within' if ce['within'] else 'BLOCKED_BY_CEILING'}")
            if a.get("conditional_on"):
                out.append(f"        conditional on a primary trigger: {a['conditional_on']}")
            if a["refusal_reason"]:
                out.append(f"        would not dispatch because: {a['refusal_reason']}")
        if m.get("self_composed"):
            out.append("")
            out.append("COMPOSED BY THE RUNTIME (no provider call)")
            for s in m["self_composed"]:
                out.append(f"  - {s['capability']}: cell {s['cell']} ({s['text_mechanism']}) — {s['note']}")
        sp = m.get("surface_preference") or {}
        out.append("")
        out.append(f"SURFACE PREFERENCE  rule {sp.get('rule')}  applied {sp.get('applied')}: {sp.get('reason')}")
    pv = m["provenance"]
    out.append("")
    out.append(f"PROVENANCE  spec {pv['spec_sha256'][:12]}…  decision {pv['decision_sha256'][:12]}…  "
               f"map {pv['routing_evidence_map_sha256'][:12]}…  register {pv['taint_register_sha256'][:12]}…  "
               f"roster {pv['roster_sha256'][:12]}…")
    out.append(f"            profile adopted {pv['policy_profile_adopted']}  spend_authority {pv['spend_authority_status']}  "
               f"dispatched {pv['dispatched']}  network {pv['network']}")
    if run_result is not None:
        out.append("")
        out.append(f"RUN  status {run_result['status']}   dispatched {run_result.get('dispatched')}   "
                   f"network {run_result.get('network')}")
        for a in run_result.get("attempts") or []:
            out.append(f"  - {a['attempt_id']}: {a['status']}  settled {a['settled_usd']}  reserved {a['reserved_usd']}  "
                       f"artifact {a['artifact_sha256']}")
        if run_result.get("refusal"):
            out.append(f"  refusal: {run_result['refusal']}")
    return "\n".join(out)
