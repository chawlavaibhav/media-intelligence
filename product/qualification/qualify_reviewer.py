"""Qualify the independent reviewer on real historical media (Controller concern 3 on PR #108).

    python3 -m product.qualification.qualify_reviewer --film v1|v2 [--live] [--budget 1.00]

Runs the PRODUCT's reviewer role (product.reasoning.Reasoner, isolated context, ledger reservation, same model and
review copy as production) on a Mokobara film, then proposes a match between the reviewer's defects and the key.
Without --live the reasoning backend is simulated (USD 0; proves the plumbing, qualifies nothing). A proposed
match is not a verdict: the sheet is written for a person to confirm each row.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

import yaml

from product import config, media, verify
from product.reasoning import Reasoner
from product.store import Store, utc_now as config_utc

HERE = Path(__file__).parent
KEY = HERE / "MOKOBARA-V1-V2-KEY.yaml"
REL = "media-intelligence-mokobara/agency/jobs/AGY-2026-09-21-MOKOBARA-ODYSSEY-001"
CUTS = {"v1": [1.54, 3.5, 7.5, 12.5, 20.5, 24.5], "v2": [1.5, 3.5, 7.5, 13.0, 21.0, 24.21]}


def job_dir() -> Path:
    for base in [Path(os.environ.get("MI_HISTORICAL_MOKOBARA_JOB", "/nonexistent"))] + \
                [b / REL for b in (config.REPO.parent, config.REPO.parent.parent)]:
        if (base / "board.json").exists():
            return base
    raise SystemExit("the Mokobara job folder is not on this host (set MI_HISTORICAL_MOKOBARA_JOB)")


def context(j: Path, film: Path, which: str) -> dict:
    brief = json.loads((j / "brief.job.json").read_text())
    board = json.loads((j / "board.json").read_text())
    deck = json.loads((j / "copy-deck.json").read_text())
    det = verify.film_checks(film, cuts=CUTS[which][:-1] + [CUTS[which][-1]], source_sizes=[[720, 1280]], delivered=(1080, 1920),
                             planned_s=30.0, card_in_s=26.0)
    return {
        "BRIEF": {"text": brief["brief"]["text"], "exact_strings": brief.get("exact_text_strings"), "product": "Mokobara Transit Backpack 30L"},
        "INTENT": {"objective": "a 30 s cinematic brand film: a castaway's Odyssey-shaped story told through the Mokobara bag",
                   "audience": "Indian D2C travel-bag buyers on phone feeds", "audience_response": "delight and brand recall",
                   "mandatory": [{"id": f"B{b['n']}", "what": b.get("impact") or b.get("title"), "observable_as": b.get("framing")}
                                 for b in board["beats"]],
                   "forbidden": ["speech or singing", "model-drawn lettering or logos", "copyrighted film references"]},
        "DIRECTION": {"identity_anchors": board["identity_anchors"], "beats": board["beats"], "copy_deck": deck["strings"]},
        "DETERMINISTIC_CHECKS": [{"check": r["check_id"], "status": r["status"], "detail": r["detail"]} for r in det],
        "MEDIA_NOTE": "The attached MP4 is the complete assembled film with its sound (720p review copy). Timecodes refer to it.",
    }


def propose_matches(review: dict, key: dict, which: str) -> list:
    out = []
    found = review.get("defects", [])
    for k in key["defects"]:
        hits = []
        for i, d in enumerate(found):
            text = (d.get("description", "") + " " + d.get("where", "") + " " + d.get("id", "")).lower()
            if sum(str(w).lower() in text for w in k["words"]) >= 2:
                hits.append(i)
        out.append({"id": k["id"], "truth_on_this_file": k[which], "target": k["id"] in key["target_on_v1"],
                    "proposed_reviewer_defects": hits, "confirmed_by_person": None})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--film", choices=("v1", "v2"), required=True)
    ap.add_argument("--live", action="store_true", help="call the configured reviewer model (spends; needs an authorised budget)")
    ap.add_argument("--budget", default="1.00")
    ap.add_argument("--model", default=None, help="reviewer model to qualify (default: the configured MI_REVIEWER_MODEL)")
    ap.add_argument("--fps", type=float, default=None, help="frames per second the reviewer samples")
    ap.add_argument("--out", default=None)
    ap.add_argument("--reuse", action="store_true", help="rebuild the report from the reviewer call already stored in --out (no spend)")
    a = ap.parse_args(argv)
    j = job_dir()
    film = j / "gen/final" / ("v1/" if a.film == "v1" else "") / "mokobara-odyssey-9x16-30s.mp4"
    work = Path(a.out or tempfile.mkdtemp(prefix=f"mi-qualify-{a.film}-"))
    work.mkdir(parents=True, exist_ok=True)
    over = {"reasoning_mode": "live" if a.live else "simulated"}
    if a.model:
        over["reviewer_model"] = a.model
    if a.fps:
        over["review_fps"] = a.fps
    s = config.load(work / "data", **over)
    st = Store(s.db_path)
    if a.reuse:
        call = st.q1("SELECT * FROM llm_calls WHERE role='reviewer' AND status='ok' ORDER BY id DESC LIMIT 1")
        if call is None:
            raise SystemExit("no stored reviewer call to reuse in " + str(work))
        review = json.loads(call["output_json"]); jid = call["job_id"]
        review["_call"] = {"isolated": bool(call["isolated"]), "model": call["model"], "provider": call["provider"]}
        return _report(a, film, work, st, jid, review)
    acct = st.create_account("reviewer-qualification", ceiling_usd=a.budget)
    jid = st.create_job(account_id=acct, user_id="qualification", title=f"reviewer qualification {a.film}", media="video",
                        brief={"text": "reviewer qualification on MOKOBARA-ODYSSEY-007 " + a.film}, budget_usd=a.budget)
    st.set_job(jid, budget_authorised_by="founder (reviewer-qualification spend record)", budget_authorised_at=config_utc())
    small = work / f"{a.film}-review.mp4"
    media.reencode_small(film, small)
    review = Reasoner(s, st).call(jid, "reviewer", context(j, film, a.film), media=[("video/mp4", small.read_bytes())], max_tokens=16000)
    return _report(a, film, work, st, jid, review)


def _report(a, film, work, st, jid, review):
    key = yaml.safe_load(KEY.read_text())
    matches = propose_matches(review, key, a.film)
    rows = verify.review_rows(review, mandatory_ids=[], media_kind="video")
    report = {"model": (review.get("_call") or {}).get("model"), "fps": a.fps, "film": a.film, "sha256": media.sha256_file(film), "live": a.live, "review": review, "proposed_matches": matches,
              "review_rows": rows, "ledger": st.ledger_summary(jid)}
    (work / f"qualification-{a.film}.json").write_text(json.dumps(report, indent=1, default=str, ensure_ascii=False))
    tgt = [m for m in matches if m["target"]]
    print(json.dumps({"film": a.film, "live": a.live, "verdict": review.get("verdict"), "defects_reported": len(review.get("defects", [])),
                      "targets_proposed_found": sum(1 for m in tgt if m["proposed_reviewer_defects"]), "of": len(tgt),
                      "spent_usd": str(report["ledger"].get("committed_usd")), "report": str(work / f"qualification-{a.film}.json")}, indent=1))


if __name__ == "__main__":
    main()
