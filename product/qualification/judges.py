"""Qualification harness for the three judges — recipe checker, small taster, big taster (spec §10).

    python3 -m product.qualification.judges                         # simulated: USD 0, proves the plumbing, qualifies nothing
    python3 -m product.qualification.judges --live --founder-session TOKEN --product-data DIR --budget 2.00
                                                                     # live: ONLY with the founder's own signed-in session
    python3 -m product.qualification.judges --trial --estimate       # model trial: estimated cost per candidate model, USD 0
    python3 -m product.qualification.judges --trial --max-usd 10 --approved-by "founder in chat, 2026-09-23"
                                                                     # model trial: real calls, hard cap; compares models, qualifies nothing

The cases (JUDGE-CASES.yaml) are old jobs whose verdict the founder already gave; nothing new is generated. Each judge
runs through the product's own worker call (its rulebook card, the customer's exact words, its form) and is scored
against the known verdicts with the pass marks in PASS-MARKS.yaml. A simulated run can never qualify a judge, and neither
can a run whose pass marks the founder has not confirmed. A case whose files are not on this host is "unavailable".

Amendment 1 §2: the big taster is also tested on the old jobs the founder already judged (historical/CASES.yaml in the
evidence repo: 14 films, 62 images) — a file is used only if its SHA-256 matches the case record — and the recipe checker
on the old jobs whose plan is on the job's branch in this repository (read with `git show`). Agreement is reported
SEPARATELY for accepted and not-accepted cases (and their mean), and the pass marks apply to each group.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
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


CONTENT_TYPES = {".mp4": "video/mp4", ".mov": "video/quicktime", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".webp": "image/webp"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_file(branch: str, path: str) -> str | None:
    """A file from an old job's branch in this repository (origin/<branch>, or a local <branch>); None if not on this host."""
    for ref in (f"origin/{branch}", branch):
        try:
            out = subprocess.run(["git", "-C", str(config.REPO), "show", f"{ref}:{path}"], capture_output=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if out.returncode == 0:
            return out.stdout.decode("utf-8", "replace")
    return None


def _jsonl(root, name):
    return [json.loads(line) for line in (root / "db" / "export" / name).read_text().splitlines() if line.strip()]


class Evidence:
    def __init__(self, root: Path | None):
        self.root = root
        self.assets = {a["id"]: a for a in _jsonl(root, "assets.jsonl")} if root else {}
        self.artifacts = _jsonl(root, "artifacts.jsonl") if root else []
        self.jobs = {j["id"]: j for j in _jsonl(root, "jobs.jsonl")} if root else {}

    def historical(self, ev: dict):
        """(path, content type) for a historical case file, only when it is on this host AND its SHA-256 matches."""
        if not self.root:
            return None
        p = self.root / ev["historical"]
        if not p.exists() or sha256_file(p) != ev["sha256"]:
            return None
        return p, CONTENT_TYPES.get(p.suffix.lower(), "application/octet-stream")

    def asset(self, aid):
        a = self.assets.get(aid)
        if not a:
            return None
        p = self.root / "livebeta" / a["path"]
        return (a, p) if p.exists() else None

    def product_photos(self, job, limit=3) -> list:
        """The customer's own product photos for a P1 job (what the waiter and the recipe checker see)."""
        out = []
        for a in self.assets.values():
            if a["job_id"] == job and a.get("role") == "product" and a.get("source") == "customer":
                p = self.root / "livebeta" / a["path"]
                if p.exists():
                    out.append((a["content_type"] or "image/jpeg", p.read_bytes()))
        return out[:limit]

    def artifact(self, job, kind, version):
        rows = [x for x in self.artifacts if x["job_id"] == job and x["kind"] == kind]
        if not rows:
            return None
        row = max(rows, key=lambda x: x["version"]) if version == "latest" else next((x for x in rows if x["version"] == version), None)
        return json.loads(row["data_json"]) if row else None


# Old jobs: the customer's order, the waiter's sheet of the time (01-INTENT / normalized request) and product photos, so a
# judge of an old job gets the same inputs a v2 judge gets (founder 2026-09-24).
OLD_JOBS = {
    "MOKOBARA-ODYSSEY-007": {"branch": "work/agency-job-mokobara-odyssey-001", "job": "agency/jobs/AGY-2026-09-21-MOKOBARA-ODYSSEY-001",
                             "brief": "brief.job.json", "sheet": "stages/01-INTENT.md",
                             "photos": ["source/mokobara/The_Transit_Backpack_30L_Private_Island_1.jpg",
                                        "source/mokobara/The_Transit_Backpack_30L_Private_Island_2.jpg",
                                        "source/mokobara/The_Transit_Backpack_30L_Private_Island_5.jpg"]},
    "RENTOK-GAME-A-004": {"branch": "work/agency-job-rentok-game-lane-a-001", "job": "agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-A-001",
                          "brief": "brief.job.json", "sheet": "stages/01-INTENT.md", "photos": []},
    "RENTOK-GAME-B-005": {"branch": "work/agency-job-rentok-game-lane-b-001", "job": "agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-B-001",
                          "brief": "brief.job.json", "sheet": "stages/01-INTENT.md", "photos": []},
    "RENTOK-GAME-V2-006": {"branch": "work/agency-job-rentok-game-v2-001", "job": "agency/jobs/AGY-2026-09-21-RENTOK-GAME-V2-001",
                           "brief": "brief.job.json", "sheet": "stages/01-INTENT.md", "photos": []},
    "CUMINCO-CHOPSTICKS-003": {"branch": "work/agency-job-cuminco-chopsticks-001", "job": "agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001",
                               "brief": "brief.job.json", "sheet": None,
                               "photos": ["source/images/Slide_01.jpg", "source/images/Single_Green.jpg", "source/images/Set_of_2_Rose.jpg"]},
    "UPWORK-INTRO-001": {"branch": "work/pilot-upwork-intro-video-v4", "job": "pilots/upwork-intro-video-2026-09-14",
                         "brief": "preprod/COMMERCIAL-BRIEF.md", "sheet": "v4/plan/NORMALIZED-REQUEST-V4.yaml", "photos": []},
}


def git_bytes(branch: str, path: str) -> bytes | None:
    import subprocess
    r = subprocess.run(["git", "show", f"origin/{branch}:{path}"], cwd=config.REPO, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def old_job_inputs(case: str) -> dict:
    """{'words', 'sheet', 'photos'} for an old job, from its own branch; missing parts are said to be missing."""
    j = OLD_JOBS.get(case)
    if not j:
        return {"words": "(no order on record for this job)", "sheet": None, "photos": []}
    raw = git_file(j["branch"], f"{j['job']}/{j['brief']}")
    words = "(no order on record for this job)"
    if raw:
        try:
            b = json.loads(raw)
            words = (b.get("brief") or {}).get("text") or json.dumps(b.get("brief") or b, ensure_ascii=False)[:6000]
            extra = {k: b[k] for k in ("exact_text_strings", "deliverable_request") if k in b}
            if extra:
                words += "\n\nORDER DETAILS: " + json.dumps(extra, ensure_ascii=False)[:3000]
        except ValueError:
            words = raw[:6000]
    sheet = git_file(j["branch"], f"{j['job']}/{j['sheet']}") if j.get("sheet") else None
    photos = []
    for ph in j.get("photos", []):
        b = git_bytes(j["branch"], f"{j['job']}/{ph}")
        if b:
            photos.append(("image/jpeg" if ph.lower().endswith((".jpg", ".jpeg")) else "image/png", b))
    return {"words": words, "sheet": sheet[:12000] if sheet else None, "photos": photos}


def recipe_from_v1(direction: dict) -> dict:
    """A v1 direction re-expressed as the v2 Recipe block the recipe checker reads (beats → shots)."""
    shots = []
    for b in direction.get("beats", []):
        card = b.get("first_frame", "").strip().lower() == "end card"
        shots.append({"n": b["n"], "duration_s": b["duration_s"], "action": b.get("action"), "first_frame": b.get("first_frame"),
                      "end_state": b.get("end_state"), "route": "END-CARD" if card else "FILM-C", "starts_from": "master_plate",
                      "product_state": b.get("product_state"), "continuity": b.get("continuity")})
    if not shots:  # a still-image plan has no beats: the whole direction is the recipe, not an empty shot list
        return dict(direction) | {"deliverable_kind": "still image (no shots; the plan is the concept, composition and copy)"}
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
    report["recipe_checker_missing"] = cases.get("recipe_checker_missing", [])
    report["spent_usd"] = str(sum(Decimal(a["settled_usd"] or 0) for a in st.q("SELECT settled_usd FROM attempts")))
    (work / "qualification-report.json").write_text(json.dumps(report, indent=1, default=str))
    report["report_path"] = str(work / "qualification-report.json")
    return report


# ── model trial (founder 2026-09-23: the kitchen is independent of the models; try several, cheap, open and strong) ──
# Each judge runs the same known-verdict cases on each candidate model. A trial compares models; it never qualifies a
# judge and never changes the product's configuration. Models are "provider:model" (azure_openai:<deployment name> works
# for any model deployed on the Azure resource, including open models such as DeepSeek, Llama or Kimi if deployed there).
TRIAL_MODELS = {
    "recipe_checker": ["azure_openai:gpt-5.6-terra", "azure_openai:gpt-5.6-sol", "azure_openai:DeepSeek-V3.1",
                       "azure_openai:Kimi-K2-Instruct", "gemini:gemini-3.1-pro-preview"],
    "small_taster": ["azure_openai:gpt-5.6-terra", "azure_openai:Llama-4-Maverick-17B-128E-Instruct-FP8", "anthropic:claude-haiku-4-5",
                     "gemini:gemini-3.5-flash"],
    "big_taster": ["azure_openai:gpt-5.6-terra", "azure_openai:gpt-5.6-sol", "azure_openai:Llama-4-Maverick-17B-128E-Instruct-FP8",
                   "gemini:gemini-3.1-pro-preview"],
}
KEYS = {"azure_openai": ("AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"), "anthropic": ("ANTHROPIC_API_KEY",),
        "gemini": ("GOOGLE_API_KEY",)}


def _usable(spec: str) -> str | None:
    """Why this model cannot be called on this host (a missing key), or None."""
    import os
    need = KEYS.get(spec.split(":", 1)[0], ())
    missing = [kk for kk in need if not os.environ.get(kk)]
    if spec.startswith("gemini:") and os.environ.get("GEMINI_API_KEY"):
        missing = []
    return f"missing {', '.join(missing)}" if missing else None


def trial(*, models: dict | None = None, max_usd="10.00", estimate_only=False, approved_by=None, out=None,
          judges=("recipe_checker", "small_taster", "big_taster")) -> dict:
    """Run each judge's cases on each candidate model (or, with estimate_only, price it at USD 0). A hard cap: the run
    stops before the case that would take the total past max_usd."""
    from product.reasoning import _price
    models = models or TRIAL_MODELS
    cases = yaml.safe_load((HERE / "JUDGE-CASES.yaml").read_text())
    marks = yaml.safe_load((HERE / "PASS-MARKS.yaml").read_text())
    if not estimate_only and not approved_by:
        raise SystemExit("a paid model trial needs --approved-by (who approved the spend, and when) and --max-usd")
    work = Path(out or tempfile.mkdtemp(prefix="mi-trial-"))
    ev = Evidence(evidence_root())
    cap, report = Decimal(str(max_usd)), {"utc": utc_now(), "estimate_only": estimate_only, "approved_by": approved_by,
                                           "max_usd": str(max_usd), "evidence_repo": str(ev.root) if ev.root else None, "judges": {}}
    spent = Decimal(0)
    for judge in judges:
        report["judges"][judge] = {}
        for spec in models.get(judge, []):
            why = None if estimate_only else _usable(spec)
            row = {"model": spec, "price_per_mtok": [str(x) for x in _price(spec.split(":", 1)[1])]}
            if why:
                report["judges"][judge][spec] = {**row, "skipped": why}
                continue
            s = config.load(work / judge / spec.replace(":", "_").replace("/", "_"),
                            reasoning_mode="simulated" if estimate_only else "live", provider_mode="simulated")
            s.models = {**s.models, judge: spec}
            st = Store(s.db_path)
            k = Orchestrator(s, st)
            acct = st.create_account("model-trial", ceiling_usd=str(cap))
            jid = st.create_job(account_id=acct, user_id="trial", title=f"trial {judge} {spec}", media="video",
                                brief={"text": f"model trial of the {judge}"}, budget_usd=str(cap - spent))
            st.set_job(jid, budget_authorised_by=approved_by or "estimate (USD 0)", budget_authorised_at=utc_now())
            rows, est = [], Decimal(0)
            for c in cases[judge]:
                done = sum(Decimal(a["settled_usd"] or 0) for a in st.q("SELECT settled_usd FROM attempts"))
                if not estimate_only and spent + done >= cap:
                    rows.append({"id": c["id"], "available": False, "known": c.get("known") or c.get("known_verdict"), "why": "spend cap reached"})
                    continue
                try:
                    rows.append(globals()[f"_{judge}"](k, jid, c, ev))
                except Exception as e:  # noqa: BLE001 — one model failing on one case is a result, not a crash
                    rows.append({"id": c["id"], "available": False, "known": c.get("known") or c.get("known_verdict"),
                                 "why": f"call failed: {str(config.scrub(str(e)))[:200]}"})
            est = sum((Decimal(r["est_cost_usd"] or 0) for r in st.llm_calls(jid)), Decimal(0))
            paid = sum((Decimal(a["settled_usd"] or 0) for a in st.q("SELECT settled_usd FROM attempts")), Decimal(0))
            spent += paid
            scored = _score(judge, rows, marks, live=not estimate_only)
            scored.pop("cases", None) if estimate_only else None
            report["judges"][judge][spec] = {**row, "estimated_usd": str(est.quantize(Decimal("0.0001"))),
                                            "spent_usd": str(paid.quantize(Decimal("0.0001"))), **scored,
                                            "qualified": False, "why_not_qualified": "a model trial never qualifies a judge"}
    report["spent_usd"] = str(spent.quantize(Decimal("0.000001")))
    (work / "model-trial-report.json").write_text(json.dumps(report, indent=1, default=str))
    report["report_path"] = str(work / "model-trial-report.json")
    return report


def _words(ev, job):
    j = ev.jobs.get(job)
    return json.loads(j["brief_json"])["text"] if j else "(the customer's words are not on this host)"


def _recipe_checker(k, jid, c, ev):
    if "branch" in c:
        return _recipe_checker_historical(k, jid, c)
    d = ev.artifact(c["evidence"]["job"], c["evidence"]["artifact"], c["evidence"]["version"]) if ev.root else None
    if d is None:
        return {"id": c["id"], "available": False, "known": c["known_verdict"]}
    intent = ev.artifact(c["evidence"]["job"], "intent", "latest") or {}
    ctx = {"UNDERSTANDING": {kk: intent.get(kk) for kk in ("objective", "audience", "mandatory", "deliverable", "product")},
           "FEASIBILITY": {"note": "v1 had no feasibility check; judge the plan against the equipment you know"},
           "RECIPE": recipe_from_v1(d)}
    f = k.workers.call(jid, "recipe_checker", "recipe_check", ctx, exact_words=_words(ev, c["evidence"]["job"]),
                       media=ev.product_photos(c["evidence"]["job"]))
    got = "accept" if f["verdict"] == "approve" and f["predicted_acceptance"] != "unlikely" else "reject"
    return {"id": c["id"], "available": True, "known": c["known_verdict"], "got": got, "verdict": f["verdict"],
            "predicted_acceptance": f["predicted_acceptance"], "simulated": f["written_by"]["simulated"]}


def _recipe_checker_historical(k, jid, c):
    plan = git_file(c["branch"], c["plan"])
    structure = git_file(c["branch"], c["plan"].rsplit("/", 1)[0] + "/02-STRUCTURE.md") if c["plan"].endswith("03-CREATIVE.md") else None
    if plan is None:
        return {"id": c["id"], "available": False, "known": c["known_verdict"], "why": f"{c['branch']} is not on this host"}
    inp = old_job_inputs(c["case"]) if c.get("case") else {"words": "(no order on record)", "sheet": None, "photos": []}
    ctx = {"UNDERSTANDING": {"waiters_sheet": inp["sheet"] or "(this old job kept no separate sheet; its order above is complete)"},
           "FEASIBILITY": {"note": "old jobs had no feasibility check; judge the plan against the equipment you know"},
           "RECIPE": {"structure_document": structure, "plan_document": plan, "source": f"{c['branch']}:{c['plan']}"}}
    f = k.workers.call(jid, "recipe_checker", "recipe_check", ctx, exact_words=inp["words"], media=inp["photos"])
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
    known = c.get("known_judge_verdict") or {"accept": "pass", "reject": "fail"}[c["known_verdict"]]
    if "historical" in c.get("evidence", {}):
        hit = ev.historical(c["evidence"])
        if not hit:
            return {"id": c["id"], "available": False, "known": known, "why": "file not on this host or its SHA-256 does not match"}
        p, ctype = hit
        media_items = [(ctype, p.read_bytes())]
    elif "evidence" in c and ev.root:
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
        return {"id": c["id"], "available": False, "known": known}
    sent_type = media_items[0][0]
    if sent_type.startswith("video/") and not k.s.models.get("big_taster", "").startswith("gemini"):
        # only Gemini takes video with sound; every other model gets the same contact sheet of still frames
        from product import media as media_mod
        tmp = Path(tempfile.mkdtemp(prefix="mi-sheet-"))
        (tmp / "film.mp4").write_bytes(media_items[0][1])
        try:
            media_items = [("image/png", media_mod.contact_sheet(tmp / "film.mp4", tmp / "contact.png").read_bytes())]
        except media_mod.MediaError:
            return {"id": c["id"], "available": False, "known": known, "why": "could not make a contact sheet"}
    understanding = {"what": c.get("what") or f"{c.get('case')} version {c.get('version')} ({c.get('media')})"}
    if c.get("case"):
        inp = old_job_inputs(c["case"])
        words = inp["words"]
        understanding["waiters_sheet"] = inp["sheet"] or "(this old job kept no separate sheet; its order is complete)"
    elif "evidence" in c and ev.root and c["evidence"].get("asset"):
        a = ev.assets.get(c["evidence"]["asset"])
        intent = ev.artifact(a["job_id"], "intent", "latest") if a else None
        if intent:
            understanding["waiters_sheet"] = {kk: intent.get(kk) for kk in ("objective", "audience", "mandatory", "forbidden", "deliverable", "product")}
    ctx = {"UNDERSTANDING": understanding, "MANDATORY": [], "MEASUREMENTS": [],
           "MEDIA_NOTE": "The attached item is the finished work, exactly as the customer saw it."}
    f = k.workers.call(jid, "big_taster", "final_review", ctx, exact_words=words or "(the customer's words are not on this host)",
                       media=media_items)
    got = f["verdict"]
    found = []
    if c["id"] == MOKO7_V1:
        from product.qualification.qualify_reviewer import KEY, propose_matches
        key = yaml.safe_load(KEY.read_text())
        found = [m["id"] for m in propose_matches({"defects": [{**d, "beat": d.get("shot")} for d in f["defects"]]}, key, "v1")
                 if m["target"] and m["proposed_reviewer_defects"]]
    saw = ("video with sound" if media_items[0][0].startswith("video/") else
           "still frames, no sound" if sent_type.startswith("video/") else "image")
    return {"id": c["id"], "available": True, "known": known, "got": got, "defects_found": found, "media": c.get("media"),
            "saw": saw, "had_order": not str(words or "").startswith("("), "simulated": f["written_by"]["simulated"]}


MOKO7_V1 = "BT-H-MOKOBARA-ODYSSEY-007-1"


def _split_agreement(avail, accepted_value, agrees) -> dict:
    """Agreement on accepted and on not-accepted cases, separately, and their mean (amendment 1 §2)."""
    acc = [r for r in avail if r["known"] == accepted_value]
    rest = [r for r in avail if r["known"] != accepted_value]
    a = round(sum(agrees(r) for r in acc) / len(acc), 3) if acc else None
    n = round(sum(agrees(r) for r in rest) / len(rest), 3) if rest else None
    return {"accepted_cases": len(acc), "not_accepted_cases": len(rest), "agreement_accepted": a, "agreement_not_accepted": n,
            "agreement_balanced": round((a + n) / 2, 3) if a is not None and n is not None else None,
            "agreement": round(sum(agrees(r) for r in avail) / len(avail), 3) if avail else None}


def _score(judge, rows, marks, live) -> dict:
    avail = [r for r in rows if r["available"]]
    out = {"cases": rows, "available": len(avail), "unavailable": len(rows) - len(avail)}
    m = marks[judge]
    if judge == "recipe_checker":
        out.update(_split_agreement(avail, "accept", lambda r: r["got"] == r["known"]))
        mk = m["agreement_with_known_outcome_min"]
        passed = out["agreement_accepted"] is not None and out["agreement_not_accepted"] is not None \
            and out["agreement_accepted"] >= mk and out["agreement_not_accepted"] >= mk
    elif judge == "small_taster":
        bad = [r for r in avail if r["known"] == "bad"]
        good = [r for r in avail if r["known"] == "good"]
        out["known_bad_caught"] = round(sum(r["got"] == "bad" for r in bad) / len(bad), 3) if bad else None
        out["good_wrongly_rejected"] = round(sum(r["got"] == "bad" for r in good) / len(good), 3) if good else None
        passed = (out["known_bad_caught"] is not None and out["good_wrongly_rejected"] is not None
                  and out["known_bad_caught"] >= m["known_bad_caught_min"] and out["good_wrongly_rejected"] <= m["good_wrongly_rejected_max"])
    else:
        # accepted ↔ the judge says pass; not accepted ↔ the judge says fix or fail (exact fix/fail agreement reported too)
        out.update(_split_agreement(avail, "pass", lambda r: (r["got"] == "pass") == (r["known"] == "pass")))
        out["exact_verdict_agreement"] = round(sum(r["got"] == r["known"] for r in avail) / len(avail), 3) if avail else None
        out["by_media"] = {m_: _split_agreement([r for r in avail if r.get("media") == m_], "pass",
                                                lambda r: (r["got"] == "pass") == (r["known"] == "pass")) for m_ in ("film", "image")}
        moko = next((r for r in avail if r["id"] == MOKO7_V1), None)
        out["moko7_v1_target_defects_found"] = len(moko["defects_found"]) if moko else None
        mk = m["agreement_with_customer_verdict_min"]
        passed = (out["agreement_accepted"] is not None and out["agreement_not_accepted"] is not None
                  and out["agreement_accepted"] >= mk and out["agreement_not_accepted"] >= mk
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
    ap.add_argument("--trial", action="store_true")
    ap.add_argument("--estimate", action="store_true")
    ap.add_argument("--max-usd", default="10.00")
    ap.add_argument("--approved-by")
    a = ap.parse_args(argv)
    if a.trial:
        rep = trial(max_usd=a.max_usd, estimate_only=a.estimate, approved_by=a.approved_by, out=a.out)
        for j, per in rep["judges"].items():
            for spec, r in per.items():
                print(f"{j:15s} {spec:55s} " + (f"skipped: {r['skipped']}" if r.get("skipped") else
                      f"est USD {r['estimated_usd']:>8s} spent USD {r['spent_usd']:>8s} "
                      f"accepted {r.get('agreement_accepted')} not-accepted {r.get('agreement_not_accepted')}"))
        print("report:", rep["report_path"], "spent USD", rep["spent_usd"])
        return 0
    rep = run(live=a.live, founder_session=a.founder_session, product_data=a.product_data, budget=a.budget, out=a.out)
    print(json.dumps({j: {kk: v for kk, v in r.items() if kk != "cases"} for j, r in rep["judges"].items()}, indent=1))
    print("report:", rep["report_path"], "spent USD", rep["spent_usd"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
