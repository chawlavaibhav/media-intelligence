"""Fixtures from the 23-September evidence (private repo chawlavaibhav/mi-p1-evidence), PARAPHRASED so that no customer
material enters this public repository: the order's structure, every action it asks for, the three photos and the wrong
photo note are kept; the product photos themselves are replaced by blank test images that carry a text note of what the
real photo shows (read only by the simulated vision). When the evidence repository is checked out next to this one (or
MI_P1_EVIDENCE points at it), test_v2_front_of_house also runs the same checks on the verbatim records.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from product.stations.simulated import with_shows
from runtime.loop.synthetic import make_png

# job_20260923_7d36a5b6 — the rejected 30-s Reel (paraphrased)
BACKPACK_FILM_ORDER = (
    "A 30-second Instagram Reel for our Transit Backpack 30L (navy outside, bright yellow lining). Story: a young "
    "professional's hands pack for a two-day work trip — a laptop slides into the padded laptop compartment, a change of "
    "clothes goes into the yellow front bucket pocket, and the bag is zipped shut and lifted, ready to go. Only hands "
    "appear, never a face. It must show the yellow bucket pocket open and the bag being zipped shut. Calm, premium, "
    "satisfying; no dialogue, no voice-over. End on our line and website.")
BACKPACK_PRODUCT = {"name": "Transit Backpack 30L", "brand": "Mokobara", "category": "backpack",
                    "description": "30 L; 48 x 31 x 16 cm; padded laptop compartment for up to a 16-inch laptop; navy body, bright yellow lining."}
# What the three uploaded photos really show (checked against the evidence files), and the customer's note, which is wrong
# about photo 2: photo 2 is the labelled infographic of the open front pocket, photo 3 is the people.
BACKPACK_PHOTOS = [
    ("photo-1.png", "front three-quarter view of the closed navy backpack, product only"),
    ("photo-2.png", "infographic: the front bucket pocket open, bag lying flat, bright yellow lining, with text labels and callouts"),
    ("photo-3.png", "five people wearing and holding the backpack in a studio, for scale; headline text above them"),
]
BACKPACK_NOTE = "Photo 2 (people) is only for scale and feel; photos 1 and 3 show the product."
BACKPACK_EXACT = ["Room for the long way home.", "mokobara.com"]

# The v1 recipe's shots (the rejected film's direction, beats 1–9, actions paraphrased)
V1_FILM_SHOTS = [
    (1, 4, "Both hands guide the laptop straight down in one smooth slide until it is fully seated in the padded compartment."),
    (2, 4, "The hands pull the paired zippers outward along the curved flap edge until both reach their open stops."),
    (3, 3, "The hand guides the released flap downward on its hinge until it lies folded over the front and the yellow bucket is exposed."),
    (4, 4, "Both hands lower the folded clothing bundle into the yellow bucket and press it gently into place."),
    (5, 3, "Both hands raise the flap in one controlled hinge movement until it sits flush over the packed bucket."),
    (6, 3, "The hands draw the paired front zipper pulls inward along the curved edge until they meet at the closed position."),
    (7, 3, "The hands pull the laptop-compartment zippers around the opening until the compartment is fully closed."),
    (8, 3, "The hand lifts the closed backpack vertically until its base clears the tabletop and it hangs by the handle."),
]


def photo_uploads(photos=BACKPACK_PHOTOS, labels=(None, None, None)):
    ups = []
    for i, (name, shows) in enumerate(photos):
        ups.append({"role": "product", "filename": name, "data": with_shows(make_png(64, 64, seed=10 + i), shows),
                    "label": labels[i] if i < len(labels) else None})
    ups.append({"role": "logo", "filename": "logo.png", "data": make_png(32, 16, seed=5)})
    return ups


def submit_backpack_film(env, *, text=BACKPACK_FILM_ORDER, photos=BACKPACK_PHOTOS, note=BACKPACK_NOTE, budget="15", user=None):
    return env.svc.submit(user or env.user, title="backpack reel", media="video", text=text, formats=["9:16"], duration_s=30,
                          exact_strings=BACKPACK_EXACT, product=BACKPACK_PRODUCT, brand_colours=["#101820"], max_budget_usd=budget,
                          allow_preview_spend=True, uploads=photo_uploads(photos), references_note=note)


def v1_recipe(understanding: dict, feasibility: dict) -> dict:
    """The v1 film's recipe re-expressed in the v2 Recipe form: every action shot on the video route (FILM-C), each shot
    generated from its own still — exactly what the 23-September job did."""
    shots = [{"n": n, "duration_s": float(d), "purpose": "packing", "first_frame": "the upright backpack on a table",
              "action": a, "end_state": "the step completed", "camera": "medium close-up", "route": "FILM-C",
              "action_class": "simple_hand_gesture", "starts_from": "master_plate", "feasibility_refs": [],
              "product_present": True, "product_state": "intact", "continuity": ["same two hands"], "must_not": [], "super_id": None,
              "mandatory_ids": []} for n, d, a in V1_FILM_SHOTS]
    shots.append({"n": 9, "duration_s": 3.0, "purpose": "sign-off", "first_frame": "end card", "action": "none", "end_state": "logo and line",
                  "camera": "n/a", "route": "END-CARD", "action_class": "none", "starts_from": "still_only", "feasibility_refs": [],
                  "product_present": False, "product_state": "n/a", "continuity": [], "must_not": [], "super_id": None,
                  "mandatory_ids": [m["id"] for m in understanding.get("mandatory", [])]})
    return {"proposition": "Everything for two days, packed in thirty seconds", "concepts": [{"name": "The pack", "idea": "hands pack the bag",
            "why_it_works": "shows capacity"}], "selected_concept": "The pack", "rationale": "v1", "audience_experience": "satisfying",
            "hook": "a laptop slides in", "remember": "it all fits",
            "visual_language": {"look": "premium", "light": "soft", "palette": ["#101820"], "camera": "macro"},
            "sound": {"music_brief": "calm", "ambience": "room"}, "product_anchor": "the navy backpack with its yellow front bucket",
            "master_plate": {"description": "the backpack upright on an oak table", "product_state": "closed"},
            "character": {"present": True, "description": "two medium-brown hands with off-white cuffs"},
            "copy_deck": [{"id": f"c{i + 1}", "text": s, "role": "line", "source": "customer_exact"} for i, s in enumerate(BACKPACK_EXACT)],
            "composition": {"hero": "", "text_zone": "none", "background": "", "product_treatment": ""},
            "shots": shots, "end_card": {"copy_ids": ["c1", "c2"], "background_hex": "#101820"}, "risks": [],
            "library_used": [], "reuse_shelf_items": [], "customer_summary": "Hands pack the bag."}


def evidence_dir() -> Path | None:
    for p in [os.environ.get("MI_P1_EVIDENCE")] + [str(Path(__file__).resolve().parents[3] / "mi-p1-evidence")]:
        if p and (Path(p) / "db" / "export" / "jobs.jsonl").exists():
            return Path(p)
    return None


def evidence_film(ev: Path) -> dict:
    job = next(json.loads(line) for line in (ev / "db/export/jobs.jsonl").read_text().splitlines()
               if json.loads(line)["id"] == "job_20260923_7d36a5b6")
    brief = json.loads(job["brief_json"])
    ups = [json.loads(line) for line in (ev / "db/export/assets.jsonl").read_text().splitlines()]
    ups = [a for a in ups if a["job_id"] == job["id"] and a["source"] == "customer"]
    return {"brief": brief, "uploads": [(a["role"], ev / "livebeta" / a["path"]) for a in ups]}


def film_to_hold(e, jid, *, accept_alternatives=True):
    """Drive a film order through the front of house, the founder's recipe confirmation, the customer's approval and
    master-plate approval, to the door guard. Returns the final state."""
    e.drain()
    if e.state(jid) == "awaiting_customer_input" and accept_alternatives:
        f = e.store.artifact(jid, "feasibility")
        e.orch.provide_input(jid, by=e.user["email"], accepted_alternatives=[
            {"instead_of": x["for_action"], "use": "the bag shown closed and zipped as a still"} for x in f["alternatives"]])
        e.drain()
    if e.state(jid) == "paused_for_founder" and e.store.artifact(jid, "founder_decision")["decision"] == "confirm recipe":
        e.orch.confirm_recipe(jid, session=e.founder_session(), reason="Read the plan: stills for zips; risky slides first.")
    if e.state(jid) == "awaiting_approval":
        e.orch.approve(jid, by=e.user["email"], budget_usd="15")
        e.drain()
    if e.state(jid) == "awaiting_master_approval":
        e.orch.approve_master(jid, by=e.user["email"])
        e.drain()
    return e.state(jid)


def confirm_and_release(e, jid, note="DRY RUN — simulated media; the founder looked at nothing real"):
    """What the founder does at the door in a dry run: confirm the person-checks, waive what a simulation cannot verify."""
    from product import verify
    s = e.founder_session()
    g = e.store.artifact(jid, "gateway_report")
    for r in g["results"]:
        for b in r["blocking"]:
            if verify.attestable(b["check_id"]):
                e.orch.confirm_check(jid, session=s, asset_id=r["asset_id"], check_id=b["check_id"], note=note)
            else:
                e.orch.waive_check(jid, session=s, asset_id=r["asset_id"], check_id=b["check_id"], reason=note)
    e.orch.release(jid, session=s)
