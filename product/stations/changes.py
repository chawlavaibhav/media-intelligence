"""Customer changes (spec §6.2 last row, §4.9): the waiter writes a Change request form for each request, and only the
affected station redoes work — usually the head cook. A change to the idea goes back to the chef and is re-quoted."""
from __future__ import annotations

import json
import re

from product import flow
from product.stations.head_cook import _reset_downstream


def request(k, job_id, by: str, items: list):
    """items: [{"target": "shot:3" | "copy:c1" | "music" | "master" | None, "text": "..."}]"""
    finals = k.final_assets(job_id)
    for it in items:
        k.store.add_feedback(job_id, asset_id=finals[0] if finals else None, target=it.get("target"), text=it["text"], kind="revision", by_user=by)
    k._end_wait(job_id, "review")
    k.store.transition(job_id, "ready_for_review", "revising", actor=by, data={"items": len(items)})


def revise(k, job_id: str):
    from product.stations import waiter
    pending = [f for f in k.store.feedback(job_id) if f["kind"] == "revision" and not f["resolved_in_cut"]]
    recipe = k.store.artifact(job_id, "recipe")
    cut = 1 + len(k.store.events(job_id, ("cut_ready",)))
    forms = []
    with k.store.timed(job_id, "repair", "change request"):
        for f in pending:
            flow.send_back(k.store, job_id, "SB-CUSTOMER-CHANGE", key=str(f["id"]), actor="customer", why=f["text"][:300])
            forms.append((f, waiter.change_request(k, job_id, {"target": f["target"], "text": f["text"]})))
    if any(cr["class"] == "concept_change" for _, cr in forms):
        k.store.put_artifact(job_id, "plan_change", {"request": [f["text"] for f, _ in forms], "by": "customer"}, "waiter")
        _resolve(k, pending, cut)
        k.store.transition(job_id, "revising", "directing", actor="waiter", data={"reason": "concept change → the chef, and a new quote"})
        return
    reset = []
    new = json.loads(json.dumps(recipe))
    overrides = dict(k.store.artifact(job_id, "copy_overrides") or {})
    for _, cr in forms:
        for cc in cr.get("copy_changes", []):
            for c in new["copy_deck"]:
                if c["id"] == cc["id"]:
                    for orig in k.brief(job_id).get("exact_strings", []):
                        if overrides.get(orig, orig) == c["text"]:
                            overrides[orig] = cc["text"]
                    c["text"], c["source"] = cc["text"], "customer_exact"
                    reset += _copy_nodes(k, job_id, c["id"])
        for t in cr.get("targets", []):
            kind, ref = t["kind"], str(t["ref"])
            if kind == "copy":
                reset += _copy_nodes(k, job_id, ref)
            elif kind == "music":
                reset += _reset_downstream(k, job_id, "music", t["change"])
            elif kind in ("shot", "first_frame"):
                n = re.sub(r"\D", "", ref)
                node = (f"frame_{n}" if kind == "first_frame" else f"shot_{n}")
                if k.store.node(job_id, node):
                    reset += _reset_downstream(k, job_id, node, t["change"])
                else:
                    reset += _plates(k, job_id, t["change"])
            elif kind == "master_plate":
                reset += _reset_downstream(k, job_id, "master" if k.store.node(job_id, "master") else _first_plate(k, job_id), t["change"])
            elif kind in ("edit", "composition"):
                for nd in k.store.nodes(job_id):
                    if nd["kind"] in ("assemble", "compose_still"):
                        reset += _reset_downstream(k, job_id, nd["node_id"], t["change"])
                if kind == "composition" and k.store.job(job_id)["media"] == "image":
                    reset += _plates(k, job_id, t["change"])
    if new != recipe:
        k.put_form(job_id, "recipe", new)
    if overrides:
        k.store.put_artifact(job_id, "copy_overrides", overrides, "customer")
    k.store.put_artifact(job_id, "revision_plan", {"cut": cut, "forms": [cr for _, cr in forms], "reset_nodes": sorted(set(reset))}, "waiter")
    _resolve(k, pending, cut)
    if not reset:
        from product.orchestrator import NodeFailed
        raise NodeFailed("the change request could not be mapped to any part of the production; the founder will look at it")
    k.store.transition(job_id, "revising", "producing", actor="waiter", data={"reset": sorted(set(reset)), "cut": cut})


def _plates(k, job_id, note):
    out = []
    for n in k.store.nodes(job_id):
        if n["kind"] == "plate":
            out += _reset_downstream(k, job_id, n["node_id"], note)
    return out


def _first_plate(k, job_id):
    return next(n["node_id"] for n in k.store.nodes(job_id) if n["kind"] == "plate")


def _copy_nodes(k, job_id, copy_id) -> list:
    out = []
    for n in k.store.nodes(job_id):
        spec = json.loads(n["spec_json"])
        if n["kind"] in ("compose_still", "end_card") or (n["kind"] == "super" and spec.get("copy_id") == copy_id):
            out += _reset_downstream(k, job_id, n["node_id"], f"copy {copy_id} changed")
    return out


def _resolve(k, pending, cut):
    with k.store.tx() as c:
        for f in pending:
            c.execute("UPDATE feedback SET resolved_in_cut=? WHERE id=?", (cut, f["id"]))
