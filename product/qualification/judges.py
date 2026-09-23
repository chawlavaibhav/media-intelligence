"""Qualification harness for the three judges — recipe checker, small taster, big taster (spec §10).

    python3 -m product.qualification.judges                         # simulated: USD 0, proves the plumbing, qualifies nothing
    python3 -m product.qualification.judges --live --founder-session TOKEN --product-data DIR --budget 2.00
                                                                     # live: ONLY with the founder's own signed-in session

The cases (JUDGE-CASES.yaml) are old jobs whose verdict the founder already gave; nothing new is generated. Each judge
runs through the product's own worker call (its rulebook card, the customer's exact words, its form) and is scored
against the known verdicts with the pass marks in PASS-MARKS.yaml. A simulated run can never qualify a judge, and neither
can a run whose pass marks the founder has not confirmed. A case whose files are not on this host is "unavailable".
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

import yaml

from product import authority, config
from product.orchestrator import Orchestrator
from product.store import Store, utc_now

HERE = Path(__file__).parent


def evidence_root() -> Path | None:
    import os
    for p in [os.environ.get("MI_P1_EVIDENCE"), str(config.REPO.parent / "mi-p1-evidence")]:
        if p and (Path(p) / "db" / "export" / "assets.jsonl").exists():
            return Path(p)
    return None


def _jsonl(root, name):
    return [json.loads(line) for line in (root / "db" / "export" / name).read_text().splitlines() if line.strip()]


class Evidence:
    def __init__(self, root: Path | None):
        self.root = root
        self.assets = {a["id"]: a for a in _jsonl(root, "assets.jsonl")} if root else {}
        self.artifacts = _jsonl(root, "artifacts.jsonl") if root else []
        self.jobs = {j["id"]: j for j in _jsonl(root, "jobs.jsonl")} if root else {}

    def asset(self, aid):
        a = self.assets.get(aid)
        if not a:
            return None
        p = self.root / "livebeta" / a["path"]
        return (a, p) if p.exists() else None

    def artifact(self, job, kind, version):
        rows = [x for x in self.artifacts if x["job_id"] == job and x["kind"] == kind]
        if not rows:
            return None
        row = max(rows, key=lambda x: x["version"]) if version == "latest" else next((x for x in rows if x["version"] == version), None)
        return json.loads(row["data_json"]) if row else None


def recipe_from_v1(direction: dict) -> dict:
    """A v1 direction re-expressed as the v2 Recipe block the recipe checker reads (beats → shots)."""
    shots = []
    for b in direction.get("beats", []):
        card = b.get("first_frame", "").strip().lower() == "end card"
        shots.append({"n": b["n"], "duration_s": b["duration_s"], "action": b.get("action"), "first_frame": b.get("first_frame"),
                      "end_state": b.get("end_state"), "route": "END-CARD" if card else "FILM-C", "starts_from": "master_plate",
                      "product_state": b.get("product_state"), "continuity": b.get("continuity")})
    return {k: direction.get(k) for k in ("proposition", "selected_concept", "product_anchor", "character", "copy_deck", "composition",
                                          "risks")} | {"shots": shots}


def run(*, live=False, founder_session=None, product_data=None, budget="2.00", out=None, judges=("recipe_checker", "small_taster", "big_taster")):
    cases = yaml.safe_load((HERE / "JUDGE-CASES.yaml").read_text())
    marks = yaml.safe_load((HERE / "PASS-MARKS.yaml").read_text())
    authorised_by = None
    if live:
        if not (founder_session and product_data):
            raise SystemExit("a live qualification run needs the founder's signed-in session (--founder-session) and the product's "
                             "data directory (--product-data): only the founder can authorise this spend")
        pstore = Store(Path(product_data) / "mi.sqlite3")
        proof = authority.founder_proof(pstore, founder_session, action="authorise a live judge qualification run")
        authorised_by = proof.actor
    work = Path(out or tempfile.mkdtemp(prefix="mi-judges-"))
    s = config.load(work / "data", reasoning_mode="live" if live else "simulated", provider_mode="simulated")
    st = Store(s.db_path)
    k = Orchestrator(s, st)
    ev = Evidence(evidence_root())
    acct = st.create_account("judge-qualification", ceiling_usd=budget)
    report = {"utc": utc_now(), "live": live, "authorised_by": authorised_by, "pass_marks": marks, "evidence_repo": str(ev.root) if ev.root else None,
              "judges": {}}
    for judge in judges:
        jid = st.create_job(account_id=acct, user_id="qualification", title=f"qualify {judge}", media="video",
                            brief={"text": f"qualification of the {judge}"}, budget_usd=budget)
        st.set_job(jid, budget_authorised_by=authorised_by or "simulated (USD 0)", budget_authorised_at=utc_now())
        rows = [globals()[f"_{judge}"](k, jid, c, ev) for c in cases[judge]]
        report["judges"][judge] = _score(judge, rows, marks, live)
    report["spent_usd"] = str(sum(Decimal(a["settled_usd"] or 0) for a in st.q("SELECT settled_usd FROM attempts")))
    (work / "qualification-report.json").write_text(json.dumps(report, indent=1, default=str))
    report["report_path"] = str(work / "qualification-report.json")
    return report


def _words(ev, job):
    j = ev.jobs.get(job)
    return json.loads(j["brief_json"])["text"] if j else "(the customer's words are not on this host)"


def _recipe_checker(k, jid, c, ev):
    d = ev.artifact(c["evidence"]["job"], c["evidence"]["artifact"], c["evidence"]["version"]) if ev.root else None
    if d is None:
        return {"id": c["id"], "available": False, "known": c["known_verdict"]}
    intent = ev.artifact(c["evidence"]["job"], "intent", "latest") or {}
    ctx = {"UNDERSTANDING": {kk: intent.get(kk) for kk in ("objective", "audience", "mandatory", "deliverable", "product")},
           "FEASIBILITY": {"note": "v1 had no feasibility check; judge the plan against the equipment you know"},
           "RECIPE": recipe_from_v1(d)}
    f = k.workers.call(jid, "recipe_checker", "recipe_check", ctx, exact_words=_words(ev, c["evidence"]["job"]))
    got = "accept" if f["verdict"] == "approve" and f["predicted_acceptance"] != "unlikely" else "reject"
    return {"id": c["id"], "available": True, "known": c["known_verdict"], "got": got, "verdict": f["verdict"],
            "predicted_acceptance": f["predicted_acceptance"], "simulated": f["written_by"]["simulated"]}


def _small_taster(k, jid, c, ev):
    hit = ev.asset(c["evidence"]["asset"]) if ev.root else None
    if not hit:
        return {"id": c["id"], "available": False, "known": c["known"]}
    a, p = hit
    ctype = a["content_type"] or ("video/mp4" if p.suffix == ".mp4" else "image/png")
    meta = json.loads(a["meta_json"])
    ctx = {"INSTRUCTION": {"asset": c["what"], "prompt": meta.get("prompt", "")[:1500]},
           "MEDIA_NOTE": "The last item is the output to inspect."}
    f = k.workers.call(jid, "small_taster", "ingredient_check", ctx, exact_words=_words(ev, a["job_id"]), media=[(ctype, p.read_bytes())])
    got = "good" if f["usable"] and f["product_identity_ok"] != "no" and f["lettering_present"] != "yes" else "bad"
    return {"id": c["id"], "available": True, "known": c["known"], "got": got, "simulated": f["written_by"]["simulated"], "notes": f["notes"][:200]}


def _big_taster(k, jid, c, ev):
    media_items, words = [], None
    if "evidence" in c and ev.root:
        hit = ev.asset(c["evidence"]["asset"])
        if hit:
            a, p = hit
            media_items = [(a["content_type"] or "video/mp4", p.read_bytes())]
            words = _words(ev, a["job_id"])
    elif "agency" in c:
        try:
            from product.qualification.qualify_reviewer import job_dir
            j = job_dir()
            film = j / "gen/final" / ("v1/" if c["agency"]["film"] == "v1" else "") / "mokobara-odyssey-9x16-30s.mp4"
            if film.exists():
                media_items = [("video/mp4", film.read_bytes())]
                words = json.loads((j / "brief.job.json").read_text())["brief"]["text"]
        except SystemExit:
            pass
    if not media_items:
        return {"id": c["id"], "available": False, "known": c["known_verdict"]}
    ctx = {"UNDERSTANDING": {"objective": c["what"]}, "MANDATORY": [], "MEASUREMENTS": [],
           "MEDIA_NOTE": "The attached item is the finished work, exactly as the customer saw it."}
    f = k.workers.call(jid, "big_taster", "final_review", ctx, exact_words=words, media=media_items)
    got = "accept" if f["verdict"] == "pass" else "reject"
    found = []
    if c["id"] == "BT-MOKO7-V1":
        from product.qualification.qualify_reviewer import KEY, propose_matches
        key = yaml.safe_load(KEY.read_text())
        found = [m["id"] for m in propose_matches({"defects": [{**d, "beat": d.get("shot")} for d in f["defects"]]}, key, "v1")
                 if m["target"] and m["proposed_reviewer_defects"]]
    return {"id": c["id"], "available": True, "known": c["known_verdict"], "got": got, "defects_found": found,
            "simulated": f["written_by"]["simulated"]}


def _score(judge, rows, marks, live) -> dict:
    avail = [r for r in rows if r["available"]]
    out = {"cases": rows, "available": len(avail), "unavailable": len(rows) - len(avail)}
    m = marks[judge]
    if judge == "recipe_checker":
        agree = sum(r["got"] == r["known"] for r in avail)
        out["agreement"] = round(agree / len(avail), 3) if avail else None
        passed = out["agreement"] is not None and out["agreement"] >= m["agreement_with_known_outcome_min"]
    elif judge == "small_taster":
        bad = [r for r in avail if r["known"] == "bad"]
        good = [r for r in avail if r["known"] == "good"]
        out["known_bad_caught"] = round(sum(r["got"] == "bad" for r in bad) / len(bad), 3) if bad else None
        out["good_wrongly_rejected"] = round(sum(r["got"] == "bad" for r in good) / len(good), 3) if good else None
        passed = (out["known_bad_caught"] is not None and out["good_wrongly_rejected"] is not None
                  and out["known_bad_caught"] >= m["known_bad_caught_min"] and out["good_wrongly_rejected"] <= m["good_wrongly_rejected_max"])
    else:
        agree = sum(r["got"] == r["known"] for r in avail)
        out["agreement"] = round(agree / len(avail), 3) if avail else None
        moko = next((r for r in avail if r["id"] == "BT-MOKO7-V1"), None)
        out["moko7_v1_target_defects_found"] = len(moko["defects_found"]) if moko else None
        passed = (out["agreement"] is not None and out["agreement"] >= m["agreement_with_customer_verdict_min"]
                  and moko is not None and len(moko["defects_found"]) >= m["moko7_v1_target_defects_found_min"])
    simulated = any(r.get("simulated") for r in avail) or not live
    out["meets_pass_marks"] = bool(passed)
    out["qualified"] = bool(passed) and not simulated and marks.get("status") == "confirmed_by_founder"
    out["why_not_qualified"] = None if out["qualified"] else (
        "simulated run — nobody judged anything" if simulated else
        "pass marks not yet confirmed by the founder" if marks.get("status") != "confirmed_by_founder" else "below the pass marks")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--founder-session")
    ap.add_argument("--product-data")
    ap.add_argument("--budget", default="2.00")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    rep = run(live=a.live, founder_session=a.founder_session, product_data=a.product_data, budget=a.budget, out=a.out)
    print(json.dumps({j: {kk: v for kk, v in r.items() if kk != "cases"} for j, r in rep["judges"].items()}, indent=1))
    print("report:", rep["report_path"], "spent USD", rep["spent_usd"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
